import os
import sys
sys.path.append('../')

from random import sample
from time import strftime
from typing import List, Tuple

from src.common.dataset_config import (DATASETS_DIRECTORY_PATH,
                                       DATASETS_METADATA_FILENAME)

from src.utils import files_utils, folders_utils
from src.utils.random_utils import handle_random_state
from src.utils.iter_utils import flatten

from src.annots_formats.yolo_format import YoloAnnotation


def get_ds_classes_meta(
    ds_class_params: dict,
    ds_meta: dict
) -> dict:
    """Get dataset new classes mapping after split.
    
    Parameters
    ----------
    ds_class_params: dict
        Dataset parameters from split_config file, describing
        new:old_list classes mapping.
        
    ds_meta: dict
        Metadata about dataset from datasets_meta file.
    
    Returns
    -------
    ds_classes_meta: dict
        Dict like {old_cl_id: new_class_id, ...}, where
        new_class_id either None or int object. None means that
        old_cl_id is not used in the sought dataset. Int value
        is the corresponding mapping of old_cl_id in space of
        new class ids."""
    
    all_ds_classes = set(ds_meta['classes'].keys())
    ds_classes_in_use = set()
    ds_classes_meta = {}
    for new_class_id, old_classes_ids in ds_class_params.items():
        for old_cl_id in old_classes_ids:
            ds_classes_meta[old_cl_id] = new_class_id
            ds_classes_in_use.add(old_cl_id)
    ds_complement_classes = all_ds_classes - ds_classes_in_use
    for cl_id in ds_complement_classes:
        ds_classes_meta[cl_id] = None
    return ds_classes_meta


def get_sizes(coefs: List[float], total_size: int) -> List[int]:
    """Get sizes due to split coefs.
    
    Parameters
    ----------
    coefs: List[float]
        List of coefs.
    total_size: int
        Total size of dataset.
        
    Returns
    -------
    sizes: List[int]
        List of corresponding sizes."""
    sizes = [int(coef*total_size) for coef in coefs[:-1]]
    sizes.append(total_size-sum(sizes))
    return sizes


def get_slices(sizes: List[int]) -> List[Tuple[int, int]]:
    """Get slices borders from list of sizes."""
    slices = []
    for i in range(len(sizes)):
        s = sum(sizes[:i])
        left, right = s, sizes[i] + s
        slices.append((left, right))
    return slices


def split_list(
    lst: List[int],
    slices: List[Tuple[int, int]],
    random_state: int = None
) -> List[List[int]]:
    """Split list due slices."""
    handle_random_state(random_state)
    lst_sample = sample(lst, len(lst))
    splits = [lst_sample[s[0]: s[1]].copy() for s in slices]
    return splits


def split_indexes(
    indexes: List[int],
    splits: dict,
    total_size: int,
    random_state: int = None
) -> Tuple[List[str], List[List[int]]]:
    """Split indexes of dataset into subsets.
    
    Parameters
    ----------
    indexes: List[int]
        Source list of indexes.
    splits: dict
        Configuration of split dict like {split_name: coeff, ...}.
    total_size: int  # TODO: calculate this param instead of get as argument.
        Size of indexes.  
    random_state: Union[int, None]
        Random state.
    
    Returns
    -------
    splits_names: List[str]
        List of names of splits.
    split_target: List[List[int]]
        List of corresponding to split name lists of indexes."""
    # splits configuration:
    splits_names = list(splits.keys())
    splits_coefs = [splits[k] for k in splits_names]
    # prepare slices:
    splits_sizes = get_sizes(splits_coefs, total_size)
    split_slices = get_slices(splits_sizes)
    # split:
    split_target = split_list(indexes, split_slices, random_state)
    return splits_names, split_target


# TODO: Should reformat the way to reformat labels if any other
# annotations format will appear.
# Most likely add annotations container as arguments for this func.
def reformat_labels(
    dataset_path: str,
    ds_folder: str,
    splited_indexes: List[List[int]],
    all_ds_indexes: dict,
    classes_meta: dict,
    lbls_dir: str
) -> None:
    """Reformat labels due to new dataset classes and for yolo train.
    
    Parameters
    ----------
    dataset_path: str
        Path to dataset root directory.
    ds_folder: str
        Dataset folder name.
    splited_indexes: List[List[int]]
        Dataset splited indexes.
    all_ds_indexes: dict
        All indexes of all datasets.
    classes_meta: dict
        Dict like {class_id: mark, ...}, where
        mark either None or int object. None means that
        class_id is not used and will be filtered out. Int
        value is the corresponding mapping of class_id .
    lbls_dir: str
        The sought labels directory name
    """
    ds_folder_path = os.path.join(dataset_path, ds_folder)
    folders_utils.make_directory(ds_folder_path, lbls_dir)
    new_labels_dir = os.path.join(ds_folder_path, lbls_dir)
    for label_indx in flatten(splited_indexes):
        old_lbl_path = os.path.join(
            ds_folder_path, all_ds_indexes[label_indx])
        yolo_annot = YoloAnnotation(old_lbl_path)
        yolo_annot.read_annotfile()
        yolo_annot.filter_map_annots_class(classes_meta)
        new_lbl_filepath = os.path.join(
            ds_folder_path, lbls_dir,
            os.path.basename(all_ds_indexes[label_indx]))
        yolo_annot.save_annot(new_lbl_filepath)


# TODO: Should reformat the way to make folders if any other
# annotations format will appear.
def make_yolo_dir_with_paths(
    ds_path: str,
    main_dirname: str = 'yolo_collected_datasets'
) -> str:
    """Create directory for split files with paths for yolo config.
    
    Parameters
    ----------
    ds_path: str
        Dataset path.
    main_dirname: str
        Name of main folder for yolo files.
        
    Returns
    -------
    sub_folder_path: str
        Subfolder for split files path.
    """
    # make main folder:
    folders_utils.make_directory(ds_path, main_dirname)
    main_folder_path = os.path.join(ds_path, main_dirname)
    # make sub folder for files with paths:
    current_time = strftime('%y-%m-%d_%H-%M-%S')
    folders_utils.make_directory(main_folder_path, current_time)
    sub_folder_path = os.path.join(main_folder_path, current_time)
    return sub_folder_path


def add_paths_to_file(
    splited_indexes: List[List[int]],
    splited_names: List[str],
    folder_path: str,
    all_ds_indexes: dict,
    ds_path: str
) -> List[str]:
    """Make yolo data files ~ splited files with paths to images.
    
    Parameters
    ----------
    splited_indexes: List[List[int]]
        Dataset splited indexes.
    splited_names: List[str]
       Split names.
    folder_path: str
        Yolo data files folder path.
    all_ds_indexes: dict
        All indexes of all datasets.
    ds_path:
        Path to dataset root directory.
    
    Returns
    -------
    out_files_paths: List[str]
        List of paths to sought splits.
    """
    out_files_paths = []
    for s_name, s_indxs in zip(splited_names, splited_indexes):
        filepath = os.path.join(folder_path, f'{s_name}.txt')
        out_files_paths.append(filepath)
        lines = map(
            lambda indx: os.path.join(
                ds_path, all_ds_indexes[indx].replace('.txt', '.jpg')),  # TODO: Fix replace (make indexes from images instead of labels)
            s_indxs)
        files_utils.save_lines_into_file(filepath, lines, read_mode='a')
    return out_files_paths


# TODO: Should reformat the way to make folders if any other
# annotations format will appear.
def make_yolo_data(
    filepath: str,
    spl_cl_map: dict,
    split_names: List[str],
    out_files_paths: List[str],
    dataset_path: str
) -> None:
    """Make yolo data files.
    
    Parameters
    ----------
    filepath: str
        Yolo data file path.
    spl_cl_map: dict
        New classes mapping from split config.
    split_names: List[str]
        Names of splits.
    out_files_paths: List[str]
        Path to separate split data files.
    dataset_path: str
        Path to dataset root directory.
    """
    splits = zip(split_names, out_files_paths)
    split_paths = map(lambda s : f'{s[0]}: {s[1]}', splits)
    cl_amount = len(spl_cl_map)
    cl_names = [spl_cl_map[k] for k in sorted(spl_cl_map.keys())]
    yolo_cfg_lines = (
        ['# train and val data']
        + [f'path: {dataset_path}']
        + list(split_paths)
        + ['']
        + ['# number of classes']
        + [f'nc: {cl_amount}']
        + ['']
        + ['# class names']
        + [f'names: {cl_names}']
    )
    files_utils.save_lines_into_file(filepath, yolo_cfg_lines)


def split_and_collect_labels(
    split_config: dict,
    ds_meta: dict
) -> None:
    """Collect all datasets and split them into part due to split config.
    
    Parameters
    ----------
    split_config: dict
        Split config.
    ds_meta: dict
        Dataset meta.
    """
    # metainfo:
    split_params = split_config['split']
    indexes = files_utils.read_yaml(split_params['indexing_path'])
    dataset_path = indexes['dataset_path']
    # main folder for yolo files with paths:
    splited_files_folder_path = make_yolo_dir_with_paths(
        dataset_path)
    for ds_key, class_params in split_config['datasets'].items():
        # dataset split:
        split_names, splited_indexes = split_indexes(
            list(indexes[ds_key].keys()), split_params['parts'],
            len(indexes[ds_key]), split_params['random_state'])
        # reformat and save labels:
        current_ds_folder_path = os.path.join(dataset_path, ds_key)
        ds_classes_meta = get_ds_classes_meta(
            split_config['datasets'][ds_key]['classes'],
            ds_meta[ds_key])
        lbls_dir = 'labels'  # TODO: Fix implicit usage
        reformat_labels(
            dataset_path, ds_key, splited_indexes, indexes[ds_key],
            ds_classes_meta, lbls_dir)
        lbls_dir
        new_ds_indx_paths = {
            i: pth.replace(
                ds_meta[ds_key]['labels_directory'],
                ds_meta[ds_key]['images_directory'])
            for i, pth in indexes[ds_key].items()}
        # add splited filepaths into sought files with paths:
        out_files_paths = add_paths_to_file(
            splited_indexes, split_names,
            splited_files_folder_path,
            new_ds_indx_paths,
            current_ds_folder_path)
        break
    # make data file to train yolo:
    yolo_data_filepath = os.path.join(
        splited_files_folder_path, 'yolo_data.yaml')
    make_yolo_data(
        yolo_data_filepath, split_config['class_mapping'],
        split_names, out_files_paths, dataset_path
    )


def main():
    split_config_filepath = '../common/split_dataset_configs/split_dataset_config_test.yaml'
    split_config = files_utils.read_yaml(split_config_filepath)
    metadata_filepath = os.path.join(
        DATASETS_DIRECTORY_PATH, DATASETS_METADATA_FILENAME)
    ds_metadata_dict = files_utils.read_yaml(metadata_filepath)
    split_and_collect_labels(split_config, ds_metadata_dict)


if __name__ == '__main__':
    main()
