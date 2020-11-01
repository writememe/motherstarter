"""
This is where I am testing inputs via the CLI
"""

# Import modules
from click.testing import CliRunner
import pytest
from motherstarter import motherstarter as ms


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_default_convert(runner):
    result = runner.invoke(ms.cli, ["convert"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    expected_source_dir = (
        "WARNING - Source directory not specified, using default: motherstarter/inputs"
    )
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir in result.output


def test_version(runner):
    result = runner.invoke(ms.cli, ["--version"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected = "version 0.0.1"
    assert result.exit_code == 0
    assert expected in result.output


def test_named_convert_csv(runner):
    st = "csv"
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_block = f"DEBUG - Inventory source type is {st}"
    assert result.exit_code == 0
    assert expected_block in result.output


def test_named_convert_json(runner):
    st = "json"
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_block = f"DEBUG - Inventory source type is {st}"
    assert result.exit_code == 0
    assert expected_block in result.output


def test_named_convert_xlsx(runner):
    st = "xlsx"
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_block = f"DEBUG - Inventory source type is {st}"
    assert result.exit_code == 0
    assert expected_block in result.output

def test_named_convert_bad(runner):
    st = "bad"
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        print(result.output)
        print(result.exception)
        print(result.exc_info)
    expected_block = f"Error: Invalid value for '--source-type' / '-st': invalid choice: {st}. (choose from csv, json, xlsx)"
    assert result.exit_code == 2
    assert expected_block in result.output