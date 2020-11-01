from PIL import Image
from PIL import ImageOps
import numpy as np


def image_func(ls: list) -> Image:
    total_image = np.full((1000, 1000, 3), 0, dtype=np.float64)
    voting_matrix = np.full((1000, 1000, 3), 0, dtype=np.float64)

    for i in range(len(ls)):
        png_image = Image.open(ls[i])
        width, height = png_image.size
        if not (width == 1000 and height == 1000):
            continue

        num_of_pixels = width*height
        image_raw_data = 255 - np.array(png_image)

        num_of_pixel_votes = np.count_nonzero(image_raw_data > 0)
        pixel_vote_power = num_of_pixels/num_of_pixel_votes

        voting_matrix[image_raw_data > 0] += pixel_vote_power

        total_image += image_raw_data * pixel_vote_power

    total_image = np.divide(total_image, voting_matrix, out=np.zeros_like(total_image), where=voting_matrix!=0)

    total_image = 255 - total_image
    print(total_image[total_image>=255])
    total_image = total_image.astype(np.uint8)
    im = Image.fromarray(total_image, 'RGB')
    return im


#image_ls = ['hello.png', 'jeff.png', 'me.png', 'troll.png', 'topright.png', 'lilpurple.png','englandtroll.png']
#img = image_func(image_ls)
#img.show()
