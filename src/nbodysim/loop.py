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
"""The simulation loop that generates differences of time for consumption.

The way the differences of time are calculated is by using the strategy desing
pattern for a generator. This differences of time are stored on a queue for
further consumption.

Default generator strategies are also available in the module

The `Loop` works with a thread, allowing parallelism.

See Also
--------
nbodysim.simulator.Simulator :
    Uses a loop to simulate.

Examples
--------
>>> with Loop(lambda: fixed_step(1/24)) as loop:
...     loop.skip_forward(3)
...     for dt in loop:
...         print(dt)
...
0.041666666666666664
0.041666666666666664
0.041666666666666664
"""

import threading
import queue
import time
from typing import Annotated, Callable, Generator, Iterator


class Loop(Iterator):
    """The loop (thread) that generates differences of time.

    It uses Python's `threading` module to allow parallelism. Its istances
    allow to use context with the `with` keyword and are also iterators. Has an
    API that tries to mimic a simple media player.

    Parameters
    ----------
    strategy
        The generator of the differences of time.
    queue_block : bool, default True
        Whether or not to wait for the generator to give a difference of time.
    queue_timeout : float, optional
        If `queue_block`, how much seconds to wait.
    queue_maxsize : int, default 0
        How much differences of time is the queue able to hold.
    drop : bool, default False
        Instead of waiting if `queue_block` and the queue is full, drop the
        oldest difference of time.

    Attributes
    ----------
    strategy
    queue_block
    queue_timeout

    See Also
    --------
    variable_step :
        Strategy that generates steps depending on how much time has passed
        exactly.
    fixed_step :
        Strategy that generates always the same time differences.
    """

    __strategy: Generator[float]

    def __init__(
        self,
        strategy: Callable[[], Generator[float]],
        *,
        queue_block: bool = True,
        queue_timeout: float | None = None,
        queue_maxsize: int = 0,
        drop: bool = False,
    ) -> None:
        self.queue_block = queue_block
        self.queue_timeout = queue_timeout
        self.drop = drop
        self.__remaining: int | None = None
        self.__play_state = threading.Event()
        self.__stop_state = threading.Event()
        self.__thread = threading.Thread(target=self.run, daemon=True)
        self.__queue: queue.Queue[float] = queue.Queue(queue_maxsize)
        self.strategy = strategy

    @property
    def looping(self) -> bool:
        return not self.__stop_state.is_set()

    def start(self) -> None:
        """Makes the `Loop` generate differences of time until it `pause`s or
        `stop`s.

        See Also
        --------
        pause :
            Pauses the `Loop`.
        stop :
            Stops the `Loop` and ends the thread.
        """
        self.__play_state.set()
        if not self.__thread.is_alive():
            self.__thread.start()

    def pause(self) -> None:
        """Pauses the `Loop`.

        See Also
        --------
        start :
            Use `start` (resume) to make the `Loop` generate more differences
            of time.
        """
        self.__play_state.clear()

    def stop(self) -> None:
        """Stops the `Loop` and consequently ends the thread."""
        self.__stop_state.set()
        self.__play_state.set()

    def skip_forward(self, n: Annotated[int, "normal"]) -> None:
        """Use to generate exactly more `n` differences of time.

        Parameters
        ----------
        n : int, positive
            How many differences of time to generate.

        See Also
        --------
        start :
            After creating them, the `Loop` `pause`s. You might want to `start`
            (resume) it after, or just `skip_forward` again.
        """
        if n <= 0:
            raise ValueError()

        self.__remaining = n
        self.start()

    def run(self):
        while self.looping:
            self.__play_state.wait()
            dt = next(self.__strategy)
            try:
                self.__queue.put(dt, self.queue_block, self.queue_timeout)
            except queue.Full:
                if self.drop:
                    self.__queue.get_nowait()
                    self.__queue.put_nowait(dt)

            if self.__remaining is not None:
                self.__remaining -= 1
                if self.__remaining <= 0:
                    self.__remaining = None
                    self.pause()

        self.__queue.shutdown()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        if self.__thread.is_alive():
            self.__thread.join()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            dt = self.__queue.get(self.queue_block)
            self.__queue.task_done()
            return dt
        except (queue.Empty, queue.ShutDown) as e:
            raise StopIteration from e

    def refresh(self) -> None:
        """Empties the differences of time's queue."""
        while True:
            try:
                self.__queue.get_nowait()
                self.__queue.task_done()
            except queue.Empty:
                return

    @property
    def strategy(self) -> Generator[float]:
        return self.__strategy

    @strategy.setter
    def strategy(self, factory: Callable[[], Generator[float]]) -> None:
        self.pause()
        self.refresh()
        self.__strategy = factory()


def variable_step(
    *, max_delta: float | None = None, target_hz: float | None = None
) -> Generator[float]:
    """Generates differences of time based on how much time has passed.

    Parameters
    ----------
    max_delta : float, optional
        Doesn't allow differences of time bigger that the `max_delta`.
    target_hz : float, optional
        Whether you want to "throtte" the generation of differences of time,
        but still generating the actual time that has passed.

    Returns
    -------
    iterable object
        The generator.

    Yields
    ------
    float
        How much time has passed.
    """
    target_interval = (1 / target_hz) if target_hz else None

    t0 = time.monotonic()

    while True:
        t = time.monotonic()
        dt = t - t0
        t0 = t

        if max_delta is not None:
            dt = min(dt, max_delta)

        yield dt

        if target_interval is not None:
            elapsed = time.monotonic() - t
            sleep_time = target_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)


def fixed_step(dt: float) -> Generator[float]:
    """Generates differences of time after `dt` time has passed.

    Parameters
    ----------
    max_delta : float
        How much time it needs to pass to generate a difference of time.

    Returns
    -------
    iterable object
        The generator.

    Yields
    ------
    float
        How much time has passed.
    """
    t0 = time.monotonic()
    acc = 0

    while True:
        t = time.monotonic()
        acc += t - t0
        t0 = t

        while acc >= dt:
            yield dt
            acc -= dt
