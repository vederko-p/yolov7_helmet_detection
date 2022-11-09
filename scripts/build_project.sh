# get yolo repository:
echo 'Downloading yolov7 repository and install requirements ...'

MODELS_DIR="../src/models"
if [[ ! -d $MODELS_DIR ]]
then
	mkdir $MODELS_DIR
fi

cd $MODELS_DIR
git clone https://github.com/WongKinYiu/yolov7.git && cd yolov7
pip install -r requirements.txt
