from numba import cuda
from time import perf_counter
from PIL import Image
import numpy as np


# pocet poli, na ktoré sa rozdelí hlavné pole
X = 8192


@cuda.jit
def sumImages(im1, im2):
    x = cuda.grid(1)
    num_iters = im1.size / cuda.blockDim.x
    for j in range(num_iters):
        i = j * cuda.blockDim.x + x
        im2[i] = (im1[i] + im2[i]) % 256


def main(image1, image2):
    streams = []
    start_events = []
    end_events = []
    data1_gpu = []
    data2_gpu = []
    gpu_out = []
    out = []

    data_image1 = np.array(image1)
    data_image2 = np.array(image2)
    print(data_image1.shape, data_image2.shape)

    shpape_A = data_image1.shape
    # prevaod na 1 rozmerne pole
    data_image1 = data_image1.ravel()
    data_image2 = data_image2.ravel()

    input1 = np.split(data_image1, X)
    input2 = np.split(data_image1, X)

    for _ in range(len(input1)):
        streams.append(cuda.stream())
        start_events.append(cuda.event())
        end_events.append(cuda.event())

    for i in range(len(input1)):
        data1_gpu.append(cuda.to_device(input1[i], stream=streams[i]))
        data2_gpu.append(cuda.to_device(input2[i], stream=streams[i]))

    t_start = perf_counter()
    for i in range(len(input1)):
        start_events[i].record(streams[i])
        sumImages[1, 32, streams[i]](data1_gpu[i], data2_gpu[i])
    t_end = perf_counter()

    for i in range(len(input1)):
        end_events[i].record(streams[i])
        gpu_out.append(data2_gpu[i].copy_to_host(stream=streams[i]))

    for i in range(len(gpu_out)):
        out = np.concatenate((out, gpu_out[i]))

    kernel_times = []

    for k in range(len(input1)):
        kernel_times.append(
            cuda.event_elapsed_time(start_events[k], end_events[k]))

    out = out.reshape(shpape_A)
    out = out.astype('uint8')
    out = Image.fromarray(out)
    out.save("out_stream.png")
    print(f'Total time: {t_end - t_start}')
    print(f'Mean kernel duration (milliseconds): {np.mean(kernel_times)}')
    print(f'Mean kernel standard deviation \
          (milliseconds): {np.std(kernel_times)}')


if __name__ == "__main__":
    image1 = Image.open('chronometer.png')
    image2 = Image.open('calendar.png')
    main(image1, image2)
    exit(0)
