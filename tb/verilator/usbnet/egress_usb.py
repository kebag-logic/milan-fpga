#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Add USB interference to the unchanged control service egress queue.

A longest injected frame precedes every wire busy period. This envelope
ignores the host token bucket, conservatively. The injection occupies no
store-and-forward slot, but delays its releases and hence mailbox tails.
The baseline replay must first reproduce every recorded departure exactly.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVICE = HERE.parent / "ctrl_service_budget"
sys.path.insert(0, str(SERVICE))
import egress_mii as base
import receipt_regrade

#: Rounded up from 1539 wire octets at 100 Mb/s, including inter-frame gap.
INJECT_PS = 123_200_000
#: Filled by the shipping-chain measurement, conservatively rounded upward.
HANDSHAKE_PS = 260_000


class Queue(base.Queue):
    """The inherited queue with one lower-priority frame per busy period."""

    def __init__(self, p: base.Params, phase_ps: int = 0) -> None:
        super().__init__(p, phase_ps)
        self.injections = 0

    def complete(self, t: int, length: int, control: bool) -> None:
        """A grant just before the first waiting datapath frame delays that busy period."""
        if t >= self.wire_free:
            self.wire_free = t + INJECT_PS + HANDSHAKE_PS
            self.injections += 1
        super().complete(t, length, control)


def replay(recs: list[base.Record], holds: list, p: base.Params, phase_ps: int) -> tuple[list, int]:
    """Replay unchanged commit times, with byte-level backpressure from injection.

    The baseline's small host-acknowledgement offsets are recovered first.
    They are then kept, never re-fitted to the delayed USB departures.
    """
    q0, q = base.Queue(p, 0), Queue(p, phase_ps)
    windows, free0, free = base.hold_windows(holds), 0, 0
    tails = []
    for r in recs:
        e0 = max(r.commit + base.MBX_VISIBLE, free0) + base.MBX_LEAD
        offset = next((d for d in base.ANCHOR if base.stream(q0.clone(), r, e0 + d, windows) == r.wire), None)
        if offset is None:
            raise ValueError(f"cannot reproduce baseline mailbox departure at {r.wire}")
        free0 = base.stream(q0, r, e0 + offset, windows) + base.MBX_AFTER
        start = max(r.commit + base.MBX_VISIBLE, free) + base.MBX_LEAD + offset
        tails.append(base.stream(q, r, start, windows))
        free = tails[-1] + base.MBX_AFTER
    q.advance((free + 1) * p.sys_ps + 64 * p.wire_ps(1514) + 2 * p.gptp_period_ps // 1000)
    out = {(d[0], d[1]): d for d in q.departed}
    return [(tail, out[tail, r.ch][3], out[tail, r.ch][4]) for tail, r in zip(tails, recs)], q.injections


def free_space(recs: list, tails: list, p: base.Params) -> list:
    """Refuse a commit lacking space, before claiming the census carries.

    Each record retires two system cycles after its last byte (KL_mbx_tx DONE).
    This checks successful commits; exact tail equality is additionally required
    for other readers and failed free-space tests not printed in a trace.
    """
    seen: dict = {}
    fails = []
    for i in sorted(range(len(recs)), key=lambda j: recs[j].commit):
        r = recs[i]
        previous = seen.setdefault(r.ch, [])
        used = sum(recs[j].words for j in previous if tails[j][0] + base.MBX_AFTER >= r.commit)
        if used + r.words > p.ring_words[r.ch]:
            fails.append(dict(commit=r.commit, ch=r.ch, used=used, need=r.words, capacity=p.ring_words[r.ch]))
        previous.append(i)
    return fails


def grade(text: str, p: base.Params) -> dict:
    """All records, the inherited held-egress disposition, and eight SR phases."""
    baseline = base.grade_case(text, p)
    if "refused" in baseline or baseline["agree_ps"]:
        return dict(refused="baseline does not reproduce", baseline=baseline)
    log = base.parse(text)
    recs = base.records(log)
    base.mark_held(recs, base.hold_windows(log["holds"]), [r.egress[4] // p.sys_ps + 1 for r in recs])
    worst, changed, fails, injected = 0, 0, [], 0
    for phase in range(base.PHASES):
        run, count = replay(recs, log["holds"], p, phase * p.sr_period_ps // base.PHASES)
        injected = max(injected, count)
        if phase == 0:
            changed = sum(t != r.wire for r, (t, _, _) in zip(recs, run))
            fails = free_space(recs, run, p)
        worst = max([worst] + [end - r.commit * p.sys_ps for r, (_, _, end) in zip(recs, run) if not r.held])
    return dict(records=len(recs), held=sum(r.held for r in recs), wait_ps=worst, changed_tails=changed,
                free_space_failures=fails, injections=injected, baseline=baseline)


def packet(packet_dir: Path, output: Path) -> int:
    """Read every manifest-bound case and publish a replay table."""
    census = json.loads((packet_dir / "census.json").read_text())
    p, rows = base.params(base.arty_spec()), {}
    for row in census["cases"]:
        path = packet_dir / row["manifest"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError("manifest hash mismatch: " + row["case"])
        manifest = json.loads(path.read_text())
        raw = receipt_regrade.read_parts(path.parent, manifest["extract"], census.get("part_limit", 14_000_000) + 1)
        rows[row["case"]] = grade(raw.decode(), p)
        output.write_text(json.dumps(rows, indent=2) + "\n")
        print(row["case"], json.dumps(rows[row["case"]]), flush=True)
    worst = max(r.get("wait_ps", 0) for r in rows.values())
    bound_us = (worst + base.gptp_wire_ps(p)) * base.MARGIN / 1_000_000 + base.MII_FIXED_NS / 1000
    carry = all(not r.get("refused") and r["changed_tails"] == 0 and not r["free_space_failures"]
                for r in rows.values())
    print(f"EGRESS USB {bound_us:.3f} us; census carries {carry}; cases {len(rows)}", flush=True)
    return int(bound_us > base.BOUND_US or not carry)


if __name__ == "__main__":
    sys.exit(packet(Path(sys.argv[1]), Path(sys.argv[2])))
