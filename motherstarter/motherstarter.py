#!bin/bash/python3
"""
This application is used to take source file(s) and translate them to
produce outputs in various file formats. Those file formats can then be
used to perform network automation tasks.
"""

# Import modules
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pathlib as pl
from colorama import init  # type: ignore
from logging import Logger
import logging
import click
from typing import Optional, TextIO, Union, List, Dict, Any
from motherstarter import __version__
import os
import sys


# Get path of the current dir under which the file is executed
dirname = os.path.dirname(os.path.abspath(__file__))
# Append sys path so that relative pathing works for input
# files and templates
sys.path.append(os.path.join(dirname))

# Auto-reset colorama colours back after each print statement
init(autoreset=True)


# This block of code initialises motherstarter from the command
# line
@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """
    Function to initialise motherstarter from the command line.

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A
    """
    pass


@cli.command()
@click.option(
    "--log-level",
    "-l",
    help="Specify the logging level.",
    default="debug",
    type=click.Choice(
        ["debug", "info", "warning", "error", "critical"], case_sensitive=False
    ),
    show_default=True,
)
@click.option(
    "--source-type",
    "-st",
    help="Specify the source file type.",
    default="json",
    type=click.Choice(["csv", "json", "xlsx"], case_sensitive=False),
    show_default=True,
)
@click.option(
    "--source-dir",
    "-sd",
    help="Specify the source directory for the source files.",  # noqa (pylama ignore)
    default="motherstarter/inputs/",
    show_default=True,
)
@click.option(
    "--template-dir",
    "-td",
    help="Specify the template directory for the template files.",  # noqa (pylama ignore)
    default="motherstarter/templates/core/",
    show_default=True,
)
@click.option(
    "--output-type",
    "-o",
    help="Specify the output file types.  This argument only takes one option.",
    default="all",
    type=click.Choice(
        ["all", "ansible", "csv", "json", "nornir", "pyats", "xlsx"],
        case_sensitive=False,
    ),
    show_default=True,
)
def convert(
    log_level: str,
    source_type: str,
    source_dir: str,
    template_dir: str,
    output_type: str,
) -> None:
    """
    Convert source file(s) into network automation inventory outputs
    based on multiple command-line inputs.

    For example:
        Input type: json
        Output type: nornir

    Args:\n
        log_level: The severity logging level for all events. Valid
        options: "debug", "info", "warning", "error" and "critical".
        source_type: The source file type to read the inventory/group
        data from. Valid options: "csv", "json" and "xlsx".\n
        source_dir: The source directory to find the files in.\n
        template_dir: The template directory to find the templates in.\n
        output_type: What file type(s) you would like to be outputted
        as a result of running the function. Valid options: "all", "ansible",
        "csv", "json", "nornir", "pyats" and "xlsx".\n

    Returns:
        N/A

    Raises:
        N/A
    """
    # Convert log level to an upper-case variable
    ll = log_level.upper()
    # Rename the other inputs for usage below
    st = source_type
    ot = output_type
    # If/else block to handle using when the user
    # doesn't specify a template_dir from the command-line
    # If the default value is triggered at this point
    if template_dir == "motherstarter/templates/core/":
        # Assign the td variable by joining it with the
        # absolute path of the file + the default template_dir
        td = os.path.join(dirname, "templates/core/")
    else:
        # If the user supplies something, use that instead.
        td = template_dir
    # If/else block to handle using when the user
    # doesn't specify a source_dir from the command-line
    # If the default value is triggered at this point
    if source_dir == "motherstarter/inputs/":
        # Assign the td variable by joining it with the
        # absolute path of the file + the default source_dir
        sd = os.path.join(dirname, "inputs/")
    else:
        # If the user supplies something, use that instead.
        sd = source_dir
    # Initialise the logger
    logger = init_logger(log_level=ll, log_name="motherstarter.log")
    # Initialise the main workflow
    main(logger=logger, source_type=st, output_type=ot, source_dir=sd, template_dir=td)


def init_logger(log_level: str, log_name: str = "ms.log") -> Logger:
    """
    Initialise a logger object, to be used to perform logging
    and console outputs to the screen.
    The log_level is passed into the function and used to set
    the logging level.

    Args:
        log_level: The severity logging level for all events
        log_name: The name of the log file.

    Returns:
        logger: An initialised Logger object

    Raises:
        N/A
    """
    # Create a logger object
    logger = logging.getLogger(__name__)
    # Setup the logging formatters for log and stream outputs
    log_fmt = logging.Formatter("%(asctime)s - " "%(levelname)s - " "%(message)s")
    stream_fmt = logging.Formatter("%(levelname)s - " "%(message)s")
    # Setup file handler and use a different log format for output
    f_handler = logging.FileHandler(log_name)
    f_handler.setFormatter(log_fmt)
    # Setup stream handler and use a different log format for output
    s_handler = logging.StreamHandler()
    s_handler.setFormatter(stream_fmt)
    # Create a dictionary of log_level mappings
    logger_map = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    # Set logging level based on the log_level
    # taken from the user using argparse and the log_level dictionary map above
    # NOTE: This will be an integer value
    # https://docs.python.org/3/library/logging.html#logging-levels
    log_integer = logger_map.get(log_level)
    logger.setLevel(level=log_integer)  # type: ignore
    f_handler.setLevel(level=log_integer)  # type: ignore
    s_handler.setLevel(level=log_integer)  # type: ignore
    # Add these handlers to the logger objects
    logger.addHandler(f_handler)
    logger.addHandler(s_handler)
    return logger


def init_inventory(
    logger: Logger, source_dir: str = "", source_type: str = "json"
) -> pd.DataFrame:
    """
    Initialise the inventory data based on the source_type and from the source
    directory and return a pandas dataframe object.

    Args:
        logger: The initialised Logger object.
        source_dir: The source directory to find the files in.
        source_type: The source file type to read the inventory data from.

    Returns:
        df: The pandas dataframe object for further processing.

    Raises:
        ValueError: When a non-valid input is specified.
    """
    # Provide debugging output if needed.
    logger.debug(f"Inventory source type is {source_type}")
    # If/Else block to execute the applicable function, based on the
    # source file type
    if source_type == "json":
        # Execute the JSON specific init inventory
        df = init_inventory_json(source_dir)
    elif source_type == "xlsx":
        # Execute the xlsx specific init inventory
        df = init_inventory_xlsx(source_dir)
    elif source_type == "csv":
        # Execute the xlsx specific init inventory
        df = init_inventory_csv(source_dir)
    else:
        # Output and raise ValueError error. NOTE: Due to using argparse options, we should
        # never hit this error but just in case we do.
        invalid_error = f"Source Type: {source_type} not supported..."
        logger.error(invalid_error)
        raise ValueError(invalid_error)
    # Return the df object
    return df


def init_groups(
    logger: Logger, source_dir: str = "", source_type: str = "json"
) -> pd.DataFrame:
    """
    Initialise the group data based on the source_type and from the source
    directory and return a pandas dataframe object

    Args:
        logger: The initialised logger object
        source_dir: The source directory to find the inventory files in.
        source_type: The source file type to read the group data from.

    Returns:
        df: The pandas dataframe object for further processing.

    Raises:
        ValueError: When a non-valid input is specified.
    """
    # Provide debugging output if needed.
    logger.debug(f"Inventory source type is {source_type}")
    # If/Else block to execute the applicable function, based on the
    # source file type
    if source_type == "json":
        # Execute the JSON specific init group
        df = init_groups_json(source_dir)
    elif source_type == "xlsx":
        # Execute the xlsx specific init group
        df = init_groups_xlsx(source_dir)
    elif source_type == "csv":
        # Execute the csv specific init group
        df = init_groups_csv(source_dir)
    else:
        # Output and raise ValueError error. NOTE: Due to using argparse options, we should
        # never hit this error but just in case we do.
        invalid_error = f"Source Type: {source_type} not supported..."
        logger.error(invalid_error)
        raise ValueError(invalid_error)
    # Return the df object
    return df


def init_inventory_json(
    source_dir: Optional[str] = "motherstarter/inputs",
) -> Union[pd.DataFrame, Any]:
    """
    Initialise a pandas dataframe by using pandas read_json
    function by reading in the "inventory.json" file from the
    applicable source directory

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'motherstarter/inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.

    Args:
        source_dir: The source directory to find the inventory files in.

    Returns:
        df: The pandas dataframe object for further processing.

    Raises:
        N/A
    """
    # Return dataframe
    return pd.read_json(f"{source_dir}/inventory.json")


def init_inventory_xlsx(
    source_dir: Optional[str] = "motherstarter/inputs",
) -> Union[pd.DataFrame, Any]:
    """
    Initialise a pandas dataframe by using pandas read_excel
    function by reading in the "inventory.xlsx" file from the
    applicable source directory

    Args:
        source_dir: The source directory to find the inventory files in.

    Returns:
        df: The pandas dataframe object for further processing.

    Raises:
        N/A
    """
    # Return dataframe
    return pd.read_excel(  # type: ignore
        f"{source_dir}/inventory.xlsx", sheet_name="inventory", engine="openpyxl"
    )


def init_inventory_csv(
    source_dir: Optional[str] = "motherstarter/inputs",
) -> pd.DataFrame:
    """
    Initialise a pandas dataframe by using pandas read_csv
    function by reading in the "inventory.csv" file from the
    applicable source directory


    Args:
        source_dir: The source directory to find the inventory files in.

    Returns:
        df: The pandas dataframe object for further processing.

    Raises:
        N/A
    """
    # Return dataframe
    return pd.read_csv(f"{source_dir}/inventory.csv")


def init_groups_json(
    source_dir: Optional[str] = "motherstarter/inputs",
) -> Union[pd.DataFrame, Any]:
    """
    Initialise a pandas dataframe by using pandas read_json
    function by reading in the "groups.json" file from the
    applicable source directory

    Args:
        source_dir: The source directory to find the inventory files in.

    Returns:
        df: The pandas dataframe object for further processing.

    Raises:
        N/A
    """
    # Return dataframe
    return pd.read_json(f"{source_dir}/groups.json")


def init_groups_xlsx(
    source_dir: Optional[str] = "motherstarter/inputs",
) -> Union[pd.DataFrame, Any]:
    """
    Initialise a pandas dataframe by using pandas read_excel
    function by reading in the "groups.xlsx" file from the
    applicable source directory

    Args:
        source_dir: The source directory to find the inventory files in.

    Returns:
        df: The pandas dataframe object for further processing.

    Raises:
        N/A
    """
    # Return dataframe
    return pd.read_excel(  # type: ignore
        f"{source_dir}/groups.xlsx", sheet_name="groups", engine="openpyxl"
    )


def init_groups_csv(source_dir: Optional[str] = "motherstarter/inputs") -> pd.DataFrame:
    """
    Initialise a pandas dataframe by using pandas read_csv
    function by reading in the "groups.csv" file from the
    applicable source directory

    Args:
        source_dir: The source directory to find the inventory files in.

    Returns:
        df: The pandas dataframe object for further processing.

    Raises:
        N/A
    """
    return pd.read_csv(f"{source_dir}/groups.csv")


def dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Helper function to return a Pandas dataframe into
    a dictionary so that it can be used for further
    processing throughout the application

    Args:
        df: The pandas dataframe object.

    Returns:
        df: A list of dictionaries of the dataframe object.

    Raises:
        N/A
    """
    return df.to_dict(orient="records")


def prep_templates(
    tmpl_dir: Any = "motherstarter/templates/outputs/core",
) -> Environment:
    """
    Take the template directory and load a Jinja2 environment
    with those templates and other settings enabled

    For example:
     .
     |
     └── templates
            └── core
                └── outputs <---- Set tmpl_dir to here
                    ├── pyats
                    │     └── testbed.j2
                    └── nornir
                        ├── hosts.j2
                        └── groups.j2

    NOTE: Whilst this function exposes the ability to change the tmpl_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the
    'motherstarter/templates/outputs/core' directory. We would recommend just sticking with
    that, unless you want to write your own custom workflow.

    Args:
        tmpl_dir: The template directory one-level above where the Jinja2
    templates are stored.

    Returns:
        env: The loaded jinja2 environment.

    Raises:
        N/A
    """
    # Load template directory where Jinja2 templates are located
    templates = FileSystemLoader(tmpl_dir)
    return Environment(
        loader=templates, autoescape=True, trim_blocks=True, lstrip_blocks=True
    )


def to_nr_hosts(
    logger: Logger, env: Environment, df: pd.DataFrame, output_dir: str = ""
) -> TextIO:
    """
    Take the pandas dataframe, convert it to a dictionary
    and render that dictionary through a Jinja2 template to
    create an nornir hosts inventory file.

    Args:
        logger: The initialised Logger object.
        env: The loaded Jinja2 environment, used to retrieve
        templates from.
        df: The pandas dataframe object, initialised from the
        inventory data source
        output_dir: The output directory.

    Returns:
        nr_h_file : The nornir hosts file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/nr/inventory"
    # # Temp hack TODO
    # output_dir = "motherstarter/outputs/nr/inventory"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Convert pandas dataframe to a dictionary and assign to the
    # 'inv' variable
    inv = dataframe_to_dict(df)
    # Get template and assign to a variable
    template = env.get_template("nornir/hosts.j2")
    # Render inventory dictionary through a template and assign and output
    # to a variable
    output = template.render(inventory=inv)
    # Create file and write contents to file
    with open(f"{output_dir}/hosts.yaml", "w+") as nr_h_file:
        nr_h_file.write(output)
    # Log diagnostic information
    logger.info(f"File output location: {nr_h_file.name}")
    return nr_h_file


def to_nr_groups(
    logger: Logger, env: Environment, df: pd.DataFrame, output_dir: str = ""
) -> TextIO:
    """
    Take the pandas dataframe, convert it to a dictionary
    and render that dictionary through a Jinja2 template to
    create an nornir groups inventory file.

    Args:
        logger: The initialised Logger object.
        env: The loaded Jinja2 environment, used to retrieve
        templates from.
        df: The pandas dataframe object, initialised from the
        inventory data source.
        output_dir: The output directory.

    Returns:
        nr_g_file: The nornir groups file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/nr/inventory"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Convert pandas dataframe to a dictionary and assign to the
    # 'grp' variable
    grp = dataframe_to_dict(df)
    # Get template and assign to a variable
    template = env.get_template("nornir/groups.j2")
    # Render groups dictionary through a template and assign and output
    # to a variable
    output = template.render(groups=grp)
    # Create file and write contents to file
    with open(f"{output_dir}/groups.yaml", "w+") as nr_g_file:
        nr_g_file.write(output)
    # Log diagnostic information
    logger.info(f"File output location: {nr_g_file.name}")
    return nr_g_file


def to_pyats(
    logger: Logger, env: Environment, df: pd.DataFrame, output_dir: str = ""
) -> TextIO:
    """
    Take the pandas dataframe, convert it to a dictionary
    and render that dictionary through a Jinja2 template to
    create an pyATS testbed file.

    Args:
        logger: The initialised Logger object.
        env : The loaded Jinja2 environment, used to retrieve
        templates from.
        df: The pandas dataframe object, initialised from the
        inventory data source.
        output_dir: The output directory.

    Returns:
        tb_file : The pyATS testbed file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/pyats"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Convert pandas dataframe to a dictionary and assign to the
    # 'inv' variable
    inv = dataframe_to_dict(df)
    # Get template and assign to a variable
    template = env.get_template("pyats/testbed.j2")
    # Render inventory dictionary through a template and assign and output
    # to a variable
    output = template.render(inventory=inv)
    # Create file and write contents to file
    with open(f"{output_dir}/mother_starter_tb.yaml", "w+") as tb_file:
        tb_file.write(output)
    # Log diagnostic information
    logger.info(f"File output location: {tb_file.name}")
    return tb_file


def to_csv_inventory(logger: Logger, df: pd.DataFrame, output_dir: str = "") -> str:
    """
    Take the pandas dataframe and save it to a CSV file.

    Args:
        logger: The initialised Logger object.
        df: The pandas dataframe object, initialised from the
        inventory data source
        output_dir: The output directory.

    Returns:
        csv_file: The CSV file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/csv"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign CSV file name to a variable
    csv_file = f"{output_dir}/inventory.csv"
    # Output the dataframe to CSV, save in CSV file
    df.to_csv(csv_file, index=False)
    # Log diagnostic information
    logger.info(f"File output location: {csv_file}")
    return csv_file


def to_xlsx_inventory(logger: Logger, df: pd.DataFrame, output_dir: str = "") -> str:
    """
    Take the pandas dataframe and save it to a xlsx file.

    Args:
        logger: The initialised Logger object.
        df: The pandas dataframe object, initialised from the
        inventory data source.
        output_dir: The output directory.

    Returns:
        xlsx_file: The xlsx file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/xlsx"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign xlsx file name to a variable
    xlsx_file = f"{output_dir}/inventory.xlsx"
    # Output the dataframe to Excel, save in xlsx file
    df.to_excel(xlsx_file, index=False, sheet_name="inventory")  # type: ignore
    # Log diagnostic information
    logger.info(f"File output location: {xlsx_file}")
    return xlsx_file


def to_json_inventory(logger: Logger, df: pd.DataFrame, output_dir: str = "") -> str:
    """
    Take the pandas dataframe and save it to a json file.

    Args:
        logger: The initialised Logger object.
        df: The pandas dataframe object, initialised from the
        inventory data source
        output_dir: The output directory.

    Returns:
        json_file: The json file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/json"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign json file name to a variable
    json_file = f"{output_dir}/inventory.json"
    # Output the dataframe to json, save in json file
    df.to_json(json_file, indent=4, orient="records")  # type: ignore
    # Log diagnostic information
    logger.info(f"File output location: {json_file}")
    return json_file


def to_csv_groups(logger: Logger, df: pd.DataFrame, output_dir: str = "") -> str:
    """
    Take the pandas dataframe and save it to a CSV file.

    Args:
        logger: The initialised Logger object.
        df: The pandas dataframe object, initialised from the
        inventory data source
        output_dir: The output directory.

    Returns:
        csv_file: The CSV file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/csv"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign CSV file name to a variable
    csv_file = f"{output_dir}/groups.csv"
    # Output the dataframe to CSV, save in CSV file
    df.to_csv(csv_file, index=False)
    # Log diagnostic information
    logger.info(f"File output location: {csv_file}")
    return csv_file


def to_xlsx_groups(logger: Logger, df: pd.DataFrame, output_dir: str = "") -> str:
    """
    Take the pandas dataframe and save it to a xlsx file.

    Args:
        logger: The initialised Logger object.
        df: The pandas dataframe object, initialised from the
        inventory data source.
        output_dir: The output directory.

    Returns:
        xlsx_file: The xlsx file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/xlsx"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign xlsx file name to a variable
    xlsx_file = f"{output_dir}/groups.xlsx"
    # Output the dataframe to Excel, save in xlsx file
    df.to_excel(xlsx_file, index=False, sheet_name="groups")  # type: ignore
    # Log diagnostic information
    logger.info(f"File output location: {xlsx_file}")
    return xlsx_file


def to_json_groups(logger: Logger, df: pd.DataFrame, output_dir: str = "") -> str:
    """
    Take the pandas dataframe and save it to a json file.

    Args:
        logger: The initialised Logger object.
        df: The pandas dataframe object, initialised from the
        inventory data source
        output_dir: The output directory.

    Returns:
        json_file: The json file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/json"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign json file name to a variable
    json_file = f"{output_dir}/groups.json"
    # Output the dataframe to json, save in json file
    df.to_json(json_file, indent=4, orient="records")  # type: ignore
    # Log diagnostic information
    logger.info(f"File output location: {json_file}")
    return json_file


def to_ansible(
    logger: Logger, env: Environment, df: pd.DataFrame, output_dir: str = ""
) -> TextIO:
    """
    Take the pandas dataframe, convert it to a dictionary
    and render that dictionary through a Jinja2 template to
    create an Ansible inventory file.

    Args:
        logger: The initialised Logger object.
        env: The loaded Jinja2 environment, used to retrieve
        templates from.
        df: The pandas dataframe object, initialised from the
        inventory data source
        output_dir: The output directory.

    Returns:
        ans_h_file : The Ansible inventory file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if not output_dir:
        output_dir = "motherstarter/outputs/ansible/inventory"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Convert pandas dataframe to a dictionary and assign to the
    # 'inv' variable
    inv = dataframe_to_dict(df)
    # Get template and assign to a variable
    template = env.get_template("ansible/hosts.j2")
    # Render groups dictionary through a template and assign and output
    # to a variable
    output = template.render(inventory=inv)
    # Create file and write contents to file
    with open(f"{output_dir}/hosts", "w+") as ans_h_file:
        ans_h_file.write(output)
    # Log diagnostic information
    logger.info(f"File output location: {ans_h_file.name}")
    return ans_h_file


def main(
    logger: Logger,
    source_type: str,
    output_type: str,
    source_dir: str = "motherstarter/inputs/",
    template_dir: str = "motherstarter/templates/core/",
) -> None:
    """
    Main workflow function used to execute the entire workflow

    Args:
        logger: The initialised Logger object.
        source_type: The source file type to read the inventory
        and group data in from.
        output_type: What file type(s) you would like to be outputted
        as a result of running the function.
        source_dir: The source directory of the input files.
        template_dir: The template directory of the template files.
    Returns:
        N/A

    Raises:
        N/A
    """
    # Debug logging
    logger.debug(f"Source directory is: {source_dir}")
    logger.debug(f"Source template directory is: {template_dir}")
    # Initialise inventory dataframe, based on the source_dir and source_type
    inv_df = init_inventory(
        logger=logger, source_dir=source_dir, source_type=source_type
    )
    # Initialise group dataframe, based on the source_dir and source_type
    group_df = init_groups(
        logger=logger, source_dir=source_dir, source_type=source_type
    )
    # Prepare the jinja2 template environment
    env = prep_templates(tmpl_dir=template_dir)
    # Diagnostic outputs
    logger.debug(f"Output type is: {output_type}")
    # If/Else block to execute the desired output_type based on
    # what is passed in from argparse
    # If output type is all, output all file types
    if output_type == "all":
        to_nr_hosts(logger=logger, env=env, df=inv_df)
        to_nr_groups(logger=logger, env=env, df=group_df)
        to_csv_inventory(logger=logger, df=inv_df)
        to_xlsx_inventory(logger=logger, df=inv_df)
        to_csv_groups(logger=logger, df=group_df)
        to_xlsx_groups(logger=logger, df=group_df)
        to_pyats(logger=logger, env=env, df=inv_df)
        to_ansible(logger=logger, env=env, df=inv_df)
        to_json_inventory(logger=logger, df=inv_df)
        to_json_groups(logger=logger, df=group_df)
    # If output type is nornir, output all nornir types
    elif output_type == "nornir":
        to_nr_hosts(logger=logger, env=env, df=inv_df)
        to_nr_groups(logger=logger, env=env, df=group_df)
    # If output type is csv, output all CSV types
    elif output_type == "csv":
        to_csv_inventory(logger=logger, df=inv_df)
        to_csv_groups(logger=logger, df=group_df)
    # If output type is xlsx, output all xlsx types
    elif output_type == "xlsx":
        to_xlsx_inventory(logger=logger, df=inv_df)
        to_xlsx_groups(logger=logger, df=group_df)
    # If output type is pyats, output all pyATS types
    elif output_type == "pyats":
        to_pyats(logger=logger, env=env, df=inv_df)
    # If output type is ansible, output all ansible types
    elif output_type == "ansible":
        to_ansible(logger=logger, env=env, df=inv_df)
    # If output type is json, output all ansible types
    elif output_type == "json":
        to_json_inventory(logger=logger, df=inv_df)
        to_json_groups(logger=logger, df=group_df)


if __name__ == "__main__":
    # Initialise click from the command-line
    cli()  # pragma: no cover (ignore pytest)
