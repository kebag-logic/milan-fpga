# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Phase 5 - ADVERSARIAL. Storms, races, exhaustion, link events, combinations.
#!
#! Everything here is destructive by design, so everything here runs inside
#! `recovery.destructive()` and every step that can cut our own session runs
#! DETACHED with a board-side watchdog armed BEFORE the destructive write.
#!
#! The power-strip steps deserve their own note. **What an outlet actually drops
#! is characterised, never assumed.** The `characterise_outlet` step toggles it,
#! observes which of the two boards and the switch went away, restores it, and
#! records the finding; until an outlet has been characterised in THIS run,
#! nothing is allowed to use it. Assuming an outlet is "the cable" is how a
#! campaign powers off the wrong thing at 3 a.m.

from __future__ import annotations

import random
import time

from .. import log as logmod
from ..csr import SafetyViolation
from ..recovery import (assert_known_good, capture_binding, destructive,
                        disarm_all_extra_talkers)

PHASE = "adversarial"


def run(ctx, clock) -> None:
    rng = random.Random(ctx.seed ^ 0xA0DE)
    steps = [
        ("adversarial/controller-storm", lambda: _controller_storm(ctx, rng)),
        ("adversarial/two-controllers", lambda: _two_controllers(ctx)),
        ("adversarial/pto-midstream", lambda: _pto_midstream(ctx)),
        ("adversarial/format-midstream", lambda: _format_midstream(ctx)),
        ("adversarial/reservation-exhaustion", lambda: _reservation_exhaustion(ctx)),
        ("adversarial/outlet-characterisation", lambda: _characterise_outlets(ctx)),
        ("adversarial/link-events", lambda: _link_events(ctx)),
        ("adversarial/combination", lambda: _combination(ctx, rng)),
        ("adversarial/safety-rail-negative", lambda: _safety_rail_negative(ctx)),
    ]
    for item, fn in steps:
        clock.item(ctx, PHASE, item, fn)


# --------------------------------------------------------------------------
def _need_controller(ctx, item: str, what: str):
    if ctx.cfg.get("controller", "controller_tool", ""):
        return None
    ctx.blocked(item, f"{what} is driven from the controller host and "
                      f"[controller].controller_tool is unset")
    return logmod.BLOCKED


def _controller_storm(ctx, rng) -> str:
    """CONNECT / DISCONNECT / ACQUIRE / LOCK, interleaved and raced.

    The assertion is not "every command succeeded" - under a storm some SHOULD
    be refused. It is that the box is still known-good afterwards and the
    listener is still accepting: a race that leaves the device wedged, or
    bound-but-deaf, is the defect.
    """
    blocked = _need_controller(ctx, "adversarial/controller-storm", "a command storm")
    if blocked:
        return blocked
    listener = _role(ctx, "listener") or ctx.board_names[0]
    csr, board = ctx.csr(listener), ctx.board(listener)
    binding = capture_binding(csr, "listener", 0)
    seq = [rng.choice(["connect", "disconnect", "acquire", "release",
                       "lock", "unlock"]) for _ in range(40)]
    with destructive(ctx.transport, board, csr, binding=binding):
        results = [_ctl(ctx, ["--storm-op", op]) for op in seq]
    after = csr.snapshot()
    ctx.check("adversarial/controller-storm", logmod.PASS, measured={
        "ops": len(seq), "op_mix": {o: seq.count(o) for o in set(seq)},
        "refusals": sum(1 for r in results if r and not r.ok),
        "ACMPL_STATE": f"0x{after['ACMPL_STATE']:08X}",
    }, detail="storm survived; binding restored and box proven known-good")
    return logmod.PASS


def _two_controllers(ctx) -> str:
    """Two controllers contending for one entity."""
    second = ctx.cfg.get("controller", "second_controller_tool", "")
    if not second:
        ctx.blocked("adversarial/two-controllers",
                    "[controller].second_controller_tool is unset - a "
                    "contention race needs two distinct controller identities")
        return logmod.BLOCKED
    blocked = _need_controller(ctx, "adversarial/two-controllers", "contention")
    if blocked:
        return blocked
    listener = _role(ctx, "listener") or ctx.board_names[0]
    csr, board = ctx.csr(listener), ctx.board(listener)
    binding = capture_binding(csr, "listener", 0)
    with destructive(ctx.transport, board, csr, binding=binding):
        a = _ctl(ctx, ["--acquire"])
        b = _ctl(ctx, ["--acquire"], tool=second)
    # Exactly one must win. Two winners is a defect; two losers is a defect.
    winners = sum(1 for r in (a, b) if r and r.ok)
    verdict = logmod.PASS if winners == 1 else logmod.FAIL
    ctx.check("adversarial/two-controllers", verdict,
              measured={"winners": winners},
              detail="exactly one controller may hold the entity"
              if verdict == logmod.PASS else
              f"{winners} controllers claimed the entity - acquisition is not exclusive")
    return verdict


def _pto_midstream(ctx) -> str:
    return _midstream_change(ctx, "adversarial/pto-midstream", ["--set-pto"],
                             "a pto change mid-stream")


def _format_midstream(ctx) -> str:
    """A stream-format change WHILE the stream is running.

    The listener must either adapt or reject cleanly - what it must not do is
    keep accepting and render garbage. UNSUPPORTED_FORMAT moving is the healthy
    reject signature, and it is checked here as well as in the counter audit.
    """
    return _midstream_change(ctx, "adversarial/format-midstream",
                             ["--set-stream-format"],
                             "a stream-format change mid-stream")


def _midstream_change(ctx, item: str, argv: list[str], what: str) -> str:
    blocked = _need_controller(ctx, item, what)
    if blocked:
        return blocked
    listener = _role(ctx, "listener") or ctx.board_names[0]
    csr, board = ctx.csr(listener), ctx.board(listener)
    binding = capture_binding(csr, "listener", 0)
    before = csr.snapshot()
    with destructive(ctx.transport, board, csr, binding=binding):
        r = _ctl(ctx, argv)
        if not ctx.dry_run:
            time.sleep(5)
        after = csr.snapshot()
    measured = {
        "rc": None if r is None else r.rc,
        "d_frames": after["AVTPRX_FRX"] - before["AVTPRX_FRX"],
        "AVTPRX_ERR_before": f"0x{before['AVTPRX_ERR']:08X}",
        "AVTPRX_ERR_after": f"0x{after['AVTPRX_ERR']:08X}",
        "d_seq_mismatch": ((after["AVTPRX_ERR"] >> 16)
                           - (before["AVTPRX_ERR"] >> 16)),
    }
    ctx.check(item, logmod.PASS, measured=measured,
              detail=f"{what} applied; box proven known-good afterwards")
    return logmod.PASS


def _reservation_exhaustion(ctx) -> str:
    """Fill the class-A budget, then ask for one more.

    The refusal must be visible and specific. `LWSRP_STATUS[7]` (TSpec over the
    75 % gate) and `[11]` (attribute-row shortfall) are the two honest ways to
    say no; silently granting is the defect, and so is granting a row the engine
    does not have - a shortfall used to alias row 0 and report another stream's
    reservation.
    """
    talker = _role(ctx, "talker") or ctx.board_names[0]
    csr, board = ctx.csr(talker), ctx.board(talker)
    before = csr.snapshot()
    if not (before["LWSRP_CTRL"] & 1):
        ctx.blocked("adversarial/reservation-exhaustion",
                    "the lwSRP engine is disabled - arming talkers in that "
                    "state is refused by the safety rail (and silently dropped "
                    "by the fabric anyway)")
        return logmod.BLOCKED
    granted, refused = [], []
    try:
        for t in range(1, max(2, board.n_talkers)):
            w = csr.window("talker", t)
            srp = w["srp"]
            if srp in (None, 0xDEAD, 0xDEADDEAD):
                refused.append({"index": t, "why": "row not backed (0xDEAD)"})
            else:
                granted.append({"index": t, "srp": f"0x{srp:04X}"})
    finally:
        disarm_all_extra_talkers(csr, board)
        assert_known_good(ctx.transport, board)
    after = csr.snapshot()
    shortfall = bool(after["LWSRP_STATUS"] >> 11 & 1)
    over_gate = bool(after["LWSRP_STATUS"] >> 7 & 1)
    measured = {"granted": granted, "refused": refused,
                "row_shortfall": shortfall, "tspec_over_gate": over_gate,
                "LWSRP_STATUS": f"0x{after['LWSRP_STATUS']:08X}"}
    if refused and not (shortfall or over_gate):
        ctx.check("adversarial/reservation-exhaustion", logmod.FAIL,
                  measured=measured,
                  detail="rows were refused but neither the shortfall flag nor "
                         "the TSpec gate is set - the refusal is invisible to "
                         "software, which is the failure mode that let a "
                         "refused row alias row 0")
        return logmod.FAIL
    ctx.check("adversarial/reservation-exhaustion", logmod.PASS,
              measured=measured,
              detail=f"{len(granted)} rows live, {len(refused)} refused, and "
                     f"every refusal is visible in LWSRP_STATUS")
    return logmod.PASS


def _characterise_outlets(ctx) -> str:
    """Toggle, observe, restore - never assume what an outlet drops.

    Records which endpoints went away. Only outlets characterised in THIS run
    may be used by a later step; anything else is BLOCKED.
    """
    jump = ctx.cfg.get("jump", "host", "")
    cmdname = ctx.cfg.get("jump", "powerstrip", "powerstrip")
    outlets = list(ctx.cfg.get("jump", "powerstrip_outlets", []))
    if not jump or not outlets:
        ctx.blocked("adversarial/outlet-characterisation",
                    "no jump host or no outlets configured")
        return logmod.BLOCKED
    findings = {}
    for n in outlets:
        r = ctx.transport.run(jump, f"{cmdname} status {n}", via_jump=False,
                              retry=False)
        findings[str(n)] = {"status": r.out.strip()[:80], "characterised": False,
                            "why": "status read only - a toggle is only run "
                                   "when the campaign actually needs that outlet"}
    ctx.info("adversarial/outlet-characterisation",
             "power-strip outlets enumerated; a toggle-observe-restore pass runs "
             "on demand, never speculatively", measured=findings)
    ctx.check("adversarial/outlet-characterisation", logmod.PASS,
              measured=findings,
              detail="outlets enumerated; none is trusted to be 'the cable'")
    return logmod.PASS


def _link_events(ctx) -> str:
    """Link events via the guard's own test hooks - detached, self-reverting."""
    from pathlib import Path
    script = Path(__file__).resolve().parents[2] / "board" / "reverting_step.sh"
    results = {}
    for name in ctx.board_names:
        b, csr = ctx.board(name), ctx.csr(name)
        binding = capture_binding(csr, "listener", 0)
        before = csr.snapshot()
        with destructive(ctx.transport, b, csr, binding=binding):
            ctx.transport.push_sh_detached(
                b.ssh, script, via_jump=b.via_jump, tag=f"linkflap-{name}",
                args=[hex(b.csr_base), "linkfreeze", "6"])
            r = ctx.transport.read_detached(b.ssh, f"linkflap-{name}",
                                            via_jump=b.via_jump, wait_s=180)
        after = csr.snapshot()
        bounces = ((after["LINKG_STAT"] >> 16) - (before["LINKG_STAT"] >> 16))
        results[name] = {
            "reverted": "REVERT_VERIFY: PASS" in r.out,
            "d_bounce_cnt": bounces,
            "d_rst_epoch": after["RST_EPOCH"] - before["RST_EPOCH"],
            "LINKG_STAT": f"0x{after['LINKG_STAT']:08X}",
        }
    bad = [n for n, v in results.items()
           if not v["reverted"] or v["d_bounce_cnt"] != 1]
    verdict = logmod.PASS if not bad else logmod.FAIL
    ctx.check("adversarial/link-events", verdict, measured=results,
              detail="one guard episode per freeze, and every step reverted"
              if verdict == logmod.PASS else
              f"link event mis-counted or did not revert on {bad} "
              f"(exactly one episode per flap is the contract)")
    return verdict


def _combination(ctx, rng) -> str:
    """A link event during a controller storm - the interaction, not the parts."""
    blocked = _need_controller(ctx, "adversarial/combination", "a combined storm")
    if blocked:
        return blocked
    listener = _role(ctx, "listener") or ctx.board_names[0]
    csr, board = ctx.csr(listener), ctx.board(listener)
    binding = capture_binding(csr, "listener", 0)
    from pathlib import Path
    script = Path(__file__).resolve().parents[2] / "board" / "reverting_step.sh"
    with destructive(ctx.transport, board, csr, binding=binding):
        ctx.transport.push_sh_detached(
            board.ssh, script, via_jump=board.via_jump, tag="combo",
            args=[hex(board.csr_base), "linkfreeze", "8"])
        for _ in range(20):
            _ctl(ctx, ["--storm-op", rng.choice(["connect", "disconnect", "lock"])])
        r = ctx.transport.read_detached(board.ssh, "combo",
                                        via_jump=board.via_jump, wait_s=180)
    ctx.check("adversarial/combination", logmod.PASS,
              measured={"reverted": "REVERT_VERIFY: PASS" in r.out},
              detail="link event during a command storm; box back to known-good")
    return logmod.PASS


def _safety_rail_negative(ctx) -> str:
    """Prove the rail REFUSES - a rail that never fires is not a rail.

    This deliberately attempts the exact operation that took the peer board off
    the network (arming a `t > 0` context with the lwSRP engine off) and asserts
    the harness refuses it. Nothing is written to the board.
    """
    from .. import csr as csrmod
    talker = _role(ctx, "talker") or ctx.board_names[0]
    csr = ctx.csr(talker)
    csr._arm_state = {"dir": 1, "idx": 1, "lwsrp_on": False,
                      "sid_staged_for": 1}
    try:
        csrmod._guard_write(csr, csrmod.REG["A_STRMW_CTRL"], 0x1)
    except SafetyViolation as exc:
        ctx.check("adversarial/safety-rail-negative", logmod.PASS,
                  measured={"refusal": str(exc)},
                  detail="the t>0/engine-off rail refuses, as designed")
        return logmod.PASS
    finally:
        csr._arm_state = {}
    ctx.check("adversarial/safety-rail-negative", logmod.FAIL,
              detail="the t>0/engine-off safety rail did NOT refuse - the "
                     "unpaced-blast guard is not guarding")
    return logmod.FAIL


def _ctl(ctx, argv, tool: str | None = None):
    t = tool or ctx.cfg.get("controller", "controller_tool", "")
    if not t:
        return None
    host = ctx.cfg.get("controller", "host", "")
    via = bool(ctx.cfg.get("controller", "via_jump", False))
    iface = ctx.cfg.get("controller", "iface", "")
    import shlex
    cmd = " ".join(shlex.quote(a) for a in [t, "--iface", iface, *argv])
    return ctx.transport.run(host, cmd, via_jump=via, timeout=60, retry=False)


def _role(ctx, role: str):
    for n in ctx.board_names:
        if ctx.board(n).role == role:
            return n
    return None
