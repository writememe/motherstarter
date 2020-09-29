# Import modules
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pprint
import pathlib as pl

# Set indentation on pretty print
pp = pprint.PrettyPrinter(indent=2)


def init_dataframe(source_dir=None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "sample/inputs/"
    # Read in source files
    df = pd.read_json(f"{source_dir}inventory.json")
    return df


def init_grp_dataframe(source_dir=None):
    if source_dir is None:
        # Specify the source dirs for inputs and templates
        source_dir = "sample/inputs/"
    # Read in source files
    df = pd.read_json(f"{source_dir}groups.json")
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


def main():
    df = init_dataframe()
    group_df = init_grp_dataframe()
    env = prep_templates()
    to_nr_hosts(env, df)
    to_nr_groups(env=env, df=group_df)


main()
