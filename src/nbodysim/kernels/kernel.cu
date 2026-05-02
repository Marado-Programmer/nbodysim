__global__ void pre_update(float *r, float *v, float *a, float dt, int dim,
                           int N) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i >= N)
    return;

  for (int d = 0; d < dim; d++) {
    int idx = i * dim + d;

    r[idx] += v[idx] * dt + 0.5f * a[idx] * dt * dt;
    v[idx] += 0.5f * a[idx] * dt;
  }
}

__global__ void compute_acc(float *r, float *m, float *a, float G, float eps2,
                            int dim, int N) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i >= N)
    return;

  for (int d = 0; d < dim; d++)
    a[i * dim + d] = 0.0f;

  for (int j = 0; j < N; j++) {
    if (i == j)
      continue;

    float dist2 = eps2;

    float diff[3]; // assuming dim ≤ 3

    for (int d = 0; d < dim; d++) {
      diff[d] = r[j * dim + d] - r[i * dim + d];
      dist2 += diff[d] * diff[d];
    }

    float inv_r3 = rsqrtf(dist2 * dist2 * dist2);

    for (int d = 0; d < dim; d++) {
      a[i * dim + d] += G * m[j] * diff[d] * inv_r3;
    }
  }
}

__global__ void post_update(float *v, float *a, float dt, int dim, int N) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i >= N)
    return;

  for (int d = 0; d < dim; d++) {
    int idx = i * dim + d;
    v[idx] += 0.5f * a[idx] * dt;
  }
}
