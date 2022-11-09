from typing import Tuple, Union


def convert_annot_xywh2xyxy(
    bx: float, by: float, bw: float, bh: float,
    img_w: Union[float, int], img_h: Union[float, int]
) -> Tuple[int, int, int, int]:
    """Convert yolo-like box annotation into
    top-left bottom-right box annotation.
    
    Parameters
    ----------
    bx: float
        Box x center.
    by: float
        Box y center.
    bw: float
        Box width.
    bh: float
        Box height.
    img_w: Union[float, int]
        Image width.
    img_h: Union[float, int]
        Image height.
    
    Returns
    -------
    left_x : int
        Box left x.
    top_y : int
        Box top y.
    right_x : int
        Box right x.
    botom_y : int
        Box bottom y."""
    left_x = int((bx - bw/2)*img_w)
    top_y = int((by - bh/2)*img_h)
    right_x = int((bx + bw/2)*img_w)
    botom_y = int((by + bh/2)*img_h)
    return left_x, top_y, right_x, botom_y


def convert_annot_xyxy2xywh(
    blx: int, bty: int, brx: int, bby: int,
    img_w: Union[float, int], img_h: Union[float, int]
) -> Tuple[float, float, float, float]:
    """Convert top-left bottom-right box annotation
    into yolo-like box annotation.
    Parameters
    ----------
    left_x : int
        Box left x.
    top_y : int
        Box top y.
    right_x : int
        Box right x.
    botom_y : int
        Box bottom y.
    img_w: Union[float, int]
        Image width.
    img_h: Union[float, int]
        Image height.
    
    Returns
    -------
    bx: float
        Box x center.
    by: float
        Box y center.
    bw: float
        Box width.
    bh: float
        Box height."""
    b_center_x = ((blx + brx) / 2) / img_w
    b_center_y = ((bty + bby) / 2) / img_h
    b_width = (brx - blx) / img_w
    b_height = (bby - bty) / img_h
    return b_center_x, b_center_y, b_width, b_height
