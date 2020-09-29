# Import modules
import pandas as pd
import json
from jinja2 import Environment, FileSystemLoader
import os
import json
import pprint

# Set indentation on pretty print
pp = pprint.PrettyPrinter(indent=2)

inventory_df = pd.read_json('sample/inputs/inventory.json', orient="records")
inventory_df.head()
print("*" * 100)
print(inventory_df)


print(pd.DataFrame.from_dict(inventory_df))
# Convert dataframe to dictionary
inv_dict = pd.DataFrame.to_dict(inventory_df)
pp.pprint(inv_dict)
print(type(inv_dict))

import json


# jsonfiles = json.loads(df.to_json(orient='records'))

# Load template directory where templates are located
tmpl_dir = FileSystemLoader("templates/outputs")
print(tmpl_dir)

# Loading environment and setting autoescape to True
# to prevent XSS attacks
env = Environment(
    loader=tmpl_dir, autoescape=True, trim_blocks=True, lstrip_blocks=True
)
nr_hosts_tmpl = env.get_template("nr_hosts.j2")
# Render the data through the Nornir template and assign to a variable
nr_inv = nr_hosts_tmpl.render(inventory=inv_dict)
# Write output to file
with open("hosts.yaml", "w+") as nr_file:
    nr_file.write(nr_inv)
