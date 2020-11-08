"""
Unit tests to test two functions which
both have a "catch all" else statement to catch
bad source_types.

Given the entire package is run from click, I've
written these tests to test this functionality.

It's not anticipated that it would be needed in
the wild.
"""

# Import module
from motherstarter import motherstarter as ms


def test_init_inventory_bad():
    # Initialise the logger
    logger = ms.init_logger(log_level="CRITICAL", log_name="unit-tests.log")
    # Initialise the init_inventory function with a bad source_type
    df = ms.init_inventory(
        logger=logger, source_dir="tests/test_data/inputs/core", source_type="bad"
    )
    assert df is None


def test_init_groups_bad():
    # Initialise the logger
    logger = ms.init_logger(log_level="CRITICAL", log_name="unit-tests.log")
    # Initialise the init_groups function with a bad source_type
    df = ms.init_groups(
        logger=logger, source_dir="tests/test_data/inputs/core", source_type="bad"
    )
    assert df is None
