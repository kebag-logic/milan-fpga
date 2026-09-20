#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The saved-state co-simulation's ORACLE: what a container should hold.

Every record this module frames, it frames itself, from the case file's own
bindings and the repository's record table -- never from anything the
firmware under test produced. `cosim_checks.py` compares those frames with
the journal slots a run dumped, decoded by the repository's own
``scripts/nvm_klj2.py``, and :class:`Ctx` is the reading face it does it
through: one run, one shape, and the questions a check asks of them.

Private to the suite; `cosim_checks.py` is its only consumer.
"""
from __future__ import annotations

import dataclasses
import struct
from pathlib import Path

#: the co-simulation's backend clock in MODEL time: one cycle is 1 us
CLK_HZ = 1_000_000
#: the capture hold bound the suite builds with, in those milliseconds
T_HOLD_MS = 50
#: the contract tag a build carrying the contract publishes at [31:24]
TAG_C3 = 0xC3

from nvm_klj2 import klj2_decode      # noqa: E402  (after the path is set up)
from nvm_contract import VD_OK        # noqa: E402


@dataclasses.dataclass
class ShapeInfo:
    name: str
    header: str            # the generated constants header
    records: Path          # the record table from the record-space gate
    params: dict
    donor: object
    ident: object
    expect: dict
    img_len: int
    recs: dict             # rid -> (offset, framed length)


@dataclasses.dataclass
class Run:
    case: str
    build: str
    variant: str
    exit: int
    wall_s: float
    obs: dict
    notes: dict
    evts: list
    fw: list
    done: bool
    pending: bool
    outdir: Path


def _crc16(d: bytes) -> int:
    c = 0xFFFF
    for x in d:
        c ^= x << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return c


def _frame(rid: int, payload: bytes) -> bytes:
    hdr = bytes([0x17, 0x22, 0x02, rid, len(payload) >> 8, len(payload) & 0xFF])
    return hdr + _crc16(hdr + payload).to_bytes(2, "big") + payload


def _bind_frame(sink: int, state: tuple[int, int, int],
                ids: tuple[int, int, int]) -> bytes:
    """One binding record, framed here and never read back from anything
    the firmware produced: `state` is (bound, started, srp_wait) and `ids` is
    (unique id, talker entity id, controller entity id)."""
    bound, started, sw = state
    uid, teid, ceid = ids
    pl = bytes([bound | started << 1 | sw << 2, 0]) + uid.to_bytes(2, "big") + \
        teid.to_bytes(8, "big") + ceid.to_bytes(8, "big")
    return _frame(0x20 + sink, pl)


#: The case file's bindings, framed independently here: sink, then the state
#: triple (bound, started, srp_wait) and the identity triple (unique id,
#: talker entity id, controller entity id).
B = {
    "X":  (0, (1, 1, 0), (1, 0x1122334455667788, 0x99aabbccddeeffff)),
    "X2": (0, (1, 0, 0), (1, 0x1122334455667788, 0x99aabbccddeeffff)),
    "X3": (0, (1, 1, 1), (3, 0x2122232425262728, 0x99aabbccddeeffff)),
    "Z":  (1, (1, 1, 0), (2, 0x0102030405060708, 0x1112131415161718)),
    "Z2": (1, (1, 0, 0), (2, 0x0102030405060708, 0x1112131415161718)),
    "Z3": (1, (1, 1, 1), (4, 0x3132333435363738, 0x1112131415161718)),
}
F = {k: _bind_frame(*v) for k, v in B.items()}
F["FMT_A"] = _frame(0x30, bytes([0x00, 0xA0, 0x02, 0x01, 0x00, 0x40, 0x00, 0x08]))


class Ctx:
    """What a check may read about one run."""

    def __init__(self, run: Run, s: ShapeInfo):
        self.r, self.s = run, s
        self._slots = {}

    def o(self, tag: str) -> dict:
        """The observation the case dumped at `tag`, or a KeyError naming
        it: a check that asks for a point the case never reached is a check
        aimed at the wrong case, not a pass."""
        if tag not in self.r.obs:
            raise KeyError(f"no observation '{tag}'")
        return self.r.obs[tag]

    def contract(self, tag: str = "boot") -> bool:
        """Whether the build under test carries the snapshot-ownership
        contract, read from the tag the backend publishes at [31:24]."""
        return (self.o(tag)["stat"] >> 24) == TAG_C3

    def newest(self, tag: str) -> tuple[str, bytes, int] | None:
        """The slot the A/B rule of section 7 would offer, decoded by the
        repository's klj2_decode: (letter, blob, seq) or None."""
        if tag in self._slots:
            return self._slots[tag]
        ok = []
        for letter in "AB":
            raw = (self.r.outdir / f"{tag}-slot{letter}.bin").read_bytes()
            n = struct.unpack_from("<I", raw, 16)[0] if raw[:4] != b"\xff" * 4 else 0
            blob = raw[:n] if 44 <= n <= 65536 else raw[:44]
            vd, _ = klj2_decode(blob, self.s.donor, self.s.ident, self.s.expect)
            if vd == VD_OK:
                ok.append((letter, blob, struct.unpack_from("<I", blob, 8)[0]))
        res = None
        if len(ok) == 2:
            a, b = ok
            d = (a[2] - b[2]) & 0xFFFFFFFF
            res = a if d < 0x80000000 else b
        elif ok:
            res = ok[0]
        self._slots[tag] = res
        return res

    def rec(self, tag: str, rid: int) -> bytes | None:
        """Record `rid`'s bytes in the slot the A/B rule would offer at
        `tag`, or None when no slot is acceptable there."""
        n = self.newest(tag)
        if n is None:
            return None
        off, ln = self.s.recs[rid]
        return n[1][40 + off:40 + off + ln]

    def durable_claim(self, tag: str) -> bool:
        """What a reader of the published bits concludes: durable when
        backed, not dirty, not stale and -- on a build that has it, per the
        owner decision -- nothing pending. The tracked build has no pending
        bit, so its claim is the section 9.3 (1, 0, 0) row."""
        o = self.o(tag)
        return (o["backed"] == 1 and o["dirty_pub"] == 0 and o["stale"] == 0
                and o["pend"] == 0)

    def dirty_img(self, tag: str) -> int:
        """PP_NVM_STAT[8] at `tag`: the COMMITTABLE image work, which is
        what drives a commit and what an acknowledgement can retire."""
        return (self.o(tag)["stat"] >> 8) & 1


def _erased(b: bytes | None) -> bool:
    return b is not None and all(x == 0xFF for x in b)

