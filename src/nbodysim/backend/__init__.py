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
