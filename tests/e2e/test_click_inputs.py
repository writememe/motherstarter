"""
This is where I am testing inputs via the CLI
"""

# Import modules
from click.testing import CliRunner
import pytest
from motherstarter import motherstarter as ms
import traceback

# Import motherstarter version so we can validate
# it from the command-line
from motherstarter import __version__


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_convert_default(runner):
    """
    Test the default motherstarter convert
    options from the command-line.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Execute command and assign to variable
    result = runner.invoke(ms.cli, ["convert"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Assign expected strings to variables, for further validation.
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
    # Assign expected strings to variables, for further validation.
    expected_source_dir_start = "DEBUG - Source directory is: "
    expected_source_dir_end = "motherstarter/inputs/"
    expected_template_dir_start = "DEBUG - Source template directory is: "
    expected_template_dir_end = "motherstarter/templates/core/"
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir_start in result.output
    assert expected_source_dir_end in result.output
    assert expected_template_dir_start in result.output
    assert expected_template_dir_end in result.output


def test_base_version(runner):
    """
    Test that the motherstarter version returned from
    the command-line is the expected version.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Execute command and assign to variable
    result = runner.invoke(ms.cli, ["--version"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Use the imported motherstarter version from the import
    # and assign to a variable
    expected = __version__
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected in result.output


def test_base_help(runner):
    """
    Test that the motherstarter help command operates
    as expected.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Execute command and assign to variable

    result = runner.invoke(ms.cli, ["--help"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Assign expected strings to variables, for further validation.
    expected_usage = "Usage: cli [OPTIONS] COMMAND [ARGS]."
    expected_convert = (
        "convert  Convert source file(s) into network automation inventory outputs"
    )
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_usage in result.output
    assert expected_convert in result.output


def test_convert_help(runner):
    """
    Test that the motherstarter convert help command operates
    as expected.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["--help"])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Assign expected strings to variables, for further validation.
    expected_usage = "Usage: convert [OPTIONS]"
    expected_convert = (
        "Convert source file(s) into network automation inventory outputs based on"
        "\n  multiple command-line inputs"
    )
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_usage in result.output
    assert expected_convert in result.output


def test_convert_source_type_csv(runner):
    """
    Test that the motherstarter convert with a source type
    of csv works as expected.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign source_type of csv to a variable
    st = "csv"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Assign expected strings to variables, for further validation.
    expected_block = f"DEBUG - Inventory source type is {st}"
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_block in result.output


def test_convert_source_type_json(runner):
    """
    Test that the motherstarter convert with a source type
    of json works as expected.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign source_type of json to a variable
    st = "json"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Assign expected strings to variables, for further validation.
    expected_block = f"DEBUG - Inventory source type is {st}"
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_block in result.output


def test_convert_source_type_xlsx(runner):
    """
    Test that the motherstarter convert with a source type
    of xlsx works as expected.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign source_type of xlsx to a variable
    st = "xlsx"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-st", st])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Assign expected strings to variables, for further validation.
    expected_block = f"DEBUG - Inventory source type is {st}"
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_block in result.output


def test_convert_source_type_bad(runner):
    """
    Test that the motherstarter convert with a source type
    of bad fails as expected.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign source_type of bad to a variable
    st = "bad"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-st", st])
    # Assign expected strings to variables, for further validation.
    expected_block = f"Error: Invalid value for '--source-type' / '-st': invalid choice: {st}. (choose from csv, json, xlsx)"  # noqa
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 2
    assert expected_block in result.output


def test_convert_source_dir_custom(runner):
    """
    Test that the motherstarter convert with a custom source dir
    of works as expected.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign custom source_dir to a variable
    sd = "tests/test_data/inputs/core"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-sd", sd])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Assign expected strings to variables, for further validation.
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    expected_source_dir_start = "DEBUG - Source directory is: "
    expected_source_dir_end = f"{sd}"
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir_start in result.output
    assert expected_source_dir_end in result.output


def test_convert_source_dir_bad(runner):
    """
    Test that the motherstarter convert with a bad custom source dir
    of fails as expected.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign bad custom source_dir to a variable
    sd = "tests/test_data/inputs/core/bad"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-sd", sd])
    # Assert that this fails with an exit code of 1
    assert result.exit_code == 1


def test_convert_log_level_debug(runner):
    """
    Test that the motherstarter log level of DEBUG
    works as expected

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign log level to a variable
    ll = "debug"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Assign expected strings to variables, for further validation.
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    # Assert that there is no ERROR or CRITICAL log errors.
    assert "ERROR -" not in result.output
    assert "CRITICAL -" not in result.output


def test_convert_log_level_info(runner):
    """
    Test that the motherstarter log level of INFO
    works as expected

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign log level to a variable
    ll = "info"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    # Assert that there is no DEBUG, ERROR or CRITICAL log errors.
    assert "DEBUG -" not in result.output
    assert "ERROR -" not in result.output
    assert "CRITICAL -" not in result.output


def test_convert_log_level_warning(runner):
    """
    Test that the motherstarter log level of WARNING
    works as expected

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign log level to a variable
    ll = "warning"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    # Assert that there is no DEBUG, INFO, ERROR or CRITICAL log errors.
    assert "DEBUG -" not in result.output
    assert "INFO -" not in result.output
    assert "ERROR -" not in result.output
    assert "CRITICAL -" not in result.output


def test_convert_log_level_error(runner):
    """
    Test that the motherstarter log level of ERROR
    works as expected

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign log level to a variable
    ll = "error"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    # Assert that there is no DEBUG, INFO, WARNING or CRITICAL log errors.
    assert "DEBUG -" not in result.output
    assert "INFO -" not in result.output
    assert "WARNING -" not in result.output
    assert "CRITICAL -" not in result.output


def test_convert_log_level_critical(runner):
    """
    Test that the motherstarter log level of CRITICAL
    works as expected

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign log level to a variable
    ll = "critical"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-l", ll])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    # Assert that there is no DEBUG, INFO, WARNING or ERROR log errors.
    assert "DEBUG -" not in result.output
    assert "INFO -" not in result.output
    assert "WARNING -" not in result.output
    assert "ERROR -" not in result.output


def test_convert_log_level_bad(runner):
    """
    Test that the motherstarter log level of bad
    failes as expected

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign log level to a variable
    ll = "bad"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-l", ll])
    # Assign expected strings to variables, for further validation.
    expected_block = f"Error: Invalid value for '--log-level' / '-l': invalid choice: {ll}. (choose from debug, info, warning, error, critical)"  # noqa
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 2
    assert expected_block in result.output


def test_convert_template_dir_custom(runner):
    """
    Test that the motherstarter convert with a custom template
    directory works as expected

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign the custom directory to a variable
    td = "tests/test_data/templates/custom"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-td", td])
    if result.exception:
        traceback.print_exception(*result.exc_info)  # noqa
    # Assign expected strings to variables, for further validation.
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    expected_source_dir_start = "DEBUG - Source directory is: "
    expected_source_dir_end = "motherstarter/inputs/"
    expected_template_dir = f"DEBUG - Source template directory is: {td}"
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir_start in result.output
    assert expected_source_dir_end in result.output
    assert expected_template_dir in result.output


def test_convert_template_dir_bad(runner):
    """
    Test that the motherstarter convert with a bad custom template
    directory fails as expected

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign custom source_dir to a variable
    td = "tests/test_data/templates/bad"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-td", td])
    # Assign expected strings to variables, for further validation.
    expected_source_type = "DEBUG - Inventory source type is json"
    expected_output_type = "DEBUG - Output type is: all"
    expected_source_dir_start = "DEBUG - Source directory is: "
    expected_source_dir_end = "motherstarter/inputs/"
    expected_template_dir = f"DEBUG - Source template directory is: {td}"
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 1
    assert expected_source_type in result.output
    assert expected_output_type in result.output
    assert expected_source_dir_start in result.output
    assert expected_source_dir_end in result.output
    assert expected_template_dir in result.output


def test_convert_output_type_csv(runner):
    """
    Test that the motherstarter convert outputs CSV
    files to the correct location.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign output_type to a variable
    ot = "csv"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-o", ot])
    # Assign expected strings to variables, for further validation.
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/inventory.{ot}"
    )
    expected_output_groups_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/groups.{ot}"
    )
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output
    assert expected_output_groups_file in result.output


def test_convert_output_type_json(runner):
    """
    Test that the motherstarter convert outputs json
    files to the correct location.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign output_type to a variable
    ot = "json"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-o", ot])
    # Assign expected strings to variables, for further validation.
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/inventory.{ot}"
    )
    expected_output_groups_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/groups.{ot}"
    )
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output
    assert expected_output_groups_file in result.output


def test_convert_output_type_xlsx(runner):
    """
    Test that the motherstarter convert outputs xlsx
    files to the correct location.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign output_type to a variable
    ot = "xlsx"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-o", ot])
    # Assign expected strings to variables, for further validation.
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/inventory.{ot}"
    )
    expected_output_groups_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/groups.{ot}"
    )
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output
    assert expected_output_groups_file in result.output


def test_convert_output_type_nornir(runner):
    """
    Test that the motherstarter convert outputs nornir
    files to the correct location.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign output_type to a variable
    ot = "nornir"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-o", ot])
    # Assign expected strings to variables, for further validation.
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        "INFO - File output location: motherstarter/outputs/nr/inventory/groups.yaml"
    )
    expected_output_groups_file = (
        "INFO - File output location: motherstarter/outputs/nr/inventory/hosts.yaml"
    )
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output
    assert expected_output_groups_file in result.output


def test_convert_output_type_pyats(runner):
    """
    Test that the motherstarter convert outputs pyats
    files to the correct location.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign output_type to a variable
    ot = "pyats"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-o", ot])
    # Assign expected strings to variables, for further validation.
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = f"INFO - File output location: motherstarter/outputs/{ot}/mother_starter_tb.yaml"  # noqa
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output


def test_convert_output_type_ansible(runner):
    """
    Test that the motherstarter convert outputs ansible
    files to the correct location.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign output_type to a variable
    ot = "ansible"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-o", ot])
    # Assign expected strings to variables, for further validation.
    expected_output_type = f"DEBUG - Output type is: {ot}"
    expected_output_inv_file = (
        f"INFO - File output location: motherstarter/outputs/{ot}/inventory/hosts"
    )
    # Perform assertion tests to ensure variables are in the expected outputs
    assert result.exit_code == 0
    assert expected_output_type in result.output
    assert expected_output_inv_file in result.output


def test_convert_output_type_all(runner):
    """
    Test that the motherstarter convert outputs all
    files to the correct location.

    Args:
        runner: The runner which simulates command-line
        inputs, replicating an end user.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Assign output_type to a variable
    ot = "all"
    # Execute command and assign to variable
    result = runner.invoke(ms.convert, ["-o", ot])
    # Assign expected strings to variables, for further validation.
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
    # Perform assertion tests to ensure variables are in the expected outputs
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
