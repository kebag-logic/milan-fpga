#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Desk model of the AAF clock meter rules, #629 design round 4.

A model of the meter's stated rules and of the servo's lock test, under
assumed presentation-time error shapes and PDU-loss patterns. Not a model of
any talker or network.

Round 3's rules are kept (the round-3 model, meter_rules_model_r3.py, is the
base of this file):
  * one PDU per 125,000 ns; groups of 16 by sequence_num % 16 (8-bit wrap);
  * every PDU of a group is required;
  * an in-group deviation |ts_i - ts_0 - i*125,000| above B = 4,096 ns
    voids the group and restarts the history (a deviation void);
  * pick P2 = ts_0 + floor(sum_i (ts_i - ts_0 - i*125,000) / 16), integer ns
    modulo 2^32;
  * adjacent picks must be 2 ms +/- B apart, or the history restarts;
  * E8: a snapshot every 256 group intervals into an 8-entry ring,
    rate = (S_now - S_8_ago - 8 * 512,000,000) >>> 3, valid once the ring
    holds 8 snapshots and a ninth is written (2,048 intervals).

Round 4 changes one rule, the manager's option (b) for a lost PDU:
  LOSS RULE "b" (the design):
  * a sequence gap (a PDU lost, or not consumed) voids the group it falls in
    (a loss void) and does NOT restart the history;
  * the next valid pick is checked across the gap: k, the number of group
    intervals since the last valid pick, comes from sequence_num[7:4]
    (mod 16); k = 2 (one voided group) needs a spacing of 4 ms +/- BGAP,
    BGAP = 5,120 ns; k >= 3 (two or more adjacent voided groups) restarts
    the history; a check that fails restarts it;
  * snapshots stay on the group grid: the group counter advances by k; a
    loss-voided snapshot group is filled with the midpoint of its two
    neighbours, last + (s32(new - last) >>> 1).
  LOSS RULE "r3" (round 3, and the round-4 mutant "restart on any loss"):
  * a sequence gap voids the group and restarts the history.
Other mutants: gap_check=False (no continuity check across a gap);
snap_fill="nominal" (the next valid pick less the nominal 2 ms per group),
"next" (the next valid pick stored uncorrected) and "restart" (a voided
snapshot group restarts the history); kmax=16 (no restart on a
multi-group gap).

Servo (KL_mmcm_drp_servo.sv), as in round 3: samples the rate once per
512 ms window (:609); runs PI only on a valid rate (:613-615), so an invalid
rate holds u, the integrator and the lock count, and LOCKED with them;
e = locerr - rate (:643); integ += e >>> 1 (:228, :647);
u = clamp(integ) + e >>> 2 (:229, :669), clamped to +-102,400 and slewed by
+-51,200 per window (:230-231, :681); lock qualification |e| < 1,024 (:232,
:648); LOCKED after 4 qualifying windows (:233, :566), and one failing
window drops LOCKED (:567, :689-694). Closed loop on a plant of gain 1 with
a one-window delay: locerr_k = true + D0 - u_{k-1} + q_k, D0 = 10.64 ppm,
q_k uniform +-20 ns.

Error shapes (peak J ns per PDU timestamp) are round 3's: white, galt,
gsign, guni, sineP (P in ms), adv (the worst case for E8 in closed loop).

Loss patterns (PDU index n from the stream's first PDU, seq0 = 0):
  per:K:P     drop n where n % K == P (n >= K)
  burst:K:L:P drop L consecutive PDUs from each n % K == P (n >= K)
  rand:p      drop each PDU with probability p (own seed)
  after:N:... the pattern ... from PDU N on

Standard library only, deterministic seeds, at most 8 worker processes.
Usage: python3 meter_rules_model_r4.py
         [bound|regress|fill|p1|loss|steps|tol|fstep|legs|shapes|all]
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
RING = 256                      # group intervals per 512 ms window
NOM_WIN = RING * NOM            # 512,000,000 ns
WIN_PDU = RING * GROUP          # 4,096 PDUs per 512 ms window
THR = 1_024
B = 4_096
BGAP = 5_120
M32 = 1 << 32
U_MAX, SLEW = 102_400, 51_200
LOCK_WIN = 4
D0 = round(10.64 * 512)         # initial local frequency error, x512 units
QN = 20                         # local window quantisation, ns
PHASE_PDU = 1_234               # servo window phase against the stream
WORKERS = 8


def s32(x):
    x &= M32 - 1
    return x - M32 if x >= 1 << 31 else x


# ---------------------------------------------------------------- the loop
def loop_impulse(n_est, taps=64, gain=1.0):
    out = []
    integ = u = 0.0
    hist = [0.0] * (n_est + 1)
    for k in range(taps):
        ek = 1.0 if k == 0 else 0.0
        hist = hist[1:] + [ek]
        n = (hist[-1] - hist[0]) / n_est
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
    n = {"E1": 1, "E4": 4, "E8": 8}[est]
    h = loop_impulse(n, taps=period)
    return [(1 if h[period - 1 - j] < 0 else -1) for j in range(period)]


# ---------------------------------------------------------------- stimulus
def loss_fn(spec, seed):
    if spec is None:
        return lambda n: False
    kind, *a = spec.split(":")
    if kind == "after":
        n0, inner = int(a[0]), loss_fn(":".join(a[1:]), seed)
        return lambda n: n >= n0 and inner(n)
    if kind == "per":
        k, p = int(a[0]), int(a[1])
        return lambda n: n >= k and n % k == p
    if kind == "burst":
        k, ln, p = int(a[0]), int(a[1]), int(a[2])
        return lambda n: n >= k and 0 <= (n - p) % k < ln
    if kind == "rand":
        p = float(a[0])
        r = random.Random(seed ^ 0x10551055)
        return lambda n: r.random() < p
    if kind == "set":
        s = set(int(x) for x in a[0].split(","))
        return lambda n: n in s
    raise ValueError(spec)


def gen(shape, jit, ppm, seconds, seed, est="E8", step_at=None, step_ns=0,
        seq0=0, ts0=0, loss=None, fstep=None):
    rng = random.Random(seed)
    lost = loss_fn(loss, seed)
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
            blk = g // RING
            e = jit * pat[blk % len(pat)]
        else:
            e = 0.0
        if step_at is not None and n >= step_at:
            e += step_ns
        t = n * PDU_NS * (1 + ppm * 1e-6)
        if fstep is not None and n >= fstep[0]:
            t += (n - fstep[0]) * PDU_NS * fstep[1] * 1e-6
        ts = int(round(ts0 + t + e)) % M32
        yield n, (seq0 + n) & 0xFF, ts, lost(n)


# ---------------------------------------------------------------- meter
class Meter:
    def __init__(self, est="E8", pick="P2", loss_rule="b", use_void=True,
                 seq_wrap=True, gap_check=True, snap_fill="mid", kmax=2):
        assert est in ("E1", "E8")
        assert est == "E8" or loss_rule == "r3"
        self.est, self.pick, self.loss_rule = est, pick, loss_rule
        self.use_void, self.seq_wrap = use_void, seq_wrap
        self.gap_check, self.snap_fill, self.kmax = gap_check, snap_fill, kmax
        self.restarts = self.voids = self.loss_voids = self.fills = 0
        self.rate, self.valid = 0, False
        self.exp_seq = None
        self.grp = None
        self._restart()

    def _restart(self):
        self.c = None                         # group intervals since restart
        self.last = None
        self.last_g = None
        self.hist = deque(maxlen=RING + 1)    # E1 picks
        self.snaps = deque(maxlen=9)          # E8 ring plus the new entry
        self.valid = False

    def _break(self):
        self.restarts += 1
        self._restart()

    def _begin(self, pk, gi):
        self.c = 0
        self.last, self.last_g = pk, gi
        self._estimate(pk, snap=True)

    def pdu(self, seq, ts):
        if self.exp_seq is not None and seq != self.exp_seq:
            self.grp = None
            if self.loss_rule == "r3":
                self.voids += 1
                self._break()
            else:
                self.loss_voids += 1
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
        gi = (seq >> 4) & 0xF
        if self.last is None:
            self._begin(pk, gi)
            return
        k = (gi - self.last_g) % 16 or 16
        if not self.seq_wrap:
            k = 1 if (seq >> 4) - self.last_g == 1 else 99
        if k > self.kmax:
            self._break()
            self._begin(pk, gi)
            return
        sp = s32(pk - self.last) - k * NOM
        bound = B if k == 1 else BGAP
        if (k == 1 or self.gap_check) and abs(sp) > bound:
            self._break()
            self._begin(pk, gi)
            return
        c_old, self.c = self.c, self.c + k
        if self.est == "E1":
            self.hist.append(pk)
            if self.c >= RING:
                self.rate = s32(pk - self.hist[0] - NOM_WIN)
                self.valid = True
        else:
            m = (c_old // RING + 1) * RING     # next snapshot group
            if m <= self.c:
                if m == self.c:
                    self._estimate(pk, snap=True)
                else:
                    d = m - c_old                # 1 when k = 2
                    if self.snap_fill == "mid":
                        fill = (self.last + (s32(pk - self.last) * d) // k) % M32
                    elif self.snap_fill == "nominal":
                        fill = (pk - (k - d) * NOM) % M32
                    elif self.snap_fill == "next":
                        fill = pk
                    else:                        # "restart" mutant
                        self._break()
                        self._begin(pk, gi)
                        return
                    self.fills += 1
                    self._estimate(fill, snap=True)
        self.last, self.last_g = pk, gi

    def _estimate(self, s, snap):
        if self.est == "E1":
            self.hist.append(s)
            return
        self.snaps.append(s)
        if len(self.snaps) == 9:
            d = s32(self.snaps[-1] - self.snaps[0] - 8 * NOM_WIN)
            self.rate = d >> 3
            self.valid = True


# ---------------------------------------------------------------- servo
class Servo:
    def __init__(self, true_rate, rng, gain=1.0):
        self.true = true_rate
        self.rng = rng
        self.gain = gain
        self.integ = self.u = 0
        self.lock_cnt = 0
        self.locked = False
        self.first_lock = None
        self.drops = 0
        self.ok = self.runs = 0
        self.emax = 0
        self.lk_win = self.post_win = 0

    def window(self, k, rate, valid):
        if self.first_lock is not None:
            self.post_win += 1
            self.lk_win += self.locked
        if not valid:
            return
        loc = self.true + D0 - int(round(self.gain * self.u)) \
            + self.rng.randint(-QN, QN)
        e = loc - rate
        isum = self.integ + (e >> 1)
        ig = max(-U_MAX, min(U_MAX, isum))
        un = ig + (e >> 2)
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


def run(shape, jit, ppm, est="E8", pick="P2", seconds=120, seed=None,
        step_at=None, step_ns=0, loss=None, fstep=None, gain=1.0,
        open_thr=None, **mk):
    if seed is None:
        seed = zlib.crc32(f"{shape}/{jit}/{ppm}".encode())
    m = Meter(est, pick, **mk)
    true = int(round(ppm * 512))
    sv = Servo(true, random.Random(seed ^ 0x5A5A), gain)
    open_ok = open_n = open_over = 0
    open_max = 0
    nwin = 0
    first_valid = None
    rates = []
    k = 0
    for n, seq, ts, lost in gen(shape, jit, ppm, seconds, seed, est,
                                step_at, step_ns, loss=loss, fstep=fstep):
        # a lost PDU never reaches the meter; the servo's window is local
        # time, so it is sampled whether or not that PDU arrived
        if not lost:
            m.pdu(seq, ts)
        if n % WIN_PDU == PHASE_PDU:
            nwin += 1
            if m.valid:
                if first_valid is None:
                    first_valid = n
                err = m.rate - true
                if fstep is not None and n >= fstep[0]:
                    err = None
                if err is not None:
                    open_ok += abs(err) < THR
                    open_n += 1
                    open_max = max(open_max, abs(err))
                    if open_thr is not None:
                        open_over += abs(err) > open_thr
            rates.append(m.rate if m.valid else None)
            sv.window(k, m.rate, m.valid)
            k += 1
    return dict(
        restarts=m.restarts, voids=m.voids, loss_voids=m.loss_voids,
        fills=m.fills,
        valid=sum(r is not None for r in rates) / max(nwin, 1),
        open=open_ok / open_n if open_n else 0.0, open_max=open_max,
        open_over=open_over, open_n=open_n,
        t_valid=(first_valid / 8_000.0) if first_valid is not None else None,
        t_lock=(sv.first_lock * 0.512 + PHASE_PDU / 8_000.0)
        if sv.first_lock is not None else None,
        closed=sv.ok / sv.runs if sv.runs else 0.0, drops=sv.drops,
        closed_max=sv.emax,
        lk=sv.lk_win / sv.post_win if sv.post_win else 0.0,
        rates=rates)


def fmt(tag, r):
    tl = f"{r['t_lock']:6.2f}" if r["t_lock"] is not None else "  none"
    return (f"{tag} valid={r['valid']:6.4f} restarts={r['restarts']:5d} "
            f"lossvoids={r['loss_voids']:6d} fills={r['fills']:3d} "
            f"open_max={r['open_max']:5d} | closed<2ppm={r['closed']:6.3f} "
            f"closed_max={r['closed_max']:5d} drops={r['drops']:3d} "
            f"lockedfrac={r['lk']:5.3f} t_lock_s={tl}")


def pmap(fn, rows):
    with Pool(WORKERS) as pool:
        return pool.map(fn, rows)


# ---------------------------------------------------------------- sections
def bound():
    print("== K. the gap bound: a continuity bound B_k across k group "
          "intervals must admit the design point (2J + 601 k, J = 1,426 ns, "
          "300 ppm; 601 ns is KL_crf_rx's rate term per 2 ms) and still catch "
          "a half-sample step (B_k < 10,417 - 2J - 601 k)")
    J = 1426
    for k in range(1, 6):
        lo = 2 * J + 601 * k
        hi = 10_417 - 2 * J - 601 * k
        b = B if k == 1 else BGAP
        ok = lo <= b < hi
        print(f"k={k}: need {lo:5d} <= B_k < {hi:5d}  "
              f"{'window exists' if lo < hi else 'NO window'}; "
              f"{'B' if k == 1 else 'BGAP'}={b} "
              f"{'inside' if ok else 'outside'}; tolerance at 300 ppm "
              f"J <= {(b - 601 * k) // 2} ns, at 0 ppm J <= {b // 2} ns")
    print("generic E8 closed-loop bound for ANY sequence of E8 rates "
          f"(|rate error| <= 2J/8): 2.125 * 2 * 1426 / 8 = "
          f"{2.125 * 2 * 1426 / 8:.0f} ns")
    print("random independent PDU loss p: a restart needs two adjacent "
          "loss-voided groups; groups per second 500; rate ~ 500 q^2, "
          "q = 1 - (1-p)^16")
    for p in (1e-6, 1e-5, 1e-4, 3e-4, 1e-3, 1.4e-3, 3e-3, 1e-2):
        q = 1 - (1 - p) ** 16
        r = 500 * q * q
        print(f"p={p:8.1e} ({p * 8000:7.3f} lost/s): restarts ~{r:9.2e}/s "
              f"(one per {1 / r:10.1f} s); r3 rule restart rate "
              f"{8000 * p:9.2e}/s")


def regress_case(a):
    shape, jit, ppm, rule = a
    r = run(shape, jit, ppm, loss_rule=rule)
    return fmt(f"{shape:8s} J={jit:5d} ppm={ppm:3d} E8-P2 rule={rule:2s}", r)


def regress():
    print("== R. regression, no loss: rule b equals the round-3 rules "
          "(each pair must match exactly)")
    rows = []
    for shape in ("white", "gsign", "sine10", "adv"):
        for jit in (1042, 1426):
            for ppm in (0, 300):
                for rule in ("r3", "b"):
                    rows.append((shape, jit, ppm, rule))
    out = pmap(regress_case, rows)
    for i in range(0, len(out), 2):
        a, b = out[i], out[i + 1]
        same = a.split("rule=")[1][2:] == b.split("rule=")[1][2:]
        print(a)
        print(b + ("   [match]" if same else "   [DIFFERS]"))


def loss_case(a):
    tag, loss, jit, ppm, rule, kw, secs = a
    r = run("white", jit, ppm, loss=loss, loss_rule=rule, seconds=secs, **kw)
    return fmt(f"{tag:34s} J={jit:5d} ppm={ppm:3d} rule={rule:2s}", r)


def loss():
    print("== P. PDU loss, independent error, E8-P2; rule b (design) against "
          "rule r3 (round 3, the restart-on-any-loss mutant); 120 s unless "
          "stated")
    rows = []
    pats = [
        ("none", None),
        ("1 in 1 s (8000)", "per:8000:1234"),
        ("1 in 0.3 s (2400)", "per:2400:777"),
        ("1 in 0.5 s (4000)", "per:4000:100"),
        ("1 in 2 s", "per:16000:5000"),
        ("1 in 5 s", "per:40000:9000"),
        ("1 in 512 ms on the snapshot group", "per:4096:5"),
        ("1 in 32 PDUs (4 ms)", "per:32:3"),
        ("1 in 48 PDUs (6 ms)", "per:48:21"),
        ("1 in 33 PDUs", "per:33:0"),
        ("1 in 24 PDUs (beyond: adjacent groups)", "per:24:7"),
        ("2-burst 1 in 1 s inside a group", "burst:8000:2:1236"),
        ("2-burst 1 in 1 s across a group edge", "burst:8000:2:1247"),
        ("2-burst 1 in 5 s across a group edge", "burst:40000:2:1247"),
        ("17-burst 1 in 1 s", "burst:8000:17:1234"),
    ]
    for tag, sp in pats:
        for jit, ppm in ((1042, 0), (1426, 300)):
            for rule in ("b", "r3"):
                rows.append((tag, sp, jit, ppm, rule, {}, 120))
    for tag, sp in (("beyond the bound from 20 s: 2-burst "
                     "across an edge 1 in 1 s", "after:160000:burst:8000:2:1247"),
                    ("beyond the bound from 20 s: 1 in 24 PDUs",
                     "after:160000:per:24:7")):
        for rule in ("b",):
            rows.append((tag, sp, 1426, 300, rule, {}, 60))
    for p in (1e-5, 1e-4, 3e-4, 1e-3, 3e-3):
        for rule in ("b", "r3"):
            rows.append((f"random p={p:.0e}", f"rand:{p}", 1042, 0, rule, {},
                         300))
    for line in pmap(loss_case, rows):
        print(line, flush=True)


def shape_case(a):
    shape, jit, ppm, loss, gain = a
    r = run(shape, jit, ppm, loss=loss, gain=gain)
    lt = loss if loss else "none"
    return fmt(f"{shape:8s} J={jit:5d} ppm={ppm:3d} g={gain:3.1f} "
               f"loss={lt:12s} E8-P2-b", r)


def shapes():
    print("== A. lock test by error shape with losses, E8-P2, rule b, "
          "B = 4,096 ns, BGAP = 5,120 ns, 120 s per case")
    rows = []
    shp = ("white", "galt", "gsign", "guni", "sine10", "sine100",
           "sine1000", "sine2000", "sine5000", "adv")
    for loss in (None, "per:8000:1234", "per:2400:777", "per:4096:5",
                 "per:32:3"):
        for shape in shp:
            for jit in (1042, 1426):
                for ppm in (0, 300):
                    rows.append((shape, jit, ppm, loss, 1.0))
    for loss in (None, "per:4096:5"):
        for gain in (0.8, 1.2):
            rows.append(("adv", 1426, 300, loss, gain))
    for line in pmap(shape_case, rows):
        print(line, flush=True)


def step_case(a):
    tag, s, pos, lpos, kw = a
    base = 12 * 8_000                # 12 s in, after lock
    base -= base % GROUP
    at = base + pos                  # the step lands at group position pos
    loss = None if lpos is None else f"set:{base + lpos}"
    r = run("white", 1426, 300, seconds=24, seed=pos + 7, step_at=at,
            step_ns=s, loss=loss, **kw)
    return (f"{tag:22s} step {s:7d} ns at pos {pos:2d}, lost pos "
            f"{'-' if lpos is None else lpos:>2}: restarts={r['restarts']} "
            f"lossvoids={r['loss_voids']} voids={r['voids']} "
            f"closed_max={r['closed_max']:5d} drops={r['drops']}")


def steps():
    print("== S. steps: white +/-1,426 ns, 300 ppm, E8-P2, rule b; the step "
          "lands 12 s in (after lock) at each group position. 'in gap': "
          "the same group also loses one PDU, so the step meets the "
          "continuity check across the gap, not the in-group void")
    rows = []
    for s in (20_833, -20_833, 10_417, -10_417):
        for pos in range(16):
            rows.append(("no loss", s, pos, None, {}))
            rows.append(("in gap", s, pos, 15 if pos != 15 else 0, {}))
            rows.append(("in gap, mutant no-chk", s, pos,
                         15 if pos != 15 else 0, {"gap_check": False}))
    for s in (0,):
        for pos in (0, 7):
            rows.append(("control in gap", s, pos, 15, {}))
    out = pmap(step_case, rows)
    for line in out:
        print(line, flush=True)


def tol_case(a):
    shape, jit, ppm, loss = a
    r = run(shape, jit, ppm, seconds=30, loss=loss)
    return (f"{shape:6s} J={jit:5d} ppm={ppm:3d} loss="
            f"{loss if loss else 'none':12s} restarts={r['restarts']:6d} "
            f"voids={r['voids']:6d} lossvoids={r['loss_voids']:5d} "
            f"valid={r['valid']:6.4f}")


def tol():
    print("== T. tolerance of the void and spacing rules with and without "
          "loss (1 in 0.3 s), 30 s per case")
    rows = []
    for shape in ("white", "gsign"):
        for ppm in (0, 300):
            for jit in (1426, 1740, 1748, 1749, 1760, 1800, 2040, 2048, 2049,
                        2060, 2500):
                for loss in (None, "per:2400:777"):
                    rows.append((shape, jit, ppm, loss))
    for line in pmap(tol_case, rows):
        print(line, flush=True)


def fill():
    print("== F. a loss in a snapshot group, ideal timestamps at +100 ppm "
          "(lost PDU 5 of the snapshot group at 3 x 512 ms, n = 12,293); "
          "rate against the no-loss run, every window")
    ref = run("none", 0, 100, seconds=12)["rates"]
    for tag, kw in (("design (midpoint fill)", {}),
                    ("mutant: next pick less nominal 2 ms",
                     {"snap_fill": "nominal"}),
                    ("mutant: next pick, uncorrected", {"snap_fill": "next"}),
                    ("mutant: restart on a voided snapshot group",
                     {"snap_fill": "restart"}),
                    ("mutant: restart on any loss (r3)", {"loss_rule": "r3"})):
        r = run("none", 0, 100, seconds=12, loss="set:12293", **kw)
        diffs = [(a - b) for a, b in zip(r["rates"], ref)
                 if a is not None and b is not None]
        mx = max((abs(d) for d in diffs), default=None)
        print(f"{tag:44s} restarts={r['restarts']} fills={r['fills']} "
              f"valid={r['valid']:.4f} max|rate - no-loss rate|={mx}")
    print("-- the gap bound: two lost PDUs in adjacent groups (n = 12,300 "
          "and 12,310, groups 768 and 769), 12 s")
    for tag, kw in (("design", {}), ("mutant: kmax 16", {"kmax": 16})):
        r = run("none", 0, 100, seconds=12, loss="set:12300,12310", **kw)
        print(f"{tag:44s} restarts={r['restarts']} lossvoids={r['loss_voids']}")


def fstep_case(a):
    est, dppm, ph = a
    at = 20 * 8_000 + (ph * WIN_PDU) // 16
    r = run("none", 0, 10, est=est, seconds=40, fstep=(at, dppm),
            loss_rule="r3" if est == "E1" else "b")
    return (est, dppm, ph, r["drops"], r["closed_max"])


def fstep():
    print("== Q. a real talker frequency step of D ppm, 20 s in, after lock, "
          "at 16 phases across one servo window; full meter and servo, "
          "ideal timestamps, 40 s")
    rows = []
    ds = (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 8.5, 9.0,
          9.5, 10.0, 11.0)
    for est in ("E1", "E8"):
        for d in ds:
            for ph in range(16):
                rows.append((est, d, ph))
    res = pmap(fstep_case, rows)
    for est in ("E1", "E8"):
        for d in ds:
            sub = [r for r in res if r[0] == est and r[1] == d]
            nd = sum(r[3] > 0 for r in sub)
            mx = max(r[4] for r in sub)
            mn = min(r[4] for r in sub)
            print(f"{est} step {d:4.1f} ppm: drops LOCKED at {nd:2d} of 16 "
                  f"phases; worst |e| {mn:5d} to {mx:5d} ns across phases")


def p1():
    print("== M. the first-PDU pick mutant (P1) against the 256 ns "
          "independent-error criterion, white +/-1,426 ns, 300 ppm, pinned "
          "seed, 120 s; open-loop rate error per servo window")
    for pick in ("P2", "P1"):
        r = run("white", 1426, 300, pick=pick, open_thr=256)
        print(f"{pick}: windows with a valid rate {r['open_n']}, "
              f"over 256 ns {r['open_over']}, open_max {r['open_max']} ns, "
              f"closed_max {r['closed_max']} ns")
    print("-- the window-error quantity (R428-3 S1): white +/-1,426 ns, 0 ppm")
    for pick in ("P2", "P1"):
        r = run("white", 1426, 0, pick=pick)
        print(f"{pick}: open-loop rate error max {r['open_max']} ns; "
              f"closed-loop |e| max {r['closed_max']} ns")


def legs_case(rule):
    # +20 ppm talker, independent +/-1,426 ns; from 60 s on one PDU lost in
    # every 0.3 s and the talker stepped to +24 ppm; 120 s
    at = 60 * 8_000
    m = Meter("E8", "P2", loss_rule=rule)
    true = int(round(20 * 512))
    sv = Servo(true, random.Random(0xC0FFEE))
    k = 0
    u_at = None
    for n, seq, ts, lost in gen("white", 1426, 20, 120, 4242,
                                loss=f"after:{at}:per:2400:777",
                                fstep=(at, 4.0)):
        if not lost:
            m.pdu(seq, ts)
        if n % WIN_PDU == PHASE_PDU:
            if u_at is None and n >= at:
                u_at = sv.u
            sv.window(k, m.rate, m.valid)
            k += 1
    return (rule, m.restarts, sv.drops, sv.emax, sv.first_lock, u_at, sv.u)


def legs():
    print("== V. the servo row's loss leg: +20 ppm talker, independent "
          "+/-1,426 ns, 120 s; from 60 s one PDU lost in every 0.3 s and the "
          "talker stepped by +4 ppm (2,048 in the servo's units)")
    for rule, rs, dr, em, fl, u0, u1 in pmap(legs_case, ["b", "r3"]):
        print(f"rule={rule:2s} restarts={rs} drops={dr} worst|e|={em} "
              f"first_lock_window={fl} u_at_60s={u0} u_end={u1} "
              f"trim moved {u0 - u1} (step 2048; within 0.5 ppm = 256: "
              f"{'yes' if abs((u0 - u1) - 2048) <= 256 else 'no'})")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, fn in (("bound", bound), ("regress", regress), ("fill", fill),
                     ("p1", p1), ("loss", loss), ("steps", steps),
                     ("tol", tol), ("fstep", fstep), ("legs", legs),
                     ("shapes", shapes)):
        if what in (name, "all"):
            fn()
            print(flush=True)
