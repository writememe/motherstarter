"""
Just mucking around here.
"""

# Import modules
import pprint

# import pytest
import motherstarter.motherstarter as motherstarter
import json

# Set indentation on pretty print
pp = pprint.PrettyPrinter(indent=2)
# Params for testing
log_level = "DEBUG"
source_type = "json"
output_type = "all"
source_dir = "../test_data/core"
log_name = "tester.log"


def logger(log_level=log_level, log_name=log_name):
    # Initialise the logger
    log_result = motherstarter.init_logger(log_level=log_level, log_name=log_name)
    return log_result


def inventory_json(logger, source_type, output_type, source_dir):
    result = motherstarter.main(
        logger=logger,
        source_type=source_type,
        output_type=output_type,
        source_dir=source_dir,
    )
    with open("../../motherstarter/outputs/json/inventory.json") as f:
        inv_data = json.load(f)
    assert inv_data[0]["name"] == "lab-csr-01.lab.dfjt.local2"
    print(result)


log_result = logger(log_level=log_level, log_name=log_name)
inventory_json(
    logger=log_result,
    source_type=source_type,
    output_type=output_type,
    source_dir=source_dir,
)
