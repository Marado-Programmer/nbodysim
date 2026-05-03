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
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

from nbodysim.object import Object, Vec


@dataclass
class Env:
    objects: Sequence[tuple[Object, Vec]]
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


class Backend(ABC):
    @abstractmethod
    def step(self, dt: float, env: Env) -> Env: ...
