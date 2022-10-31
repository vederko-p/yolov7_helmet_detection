import yaml

from common.dataset_config import DATASETS_METADATA_PATH


if __name__ == '__main__':
    with open(DATASETS_METADATA_PATH, 'r') as yaml_file:
        ds_meta = yaml.load(yaml_file, Loader=yaml.Loader)
    print(ds_meta)
