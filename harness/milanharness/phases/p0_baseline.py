# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Phase 0 - BASELINE. Everything later is diffed against this.
#!
#! A baseline that perturbs what it measures is worthless, so this phase only
#! reads: no arm, no clear, no strobe (RMON's `STATS_CTRL` snapshot IS armed,
#! deliberately and separately, because an un-armed RMON window is stale by
#! definition and a stale baseline is worse than none).
#!
#! It also records the board-side flash-log probe, whose falsifier is
#! `cat /proc/mtd`: today it reports absent, the harness logs host-only, and
#! nothing depends on it.

from __future__ import annotations

import json
from pathlib import Path

from .. import latency as latmod
from .. import log as logmod
from ..csr import RMON_LANES, RMON_LANE0
from ..recovery import assert_known_good

BOARD_DIR = Path(__file__).resolve().parent.parent.parent / "board"
PHASE = "baseline"


def run(ctx, clock) -> None:
    for name in ctx.board_names:
        clock.item(ctx, PHASE, f"baseline/{name}/snapshot",
                   lambda n=name: _snapshot(ctx, n))
        clock.item(ctx, PHASE, f"baseline/{name}/known-good",
                   lambda n=name: _known_good(ctx, n))
        clock.item(ctx, PHASE, f"baseline/{name}/window",
                   lambda n=name: _windows(ctx, n))
        clock.item(ctx, PHASE, f"baseline/{name}/latency-taps",
                   lambda n=name: _taps(ctx, n))
        clock.item(ctx, PHASE, f"baseline/{name}/flashlog-probe",
                   lambda n=name: _flashlog(ctx, n))
    clock.item(ctx, PHASE, "baseline/controller", lambda: _controller(ctx))


def _baseline_path(ctx, board: str) -> Path:
    return ctx.run.dir / f"baseline-{board}.json"


def _snapshot(ctx, name: str) -> str:
    board, csr = ctx.board(name), ctx.csr(name)
    snap = csr.snapshot()
    named = snap.as_named()
    _baseline_path(ctx, name).write_text(
        json.dumps({"method": snap.method,
                    "registers": {k: v for k, v in sorted(named.items())}},
                   indent=2) + "\n", encoding="utf-8")

    # STATS_CAP is the register that turns "this lane reads 0" from a
    # non-answer into an answer: bit n = 0 means the lane has no source in this
    # build and a UI must render it "not supported", never "0 errors".
    cap = snap["STATS_CAP"]
    lanes = {RMON_LANES[n]: {"value": snap.get(RMON_LANE0 + 4 * n),
                             "supported": bool(cap >> n & 1)}
             for n in range(len(RMON_LANES))}
    ctx.info(f"baseline/{name}/rmon", "RMON lanes with their declared capability",
             measured={"stats_cap": f"0x{cap:03X}", "lanes": lanes})

    ctx.check(f"baseline/{name}/snapshot", logmod.PASS, measured={
        "read_method": snap.method,
        "registers": len(named),
        "VERSION": f"0x{snap['VERSION']:08X}",
        "AAF_CTRL": f"0x{snap['AAF_CTRL']:08X}",
        "ACMPL_STATE": f"0x{snap['ACMPL_STATE']:08X}",
        "LWSRP_STATUS": f"0x{snap['LWSRP_STATUS']:08X}",
        "LINKG_STAT": f"0x{snap['LINKG_STAT']:08X}",
        "APRB_PARSED": snap["APRB_PARSED"],
        "APRB_MATCHED": snap["APRB_MATCHED"],
    }, detail=f"{len(named)} registers via the {snap.method} path")
    return logmod.PASS


def _known_good(ctx, name: str) -> str:
    kg = assert_known_good(ctx.transport, ctx.board(name))
    ctx.check(f"baseline/{name}/known-good", logmod.PASS, measured=kg.checks,
              detail="all planes proven, including RX-parser movement")
    return logmod.PASS


def _windows(ctx, name: str) -> str:
    board, csr = ctx.board(name), ctx.csr(name)
    out = {}
    for direction, n in (("listener", board.n_listeners), ("talker", board.n_talkers)):
        for idx in range(n):
            w = csr.window(direction, idx)
            out[f"{direction}[{idx}]"] = {
                "ctrl": w["ctrl"], "state": w["state"], "fresh": w["fresh"],
                "sid": None if w["sid"] is None else f"0x{w['sid']:016X}",
                "srp": w["srp"], "not_backed": w["not_backed"],
                "cnt": w["cnt"],
            }
            if not w["fresh"]:
                # Reading 0 straight after a SEL is "not fresh yet", not "no
                # bind". Recorded as INFO so a later diff cannot mistake it.
                ctx.info(f"baseline/{name}/window",
                         f"{direction}[{idx}] snapshot block reads all-zero - "
                         f"not fresh, NOT proof of an empty context",
                         measured={"index": idx, "direction": direction})
    ctx.check(f"baseline/{name}/window", logmod.PASS, measured=out,
              detail=f"{len(out)} stream contexts snapshotted")
    return logmod.PASS


def _taps(ctx, name: str) -> str:
    board, csr = ctx.board(name), ctx.csr(name)
    snap = csr.snapshot()
    budget = float(ctx.cfg.get("latency", "in_system_budget_us", 20.83))
    measured = {}
    for d in ("tx", "rx"):
        chain = latmod.decode(snap, d)
        ins = latmod.in_system(chain, board, budget)
        measured[d] = {"chain": chain.as_dict(), "in_system": ins.as_dict()}
        if not chain.trustworthy:
            ctx.info(f"baseline/{name}/latency-taps",
                     f"{d} tap chain is not trustworthy yet "
                     f"(samples={chain.samples} timeouts={chain.timeouts}) - "
                     f"only min/last survive a timed-out period",
                     measured={"direction": d})
    ctx.check(f"baseline/{name}/latency-taps", logmod.PASS, measured=measured,
              detail="baseline latency envelope recorded (not yet judged)")
    return logmod.PASS


def _flashlog(ctx, name: str) -> str:
    board = ctx.board(name)
    r = ctx.transport.push_sh(board.ssh, BOARD_DIR / "flashlog.sh",
                              via_jump=board.via_jump,
                              args=[board.user_mtd_mount or "/user",
                                    ctx.run.rid, "baseline probe"])
    present = "#PROC_MTD_PRESENT=1" in r.out
    written = "#FLASHLOG=written" in r.out
    ctx.info(f"baseline/{name}/flashlog-probe",
             "board-side durable log probe (falsifier: cat /proc/mtd)",
             measured={"proc_mtd_present": present, "wrote": written,
                       "raw": r.out.strip()})
    if not written:
        # Expected today: no deployed tree carries an mtd node. Host-only
        # logging is the primary record anyway; this must never fail a run.
        ctx.info(f"baseline/{name}/flashlog-probe",
                 "board-side flash logging unavailable - host-only logging, "
                 "which is the primary record regardless")
    return logmod.PASS


def _controller(ctx) -> str:
    tool = ctx.cfg.get("controller", "controller_tool", "")
    if not tool:
        ctx.blocked("baseline/controller",
                    "[controller].controller_tool is unset - every "
                    "controller-driven item will report BLOCKED, not FAILED")
        return logmod.BLOCKED
    host = ctx.cfg.get("controller", "host", "")
    via = bool(ctx.cfg.get("controller", "via_jump", False))
    r = ctx.transport.run(host, f"test -x {tool} && echo OK", via_jump=via,
                          retry=False)
    if "OK" not in r.out:
        ctx.blocked("baseline/controller",
                    f"controller tool not executable on the controller host: {tool}")
        return logmod.BLOCKED
    ctx.check("baseline/controller", logmod.PASS,
              measured={"tool": tool, "iface": ctx.cfg.get("controller", "iface", "")},
              detail="controller host reachable and the tool is present")
    return logmod.PASS
