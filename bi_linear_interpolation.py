import cv2
import numpy as np
from os import getcwd


def get_blank_image(image, chunk_size):
    height = (image.shape[0]-1) * (chunk_size-1) + 1
    width = (image.shape[1]-1) * (chunk_size-1) + 1
    new_image = np.zeros((height, width, 3), np.uint8)
    return new_image


def interpolate_pixel(corners, pI, pJ):
    return (
        corners[0][0] *     pI*pJ     +
        corners[0][1] *     pI*(1-pJ) +
        corners[1][0] * (1-pI)*pJ     +
        corners[1][1] * (1-pI)*(1-pJ)
    )


def get_chunk(corners, chunk_size):
    chunk = np.zeros((chunk_size, chunk_size, 3), np.uint8)

    for i in range(chunk_size):
        for j in range(chunk_size):
            pI = i/(chunk_size-1)
            pJ = j/(chunk_size-1)
            chunk[i, j] = interpolate_pixel(corners, pI, pJ)

    return chunk


def set_chunks(image, new_image, chunk_size):
    for i in range(len(image)-1):
        for j in range(len(image[0])-1):
            corners = image[i:i+2, j:j+2]
            x_range = slice(i*(chunk_size-1), (i+1)*(chunk_size-1)+1)
            y_range = slice(j*(chunk_size-1), (j+1)*(chunk_size-1)+1)

            new_image[x_range, y_range] = get_chunk(corners, chunk_size)

    return new_image


def bi_interpolation(path, chunk_size):
    image = cv2.imread(path)
    blank_image = get_blank_image(image, chunk_size)
    new_image = set_chunks(image, blank_image, chunk_size)

    cv2.imwrite(rf'{getcwd()}\bi_interpolated_image.jpeg', new_image)
    #cv2.imshow('image', new_image)
    #cv2.waitKey()


def main():
    path = rf'{getcwd()}\image.jpeg'
    bi_interpolation(path, 4)


main()
