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
from dataclasses import dataclass
from typing import MutableSequence
import numpy as np

from nbodysim.object import Object, Vec
from nbodysim import G


@dataclass
class Env:
    objects: MutableSequence[tuple[Object, Vec]]
    epsilon: float

    def __post_init__(self, /):
        if len(self.objects) == 0:
            return

        self.dim = self.objects[0][0].dim

        for o, a in self.objects:
            if o.dim != self.dim:
                raise ValueError(
                    _(
                        "`Object`s in the `objects` `Sequence` aren't all of the same dimension"
                    )
                )

            if not o.valid_sequence(a):
                raise ValueError(
                    _(
                        "At least one of the accelarations given to an object is incompatible with the objects dimensions"
                    )
                )


def random_env(
    n: int,
    dim: int = 2,
    *,
    space_scale: float = 10.0,
    mass_scale: float = 10.0,
    seed: int | None = None,
) -> Env:
    rng = np.random.default_rng(seed)

    objects = []

    for _ in range(n):
        position = rng.uniform(-space_scale, space_scale, size=dim)
        # velocity = rng.uniform(-velocity_scale, velocity_scale, size=dim)
        # v_scale = np.sqrt(G * mass_scale / space_scale)
        # velocity = rng.normal(0, v_scale, size=dim)
        velocity = np.zeros(dim)
        mass = rng.uniform(0.1, mass_scale)

        obj = Object(
            position=position.astype(np.float64),
            velocity=velocity.astype(np.float64),
            mass=float(mass),
        )

        objects.append((obj, np.zeros(dim)))

    return Env(objects=objects, epsilon=1e-3)
