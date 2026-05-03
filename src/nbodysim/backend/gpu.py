#        nbodysim — n-body problem simulation with HPC
#        Copyright (C) 2026  João Augusto Costa Branco Marado Torres
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        (at your option) any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <https://www.gnu.org/licenses/>.
from nbodysim.env import Env
import numpy as np
from . import Backend
from nbodysim import G


class GPUBackend(Backend):
    def __init__(self):
        from pycuda.compiler import SourceModule

        with open("../kernels/kernel.cu") as f:
            self.mod = SourceModule(f.read())

        self.pre = self.mod.get_function("pre_update")
        self.acc = self.mod.get_function("compute_acc")
        self.post = self.mod.get_function("post_update")

    def step(self, dt: float, env: Env) -> Env:
        import pycuda.driver as cuda

        threads = 1 << 8

        objs = [obj for obj, _ in env.objects]
        a = np.array([a for _, a in env.objects], dtype=np.float32)

        N = len(objs)
        dim = objs[0].dim
        blocks = (N + threads - 1) // threads

        r = np.stack([o.position for o in objs], dtype=np.float32)
        v = np.stack([o.velocity for o in objs], dtype=np.float32)
        m = np.array([o.mass for o in objs], dtype=np.float32)

        r_flat = r.ravel()
        v_flat = v.ravel()
        a_flat = a.ravel()

        r_gpu = cuda.mem_alloc(r_flat.nbytes)
        v_gpu = cuda.mem_alloc(v_flat.nbytes)
        a_gpu = cuda.mem_alloc(a_flat.nbytes)
        m_gpu = cuda.mem_alloc(m.nbytes)

        cuda.memcpy_htod(r_gpu, r_flat)
        cuda.memcpy_htod(v_gpu, v_flat)
        cuda.memcpy_htod(a_gpu, a_flat)
        cuda.memcpy_htod(m_gpu, m)

        dt32 = np.float32(dt)
        G32 = np.float32(G)
        eps2 = np.float32(env.epsilon**2)
        dim32 = np.int32(dim)
        N32 = np.int32(N)

        self.pre(
            r_gpu,
            v_gpu,
            a_gpu,
            dt32,
            dim32,
            N32,
            block=(threads, 1, 1),
            grid=(blocks, 1),
        )

        self.acc(
            r_gpu,
            m_gpu,
            a_gpu,
            G32,
            eps2,
            dim32,
            N32,
            block=(threads, 1, 1),
            grid=(blocks, 1),
        )

        self.post(
            v_gpu, a_gpu, dt32, dim32, N32, block=(threads, 1, 1), grid=(blocks, 1)
        )

        cuda.memcpy_dtoh(r_flat, r_gpu)
        cuda.memcpy_dtoh(v_flat, v_gpu)
        cuda.memcpy_dtoh(a_flat, a_gpu)

        r = r_flat.reshape(N, dim)
        v = v_flat.reshape(N, dim)
        a = a_flat.reshape(N, dim)

        for i, o in enumerate(objs):
            o.position = r[i]
            o.velocity = v[i]

        env.objects = list(zip(objs, a))
        return env


def cuda_available():
    try:
        import pycuda.autoinit
        import pycuda.driver as cuda

        cuda.init()
        return cuda.Device.count() > 0
    except Exception:
        return False
