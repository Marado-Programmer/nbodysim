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
from queue import ShutDown
import unittest
import time

from nbodysim.loop import Loop, fixed_step, variable_step


class TestLoop(unittest.TestCase):
    def collect_n(self, loop, n, timeout=1.0):
        result = []
        start = time.monotonic()

        while len(result) < n:
            if time.monotonic() - start > timeout:
                self.fail("Timeout while collecting values")

            try:
                result.append(next(loop))
            except StopIteration:
                time.sleep(0.001)

        return result

    def test_start_and_produce(self):
        with Loop(variable_step) as loop:
            loop.skip_forward(3)
            values = self.collect_n(loop, 3)

            self.assertEqual(len(values), 3)
            for dt in values:
                self.assertGreaterEqual(dt, 0)

    def test_pause_stops_production(self):
        with Loop(variable_step, queue_block=False) as loop:
            loop.skip_forward(2)
            self.collect_n(loop, 2)

            loop.pause()
            loop.refresh()

            time.sleep(0.01)

            with self.assertRaises(StopIteration):
                next(loop)

    def test_skip_forward_exact_count(self):
        with Loop(variable_step, queue_block=False) as loop:
            loop.skip_forward(5)
            values = self.collect_n(loop, 5)

            self.assertEqual(len(values), 5)

            loop.refresh()
            with self.assertRaises(StopIteration):
                next(loop)

    def test_skip_forward_zero_or_negative(self):
        with Loop(variable_step, queue_block=False) as loop:
            with self.assertRaises(ValueError):
                loop.skip_forward(0)
            time.sleep(0.02)

            with self.assertRaises(StopIteration):
                next(loop)

            with self.assertRaises(ValueError):
                loop.skip_forward(-5)
            time.sleep(0.02)

            with self.assertRaises(StopIteration):
                next(loop)

    def test_queue_drop_oldest(self):
        with Loop(variable_step, queue_maxsize=1, drop=True) as loop:
            loop.start()
            time.sleep(0.05)

            next(loop)
            time.sleep(0.01)
            dt2 = next(loop)

            self.assertGreaterEqual(dt2, 0)

    def test_queue_blocking(self):
        with Loop(variable_step, queue_maxsize=1, queue_block=True) as loop:
            loop.start()

            dt1 = self.collect_n(loop, 1)[0]

            dt2 = self.collect_n(loop, 1)[0]

            self.assertGreaterEqual(dt1, 0)
            self.assertGreaterEqual(dt2, 0)

    def test_strategy_switch_resets(self):
        with Loop(variable_step) as loop:
            loop.skip_forward(2)
            self.collect_n(loop, 2)

            loop.strategy = lambda: fixed_step(0.01)

            loop.skip_forward(3)
            vals2 = self.collect_n(loop, 3)

            for dt in vals2:
                self.assertAlmostEqual(dt, 0.01, places=3)

    def test_fixed_step_outputs_constant_dt(self):
        with Loop(lambda: fixed_step(0.02)) as loop:
            loop.skip_forward(5)
            values = self.collect_n(loop, 5)

            for dt in values:
                self.assertAlmostEqual(dt, 0.02, places=3)

    def test_refresh_clears_queue(self):
        with Loop(variable_step, queue_block=False) as loop:
            loop.skip_forward(5)
            time.sleep(0.05)

            loop.refresh()

            with self.assertRaises(StopIteration):
                next(loop)

    def test_stop_terminates_loop(self):
        with Loop(variable_step) as loop:
            loop.start()
            time.sleep(0.02)

        time.sleep(0.02)

        self.assertFalse(loop.looping)

    def test_non_blocking_iteration(self):
        with Loop(variable_step, queue_block=False) as loop:
            with self.assertRaises(StopIteration):
                next(loop)

    def test_queue_shutdown_stops_iteration(self):
        loop = Loop(variable_step)

        loop.start()
        time.sleep(0.02)
        loop.stop()

        time.sleep(0.02)

        with self.assertRaises((StopIteration, ShutDown)):
            loop.refresh()

    def test_pause_resume(self):
        with Loop(variable_step, queue_block=False) as loop:
            loop.start()
            time.sleep(0.02)

            loop.pause()
            loop.refresh()

            time.sleep(0.02)

            with self.assertRaises(StopIteration):
                next(loop)

            loop.start()
            vals = self.collect_n(loop, 2)

            self.assertEqual(len(vals), 2)

    def test_strategy_switch_while_running(self):
        with Loop(variable_step) as loop:
            loop.start()
            time.sleep(0.02)

            loop.strategy = lambda: fixed_step(0.01)

            loop.skip_forward(3)
            vals = self.collect_n(loop, 3)

            for dt in vals:
                self.assertAlmostEqual(dt, 0.01, places=3)
