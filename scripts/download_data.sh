# Download standard dataset

OUTPUT_DIR="../data"

default_data_files_ids=(
  10rCVev-RhAQKhSDN_OORvzzZM_LMNORl
  15TMLBuTLwduQOm069LiZU94l8Lod_Xob
)

default_data_names=(
  chv
  safety_vest
)

cd $OUTPUT_DIR

for i in ${!default_data_files_ids[*]}
do
  file_id=${default_data_files_ids[i]}
  file_name=${default_data_names[i]}
  echo Download $file_name dataset...
  gdown $file_id
  unzip "$file_name.zip" -d $file_name
  rm "$file_name.zip"
done
