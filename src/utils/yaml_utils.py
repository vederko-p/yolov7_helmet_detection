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
