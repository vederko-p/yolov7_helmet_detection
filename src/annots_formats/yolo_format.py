import sys
sys.path.append('../')

from typing import List
from src.utils import files_utils


class YoloObjectAnnotation:
    """Instance suppose to be an annotation of one object."""
    
    def __init__(self):
        self.class_id = None
        self.x, self.y = None, None
        self.w, self.h = None, None
        
    def fill_from_string(self, annot_str: str):
        """Convert string annotation of one object into
        atributes of instance.
        
        Parameters
        ----------
        annot_str: str
            YOLO-like object annotatoin string."""
        annot_parts = annot_str.split(' ')
        self.class_id = int(annot_parts[0])
        self.x, self.y = float(annot_parts[1]), float(annot_parts[2])
        self.w, self.h = float(annot_parts[3]), float(annot_parts[4])
        
    def change_class_id(self, new_class_id):
        """Change class id of object (instance)."""
        self.class_id = new_class_id
        return self


class YoloAnnotation:
    """Instance suppose to be a set of objects annotations for
    one image."""
    
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.objects_annots = None
        
    def read_annotfile(self) -> None:
        """Read annot file into instance attributes."""
        annot_strings = files_utils.read_file_lines(self.filepath)
        objects_annots = []
        for s_annot in annot_strings:
            obj_annot = YoloObjectAnnotation()
            obj_annot.fill_from_string(s_annot)
            objects_annots.append(obj_annot)
        self.objects_annots = objects_annots
        
    def filter_map_annots_class(self, classes_map: dict) -> None:
        """Filter off image annotations due to classes map.
        
        Parameters
        ----------
        classes_map: dict
            Dict like {class_id: mark, ...}, where
            mark either None or int object. None means that
            class_id is not used and will be filtered out. Int
            value is the corresponding mapping of class_id."""
        self.objects_annots = map(
            lambda obj_an: obj_an.change_class_id(
                classes_map[obj_an.class_id]),
            filter(
                lambda obj_an:
                classes_map.get(obj_an.class_id) is not None,
                self.objects_annots
            )
        )
        
    def annots_to_strings(self) -> List[str]:
        """Convert objects annotations into lines of YOLO string
        annotation format."""
        str_annots = [
            f'{obj_an.class_id} {obj_an.x} {obj_an.y} {obj_an.w} {obj_an.h}'
            for obj_an in self.objects_annots
        ]
        return str_annots
        
    def save_annot(self, filepath):
        """Save objects annotations into string YOLO format."""
        string_annots = self.annots_to_strings()
        files_utils.save_lines_into_file(filepath, string_annots)
