from collections import defaultdict
from logging import info

from SSIM_PIL import compare_ssim
from PIL import Image
from utility.logger import Logger
from os import walk

from utility.os_interface import delete_file, get_file_size
from utility.path_str import get_full_path
from utility.utilities import format_byte


def compare_images(sorted_images, current_image):
    """

    :param sorted_images:
    :param current_image:
    :return: Size of deleted image or zero
    """
    size = 0.0
    # Iterate over images with same size
    for i, file in enumerate(sorted_images[current_image.size]):
        with Image.open(file) as image:

            # If image with same content exists
            if compare_ssim(current_image, image) >= 0.999:
                # Delete current file
                print(current_image.filename, image.filename)
                current_image.show()
                image.show()
                select = 1# input('DELETE: 1 or 2')

                if select == 2:
                    size = get_file_size(image.filename)
                    delete_file(image.filename)
                    print(sorted_images[current_image.size])
                    sorted_images[current_image.size].pop(i)
                    print(sorted_images[current_image.size])
                    break
                else:
                    size = get_file_size(current_image.filename)
                    delete_file(current_image.filename)
                    return size

    # Save current image for later comparison
    sorted_images[current_image.size] += [current_image.filename]
    return size


def delete_images(path):
    total_size = 0.0
    sorted_images = defaultdict(list)

    for root, directories, files in walk(path):
        for file in files:
            try:
                # Open current image
                with Image.open(get_full_path(root, file)) as current_image:
                    total_size += compare_images(sorted_images, current_image)


            except Exception as e:
                pass

    info("SAVED: " + format_byte(total_size))


if __name__ == "__main__":
    with Logger():
        s_input = True
        while s_input:
            s_input = input('PATH: ').strip('"')
            delete_images(s_input)
