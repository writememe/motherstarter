"""
motherstarter noxfile
"""
# Import modules
import nox


@nox.session(python=["3.7", "3.8", "3.9"])
def lint(session):
    """
    Run all linting tests.
    Nox run black, pylama, yamllint and bandit

    Args:
        session: nox session

    Returns:
        N/A

    Raises:
        N/A
    """
    session.install("-r", "requirements.txt")
    session.run("black", ".", "--check")
    session.run("pylama", ".")
    session.run("yamllint", ".")
    session.run(
        "bandit",
        "-v",
        "--exclude",
        "./venv",
        "--recursive",
        "--format",
        "json",
        "motherstarter/",
        "--verbose",
        "-s",
        "B101",
    )
    session.run("python", "-m", "mypy", "--strict", "motherstarter/")


@nox.session(python=["3.7", "3.8", "3.9"])
def black(session):
    """
    Nox run black

    Args:
        session: nox session

    Returns:
        N/A

    Raises:
        N/A

    """
    session.install("-r", "requirements.txt")
    session.run("black", ".", "--check")


@nox.session(python=["3.7", "3.8", "3.9"])
def pylama(session):
    """
    Nox run pylama

    Args:
        session: nox session

    Returns:
        N/A

    Raises:
        N/A

    """
    session.install("-r", "requirements.txt")
    session.run("pylama", ".")


@nox.session(python=["3.7", "3.8", "3.9"])
def yamllint(session):
    """
    Nox run yamllint

    Args:
        session: nox session

    Returns:
        N/A

    Raises:
        N/A

    """
    session.install("-r", "requirements.txt")
    session.run("yamllint", ".")


@nox.session(python=["3.7", "3.8", "3.9"])
def bandit(session):
    """
    Nox run bandit

    Args:
        session: nox session

    Returns:
        N/A

    Raises:
        N/A

    """
    session.install("-r", "requirements.txt")
    session.run(
        "bandit",
        "-v",
        "--exclude",
        "./venv",
        "--recursive",
        "--format",
        "json",
        "motherstarter/",
        "--verbose",
        "-s",
        "B101",
    )


@nox.session(python=["3.7", "3.8", "3.9"])
def mypy(session):
    """
    Nox run mypy

    Args:
        session: nox session

    Returns:
        None

    Raises:
        N/A
    """
    session.install("-r", "requirements.txt")
    session.run("python", "-m", "mypy", "--strict", "motherstarter/")


@nox.session(python=["3.7", "3.8", "3.9"])
def tests(session):
    """
    Nox run tests using pytest

    Args:
        session: nox session

    Returns:
        N/A

    Raises:
        N/A

    """
    session.install("-r", "requirements.txt")
    session.run("pytest", "--cov=./", "--cov-report=xml")
