# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Recovery: restore the working binding, then PROVE the box is known-good.
#!
#! **Half-recovered is the dangerous outcome.** A board can answer ssh, answer
#! `devmem`, and report a bound listener while accepting not one frame - that
#! exact combination is what the accept blocker looked like. So "responds" is
#! never a recovery criterion here: `assert_known_good()` runs positive checks
#! per plane, including a MOVEMENT check on the RX parser, and a step is only
#! finished when they pass.
#!
#! Every destructive step goes through `destructive()`, which restores in a
#! `finally` and asserts known-good afterwards - so an exception inside the step
#! cannot leave the bench armed, looped back or link-cut.

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from . import csr as csrmod
from .transport import Outage

BOARD_DIR = Path(__file__).resolve().parent.parent / "board"


class NotKnownGood(Exception):
    """The box did not come back to a proven-good state."""


@dataclass
class KnownGood:
    ok: bool
    checks: dict
    raw: str

    @property
    def failures(self) -> list[str]:
        return [k for k, v in self.checks.items() if not v]


def parse_known_good(text: str) -> KnownGood:
    checks: dict[str, bool] = {}
    ok = False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("CHECK "):
            rest = line[6:]
            name, _, verdict = rest.partition(":")
            checks[name.strip()] = verdict.strip().startswith("PASS")
        elif line.startswith("KNOWN_GOOD:"):
            ok = "PASS" in line
    return KnownGood(ok=ok and all(checks.values()) and bool(checks),
                     checks=checks, raw=text)


def assert_known_good(transport, board, *, timeout: int = 120) -> KnownGood:
    r = transport.push_sh(board.ssh, BOARD_DIR / "known_good.sh",
                          via_jump=board.via_jump, timeout=timeout,
                          args=[hex(board.csr_base), hex(board.version_expect),
                                board.netif])
    kg = parse_known_good(r.out)
    if not kg.ok:
        raise NotKnownGood(
            f"{board.name} is not known-good: failing {kg.failures or ['(no checks parsed)']}")
    return kg


@dataclass
class Binding:
    """The working binding a destructive step must put back."""
    direction: str
    index: int
    sid: int
    dmac: int | None
    ctrl: int


def capture_binding(csr: "csrmod.Csr", direction: str, index: int) -> Binding:
    """Read the live binding BEFORE anything destructive touches it.

    Read order matters: a bind edge CLEARS the per-stream error counters
    (Milan 5.3.8.10), so any counter reading a caller cares about must be taken
    here, before a re-bind, or it reads clean and proves nothing.
    """
    w = csr.window(direction, index)
    return Binding(direction=direction, index=index,
                   sid=w["sid"] if isinstance(w["sid"], int) else 0,
                   dmac=w["dmac"] if isinstance(w["dmac"], int) else None,
                   ctrl=w["ctrl"] or 0)


def restore_binding(csr: "csrmod.Csr", b: Binding) -> None:
    """Put the binding back, or release entry 0 to its ACMP alias.

    A zero sid means there was no override to restore: the correct restoration
    is RELEASE-TO-ALIAS (`{en = 0, sid = 0}`), which hands the entry back to the
    live ACMP bound record rather than pinning it disabled - pinning it is what
    made the accept blocker permanent.
    """
    if not b.sid:
        csrmod.release_to_alias(csr, b.index)
        return
    csrmod.arm_context(csr, b.direction, b.index, b.sid, dmac=b.dmac,
                       ctrl=b.ctrl or 0x3)


@contextmanager
def destructive(transport, board, csr, *, binding: Binding | None = None,
                on_event=None, timeout: int = 180):
    """Wrap any step that perturbs the bench.

    On the way out - success, exception, or step timeout alike - it restores the
    binding and asserts known-good. An outage during recovery is re-raised so
    the runner can mark the item BLOCKED and, importantly, NOT continue running
    later items against a bench in an unknown state.
    """
    say = on_event or (lambda *_a, **_k: None)
    try:
        yield
    finally:
        errors = []
        if binding is not None:
            try:
                restore_binding(csr, binding)
                say("restore", {"board": board.name, "index": binding.index,
                                "sid": f"0x{binding.sid:016X}"})
            except (csrmod.CsrError, csrmod.SafetyViolation, Outage) as exc:
                errors.append(f"binding restore: {exc}")
        try:
            kg = assert_known_good(transport, board, timeout=timeout)
            say("known-good", {"board": board.name, "checks": kg.checks})
        except (NotKnownGood, Outage) as exc:
            errors.append(str(exc))
        if errors:
            raise NotKnownGood(
                f"{board.name} did not return to a known-good state: "
                + "; ".join(errors))


def disarm_all_extra_talkers(csr: "csrmod.Csr", board) -> list[int]:
    """The standing safety sweep: no `t > 0` context left armed.

    Run at the end of every phase that could have armed one, and before the
    harness exits. An armed extra talker with the lwSRP engine off transmits
    unpaced (~56 k frames/s measured) and takes the peer board off the network -
    so this sweep runs with the engine ON, which is also the only state in which
    the disarm is actually stored.
    """
    disarmed: list[int] = []
    lwsrp_on = bool(csr.read("LWSRP_CTRL") & 1)
    if not lwsrp_on:
        csr.write("LWSRP_CTRL", csr.read("LWSRP_CTRL") | 1)
    for t in range(1, max(1, board.n_talkers)):
        w = csr.window("talker", t)
        state = w["state"]
        if state in (None, csrmod.NOT_BACKED):
            continue
        if (state >> 3) & 1:
            csr._arm_state = {"dir": 1, "idx": t, "lwsrp_on": True,
                              "sid_staged_for": t}
            csr.write_many([("A_STRM_SEL", (1 << 8) | t),
                            ("A_STRMW_SID_LO", 0), ("A_STRMW_SID_HI", 0),
                            ("A_STRMW_CTRL", 0)], guard=False)
            disarmed.append(t)
    return disarmed
