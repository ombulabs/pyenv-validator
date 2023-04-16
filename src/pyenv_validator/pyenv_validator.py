"""Define environment variable validator module."""
import logging
import os
import re
import sys
import uuid
from pathlib import Path

log = logging.getLogger(__name__)

FORMATS = {
    "str": str,
    "string": str,
    "String": str,
    "email": lambda x: re.match(r"[^@]+@[^@]+\.[^@]+", x),
    "url": lambda x: re.match(r"https?://[^\s/$.?#].\S*", x),
    "bool": lambda x: x.lower() in ("true", "false"),
    "boolean": lambda x: x.lower() in ("true", "false"),
    "Boolean": lambda x: x.lower() in ("true", "false"),
    "uuid": lambda x: uuid.UUID(x, version=4),
}


def get_env_file() -> dict[str, list]:
    """Retrieve and parse .env.example file is one exists."""
    env_example_file = Path.cwd() / ".env.example"
    if not env_example_file.exists():
        log.error("pyenv_validator: The .env.example file is missing.")
        sys.exit(-1)
    with env_example_file.open() as file:
        env_example = file.readlines()
    return {
        "required": [
            parse_line(line)
            for line in remove_comments(env_example)
            if "required" in line.lower()
        ],
        "optional": [
            parse_line(line)
            for line in remove_comments(env_example)
            if "required" not in line.lower()
        ],
    }


def remove_comments(lines: list[str]) -> list[str]:
    """Remove comment lines i.e. lines starting with #."""
    return [
        line for line in lines if line.strip() and not line.startswith("#")
    ]


def parse_line(line: str) -> dict[str, str | None]:
    """Turn each line into a dictionary with variable name and format."""
    value_match = re.search(r"format=(.*)", line)
    value = value_match.group(1) if value_match else None
    return {line.split("=")[0].strip(): value}


def is_valid_format(env_var: dict) -> bool:
    """Check if the env variable is set in the expected format."""
    name, expected_format = next(iter(env_var.items()))
    if env_var[name] not in FORMATS:
        return False
    return bool(FORMATS[expected_format](os.environ[name]))  # type: ignore


def build_error_string(var_list: list[dict]) -> str:
    """Build format error string from list of variables."""
    error_list = [
        f"\n {variable['name']}: expected format {variable['expected']}"
        for variable in var_list
        if variable
    ]
    return "".join(error_list)


def check_missing_variables(required_envs: list[dict]) -> None:
    """Check that no required variables are missing from the environment."""
    missing = [
        list(variable.keys())[0]
        for variable in required_envs
        if list(variable.keys())[0] not in os.environ
    ]
    if missing:
        PyenvValidator.errors.append(
            f"pyenv_validator: The following env variables are missing: {', '.join(missing)}"  # noqa=E501
        )


def check_format(required_envs: list[dict]) -> None:
    """Check that all defined variables are set with the right format."""
    invalid_format = [
        {"name": name, "expected": value}
        for variable in required_envs
        for name, value in variable.items()
        if name in os.environ
        and value is not None
        and not is_valid_format(variable)
    ]
    if invalid_format:
        PyenvValidator.errors.append(
            f"pyenv_validator: The following env variables are set in the wrong format: "  # noqa=E501
            f"{build_error_string(invalid_format)}"
        )


class PyenvValidator:
    """Validate that environment variables are present."""

    errors: list[str] = []

    @classmethod
    def check(cls) -> None:
        """Check for missing or invalid environment variables."""
        required_envs = get_env_file()
        check_missing_variables(required_envs["required"])
        check_format(required_envs["required"] + required_envs["optional"])
        if cls.errors:
            log.error("\n".join(cls.errors))
            sys.exit(-1)
