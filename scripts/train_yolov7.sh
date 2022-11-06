# start yolo training
cd src/models/yolov7

WEIGHTS_FILEPATH="/home/maksim/Desktop/Projects/neft_project/yolov7_helmet_detection/src/models/weights/yolov7/yolov7_training.pt"

DATA_FILEPATH="/home/maksim/Desktop/Projects/neft_project/yolov7_helmet_detection/data/yolo_collected_datasets/22-11-07_00-26-00/yolo_data.yaml"

python3 train.py --batch-size 4 --weights $WEIGHTS_FILEPATH --epochs 3 --data $DATA_FILEPATH

