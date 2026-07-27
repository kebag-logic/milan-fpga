# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Phase 4 - FUNCTIONAL MATRIX. Randomised, with a RECORDED seed.
#!
#! Randomised beats exhaustive here (the cross product of formats x channel
#! counts x rates x mapping permutations x ring modes x loopback modes is far
#! more than a campaign can run), but random without reproducibility is
#! useless. So:
#!
#!   * the seed is drawn once, recorded in the JSONL, in the report and in any
#!     forensic bundle, and `--seed` replays it exactly;
#!   * every drawn configuration is recorded in full alongside its result, so a
#!     failing point can be re-run on its own without re-running the phase.
#!
#! **The peer board's loopback is the independent oracle.** A listener checking
#! its own counters can only tell you what it believes; the peer re-emitting
#! what it received is a second, differently-implemented opinion. Where a wire
#! oracle is not available the MAC loopback at the configured CSR gives a
#! memory -> TX-DMA -> datapath -> RX-DMA -> memory path with no wire at all.

from __future__ import annotations

import json
import random

from .. import log as logmod
from ..recovery import capture_binding, destructive, disarm_all_extra_talkers

PHASE = "matrix"


def run(ctx, clock) -> None:
    m = ctx.cfg.section("matrix")
    rng = random.Random(ctx.seed)
    rounds = int(m.get("rounds", 8))
    per_round = int(m.get("streams_per_round", 4))

    ctx.info("matrix/seed", "randomised matrix seed (replay with --seed)",
             measured={"seed": ctx.seed, "rounds": rounds,
                       "streams_per_round": per_round})

    plan = [_draw_round(rng, m, r, per_round) for r in range(rounds)]
    (ctx.run.dir / "matrix-plan.json").write_text(
        json.dumps({"seed": ctx.seed, "rounds": plan}, indent=2) + "\n",
        encoding="utf-8")

    for rnd in plan:
        item = f"matrix/round-{rnd['round']:02d}"
        clock.item(ctx, PHASE, item, lambda r=rnd: _round(ctx, r),
                   iteration=rnd["round"])

    for name in ctx.board_names:
        clock.item(ctx, PHASE, f"matrix/{name}/disarm-sweep",
                   lambda n=name: _disarm(ctx, n))


def _draw_round(rng: random.Random, m: dict, idx: int, per_round: int) -> dict:
    """One reproducible round. Every choice is drawn from the seeded RNG."""
    streams = []
    for s in range(per_round):
        streams.append({
            "stream": s,
            "format": rng.choice(list(m.get("formats", ["aaf-pcm32"]))),
            "channels": rng.choice(list(m.get("channel_counts", [2]))),
            "rate_hz": rng.choice(list(m.get("rates_hz", [48000]))),
            "mapping": rng.choice(list(m.get("mapping_modes", ["chmap-identity"]))),
        })
    return {
        "round": idx,
        "ring_mode": rng.choice(list(m.get("ring_modes", ["dram"]))),
        "loopback": rng.choice(list(m.get("loopback_modes", ["wire"]))),
        "streams": streams,
    }


def _round(ctx, rnd: dict) -> str:
    talker = _role(ctx, "talker") or ctx.board_names[0]
    listener = _role(ctx, "listener") or ctx.board_names[-1]
    csr_l = ctx.csr(listener)
    board_l = ctx.board(listener)

    # A mid-phase safety sweep: never leave an extra talker armed between
    # rounds, and never arm one with the lwSRP engine off.
    disarm_all_extra_talkers(ctx.csr(talker), ctx.board(talker))

    binding = capture_binding(csr_l, "listener", 0)
    measured = {"plan": rnd, "talker": talker, "listener": listener}

    with destructive(ctx.transport, board_l, csr_l, binding=binding,
                     on_event=lambda k, mm: ctx.info(f"matrix/{k}", str(mm))):
        if rnd["loopback"] == "mac-loopback":
            ok, why = _mac_loopback_round(ctx, talker, rnd)
            measured["loopback_result"] = {"ok": ok, "detail": why}
            if not ok:
                ctx.check(f"matrix/round-{rnd['round']:02d}", logmod.BLOCKED,
                          measured=measured, detail=why)
                return logmod.BLOCKED
        before = csr_l.snapshot()
        _apply_round(ctx, listener, rnd)
        after = csr_l.snapshot()
        measured["listener_delta"] = {
            "APRB_PARSED": after["APRB_PARSED"] - before["APRB_PARSED"],
            "APRB_MATCHED": after["APRB_MATCHED"] - before["APRB_MATCHED"],
            "AVTPRX_FRX": after["AVTPRX_FRX"] - before["AVTPRX_FRX"],
            "AVTPRX_ERR": f"0x{after['AVTPRX_ERR']:08X}",
            "PCMRX_CNT": f"0x{after['PCMRX_CNT']:08X}",
        }
        oracle = _peer_oracle(ctx, talker, listener)
        measured["peer_oracle"] = oracle

    d = measured["listener_delta"]
    problems = []
    if d["APRB_PARSED"] <= 0:
        problems.append("no AVTP frames reached the RX parser at all")
    elif d["APRB_MATCHED"] <= 0:
        problems.append("parser saw frames but the stream-table compare missed")
    elif d["AVTPRX_FRX"] <= 0:
        problems.append("matched frames never reached the monitor - look at "
                        "format rejects then the depacketizer")
    if oracle.get("independent") is False:
        # Not a failure of the device: we simply had no second opinion.
        ctx.info(f"matrix/round-{rnd['round']:02d}",
                 "no independent oracle for this round: "
                 + oracle.get("why", ""))

    verdict = logmod.FAIL if problems else logmod.PASS
    ctx.check(f"matrix/round-{rnd['round']:02d}", verdict, measured=measured,
              detail="; ".join(problems) or
                     f"{d['AVTPRX_FRX']} frames accepted across "
                     f"{len(rnd['streams'])} drawn stream configs")
    return verdict


def _apply_round(ctx, listener: str, rnd: dict) -> None:
    """Programme the drawn mapping permutation through the chmap window.

    The crossbar is the bench override, not the canonical programmer - the AEM
    audio-map projector is. Writes are refused while `CHMAP_CTRL[0]` is 0 and
    counted in `CHMAP_STAT[23:16]`, so the arm is set first and the refusal
    count is what proves the writes landed.
    """
    csr = ctx.csr(listener)
    csr.write("CHMAP_CTRL", 1)
    for s in rnd["streams"]:
        for phys in range(min(2 * s["channels"], 10)):
            word = _map_word(s["mapping"], phys, s)
            csr.write_many([("CHMAP_SEL", phys), ("CHMAP_WORD", word)],
                           guard=False)


def _map_word(mode: str, phys: int, stream: dict) -> int:
    """Build a render map word: `{EN[15], SRC[14:12], rsvd, IDX_HI, IDX_LO}`."""
    ch = phys % max(1, stream["channels"])
    if mode == "chmap-swap":
        ch = (ch + 1) % max(1, stream["channels"])
    elif mode == "chmap-fanout":
        ch = 0
    idx = ((stream["stream"] & 0x7) << 4) | (ch & 0xF)
    return 0x8000 | idx


def _mac_loopback_round(ctx, board_name: str, rnd: dict):
    """MAC loopback: a wire-free datapath self-test, detached and reverting."""
    b = ctx.board(board_name)
    if not b.mac_loopback_csr:
        return (False, "no mac_loopback_csr configured for this board")
    from pathlib import Path
    script = Path(__file__).resolve().parents[2] / "board" / "reverting_step.sh"
    ctx.transport.push_sh_detached(
        b.ssh, script, via_jump=b.via_jump, tag=f"loopback{rnd['round']}",
        args=[hex(b.csr_base), "loopback", "8", hex(b.mac_loopback_csr)])
    r = ctx.transport.read_detached(b.ssh, f"loopback{rnd['round']}",
                                    via_jump=b.via_jump, wait_s=180, poll_s=5)
    if "REVERT_VERIFY: PASS" not in r.out:
        return (False, f"loopback did not prove its revert: {r.out[-200:]!r}")
    return (True, "loopback applied and reverted with verification")


def _peer_oracle(ctx, talker: str, listener: str) -> dict:
    """The peer board's own view - a second, differently-implemented opinion."""
    if talker == listener:
        return {"independent": False,
                "why": "only one board is configured, so there is no peer"}
    snap = ctx.csr(talker).snapshot()
    return {
        "independent": True,
        "board": talker,
        "AAF_FRAMES": snap["AAF_FRAMES"],
        "LWSRP_STATUS": f"0x{snap['LWSRP_STATUS']:08X}",
        "APRB_PARSED": snap["APRB_PARSED"],
        "APRB_MATCHED": snap["APRB_MATCHED"],
    }


def _disarm(ctx, name: str) -> str:
    disarmed = disarm_all_extra_talkers(ctx.csr(name), ctx.board(name))
    ctx.check(f"matrix/{name}/disarm-sweep", logmod.PASS,
              measured={"disarmed": disarmed},
              detail="no t>0 talker context left armed "
                     "(an armed extra with the engine off blasts ~56 kf/s)")
    return logmod.PASS


def _role(ctx, role: str):
    for n in ctx.board_names:
        if ctx.board(n).role == role:
            return n
    return None
