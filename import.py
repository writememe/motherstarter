# Import modules
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pathlib as pl
from colorama import Fore, init


def init_inventory(source_dir=None, source_type='json'):
    """
    Initialise the inventory source
    """
    if source_type == "json":
        df = init_inventory_json(source_dir)
    elif source_type == 'xlsx':
        df = init_inventory_xlsx(source_dir)
    elif source_type == 'csv':
        df = init_inventory_csv(source_dir)
    else:
        print(f"{Fore.RED}ERROR: {source_type} not supported...")
        df = None
    return df


def init_groups(source_dir=None, source_type='json'):
    """
    Initialise the groups source
    """
    if source_type == "json":
        df = init_groups_json(source_dir)
    elif source_type == 'xlsx':
        df = init_groups_xlsx(source_dir)
    elif source_type == 'csv':
        df = init_groups_csv(source_dir)
    else:
        print(f"{Fore.RED}ERROR: {source_type} not supported...")
        df = None
    return df


def init_inventory_json(source_dir=None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/inventory/json"
    # Read in source files
    df = pd.read_json(f"{source_dir}/inventory.json")
    return df


def init_inventory_xlsx(source_dir=None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/inventory/xlsx"
    # Read in source files
    df = pd.read_excel(f"{source_dir}/inventory.xlsx", sheet_name="inventory")
    return df


def init_inventory_csv(source_dir=None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/inventory/csv"
    # Read in source files
    df = pd.read_csv(f"{source_dir}/inventory.csv")
    return df


def init_groups_json(source_dir=None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/groups/json"
    # Read in source files
    df = pd.read_json(f"{source_dir}/groups.json")
    return df


def init_groups_xlsx(source_dir=None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "inputs/groups/xlsx"
    # Read in source files
    df = pd.read_excel(f"{source_dir}/inventory.xlsx", sheet_name="groups")
    return df


def init_groups_csv(source_dir=None):
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


def prep_templates(tmpl_dir=None):
    """
    Prepare all the templates f
    """
    if tmpl_dir is None:
        tmpl_dir = "templates/outputs/nornir"
    # Load template directory where Jinja2 templates are located
    templates = FileSystemLoader(tmpl_dir)
    # Load environment and setting autoescape to True
    # to prevent XSS attacks
    env = Environment(
        loader=templates, autoescape=True, trim_blocks=True, lstrip_blocks=True
    )
    return env


def to_nr_hosts(env, df, output_dir=None):
    """"""
    if output_dir is None:
        output_dir = "outputs/nr/inventory"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    template = env.get_template("hosts.j2")
    output = template.render(inventory=inv)
    with open(f"{output_dir}/hosts.yaml", "w+") as nr_h_file:
        nr_h_file.write(output)
    print(f"File output location: {nr_h_file.name}")


def to_nr_groups(env, df, output_dir=None):
    """"""
    if output_dir is None:
        output_dir = "outputs/nr/inventory"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    template = env.get_template("groups.j2")
    output = template.render(groups=inv)
    with open(f"{output_dir}/groups.yaml", "w+") as nr_g_file:
        nr_g_file.write(output)
    print(f"File output location: {nr_g_file.name}")


def to_pyats(env, df, output_dir=None):
    """"""
    if output_dir is None:
        output_dir = "outputs/pyats"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    template = env.get_template("testbed.j2")
    output = template.render(inventory=inv)
    with open(f"{output_dir}/mother_starter_tb.yaml", "w+") as tb_file:
        tb_file.write(output)
    print(f"File output location: {tb_file.name}")


def to_csv_inventory(df, output_dir=None):
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


def to_xlsx_inventory(df, output_dir=None):
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


def to_csv_groups(df, output_dir=None):
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


def to_xlsx_groups(df, output_dir=None):
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


def to_ansible(env, df, output_dir=None):
    """"""
    if output_dir is None:
        output_dir = "outputs/ansible/inventory"
    # Create entry directory and/or check that it exists
    pl.Path(output_dir).mkdir(parents=True, exist_ok=True)
    inv = dataframe_to_dict(df)
    template = env.get_template("hosts.j2")
    output = template.render(inventory=inv)
    with open(f"{output_dir}/hosts", "w+") as ans_h_file:
        ans_h_file.write(output)
    print(f"File output location: {ans_h_file.name}")


def main():
    inv_df = init_inventory(source_dir=None, source_type='json')
    group_df = init_groups(source_dir=None, source_type='json')
    env = prep_templates()
    pyats_env = prep_templates(tmpl_dir="templates/outputs/pyats")
    to_nr_hosts(env, inv_df)
    to_nr_groups(env=env, df=group_df)
    to_csv_inventory(inv_df)
    to_xlsx_inventory(inv_df)
    to_csv_groups(group_df)
    to_xlsx_groups(group_df)
    to_pyats(env=pyats_env, df=inv_df)
    ans_env = prep_templates(tmpl_dir="templates/outputs/ansible")
    to_ansible(env=ans_env, df=inv_df)


main()
