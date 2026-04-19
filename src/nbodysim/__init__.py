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
import gettext
import locale
import logging

NAME = "nbodysim"
__version__ = "0.1.0"

logging.captureWarnings(True)

# TODO: decide what to do about the user beign able to define the locales
# directory they want, probably via CLI
locales_dir = None

translation = gettext.translation(NAME, locales_dir, fallback=True)
_ = translation.gettext
translation.install()

locale.setlocale(locale.LC_ALL, "")

G = (6.67430 + (5 / 660000)) * 1e-11
"""Gravitational constant.

References
----------
.. [1] ` Gravitational constant <https://en.wikipedia.org/wiki/Gravitational_constant>`_.
"""
