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
import threading

from nbodysim.backend import Backend
from nbodysim.env import Env
from nbodysim.loop import Loop


class Simulator:
    def __init__(
        self,
        env: Env,
        /,
        backend: Backend,
        loop: Loop,
        *,
        tolerance: float = 1e-3,
    ) -> None:
        self.env = env
        self.backend = backend
        self._loop = loop
        self.epsilon = tolerance
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._running = threading.Event()
        self._stop = threading.Event()
        self._lock = threading.Lock()

    @property
    def loop(self) -> Loop:
        return self._loop

    @loop.setter
    def loop(self, loop: Loop) -> None:
        looping = self._loop.looping
        self._loop.stop()
        self._loop = loop
        if looping:
            self._loop.start()

    @property
    def epsilon(self) -> float:
        return self.env.epsilon

    @epsilon.setter
    def epsilon(self, tolerance: float) -> None:
        import numpy as np

        positions = [o.position for o, _ in self.env.objects]
        if not positions:
            self.env.epsilon = tolerance
            return

        scale = np.mean([np.linalg.norm(p) for p in positions])
        self.env.epsilon = max(tolerance, tolerance * scale)

    @property
    def objects(self):
        return [o for o, _ in self.env.objects]

    def _run(self):
        with self.loop:
            for dt in self.loop:
                if self._stop.is_set():
                    break

                if not self._running.is_set():
                    continue

                with self._lock:
                    self.env = self.backend.step(dt, self.env)

    def start(self):
        """Start or resume simulation."""
        self._running.set()
        self.loop.start()

        if not self._thread.is_alive():
            self._thread.start()

    def pause(self):
        """Pause simulation."""
        self._running.clear()
        self.loop.pause()

    def stop(self):
        """Stop simulation completely."""
        self._stop.set()
        self._running.set()
        self.loop.stop()

        if self._thread.is_alive():
            self._thread.join()

    def step_n(self, n: int):
        """Run exactly n timesteps."""
        self.loop.skip_forward(n)
        self.start()

    @property
    def running(self) -> bool:
        return self._running.is_set()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.stop()
