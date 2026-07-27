# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Phase 6 - QUALITY + LATENCY.
#!
#! Three separate claims, kept separate because they fail for different reasons:
#!
#!   1. **THD+N over all frames per configuration.** Coherent tone, un-windowed
#!      FFT (see `thdn.py` for why a window would manufacture the number).
#!   2. **E2E latency == pto at every pto tested.** Not on average - at every
#!      point, because a sweep that only works at one pto is a coincidence.
#!   3. **In-system latency < one sample (20.83 us at 48 kHz)**, where
#!      "in-system" EXCLUDES the ring-fill stage that implements the pto (USER
#!      decision): RX = MAC_RX->ACCEPT->DEPKT, TX = SOF->EOF->MAC_TX. Counting
#!      the excluded stage would be measuring the pto twice.

from __future__ import annotations

import base64
import time

from .. import latency as latmod
from .. import log as logmod
from ..thdn import ThdnError, analyse_capture, verdict as thdn_verdict

PHASE = "quality"


def run(ctx, clock) -> None:
    for name in ctx.board_names:
        clock.item(ctx, PHASE, f"quality/{name}/thdn",
                   lambda n=name: _thdn(ctx, n))
        clock.item(ctx, PHASE, f"quality/{name}/in-system-latency",
                   lambda n=name: _in_system(ctx, n))
    clock.item(ctx, PHASE, "quality/pto-sweep", lambda: _pto_sweep(ctx))


# --------------------------------------------------------------------------
def _thdn(ctx, name: str) -> str:
    from pathlib import Path

    board = ctx.board(name)
    a = ctx.cfg.section("audio")
    rate = int(a.get("rate_hz", 48000))
    tone = int(a.get("tone_hz", 1000))
    secs = int(a.get("capture_secs", 10))
    accept = float(a.get("thdn_accept_dbfs", -120.0))
    chans = board.alsa_capture_channels

    script = Path(__file__).resolve().parents[2] / "board" / "capture_raw.sh"
    out = "/tmp/mh-thdn.raw"
    r = ctx.transport.push_sh(board.ssh, script, via_jump=board.via_jump,
                              timeout=secs + 120,
                              args=[board.alsa_capture_device, str(chans),
                                    str(rate), str(secs), out])
    if "#ERROR=no-arecord" in r.out:
        ctx.blocked(f"quality/{name}/thdn", "no arecord on the board")
        return logmod.BLOCKED
    if not r.ok:
        ctx.blocked(f"quality/{name}/thdn",
                    f"capture failed: {r.out.strip()[-200:]}")
        return logmod.BLOCKED

    raw = _fetch(ctx, board, out)
    if raw is None:
        ctx.blocked(f"quality/{name}/thdn", "could not retrieve the capture "
                    "(a board has no scp; the base64 pull failed)")
        return logmod.BLOCKED

    try:
        results = analyse_capture(raw, rate_hz=rate, f0_hz=tone, channels=chans)
    except ThdnError as exc:
        # A measurement that cannot be made is BLOCKED, not a distortion result.
        ctx.blocked(f"quality/{name}/thdn", f"analysis refused: {exc}")
        return logmod.BLOCKED
    except ImportError:
        ctx.blocked(f"quality/{name}/thdn",
                    "numpy is not importable - point [exec].python at a venv "
                    "that has it (harness/README.md)")
        return logmod.BLOCKED

    ok, why = thdn_verdict(results, accept)
    ctx.check(f"quality/{name}/thdn", logmod.PASS if ok else logmod.FAIL,
              measured={"channels": [r.as_dict() for r in results],
                        "accept_dbfs": accept,
                        "reference_dbfs": a.get("thdn_reference_dbfs"),
                        "window": "none (coherently sampled exact-period tone)"},
              detail=why)
    return logmod.PASS if ok else logmod.FAIL


def _fetch(ctx, board, path: str) -> bytes | None:
    """Pull a capture off a board that has no `scp`.

    base64 through the ssh channel is the supported path here; it is slow but it
    is the one that always exists.
    """
    r = ctx.transport.run(board.ssh, f"base64 < {path}", via_jump=board.via_jump,
                          timeout=600)
    if not r.ok:
        return None
    try:
        return base64.b64decode("".join(r.out.split()), validate=False)
    except (ValueError, TypeError):
        return None


# --------------------------------------------------------------------------
def _in_system(ctx, name: str) -> str:
    board, csr = ctx.board(name), ctx.csr(name)
    budget = float(ctx.cfg.get("latency", "in_system_budget_us", 20.83))

    # Clear the tap stats first: a saturated max from an earlier blocked period
    # is not a latency result, and only min/last survive it.
    csr.write("LTAP_CTRL", 0x3)
    if not ctx.dry_run:
        time.sleep(5)
    snap = csr.snapshot()

    measured, problems, untrusted = {}, [], []
    for d in ("rx", "tx"):
        chain = latmod.decode(snap, d)
        ins = latmod.in_system(chain, board, budget)
        measured[d] = {"chain": chain.as_dict(), "in_system": ins.as_dict()}
        if not ins.trustworthy:
            untrusted.append(d)
        if not ins.within_budget:
            worst = ins.max_us if ins.trustworthy else ins.last_us
            problems.append(f"{d} in-system {worst:.2f} us > {budget:.2f} us "
                            f"budget over {' + '.join(ins.stages)}")
    measured["excluded"] = {d: latmod.EXCLUDED[d][1] for d in ("rx", "tx")}

    if problems:
        ctx.check(f"quality/{name}/in-system-latency", logmod.FAIL,
                  measured=measured, detail="; ".join(problems))
        return logmod.FAIL
    detail = (f"in-system latency within one sample ({budget:.2f} us) on both "
              f"directions, excluding the pto-implementing stage")
    if untrusted:
        detail += (f" - NOTE {untrusted} chain(s) had timeouts/saturation, so "
                   f"the claim rests on last, not max")
    ctx.check(f"quality/{name}/in-system-latency", logmod.PASS,
              measured=measured, detail=detail)
    return logmod.PASS


# --------------------------------------------------------------------------
def _pto_sweep(ctx) -> str:
    """E2E latency == pto, at EVERY pto tested."""
    lat = ctx.cfg.section("latency")
    ptos = [float(p) for p in lat.get("pto_sweep_us", [])]
    tol = float(lat.get("pto_tolerance_us", 25.0))
    if not ctx.cfg.get("controller", "controller_tool", ""):
        ctx.blocked("quality/pto-sweep",
                    "setting pto is a controller operation and "
                    "[controller].controller_tool is unset")
        return logmod.BLOCKED

    listener = _role(ctx, "listener") or ctx.board_names[0]
    board, csr = ctx.board(listener), ctx.csr(listener)
    points = []
    for pto in ptos:
        _set_pto(ctx, pto)
        if not ctx.dry_run:
            time.sleep(5)
        snap = csr.snapshot()
        chain = latmod.decode(snap, "rx")
        # E2E is the WHOLE RX chain, including the ring-fill stage - that stage
        # is exactly what implements the pto, which is why it is excluded from
        # the in-system figure and included here.
        total_cyc = sum(d.last_cyc for d in chain.deltas)
        points.append(latmod.PtoPoint(pto_us=pto,
                                      measured_us=board.cycles_to_us(total_cyc),
                                      tolerance_us=tol))
    ok, why = latmod.pto_sweep_verdict(points)
    ctx.check("quality/pto-sweep", logmod.PASS if ok else logmod.FAIL,
              measured={"points": [p.as_dict() for p in points],
                        "board": listener, "tolerance_us": tol},
              detail=why)
    return logmod.PASS if ok else logmod.FAIL


def _set_pto(ctx, pto_us: float):
    import shlex
    tool = ctx.cfg.get("controller", "controller_tool", "")
    host = ctx.cfg.get("controller", "host", "")
    via = bool(ctx.cfg.get("controller", "via_jump", False))
    iface = ctx.cfg.get("controller", "iface", "")
    cmd = " ".join(shlex.quote(a) for a in
                   [tool, "--iface", iface, "--set-pto", str(int(pto_us))])
    return ctx.transport.run(host, cmd, via_jump=via, timeout=60)


def _role(ctx, role: str):
    for n in ctx.board_names:
        if ctx.board(n).role == role:
            return n
    return None
