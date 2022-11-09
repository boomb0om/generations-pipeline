# generations-pipeline

Утилиты для работы с text2image моделями:
- генерация изображений по списку запросов
- улучшение качества всех изображений в папке

## Установка
```bash
git clone https://github.com/boomb0om/generations-pipeline
cd generations-pipeline
pip install -r requirements.txt
```

## Использование
Ноутбук с примером: [example.ipynb](https://github.com/boomb0om/generations-pipeline/blob/main/example.ipynb)
В примере для генерации я использую модель [Малевич](https://github.com/ai-forever/ru-dalle). Но вы можете использовать любую другую text2image нейросеть.

**Генерация**
---
Для генерации используется функция `generate_queries(generate_func, queries: List[str], save_folder: str, grid_nrow: int = 4, image_format: str = '.jpg')`.
- `generate_func` - пользовательская функция, которая принимает текстовый запрос и возвращает список из `PIL.Image.Image`. В ней как раз реализуется логика генерации изображений.
```python
def generate_func(query: str) -> List[PIL.Image.Image]:
    ...
    return pil_images_list
```
- `queries` - список текстовых кэпшенов для генерации.
- `save_folder` - путь к папке, в которую будут сохранены результаты
- `grid_nrow` - сколько изображений поместить на одной строке в изображении-сетке (для каждого запроса сохраняется сетка со всеми генерациями).
- `image_format` - расширение, в котором сохранять изображения

Сгенерированные изображения сохраняются в такой структуре:
```bash
save_folder/
  query1/
    grid.jpg
    0.jpg
    1.jpg
    ...
  query2/
    grid.jpg
    0.jpg
    1.jpg
    ...
  ...
```

**Апскейл**
---
Для улучшения качества изображений используется функция `superres_folder(superres_func, folder_path: str, skip_grid: bool = True, filter_path = lambda x: True)`. Она рекурсиво проходится по папке и вызывает `superres_func` для каждого фото.
- `superres_func` - пользовательская функция, которая принимает изображение `PIL.Image.Image` и возвращает `PIL.Image.Image`. В ней вы должны реализовать логику работы с изображением.
```python
def superres_func(pil_image: PIL.Image.Image) -> PIL.Image.Image:
    ...
    return pil_image
```
- `folder_path` - путь к папке, в которой нужно улучшить изображения.
- `skip_grid` - если True, то не улучшает изображение с сеткой `grid.jpg`, которые получаются после генераций.
- `filter_path` - пользовательская функция, которая задает условия, изображения с какими путями нужно улучшать, а какие нет. Будут улучшены те изображения, для которых данная функция вернет True. По умолчанию улучшаются все изображения. Имеет такой вид:
```python
def filter_path(filepath: str) -> bool:
    return accept
```
