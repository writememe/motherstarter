"""
This is where I am testing inputs via the CLI
"""

# Import modules
from click.testing import CliRunner
import pytest
from motherstarter import motherstarter as ms
import traceback
from motherstarter import __version__


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_convert_default(runner):
    result = runner.invoke(ms.cli, ["convert"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    """
    NOTE: Due to the default dir being a combination of the input/template dirs
    and the motherstarter_file dir, these tests are split into two.
    An example is:
    motherstarter_dir = /mnt/c/Users/acme/projects/motherstarter/
    default_template_dir = motherstarter/templates/core/
    default_source_dir = motherstarter/inputs/
    You end up with something like:
    template_dir = motherstarter_dir + default_template_dir
    source_dir = motherstarter_dir + default_source_dir
    The motherstarter_dir changes on every platform, so we don't bother
    testing that. Instead, we just want to make sure we detect the
    default_source_dir and default_template_dir in the outputs and the DEBUG stamps
    at the front of the outputs.
    """
    expected_source_dir_start = "DEBUG - Source directory is: "
    expected_source_dir_end = "motherstarter/inputs/"
    expected_template_dir_start = "DEBUG - Source template directory is: "
    expected_template_dir_end = "motherstarter/templates/core/"
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir_start in result.output
    assert expected_source_dir_end in result.output
    assert expected_template_dir_start in result.output
    assert expected_template_dir_end in result.output


def test_base_version(runner):
    result = runner.invoke(ms.cli, ["--version"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected = __version__
    assert result.exit_code == 0
    assert expected in result.output


def test_base_help(runner):
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


def test_convert_help(runner):
    result = runner.invoke(ms.convert, ["--help"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_usage = "Usage: convert [OPTIONS]"
    expected_convert = (
        "Convert source file(s) into network automation inventory outputs based on"
        "\n  multiple command-line inputs"
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
    sd = "tests/test_data/inputs/core"
    result = runner.invoke(ms.convert, ["-sd", sd])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    expected_source_dir_start = "DEBUG - Source directory is: "
    expected_source_dir_end = f"{sd}"
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir_start in result.output
    assert expected_source_dir_end in result.output


def test_convert_source_dir_bad(runner):
    sd = "tests/test_data/inputs/core/bad"
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


def test_convert_template_dir_custom(runner):
    td = "tests/test_data/templates/custom"
    result = runner.invoke(ms.convert, ["-td", td])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    expected_source_dir_start = "DEBUG - Source directory is: "
    expected_source_dir_end = "motherstarter/inputs/"
    expected_template_dir = f"DEBUG - Source template directory is: {td}"
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir_start in result.output
    assert expected_source_dir_end in result.output
    assert expected_template_dir in result.output


def test_convert_template_dir_bad(runner):
    td = "tests/test_data/templates/bad"
    result = runner.invoke(ms.convert, ["-td", td])
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    expected_source_dir_start = "DEBUG - Source directory is: "
    expected_source_dir_end = "motherstarter/inputs/"
    expected_template_dir = f"DEBUG - Source template directory is: {td}"
    assert result.exit_code == 1
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir_start in result.output
    assert expected_source_dir_end in result.output
    assert expected_template_dir in result.output


def test_convert_output_type_csv(runner):
    ot = "csv"
    result = runner.invoke(ms.convert, ["-o", ot])
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/inventory.{ot}"
    )
    expected_output_groups_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/groups.{ot}"
    )
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output
    assert expected_output_groups_file in result.output


def test_convert_output_type_json(runner):
    ot = "json"
    result = runner.invoke(ms.convert, ["-o", ot])
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/inventory.{ot}"
    )
    expected_output_groups_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/groups.{ot}"
    )
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output
    assert expected_output_groups_file in result.output


def test_convert_output_type_xlsx(runner):
    ot = "xlsx"
    result = runner.invoke(ms.convert, ["-o", ot])
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/inventory.{ot}"
    )
    expected_output_groups_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/groups.{ot}"
    )
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output
    assert expected_output_groups_file in result.output


def test_convert_output_type_nornir(runner):
    ot = "nornir"
    result = runner.invoke(ms.convert, ["-o", ot])
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        "INFO - File output location: motherstarter/outputs/nr/inventory/groups.yaml"
    )
    expected_output_groups_file = (
        "INFO - File output location: motherstarter/outputs/nr/inventory/hosts.yaml"
    )
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output
    assert expected_output_groups_file in result.output


def test_convert_output_type_pyats(runner):
    ot = "pyats"
    result = runner.invoke(ms.convert, ["-o", ot])
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = f"INFO - File output location: motherstarter/outputs/{ot}/mother_starter_tb.yaml"  # noqa
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output


def test_convert_output_type_ansible(runner):
    ot = "ansible"
    result = runner.invoke(ms.convert, ["-o", ot])
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/inventory/hosts"
    )
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output


def test_convert_output_type_all(runner):
    ot = "all"
    result = runner.invoke(ms.convert, ["-o", ot])
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_csv_file = (
        "INFO - File output location: motherstarter/outputs/csv/inventory.csv"
    )
    expected_output_groups_csv_file = (
        "INFO - File output location: motherstarter/outputs/csv/groups.csv"
    )
    expected_output_inv_json_file = (
        "INFO - File output location: motherstarter/outputs/json/inventory.json"
    )
    expected_output_groups_json_file = (
        "INFO - File output location: motherstarter/outputs/json/groups.json"
    )
    expected_output_inv_xlsx_file = (
        "INFO - File output location: motherstarter/outputs/xlsx/inventory.xlsx"
    )
    expected_output_groups_xlsx_file = (
        "INFO - File output location: motherstarter/outputs/xlsx/groups.xlsx"
    )
    expected_output_inv_nornir_file = (
        "INFO - File output location: motherstarter/outputs/nr/inventory/groups.yaml"
    )
    expected_output_groups_nornir_file = (
        "INFO - File output location: motherstarter/outputs/nr/inventory/hosts.yaml"
    )
    expected_output_pyats_inv_file = "INFO - File output location: motherstarter/outputs/pyats/mother_starter_tb.yaml"  # noqa
    expected_output_inv_ansible_file = (
        "INFO - File output location: motherstarter/outputs/ansible/inventory/hosts"
    )
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_csv_file in result.output
    assert expected_output_groups_csv_file in result.output
    assert expected_output_inv_json_file in result.output
    assert expected_output_groups_json_file in result.output
    assert expected_output_inv_xlsx_file in result.output
    assert expected_output_groups_xlsx_file in result.output
    assert expected_output_inv_nornir_file in result.output
    assert expected_output_groups_nornir_file in result.output
    assert expected_output_pyats_inv_file in result.output
    assert expected_output_inv_ansible_file in result.output


def test_convert_output_type_bad(runner):
    ot = "bad"
    result = runner.invoke(ms.convert, ["-o", ot])
    expected_block = f"Error: Invalid value for '--output-type' / '-o': invalid choice: {ot}. (choose from all, ansible, csv, json, nornir, pyats, xlsx)"  # noqa
    assert result.exit_code == 2
    assert expected_block in result.output
