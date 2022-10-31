from yaml import load, Loader


def open_yaml(filepath: str) -> dict:
    """Open yaml file."""
    with open(filepath, 'r') as yaml_file:
        data = load(yaml_file, Loader=Loader)
    return data
