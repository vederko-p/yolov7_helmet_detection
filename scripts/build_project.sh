# Install project requirements
echo Install project requirements...
pip -r requirements.txt

# Get yolo repository
echo 'Download yolov7 repository...'

MODELS_DIR="../src/models"
if [[ ! -d $MODELS_DIR ]]
then
  mkdir $MODELS_DIR
fi

cd $MODELS_DIR
git clone https://github.com/WongKinYiu/yolov7.git && cd yolov7

echo Install yolov7 requirements...
pip install -r requirements.txt
