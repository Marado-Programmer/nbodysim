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
import unittest
import numpy as np

from nbodysim.backend.cpu import CPUBackend
from nbodysim.backend import Env
from nbodysim.object import Object


def cuda_available():
    try:
        import pycuda.driver as cuda

        cuda.init()
        return cuda.Device.count() > 0
    except Exception:
        return False


@unittest.skipUnless(cuda_available(), "CUDA not available")
class TestGPUBackend(unittest.TestCase):
    def make_env(self):
        o1 = Object(
            position=np.array([0.0, 0.0]),
            velocity=np.array([0.0, 0.0]),
            mass=1.0,
        )
        o2 = Object(
            position=np.array([1.0, 0.0]),
            velocity=np.array([0.0, 1.0]),
            mass=1.0,
        )

        zero_acc = np.zeros(2)
        return Env(objects=[(o1, zero_acc.copy()), (o2, zero_acc.copy())], epsilon=1e-3)

    def test_gpu_matches_cpu(self):
        from nbodysim.backend.gpu import GPUBackend
        env_cpu = self.make_env()
        env_gpu = self.make_env()

        cpu = CPUBackend()
        gpu = GPUBackend()

        dt = 0.01

        cpu.step(dt, env_cpu)
        gpu.step(dt, env_gpu)

        for (o_cpu, a_cpu), (o_gpu, a_gpu) in zip(env_cpu.objects, env_gpu.objects):
            np.testing.assert_allclose(
                o_cpu.position, o_gpu.position, rtol=1e-4, atol=1e-6
            )
            np.testing.assert_allclose(
                o_cpu.velocity, o_gpu.velocity, rtol=1e-4, atol=1e-6
            )
            np.testing.assert_allclose(a_cpu, a_gpu, rtol=1e-4, atol=1e-6)

    def test_multiple_steps_consistency(self):
        from nbodysim.backend.gpu import GPUBackend
        env_cpu = self.make_env()
        env_gpu = self.make_env()

        cpu = CPUBackend()
        gpu = GPUBackend()

        dt = 0.01

        for _ in range(10):
            cpu.step(dt, env_cpu)
            gpu.step(dt, env_gpu)

        for (o_cpu, a_cpu), (o_gpu, a_gpu) in zip(env_cpu.objects, env_gpu.objects):
            np.testing.assert_allclose(
                o_cpu.position, o_gpu.position, rtol=1e-3, atol=1e-5
            )
            np.testing.assert_allclose(
                o_cpu.velocity, o_gpu.velocity, rtol=1e-3, atol=1e-5
            )
            np.testing.assert_allclose(a_cpu, a_gpu, rtol=1e-3, atol=1e-5)
