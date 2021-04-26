from numba import cuda
from PIL import Image
import numpy as np
import math


@cuda.jit
def sumImages(im1, im2, out):
    x, y, z = cuda.grid(3)

    if x < im1.shape[0] and y < im1.shape[1] and z < im1.shape[2]:
        out[x][y][z] += (im2[x][y][z] + im1[x][y][z]) % 256


def main(image1, image2):
    data_image1 = np.array(image1)
    data_image2 = np.array(image2)
    print(data_image1.shape, data_image2.shape)

    threadsperblock = (16, 16, 4)
    blocksper_x = int(math.ceil(data_image1.shape[0] // threadsperblock[0]))
    blocksper_y = int(math.ceil(data_image1.shape[1] // threadsperblock[1]))
    blocksper_z = int(math.ceil(data_image1.shape[2] // threadsperblock[2]))
    blockspergrid = (blocksper_x, blocksper_y, blocksper_z)

    input1 = cuda.to_device(data_image1)
    input2 = cuda.to_device(data_image2)
    output = cuda.device_array(data_image1.shape)

    sumImages[blockspergrid, threadsperblock](input1, input2, output)

    out = output.copy_to_host()
    out = out.astype('uint8')
    out = Image.fromarray(out)
    out.save("out.png")


if __name__ == "__main__":
    image1 = Image.open('chronometer.png')
    image2 = Image.open('calendar.png')
    main(image1, image2)
