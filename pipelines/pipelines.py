import os
import re
from tqdm import tqdm
from PIL import Image
from typing import List

from .utils import merge_pil_images


IMAGE_EXTINSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG')


def generate_queries(generate_func, queries: List[str], save_folder: str, 
                     grid_nrow: int = 4, image_format: str = '.jpg'):
    image_format = image_format.lstrip('.')
    assert '.'+image_format in IMAGE_EXTINSIONS
    
    valid_filenames_regex = re.compile("[^\w0-9\ \-\_]+")
    os.makedirs(save_folder, exist_ok=True)
    
    for query in tqdm(queries):
        pil_images = generate_func(query)
        grid_image = merge_pil_images(pil_images, nrow=grid_nrow)
        
        query_filtered = valid_filenames_regex.sub('', query)
        query_save_path = os.path.join(save_folder, query_filtered)
        os.makedirs(query_save_path, exist_ok=True)
        
        grid_image.save(os.path.join(query_save_path, 'grid.jpg'))
        for c, pil_img in enumerate(pil_images):
            pil_img.save(os.path.join(query_save_path, f'{c}.{image_format}'))
            

def superres_folder(superres_func, folder_path: str, skip_grid: bool = True, 
                    filter_path = lambda x: True):
    pbar = tqdm()
    for path, dirs, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(path, filename)
            if skip_grid and filename == 'grid.jpg':
                continue
            if filter_path(filepath):
                img = Image.open(filepath)
                superres_img = superres_func(img)
                superres_img.save(filepath)
                pbar.update(1)
    pbar.close()