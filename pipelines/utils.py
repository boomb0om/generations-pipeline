from PIL import Image
import torch
import torchvision
import numpy as np

def pil_list_to_torch_tensors(pil_images):
    result = []
    for pil_image in pil_images:
        image = np.array(pil_image, dtype=np.uint8)
        image = torch.from_numpy(image)
        image = image.permute(2, 0, 1).unsqueeze(0)
        result.append(image)
    return torch.cat(result, dim=0)

def merge_pil_images(pil_images, nrow=16, imgsize=192):
    ratio = pil_images[0].size[0]/pil_images[0].size[1]
    if ratio >= 1:
        resize_shape = (int(imgsize*ratio), imgsize)
    else:
        ratio = 1/ratio
        resize_shape = (imgsize, int(imgsize*ratio))
    merged_images = [pil_image.resize(resize_shape) for pil_image in pil_images]
    merged_images = pil_list_to_torch_tensors(merged_images)
    merged_images = torchvision.utils.make_grid(merged_images, nrow=nrow)
    merged_images = torchvision.transforms.functional.to_pil_image(merged_images.detach())
    return merged_images