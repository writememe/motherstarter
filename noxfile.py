"""
motherstarter noxfile
"""
# Import modules
import nox


@nox.session(python=["3.8"])
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
    session.run("black", "--check", ".")


@nox.session(python=["3.8"])
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


@nox.session(python=["3.8"])
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


@nox.session(python=["3.8"])
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
        ".",
        "--verbose",
        "-s",
        "B101",
    )


@nox.session(python=["3.8"])
def pytest(session):
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
