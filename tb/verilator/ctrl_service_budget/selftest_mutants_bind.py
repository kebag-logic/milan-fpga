# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""#1009's mutants of the self-test (selftest_mutants.py): the binding class's grade (bind_save.py) and a save's verify
(save_grade.py), each rule replaced with a plausible defect; selftest_bind.py's checks catch each."""
from __future__ import annotations

import dataclasses
import os
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import bind_save
import grade
import save_burst
import save_grade


class _Answered(dict):
    """Responses that answer every sequence_id, at cycle 0 with SUCCESS, where the log lacks one."""

    def __contains__(self, key: object) -> bool:
        return True

    def __missing__(self, key: int) -> tuple[int, int]:
        return (0, 0)


def _slot_a(path: Path, image: int, base: int) -> dict[int, bytes]:
    """bind_save.bind_of reading slot A whatever the two slots' sequences."""
    data = path.read_bytes()
    return bind_save.held(data[:image], image, base) if save_burst.accepted(data[:image], image) is not None else {}


def _bytes_summed(reads: list, spans: list) -> int | None:
    """save_grade.read_back counting every run's bytes, a byte read twice twice."""
    done, want = 0, sum(b - a for a, b in spans)
    for _, end, _, n in sorted(reads, key=lambda r: r[1]):
        done += n
        if spans and done >= want:
            return end
    return None


def _merged_across(log: grade.Log) -> list:
    """save_grade.merged_reads as before #1009: runs merged whatever write came between them."""
    out: list[list[int]] = []
    for first, last, address, n in log.reads:
        if out and out[-1][2] <= address <= out[-1][2] + out[-1][3] and first - out[-1][1] <= log.sys_hz // 1000:
            out[-1][1], out[-1][3] = max(out[-1][1], last), max(out[-1][3], address + n - out[-1][2])
        else:
            out.append([first, last, address, n])
    return [tuple(run) for run in out]


def _idle_without(word: str) -> list:
    """bind_save.idle_faults with the faults that say word left out."""
    return [patch.object(bind_save, 'idle_faults', lambda *a, f=bind_save.idle_faults: [
        x for x in f(*a) if word not in x])]


def _flight_without(word: str) -> list:
    """bind_save.flight_faults with the faults that say word left out."""
    return [patch.object(bind_save, 'flight_faults', lambda *a, f=bind_save.flight_faults: [
        x for x in f(*a) if word not in x])]


def _burst_without(word: str) -> list:
    """bind_save.burst_faults with the faults that say word left out."""
    return [patch.object(bind_save, 'burst_faults', lambda *a, f=bind_save.burst_faults: [
        x for x in f(*a) if word not in x])]


MUTANTS: dict[str, Callable[[], list]] = {
    "bind: a command's status is not read": lambda: [patch.object(
        bind_save, 'responses', lambda log, _r=bind_save.responses: {k: (c, 0) for k, (c, _) in _r(log).items()})],
    'bind: an unanswered command is not refused': lambda: [patch.object(
        bind_save, 'responses', lambda log, _r=bind_save.responses: _Answered(_r(log)))],
    'bind: the target is not held': lambda: [patch.object(
        bind_save, 'misses', lambda g, name, _m=bind_save.misses: [
            w for w in _m(g, name) if 'over its target' not in w])],
    'bind: a save erased before the response counts': lambda: [patch.object(
        bind_save, 'first_durable', lambda done, cycle, *a, _f=bind_save.first_durable: _f(done, -1, *a))],
    "bind: a save's contents are not read": lambda: [patch.object(
        bind_save, 'held', lambda blob, image, base: {s: bind_save.record(True) for s in range(bind_save.SINKS)})],
    "bind: the cut's container is not read": lambda: [patch.object(bind_save, 'bind_of', lambda path, image, base: {})],
    'bind: the cut reads slot A whatever the sequences': lambda: [patch.object(bind_save, 'bind_of', _slot_a)],
    'bind: a missing journal passes': lambda: [patch.object(
        bind_save, 'misses', lambda g, name, _m=bind_save.misses: [
            w for w in _m(g, name) if 'left no journal' not in w])],
    "bind: the part's times the run modelled are not checked": lambda: [patch.object(
        bind_save, 'flash_times', lambda log, group: tuple(group.save['flash_us']))],
    "bind: a group's run does not model the part": lambda: [patch.object(
        bind_save, 'environment', lambda save, journal, f=bind_save.environment: f(
            {k: v for k, v in save.items() if k != 'flash_us'}, journal))],
    "bind: a group's run keeps the part's times the harness was started with": lambda: [patch.object(
        bind_save, 'environment', lambda save, journal, f=bind_save.environment: {**os.environ, **f(save, journal)})],
    'bind: a save that is not a whole container read back passes': lambda: [patch.object(
        bind_save, 'whole_faults', lambda every: [])],
    'idle: a command with a save in flight is graded as one to an idle store': lambda: _idle_without('idle store'),
    'idle: a command that took two saves is graded': lambda: _idle_without('saves, not one'),
    "idle: a save erased before the command's window is graded as its own": lambda: _idle_without('before its window'),
    'flight: a bind the save in flight took in its capture is graded': lambda: _flight_without('capture ended'),
    "flight: a bind whose response came outside its arrival's phase is graded": lambda: _flight_without(
        'phase, not in'),
    'flight: a run of other saves than the two is graded': lambda: _flight_without('saves, not the one'),
    'flight: the seal measured from the first CRC call in the log': lambda: [patch.object(
        bind_save, 'phase_of', lambda log, save, cycle, f=bind_save.phase_of: f(
            dataclasses.replace(log, traced=[t for t in log.traced if t[3] != bind_save.SEAL_CALL]
                                + [t for t in log.traced if t[3] == bind_save.SEAL_CALL][:1]), save, cycle))],
    'burst: more erases than the cap are graded': lambda: _burst_without('erases, more than'),
    'burst: a burst of one save is graded': lambda: _burst_without('during another save'),
    'arrivals: none just after the capture': lambda: [patch.object(
        bind_save, 'arrivals', lambda image, f=bind_save.arrivals: f(image)[1:])],
    'verify: a byte read twice counts twice': lambda: [patch.object(save_grade, 'read_back', _bytes_summed)],
    'verify: a read before the last page was programmed counts': lambda: [patch.object(
        save_grade, 'verify_reads', lambda log, last, stop: [r for r in log.reads if r[0] < stop])],
    'verify: a run of reads across a write is graded': lambda: [patch.object(save_grade, 'in_order', lambda log: None)],
    'verify: runs of reads merged across a write': lambda: [patch.object(save_grade, 'merged_reads', _merged_across)],
}
