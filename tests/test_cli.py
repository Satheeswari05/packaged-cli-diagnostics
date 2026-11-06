from contextlib import redirect_stdout
import tempfile
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from devcheck.cli import main
import unittest
from unittest.mock import patch
from devcheck.cli import run_diagnostics


class TestDiagnostics(unittest.TestCase):

    def test_diagnostics_success(self):
        result = run_diagnostics()

        self.assertIn("python_version", result)
        self.assertIn("operating_system", result)
        self.assertIn("disk_space", result)
        self.assertIn("developer_tools", result)

    @patch("devcheck.cli.shutil.which")
    def test_missing_dependency(self, mock_which):
        mock_which.return_value = None

        result = run_diagnostics()

        self.assertFalse(result["developer_tools"]["git"])
        self.assertFalse(result["developer_tools"]["python"])
        self.assertFalse(result["developer_tools"]["pip"])

    def test_invalid_output_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_path = Path(temp_dir) / "missing" / "report.json"

            with patch("sys.argv", [
                "devcheck",
                "--output",
                str(invalid_path)
            ]):
                error_output = StringIO()

                with redirect_stderr(error_output):
                    result = main()

            self.assertEqual(result, 1)
    @patch("sys.argv", ["devcheck"])
    def test_success_exit_code(self):
        output = StringIO()

        with redirect_stdout(output):
            result = main()

        self.assertEqual(result, 0)
    def test_missing_config_file(self):
        with patch("sys.argv", [
            "devcheck",
            "--config",
            "missing.json"
        ]):
            error_output = StringIO()

            with redirect_stderr(error_output):
                result = main()

        self.assertEqual(result, 2)
        self.assertIn(
            "Configuration file not found",
            error_output.getvalue()
        )

    def test_invalid_json_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config_path.write_text(
                "{ invalid json }",
                encoding="utf-8"
            )

            with patch("sys.argv", [
                "devcheck",
                "--config",
                str(config_path)
            ]):
                error_output = StringIO()

                with redirect_stderr(error_output):
                    result = main()

        self.assertEqual(result, 2)
        self.assertIn(
            "Invalid configuration file",
            error_output.getvalue()
        )
if __name__ == "__main__":
    unittest.main()
