"""
This is where I am testing inputs via the CLI
"""

# Import modules
from click.testing import CliRunner
import pytest
from motherstarter import motherstarter as ms
import traceback


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_convert_default(runner):
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


def test_help(runner):
    result = runner.invoke(ms.cli, ["--help"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_usage = "Usage: cli [OPTIONS] COMMAND [ARGS]."
    expected_convert = (
        "convert  Convert source file(s) into network automation inventory outputs"
    )
    assert result.exit_code == 0
    assert expected_usage in result.output
    assert expected_convert in result.output


def test_convert_source_type_csv(runner):
    st = "csv"
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_block = f"DEBUG - Inventory source type is {st}"
    assert result.exit_code == 0
    assert expected_block in result.output


def test_convert_source_type_json(runner):
    st = "json"
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_block = f"DEBUG - Inventory source type is {st}"
    assert result.exit_code == 0
    assert expected_block in result.output


def test_convert_source_type_xlsx(runner):
    st = "xlsx"
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_block = f"DEBUG - Inventory source type is {st}"
    assert result.exit_code == 0
    assert expected_block in result.output


def test_convert_source_type_bad(runner):
    st = "bad"
    result = runner.invoke(ms.convert, ["-st", st])
    expected_block = f"Error: Invalid value for '--source-type' / '-st': invalid choice: {st}. (choose from csv, json, xlsx)"  # noqa
    assert result.exit_code == 2
    assert expected_block in result.output


def test_convert_source_dir_custom(runner):
    sd = "tests/test_data/core"
    # sd = "motherstarter/inputs"
    result = runner.invoke(ms.convert, ["-sd", sd])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    expected_source_dir = f"DEBUG - Source directory is: {sd}"
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir in result.output


def test_convert_source_dir_bad(runner):
    sd = "tests/test_data/core/bad"
    # sd = "motherstarter/inputs"
    result = runner.invoke(ms.convert, ["-sd", sd])
    assert result.exit_code == 1


def test_convert_log_level_debug(runner):
    ll = "debug"
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert "ERROR -" not in result.output
    assert "CRITICAL -" not in result.output


def test_convert_log_level_info(runner):
    ll = "info"
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    assert result.exit_code == 0
    assert "DEBUG -" not in result.output
    assert "ERROR -" not in result.output
    assert "CRITICAL -" not in result.output


def test_convert_log_level_warning(runner):
    ll = "warning"
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    assert result.exit_code == 0
    assert "DEBUG -" not in result.output
    assert "INFO -" not in result.output
    assert "ERROR -" not in result.output
    assert "CRITICAL -" not in result.output


def test_convert_log_level_error(runner):
    ll = "error"
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    assert result.exit_code == 0
    assert "DEBUG -" not in result.output
    assert "INFO -" not in result.output
    assert "WARNING -" not in result.output
    assert "CRITICAL -" not in result.output


def test_convert_log_level_critical(runner):
    ll = "critical"
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    assert result.exit_code == 0
    assert "DEBUG -" not in result.output
    assert "INFO -" not in result.output
    assert "WARNING -" not in result.output
    assert "ERROR -" not in result.output


def test_convert_log_level_bad(runner):
    ll = "bad"
    result = runner.invoke(ms.convert, ["-l", ll])
    expected_block = f"Error: Invalid value for '--log-level' / '-l': invalid choice: {ll}. (choose from debug, info, warning, error, critical)"  # noqa
    assert result.exit_code == 2
    assert expected_block in result.output


def test_convert_output_type_csv(runner):
    ot = "csv"
    result = runner.invoke(ms.convert, ["-o", ot])
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/inventory.csv"
    )
    expected_output_groups_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/groups.csv"
    )
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output
    assert expected_output_groups_file in result.output
