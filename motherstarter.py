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

# import coloredlogs

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
    choices=["json", "csv", "xlsx"],
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
    choices=["nornir", "csv", "xlsx", "pyats", "all"],
    dest="output_type",
    default="all",
    help="Specify the output file types. Default is all file types. This argument only takes one option.",
)
args = parser.parse_args()
# Take log_level argument, assign to var and turn into uppercase
log_level = args.logging_level.upper()
# Take source_type and output_type arguments and assign to a variable
source_type, output_type = args.source_type, args.output_type


def init_logger(log_level: str, log_name: str = "ms.log"):
    """
    Initialise a logger object, to be used to perform logging
    and console outputs to the screen.

    The log_level is passed into the function and used to set
    the logging level.

    :param log_level: The severity logging level for all events
    to be logged at.
    :param log_name: The name of the log file
    :return logger: An initialised logger object
    """
    # Setup coloredlogs based on the logging level
    # coloredlogs.install(level=log_level)
    # Create a logger object
    logger = logging.getLogger(__name__)
    # Setup the logging formatter
    log_fmt = logging.Formatter(("%(asctime)s - " "%(levelname)s - " "%(message)s"))
    stream_fmt = logging.Formatter(("%(levelname)s - " "%(message)s"))
    f_handler = logging.FileHandler(log_name)
    f_handler.setFormatter(log_fmt)
    s_handler = logging.StreamHandler()
    s_handler.setFormatter(stream_fmt)
    # TODO: Rework this ugly, yet functional block of code.
    # If/Else block to set logging level based on the log_level
    # taken from the user using argparse
    if log_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)
        s_handler.setLevel(logging.DEBUG)
    elif log_level == "INFO":
        logger.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)
        s_handler.setLevel(logging.INFO)
    elif log_level == "WARNING":
        logger.setLevel(logging.WARNING)
        f_handler.setLevel(logging.WARNING)
        s_handler.setLevel(logging.WARNING)
    elif log_level == "ERROR":
        logger.setLevel(logging.ERROR)
        f_handler.setLevel(logging.ERROR)
        s_handler.setLevel(logging.ERROR)
    elif log_level == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
        f_handler.setLevel(logging.CRITICAL)
        s_handler.setLevel(logging.CRITICAL)
    logger.addHandler(f_handler)
    logger.addHandler(s_handler)
    return logger


# Initalise logger
logger = init_logger(log_level=log_level, log_name="ms1.log")


# Auto-reset colorama colours back after each print statement
init(autoreset=True)


def init_inventory(source_dir: str = None, source_type: str = "json"):
    """
    Initialise the inventory data based on the source_type and from the source
    directory and return a pandas dataframe object?

    :param source_dir: The source directory to find the files in.
    :param source_type: The source file type to read the inventory data from.
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
    directory and return a pandas dataframe object?

    :param source_dir: The source directory to find the inventory files in.
    :param source_type: The source file type to read the group data from.
    :return df: The pandas dataframe object
    :type df: #TODO - not sure what this is..
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


def init_inventory_json(source_dir: str = None):
    """
    Initialise a pandas dataframe by using pandas read_json
    function by reading in the "inventory.json" file from the
    applicable source directory


    :param source_dir: The source directory to find the inventory files in.
    :return df: The pandas dataframe object
    :type df: #TODO - not sure what this is..

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.
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


    :param source_dir: The source directory to find the inventory files in.
    :return df: The pandas dataframe object
    :type df: #TODO - not sure what this is..

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.
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


    :param source_dir: The source directory to find the files in.
    :return df: The pandas dataframe object
    :type df: #TODO - not sure what this is..

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.
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


    :param source_dir: The source directory to find the groups files in.
    :return df: The pandas dataframe object
    :type df: #TODO - not sure what this is..

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.
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


    :param source_dir: The source directory to find the groups files in.
    :return df: The pandas dataframe object
    :type df: #TODO - not sure what this is..

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.
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


    :param source_dir: The source directory to find the groups files in.
    :return df: The pandas dataframe object
    :type df: #TODO - not sure what this is..

    NOTE: Whilst this function exposes the ability to change the source_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the 'inputs/'
    directory. We would recommend just sticking with that, unless you want
    to write your own custom workflow.
    """
    # Specify the source dirs for inputs when it is not supplied
    if source_dir is None:
        source_dir = "inputs/groups/csv"
    # Read in source file. NOTE: The source filename is hardcoded
    df = pd.read_csv(f"{source_dir}/groups.csv")
    return df


def dataframe_to_dict(df) -> dict:
    """
    Helper function to return a Pandas dataframe into
    a dictionary so that it can be used for further
    processing throughout the application

    :param df: The pandas dataframe object
    :return : A dictionary instance of the dataframe object
    """
    # Convert dataframe to a dict object and orient based on records
    return df.to_dict(orient="records")


def prep_templates(tmpl_dir: str = None):
    """
    Take the template directory and load a Jinja2 environment
    with those templates and other settings enabled

    :param tmpl_dir: The template directory one-level above where the Jinja2
    templates are stored.

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

    :return env: The loaded jinja2 environment.

    NOTE: Whilst this function exposes the ability to change the tmpl_dir,
    it's probably not something you want to be doing. Most people can just
    place the files in template folder structure supplied in the
    'templates/outputs/' directory. We would recommend just sticking with
    that, unless you want to write your own custom workflow.
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

    :param env: The loaded Jinja2 environment, used to retrieve
    templates from.
    :param df: The pandas dataframe object, initialised from the
    inventory data source
    :param output_dir: The output directory

    :return nr_h_file: The nornir hosts file object.
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

    :param env: The loaded Jinja2 environment, used to retrieve
    templates from.
    :param df: The pandas dataframe object, initialised from the
    inventory data source
    :param output_dir: The output directory

    :return nr_g_file: The nornir groups file object.
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

    :param env: The loaded Jinja2 environment, used to retrieve
    templates from.
    :param df: The pandas dataframe object, initialised from the
    inventory data source
    :param output_dir: The output directory

    :return tb_file: The pyATS testbed file object.
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
    TODO: Doco function.
    """
    if output_dir is None:
        output_dir = "outputs/generic"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    inv = df.from_dict(inv)
    csv_file = f"{output_dir}/inventory.csv"
    inv.to_csv(csv_file, index=False)
    print(f"File output location: {csv_file}")


def to_xlsx_inventory(df, output_dir: str = None):
    """
    TODO: Doco function
    """
    if output_dir is None:
        output_dir = "outputs/generic"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    inv = df.from_dict(inv)
    xlsx_file = f"{output_dir}/inventory.xlsx"
    inv.to_csv(xlsx_file, index=False)
    print(f"File output location: {xlsx_file}")


def to_csv_groups(df, output_dir: str = None):
    """
    TODO: Doco function.
    """
    if output_dir is None:
        output_dir = "outputs/generic"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    inv = df.from_dict(inv)
    csv_file = f"{output_dir}/groups.csv"
    inv.to_csv(csv_file, index=False)
    print(f"File output location: {csv_file}")


def to_xlsx_groups(df, output_dir: str = None):
    """
    TODO: Doco function.
    """
    if output_dir is None:
        output_dir = "outputs/generic"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    inv = df.from_dict(inv)
    xlsx_file = f"{output_dir}/groups.xlsx"
    inv.to_csv(xlsx_file, index=False)
    print(f"File output location: {xlsx_file}")


def to_ansible(env, df, output_dir: str = None):
    """
    TODO: Doco function.
    """
    if output_dir is None:
        output_dir = "outputs/ansible/inventory"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    template = env.get_template("ansible/hosts.j2")
    output = template.render(inventory=inv)
    with open(f"{output_dir}/hosts", "w+") as ans_h_file:
        ans_h_file.write(output)
    print(f"File output location: {ans_h_file.name}")


def main(source_type: str = source_type, output_type: str = output_type):
    """
    Main workflow function used to execute the entire workflow

    :param source_type: The source file type to read the inventory
    and group data in from.
    :param output_type: What file type(s) you would like to be outputted
    as a result of running the function.
    """
    # Initialise inventory dataframe, based on the source_dir and source_type
    inv_df = init_inventory(source_dir=None, source_type=source_type)
    # Initialise group dataframe, based on the source_dir and source_type
    group_df = init_groups(source_dir=None, source_type=source_type)
    # Prepare the jinja2 template environment
    env = prep_templates(tmpl_dir=None)
    logger.debug(f"Output type is: {output_type}")
    # If/Else block to execute the desired output_type based on
    # what is passed in from argparse
    if output_type == "all":
        to_nr_hosts(env, inv_df)
        to_nr_groups(env=env, df=group_df)
        to_csv_inventory(inv_df)
        to_xlsx_inventory(inv_df)
        to_csv_groups(group_df)
        to_xlsx_groups(group_df)
        to_pyats(env=env, df=inv_df)
        to_ansible(env=env, df=inv_df)
    elif output_type == "nornir":
        to_nr_hosts(env, inv_df)
        to_nr_groups(env=env, df=group_df)
    elif output_type == "csv":
        to_csv_inventory(inv_df)
        to_csv_groups(group_df)
    elif output_type == "xlsx":
        to_xlsx_inventory(inv_df)
        to_xlsx_groups(group_df)
    elif output_type == "pyats":
        to_pyats(env=env, df=inv_df)
    elif output_type == "ansible":
        to_ansible(env=env, df=inv_df)


# Execute main function
main(source_type=source_type, output_type=output_type)
