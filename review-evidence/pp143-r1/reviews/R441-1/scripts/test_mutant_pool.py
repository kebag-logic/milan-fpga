#!/usr/bin/env python3
"""Probe tb/common/mutant_pool.py's contract from outside the tree.

usage: test_mutant_pool.py CLONE
"""
import argparse
import sys
import threading
import time
import unittest

sys.path.insert(0, sys.argv.pop(1) + "/tb/common")
import mutant_pool  # noqa: E402


class InOrder(unittest.TestCase):
    def test_declared_order_whatever_finish_order(self):
        def work(i):
            time.sleep(0.05 * (8 - i))  # the last unit finishes first
            return i
        with mutant_pool.in_order(work, list(range(8)), 8) as results:
            self.assertEqual(list(results), list(range(8)))

    def test_concurrency_bounded_by_jobs(self):
        live, peak, lock = [0], [0], threading.Lock()
        def work(i):
            with lock:
                live[0] += 1
                peak[0] = max(peak[0], live[0])
            time.sleep(0.05)
            with lock:
                live[0] -= 1
        for jobs, want in ((1, 1), (3, 3), (0, 1), (-2, 1)):
            peak[0] = 0
            with mutant_pool.in_order(work, list(range(9)), jobs) as results:
                list(results)
            self.assertEqual(peak[0], want, f"jobs={jobs}")

    def test_unit_exception_at_its_turn_and_rest_cancelled(self):
        started = []
        def work(i):
            started.append(i)
            time.sleep(0.05)
            if i == 2:
                raise RuntimeError("unit 2")
            return i
        got = []
        with self.assertRaises(RuntimeError):
            with mutant_pool.in_order(work, list(range(40)), 2) as results:
                for r in results:
                    got.append(r)
        self.assertEqual(got, [0, 1])
        self.assertLess(len(started), 40)

    def test_early_return_cancels_and_waits(self):
        started, finished = [], []
        def work(i):
            started.append(i)
            time.sleep(0.1)
            finished.append(i)
            return i
        def consumer():
            with mutant_pool.in_order(work, list(range(40)), 4) as results:
                for r in results:
                    return r
        self.assertEqual(consumer(), 0)
        self.assertEqual(sorted(started), sorted(finished))  # nothing left running
        self.assertLess(len(started), 40)

    def test_default_and_type(self):
        p = argparse.ArgumentParser()
        mutant_pool.add_jobs_argument(p)
        self.assertEqual(p.parse_args([]).jobs, 4)
        self.assertEqual(p.parse_args(["--jobs", "8"]).jobs, 8)
        with self.assertRaises(SystemExit):
            p.parse_args(["--jobs", "x"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
