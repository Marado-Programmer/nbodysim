__global__ void multiplicar_por_dois(float *dest) {
  int idx = threadIdx.x + blockIdx.x * blockDim.x;
  dest[idx] *= 2;
}
