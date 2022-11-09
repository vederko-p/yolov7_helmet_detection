from typing import List

from yaml import load, Loader
from yaml import dump


def read_yaml(filepath: str) -> dict:
    """Open yaml file."""
    with open(filepath, 'r') as yaml_file:
        data = load(yaml_file, Loader=Loader)
    return data


def save_yaml(filepath: str, data) -> None:
    """Save data into yaml file"""
    with open(filepath, 'w') as yaml_file:
        output = dump(data, yaml_file)


def read_file_lines(filepath: str) -> List[str]:
    """Read lines from file withouh new line symbols."""
    with open(filepath, 'r') as file:
        lines = list(map(lambda s: s[:-1], file.readlines()))
    return lines


def save_lines_into_file(
    filepath: str,
    lines: List[str],
    read_mode: str = 'w'
) -> None:
    """Save lines of strings withouh new line symbols into file."""
    lines_eol = map(lambda line: f'{line}\n', lines)
    with open(filepath, read_mode) as file:
        file.writelines(lines_eol)
