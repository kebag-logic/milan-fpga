#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent arithmetic controls for the additional USB egress term."""
from __future__ import annotations

import dataclasses
import sys

import egress_grade
import egress_usb as usb


def controls() -> dict[str, bool]:
    """Known wire times and two busy periods, independent of queue output."""
    p = dataclasses.replace(usb.base.params(usb.base.arty_spec()), sr_bytes=(), gptp_bytes=())
    q = usb.Queue(p)
    q.beats = 8
    q.complete(1_000_000, 64, False)
    first = q.wire_free
    first_end = q.fifo[0][1]
    q.complete(2_000_000, 64, False)
    second = q.wire_free
    in_busy = q.injections
    q.complete(second + 1_000_000, 64, False)
    # 76 on-wire octets and 12 octets of gap for a 64-byte frame.
    one_frame_ps = 76 * 80_000
    gap_ps = 12 * 80_000
    delay_ps = 123_200_000 + 260_000
    recs = [usb.base.Record(10, 2, 381, 1514, 20), usb.base.Record(40, 2, 200, 792, 60)]
    refused = usb.free_space(recs, [(100, 0, 0), (120, 0, 0)], p)
    no_usb = egress_grade.grade(p.line(), p)
    edge_ps = int((1000 - 0.320 - 0.260) * 1_000_000 / 1.05) + 1000
    edge = {"edge": dict(wait_ps=edge_ps, agree_ps=0)}
    declaration = "== USBQUEUE injected_ps=123200000 handshake_ps=260000\n"
    missing = declaration + usb.base.testbench_log(p, [(10, 2, 64)])
    # A single small frame fits the FIFO: only its last wire octet moves.
    # This fixture's offset is arithmetic, independent of the USB queue.
    shifted = []
    for line in missing.splitlines():
        fields = line.split()
        if line.startswith("EGRESS "):
            fields[-1] = str(int(fields[-1]) + delay_ps)
            line = " ".join(fields)
        shifted.append(line)
    good = egress_grade.grade("\n".join(shifted) + "\n", p)
    bad = egress_grade.grade(missing, p)
    return {
        "one longest frame and handshake delay the first departure": first_end == 1_000_000 + delay_ps + one_frame_ps,
        "a second frame in the busy period adds only its own wire time":
            second - first == one_frame_ps + gap_ps and in_busy == 1,
        "a new busy period receives another injection":
            q.wire_free == second + 1_000_000 + delay_ps + one_frame_ps + gap_ps and q.injections == 2,
        "injection does not consume a datapath FIFO slot": len(q.fifo) == 3,
        "changed ring availability refuses census carry": len(refused) == 1 and refused[0]["commit"] == 40,
        "a census without injected traffic is refused": "refused" in no_usb,
        "the separate handshake counts at the 1000 us boundary": not egress_grade.verdict(edge, p)[0],
        "an independently shifted injected departure agrees":
            good.get("agree_ps", -1) == 0 and "wait_ps" in good,
        "a queue omitting injection cannot pass with only its declaration":
            bad.get("agree_ps", 0) > 0 and not egress_grade.verdict({"missing": bad}, p)[0],
    }


def main() -> int:
    """Each plant must break a named independently checked condition."""
    clean = controls()
    failures = sum(not ok for ok in clean.values())
    for name, ok in clean.items():
        print("PASS" if ok else "FAIL", name)
    original_complete = usb.Queue.complete
    original_base_complete = usb.base.Queue.complete
    original_free = usb.free_space
    original_grade = egress_grade.grade
    original_verdict = egress_grade.verdict
    original_agreement = usb.base.AGREE_PS

    def every_frame(self: usb.Queue, t: int, length: int, control: bool) -> None:
        """Plant a second injected frame ahead of already waiting datapath traffic."""
        self.wire_free = max(t, self.wire_free) + usb.INJECT_PS + usb.HANDSHAKE_PS
        self.injections += 1
        original_base_complete(self, t, length, control)

    def first_only(self: usb.Queue, t: int, length: int, control: bool) -> None:
        """Plant an envelope which forgets later busy periods."""
        if self.injections == 0:
            original_complete(self, t, length, control)
        else:
            original_base_complete(self, t, length, control)

    plants = {
        "injected-frame-omitted": lambda: setattr(usb, "INJECT_PS", 0),
        "injected-frame-at-gigabit-rate": lambda: setattr(usb, "INJECT_PS", 12_320_000),
        "handshake-omitted": lambda: setattr(usb, "HANDSHAKE_PS", 0),
        "injected-before-every-frame": lambda: setattr(usb.Queue, "complete", every_frame),
        "later-busy-period-forgotten": lambda: setattr(usb.Queue, "complete", first_only),
        "free-space-change-ignored": lambda: setattr(usb, "free_space", lambda *_: []),
        "uninjected-census-accepted": lambda: setattr(egress_grade, "grade", lambda *_: {}),
        "separate-handshake-omitted": lambda: setattr(egress_grade, "verdict", usb.base.verdict),
        "injected-departure-mismatch-ignored": lambda: setattr(usb.base, "AGREE_PS", 1_000_000_000),
    }
    for name, plant in plants.items():
        try:
            plant()
            caught = [name for name, ok in controls().items() if not ok]
        finally:
            usb.INJECT_PS, usb.HANDSHAKE_PS = 123_200_000, 260_000
            usb.Queue.complete = original_complete
            usb.free_space = original_free
            egress_grade.grade = original_grade
            egress_grade.verdict = original_verdict
            usb.base.AGREE_PS = original_agreement
        print("CAUGHT" if caught else "MISSED", name, "; ".join(caught))
        failures += not caught
    print(f"USB egress controls: {len(clean) + len(plants) - failures}/{len(clean) + len(plants)}")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
