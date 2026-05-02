import numpy as np
from nbodysim import G
from . import Backend, Env


class CPUBackend(Backend):
    def step(self, dt: float, env: Env) -> Env:
        objs = [obj for obj, _ in env.objects]
        a = np.array([a for _, a in env.objects])

        r = np.stack([o.position for o in objs])
        v = np.stack([o.velocity for o in objs])
        m = np.array([o.mass for o in objs])

        r += v * dt + (1 / 2) * a * dt**2
        v += (1 / 2) * a * dt

        # N = len(objs)
        dim = objs[0].dim

        # [N, N, dim]
        diff = r[np.newaxis, :, :] - r[:, np.newaxis, :]

        # [1, N, 1] * [N, N, dim] = [N, N, dim] = Δr[N_i, N_j] * m[N_j]
        numerator = m[np.newaxis, :, np.newaxis] * diff
        # diagonal 0, so later the object itself doesn't give itself
        # acceleration: i != j
        for d in range(dim):
            np.fill_diagonal(numerator[:, :, d], 0)
        # [N, N]
        denominador = (np.linalg.norm(diff**2, axis=-1) + env.epsilon**2) ** (3 / 2)

        # [N, N, dim] / [N, N, 1] = [N, N, dim] = (Δr[N_i, N_j] * m[N_j]) /
        # denominador[N_i, N_j]
        #
        # sum accelerations from each other object
        #
        # [N, dim]
        a = G * np.sum(numerator / denominador[:, :, np.newaxis], axis=1)

        v += (1 / 2) * a * dt

        for i, o in enumerate(objs):
            o.position = r[i]
            o.velocity = v[i]

        env.objects = list(zip(objs, a))
        return env
