# DevCheck – Packaged CLI Diagnostics Tool

## Project Overview

DevCheck is a Python command-line application developed as part of the RabTech Academy Python Software Engineering Internship.

It collects basic system information, checks configured developer tools, and generates diagnostic reports in human-readable or JSON format.

## Features

- Detects Python version and operating system.
- Checks available disk space.
- Reads selected environment variables.
- Detects configured developer tools such as Git, Python, pip, and VS Code.
- Supports custom JSON configuration.
- Generates human-readable and JSON reports.
- Saves reports to a specified file.
- Handles configuration and diagnostic errors with appropriate exit codes.
- Includes automated unit tests.

## Project Structure

```text
packaged-cli-diagnostics/
├── src/
│   └── devcheck/
│       ├── __init__.py
│       └── cli.py
├── tests/
│   └── test_cli.py
├── reports/
│   └── report.json
├── config.json
├── pyproject.toml
└── README.md
```

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Install the project:

```bash
python -m pip install -e .
```

## Usage

Run basic diagnostics:

```bash
devcheck
```

Generate a JSON report:

```bash
devcheck --json
```

Save a JSON report:

```bash
devcheck --json --output reports/report.json
```

Run diagnostics using a custom configuration:

```bash
devcheck --config config.json
```

Generate JSON using custom configuration:

```bash
devcheck --config config.json --json
```

Display help:

```bash
devcheck --help
```

## Configuration

DevCheck supports a JSON configuration file.

Example `config.json`:

```json
{
    "developer_tools": [
        "git",
        "python",
        "pip",
        "code"
    ]
}
```

The application checks the availability of the tools listed in this file.

## Testing

Run the complete unit test suite:

```bash
python -m unittest discover -s tests -v
```

The test suite covers:

1. Successful diagnostics.
2. Missing developer dependencies.
3. Invalid output paths.
4. Successful exit code.
5. Missing configuration files.
6. Invalid JSON configuration.

## Exit Codes

| Exit Code | Description |
|---|---|
| 0 | Successful execution |
| 1 | Diagnostic or output error |
| 2 | Configuration error |

## Technologies Used

- Python
- argparse
- JSON
- pathlib
- unittest
- setuptools

## Project Status

Core implementation, configurable diagnostics, report generation, error handling, and six unit tests have been completed.
