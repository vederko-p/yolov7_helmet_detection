import os


def make_directory(directory_path: str, directory_name: str) -> None:
    if os.path.isdir(directory_path):
        directory_full_path = os.path.join(directory_path, directory_name)
        if not os.path.isdir(directory_full_path):
            os.mkdir(directory_full_path)
    else:
        raise Exception(f'Directory {directory_path} doesn\'t exist')
