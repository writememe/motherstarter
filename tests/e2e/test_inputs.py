# Import modules
import pprint
import pytest
import motherstarter
import json

# Set indentation on pretty print
pp = pprint.PrettyPrinter(indent=2)

# Params for testing
logger = "DEBUG"
source_type = "json"
output_type = "all"
source_dir = "../test_data/core"


# Add pytest mark
@pytest.mark.inputs
def inventory_json(logger, source_type, output_type, source_dir):
    result = motherstarter.main.from_parent(
        logger=logger,
        source_type=source_type,
        output_type=output_type,
        source_dir=source_dir,
    )
    with open("../../motherstarter/outputs/json/inventory.json") as f:
        inv_data = json.load(f)
    assert inv_data[0]["name"] == "lab-csr-01.lab.dfjt.local2"
    print(result)
