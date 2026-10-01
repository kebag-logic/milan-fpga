#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe R429-2: the #629 AAF meter rules at head c554ae51.

Re-implements the rules stated in docs/design/MEDIA_CLOCK_FOLLOWING.md
(:442-459 pick and void, :489-496 bound, :533-536 history) and grades them
under error shapes the round-2 desk model (author-r2/meter_rules_model.py)
does not cover.

Rules modelled (all from the page):
  * one PDU per 125,000 ns; groups by sequence_num % 16;
  * pick = ts_0 + sum_i (ts_i - ts_0 - i*125,000) / 16 (P2), or ts_0 (P1);
  * VOID: a group whose any |ts_i - ts_0 - i*125,000| > B is voided and
    restarts the history (:457-459). The author's model omits this rule;
    the probe runs with and without it;
  * adjacent pick spacing outside 2 ms +/- B restarts the history;
  * rate valid after 256 fresh intervals; the servo samples once per 256
    picks (512 ms) and its lock test is |e| < 1,024 ns
    (KL_mmcm_drp_servo.sv:232, :648); one failing window drops LOCKED
    (:567-568, :689-694).
Lock-test columns:
  open : e = remote ring noise only (the author's assumption: the local
         clock follows exactly);
  pi   : a closed loop with the servo's gains (KI 1/2, KP 1/4,
         KL_mmcm_drp_servo.sv:227-228) on an ideal plant, e = local - remote.

Error shapes (peak J ns per PDU timestamp):
  white      independent uniform [-J, J] per PDU (the author's "independent")
  galt       +J/-J alternating per 16-PDU group (the author's "group")
  grand      one uniform [-J, J] draw per group, shared by its 16 PDUs
  gsign      one random +J/-J per group, shared by its 16 PDUs
  wanderT    J * sin(2 pi t / T): a slow phase wander of period T seconds

Standard library only, deterministic seed. Usage: python3 probe_meter_rules.py
"""
import math
import random

PDU_NS = 125_000
GROUP = 16
NOM_NS = PDU_NS * GROUP
RING = 256
LOCK_THR = 1_024
KI, KP = 0.5, 0.25


def err_fn(shape, jit, rng):
    cache = {}

    def f(n):
        g = n // GROUP
        if shape == "white":
            return rng.uniform(-jit, jit)
        if shape == "galt":
            return jit if g % 2 == 0 else -jit
        if shape in ("grand", "gsign"):
            if g not in cache:
                cache.clear()
                cache[g] = (rng.uniform(-jit, jit) if shape == "grand"
                            else rng.choice((-jit, jit)))
            return cache[g]
        if shape.startswith("wander"):
            per = float(shape[6:])
            return jit * math.sin(2 * math.pi * n * PDU_NS * 1e-9 / per)
        raise ValueError(shape)
    return f


def run(shape, jit, ppm, rule, bound, void, seconds, seed=629,
        step_at=None, step_ns=0.0):
    rng = random.Random(seed)
    ef = err_fn(shape, jit, rng)
    n_pdu = seconds * 8_000
    picks = []          # (pick or None for a voided group)
    base = 0.0
    acc = 0.0
    bad = False
    for n in range(n_pdu):
        ts = n * PDU_NS * (1 + ppm * 1e-6) + ef(n)
        if step_at is not None and n >= step_at:
            ts += step_ns
        i = n % GROUP
        if i == 0:
            base, acc, bad = ts, 0.0, False
        d = ts - base - i * PDU_NS
        if void and abs(d) > bound:
            bad = True
        acc += d
        if i == GROUP - 1:
            if bad:
                picks.append(None)
            else:
                picks.append(base if rule == "first" else base + acc / GROUP)
    step = NOM_NS * (1 + ppm * 1e-6)
    fresh = 0
    restarts = 0
    restart_groups = []
    valid = 0
    hist = []           # last-kept pick ring (index -> value)
    w_open, w_pi = [], []
    integ = 0.0
    corr = 0.0
    prev = None
    for k, p in enumerate(picks):
        if p is None:
            restarts += 1
            restart_groups.append(k)
            fresh = 0
            prev = None
            hist = []
            continue
        if prev is not None and abs(p - prev - NOM_NS) > bound:
            restarts += 1
            restart_groups.append(k)
            fresh = 0
            hist = [p]
        else:
            if prev is not None:
                fresh += 1
            hist.append(p)
            if len(hist) > RING + 1:
                hist.pop(0)
        prev = p
        ok = fresh >= RING
        valid += ok
        if k % RING == 0 and k > 0:
            if ok:
                remote = hist[-1] - hist[0] - RING * step
                w_open.append(abs(remote) < LOCK_THR)
                local = -corr
                e = local - remote
                w_pi.append(abs(e) < LOCK_THR)
                integ += KI * e
                corr = integ + KP * e
    n = len(picks) - 1
    fo = sum(w_open) / len(w_open) if w_open else 0.0
    fp = sum(w_pi) / len(w_pi) if w_pi else 0.0
    return valid / n, restarts / seconds, fo, fp, restart_groups


def main():
    secs = 120
    print("== A. lock test under 10.8-sized error, rules as the page states "
          "(B = 4,096 ns, VOID on), %d s per case" % secs)
    print("shape        J_ns  ppm  rule   void  rate_valid  restarts/s  "
          "win_open  win_pi")
    shapes = ("white", "galt", "grand", "gsign", "wander1.0", "wander2.0",
              "wander5.0", "wander20.0")
    for shape in shapes:
        for jit in (1042, 1426):
            for ppm in (0, 300):
                for rule in ("first", "mean"):
                    v, r, fo, fp, _ = run(shape, jit, ppm, rule, 4096, True,
                                          secs)
                    print(f"{shape:11s} {jit:5d} {ppm:4d}  {rule:5s}  on    "
                          f"{v:10.4f}  {r:10.2f}  {fo:8.3f}  {fp:6.3f}")
    print()
    print("== B. the page's +/-2,500 ns independent row: void off "
          "(the desk model) against void on (the page's rule :457-459)")
    for void in (False, True):
        for ppm in (0, 300):
            v, r, fo, fp, _ = run("white", 2500, ppm, "mean", 4096, void,
                                  secs)
            print(f"white  2500 {ppm:4d}  mean   {'on ' if void else 'off'}  "
                  f"  {v:10.4f}  {r:10.2f}  {fo:8.3f}  {fp:6.3f}")
    print()
    print("== C. in-group worst case at the design point: max over a group "
          "of |ts_i - ts_0 - i*125,000| for +/-1,426 ns and 300 ppm")
    worst = 2 * 1426 + 15 * PDU_NS * 300e-6
    print(f"analytic worst = 2*1426 + 15*125,000*300e-6 = {worst:.1f} ns "
          f"(bound 4,096: {'inside' if worst <= 4096 else 'OUTSIDE'})")
    print()
    print("== D. phase-step rejection: white +/-1,426 ns, 300 ppm, P2, "
          "B = 4,096 ns, void on; 64 step positions per size over one "
          "group + one PDU; caught = a history restart within 2 groups")
    for s in (1024, 2048, 3000, 4096, 6000, 10417, 20833, -20833):
        caught = 0
        trials = 64
        for t in range(trials):
            at = 8_000 * 3 + (t * 17) % (GROUP + 1)
            _, _, _, _, rg = run("white", 1426, 300, "mean", 4096, True, 4,
                                 seed=1000 + t, step_at=at, step_ns=s)
            g = at // GROUP
            if any(g - 1 <= x <= g + 2 for x in rg):
                caught += 1
        print(f"step {s:7d} ns: caught {caught:2d} of {trials}")


if __name__ == "__main__":
    main()
