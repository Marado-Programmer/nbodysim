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
from nbodysim.object import Object


class TestObject(unittest.TestCase):
    def setUp(self) -> None:
        self.dim = 3
        self.position = np.zeros(self.dim)
        self.velocity = np.ones(self.dim)
        self.mass = 1.0
        self.obj = Object(
            position=self.position.copy(), mass=self.mass, velocity=self.velocity.copy()
        )

    def test_valid_initialization(self):
        self.assertEqual(self.obj.mass, self.mass)
        self.assertTrue(np.array_equal(self.obj.position, self.position))
        self.assertTrue(np.array_equal(self.obj.velocity, self.velocity))
        self.assertTrue(np.array_equal(self.obj.acceleration, np.zeros(self.dim)))
        self.assertEqual(self.obj.dim, self.dim)

    def test_invalid_dimension_mismatch(self):
        with self.assertRaises(ExceptionGroup):
            Object(position=np.zeros(2), mass=1.0, velocity=np.zeros(3))

    def test_invalid_mass(self):
        with self.assertRaises(ExceptionGroup):
            Object(position=np.zeros(3), mass=0, velocity=np.zeros(3))

        with self.assertRaises(ExceptionGroup):
            Object(position=np.zeros(3), mass=-1, velocity=np.zeros(3))

    def test_invalid_radius(self):
        with self.assertRaises(ExceptionGroup):
            Object(position=np.zeros(3), mass=1, velocity=np.zeros(3), radius=-1)

    def test_zero_dimensions(self):
        with self.assertRaises(ExceptionGroup):
            Object(position=np.array([]), mass=1, velocity=np.array([]))

    def test_valid_sequence(self):
        self.assertTrue(self.obj.valid_sequence(np.zeros(self.dim)))
        self.assertFalse(self.obj.valid_sequence(np.zeros(self.dim + 1)))
