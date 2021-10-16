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
import pytest

# Define the source type globally for all tests.
ST = "bad"


def test_init_inventory_bad():
    # Initialise the logger
    logger = ms.init_logger(log_level="CRITICAL", log_name="unit-tests.log")
    # Ensure that a ValueError is raised when a bad source is supplied.
    # Initialise the init_inventory function with a bad source_type
    with pytest.raises(ValueError) as val_err:
        df = ms.init_inventory(  # noqa (unused import)
            logger=logger, source_dir="tests/test_data/inputs/core", source_type=ST
        )
    # Perform assertion tests to ensure error message are in the expected outputs
    assert f"Source Type: {ST} not supported..." in str(val_err.value)


def test_init_groups_bad():
    # Initialise the logger
    logger = ms.init_logger(log_level="CRITICAL", log_name="unit-tests.log")
    # Ensure that a ValueError is raised when a bad source is supplied.
    # Initialise the init_inventory function with a bad source_type
    with pytest.raises(ValueError) as val_err:
        df = ms.init_groups(  # noqa (unused import)
            logger=logger, source_dir="tests/test_data/inputs/core", source_type=ST
        )
    # Perform assertion tests to ensure error message are in the expected outputs
    assert f"Source Type: {ST} not supported..." in str(val_err.value)
