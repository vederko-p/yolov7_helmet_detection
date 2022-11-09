# Модуль для подготовки данных к обуению детектора

# Инструкция к настройке проекта

Клонировать репозиторий:

```
git clone https://github.com/vederko-p/yolov7_helmet_detection.git
```

Перейти в директорию `scripts` и выполнить скрипт конфигурации проекта:

```
bash build_project.sh`
```

Данный скрипт автоматически установит зависимости проекта, а также модель yolov7 и ее зависимости.

# Инструкция по подготовке датасета к обучению

**1. Скачивание и подготовка отдельных датасетов**

Необходимо скачать нужные датасеты и указать их параметры в YAML файле метаданных, который необходимо разместить в той же директории.

При желании можно скачать заранее подготовленный набор данных, перейда в папку `scripts` и выполнив команду:

```
  bash download_data.sh
```

Структура файла метаданных:

```YAML
dataset_1_key:  # Must be equal to dataset folder name
  name: Dataset name  # (Optional)
  source_link: Dataset source link  # (Optional)
  download_link: Dataset download link  # (Optional)
  folder_name: Dataset folder name
  images_directory: Dataset images folder
  labels_directory: Dataset labels folder. Must differ from "labels"
  labels_format: Labels format  # (Optional)
  channels: Channels order  # (Optional)
  classes:
    0: Class 1 name
    1: Class 2 name
    ...
  classes_ratio:  # (Optional)
    0: Amount of class 1 labels
    1: Amount of class 2 labels
    ...

dataset_2_key:
  ...
```

**2. Индексация датасета**

Для актуализации собранного датасета в проекте, датасет необходимо проиндексировать. Для этого необходимо перейти в директорию `src/dataset` и выполнить скрипт `python3 indexing.py`. В той же директории появится новая папка вместе со сформированным индексом.

**3. Сборка выборки**

Для сборки всех данных в одну выборку и разбиения ее на части необходимо подготовить конфиг разбиения следующей структуры:

```YAML
datasets:
  ds_1:
    classes:  # Mappings for classes union
      union_ds_id: [ds1_class_id, ...]
      ...
  ds_2:
    classes:
      union_ds_id: [ds1_class_id, ...]
      ...
  
split:
  indexing_path: <path to index file>
  parts:
    part: float_value_from_01      # part values: [
  random_state: int_value_or_None  #  train
                                   #  val  --Optional
                                   #  test  --Optional
class_mapping:
  union_class_id: name
  ...
```

В поле `datasets` перечисляются наименования папок тех датасетов, которые будут включены в новый объединенный датасет. Для каждого класса указывается маппинг классов, где ключ - id класса в новом датасете, а значение - список классов в выбранном датасете. Например, маппинг классов вида

```YAML
ds_1:
  classes:
    0: [1]
    1: [3, 4]
```

будет означать, что из датасета `ds_1` будут выбранны изображения и разметка для классов 1, 3, 4, при этом в новом датасете id классов будут изменены и иметь значения
* 0 для класса 1
* 1 для классов 3 и 4

В поле `split : indexing_path` указывается абсолютный путь до актуального файла с индексацией датасета.

В поле `split : parts` указываются наименования разбиений и их объемы в коэффициентах. При разбиении данных, количество экземпляров в каждом разбиении определяется для каждого датасета индивидуально.

В поле `split : random_state` при необходимости фиксируется случайность разбиения данных.

В поле `class_mapping` указываются маппинги классов объединеного датасета.

Для запуска разбиения необходимо перейти в `src/dataset` и выполнить `python3 split_and_collect_ds.py` предварительно указав внутри этого файла путь до конфига разбиения:

```Python
...

def main():
    split_config_filepath = '../common/split_dataset_configs/split_dataset_config_test.yaml'
    
...
```

(Это сделано так пока что с тем, чтобы не прокидовать каждый раз путь руками. Альтернатива: bash скрипт с прокидыванием пути.)