#!/usr/bin/env python3
"""Reviewer-owned desk model for PR #631 round 5 (issue #629, lane M1).

Written from the design page at f4f0ecb4 and the servo/receiver RTL it cites
(KL_mmcm_drp_servo.sv: KI_SHIFT 1, KP_SHIFT 2, U_MAX 102,400, SLEW 51,200,
LOCK_THR 1,024, LOCK_WIN 4; ACQUIRE/LOCKED/HOLDOVER at :562-579, the PI run
gate at :613-618, the writeback at :677-697). It is independent of the
author's model: own structure, own seeds, own simplifications (stated per
section). Standard library only, deterministic.

Sections (argv[1]): formula, random, spread, counter, servoleg, meter,
steploop, all.
"""
import math
import random
import sys

# ---------------------------------------------------------------- constants
PDU_NS = 125_000            # 48 kHz base format, 6 samples per PDU
GROUP_S = 0.002             # 16 PDUs
WIN_S = 0.512               # servo window
PPM_NS = 512                # ns per 512 ms window per ppm
KI, KP = 1, 2
U_MAX, SLEW, THR, LOCK_WIN = 102_400, 51_200, 1_024, 4
A0 = round(10.64 * PPM_NS)  # MMCM plan offset, ns per window
HALF = 10_417               # half sample at 48 kHz, ns
ONE = 20_833                # one sample


def clamp(v):
    return max(-U_MAX, min(U_MAX, v))


class PI:
    """The servo's PI and lock count, one call per committed window."""

    def __init__(self):
        self.integ = 0
        self.u = 0
        self.lock_cnt = 0

    def run(self, e):
        e = int(round(e))
        isum = self.integ + (e >> KI)
        ig = clamp(isum)
        ut = clamp(ig + (e >> KP))
        du = ut - self.u
        if du > SLEW:
            self.u += SLEW
        elif du < -SLEW:
            self.u -= SLEW
        else:
            self.u = ut
        self.integ = ig
        if -THR < e < THR:
            self.lock_cnt = min(self.lock_cnt + 1, LOCK_WIN)
        else:
            self.lock_cnt = 0


# ------------------------------------------------------------------ formula
def q_of(p):
    return 1.0 - (1.0 - p) ** 16


def sec_formula():
    print("== formula: restart rate and valid fraction, analytic")
    print("lost/s  p        q         500q^2    500q^2(1-q)  approx_valid  exact_valid")
    for p in (1e-4, 5e-4, 1e-3, 1.4e-3, 2e-3, 3e-3):
        q = q_of(p)
        a = 500 * q * q
        x = a * (1 - q)
        print(f"{8000*p:5.1f}  {p:.1e}  {q:.6f}  {a:.4f}    {x:.4f}       "
              f"{math.exp(-4.096*a):.4f}        {math.exp(-4.096*x):.4f}")
    print("-- loss rate per second at which the exact-rate validity reaches a level")
    for lvl in (0.9, 0.5, 0.1, 0.01):
        lo, hi = 1e-6, 1e-2
        for _ in range(200):
            mid = (lo + hi) / 2
            q = q_of(mid)
            v = math.exp(-4.096 * 500 * q * q * (1 - q))
            if v > lvl:
                lo = mid
            else:
                hi = mid
        print(f"valid {lvl:4.2f} at {8000*lo:5.2f} lost PDUs/s (p = {lo:.3e})")
    print("-- round 4 single-seed rows, 300 s: expected restarts and validity")
    for p in (1e-4, 1e-3):
        q = q_of(p)
        x = 500 * q * q * (1 - q)
        fill = (300 - 4.1) / 300
        print(f"p={p:.0e}: restarts {300*x:.2f}; valid exact x fill "
              f"{math.exp(-4.096*x)*fill:.3f}; approx x fill "
              f"{math.exp(-4.096*500*q*q)*fill:.3f}")
    print("-- round 3 rule (restart on any loss): valid = exp(-4.096 * 8000 p)")
    print(f"p=3e-5 ({8000*3e-5:.2f}/s): {math.exp(-4.096*8000*3e-5):.3f}")
    r1 = math.log(100) / 4.096
    print(f"valid 0.01 at {r1:.3f} lost PDUs/s")


# ------------------------------------------------------------------- random
def voided_groups(rng, q, n_groups):
    """Indices of loss-voided groups, iid Bernoulli(q), by geometric gaps."""
    out = []
    i = -1
    lq = math.log(1.0 - q)
    while True:
        i += 1 + int(math.log(1.0 - rng.random()) / lq)
        if i >= n_groups:
            return out
        out.append(i)


def restart_groups(vo):
    """A run of two or more adjacent voided groups restarts the history at
    the first valid group after it (k >= 3 across the gap)."""
    rs = []
    j = 0
    n = len(vo)
    while j < n:
        s = j
        while j + 1 < n and vo[j + 1] == vo[j] + 1:
            j += 1
        if j > s:                  # run length >= 2
            rs.append(vo[j] + 1)
        j += 1
    return rs


def run_random(p, dur, seed, w0, meas_from=8.4, sigma=None):
    """Group-level model of one seed. Returns (restarts, valid_frac,
    valid_frac_all, lock_time, drops)."""
    rng = random.Random(seed)
    q = q_of(p)
    n_groups = int(dur / GROUP_S)
    vo = voided_groups(rng, q, n_groups)
    rs = [0] + restart_groups(vo)          # cold start: history from group 0
    pick_sd = 1042 / math.sqrt(3) / 4      # mean of 16 uniform(+/-1,042)
    pi = PI()
    state = "ACQUIRE"
    lock_t = None
    drops = 0
    nv = nall = vv = vall = 0
    ri = 0
    ring = [rng.gauss(0, pick_sd) for _ in range(9)]
    a_prev_u = 0
    n = 1
    while True:
        t = w0 + n * WIN_S
        if t > dur:
            break
        g_done = int(t / GROUP_S) - 1      # last group whose pick is complete
        while ri + 1 < len(rs) and rs[ri + 1] <= g_done:
            ri += 1
        valid = (g_done - rs[ri]) >= 2048
        nall += 1
        vall += valid
        if t >= meas_from:
            nv += 1
            vv += valid
        if valid:
            ring = ring[1:] + [rng.gauss(0, pick_sd)]
            r_err = (ring[-1] - ring[0]) / 8
            a = A0 - a_prev_u + rng.uniform(-20, 20)
            pi.run(a - r_err)
            a_prev_u = pi.u
            if state == "ACQUIRE" and pi.lock_cnt >= LOCK_WIN:
                state = "LOCKED"
                if lock_t is None:
                    lock_t = t
            elif state == "LOCKED" and pi.lock_cnt == 0:
                state = "ACQUIRE"
                drops += 1
        n += 1
    return len(rs) - 1, vv / max(nv, 1), vall / max(nall, 1), lock_t, drops


def quantiles(xs):
    xs = sorted(xs)
    n = len(xs)

    def qt(f):
        k = f * (n - 1)
        lo = int(math.floor(k))
        hi = min(lo + 1, n - 1)
        return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)
    return qt(0.5), qt(0.25), qt(0.75), xs[-1]


def sec_random():
    print("== random: independent loss, 32 seeds per rate (group-level model)")
    print("Window phase: first servo boundary at w0 + 0.512 s; w0 = 0.100 s")
    print("calibrates the no-loss cold start to the page's 7.3 s. Rate valid")
    print("when >= 2,048 group intervals since the last restart; LOCKED from")
    print("the PI and lock count of KL_mmcm_drp_servo, an invalid window")
    print("holding both.")
    print("lost/s  restarts/s  valid(>=8.4s)  lock median; q25..q75; max   drops  unlocked")
    for p, dur in ((1e-4, 600), (5e-4, 600), (1e-3, 600), (1.4e-3, 600),
                   (2e-3, 1200), (3e-3, 1200)):
        res = [run_random(p, dur, 428_000 + 97 * s + int(p * 1e7), 0.100)
               for s in range(32)]
        rst = sum(r[0] for r in res) / (32 * dur)
        val = sum(r[1] for r in res) / 32
        locks = [r[3] for r in res if r[3] is not None]
        unl = sum(1 for r in res if r[3] is None)
        drops = sum(r[4] for r in res)
        m, a, b, mx = quantiles(locks)
        print(f"{8000*p:5.1f}   {rst:.4f}      {val:.3f}          "
              f"{m:6.1f}; {a:6.1f}..{b:6.1f}; {mx:6.1f}   {drops}     {unl}")
    print("-- sensitivity: window phase uniform per seed (w0 in 0..0.512 s)")
    for p, dur in ((1e-3, 600), (1.4e-3, 600), (3e-3, 1200)):
        res = []
        for s in range(32):
            ph = random.Random(7_000 + s).uniform(0.0, WIN_S)
            res.append(run_random(p, dur, 529_000 + 31 * s + int(p * 1e7), ph))
        locks = [r[3] for r in res if r[3] is not None]
        m, a, b, mx = quantiles(locks)
        print(f"{8000*p:5.1f}  lock median {m:.1f}; {a:.1f}..{b:.1f}; max {mx:.1f}; "
              f"unlocked {sum(1 for r in res if r[3] is None)}")
    nl = run_random(0.0 + 1e-12, 60, 1, 0.100)
    print(f"no loss: LOCKED at {nl[3]:.3f} s")


def sec_spread():
    print("== spread: one 300 s run at p = 1e-3, validity over all windows, 64 seeds")
    vals = [run_random(1e-3, 300, 900_000 + s, 0.100)[2] for s in range(64)]
    m = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
    print(f"mean {m:.3f}  sd {sd:.3f}  min {min(vals):.3f}  max {max(vals):.3f}")
    vals = [run_random(1e-4, 300, 910_000 + s, 0.100)[2] for s in range(64)]
    m = sum(vals) / len(vals)
    print(f"p = 1e-4: mean {m:.3f}")


# ---------------------------------------------------------- servo SM (1 ms)
def run_servo(variant, level, talker_ppm0=20.0, step_ppm=0.0, leg=(20.0, 80.0),
              period=0.3, end=100.0, w0=0.003):
    """1 ms time-step model of the meter lock, rate validity and the servo
    FSM. variant: 'design' (lock held on a gap, no restart on an isolated
    loss), 'mutant' (lock cleared on a gap; back after 8 PDUs), 'anyloss'
    (restart on any loss; lock held). level: C0, C1 or C2 counters."""
    dt = 0.001
    losses = []
    t = leg[0] + 0.1
    while t < leg[1]:
        losses.append(round(t / dt))
        t += period
    loss_set = set(losses)
    last_restart = 0.0
    lock = False
    lock_back = None
    state = "IDLE"
    pi = PI()
    skip = 0
    win_next = None
    counters = {"UNLOCKED": [], "LOCKED": []}
    prev_level = None
    holdover_entries = 0
    first_lock = None
    leg_u_start = leg_u_end = None
    leg_runs = 0
    n_end = round(end / dt)
    for k in range(n_end + 1):
        t = k * dt
        talker = talker_ppm0 + (step_ppm if t >= leg[0] else 0.0)
        # meter lock: 8 PDUs (1 ms) after the first; mutant clears on a gap
        if not lock and lock_back is None and k == 1:
            lock = True
        if k in loss_set:
            if variant == "mutant":
                lock = False
                lock_back = k + 2         # gap seen at the next PDU, 8 more
            if variant == "anyloss":
                last_restart = t
        if lock_back is not None and k >= lock_back:
            lock = True
            lock_back = None
        # E8 rate: valid 4.096 s after the last restart; the mean talker
        # rate over the last 4.096 s
        valid = (t - last_restart) >= 4.1
        lo, hi = t - 4.096, t
        if hi <= leg[0] or step_ppm == 0.0:
            r_ppm = talker
        elif lo >= leg[0]:
            r_ppm = talker
        else:
            r_ppm = talker_ppm0 + step_ppm * (hi - leg[0]) / 4.096
        # servo FSM (KL_mmcm_drp_servo.sv:538-579)
        if state == "IDLE":
            if lock:
                state = "ACQUIRE"
                win_next = k + round(WIN_S / dt) + round(w0 / dt)
        elif state in ("ACQUIRE", "LOCKED"):
            if not lock:
                state = "HOLDOVER"
                holdover_entries += 1
            elif state == "ACQUIRE" and pi.lock_cnt >= LOCK_WIN:
                state = "LOCKED"
                if first_lock is None:
                    first_lock = t
            elif state == "LOCKED" and pi.lock_cnt == 0:
                state = "ACQUIRE"
        elif state == "HOLDOVER":
            if lock:
                state = "ACQUIRE"
                skip = 2
                pi.lock_cnt = 0
        # window boundary (:603-618) and writeback (:677-697)
        if win_next is not None and k == win_next:
            win_next += round(WIN_S / dt)
            run = skip == 0 and state != "HOLDOVER" and valid
            if skip:
                skip -= 1
            if run:
                a = A0 - pi.u            # audio offset, plant gain 1
                pi.run(a - r_ppm * PPM_NS)
                if leg[0] <= t < leg[1]:
                    leg_runs += 1
        if abs(t - leg[0]) < dt / 2:
            leg_u_start = pi.u
        if abs(t - leg[1]) < dt / 2:
            leg_u_end = pi.u
        # counters
        if level == "C1":
            lv = state == "LOCKED"
        elif level == "C2":
            lv = lock
        else:
            lv = True                     # C0: ~tu, tu constant
        if prev_level is not None and lv != prev_level:
            counters["LOCKED" if lv else "UNLOCKED"].append(round(t, 3))
        prev_level = lv
    trim_ppm = (A0 - leg_u_end) / PPM_NS if leg_u_end is not None else None
    return {"holdover": holdover_entries, "first_lock": first_lock,
            "counters": counters, "u_start": leg_u_start, "u_end": leg_u_end,
            "trim_ppm_end": trim_ppm, "leg_runs": leg_runs,
            "last_loss": losses[-1] * dt, "state_end": state}


def in_leg(ts, leg):
    return [x for x in ts if leg[0] <= x <= leg[1]]


def sec_counter():
    print("== counter: the counter row's 60 s loss leg, one PDU lost in every 0.3 s")
    print("Talker at +20 ppm, no step; leg from 20 s to 80 s, losses from 20.1 s.")
    leg = (20.0, 80.0)
    for variant, level in (("design", "C1"), ("mutant", "C1"), ("design", "C0"),
                           ("design", "C2"), ("anyloss", "C1")):
        r = run_servo(variant, level, leg=leg)
        u = in_leg(r["counters"]["UNLOCKED"], leg)
        lk = in_leg(r["counters"]["LOCKED"], leg)
        after = [x for x in r["counters"]["LOCKED"] if x > leg[1]]
        print(f"{variant:8s} {level}: first LOCKED {r['first_lock']:.3f} s; "
              f"HOLDOVER entries {r['holdover']}; in leg UNLOCKED {len(u)} {u[:2]} "
              f"LOCKED {len(lk)}; LOCKED after leg {after[:1]}; "
              f"last loss {r['last_loss']:.3f}; PI runs in leg {r['leg_runs']}")
        if after:
            print(f"         LOCKED {after[0] - r['last_loss']:.3f} s after the last loss")


def sec_servoleg():
    print("== servoleg: the servo-with-meter row's loss leg, +20 -> +24 ppm at the leg start")
    leg = (20.0, 80.0)
    for variant in ("design", "mutant", "anyloss"):
        r = run_servo(variant, "C1", step_ppm=4.0, leg=leg)
        lost_lock = in_leg(r["counters"]["UNLOCKED"], leg)
        talker_end = 24.0
        trim = (r["u_end"]) / PPM_NS
        # audio offset = A0 - u; follows the talker when A0 - u = talker
        audio_ppm = (A0 - r["u_end"]) / PPM_NS
        print(f"{variant:8s}: LOCKED left in leg at {lost_lock[:1]}; PI runs in leg "
              f"{r['leg_runs']}; audio offset at leg end {audio_ppm:+.2f} ppm "
              f"(talker {talker_end:+.1f}); error {audio_ppm - talker_end:+.2f} ppm")


# -------------------------------------------------------------- meter (PDU)
class Meter:
    """The meter's restart rules at PDU level, as the page states them:
    group = sequence_num[7:4]; pick = mean of ts_i - i * 125,000 over a
    fully received group; deviation |ts_i - ts_0 - i * 125,000| > 4,096 ns
    compared as each PDU arrives, up to a gap (rule 1); adjacent picks
    2 ms +/- 4,096 ns; one voided group between picks (k = 2) 4 ms +/- B2;
    every other k restarts (rule 3)."""

    def __init__(self, b2=5120, nocheck_gap=False, accept_big=False):
        self.b2 = b2
        self.nocheck_gap = nocheck_gap
        self.accept_big = accept_big
        self.prev_seq = None
        self.hi = None
        self.ref = None
        self.sum = 0.0
        self.n = 0
        self.void = False
        self.last = None
        self.last_hi = None
        self.restarts = []

    def restart(self, idx, cause):
        self.restarts.append((idx, cause))

    def pick(self, idx, p, hi):
        if self.last is None:
            self.last, self.last_hi = p, hi
            return
        k = (hi - self.last_hi) & 15
        d = p - self.last
        if k == 1:
            ok = abs(d - 2_000_000) <= 4096
            cause = "spacing"
        elif k == 2:
            ok = self.nocheck_gap or abs(d - 4_000_000) <= self.b2
            cause = "gap-k2"
        else:
            ok = self.accept_big
            cause = f"gap-k{k}"
        if not ok:
            self.restart(idx, cause)
        self.last, self.last_hi = p, hi

    def pdu(self, idx, seq, ts):
        hi, pos = seq >> 4, seq & 15
        gap = self.prev_seq is not None and seq != ((self.prev_seq + 1) & 255)
        if self.prev_seq is None or hi != self.hi:
            # a new group; the old one closed already if it was complete
            self.hi = hi
            self.n = 0
            self.sum = 0.0
            self.void = pos != 0
            self.ref = ts if pos == 0 else None
        elif gap:
            self.void = True              # the PDUs after the gap: not used
        self.prev_seq = seq
        if not self.void:
            dev = ts - self.ref - pos * PDU_NS
            if abs(dev) > 4096:
                self.restart(idx, "deviation")
                self.void = True
                self.last = None          # the next clean pick seeds
                return
            self.sum += ts - pos * PDU_NS
            self.n += 1
            if pos == 15 and self.n == 16:
                self.pick(idx, self.sum / 16, hi)


def feed(meter, n_pdus, ts_fn, lost):
    for i in range(n_pdus):
        if i in lost:
            continue
        meter.pdu(i, i & 255, ts_fn(i))
    return meter.restarts


def sec_meter():
    print("== meter: PDU-level restart rules")
    g0 = 100
    n0 = 16 * g0

    def ts_a(i):                           # +300 ppm, +3,900 ns at lost PDU 0
        return i * PDU_NS * (1 + 300e-6) + (3900 if i >= n0 else 0)

    def ts_b(i):                           # -300 ppm, half sample, +J then -J
        return (i * PDU_NS * (1 - 300e-6) + (HALF - 1426 if i >= n0 else 1426))

    lost = {n0}
    passes = []
    for b2 in range(4096, 8193):
        ra = feed(Meter(b2=b2), 16 * 140, ts_a, lost)
        rb = feed(Meter(b2=b2), 16 * 140, ts_b, lost)
        if len(ra) == 0 and len(rb) == 1:
            passes.append(b2)
    print(f"gap-bound row: (a) and (b) both pass for B2 in "
          f"[{min(passes)}, {max(passes)}], {len(passes)} values, contiguous "
          f"{max(passes) - min(passes) + 1 == len(passes)}")
    for b2 in (4096, 5099, 5100, 5120, 6364, 6365, 6400, 8192):
        ra = feed(Meter(b2=b2), 16 * 140, ts_a, lost)
        rb = feed(Meter(b2=b2), 16 * 140, ts_b, lost)
        print(f"  B2 {b2}: (a) restarts {len(ra)}  (b) restarts {len(rb)}")

    # the step row: 120 cases at the design point
    print("step row: design point +/-1,426 ns independent, +300 ppm")
    tally = {"design": {}, "nocheck": {}}
    total = {"design": 0, "nocheck": 0}
    case = 0
    for place in ("a", "b"):
        positions = range(1, 16) if place == "a" else range(0, 15)
        for pos in positions:
            for step in (ONE, -ONE, HALF, -HALF):
                case += 1
                rng = random.Random(42_800 + case)
                err = [rng.uniform(-1426, 1426) for _ in range(16 * 140)]
                ns = n0 + pos
                lost = {n0} if place == "a" else {n0 + 15}

                def ts(i, err=err, ns=ns, step=step):
                    return (i * PDU_NS * (1 + 300e-6) + err[i]
                            + (step if i >= ns else 0))
                for kind, m in (("design", Meter()),
                                ("nocheck", Meter(nocheck_gap=True))):
                    r = feed(m, 16 * 140, ts, lost)
                    key = (place, len(r), r[0][1] if r else "-")
                    tally[kind][key] = tally[kind].get(key, 0) + 1
                    total[kind] += len(r)
    for kind in ("design", "nocheck"):
        print(f"  {kind}: total restarts {total[kind]} over {case} cases")
        for key in sorted(tally[kind]):
            print(f"    placement {key[0]}, restarts {key[1]}, cause {key[2]}: "
                  f"{tally[kind][key]} cases")

    # no-error baseline: the design point alone restarts nothing
    rng = random.Random(1)
    err = [rng.uniform(-1426, 1426) for _ in range(16 * 2000)]
    r = feed(Meter(), 16 * 2000, lambda i: i * PDU_NS * (1 + 300e-6) + err[i],
             set())
    print(f"design point, no loss, no step, 64 ms x 1000: restarts {len(r)}")
    r = feed(Meter(), 16 * 2000, lambda i: i * PDU_NS * (1 + 300e-6) + err[i],
             set(range(16 * 50, 16 * 2000, 37)))
    print(f"design point, one PDU in 37 lost (isolated): restarts {len(r)}")

    # long gaps and aliasing (0 ppm ideal)
    print("long gaps, from a group's PDU 0 (ideal timestamps, 0 ppm)")
    out = []
    for ng in range(1, 34):
        lost = set(range(n0, n0 + 16 * ng))
        r = feed(Meter(), 16 * (g0 + ng + 40), lambda i: i * PDU_NS, lost)
        out.append(f"{ng}:{len(r)}")
    print("  whole lost groups:restarts " + " ".join(out))
    for start in (0, 5):
        row = []
        for L in (255, 256, 257, 512):
            lost = set(range(n0 + start, n0 + start + L))
            r = feed(Meter(), 16 * (g0 + 80), lambda i: i * PDU_NS, lost)
            row.append(f"{L}:{len(r)}({r[0][1] if r else '-'})")
        print(f"  from PDU {start}: " + " ".join(row))
    # the bound row (+100 ppm, ideal) with the accept-bigger mutant
    print("bound row at +100 ppm, ideal: design / gap of >1 voided group accepted")
    cases = {
        "two lost in adjacent groups": {n0 + 3, n0 + 16 + 3},
        "run of 17": set(range(n0 + 3, n0 + 20)),
        "run of 2 across a boundary": {n0 + 15, n0 + 16},
        "run of 2 inside a group": {n0 + 4, n0 + 5},
        "singles 32 apart for 10 s": set(range(n0, n0 + 80_000, 32)),
    }
    for name, lost in cases.items():
        npd = n0 + 80_000 + 64 if "singles" in name else 16 * 200
        rd = feed(Meter(), npd, lambda i: i * PDU_NS * (1 + 100e-6), lost)
        rm = feed(Meter(accept_big=True), npd,
                  lambda i: i * PDU_NS * (1 + 100e-6), lost)
        print(f"  {name}: {len(rd)} / {len(rm)}")


def sec_steploop():
    print("== steploop: a locked servo, the E8 rate carrying a step for 8 windows")
    print("(the no-check mutant's carried step; window-level PI, plant gain 1)")
    for s in (ONE, -ONE, HALF, -HALF):
        pi = PI()
        a_u = 0
        state = "ACQUIRE"
        drops = 0
        for n in range(40):                # settle and lock on a 0 ppm talker
            a = A0 - a_u
            pi.run(a)
            a_u = pi.u
            if state == "ACQUIRE" and pi.lock_cnt >= LOCK_WIN:
                state = "LOCKED"
        assert state == "LOCKED"
        for n in range(40):
            r_err = s / 8 if n < 8 else 0
            a = A0 - a_u
            pi.run(a - r_err)
            a_u = pi.u
            if state == "ACQUIRE" and pi.lock_cnt >= LOCK_WIN:
                state = "LOCKED"
            elif state == "LOCKED" and pi.lock_cnt == 0:
                state = "ACQUIRE"
                drops += 1
        print(f"step {s:+6d} ns: LOCKED drops {drops}; final state {state}")


def sec_medians():
    print("== medians: how far a 32-seed cold-start median moves (256 seeds,")
    print("window phase uniform per seed; 32-seed medians from 8 disjoint blocks)")
    for p, dur in ((1e-3, 600), (1.4e-3, 600), (3e-3, 1200)):
        locks = []
        for s in range(256):
            ph = random.Random(17_000 + s).uniform(0.0, WIN_S)
            r = run_random(p, dur, 733_000 + 13 * s + int(p * 1e7), ph)
            locks.append(r[3] if r[3] is not None else float("inf"))
        m, a, b, mx = quantiles(locks)
        blocks = [quantiles(locks[i:i + 32])[0] for i in range(0, 256, 32)]
        print(f"{8000*p:5.1f}/s: 256-seed median {m:.1f} s ({a:.1f}..{b:.1f}); "
              f"32-seed block medians {min(blocks):.1f}..{max(blocks):.1f} s; "
              f"unlocked {sum(1 for x in locks if x == float('inf'))}")


SECTIONS = {"formula": sec_formula, "random": sec_random, "spread": sec_spread,
            "medians": sec_medians,
            "counter": sec_counter, "servoleg": sec_servoleg,
            "meter": sec_meter, "steploop": sec_steploop}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, fn in SECTIONS.items():
        if which in ("all", name):
            fn()
