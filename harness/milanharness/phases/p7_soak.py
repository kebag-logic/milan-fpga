# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Phase 7 - SOAK. Long run, periodic assertions, three specific watches.
#!
#! A soak that only asks "is it still alive" learns nothing. The three things
#! this one watches are the ones that go wrong slowly and look fine until they
#! don't:
#!
#!   * **Counter saturation.** A saturating narrow view sitting at its ceiling
#!     is not a value, it is a ceiling - and before the widths were fixed a
#!     16-bit field counted DOWN again after a wrap, which made a degrading link
#!     look like a healing one. Every saturating view is checked against its
#!     full-width source in the `0x800` window.
#!   * **Ring lap.** The host lapping the reader shows up as overrun rails and a
#!     `rd_ptr` fast-forward, not as an error.
#!   * **Servo drift.** The applied trim wandering, or the servo dropping out of
#!     LOCKED into HOLDOVER/FAULT, is the media clock quietly giving up.
#!
#! Each interval is its own item, so a crash resumes at the next interval and
#! the campaign does not lose the soak.

from __future__ import annotations

import time

from .. import log as logmod
from ..csr import RMON_LANE0, WINDOW_CNT

PHASE = "soak"

SERVO_STATES = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED",
                5: "HOLDOVER", 6: "FAULT"}


def run(ctx, clock) -> None:
    s = ctx.cfg.section("soak")
    duration = float(s.get("duration_s", 43200))
    every = float(s.get("assert_every_s", 300))
    watch_sat = bool(s.get("saturation_watch", True))

    intervals = max(1, int(duration // every))
    ctx.info("soak/plan", "soak plan", measured={
        "duration_s": duration, "assert_every_s": every,
        "intervals": intervals, "saturation_watch": watch_sat})

    first = {n: ctx.csr(n).snapshot() for n in ctx.board_names}
    prev = dict(first)

    for i in range(intervals):
        if clock.expired:
            ctx.info("soak", f"phase budget reached after {i} interval(s) - "
                             f"the soak is resumable with --from soak")
            break
        item = f"soak/interval-{i:04d}"

        def one(k=i):
            nonlocal prev
            if not ctx.dry_run:
                time.sleep(every)
            now = {n: ctx.csr(n).snapshot() for n in ctx.board_names}
            verdict = _assert_interval(ctx, item, first, prev, now, watch_sat)
            prev = now
            return verdict

        clock.item(ctx, PHASE, item, one, iteration=i,
                   timeout=every + 300)


def _assert_interval(ctx, item, first, prev, now, watch_sat) -> str:
    findings, measured = [], {}
    for name, snap in now.items():
        p, f = prev[name], first[name]
        board = ctx.board(name)
        m = {
            "d_frames_rx": snap["AVTPRX_FRX"] - p["AVTPRX_FRX"],
            "d_frames_tx": snap["AAF_FRAMES"] - p["AAF_FRAMES"],
            "d_parsed": snap["APRB_PARSED"] - p["APRB_PARSED"],
            "d_matched": snap["APRB_MATCHED"] - p["APRB_MATCHED"],
            "d_rst_epoch": snap["RST_EPOCH"] - f["RST_EPOCH"],
            "bounce_cnt": snap["LINKG_STAT"] >> 16,
        }

        # --- liveness --------------------------------------------------
        if m["d_parsed"] <= 0:
            findings.append(f"{name}: RX parser saw no AVTP frames this interval")
        if m["d_rst_epoch"] > (prev[name]["RST_EPOCH"] - f["RST_EPOCH"]):
            findings.append(f"{name}: datapath reset during the soak "
                            f"(RST_EPOCH advanced) - a CSR wipe is NOT the same "
                            f"as an unbind, and this says a real reset happened")

        # --- ring lap ---------------------------------------------------
        rails = snap["PBK_RAILS"]
        i2s = snap["I2SPB_STAT"]
        m["playback_overruns"] = rails & 0xFFFF
        m["playback_underruns"] = (rails >> 16) & 0xFFFF
        m["i2s_overruns"] = i2s & 0xFFFF
        m["i2s_underruns"] = (i2s >> 16) & 0xFFFF
        d_over = (rails & 0xFFFF) - (p["PBK_RAILS"] & 0xFFFF)
        if d_over > 0:
            findings.append(f"{name}: {d_over} ring overrun(s) this interval - "
                            f"the host lapped the reader")
        pcm_drops = (snap["PCMRX_CNT"] >> 16) - (p["PCMRX_CNT"] >> 16)
        m["d_pcm_drops"] = pcm_drops
        if pcm_drops > 0:
            findings.append(f"{name}: {pcm_drops} whole RX frame(s) dropped at "
                            f"the depacketizer FIFO")

        # --- servo drift -------------------------------------------------
        st = snap["MCSRV_STAT"]
        state = st & 0x7
        trim = _signed16(st >> 16)
        m["servo_state"] = SERVO_STATES.get(state, str(state))
        m["servo_trim_ppm_16ths"] = trim
        prev_trim = _signed16(p["MCSRV_STAT"] >> 16)
        m["d_servo_trim"] = trim - prev_trim
        if state in (5, 6):
            findings.append(f"{name}: media-clock servo is in "
                            f"{SERVO_STATES[state]} - the clock has given up")
        if st & (1 << 7):
            findings.append(f"{name}: servo PSDONE watchdog fault (sticky)")

        # --- counter saturation -----------------------------------------
        if watch_sat:
            sat = _saturation(ctx, name, snap)
            m["saturation"] = sat
            for s in sat.get("saturated", []):
                findings.append(f"{name}: {s} is at its ceiling - that is a "
                                f"ceiling, not a value; read the full-width "
                                f"word in the 0x800 window")
        measured[name] = m

    if findings:
        ctx.check(item, logmod.FAIL, measured=measured, detail="; ".join(findings))
        return logmod.FAIL
    ctx.check(item, logmod.PASS, measured=measured,
              detail="soak interval clean: streams live, no ring lap, servo "
                     "holding, no counter at a ceiling")
    return logmod.PASS


def _saturation(ctx, name, snap) -> dict:
    """Compare the saturating narrow views with their full-width sources."""
    out = {"saturated": [], "narrow": {}, "full": {}}
    stat, err = snap["AVTPRX_STAT"], snap["AVTPRX_ERR"]
    narrow = {
        "MEDIA_LOCKED": (stat >> 8) & 0xFF,
        "MEDIA_UNLOCKED": (stat >> 16) & 0xFF,
        "STREAM_INTERRUPTED": (stat >> 24) & 0xFF,
        "TIMESTAMP_UNCERTAIN": err & 0xFF,
        "UNSUPPORTED_FORMAT": (err >> 8) & 0xFF,
        "SEQ_NUM_MISMATCH": (err >> 16) & 0xFFFF,
    }
    out["narrow"] = narrow
    for key, val in narrow.items():
        ceiling = 0xFFFF if key == "SEQ_NUM_MISMATCH" else 0xFF
        if val >= ceiling:
            out["saturated"].append(key)
    try:
        w = ctx.csr(name).window("listener", 0)
        out["full"] = {k: w["cnt"].get(k) for k in WINDOW_CNT}
    except Exception as exc:                          # noqa: BLE001
        out["full_error"] = str(exc)
    return out


def _signed16(v: int) -> int:
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v
