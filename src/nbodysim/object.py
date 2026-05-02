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
"""The representation of a motionable object.

Notes
-----
This might just be a temporary representation, because I don't know how this
approach will affect performance later on.

Examples
--------
>>> dim = 2
>>> Object(position=np.empty(dim), mass=1, velocity=np.zeros(dim))  # doctest: +SKIP
Object(position=array([0., 0.]), mass=1, velocity=array([0., 0.]), acceleration=array([0., 0.]), radius=None)   # may vary
"""

from dataclasses import KW_ONLY, dataclass, field
from typing import Annotated, Sequence
import numpy as np
import numpy.typing as npt

type Positive[T: (int, float)] = Annotated[T, "positive"]
type Vec = npt.NDArray[np.float64]


@dataclass
class Object:
    """The representation of a motionable object.

    An object has an position and an acceleration. Its position and velocity
    will update depending on the current acceleration. Each object also has a
    mass. The number of dimmensions on which this object is represented is
    represented by the number of dimmensions that its position, velocity, and
    acceleration are represented in.

    Parameters
    ----------
    position : array_like
        The current position of the object (in meters). Has to have the same
        number of elements as `velocity`.
    mass : float, positive
        The current mass of the object (in kilograms).
    velocity : array_like
        The current velocity of the object (in meters per second). Has to have
        the same number of elements as `position`.
    radius : float, positive, optional
        Serves as a temporary way to represent the body perimeter/area/volume
        of the object in any number of dimmensions, to compute collisions.

    Attributes
    ----------
    position
    mass
    velocity
    acceleration : array_like
        The current acceleration of the object (in meters per second squared).
        Has the same number of elements as `position` and `velocity`.
    radius

    Raises
    ------
    ValueError
        If any of the parameters given are not compatible, representable, or
        physically possible.

    """

    _: KW_ONLY
    position: Vec
    mass: Positive[float]
    velocity: Vec
    acceleration: Vec = field(init=False)
    radius: Positive[float] | None = None

    def __post_init__(self, /):
        excs: Sequence[Exception] = []

        if not (len(self.position) == len(self.velocity)):
            excs.append(
                ExceptionGroup(
                    _(
                        "`position` and `velocity` do not represent the same amount of dimensions"
                    ),
                    [
                        ValueError(
                            _("`position` represents {dimensions} dimensions").format(
                                dimensions=len(self.position)
                            )
                            if len(self.position) != 1
                            else _("`position` represents 1 dimension")
                        ),
                        ValueError(
                            _("`velocity` represents {dimensions} dimensions").format(
                                dimensions=len(self.velocity)
                            )
                            if len(self.velocity) != 1
                            else _("`velocity` represents 1 dimension")
                        ),
                    ],
                )
            )

        self.dim = len(self.position)

        if self.dim < 1:
            excs.append(ValueError(_("number of dimmensions is not representable")))

        if self.mass <= 0:
            excs.append(ValueError(_("negative `mass` is not physically possible")))

        if self.radius is not None and self.radius < 0:
            excs.append(ValueError(_("`radius` has to be positive")))

        if excs:
            raise ExceptionGroup(_("tried to create a not representable object"), excs)

        self.acceleration = np.zeros(self.dim)

    def collides(self, pos: Vec) -> bool:
        if not self.valid_sequence(pos):
            raise ValueError(
                _("`pos` has to have {dimensions} dimensions").format(
                    dimensions=self.dim
                )
                if self.dim != 1
                else _("`pos` has to have 1 dimension")
            )

        if self.radius is None:
            return False

        acc = 0
        for i in range(self.dim):
            acc += (pos[i] - self.position[i]) ** 2

        return acc <= self.radius**2

    def valid_sequence(self, seq: Vec, /) -> bool:
        return self.dim == len(seq)
