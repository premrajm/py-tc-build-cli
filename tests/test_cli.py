import pytest
from click.testing import CliRunner
from tc import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_status(runner):
    result = runner.invoke(cli.status)
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == 'SUCCESS'
