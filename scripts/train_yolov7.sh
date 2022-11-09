# start yolo training
YOLO_DIR="../src/models/yolov7"
cd $YOLO_DIR

WEIGHTS_FILEPATH="/home/skibinmv/Desktop/cis/yolov7_helmet_detection/src/models/weights/yolov7_training.pt"

DATA_FILEPATH="/home/skibinmv/Desktop/cis/yolov7_helmet_detection/data/yolo_collected_datasets/22-11-08_16-21-19/yolo_data.yaml"

python3 train.py --workers 8 --device 0 --batch-size 2 --weights $WEIGHTS_FILEPATH --epochs 3 --data $DATA_FILEPATH

