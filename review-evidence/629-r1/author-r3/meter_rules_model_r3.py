#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Desk model of the AAF clock meter rules, #629 design round 3.

A model of the meter's stated rules and of the servo's lock test, under
assumed presentation-time error shapes. Not a model of any talker.

Meter rules (docs/design/MEDIA_CLOCK_FOLLOWING.md, round 2 text, all kept):
  * one PDU per 125,000 ns; groups of 16 by sequence_num % 16 (8-bit wrap);
  * every PDU of a group is required: a sequence gap voids the group;
  * VOID: a group with any |ts_i - ts_0 - i*125,000| above the bound B is
    voided (the rule the round-2 model omitted);
  * pick: P2 = ts_0 + floor(sum_i (ts_i - ts_0 - i*125,000) / 16), or
    P1 = ts_0; integer ns modulo 2^32;
  * a voided group, or an adjacent pick spacing outside 2 ms +/- B, restarts
    the history. B = 4,096 ns.

Rate estimators (the round-3 question):
  E1   two-point over 256 picks (512 ms), sliding: round 2's rule,
       KL_crf_rx's (KL_crf_rx.sv:523-526);
  E4   two-point over 4 x 256 picks (2,048 ms), snapshots every 256 picks,
       rate = (P_now - P_4_snapshots_ago - 4*NOM_WIN) >>> 2;
  E8   two-point over 8 x 256 picks (4,096 ms), snapshots every 256 picks,
       rate = (P_now - P_8_snapshots_ago - 8*NOM_WIN) >>> 3;
  LS1  least-squares slope over the last 257 picks (512 ms), scaled to ns
       per 512 ms (the alternative the round-3 assignment names).
Every estimator reports ns per 512 ms (KL_crf_rx rate_o units) and a valid
level: E1 and LS1 after 256 fresh intervals, E4 after 1,024, E8 after 2,048.

Servo (KL_mmcm_drp_servo.sv): samples the rate once per 512 ms window
(:609); runs PI only on a valid rate (:613-615); e = locerr - rate (:643);
integ += e >>> 1 (:228, :647); u = clamp(integ) + e >>> 2 (:229, :669),
clamped to +-102,400 and slewed by +-51,200 per window (:230-231, :681);
lock qualification |e| < 1,024 (:232, :648); LOCKED after 4 qualifying
windows (:233, :566), and one failing window drops LOCKED (:567, :689-694).
Two gradings:
  open   the local clock follows the talker exactly: e = rate - true rate
         (the round-2 model's assumption);
  closed the PI above on a plant of gain 1 with a one-window delay:
         locerr_k = true + D0 - u_{k-1} + q_k, D0 = 10.64 ppm (the MMCM
         plan's offset), q_k uniform +-20 ns (the local window's own
         quantisation). The window phase is offset from the meter's.

Error shapes (peak J ns per PDU timestamp; 10.8 Equation (15) bounds only
the magnitude):
  white   independent uniform [-J, J] per PDU
  galt    +J / -J alternating per 16-PDU group (round 2's "group")
  gsign   one random +J / -J per group, shared by its 16 PDUs
  guni    one uniform [-J, J] draw per group, shared by its 16 PDUs
  sineP   J sin(2 pi t / P), P in ms (10 ms is the reviews' periodic case)
  adv     the worst case for the estimator in closed loop: +-J held for
          each 512 ms snapshot block, the sign pattern taken from the
          loop's impulse response (for LS1, a +-J step at mid-block)

Standard library only, deterministic seeds, at most 8 worker processes.
Usage: python3 meter_rules_model_r3.py [gain|fstep|latency|wrap|tol|steps|shapes|all]
"""
import math
import random
import sys
import zlib
from collections import deque
from multiprocessing import Pool

PDU_NS = 125_000
GROUP = 16
NOM = PDU_NS * GROUP            # 2 ms pick spacing
RING = 256                      # picks per 512 ms window
NOM_WIN = RING * NOM            # 512,000,000 ns
WIN_PDU = RING * GROUP          # 4,096 PDUs per 512 ms window
THR = 1_024
B = 4_096
M32 = 1 << 32
U_MAX, SLEW = 102_400, 51_200
LOCK_WIN = 4
D0 = round(10.64 * 512)         # initial local frequency error, x512 units
QN = 20                         # local window quantisation, ns
PHASE_PDU = 1_234               # servo window phase against the stream


def s32(x):
    x &= M32 - 1
    return x - M32 if x >= 1 << 31 else x


# ---------------------------------------------------------------- the loop
def loop_impulse(n_est, taps=64, gain=1.0):
    """Impulse response from a per-window error E_k (held over the window,
    seen by an N-window two-point estimator) to the servo's window error e,
    for the linear PI (no shifts' truncation)."""
    out = []
    integ = u = 0.0
    hist = [0.0] * (n_est + 1)
    for k in range(taps):
        ek = 1.0 if k == 0 else 0.0
        hist = hist[1:] + [ek]
        n = (hist[-1] - hist[0]) / n_est      # estimator noise
        e = -gain * u - n
        integ += e / 2
        u = integ + e / 4
        out.append(e)
    return out


def sens_impulse(taps=200, gain=1.0):
    out = []
    integ = u = 0.0
    for k in range(taps):
        e = -gain * u - (1.0 if k == 0 else 0.0)
        integ += e / 2
        u = integ + e / 4
        out.append(e)
    return out


def adv_pattern(est, period=64):
    """Sign per 512 ms block so that block (period-1) of every period sees
    the worst closed-loop e for the estimator."""
    if est == "LS1":
        # LS1's estimate at window k sees block k-1's mid-block step only
        h = sens_impulse(taps=period)
        return [(1 if h[period - 2 - j] < 0 else -1) if j < period - 1
                else 1 for j in range(period)]
    n = {"E1": 1, "E4": 4, "E8": 8}[est]
    h = loop_impulse(n, taps=period)
    return [(1 if h[period - 1 - j] < 0 else -1) for j in range(period)]


# ---------------------------------------------------------------- stimulus
def gen(shape, jit, ppm, seconds, seed, est="E8", step_at=None, step_ns=0,
        seq0=0, ts0=0):
    rng = random.Random(seed)
    n_pdu = int(seconds * 8_000)
    gerr = 0.0
    pat = adv_pattern(est) if shape == "adv" else None
    for n in range(n_pdu):
        g = n // GROUP
        if n % GROUP == 0:
            if shape == "gsign":
                gerr = jit if rng.random() < 0.5 else -jit
            elif shape == "guni":
                gerr = rng.uniform(-jit, jit)
        if shape == "white":
            e = rng.uniform(-jit, jit)
        elif shape == "galt":
            e = jit if g % 2 == 0 else -jit
        elif shape in ("gsign", "guni"):
            e = gerr
        elif shape.startswith("sine"):
            per_ns = float(shape[4:]) * 1e6
            e = jit * math.sin(2 * math.pi * n * PDU_NS / per_ns)
        elif shape == "adv":
            blk, pos = divmod(g, RING)
            sgn = pat[blk % len(pat)]
            if est == "LS1":
                e = jit * sgn * (1 if pos >= RING // 2 else -1)
            else:
                e = jit * sgn
        else:
            e = 0.0
        if step_at is not None and n >= step_at:
            e += step_ns
        ts = int(round(ts0 + n * PDU_NS * (1 + ppm * 1e-6) + e)) % M32
        yield n, (seq0 + n) & 0xFF, ts


# ---------------------------------------------------------------- meter
class Meter:
    def __init__(self, est, pick, use_void=True, seq_wrap=True):
        self.est, self.pick = est, pick
        self.use_void, self.seq_wrap = use_void, seq_wrap
        self.nwin = {"E1": 1, "E4": 4, "E8": 8, "LS1": 1}[est]
        self.restarts = self.voids = 0
        self.rate, self.valid = 0, False
        self.exp_seq = None
        self.grp = None
        self._restart()

    def _restart(self):
        self.fresh = 0
        self.last = None
        self.hist = deque(maxlen=RING + 1)     # E1 / LS1 picks
        self.snaps = deque(maxlen=self.nwin + 1)
        self.valid = False

    def _break(self):
        self.restarts += 1
        self._restart()

    def pdu(self, seq, ts):
        if self.exp_seq is not None and seq != self.exp_seq:
            self.grp = None
            self.voids += 1
            self._break()
        self.exp_seq = (seq + 1) & 0xFF if self.seq_wrap else seq + 1
        pos = seq % GROUP
        if pos == 0:
            self.grp = [ts]
        elif self.grp is not None and len(self.grp) == pos:
            self.grp.append(ts)
        else:
            self.grp = None
            return
        if len(self.grp) < GROUP:
            return
        g0 = self.grp[0]
        devs = [s32(t - g0 - i * PDU_NS) for i, t in enumerate(self.grp)]
        self.grp = None
        if self.use_void and max(abs(d) for d in devs) > B:
            self.voids += 1
            self._break()
            return
        pk = (g0 + sum(devs) // GROUP) % M32 if self.pick == "P2" else g0
        if self.last is not None:
            if abs(s32(pk - self.last) - NOM) > B:
                self._break()
            else:
                self.fresh += 1
        self.last = pk
        self._estimate(pk)

    def _estimate(self, pk):
        f = self.fresh
        if self.est == "E1":
            self.hist.append(pk)
            if f >= RING:
                self.rate = s32(pk - self.hist[0] - NOM_WIN)
                self.valid = True
        elif self.est == "LS1":
            self.hist.append(pk)
            if f >= RING and f % RING == 0:
                base = self.hist[0]
                ys = [s32(p - base) for p in self.hist]
                n = len(ys)
                xm = (n - 1) / 2
                ym = sum(ys) / n
                sxy = sum((i - xm) * (y - ym) for i, y in enumerate(ys))
                sxx = sum((i - xm) ** 2 for i in range(n))
                self.rate = int(round(sxy / sxx * RING - NOM_WIN))
                self.valid = True
        else:
            if f % RING == 0:
                self.snaps.append(pk)
                if len(self.snaps) == self.nwin + 1:
                    d = s32(self.snaps[-1] - self.snaps[0]
                            - self.nwin * NOM_WIN)
                    self.rate = d >> int(math.log2(self.nwin))
                    self.valid = True


# ---------------------------------------------------------------- servo
def shr(x, s):
    return x >> s          # Python >> floors, as SystemVerilog >>> does


class Servo:
    def __init__(self, true_rate, rng):
        self.true = true_rate
        self.rng = rng
        self.integ = self.u = 0
        self.lock_cnt = 0
        self.locked = False
        self.first_lock = None
        self.drops = 0
        self.ok = self.runs = 0
        self.emax = 0

    def window(self, k, rate, valid):
        if not valid:
            return
        loc = self.true + D0 - self.u + self.rng.randint(-QN, QN)
        e = loc - rate
        isum = self.integ + shr(e, 1)
        ig = max(-U_MAX, min(U_MAX, isum))
        un = ig + shr(e, 2)
        ut = max(-U_MAX, min(U_MAX, un))
        du = ut - self.u
        self.u = self.u + max(-SLEW, min(SLEW, du))
        self.integ = ig
        good = -THR < e < THR
        self.lock_cnt = min(LOCK_WIN, self.lock_cnt + 1) if good else 0
        if self.first_lock is not None:
            self.runs += 1
            self.ok += good
            self.emax = max(self.emax, abs(e))
        if not self.locked and self.lock_cnt >= LOCK_WIN:
            self.locked = True
            if self.first_lock is None:
                self.first_lock = k
        elif self.locked and self.lock_cnt == 0:
            self.locked = False
            self.drops += 1


def run(shape, jit, ppm, est, pick, seconds=120, seed=None, step_at=None,
        step_ns=0, use_void=True, seq0=0, ts0=0):
    if seed is None:
        seed = zlib.crc32(f"{shape}/{jit}/{ppm}".encode())
    m = Meter(est, pick, use_void)
    true = int(round(ppm * 512))
    sv = Servo(true, random.Random(seed ^ 0x5A5A))
    open_ok = open_n = 0
    open_max = 0
    run4 = lock4 = nwin = 0
    first_valid = None
    k = 0
    for n, seq, ts in gen(shape, jit, ppm, seconds, seed, est, step_at,
                          step_ns, seq0, ts0):
        m.pdu(seq, ts)
        if n % WIN_PDU == PHASE_PDU:
            nwin += 1
            if m.valid:
                if first_valid is None:
                    first_valid = n
                err = m.rate - true
                good = abs(err) < THR
                open_ok += good
                open_n += 1
                open_max = max(open_max, abs(err))
                run4 = run4 + 1 if good else 0
                lock4 += run4 >= LOCK_WIN
            sv.window(k, m.rate, m.valid)
            k += 1
    return dict(
        restarts=m.restarts, voids=m.voids,
        valid=open_n / max(nwin, 1),
        open=open_ok / open_n if open_n else 0.0, open_max=open_max,
        lock4=lock4 / max(open_n, 1),
        t_valid=(first_valid / 8_000.0) if first_valid is not None else None,
        t_lock=(sv.first_lock * 0.512 + PHASE_PDU / 8_000.0)
        if sv.first_lock is not None else None,
        closed=sv.ok / sv.runs if sv.runs else 0.0, drops=sv.drops,
        closed_max=sv.emax)


def fmt(tag, r):
    tl = f"{r['t_lock']:6.2f}" if r["t_lock"] is not None else "  none"
    return (f"{tag} valid={r['valid']:6.4f} restarts={r['restarts']:6d} "
            f"open<2ppm={r['open']:6.3f} open_max={r['open_max']:6d} "
            f"lock4={r['lock4']:6.3f} | closed<2ppm={r['closed']:6.3f} "
            f"closed_max={r['closed_max']:6d} drops={r['drops']:3d} "
            f"t_lock_s={tl}")


# ---------------------------------------------------------------- cases
def gain():
    print("== G. closed-loop gain: worst-case |e| per unit J for an N-window "
          "two-point estimator (l1 norm of the impulse response), plant "
          "gain g")
    s = sens_impulse()
    print(f"sensitivity ||S||_1 (g=1) = {sum(abs(x) for x in s):.4f}")
    for g in (0.8, 1.0, 1.2):
        for n in (1, 2, 4, 6, 8, 16):
            h = loop_impulse(n, taps=400, gain=g)
            l1 = sum(abs(x) for x in h)
            print(f"g={g:3.1f} N={n:2d} open-loop 2/N={2 / n:6.4f} "
                  f"closed-loop={l1:6.4f}  J=1042 -> {1042 * l1:6.0f} ns  "
                  f"J=1426 -> {1426 * l1:6.0f} ns")
    print("LS over one 512 ms window: open-loop worst case 3J (step of 2J "
          "at mid-window), closed-loop 2.125 x 3J")


def fstep():
    print("== F. a real talker frequency step of D ppm, linear loop, the "
          "servo converged before it: largest window |e| afterwards")
    for n in (1, 4, 8):
        for dppm in (1, 2, 4, 6, 8, 10):
            d = dppm * 512
            integ = u = 0.0
            hist = [0.0] * (n + 1)
            emax = 0.0
            for k in range(80):
                hist = hist[1:] + [d * (k + 1)]
                e = -u - (hist[-1] - hist[0]) / n
                integ += e / 2
                u = integ + e / 4
                emax = max(emax, abs(e))
            print(f"N={n} step {dppm:2d} ppm: max |e| = {emax:6.0f} ns "
                  f"({'stays LOCKED' if emax < THR else 'leaves LOCKED'})")


def shape_case(a):
    shape, jit, ppm, est, pick = a
    return fmt(f"{shape:8s} J={jit:5d} ppm={ppm:3d} {est:3s}-{pick}",
               run(shape, jit, ppm, est, pick))


def shapes():
    print("== A. lock test by error shape: the page's rules, void on, "
          "B = 4,096 ns, 120 s per case")
    rows = []
    shp = ("white", "galt", "gsign", "guni", "sine10", "sine100",
           "sine1000", "sine2000", "sine5000", "adv")
    for est, pick, ppms in (("E1", "P2", (0, 300)), ("E8", "P2", (0, 300)),
                            ("E1", "P1", (0,)), ("E8", "P1", (0,)),
                            ("E4", "P2", (0,)), ("LS1", "P2", (0,))):
        for shape in shp:
            for jit in (1042, 1426):
                for ppm in ppms:
                    rows.append((shape, jit, ppm, est, pick))
    with Pool(8) as pool:
        for line in pool.map(shape_case, rows):
            print(line, flush=True)


def tol_case(a):
    shape, jit, ppm = a
    r = run(shape, jit, ppm, "E8", "P2", seconds=30)
    return (f"{shape:6s} J={jit:5d} ppm={ppm:3d} E8-P2 restarts={r['restarts']:6d} "
            f"voids={r['voids']:6d} valid={r['valid']:6.4f}")


def tol():
    print("== T. effective per-timestamp tolerance of the void and spacing "
          "rules (B = 4,096 ns), 30 s per case; analytic: 2 J + 600 <= B "
          "(spacing, 300 ppm) -> 1,748 ns; 2 J + 562.5 <= B (in-group, "
          "300 ppm) -> 1,766 ns; 2 J <= B (0 ppm) -> 2,048 ns")
    rows = []
    for shape in ("white", "gsign", "galt"):
        for ppm in (0, 300):
            for jit in (1426, 1700, 1740, 1760, 1800, 2000, 2040, 2060, 2200,
                        2500):
                rows.append((shape, jit, ppm))
    with Pool(8) as pool:
        for line in pool.map(tol_case, rows):
            print(line, flush=True)
    print("-- the round-2 table's +/-2,500 ns independent row, void on and "
          "off (E1-P2, 120 s)")
    for void in (False, True):
        for ppm in (0, 300):
            r = run("white", 2500, ppm, "E1", "P2", use_void=void)
            print(fmt(f"white    J= 2500 ppm={ppm:3d} E1-P2 "
                      f"void={'on ' if void else 'off'}", r))


def step_case(a):
    est, step_ns, pos = a
    at = 12 * 8_000 + pos            # 12 s in, after lock
    at -= at % GROUP
    at += pos
    r = run("white", 1426, 300, est, "P2", seconds=24, seed=pos + 7,
            step_at=at, step_ns=step_ns)
    return (f"{est} step {step_ns:7d} ns at group pos {pos:2d}: "
            f"restarts={r['restarts']} voids={r['voids']} "
            f"closed_max_after_lock={r['closed_max']:5d} drops={r['drops']}")


def steps():
    print("== S. steps: white +/-1,426 ns, 300 ppm, P2, B = 4,096 ns; the "
          "step lands 12 s in (after lock), at each of the 16 group "
          "positions; closed loop")
    rows = []
    for est in ("E1", "E8"):
        for s in (20_833, -20_833, 10_417, 4_000, 3_000, 2_000):
            for pos in range(16):
                rows.append((est, s, pos))
    with Pool(8) as pool:
        out = pool.map(step_case, rows)
    for line in out:
        print(line, flush=True)


def wrap():
    print("== W. sequence wrap: 10 s ideal stream across 312 wraps, E8-P2")
    for sw in (True, False):
        m = Meter("E8", "P2", seq_wrap=sw)
        for n, seq, ts in gen("none", 0, 0, 10, 1, seq0=251,
                              ts0=M32 - 1_000_000):
            m.pdu(seq, ts)
        print(f"{'design' if sw else 'mutant: continuity without the 8-bit wrap'}: "
              f"restarts={m.restarts} voids={m.voids} valid_at_end={m.valid}")


def latency():
    print("== L. latency on an ideal stream at +10 ppm: first valid rate and "
          "first servo LOCKED, seconds after the first PDU")
    for est in ("E1", "E4", "E8", "LS1"):
        r = run("none", 0, 10, est, "P2", seconds=20)
        print(f"{est}: t_valid={r['t_valid']:.3f} s t_lock={r['t_lock']:.3f} s")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, fn in (("gain", gain), ("fstep", fstep), ("latency", latency),
                     ("wrap", wrap),
                     ("tol", tol), ("steps", steps), ("shapes", shapes)):
        if what in (name, "all"):
            fn()
            print(flush=True)
