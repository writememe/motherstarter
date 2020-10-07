# Import modules
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pathlib as pl
from colorama import Fore, init
import logging
import argparse

# Setup argparse parameters to take user input from the command line
parser = argparse.ArgumentParser(
    description="Translate source file(s) into network automation inventory outputs"
)
# Setup argparse parameters to take user input from the command line
parser.add_argument(
    "-l",
    "--log",
    dest="logging_level",
    choices=["debug", "info", "warning", "error", "critical"],
    default="debug",
    help="Specify the logging level",
)
parser.add_argument(
    "-st",
    "--source-type",
    dest="source_type",
    choices=["json", "csv", "xlsx"],
    default="json",
    help="Specify the source file type. Default is JSON",
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
    help="Specify the output file types. Default is all file types. This arguement only takes one option.",
)
args = parser.parse_args()

log_level = args.logging_level.upper()
source_type = args.source_type
output_type = args.output_type
print(log_level)


# if args.log_level:
#     init_logger()
#     logging.basicConfig(level=getattr(logging, args.log_level.upper()))


def init_logger(log_level: str, log_name: str = "ms.log"):
    logger = logging.getLogger(__name__)
    log_fmt = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
    f_handler = logging.FileHandler(log_name)
    f_handler.setFormatter(log_fmt)
    s_handler = logging.StreamHandler()
    s_handler.setFormatter(log_fmt)
    # TODO: Rework this ugly, yet functional block of code.
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


logger = init_logger(log_level=log_level, log_name="ms1.log")

logger.debug(f"Hello debugs - {log_level}")


# logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
# file_handler = logging.FileHandler("motherstarter.log")
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.INFO)
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)


# Auto-reset colorama colours back after each print statement
init(autoreset=True)


def init_inventory(source_dir: str = None, source_type: str = "json"):
    """
    Initialise the inventory source
    """
    print(f"{Fore.CYAN}Inventory source type is {source_type}")
    logger.warning(f"{Fore.CYAN}Inventory source type is {source_type}")
    logger.debug(f"{Fore.RED}ERROR: {source_type} not supported...")
    if source_type == "json":
        df = init_inventory_json(source_dir)
    elif source_type == "xlsx":
        df = init_inventory_xlsx(source_dir)
    elif source_type == "csv":
        df = init_inventory_csv(source_dir)
    else:
        print(f"{Fore.RED}ERROR: {source_type} not supported...")

        df = None
    print(type(df))
    return df


def init_groups(source_dir: str = None, source_type: str = "json"):
    """
    Initialise the groups source
    """
    if source_type == "json":
        df = init_groups_json(source_dir)
    elif source_type == "xlsx":
        df = init_groups_xlsx(source_dir)
    elif source_type == "csv":
        df = init_groups_csv(source_dir)
    else:
        print(f"{Fore.RED}ERROR: {source_type} not supported...")
        df = None
    return df


def init_inventory_json(source_dir: str = None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/inventory/json"
    # Read in source files
    df = pd.read_json(f"{source_dir}/inventory.json")
    return df


def init_inventory_xlsx(source_dir: str = None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/inventory/xlsx"
    # Read in source files
    df = pd.read_excel(f"{source_dir}/inventory.xlsx", sheet_name="inventory")
    return df


def init_inventory_csv(source_dir: str = None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/inventory/csv"
    # Read in source files
    df = pd.read_csv(f"{source_dir}/inventory.csv")
    return df


def init_groups_json(source_dir: str = None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/groups/json"
    # Read in source files
    df = pd.read_json(f"{source_dir}/groups.json")
    return df


def init_groups_xlsx(source_dir: str = None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/groups/xlsx"
    # Read in source files
    df = pd.read_excel(f"{source_dir}/groups.xlsx", sheet_name="groups")
    return df


def init_groups_csv(source_dir: str = None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/groups/csv"
    # Read in source files
    df = pd.read_csv(f"{source_dir}/groups.csv")
    return df


def dataframe_to_dict(df):
    """
    Helper function to return a Pandas dataframe into
    a dictionary
    """
    return df.to_dict(orient="records")


def prep_templates(tmpl_dir: str = None):
    """
    Prepare all the templates f
    """
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
    """"""
    if output_dir is None:
        output_dir = "outputs/nr/inventory"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    template = env.get_template("nornir/hosts.j2")
    output = template.render(inventory=inv)
    with open(f"{output_dir}/hosts.yaml", "w+") as nr_h_file:
        nr_h_file.write(output)
    print(f"File output location: {nr_h_file.name}")


def to_nr_groups(env, df, output_dir: str = None):
    """"""
    if output_dir is None:
        output_dir = "outputs/nr/inventory"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    template = env.get_template("nornir/groups.j2")
    output = template.render(groups=inv)
    with open(f"{output_dir}/groups.yaml", "w+") as nr_g_file:
        nr_g_file.write(output)
    print(f"File output location: {nr_g_file.name}")


def to_pyats(env, df, output_dir: str = None):
    """"""
    if output_dir is None:
        output_dir = "outputs/pyats"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    template = env.get_template("pyats/testbed.j2")
    output = template.render(inventory=inv)
    with open(f"{output_dir}/mother_starter_tb.yaml", "w+") as tb_file:
        tb_file.write(output)
    print(f"File output location: {tb_file.name}")


def to_csv_inventory(df, output_dir: str = None):
    """"""
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
    """"""
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
    """"""
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
    """"""
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
    """"""
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


def main(source_type=source_type, output_type=output_type):
    inv_df = init_inventory(source_dir=None, source_type=source_type)
    group_df = init_groups(source_dir=None, source_type=source_type)
    env = prep_templates()
    print(f"OUTPUT TYPE IS {output_type}")
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


main(source_type=source_type, output_type=output_type)
