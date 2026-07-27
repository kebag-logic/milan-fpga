# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Latency: decode the AAF latency taps, and split "in-system" from the pto.
#!
#! The taps count **axis_clk cycles**; the only conversion is by the board's
#! datapath clock (`Board.cycles_to_us`).
#!
#! ## What "in-system" means here (USER decision)
#!
#! The RX chain is `MAC_RX -> ACCEPT -> DEPKT -> PCM_RING` and the TX chain is
#! `CAP -> PKT_SOF -> PKT_EOF -> MAC_TX`. One stage on each side is not
#! pipeline latency at all - it is **the presentation offset being implemented**:
#!
#!   * RX `d2` (`DEPKT -> PCM_RING`) is the ring-fill, measured sitting at the
#!     125 us class-A interval.
#!   * TX `d0` (`CAP -> PKT_SOF`) is the 6-sample AAF accumulation window,
#!     6/48 kHz = 125.0 us - the packetiser's structure, not a stall.
#!
#! Counting those against a one-sample budget would be measuring the pto twice.
#! So **in-system RX = d0 + d1** and **in-system TX = d1 + d2**, and the budget
#! is one sample: 20.83 us at 48 kHz. The excluded stages are still reported,
#! because they are what the pto sweep checks separately.
#!
#! ## Reading the tap words honestly
#!
#! Each delta packs `{max16, last16}` with `min` in its own word, all saturating
#! at 16 bits. A `0xFFFF` is "at least", not a value - and after any period when
#! the chain was timing out, `max` and the `INFO` timeout count are polluted.
#! `TapChain.trustworthy` says so rather than letting a saturated max silently
#! become a latency result.

from __future__ import annotations

from dataclasses import dataclass, asdict

SAT16 = 0xFFFF


@dataclass(frozen=True)
class Delta:
    name: str
    last_cyc: int
    min_cyc: int
    max_cyc: int

    @property
    def saturated(self) -> bool:
        return self.max_cyc >= SAT16 or self.last_cyc >= SAT16 or self.min_cyc >= SAT16


@dataclass(frozen=True)
class TapChain:
    direction: str            # "tx" | "rx"
    samples: int
    timeouts: int
    epoch_ns: int
    deltas: tuple[Delta, ...]

    @property
    def trustworthy(self) -> bool:
        """False when the numbers cannot be believed as an envelope.

        `samples == 0` means nothing completed. A nonzero timeout count means
        tokens were abandoned, which pollutes `max` (and the saturating INFO
        word) with the blocked period - only `min`/`last` survive that, and the
        caller is told so instead of quietly averaging garbage.
        """
        return self.samples > 0 and self.timeouts == 0

    def by_name(self, name: str) -> Delta:
        for d in self.deltas:
            if d.name == name:
                return d
        raise KeyError(name)

    def as_dict(self) -> dict:
        return {"direction": self.direction, "samples": self.samples,
                "timeouts": self.timeouts, "epoch_ns": self.epoch_ns,
                "trustworthy": self.trustworthy,
                "deltas": [asdict(d) for d in self.deltas]}


def _split(word: int) -> tuple[int, int]:
    return (word & 0xFFFF, (word >> 16) & 0xFFFF)   # (last, max)


def decode(snap, direction: str) -> TapChain:
    """Build a TapChain from a CSR snapshot."""
    d = direction.lower()
    if d not in ("tx", "rx"):
        raise ValueError(f"direction must be tx or rx, not {direction!r}")
    pre = f"LTAP_{d.upper()}_"
    info = snap[pre + "INFO"]
    names = (("d0", "CAP->PKT_SOF"), ("d1", "PKT_SOF->PKT_EOF"), ("d2", "PKT_EOF->MAC_TX")) \
        if d == "tx" else \
        (("d0", "MAC_RX->ACCEPT"), ("d1", "ACCEPT->DEPKT"), ("d2", "DEPKT->PCM_RING"))
    deltas = []
    for key, label in names:
        last, mx = _split(snap[pre + key.upper()])
        mn = snap[pre + key.upper() + "_MIN"] & 0xFFFF
        deltas.append(Delta(name=f"{key} {label}", last_cyc=last, min_cyc=mn,
                            max_cyc=mx))
    return TapChain(direction=d, samples=info & 0xFFFF,
                    timeouts=(info >> 16) & 0xFFFF,
                    epoch_ns=snap[pre + "EPOCH"], deltas=tuple(deltas))


#: Which stage each direction EXCLUDES from the in-system figure, and why.
EXCLUDED = {
    "rx": (2, "DEPKT->PCM_RING is the ring-fill that implements the pto"),
    "tx": (0, "CAP->PKT_SOF is the 6-sample AAF accumulation window (125.0 us)"),
}


@dataclass(frozen=True)
class InSystem:
    direction: str
    stages: tuple[str, ...]
    excluded_stage: str
    excluded_reason: str
    last_us: float
    min_us: float
    max_us: float
    budget_us: float
    trustworthy: bool

    @property
    def within_budget(self) -> bool:
        """Judged on the worst BELIEVABLE figure.

        With a clean chain that is `max`; when the chain saturated or timed out
        it is `last`, and `trustworthy` is False so the caller reports the
        weaker claim honestly instead of passing on a polluted maximum.
        """
        v = self.max_us if self.trustworthy else self.last_us
        return v <= self.budget_us

    def as_dict(self) -> dict:
        d = asdict(self)
        d["within_budget"] = self.within_budget
        return d


def in_system(chain: TapChain, board, budget_us: float) -> InSystem:
    """The in-system figure for one direction, with the pto stage removed."""
    drop, why = EXCLUDED[chain.direction]
    kept = [d for i, d in enumerate(chain.deltas) if i != drop]
    dropped = chain.deltas[drop]
    sat = any(d.saturated for d in kept)
    return InSystem(
        direction=chain.direction,
        stages=tuple(d.name for d in kept),
        excluded_stage=dropped.name,
        excluded_reason=why,
        last_us=board.cycles_to_us(sum(d.last_cyc for d in kept)),
        min_us=board.cycles_to_us(sum(d.min_cyc for d in kept)),
        max_us=board.cycles_to_us(sum(d.max_cyc for d in kept)),
        budget_us=budget_us,
        trustworthy=chain.trustworthy and not sat,
    )


@dataclass(frozen=True)
class PtoPoint:
    pto_us: float
    measured_us: float
    tolerance_us: float

    @property
    def ok(self) -> bool:
        return abs(self.measured_us - self.pto_us) <= self.tolerance_us

    def as_dict(self) -> dict:
        d = asdict(self)
        d["ok"] = self.ok
        d["error_us"] = round(self.measured_us - self.pto_us, 3)
        return d


def pto_sweep_verdict(points: list[PtoPoint]) -> tuple[bool, str]:
    """`E2E latency == pto` must hold at EVERY pto tested, not on average."""
    if not points:
        return (False, "no pto points measured")
    bad = [p for p in points if not p.ok]
    if bad:
        worst = max(bad, key=lambda p: abs(p.measured_us - p.pto_us))
        return (False, f"{len(bad)}/{len(points)} pto points off budget; worst "
                       f"pto={worst.pto_us:.0f}us measured={worst.measured_us:.1f}us")
    return (True, f"E2E latency == pto at all {len(points)} pto values "
                  f"(+/- {points[0].tolerance_us:.0f}us)")
