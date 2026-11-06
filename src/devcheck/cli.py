
import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path


DEFAULT_TOOLS = ["git", "python", "pip"]


class ConfigurationError(Exception):
    """Raised when the configuration is invalid."""


def load_config(config_path):
    """Load and validate developer tool configuration."""

    if config_path is None:
        return DEFAULT_TOOLS

    path = Path(config_path)

    if not path.exists() or not path.is_file():
        raise ConfigurationError(
            f"Configuration file not found: {path}"
        )

    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise ConfigurationError(
            f"Invalid configuration file: {error}"
        )

    if not isinstance(config, dict):
        raise ConfigurationError(
            "Configuration must be a JSON object."
        )

    tools = config.get("developer_tools")

    if (
        not isinstance(tools, list)
        or not tools
        or not all(
            isinstance(tool, str) and tool.strip()
            for tool in tools
        )
    ):
        raise ConfigurationError(
            "'developer_tools' must be a non-empty list of names."
        )

    return sorted(set(tool.strip() for tool in tools))


def run_diagnostics(configured_tools=None):
    """Collect basic system diagnostic information."""

    if configured_tools is None:
        configured_tools = DEFAULT_TOOLS

    results = {}

    results["python_version"] = platform.python_version()
    results["operating_system"] = platform.system()

    disk = shutil.disk_usage(Path.home())

    results["disk_space"] = {
        "total_gb": round(disk.total / (1024 ** 3), 2),
        "free_gb": round(disk.free / (1024 ** 3), 2)
    }

    # Avoid exposing the complete PATH environment variable.
    results["environment_variables"] = {
        "HOME": str(Path.home()),
        "TEMP": os.environ.get("TEMP", "")
    }

    results["developer_tools"] = {
        tool: shutil.which(tool) is not None
        for tool in sorted(configured_tools)
    }

    return results


def format_report(report):
    """Create a human-readable diagnostic report."""

    output = "DEVCheck System Diagnostics\n"
    output += "=" * 35 + "\n"

    for key, value in report.items():
        output += f"\n{key.replace('_', ' ').title()}:\n"

        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                output += f"  {subkey}: {subvalue}\n"
        else:
            output += f"  {value}\n"

    return output


def main():
    parser = argparse.ArgumentParser(
        description="DevCheck - System Diagnostics Tool"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate JSON report"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Save report to a file"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to JSON configuration file"
    )

    args = parser.parse_args()

    try:
        configured_tools = load_config(args.config)
    except ConfigurationError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2

    try:
        report = run_diagnostics(configured_tools)

        if args.json:
            output = json.dumps(report, indent=4)
        else:
            output = format_report(report)

        if args.output:
            Path(args.output).write_text(
                output, encoding="utf-8"
            )
            print(f"Report saved to {args.output}")
        else:
            print(output)

        return 0

    except (OSError, ValueError) as error:
        print(f"Diagnostic error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
