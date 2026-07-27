# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Phase 1 - FLASH + SMOKE. The post-flash contract, with explicit aborts.
#!
#! A new bitstream changes everything downstream, so this phase asserts the
#! contract before any measurement is allowed to mean anything:
#!
#!   1. **VERSION reads the expected word.** ABORT otherwise - every register
#!      semantic below depends on it, and running a campaign against the wrong
#!      gateware produces numbers that look fine and mean nothing.
#!   2. **Host plane up** (kernel rx_packets advancing, TS ring advancing).
#!   3. **chmap + slot 0 re-armed** - a flash wipes fabric state, and a silent
#!      empty render map is the "armed and genuinely silent" trap.
#!   4. **Peer re-bound** and *accepting* - proven by APRB/FRAMES movement, not
#!      by ACMP saying SUCCESS.
#!
#! ABORT CRITERIA are explicit and listed in `ABORTS`: hitting one stops the
#! phase immediately rather than letting seven more phases run against a board
#! that cannot produce a valid result.

from __future__ import annotations

import time
from pathlib import Path

from .. import log as logmod
from ..csr import ID_MAGIC
from ..recovery import assert_known_good

BOARD_DIR = Path(__file__).resolve().parent.parent.parent / "board"
PHASE = "smoke"

#: The conditions that stop the phase dead. Anything else is a normal FAIL.
ABORTS = (
    "csr plane silent (ID != MILN)",
    "VERSION != the campaign's expected word",
    "host plane dead (no kernel RX)",
)


class Abort(Exception):
    pass


def run(ctx, clock) -> None:
    aborted = []
    for name in ctx.board_names:
        def one(n=name):
            try:
                return _smoke(ctx, n)
            except Abort as exc:
                aborted.append(f"{n}: {exc}")
                ctx.check(f"smoke/{n}", logmod.FAIL, detail=f"ABORT: {exc}",
                          measured={"abort_criteria": list(ABORTS)})
                return logmod.FAIL
        clock.item(ctx, PHASE, f"smoke/{name}", one)
    if aborted:
        ctx.info("smoke", "post-flash contract aborted - later phases would "
                          "measure a board that cannot produce a valid result",
                 measured={"aborted": aborted})
        return
    clock.item(ctx, PHASE, "smoke/peer-binding", lambda: _peer_binding(ctx))


def _smoke(ctx, name: str) -> str:
    board, csr = ctx.board(name), ctx.csr(name)
    snap = csr.snapshot()

    if snap["ID"] != ID_MAGIC:
        raise Abort(f"ID reads 0x{snap['ID']:08X}, not 0x{ID_MAGIC:08X}")
    if snap["VERSION"] != board.version_expect:
        raise Abort(f"VERSION reads 0x{snap['VERSION']:08X}, campaign expects "
                    f"0x{board.version_expect:08X} - wrong gateware flashed")

    # Host plane: kernel RX and the TS ring must both advance. The TS ring is
    # the half that the CSR plane cannot see, and the one a stale device tree
    # silently breaks.
    r0 = _rx_packets(ctx, board)
    ts0 = csr.t.run(board.ssh, f"devmem {board.dma_ts_offset_csr} 32",
                    via_jump=board.via_jump).out.strip()
    time.sleep(6 if not ctx.dry_run else 0)
    r1 = _rx_packets(ctx, board)
    ts1 = csr.t.run(board.ssh, f"devmem {board.dma_ts_offset_csr} 32",
                    via_jump=board.via_jump).out.strip()
    if not (r1 > r0):
        raise Abort(f"kernel rx_packets stuck at {r0}")

    # chmap + slot 0. CHMAP_CTRL[0] selects the crossbar AND moves the DAC pace
    # onto the 48 kHz media grid; without it a host-ring playback can never
    # advance the DAC at all.
    chmap_armed = bool(snap["CHMAP_CTRL"] & 1)
    pbk = snap["PBK_STAT"]
    disarmed_render = pbk & 0xFFFF
    slot0_backed = bool((pbk >> 19) & 1)

    measured = {
        "VERSION": f"0x{snap['VERSION']:08X}",
        "rx_packets": [r0, r1], "ts_offset": [ts0, ts1],
        "CHMAP_CTRL": f"0x{snap['CHMAP_CTRL']:08X}",
        "CHMAP_STAT": f"0x{snap['CHMAP_STAT']:08X}",
        "PBK_STAT": f"0x{pbk:08X}",
        "chmap_armed": chmap_armed,
        "phys01_armed_in_render_map": slot0_backed,
        "disarmed_render_frames": disarmed_render,
        "AAF_CTRL": f"0x{snap['AAF_CTRL']:08X}",
    }

    problems = []
    if ts0 == ts1:
        problems.append("dma-ts ring offset did not advance (no TX timestamp "
                        "records reaching DRAM)")
    if not chmap_armed:
        problems.append("CHMAP_CTRL[0] = 0: the render crossbar is not selected, "
                        "so a host-ring playback cannot advance the DAC")
    if chmap_armed and not slot0_backed:
        problems.append("render map has no entry backing phys{0,1} - the line "
                        "out is silent because the map is empty, not the source")
    if disarmed_render:
        problems.append(f"{disarmed_render} disarmed-render frames already "
                        f"counted - frames reached the DAC with no map entry")
    if ((snap["AAF_CTRL"] >> 16) & 0xFFF) != 2:
        problems.append("AAF_CTRL VID field is not 2 - the stream would be "
                        "flooded unshaped by the bridge")

    assert_known_good(ctx.transport, board)

    if problems:
        ctx.check(f"smoke/{name}", logmod.FAIL, measured=measured,
                  detail="; ".join(problems))
        return logmod.FAIL
    ctx.check(f"smoke/{name}", logmod.PASS, measured=measured,
              detail="post-flash contract satisfied")
    return logmod.PASS


def _peer_binding(ctx) -> str:
    """The peer must be re-bound AND accepting - proven by movement.

    ACMP reporting SUCCESS and a listener reporting bound is exactly what the
    accept blocker looked like while the media plane was dead. So the assertion
    here is on the parser's own counters: PARSED climbing with MATCHED static is
    a distinct, diagnosable verdict, not a pass.
    """
    verdicts = {}
    for name in ctx.board_names:
        csr = ctx.csr(name)
        a = csr.snapshot()
        time.sleep(3 if not ctx.dry_run else 0)
        b = csr.snapshot()
        dp = b["APRB_PARSED"] - a["APRB_PARSED"]
        dm = b["APRB_MATCHED"] - a["APRB_MATCHED"]
        armed = (b["APRB_INFO"] >> 16) & 0xFF
        if dp <= 0:
            verdict = ("frames are not reaching the RX parser at all - look "
                       "upstream (MAC, filter, classify), not at the listener")
        elif dm <= 0:
            verdict = (f"parser sees frames but the compare misses "
                       f"(armed table entries: {armed}; wire sid "
                       f"0x{b['APRB_SID_HI']:08X}{b['APRB_SID_LO']:08X})")
        else:
            verdict = "match is live"
        verdicts[name] = {"d_parsed": dp, "d_matched": dm,
                          "armed_entries": armed, "verdict": verdict,
                          "ACMPL_STATE": f"0x{b['ACMPL_STATE']:08X}"}
    bad = [n for n, v in verdicts.items() if v["d_matched"] <= 0]
    if bad:
        ctx.check("smoke/peer-binding", logmod.FAIL, measured=verdicts,
                  detail=f"not accepting on {bad}")
        return logmod.FAIL
    ctx.check("smoke/peer-binding", logmod.PASS, measured=verdicts,
              detail="both boards parse AND match - the media plane is live")
    return logmod.PASS


def _rx_packets(ctx, board) -> int:
    r = ctx.transport.run(
        board.ssh, f"cat /sys/class/net/{board.netif}/statistics/rx_packets",
        via_jump=board.via_jump)
    try:
        return int(r.out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return -1
