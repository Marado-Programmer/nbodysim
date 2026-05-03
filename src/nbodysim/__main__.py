#!/usr/bin/env python3
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
import argparse
import time
from warnings import warn

import numpy as np
import matplotlib.pyplot as plt
from nbodysim.env import random_env
from nbodysim.loop import Loop, fixed_step, variable_step
from nbodysim.simulator import Simulator

from nbodysim.backend.cpu import CPUBackend


def make_backend(name: str):
    if name == "cpu":
        return CPUBackend()
    elif name == "gpu":
        try:
            from nbodysim.backend.gpu import GPUBackend

            return GPUBackend()
        except Exception as e:
            raise RuntimeError("GPU backend unavailable") from e
    else:
        raise ValueError(f"Unknown backend: {name}")


def make_loop(args):
    if args.mode == "fixed":
        return Loop(lambda: fixed_step(args.dt))
    elif args.mode == "variable":
        return Loop(lambda: variable_step(target_hz=args.hz))
    else:
        raise ValueError("Invalid mode")


def run_visual(sim: Simulator, interval: float = 0.01):
    plt.ion()
    fig, ax = plt.subplots()

    scatter = ax.scatter([], [])

    ax.set_title("n-body simulation")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    sim.start()

    try:
        while True:
            objs = sim.objects
            print([a for _, a in sim.env.objects])

            positions = np.array([o.position for o in objs])

            if len(positions) > 0:
                scatter.set_offsets(positions[:, :2])

                ax.set_xlim(positions[:, 0].min() - 1, positions[:, 0].max() + 1)
                ax.set_ylim(positions[:, 1].min() - 1, positions[:, 1].max() + 1)

            fig.canvas.draw()
            fig.canvas.flush_events()

            time.sleep(interval)

    except KeyboardInterrupt:
        pass
    finally:
        sim.stop()
        plt.ioff()
        plt.show()
        exit(0)


def parse_args():
    parser = argparse.ArgumentParser(description="N-body simulation")

    parser.add_argument("-n", "--num", type=int, default=100, help="number of bodies")
    parser.add_argument("--dim", type=int, default=2, help="dimensions")

    parser.add_argument(
        "--backend",
        choices=["cpu", "gpu"],
        default="cpu",
        help="backend to use",
    )

    parser.add_argument(
        "--mode",
        choices=["fixed", "variable"],
        default="fixed",
        help="loop mode",
    )

    parser.add_argument("--dt", type=float, default=0.01, help="fixed timestep")
    parser.add_argument("--hz", type=float, default=60.0, help="target frequency")

    parser.add_argument("--tolerance", type=float, default=1e-3)

    parser.add_argument("--seed", type=int, default=None)

    return parser.parse_args()


def main():
    args = parse_args()

    env = random_env(
        args.num,
        dim=args.dim,
        seed=args.seed,
    )

    backend = make_backend(args.backend)
    loop = make_loop(args)

    sim = Simulator(
        env,
        backend,
        loop,
        tolerance=args.tolerance,
    )
    signal.signal(signal.SIGINT, lambda sig, frame: sim.stop())

    run_visual(sim)


if __name__ == "__main__":
    import sys

    if not sys.warnoptions:
        import os, warnings

        warnings.simplefilter("default")  # Change the filter in this process
        os.environ["PYTHONWARNINGS"] = "default"  # Also affect subprocesses

    import signal
    import logging

    loglevel = "DEBUG"
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        warn(
            _("invalid log level: {loglevel}. using default level {default}").format(
                loglevel=loglevel, default="WARNING"
            ),
            UserWarning,
        )
        numeric_level = logging.WARNING
    logging.basicConfig(
        filename="simulation.log",
        encoding="utf-8",
        level=numeric_level,
        filemode="w",
        datefmt="%m-%d %H:%M",
        format="%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    main()
