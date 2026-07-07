from click.testing import CliRunner

from reqkit.cli import main


FIXTURES = "tests/fixtures/reqkit"


def test_parse_smoke():
    result = CliRunner().invoke(main, ["parse", FIXTURES])

    assert result.exit_code == 0, result.output
