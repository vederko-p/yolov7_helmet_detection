import sys
sys.path.append('../')

import os
from time import strftime

from common.dataset_config import DATASETS_DIRECTORY_PATH
from common.dataset_config import DATASETS_METADATA_FILENAME
from utils import yaml_utils, folders_utils


def indexing(dataset_path: str, dataset_meta_file_name: str) -> dict:
    meta_file_path = os.path.join(dataset_path, dataset_meta_file_name)
    ds_metadata = yaml_utils.read_yaml(meta_file_path)
    indexes_dict = {'dataset_path': dataset_path}
    for ds_key, ds_meta in ds_metadata.items():
        ds_labels_path = os.path.join(
            dataset_path,
            ds_meta['folder_name'],
            ds_meta['labels_directory'])
        labels_files = os.listdir(ds_labels_path)
        labels_ds_path = map(
            lambda lbl_loc_p: os.path.join(
                ds_meta['folder_name'], lbl_loc_p),
            labels_files)
        ds_indexing_dict = {
            index: lbl_p for index, lbl_p
            in zip(range(len(labels_files)), labels_ds_path)
        }
        indexes_dict[ds_key] = ds_indexing_dict.copy()
    return indexes_dict


def main():
    index_output = indexing(
        DATASETS_DIRECTORY_PATH, DATASETS_METADATA_FILENAME)

    index_folder_path = '.'
    index_folder_name = 'last_indexes'
    folders_utils.make_directory(index_folder_path, index_folder_name)

    current_time = strftime('%y-%m-%d_%H-%M-%S')
    index_filepath = f'./{index_folder_name}/indexing_{current_time}.yaml'
    yaml_utils.save_yaml(index_filepath, index_output)    


if __name__ == '__main__':
    main()
