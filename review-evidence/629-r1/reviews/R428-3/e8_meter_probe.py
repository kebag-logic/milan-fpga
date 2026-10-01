#!/usr/bin/env python3
"""Reviewer probe of the #629 AAF meter under E8 (PR #631, head a463a1de).

Written by the reviewer from the design page's rules, not from the author's
model. Implements, per MEDIA_CLOCK_FOLLOWING.md:
  * groups of 16 PDUs by sequence_num % 16 (8-bit wrap); every PDU required,
    a sequence gap restarts the history (:476-477, :678-680);
  * in-group void: any |ts_i - ts_0 - i*125,000| > 4,096 ns voids the group
    and restarts the history (:476-477, :523-527);
  * pick = ts_0 + floor(sum_i(ts_i - ts_0 - i*125,000) / 16) mod 2^32 (:468);
  * spacing: adjacent picks 2 ms +/- 4,096 ns, else restart (:507, :679);
  * E8: every 256 fresh intervals a snapshot; rate = (P_now - P_8ago -
    8*512,000,000) >>> 3, valid after 2,048 fresh intervals (:584-597).
Servo, from KL_mmcm_drp_servo.sv as written: e = locerr - rate (:643);
integ = clamp(integ + e>>>1); u = clamp(integ + e>>>2), slew +/-51,200
(:647-681); |e| < 1,024 counts toward LOCKED (4 in a row), one bad window
drops LOCKED (:648, :564-568); no PI and no lock update on an invalid rate
(:613-615). Plant: locerr_k = D0 - round(g * u_{k-1}) + q_k, D0 = 10.64 ppm,
q uniform +/-20 ns. Servo windows run on their own 512 ms grid, at a chosen
phase against the stream, and sample the latest published rate, so a
talker at +/-300 ppm slides against the windows.

Shapes (peak J ns per PDU timestamp):
  gsign    one random sign per 16-PDU group      galt   alternating per group
  palt     alternating per PDU                   white  independent uniform
  sineP    J sin(2 pi t / P ms)                  triP   triangle, period P ms
  sawP     sawtooth -J..+J over P ms, then a 2J return
  bsign    one random sign per 512 ms block of the stream
  adv      +/-J per 512 ms snapshot block, signs from the reviewer's own
           closed-loop impulse response of E8 (worst case for the bound)
Usage: python3 e8_meter_probe.py [latency|tol|steps|shapes|all]
Standard library only; deterministic seeds; at most 8 worker processes.
"""
import math
import random
import sys
import zlib
from multiprocessing import Pool

PDU = 125_000
NOMP = 16 * PDU
WINP = 256
NOMW = WINP * NOMP
B = 4_096
M32 = 1 << 32
THR = 1_024
D0 = round(10.64 * 512)


def s32(x):
    x &= M32 - 1
    return x - M32 if x & (1 << 31) else x


def adv_signs(n_est=8, g=1.0, taps=96):
    """Signs making e worst at the last tap: the reviewer's own derivation."""
    integ = u = 0.0
    eps = [0.0] * (n_est + 1)
    h = []
    for k in range(taps):
        eps = eps[1:] + [1.0 if k == 0 else 0.0]
        e = -g * u - (eps[-1] - eps[0]) / n_est
        integ += e / 2
        u = integ + e / 4
        h.append(e)
    return [1 if h[taps - 1 - m] >= 0 else -1 for m in range(taps)]


def err_fn(shape, j, seed):
    rng = random.Random(seed)
    if shape == "gsign":
        cache = {}
        return lambda n, t: cache.setdefault(n // 16, j if rng.random() < .5 else -j)
    if shape == "bsign":
        cache = {}
        return lambda n, t: cache.setdefault(n // 4096, j if rng.random() < .5 else -j)
    if shape == "galt":
        return lambda n, t: j if (n // 16) % 2 == 0 else -j
    if shape == "palt":
        return lambda n, t: j if n % 2 == 0 else -j
    if shape == "white":
        return lambda n, t: rng.uniform(-j, j)
    if shape.startswith("sine"):
        p = float(shape[4:]) * 1e6
        return lambda n, t: j * math.sin(2 * math.pi * t / p)
    if shape.startswith("tri"):
        p = float(shape[3:]) * 1e6
        return lambda n, t: j * (4 * abs((t / p) % 1.0 - 0.5) - 1)
    if shape.startswith("saw"):
        p = float(shape[3:]) * 1e6
        return lambda n, t: j * (2 * ((t / p) % 1.0) - 1)
    if shape == "adv":
        sg = adv_signs()
        return lambda n, t: j * sg[(n // 4096) % len(sg)]
    if shape == "none":
        return lambda n, t: 0.0
    raise ValueError(shape)


class Meter:
    def __init__(self):
        self.restarts = 0
        self.exp = None
        self.grp = None
        self.reset()

    def reset(self):
        self.last = None
        self.fresh = 0
        self.ring = [None] * 8
        self.wptr = 0
        self.valid = False
        self.rate = 0

    def restart(self):
        self.restarts += 1
        self.reset()

    def pdu(self, seq, ts):
        if self.exp is not None and seq != self.exp:
            self.grp = None
            self.restart()
        self.exp = (seq + 1) & 0xFF
        pos = seq & 15
        if pos == 0:
            self.grp = [ts]
        elif self.grp is not None and len(self.grp) == pos:
            self.grp.append(ts)
        else:
            self.grp = None
            return False
        if len(self.grp) < 16:
            return False
        g0 = self.grp[0]
        devs = [s32(t - g0 - i * PDU) for i, t in enumerate(self.grp)]
        self.grp = None
        if max(abs(d) for d in devs) > B:
            self.restart()
            return False
        pk = (g0 + sum(devs) // 16) & (M32 - 1)
        if self.last is not None:
            if abs(s32(pk - self.last) - NOMP) > B:
                self.restart()
                self.last = pk
                self._snap(pk)
                return False
            self.fresh += 1
        self.last = pk
        return self._snap(pk)

    def _snap(self, pk):
        if self.fresh % WINP:
            return False
        old = self.ring[self.wptr]
        self.ring[self.wptr] = pk
        self.wptr = (self.wptr + 1) & 7
        if self.fresh >= 8 * WINP and old is not None:
            self.rate = s32(pk - old - 8 * NOMW) >> 3
            self.valid = True
            return True
        return False


class Servo:
    def __init__(self, g, seed):
        self.g = g
        self.rng = random.Random(seed)
        self.integ = self.u = 0
        self.cnt = 0
        self.locked = False
        self.t_lock = None
        self.drops = 0
        self.worst = 0
        self.after = self.good = 0

    def window(self, t, rate, valid):
        if not valid:
            return
        loc = D0 - round(self.g * self.u) + self.rng.randint(-20, 20)
        e = loc - rate
        isum = max(-102_400, min(102_400, self.integ + (e >> 1)))
        un = max(-102_400, min(102_400, isum + (e >> 2)))
        du = max(-51_200, min(51_200, un - self.u))
        self.u += du
        self.integ = isum
        ok = -THR < e < THR
        self.cnt = min(4, self.cnt + 1) if ok else 0
        if self.t_lock is not None:
            self.after += 1
            self.good += ok
            self.worst = max(self.worst, abs(e))
        if not self.locked and self.cnt >= 4:
            self.locked = True
            if self.t_lock is None:
                self.t_lock = t
        elif self.locked and self.cnt == 0:
            self.locked = False
            self.drops += 1


def run(shape, j, ppm, seconds=120, g=1.0, phase_ms=0.37, seed=None,
        step_at=None, step_ns=0, seq0=0, ts0=0, talker_ppm_true=None):
    if seed is None:
        seed = zlib.crc32(f"{shape}|{j}|{ppm}|{phase_ms}".encode())
    ef = err_fn(shape, j, seed)
    m = Meter()
    sv = Servo(g, seed ^ 0x3C3C)
    true = round(ppm * 512)
    per = PDU * (1 + ppm * 1e-6)          # gPTP ns per PDU
    nxt = phase_ms * 1e6 + NOMW            # next servo boundary, gPTP ns
    n_pdu = int(seconds * 1e9 / per)
    first_valid = None
    for n in range(n_pdu):
        t = n * per
        while t >= nxt:
            sv.window(nxt, m.rate - true if m.valid else 0, m.valid)
            nxt += NOMW
        e = ef(n, t)
        if step_at is not None and n >= step_at:
            e += step_ns
        ts = int(round(ts0 + t + e)) & (M32 - 1)
        if m.pdu((seq0 + n) & 0xFF, ts) and first_valid is None:
            first_valid = t
    return dict(restarts=m.restarts, drops=sv.drops, worst=sv.worst,
                frac=(sv.good / sv.after) if sv.after else 0.0,
                t_lock=None if sv.t_lock is None else sv.t_lock / 1e9,
                t_valid=None if first_valid is None else first_valid / 1e9)


def fmt(tag, r):
    tl = "none" if r["t_lock"] is None else f"{r['t_lock']:.2f}"
    return (f"{tag:44s} restarts={r['restarts']:4d} windows_ok={r['frac']:.3f} "
            f"worst_e={r['worst']:5d} drops={r['drops']:2d} t_lock_s={tl}")


def shape_case(a):
    shape, j, ppm, g, ph = a
    return fmt(f"{shape:8s} J={j:5d} ppm={ppm:4d} g={g} phase={ph}ms",
               run(shape, j, ppm, g=g, phase_ms=ph))


def shapes():
    print("== shapes: E8 + P2, B = 4,096 ns, 120 s each; worst_e and drops "
          "counted after the first LOCKED")
    rows = []
    for shape in ("gsign", "bsign", "galt", "palt", "white", "sine10",
                  "sine1000", "sine2000", "sine4096", "sine8192", "tri4096",
                  "tri8192", "tri1000", "saw4096", "saw2048", "saw512",
                  "adv"):
        for j in (1042, 1426, -1426) if shape == "adv" else (1042, 1426):
            for ppm in (0, 300, -300):
                rows.append((shape, j, ppm, 1.0, 0.37))
    for ph in (0.0, 1.0, 255.9, 511.9):
        rows.append(("adv", 1426, 0, 1.0, ph))
    for g in (0.8, 1.2):
        rows.append(("adv", 1426, 0, g, 0.37))
        rows.append(("gsign", 1426, 300, g, 0.37))
    with Pool(8) as p:
        for line in p.map(shape_case, rows):
            print(line, flush=True)


def step_case(a):
    step, pos, ppm = a
    at = (20 * 8000) - ((20 * 8000) % 16) + pos   # 20 s in, after LOCKED
    r = run("gsign", 1042, ppm, seconds=40, step_at=at, step_ns=step,
            seed=pos * 31 + 5)
    return fmt(f"step {step:7d} ns pos {pos:2d} ppm={ppm:4d}", r)


def steps():
    print("== steps on gsign +/-1,042 ns at 20 s (after LOCKED), every group "
          "position; a rejected step restarts the history (restarts >= 1)")
    rows = [(s, p, ppm) for s in (20_833, -20_833, 10_417, -10_417)
            for p in range(16) for ppm in (0, 300)]
    rows += [(s, p, 0) for s in (0,) for p in (0,)]
    with Pool(8) as p:
        out = p.map(step_case, rows)
    for line in out:
        print(line, flush=True)


def tol_case(a):
    shape, j, ppm = a
    r = run(shape, j, ppm, seconds=30)
    return (f"{shape:6s} J={j:5d} ppm={ppm:4d} restarts={r['restarts']:6d} "
            f"rate_ever_valid={r['t_valid'] is not None}")


def tol():
    print("== void and spacing tolerance (B = 4,096 ns), 30 s each. Analytic: "
          "correlated 2J + 600 <= B at 300 ppm -> 1,748; in-group 2J + 562.5 "
          "<= B -> 1,766; 2J <= B at 0 ppm -> 2,048")
    rows = [(s, j, ppm) for s in ("gsign", "white")
            for ppm in (0, 300)
            for j in (1426, 1740, 1748, 1749, 1760, 1800, 2040, 2048, 2049,
                      2060, 2500)]
    with Pool(8) as p:
        for line in p.map(tol_case, rows):
            print(line, flush=True)


def latency():
    print("== latency, ideal stream, history start at t = 0")
    for ppm in (0, 10, 100):
        r = run("none", 0, ppm, seconds=20)
        print(f"ppm={ppm:3d}: first valid rate {r['t_valid']:.3f} s; first "
              f"LOCKED {r['t_lock']:.2f} s")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, fn in (("latency", latency), ("tol", tol), ("steps", steps),
                     ("shapes", shapes)):
        if what in (name, "all"):
            fn()
            print(flush=True)
