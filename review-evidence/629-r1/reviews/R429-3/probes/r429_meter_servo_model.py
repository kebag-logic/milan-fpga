#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent reviewer desk model (round R429-3) of the #629 AAF meter rules
as stated in docs/design/MEDIA_CLOCK_FOLLOWING.md at a463a1de, driving a model
of the KL_mmcm_drp_servo PI and lock rule (KL_mmcm_drp_servo.sv:228-233,
:538-579, :606-700). Written from the page and the RTL, not from the author's
model. Deterministic (fixed seeds). Usage: python3 r429_meter_servo_model.py

Meter rules modelled (page "The pick", "The jump bound", "The rate estimator",
"History, lock, era and outputs"):
  * groups of 16 PDUs by sequence_num mod 16; pick = ts_0 + floor(sum dev / 16),
    dev_i = ts_i - ts_0 - i*125000;
  * within-group void: any |dev_i| > 4096 voids the group -> history restart;
  * pick spacing outside 2 ms +/- 4096 ns -> history restart (the breaking
    pick seeds the new history);
  * a sequence gap voids the group (modelled by dropping PDUs);
  * E1: rate = P_h - P_{h-256} - 512e6, valid from h = 256, updated per pick;
  * E8: snapshot every 256 picks; rate = (S_j - S_{j-8} - 8*512e6) >> 3,
    valid from h = 2048, updated per snapshot; held between updates.
Servo modelled: e = clamp(locerr) - rate; integ += e>>>1; u = clamp(integ) +
e>>>2, clamp, slew limit 51200; lock_cnt on |e| < 1024; ACQUIRE->LOCKED at 4;
LOCKED->ACQUIRE when a run window resets lock_cnt; no PI when the rate is
invalid; VERIFY->ACQUIRE with a one-window skip; guard 2^19.
Plant: locerr_k = L0 - g * u_{k-1} + q_k, q_k uniform integer in [-20, 20].
"""
import math
import sys
import numpy as np

PDU_NS = 125_000
NOM_PICK = 2_000_000
BOUND = 4096
WIN_NS = 512_000_000
U_MAX = 102_400
SLEW = 51_200
LOCK_THR = 1024
GUARD = 1 << 19
ECLAMP = 1 << 20


# --------------------------------------------------------------------------
# Linear closed-loop analysis (no clamps): estimator error n_k -> e_k
# e_k = L0 - g*u_{k-1} - (r + n_k); u_k = I_{k-1} + 0.75 e_k; I_k = I_{k-1} + 0.5 e_k
# --------------------------------------------------------------------------
def impulse_S(g, n=400):
    """Impulse response of e to a unit estimator error n (linear, unquantised)."""
    e = np.zeros(n)
    integ = 0.0
    u_prev = 0.0
    for k in range(n):
        nk = 1.0 if k == 0 else 0.0
        ek = -g * u_prev - nk
        integ += 0.5 * ek
        u_prev = integ + 0.25 * ek
        e[k] = ek
    return e


def l1_two_point(g, N):
    """Worst |e| per unit J for a two-point estimator over N windows whose
    per-snapshot pick error is bounded by J: e = S * (eps_k - eps_{k-N}) / N."""
    s = impulse_S(g)
    h = np.zeros(len(s) + N)
    h[:len(s)] += s / N
    h[N:N + len(s)] -= s / N
    return np.abs(h).sum(), h


def stable(g):
    s = impulse_S(g, 2000)
    return abs(s[-50:]).max() < 1e-6


# --------------------------------------------------------------------------
# Error shapes: return err[n] (float ns) for PDU index n, time t = n*125 us
# --------------------------------------------------------------------------
def shape(name, J, npdu, rng, worst_h=None, snap_pdus=None, step=None):
    n = np.arange(npdu)
    t = n * PDU_NS * 1e-9
    grp = n // 16
    if name == "none":
        return np.zeros(npdu)
    if name == "indep":
        return rng.uniform(-J, J, npdu)
    if name == "alt_group":
        return np.where(grp % 2 == 0, J, -J).astype(float)
    if name == "rand_sign_group":
        s = rng.choice([-1.0, 1.0], grp[-1] + 1)
        return J * s[grp]
    if name == "uniform_group":
        s = rng.uniform(-1, 1, grp[-1] + 1)
        return J * s[grp]
    if name.startswith("sine_"):
        P = float(name.split("_")[1])
        return J * np.sin(2 * math.pi * t / P)
    if name.startswith("square_"):
        P = float(name.split("_")[1])
        return J * np.sign(np.sin(2 * math.pi * t / P + 1e-9))
    if name.startswith("tri_"):
        # triangle: ramp of 2J over P/2, then back (a ramp shape)
        P = float(name.split("_")[1])
        ph = (t / P) % 1.0
        return J * (4 * np.abs(ph - 0.5) - 1)
    if name.startswith("saw_"):
        # sawtooth: ramp of 2J over P, then a 2J jump back
        P = float(name.split("_")[1])
        ph = (t / P) % 1.0
        return J * (2 * ph - 1)
    if name == "rand_block512":
        nb = int(t[-1] / 0.512) + 2
        s = rng.choice([-1.0, 1.0], nb)
        return J * s[(t / 0.512).astype(int)]
    if name == "worst":
        # +/-J held per snapshot interval (256 picks = 4096 PDUs), signs from
        # the closed-loop impulse response h so that the error at a chosen
        # window adds up; repeated every len(h) blocks.
        blk = n // snap_pdus
        L = len(worst_h)
        sgn = np.sign(worst_h[::-1])
        sgn[sgn == 0] = 1
        return J * sgn[blk % L]
    raise ValueError(name)


# --------------------------------------------------------------------------
# Meter: groups -> picks -> history -> rate series (time-stamped)
# --------------------------------------------------------------------------
def meter(ts, seq_present, est):
    """ts: int64 timestamps for every PDU index (nan-free), seq_present: bool
    mask of PDUs received. Returns list of (t_avail_ns, rate, valid) events,
    restart count, and per-group void count."""
    ngrp = len(ts) // 16
    ts = ts[: ngrp * 16].reshape(ngrp, 16)
    pres = seq_present[: ngrp * 16].reshape(ngrp, 16)
    i = np.arange(16)
    dev = ts - ts[:, :1] - i * PDU_NS
    void = (~pres.all(axis=1)) | (np.abs(dev) > BOUND).any(axis=1)
    picks = ts[:, 0] + np.floor_divide(dev.sum(axis=1), 16)
    t_avail = ts[:, 15]
    events = []
    restarts = 0
    hist = []          # picks since last restart (E1) / count
    snaps = []         # E8 snapshots
    h = 0
    prev = None
    valid = False
    for gi in range(ngrp):
        if void[gi]:
            restarts += 1
            hist = []; snaps = []; h = 0; prev = None
            if valid:
                valid = False
                events.append((int(t_avail[gi]), 0, False))
            continue
        p = int(picks[gi])
        if prev is not None and abs(p - prev - NOM_PICK) > BOUND:
            restarts += 1
            hist = []; snaps = []; h = 0
            if valid:
                valid = False
                events.append((int(t_avail[gi]), 0, False))
        prev = p
        if est == "E1":
            hist.append(p)
            if len(hist) > 257:
                hist.pop(0)
            if h >= 256:
                rate = hist[-1] - hist[-257] - WIN_NS
                valid = True
                events.append((int(t_avail[gi]), rate, True))
        else:  # E8
            if h % 256 == 0:
                snaps.append(p)
                if len(snaps) > 9:
                    snaps.pop(0)
                if h >= 2048:
                    rate = (snaps[-1] - snaps[-9] - 8 * WIN_NS) >> 3
                    valid = True
                    events.append((int(t_avail[gi]), rate, True))
        h += 1
    return events, restarts, int(void.sum())


def rate_at(events, times):
    """Latest (rate, valid) at each servo boundary time."""
    out = []
    j = 0
    cur = (0, False)
    for tb in times:
        while j < len(events) and events[j][0] <= tb:
            cur = (events[j][1], events[j][2])
            j += 1
        out.append(cur)
    return out


def asr(x, s):
    return x >> s  # python >> on int is arithmetic (floor)


def clamp_u(v):
    return max(-U_MAX, min(U_MAX, v))


def servo(rate_samples, L0, g, rng, t_first_lock_idx=0):
    """Run the servo over len(rate_samples) windows. Returns metrics."""
    state = "ACQUIRE"
    skip = 1
    u = 0
    integ = 0
    lock_cnt = 0
    drops = 0
    first_locked = None
    es = []
    es_after = []
    for k, (rate, valid) in enumerate(rate_samples):
        q = int(rng.integers(-20, 21))
        locerr = int(round(L0 - g * u)) + q
        locerr = max(-ECLAMP, min(ECLAMP, locerr))
        run = (skip == 0) and valid and state != "HOLDOVER"
        if skip:
            skip -= 1
        if run:
            e = locerr - rate
            if abs(e) > GUARD:
                run = False
        if run:
            isum = integ + asr(e, 1)
            ig = clamp_u(isum)
            un = ig + asr(e, 2)
            ut = clamp_u(un)
            du = ut - u
            if du > SLEW:
                u = u + SLEW
            elif du < -SLEW:
                u = u - SLEW
            else:
                u = ut
            integ = ig
            if abs(e) < LOCK_THR:
                lock_cnt = min(4, lock_cnt + 1)
            else:
                lock_cnt = 0
            es.append(e)
            if first_locked is not None:
                es_after.append(e)
        if state == "ACQUIRE" and lock_cnt >= 4:
            state = "LOCKED"
            if first_locked is None:
                first_locked = k
        elif state == "LOCKED" and lock_cnt == 0:
            state = "ACQUIRE"
            drops += 1
    ea = np.array(es_after) if es_after else np.array([0])
    return dict(first_locked=first_locked, drops=drops,
                worst=int(np.abs(ea).max()) if es_after else None,
                frac=float((np.abs(ea) < LOCK_THR).mean()) if es_after else None,
                nrun=len(es))


def run_case(shape_name, J, est, *, delta_ppm=0.0, g=1.0, seconds=120.0,
             seed=1, phase_ms=1.0, need_ppm=30.64, drop_every=None,
             step_at=None, step_ns=0, worst_h=None):
    rng = np.random.default_rng(seed)
    npdu = int(seconds / (PDU_NS * 1e-9))
    npdu -= npdu % 16
    n = np.arange(npdu, dtype=np.int64)
    err = shape(shape_name, J, npdu, rng, worst_h=worst_h, snap_pdus=4096)
    if step_at is not None:
        err = err + np.where(n >= step_at, step_ns, 0)
    ideal = n * PDU_NS * (1.0 + delta_ppm * 1e-6)
    ts = np.round(ideal + err).astype(np.int64) + 1_000_000_000
    present = np.ones(npdu, dtype=bool)
    if drop_every is not None:
        present[drop_every::drop_every] = False
    ev, restarts, voids = meter(ts, present, est)
    # servo boundaries: open ~ meter lock (8 PDUs) + phase, every 512 ms
    t0 = int(ts[8]) + int(phase_ms * 1e6)
    nwin = int((ts[-1] - t0) // WIN_NS)
    times = [t0 + (k + 1) * WIN_NS for k in range(nwin)]
    rs = rate_at(ev, times)
    r_true = delta_ppm * 512.0
    L0 = r_true + need_ppm * 512.0
    m = servo(rs, L0, g, rng)
    m["restarts"] = restarts
    m["voids"] = voids
    m["valid_frac"] = float(np.mean([v for _, v in rs])) if rs else 0.0
    if m["first_locked"] is not None:
        m["t_lock_s"] = round((times[m["first_locked"]] - int(ts[0])) / 1e9, 2)
    else:
        m["t_lock_s"] = None
    return m


def fmt(m):
    if m["first_locked"] is None:
        return (f"never locks; restarts {m['restarts']}, voids {m['voids']}, "
                f"rate-valid windows {m['valid_frac']:.3f}")
    return (f"locked at {m['t_lock_s']} s; windows<1024 {m['frac']:.3f}; "
            f"worst |e| {m['worst']} ns; drops {m['drops']}; restarts "
            f"{m['restarts']}; voids {m['voids']}")


def main():
    print("== L. linear closed loop: worst |e| per unit J (l1), plant gain g")
    s1 = np.abs(impulse_S(1.0)).sum()
    print(f"||S||_1 at g=1.0 = {s1:.4f}")
    for g in (0.6, 0.8, 1.0, 1.2, 1.4, 1.6):
        a1, _ = l1_two_point(g, 1)
        a8, _ = l1_two_point(g, 8)
        print(f"g={g:.1f} stable={stable(g)} E1 {a1:.4f} (J=1042 {a1*1042:.0f}, J=1426 "
              f"{a1*1426:.0f})  E8 {a8:.4f} (J=1042 {a8*1042:.0f}, J=1426 {a8*1426:.0f})")
    # plant gain at which E8's worst case reaches the 1024 ns lock threshold
    for J in (1042, 1426):
        lo = None
        for gg in np.arange(1.0, 1.95, 0.01):
            if not stable(gg):
                break
            if l1_two_point(gg, 8)[0] * J >= LOCK_THR:
                lo = gg
                break
        print(f"E8 worst case reaches 1024 ns at J={J} for plant gain >= "
              f"{lo if lo is None else round(float(lo), 2)} (scan 1.00..1.94)")
    gmax = None
    for gg in np.arange(1.0, 4.0, 0.01):
        if not stable(gg):
            gmax = round(float(gg), 2)
            break
    print(f"linear loop loses stability at plant gain ~{gmax}")
    print("open-loop indistinguishability over 512 ms: J/T at J=1042 = "
          f"{1042/0.512/1000:.3f} ppm ({1042} ns/window); 2J/T = {2*1042/0.512/1000:.3f} ppm")

    _, h8 = l1_two_point(1.0, 8)
    _, h1 = l1_two_point(1.0, 1)
    # convert h (per-window impulse response to snapshot error) to sign
    # pattern over snapshot blocks; trim to a usable length
    h8w = h8[:64]
    h1w = h1[:64]

    shapes = ["indep", "alt_group", "rand_sign_group", "uniform_group",
              "sine_0.01", "square_0.01", "sine_1.0", "square_1.0",
              "square_2.0", "tri_1.024", "tri_8.192", "saw_0.512", "saw_4.096",
              "square_8.192", "rand_block512", "worst"]
    print()
    print("== T. time-domain, 120 s, talker +0 ppm vs gPTP, servo needs +30.64 ppm, g=1")
    for J in (1042, 1426):
        for sh in shapes:
            for est in ("E1", "E8"):
                wh = (h8w if est == "E8" else h1w) if sh == "worst" else None
                m = run_case(sh, J, est, worst_h=wh)
                print(f"J={J:5d} {sh:16s} {est}: {fmt(m)}")
    print()
    print("== T300. 120 s, talker at +300 ppm and -300 ppm vs gPTP (spacing rule), g=1")
    for J in (1426,):
        for d in (300.0, -300.0):
            for sh in ("indep", "rand_sign_group", "square_8.192", "worst"):
                m = run_case(sh, J, "E8", delta_ppm=d,
                             worst_h=h8w if sh == "worst" else None)
                print(f"J={J} delta={d:+.0f} {sh:16s} E8: {fmt(m)}")
    print()
    print("== P. E8 sensitivity: plant gain and servo-boundary phase, J=1426")
    for g in (0.8, 1.2, 1.4):
        _, hg = l1_two_point(g, 8)
        for sh in ("worst", "rand_sign_group", "square_8.192"):
            m = run_case(sh, 1426, "E8", g=g,
                         worst_h=hg[:64] if sh == "worst" else None)
            print(f"g={g} {sh:16s}: {fmt(m)}")
    for ph in (0.0, 100.0, 255.0, 400.0, 511.0):
        m = run_case("worst", 1426, "E8", phase_ms=ph, worst_h=h8w)
        print(f"phase {ph:5.0f} ms worst: {fmt(m)}")
    for seed in range(1, 6):
        m = run_case("rand_sign_group", 1426, "E8", seed=seed, seconds=300.0)
        print(f"seed {seed} rand_sign_group 300 s: {fmt(m)}")
    print()
    print("== V. void rule / tolerance (E8), first restarts by J")
    for d in (0.0, 300.0):
        for sh in ("rand_sign_group", "indep"):
            first = None
            for J in range(1700, 2101, 20):
                m = run_case(sh, J, "E8", delta_ppm=d, seconds=20.0)
                if m["restarts"] > 0:
                    first = J
                    break
            print(f"delta={d:+.0f} {sh:16s}: first restart at J={first} (20 ns steps)")
    m = run_case("indep", 2500, "E8", seconds=20.0)
    print(f"indep +/-2500 ns 20 s: {fmt(m)}")
    print()
    print("== S. a real step: one sample (20,833 ns) and half sample at each group position")
    for est in ("E1", "E8"):
        for size in (20833, -20833, 10417, -10417):
            caught = 0
            for pos in range(16):
                at = 16 * 15000 + pos   # mid-run
                rng = np.random.default_rng(7)
                m = run_case("indep", 1426, est, seconds=60.0, step_at=at,
                             step_ns=size, seed=7)
                if m["restarts"] >= 1:
                    caught += 1
            print(f"{est} step {size:+6d}: history restart at {caught}/16 positions")
    for est in ("E1", "E8"):
        for size in (2000, 3000, -3000, 3400):
            m = run_case("none", 0, est, seconds=60.0, step_at=16 * 15000 + 5,
                         step_ns=size)
            print(f"{est} sub-bound step {size:+d}: {fmt(m)}")
    print()
    print("== F. real talker frequency step (after lock), E1 vs E8, J=0")
    for est in ("E1", "E8"):
        for dppm in (2.0, 4.0, 6.0, 8.0, 9.0, 10.0):
            m = run_freq_step(est, dppm)
            print(f"{est} frequency step {dppm:4.1f} ppm: drops {m['drops']}, worst "
                  f"after lock {m['worst']} ns")
    print()
    print("== Loss. one lost PDU every K PDUs: rate-valid fraction and lock, E1 vs E8")
    for K in (4000, 8000, 16000, 24000, 40000):
        for est in ("E1", "E8"):
            m = run_case("indep", 1042, est, seconds=120.0, drop_every=K)
            print(f"loss 1/{K} ({K/8000:.1f} s) {est}: rate-valid windows "
                  f"{m['valid_frac']:.3f}; {fmt(m)}")
    print("Clean-run requirement: E1 needs 257 picks = 4,112 PDUs; E8 needs 2,049 "
          "picks = 32,784 PDUs.")
    for p in (1e-6, 1e-5, 1e-4):
        print(f"P(no loss in span) at PDU loss {p:g}: E1 {(1-p)**4112:.3f}, "
              f"E8 {(1-p)**32784:.3f}")


def run_freq_step(est, dppm, seconds=90.0):
    """Talker frequency step at 40 s (ideal timestamps)."""
    rng = np.random.default_rng(3)
    npdu = int(seconds / (PDU_NS * 1e-9))
    npdu -= npdu % 16
    n = np.arange(npdu, dtype=np.int64)
    n0 = int(40.0 / (PDU_NS * 1e-9))
    per = np.where(n < n0, PDU_NS * 1.0, PDU_NS * (1.0 + dppm * 1e-6))
    ideal = np.concatenate([[0.0], np.cumsum(per[:-1])])
    ts = np.round(ideal).astype(np.int64) + 1_000_000_000
    ev, restarts, voids = meter(ts, np.ones(npdu, bool), est)
    t0 = int(ts[8]) + 1_000_000
    nwin = int((ts[-1] - t0) // WIN_NS)
    times = [t0 + (k + 1) * WIN_NS for k in range(nwin)]
    rs = rate_at(ev, times)
    # local plant: L0 relative to the talker's pre-step rate; the talker's
    # rate moves, so the needed u moves by the step
    m = servo(rs, 30.64 * 512.0, 1.0, rng)
    return m


if __name__ == "__main__":
    sys.exit(main())
