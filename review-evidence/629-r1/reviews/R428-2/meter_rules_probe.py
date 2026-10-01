#!/usr/bin/env python3
"""Reviewer probe for the #629 AAF clock meter rules (PR #631, head c554ae51).

Implements the rules as the design page states them, including the two the
author's desk model omits:
  * a group is the 16 PDUs whose sequence_num % 16 runs 0..15 (8-bit wrap);
  * every PDU of the group is required (a sequence gap voids the group);
  * any |ts_i - ts_0 - i*125,000| above the bound B voids the group
    (design page :457-459);
  * pick = ts_0 + floor(sum_i (ts_i - ts_0 - i*125,000) / 16), integer ns
    modulo 2^32 (:450-456);
  * a voided group or an adjacent pick spacing outside 2 ms +/- B restarts
    the 256-entry history; the rate is valid after 256 fresh intervals
    (:533-536);
  * the servo samples the rate once per 512 ms (every 256 picks) and qualifies
    |rate error| < 1,024 ns; LOCKED needs 4 qualifying windows in a row
    (KL_mmcm_drp_servo.sv:232-233, :609, :648).
The local clock is assumed to follow the talker exactly, so the window error
is the remote ring noise pick[k] - pick[k-256] - 256 * nominal spacing.

Error shapes, peak J ns per PDU timestamp:
  white   independent uniform in [-J, J] per PDU
  galt    +J / -J alternating per 16-PDU group (the author's "group")
  grand   every PDU of a group shares one sign, chosen at random per group
  guni    every PDU of a group shares one value, uniform in [-J, J] per group
  sineP   J * sin(2 pi t / P), P in ms (slow wander)
Standard library only, deterministic seeds, at most 8 worker processes.
Usage: python3 meter_rules_probe.py [cases|steps|all]
"""
import math
import zlib
import random
import sys
from multiprocessing import Pool

PDU_NS = 125_000
GROUP = 16
NOM = PDU_NS * GROUP
RING = 256
THR = 1_024
M32 = 1 << 32


def s32(x):
    x &= M32 - 1
    return x - M32 if x >= 1 << 31 else x


def gen(shape, jit, ppm, seconds, seed, step_at=None, step_ns=0, seq0=0,
        ts0=0):
    rng = random.Random(seed)
    n_pdu = int(seconds * 8_000)
    gerr = 0.0
    for n in range(n_pdu):
        if n % GROUP == 0:
            if shape == "grand":
                gerr = jit if rng.random() < 0.5 else -jit
            elif shape == "guni":
                gerr = rng.uniform(-jit, jit)
        if shape == "white":
            e = rng.uniform(-jit, jit)
        elif shape == "galt":
            e = jit if (n // GROUP) % 2 == 0 else -jit
        elif shape in ("grand", "guni"):
            e = gerr
        elif shape.startswith("sine"):
            per_ns = float(shape[4:]) * 1e6
            e = jit * math.sin(2 * math.pi * n * PDU_NS / per_ns)
        else:
            e = 0.0
        if step_at is not None and n >= step_at:
            e += step_ns
        ts = int(round(ts0 + n * PDU_NS * (1 + ppm * 1e-6) + e)) % M32
        yield (seq0 + n) & 0xFF, ts


def meter(pdus, bound, use_void=True, use_mean=True, seq_mod_wrap=True):
    picks = []          # (pick, fresh_after)
    fresh = 0
    restarts = 0
    voids = 0
    last_pick = None
    grp = None          # list of ts in current group
    exp_seq = None
    for seq, ts in pdus:
        gap = exp_seq is not None and seq != exp_seq
        exp_seq = (seq + 1) & 0xFF if seq_mod_wrap else seq + 1
        pos = seq % GROUP
        if gap:
            grp = None
            voids += 1
            restarts += 1
            fresh = 0
            last_pick = None
        if pos == 0:
            grp = [ts]
        elif grp is not None and len(grp) == pos:
            grp.append(ts)
        else:
            grp = None
            continue
        if len(grp) < GROUP:
            continue
        g0 = grp[0]
        devs = [s32(t - g0 - i * PDU_NS) for i, t in enumerate(grp)]
        grp = None
        if use_void and max(abs(d) for d in devs) > bound:
            voids += 1
            restarts += 1
            fresh = 0
            last_pick = None
            picks.append((None, 0))
            continue
        if use_mean:
            pk = (g0 + (sum(devs) // GROUP)) % M32
        else:
            pk = g0
        if last_pick is not None:
            if abs(s32(pk - last_pick) - NOM) > bound:
                restarts += 1
                fresh = 0
            else:
                fresh += 1
        last_pick = pk
        picks.append((pk, fresh))
    return picks, restarts, voids


def grade(picks, ppm):
    step = NOM * (1 + ppm * 1e-6)
    n = len(picks)
    valid = sum(1 for p, f in picks if p is not None and f >= RING)
    windows = []
    for k in range(RING, n, RING):
        p, f = picks[k]
        if p is None or f < RING:
            windows.append(None)
            continue
        q = picks[k - RING][0]
        windows.append(abs(s32(p - q) - RING * step) < THR)
    good = [w for w in windows if w is not None]
    run = 0
    lock4 = 0
    for w in windows:
        run = run + 1 if w else 0
        lock4 += run >= 4
    nw = len(windows)
    return (valid / max(n - 1, 1), (sum(good) / len(good)) if good else 0.0,
            lock4 / nw if nw else 0.0, nw)


def case(args):
    shape, jit, ppm, bound, rule, void = args
    pdus = gen(shape, jit, ppm, 120, seed=zlib.crc32(f'{shape}/{jit}/{ppm}'.encode()),
               seq0=37, ts0=M32 - 3_000_000)
    pk, r, v = meter(pdus, bound, use_void=void, use_mean=(rule == "mean"))
    val, win, l4, nw = grade(pk, ppm)
    return (f"{shape:8s} {jit:5d} {ppm:4d} {rule:5s} {bound:5d} "
            f"void={'on ' if void else 'off'} valid={val:6.4f} "
            f"restarts={r:6d} voids={v:6d} win<2ppm={win:6.3f} "
            f"lock4={l4:6.3f} windows={nw}")


def cases():
    rows = []
    for shape in ("white", "galt", "grand", "guni", "sine10", "sine100",
                  "sine1000"):
        for jit in (1042, 1426, 2500):
            for ppm in (0, 300):
                for rule in ("first", "mean"):
                    for void in (True, False):
                        if rule == "first" and not void:
                            continue
                        rows.append((shape, jit, ppm, 4096, rule, void))
    with Pool(8) as pool:
        for line in pool.map(case, rows):
            print(line, flush=True)


def step_case(args):
    jit, step_ns, at, shape = args
    pdus = gen(shape, jit, 0, 4, seed=at, step_at=8_000 + at, step_ns=step_ns,
               seq0=200)
    pk, r, v = meter(pdus, 4096)
    # rate disturbance: largest window-rate error over all valid picks
    worst = 0
    for k in range(RING, len(pk)):
        p, f = pk[k]
        q = pk[k - RING][0]
        if p is None or q is None or f < RING:
            continue
        worst = max(worst, abs(s32(p - q) - RING * NOM))
    return (f"step {step_ns:6d} ns at group pos {at % 16:2d} shape {shape:5s} "
            f"J {jit:5d}: restarts={r} voids={v} worst_window_err_ns={worst}")


def steps():
    rows = []
    for step_ns in (20_833, -20_833, 10_417, 4_000, 3_000, 2_000):
        for at in range(16):
            rows.append((1426, step_ns, at, "white"))
    with Pool(8) as pool:
        for line in pool.map(step_case, rows):
            print(line, flush=True)
    # wrap check: 10 s continuous ideal stream, 312 sequence wraps
    pk, r, v = meter(gen("none", 0, 0, 10, 1, seq0=251, ts0=M32 - 1_000_000),
                     4096)
    print(f"wrap 10 s ideal: picks={len(pk)} restarts={r} voids={v} "
          f"valid_frac={grade(pk, 0)[0]:.4f}")
    # mutant: continuity checked without the 8-bit wrap
    pk, r, v = meter(gen("none", 0, 0, 10, 1, seq0=251, ts0=M32 - 1_000_000),
                     4096, seq_mod_wrap=False)
    print(f"wrap mutant (no 8-bit wrap): restarts={r} voids={v}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("cases", "all"):
        cases()
    if what in ("steps", "all"):
        steps()
