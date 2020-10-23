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
from colorama import init
import logging
import argparse
import click


# Auto-reset colorama colours back after each print statement
init(autoreset=True)
# Set global logger variable as blank
logger = ""


def set_global_logger_var(log):
    """
    This is a hack to ser the log variable
    as an to the global variable to save passing around
    all the functions. TODO: This should be reviewed.

    Args:
        log: The initialised log variable

    Returns:
        N/A

    Raises:
        N/A

    """
    # Access the global logger variable
    global logger
    # Override it with what is passed into the variable
    logger = log


# This block of code initialises motherstarter from the command
# line
@click.group()
@click.version_option(version="0.0.1")
def ms():
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


@ms.command()
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
    help="Specify the source directory for the source files. Default is tree structure under the 'inputs/' folder.",
    default=None,
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
def convert(log_level: str, source_type: str, source_dir: str, output_type: str):
    """
    Convert source file(s) into network automation inventory outputs
    based on multiple command-line inputs.

    For example:
        Input type: json
        Output type: nornir

    Args:\n
        log_level (str): The severity logging level for all events. Valid
        options: "debug", "info", "warning", "error" and "critical".
        source_type (str): The source file type to read the inventory/group
        data from. Valid options: "csv", "json" and "xlsx".\n
        source_dir (str): The source directory to find the files in.\n
        output_type (str): What file type(s) you would like to be outputted
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
    # TODO: Refactor this temp code.
    sd = source_dir
    print(sd)
    # Initialise the logger
    logger = init_logger(log_level=ll, log_name="motherstarter.log")
    # TODO: This is a hack to override the global logger variable
    # Yes, this is not cool
    set_global_logger_var(logger)
    # Initialise the main workflow
    main(source_type=st, output_type=ot, logger=logger)


def get_argparse_args():
    """
    Take argparse parameter(s) off user input from a command
    line and return those outputs for usage in other functions.

    Args:
        N/A

    Returns:
        arg_outputs: Dictionary of argument outputs which can be
        used for other functions.
            level: The logging level set at the command line.
            source: The source type set at the command line.
            output: The output type set at the command line.

    Raises:
        N/A

    """
    # Setup argparse parameters to take user input from the command line
    parser = argparse.ArgumentParser(
        description="Translate source file(s) into network automation inventory outputs"
    )
    # Setup argparse arguments to take user input from the command line
    parser.add_argument(
        "-l",
        "--log",
        dest="logging_level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="debug",
        help="Specify the logging level. Default is debug.",
    )
    parser.add_argument(
        "-st",
        "--source-type",
        dest="source_type",
        choices=["csv", "json", "xlsx"],
        default="json",
        help="Specify the source file type. Default is json.",
    )
    parser.add_argument(
        "-sd",
        "--source-dir",
        dest="source_dir",
        default=None,
        help="Specify the source directory for the source files. Default is tree structure under the 'inputs/' folder.",
    )
    parser.add_argument(
        "-o",
        "--output-type",
        choices=["all", "csv", "json", "nornir", "pyats", "xlsx"],
        dest="output_type",
        default="all",
        help="Specify the output file types. Default is all file types. This argument only takes one option.",
    )
    args = parser.parse_args()
    # Take log_level argument, assign to var and turn into uppercase
    log_level = args.logging_level.upper()
    # Take source_type and output_type arguments and assign to a variable
    source_type, output_type = args.source_type, args.output_type
    # Assign outputs to a dict, so they can be reliably used outside this function
    arg_outputs = {"level": log_level, "source": source_type, "output": output_type}
    return arg_outputs


def init_logger(log_level: str, log_name: str = "ms.log"):
    """
    Initialise a logger object, to be used to perform logging
    and console outputs to the screen.
    The log_level is passed into the function and used to set
    the logging level.

    Args:
        log_level (str): The severity logging level for all events
        log_name (str): The name of the log file. Default "ms.log"

    Returns:
        logger: An initialised logger object

    Raises:
        N/A

    """
    # Create a logger object
    logger = logging.getLogger(__name__)
    # Setup the logging formatters for log and stream outputs
    log_fmt = logging.Formatter(("%(asctime)s - " "%(levelname)s - " "%(message)s"))
    stream_fmt = logging.Formatter(("%(levelname)s - " "%(message)s"))
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
    logger.setLevel(level=log_integer)
    f_handler.setLevel(level=log_integer)
    s_handler.setLevel(level=log_integer)
    # Add these handlers to the logger objects
    logger.addHandler(f_handler)
    logger.addHandler(s_handler)
    return logger


def init_inventory(source_dir: str = None, source_type: str = "json"):
    """
    Initialise the inventory data based on the source_type and from the source
    directory and return a pandas dataframe object.

    Args:
        source_dir (str): The source directory to find the files in.
        source_type (str): The source file type to read the inventory data from.
        Default: "json".

    Returns:
        df (?): The pandas dataframe object for further processing.

    Raises:
        N/A

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
        # Output an error. NOTE: Due to using argparse options, we should
        # never hit this error but just in case we do.
        logger.error(f"Source Type: {source_type} not supported...")
        # Set df to None
        df = None
    # Return the df object
    return df


def init_groups(source_dir: str = None, source_type: str = "json"):
    """
    Initialise the group data based on the source_type and from the source
    directory and return a pandas dataframe object

    Args:
        source_dir (str): The source directory to find the inventory files in.
        Default: None
        source_type (str): The source file type to read the group data from.
        Default: "json"

    Returns:
        df (?): The pandas dataframe object for further processing.

    Raises:
        N/A

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
        # Output an error. NOTE: Due to using argparse options, we should
        # never hit this error but just in case we do.
        logger.error(f"Source Type: {source_type} not supported...")
        # Set df to None
        df = None
    # Return the df object
    return df


def init_inventory_json(source_dir: str = None):  # Make this required at this level
    """
    Initialise a pandas dataframe by using pandas read_json
    function by reading in the "inventory.json" file from the
    applicable source directory

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.

    Args:
        source_dir (str): The source directory to find the inventory files in.
        Default: None

    Returns:
        df (?): The pandas dataframe object for further processing.

    Raises:
        N/A


    """
    # Specify the source dirs for inputs when it is not supplied
    if source_dir is None:
        source_dir = "inputs/inventory/json"
    # Read in source file. NOTE: The source filename is hardcoded
    df = pd.read_json(f"{source_dir}/inventory.json")
    # Return dataframe
    return df


def init_inventory_xlsx(source_dir: str = None):
    """
    Initialise a pandas dataframe by using pandas read_excel
    function by reading in the "inventory.xlsx" file from the
    applicable source directory

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.

    Args:
        source_dir (str): The source directory to find the inventory files in.
        Default: None

    Returns:
        df (?): The pandas dataframe object for further processing.

    Raises:
        N/A

    """
    # Specify the source dirs for inputs when it is not supplied
    if source_dir is None:
        source_dir = "inputs/inventory/xlsx"
    # Read in source file. NOTE: The source filename and sheet name are hardcoded
    df = pd.read_excel(f"{source_dir}/inventory.xlsx", sheet_name="inventory")
    # Return dataframe
    return df


def init_inventory_csv(source_dir: str = None):
    """
    Initialise a pandas dataframe by using pandas read_csv
    function by reading in the "inventory.csv" file from the
    applicable source directory

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.

    Args:
        source_dir (str): The source directory to find the inventory files in.
        Default: None

    Returns:
        df (?): The pandas dataframe object for further processing.

    Raises:
        N/A

    """
    # Specify the source dirs for inputs when it is not supplied
    if source_dir is None:
        source_dir = "inputs/inventory/csv"
    # Read in source file. NOTE: The source filename is hardcoded
    df = pd.read_csv(f"{source_dir}/inventory.csv")
    # Return dataframe
    return df


def init_groups_json(source_dir: str = None):
    """
    Initialise a pandas dataframe by using pandas read_json
    function by reading in the "groups.json" file from the
    applicable source directory

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.

    Args:
        source_dir (str): The source directory to find the inventory files in.
        Default: None

    Returns:
        df (?): The pandas dataframe object for further processing.

    Raises:
        N/A

    """
    # Specify the source dirs for inputs when it is not supplied
    if source_dir is None:
        source_dir = "inputs/groups/json"
    # Read in source file. NOTE: The source filename is hardcoded
    df = pd.read_json(f"{source_dir}/groups.json")
    # Return dataframe
    return df


def init_groups_xlsx(source_dir: str = None):
    """
    Initialise a pandas dataframe by using pandas read_excel
    function by reading in the "groups.xlsx" file from the
    applicable source directory

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.

    Args:
        source_dir (str): The source directory to find the inventory files in.
        Default: None

    Returns:
        df (?): The pandas dataframe object for further processing.

    Raises:
        N/A

    """
    # Specify the source dirs for inputs when it is not supplied
    if source_dir is None:
        source_dir = "inputs/groups/xlsx"
    # Read in source file. NOTE: The source filename and sheet name are hardcoded
    df = pd.read_excel(f"{source_dir}/groups.xlsx", sheet_name="groups")
    # Return dataframe
    return df


def init_groups_csv(source_dir: str = None):
    """
    Initialise a pandas dataframe by using pandas read_csv
    function by reading in the "groups.csv" file from the
    applicable source directory

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.

    Args:
        source_dir (str): The source directory to find the inventory files in.
        Default: None

    Returns:
        df (?): The pandas dataframe object for further processing.

    Raises:
        N/A

    """
    # Specify the source dirs for inputs when it is not supplied
    if source_dir is None:
        source_dir = "inputs/groups/csv"
    # Read in source file. NOTE: The source filename is hardcoded
    df = pd.read_csv(f"{source_dir}/groups.csv")
    return df


def dataframe_to_dict(df) -> list:
    """
    Helper function to return a Pandas dataframe into
    a dictionary so that it can be used for further
    processing throughout the application

    Args:
        df (?): The pandas dataframe object.

    Returns:
        df (list): A list of dictionaries of the dataframe object.

    Raises:
        N/A
    """
    return df.to_dict(orient="records")


def prep_templates(tmpl_dir: str = None):
    """
    Take the template directory and load a Jinja2 environment
    with those templates and other settings enabled

    For example:
     .
     |
     └── templates
        └── outputs <---- Set tmpl_dir to here
            ├── pyats
            │     └── testbed.j2
            └── nornir
                  ├── hosts.j2
                  └── groups.j2

    NOTE: Whilst this function exposes the ability to change the tmpl_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the
    'templates/outputs/' directory. We would recommend just sticking with
    that, unless you want to write your own custom workflow.

    Args:
        tmpl_dir (str): The template directory one-level above where the Jinja2
    templates are stored. Default: None

    Returns:
        env (?):  The loaded jinja2 environment.

    Raises:
        N/A
    """
    # Specify the template dirs when it is not supplied
    if tmpl_dir is None:
        tmpl_dir = "templates/outputs"
    # Load template directory where Jinja2 templates are located
    templates = FileSystemLoader(tmpl_dir)
    # Load environment and setting autoescape to True
    # to prevent XSS attacks
    env = Environment(
        loader=templates, autoescape=True, trim_blocks=True, lstrip_blocks=True
    )
    return env


def to_nr_hosts(env, df, output_dir: str = None):
    """
    Take the pandas dataframe, convert it to a dictionary
    and render that dictionary through a Jinja2 template to
    create an nornir hosts inventory file.

    Args:
        env (?): The loaded Jinja2 environment, used to retrieve
        templates from.
        df (?): The pandas dataframe object, initialised from the
        inventory data source
        output_dir (str): The output directory. Default: None.

    Returns:
        nr_h_file (?): The nornir hosts file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/nr/inventory"
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


def to_nr_groups(env, df, output_dir: str = None):
    """
    Take the pandas dataframe, convert it to a dictionary
    and render that dictionary through a Jinja2 template to
    create an nornir groups inventory file.

    Args:
        env (?): The loaded Jinja2 environment, used to retrieve
        templates from.
        df (?): The pandas dataframe object, initialised from the
        inventory data source.
        output_dir (str): The output directory. Default: None.

    Returns:
        nr_g_file: The nornir groups file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/nr/inventory"
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


def to_pyats(env, df, output_dir: str = None):
    """
    Take the pandas dataframe, convert it to a dictionary
    and render that dictionary through a Jinja2 template to
    create an pyATS testbed file.

    Args:
        env (?): The loaded Jinja2 environment, used to retrieve
        templates from.
        df (?): The pandas dataframe object, initialised from the
        inventory data source.
        output_dir (?): The output directory. Default: None

    Returns:
        tb_file (?): The pyATS testbed file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/pyats"
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


def to_csv_inventory(df, output_dir: str = None):
    """
    Take the pandas dataframe and save it to a CSV file.

    Args:
        df (?): The pandas dataframe object, initialised from the
        inventory data source
        output_dir (str): The output directory. Default: None.

    Returns:
        csv_file (?): The CSV file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/csv"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign CSV file name to a variable
    csv_file = f"{output_dir}/inventory.csv"
    # Output the dataframe to CSV, save in CSV file
    df.to_csv(csv_file, index=False)
    # Log diagnostic information
    logger.info(f"File output location: {csv_file}")
    return csv_file


def to_xlsx_inventory(df, output_dir: str = None):
    """
    Take the pandas dataframe and save it to a xlsx file.

    Args:
        df (?): The pandas dataframe object, initialised from the
    inventory data source.
        output_dir (?): The output directory.

    Returns:
        xlsx_file (?): The xlsx file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/xlsx"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign xlsx file name to a variable
    xlsx_file = f"{output_dir}/inventory.xlsx"
    # Output the dataframe to Excel, save in xlsx file
    df.to_excel(xlsx_file, index=False, sheet_name="inventory")
    # Log diagnostic information
    logger.info(f"File output location: {xlsx_file}")
    return xlsx_file


def to_json_inventory(df, output_dir: str = None):
    """
    Take the pandas dataframe and save it to a json file.

    Args:
        df (?): The pandas dataframe object, initialised from the
        inventory data source
        output_dir (?): The output directory. Default: None.

    Returns:
        json_file (?): The json file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/json"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign json file name to a variable
    json_file = f"{output_dir}/inventory.json"
    # Output the dataframe to json, save in json file
    df.to_json(json_file, indent=4, orient="records")
    # Log diagnostic information
    logger.info(f"File output location: {json_file}")
    return json_file


def to_csv_groups(df, output_dir: str = None):
    """
    Take the pandas dataframe and save it to a CSV file.

    Args:
        df (?): The pandas dataframe object, initialised from the
        inventory data source
        output_dir (str): The output directory. Default: None.

    Returns:
        csv_file (?): The CSV file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/csv"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign CSV file name to a variable
    csv_file = f"{output_dir}/groups.csv"
    # Output the dataframe to CSV, save in CSV file
    df.to_csv(csv_file, index=False)
    # Log diagnostic information
    logger.info(f"File output location: {csv_file}")
    return csv_file


def to_xlsx_groups(df, output_dir: str = None):
    """
    Take the pandas dataframe and save it to a xlsx file.

    Args:
        df (?): The pandas dataframe object, initialised from the
    inventory data source.
        output_dir (?): The output directory.

    Returns:
        xlsx_file (?): The xlsx file object.


    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/xlsx"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign xlsx file name to a variable
    xlsx_file = f"{output_dir}/groups.xlsx"
    # Output the dataframe to Excel, save in xlsx file
    df.to_excel(xlsx_file, index=False, sheet_name="groups")
    # Log diagnostic information
    logger.info(f"File output location: {xlsx_file}")
    return xlsx_file


def to_json_groups(df, output_dir: str = None):
    """
    Take the pandas dataframe and save it to a json file.

    Args:
        df (?): The pandas dataframe object, initialised from the
        inventory data source
        output_dir (?): The output directory. Default: None.

    Returns:
        json_file (?): The json file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/json"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Assign json file name to a variable
    json_file = f"{output_dir}/groups.json"
    # Output the dataframe to json, save in json file
    df.to_json(json_file, indent=4, orient="records")
    # Log diagnostic information
    logger.info(f"File output location: {json_file}")
    return json_file


def to_ansible(env, df, output_dir: str = None):
    """
    Take the pandas dataframe, convert it to a dictionary
    and render that dictionary through a Jinja2 template to
    create an Ansible inventory file.

    Args:
        env (?): The loaded Jinja2 environment, used to retrieve
        templates from.
        df (?): The pandas dataframe object, initialised from the
        inventory data source
        output_dir (str): The output directory. Default: None.

    Returns:
        ans_h_file (?): The Ansible inventory file object.

    Raises:
        N/A
    """
    # Specify the output dir when it is not supplied
    if output_dir is None:
        output_dir = "outputs/ansible/inventory"
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


def main(source_type: str, output_type: str, logger):
    """
    Main workflow function used to execute the entire workflow

    Args:
        source_type: The source file type to read the inventory
    and group data in from.
        output_type: What file type(s) you would like to be outputted
    as a result of running the function.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Initialise inventory dataframe, based on the source_dir and source_type
    inv_df = init_inventory(source_dir=None, source_type=source_type)
    # Initialise group dataframe, based on the source_dir and source_type
    group_df = init_groups(source_dir=None, source_type=source_type)
    # Prepare the jinja2 template environment
    env = prep_templates(tmpl_dir=None)
    # Diagnostic outputs
    logger.debug(f"Output type is: {output_type}")
    # If/Else block to execute the desired output_type based on
    # what is passed in from argparse
    # If output type is all, output all file types
    if output_type == "all":
        to_nr_hosts(env, inv_df)
        to_nr_groups(env=env, df=group_df)
        to_csv_inventory(inv_df)
        to_xlsx_inventory(inv_df)
        to_csv_groups(group_df)
        to_xlsx_groups(group_df)
        to_pyats(env=env, df=inv_df)
        to_ansible(env=env, df=inv_df)
        to_json_inventory(inv_df)
        to_json_groups(group_df)
    # If output type is nornir, output all nornir types
    elif output_type == "nornir":
        to_nr_hosts(env, inv_df)
        to_nr_groups(env=env, df=group_df)
    # If output type is csv, output all CSV types
    elif output_type == "csv":
        to_csv_inventory(inv_df)
        to_csv_groups(group_df)
    # If output type is xlsx, output all xlsx types
    elif output_type == "xlsx":
        to_xlsx_inventory(inv_df)
        to_xlsx_groups(group_df)
    # If output type is pyats, output all pyATS types
    elif output_type == "pyats":
        to_pyats(env=env, df=inv_df)
    # If output type is ansible, output all ansible types
    elif output_type == "ansible":
        to_ansible(env=env, df=inv_df)
    # If output type is json, output all ansible types
    elif output_type == "json":
        to_json_inventory(inv_df)
        to_json_groups(group_df)


if __name__ == "__main__":
    # Initialise click from the command-line
    ms()
