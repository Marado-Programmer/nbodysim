import unittest
import numpy as np

from nbodysim.backend.cpu import CPUBackend
from nbodysim.backend import Env
from nbodysim.object import Object


class TestCPUBackend(unittest.TestCase):
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

    def test_step_runs(self):
        env = self.make_env()
        backend = CPUBackend()

        env2 = backend.step(0.01, env)

        self.assertEqual(len(env2.objects), 2)

    def test_positions_change(self):
        env = self.make_env()
        backend = CPUBackend()

        r0 = [o.position.copy() for o, _ in env.objects]

        env = backend.step(60, env)

        r = [o.position for o, _ in env.objects]

        moved = any(not np.allclose(p0, p) for p0, p in zip(r0, r))

        self.assertTrue(moved)

        env = backend.step(60, env)

        r = [o.position for o, _ in env.objects]

        for p0, p in zip(r0, r):
            displacement = np.linalg.norm(p - p0)
            self.assertGreater(displacement, 0)

    def test_acceleration_nonzero(self):
        env = self.make_env()
        backend = CPUBackend()

        backend.step(0.01, env)

        for _, a in env.objects:
            self.assertTrue(np.any(np.abs(a) > 0))

    def test_no_self_interaction(self):
        # single particle should have zero acceleration
        o = Object(
            position=np.array([0.0, 0.0]),
            velocity=np.array([1.0, 0.0]),
            mass=1.0,
        )

        env = Env(objects=[(o, np.zeros(2))], epsilon=1e-3)
        backend = CPUBackend()

        backend.step(0.01, env)

        _, a = env.objects[0]
        self.assertTrue(np.allclose(a, 0))

    def test_energy_not_exploding(self):
        # crude sanity: system shouldn't blow up immediately
        env = self.make_env()
        backend = CPUBackend()

        for _ in range(50):
            backend.step(0.01, env)

        for o, _ in env.objects:
            self.assertTrue(np.all(np.isfinite(o.position)))
            self.assertTrue(np.all(np.isfinite(o.velocity)))
