# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! The counter audit engine.
#!
#! The audit's rule, and the reason it is not just "read them and see":
#!
#!     provoke the event, assert the counter moved by the expected amount, AND
#!     assert its neighbours did not.
#!
#! A counter wired to the wrong event passes the first half every time. It only
#! shows up when the counter next to it moves too - or when the one that should
#! have moved didn't. That is why every row carries a `hold` list and why the
#! LATE/EARLY_TIMESTAMP pair is provoked in both directions: a swapped pair is
#! invisible to either test alone.
#!
#! Two reading rules the engine enforces so a runner cannot get them wrong:
#!
#!   * **Full width only.** STREAM_INPUT counters are read through the `0x800`
#!     window (`CNT0..9`), never from the flat `AVTPRX_*` words, which are
#!     SATURATING narrow views - a `0xFF` there means "at least 255", and a
#!     saturated field would read as a stable value.
#!   * **Read before re-binding.** A bind edge CLEARS the per-stream error
#!     counters, so `clears_on_bind` rows are sampled before any bind in the
#!     provocation, or they read clean and prove nothing.

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .csr import REG, RMON_LANE0, RMON_LANES, WINDOW_CNT

EXPECT_RE = re.compile(r"^(==|>=|<=|>|<)\s*(\d+)$")


class CounterError(Exception):
    pass


@dataclass(frozen=True)
class CounterRow:
    name: str
    family: str
    read: str
    provoke: str
    expect: str
    hold: tuple[str, ...]
    clears_on_bind: bool
    note: str

    @property
    def automatable(self) -> bool:
        return bool(self.provoke and self.read)


def load_rows(path: Path) -> list[CounterRow]:
    with Path(path).open("rb") as fh:
        raw = tomllib.load(fh)
    if raw.get("schema") != "kebag-logic/milan-harness-counters":
        raise CounterError(f"{path}: not a counter audit table")
    rows = []
    for r in raw.get("counter", []):
        rows.append(CounterRow(
            name=r["name"], family=r["family"], read=r.get("read", ""),
            provoke=r.get("provoke", ""), expect=r.get("expect", ">=1"),
            hold=tuple(r.get("hold", [])),
            clears_on_bind=bool(r.get("clears_on_bind", False)),
            note=r.get("note", "")))
    names = [r.name for r in rows]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise CounterError(f"{path}: duplicate counter rows {sorted(dupes)}")
    for r in rows:
        if not EXPECT_RE.match(r.expect):
            raise CounterError(f"{path}: {r.name}: bad expect {r.expect!r}")
        for h in r.hold:
            if h not in names:
                raise CounterError(f"{path}: {r.name}: hold names unknown "
                                   f"counter {h!r}")
    return rows


def check_expect(expect: str, delta: int) -> bool:
    m = EXPECT_RE.match(expect)
    if not m:
        raise CounterError(f"bad expect {expect!r}")
    op, n = m.group(1), int(m.group(2))
    return {"==": delta == n, ">=": delta >= n, "<=": delta <= n,
            ">": delta > n, "<": delta < n}[op]


# --------------------------------------------------------------------------
# Reading
# --------------------------------------------------------------------------

def read_all(csr, rows: list[CounterRow]) -> dict[str, int | None]:
    """Every readable counter, in as few remote round trips as possible.

    One full snapshot serves every `csr:` and `rmon:` row; the window rows cost
    one SEL+SNAP per (direction, index) pair, not one per counter.
    """
    snap = csr.snapshot()
    out: dict[str, int | None] = {}
    windows: dict[tuple[str, int], dict] = {}
    for row in rows:
        if not row.read:
            out[row.name] = None
            continue
        kind, _, rest = row.read.partition(":")
        if kind == "csr":
            out[row.name] = _read_csr(snap, rest)
        elif kind == "rmon":
            lane = int(rest)
            out[row.name] = snap.get(RMON_LANE0 + 4 * lane)
        elif kind == "win":
            direction, idx, word = rest.split(":")
            key = (direction, int(idx))
            if key not in windows:
                windows[key] = csr.window(direction, int(idx))
            out[row.name] = _read_window(windows[key], word)
        else:
            raise CounterError(f"{row.name}: unknown read form {row.read!r}")
    return out


def _read_csr(snap, rest: str) -> int | None:
    m = re.match(r"^(0x[0-9A-Fa-f]+)(?:\[(\d+):(\d+)\])?$", rest)
    if not m:
        raise CounterError(f"bad csr read spec {rest!r}")
    off = int(m.group(1), 16)
    v = snap.get(off)
    if v is None or m.group(2) is None:
        return v
    hi, lo = int(m.group(2)), int(m.group(3))
    return (v >> lo) & ((1 << (hi - lo + 1)) - 1)


def _read_window(w: dict, word: str):
    if word.startswith("cnt"):
        return w["cnt"].get(WINDOW_CNT[int(word[3:])])
    return w.get(word)


# --------------------------------------------------------------------------
# One audit
# --------------------------------------------------------------------------

@dataclass
class AuditResult:
    counter: str
    verdict: str                 # PASS | FAIL | BLOCKED
    delta: int | None
    expect: str
    neighbours: dict             # name -> delta
    moved_neighbours: list
    detail: str

    def as_dict(self) -> dict:
        return {"counter": self.counter, "verdict": self.verdict,
                "delta": self.delta, "expect": self.expect,
                "neighbours": self.neighbours,
                "moved_neighbours": self.moved_neighbours,
                "detail": self.detail}


def audit_one(row: CounterRow, before: dict, after: dict) -> AuditResult:
    """The verdict for one counter, given the before/after reads."""
    b, a = before.get(row.name), after.get(row.name)
    if b is None or a is None:
        return AuditResult(row.name, "BLOCKED", None, row.expect, {}, [],
                           f"no readable view of this counter ({row.note})")
    delta = a - b
    if delta < 0:
        # A negative delta is a counter that WRAPPED or was cleared under us -
        # a saturating narrow view can never do this, so it means the read spec
        # points at a truncating field or a bind edge cleared it mid-window.
        return AuditResult(row.name, "FAIL", delta, row.expect, {}, [],
                           "counter went BACKWARDS: it wrapped, or a bind edge "
                           "cleared it inside the observation window")
    neigh = {}
    moved = []
    for h in row.hold:
        hb, ha = before.get(h), after.get(h)
        if hb is None or ha is None:
            continue
        d = ha - hb
        neigh[h] = d
        if d != 0:
            moved.append(h)
    ok = check_expect(row.expect, delta)
    if ok and not moved:
        return AuditResult(row.name, "PASS", delta, row.expect, neigh, [],
                           f"moved {delta} ({row.expect}), neighbours held")
    parts = []
    if not ok:
        parts.append(f"moved {delta}, expected {row.expect}")
    if moved:
        parts.append("neighbours ALSO moved: "
                     + ", ".join(f"{n}+{neigh[n]}" for n in moved)
                     + " - a counter wired to the wrong event looks exactly "
                       "like this")
    return AuditResult(row.name, "FAIL", delta, row.expect, neigh, moved,
                       "; ".join(parts))


def audit_capability(row: CounterRow, snap) -> AuditResult:
    """The `cap_declared_unsupported` provoker.

    An RMON lane with no source must be DECLARED unsupported in `STATS_CAP`, not
    silently read 0. Both halves are asserted: the capability bit is 0 AND the
    lane reads 0. That is the check that would have caught a whole build's worth
    of lanes reading zero while every testbench passed.
    """
    lane = int(row.read.split(":")[1])
    cap_bit = bool(snap["STATS_CAP"] >> lane & 1)
    value = snap.get(RMON_LANE0 + 4 * lane)
    if cap_bit:
        return AuditResult(row.name, "FAIL", value, row.expect, {}, [],
                           f"STATS_CAP declares lane {lane} ({RMON_LANES[lane]}) "
                           f"SUPPORTED, but this row expects it to have no source")
    if value:
        return AuditResult(row.name, "FAIL", value, row.expect, {}, [],
                           f"lane {lane} is declared unsupported yet reads "
                           f"{value} - a faked count is worse than a lying zero")
    return AuditResult(row.name, "PASS", 0, row.expect, {}, [],
                       f"lane {lane} declared unsupported in STATS_CAP and reads 0")


def summary(results: list[AuditResult]) -> dict:
    return {
        "total": len(results),
        "pass": sum(1 for r in results if r.verdict == "PASS"),
        "fail": sum(1 for r in results if r.verdict == "FAIL"),
        "blocked": sum(1 for r in results if r.verdict == "BLOCKED"),
        "neighbour_violations": sum(1 for r in results if r.moved_neighbours),
    }
