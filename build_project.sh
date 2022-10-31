# get yolo repository:
echo 'Downloading yolov7 repository and install requirements ...'
cd src/models
git clone https://github.com/WongKinYiu/yolov7.git && cd yolov7
pip install -r requirements.txt
