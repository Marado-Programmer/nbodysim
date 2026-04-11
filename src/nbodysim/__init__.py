import pycuda.autoinit
import pycuda.driver as cuda
import numpy as np
from pycuda.compiler import SourceModule

def result():
    data = np.random.randn(400).astype(np.float32)

    gpu_data = cuda.mem_alloc(data.nbytes)
    cuda.memcpy_htod(gpu_data, data)

    with open("kernel.cu", "r") as f:
        cuda_source = f.read()
    mod = SourceModule(cuda_source)

    func = mod.get_function("double")
    func(gpu_data, block=(400, 1, 1), grid=(1, 1))

    res = np.empty_like(data)
    cuda.memcpy_dtoh(res, gpu_data)

    return res

def say_result():
    print(*result())
