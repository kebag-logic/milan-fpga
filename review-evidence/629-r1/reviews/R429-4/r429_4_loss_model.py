#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent reviewer model (R429-4) of the #629 AAF meter's round-4 loss rule.

Written from the page text at 1bdd6895 (docs/design/MEDIA_CLOCK_FOLLOWING.md,
"The pick", "The jump bound", "The rate estimator", "Lost PDUs") and from
hdl/ieee1722/crf/KL_mmcm_drp_servo.sv (PI shifts, clamps, slew, lock rule,
hold on an invalid rate). Standard library only, deterministic seeds.

Usage: python3 r429_4_loss_model.py [section ...]   (default: all sections)
"""
import math
import random
import sys

PDU_NS = 125_000            # 6 samples at 48 kHz
GRP = 16                    # PDUs per group
GRP_NS = GRP * PDU_NS       # 2 ms
SNAP = 256                  # group intervals per snapshot (512 ms)
NSNAP = 8                   # E8
WIN_NS = 512_000_000
B1 = 4096                   # adjacent pick spacing bound
B2 = 5120                   # spacing bound across one voided group
DEV = 4096                  # in-group deviation bound
M32 = 1 << 32


def s32(x):
    x &= M32 - 1
    return x - M32 if x >= 1 << 31 else x


# ---------------------------------------------------------------- talker
def talker(n_pdu, ppm, err_fn, t0=1_000_000_000, step=None):
    """Return per-PDU presentation times (mod 2^32) for PDU 0..n_pdu-1.
    err_fn(n) gives the timestamp error of PDU n in ns (float).
    step: (pdu_index, size_ns) adds size_ns to every PDU from pdu_index on."""
    sp = PDU_NS * (1 + ppm * 1e-6)
    out = []
    for n in range(n_pdu):
        t = t0 + n * sp + err_fn(n)
        if step is not None and n >= step[0]:
            t += step[1]
        out.append(int(math.floor(t)) & (M32 - 1))
    return out


# ---------------------------------------------------------------- meter
class Meter:
    """The page's meter rules. variant keys:
      loss_rule      'b' (round 4) | 'restart' (round 3: any loss restarts)
      cross_check    True | False (mutant: no check across a gap)
      max_k          2 (page) | 99 (mutant: any gap accepted with a k-scaled bound)
      fill           'mid' (page) | 'next_less_2ms' (mutant) | 'restart' (mutant)
      dev_in_lossy   False: a loss-voided group is not deviation-checked
                     True : its received PDUs are checked against ts_0 (if received)
    """

    def __init__(self, **v):
        self.v = dict(loss_rule='b', cross_check=True, max_k=2, fill='mid',
                      dev_in_lossy=False)
        self.v.update(v)
        self.restarts = 0
        self.loss_voids = 0
        self.dev_voids = 0
        self.fills = 0
        self.events = []   # (pdu_index_of_update, rate or None) ; None = invalid
        self._restart_history(first=True)

    def _restart_history(self, first=False):
        if not first:
            self.restarts += 1
        self.last_pick = None      # (group_index, pick)
        self.count = 0
        self.snaps = []
        self.valid = False

    def _emit(self, at, rate):
        self.events.append((at, rate))

    def run(self, ts, lost):
        """ts: list of timestamps; lost: set of PDU indices not received."""
        n = len(ts)
        ngrp = n // GRP
        for g in range(ngrp):
            base = g * GRP
            got = [i for i in range(GRP) if (base + i) not in lost]
            at = base + GRP - 1
            if len(got) < GRP:
                self.loss_voids += 1
                if self.v['loss_rule'] == 'restart':
                    if self.valid or self.last_pick is not None:
                        self._restart_history()
                        self._emit(at, None)
                    continue
                if self.v['dev_in_lossy'] and 0 in got:
                    t0 = ts[base]
                    bad = any(abs(s32(ts[base + i] - t0 - i * PDU_NS)) > DEV for i in got)
                    if bad:
                        self.dev_voids += 1
                        self._restart_history()
                        self._emit(at, None)
                continue
            t0 = ts[base]
            devs = [s32(ts[base + i] - t0 - i * PDU_NS) for i in range(GRP)]
            if max(abs(d) for d in devs) > DEV:
                self.dev_voids += 1
                self._restart_history()
                self._emit(at, None)
                continue
            pick = (t0 + (sum(devs) // GRP)) & (M32 - 1)
            self._take_pick(g, pick, at)
        return self

    def _take_pick(self, g, pick, at):
        if self.last_pick is None:
            self.last_pick = (g, pick)
            self.count = 0
            self.snaps = [pick]
            return
        g0, p0 = self.last_pick
        k = (g - g0) % 16                    # from sequence_num[7:4]
        d = s32(pick - p0)
        ok = False
        if k == 1:
            ok = abs(d - GRP_NS) <= B1
        elif k == 2:
            ok = (not self.v['cross_check']) or abs(d - 2 * GRP_NS) <= B2
        elif 3 <= k <= self.v['max_k']:
            ok = (not self.v['cross_check']) or abs(d - k * GRP_NS) <= (B1 + (k - 1) * 1024)
        if not ok:
            self._restart_history()
            self._emit(at, None)
            self.last_pick = (g, pick)
            self.count = 0
            self.snaps = [pick]
            return
        prev = self.count
        self.count += k
        # snapshot points crossed (multiples of SNAP in (prev, count])
        m_lo = prev // SNAP + 1
        m_hi = self.count // SNAP
        for m in range(m_lo, m_hi + 1):
            pt = m * SNAP
            if pt == self.count:
                snap = pick
            else:
                # the snapshot group was voided: fill
                self.fills += 1
                if self.v['fill'] == 'mid':
                    snap = (p0 + (s32(pick - p0) >> 1)) & (M32 - 1)
                elif self.v['fill'] == 'next_less_2ms':
                    snap = (pick - (self.count - pt) * GRP_NS) & (M32 - 1)
                else:  # 'restart'
                    self._restart_history()
                    self._emit(at, None)
                    self.last_pick = (g, pick)
                    self.count = 0
                    self.snaps = [pick]
                    return
            self.snaps.append(snap)
            if len(self.snaps) > NSNAP:
                old = self.snaps[-1 - NSNAP]
                rate = s32(snap - old - NSNAP * WIN_NS) >> 3
                self.valid = True
                self._emit(at, rate)
            if len(self.snaps) > NSNAP + 1:
                self.snaps = self.snaps[-(NSNAP + 1):]
        self.last_pick = (g, pick)


# ---------------------------------------------------------------- servo
def servo(events, n_pdu, true_rate, plant_gain=1.0, phase_pdu=1000, d0=15_000,
          qseed=7, qamp=20, base=None):
    """Window-level model of KL_mmcm_drp_servo's ACQUIRE/LOCKED PI.
    events: meter (pdu_index, rate|None). The servo samples the held rate at
    each window boundary (every 4096 PDUs, offset phase_pdu). true_rate(pdu)
    is the talker's true rate in ns per window; base (default: the true rate at
    PDU 0) is subtracted from every rate so the trim stays inside +/-200 ppm:
    the model is relative, as the 300 ppm of the bound is mostly the PHC's.
    d0 is the local plan's offset (ns per window).
    Returns dict: first_lock_s, drops, worst_e_after_lock, valid_frac, trim_err."""
    rq = random.Random(qseed)
    u = 0
    integ = 0
    lock_cnt = 0
    state = 'ACQ'
    first_lock = None
    drops = 0
    worst = 0
    nwin = 0
    nvalid = 0
    held = None
    ei = 0
    ev = sorted(events)
    WIN_PDU = 4096
    if base is None:
        base = true_rate(0)
    b = phase_pdu
    while b < n_pdu:
        while ei < len(ev) and ev[ei][0] <= b:
            held = ev[ei][1]
            ei += 1
        nwin += 1
        locerr = int(round(d0 - plant_gain * u)) + rq.randint(-qamp, qamp)
        if held is not None:
            nvalid += 1
            e = locerr - (held - base)
            integ_n = max(-102_400, min(102_400, integ + (e >> 1)))
            un = max(-102_400, min(102_400, integ_n + (e >> 2)))
            du = un - u
            if du > 51_200:
                u += 51_200
            elif du < -51_200:
                u -= 51_200
            else:
                u = un
            integ = integ_n
            if -1024 < e < 1024:
                lock_cnt = min(4, lock_cnt + 1)
            else:
                lock_cnt = 0
            if state == 'LOCKED':
                worst = max(worst, abs(e))
            if state == 'ACQ' and lock_cnt >= 4:
                state = 'LOCKED'
                if first_lock is None:
                    first_lock = b * PDU_NS / 1e9
            elif state == 'LOCKED' and lock_cnt == 0:
                state = 'ACQ'
                drops += 1
        b += WIN_PDU
    trim_err = (d0 - (true_rate(n_pdu - 1) - base)) / plant_gain - u   # ns/window of residual
    return dict(first_lock_s=first_lock, drops=drops, worst=worst,
                valid_frac=nvalid / max(1, nwin), trim_err_ppm=trim_err / 512.0,
                state=state)


# ---------------------------------------------------------------- errors
def err_independent(J, seed):
    r = random.Random(seed)
    cache = {}

    def f(n):
        if n not in cache:
            cache[n] = r.uniform(-J, J)
        return cache[n]
    return f


def err_group_sign(J, seed):
    r = random.Random(seed)
    cache = {}

    def f(n):
        g = n // GRP
        if g not in cache:
            cache[g] = J if r.random() < 0.5 else -J
        return cache[g]
    return f


def loop_impulse(n=200, gain=1.0):
    """Response of e to a unit estimator error, PI one window late (real valued)."""
    h = []
    integ = 0.0
    u = 0.0
    for k in range(n):
        eps = 1.0 if k == 0 else 0.0
        e = -gain * u - eps
        integ += e / 2
        u = integ + e / 4
        h.append(e)
    return h


def err_worst_e8(J, target_win=150, gain=1.0):
    """+/-J held per 512 ms block, signs chosen so the E8 rate error drives |e|
    to its maximum at window target_win."""
    h = loop_impulse(400, gain)
    c = [h[j] - (h[j - 8] if j >= 8 else 0.0) for j in range(400)]
    signs = {}
    for j in range(400):
        blk = target_win - j
        if blk >= 0:
            signs[blk] = 1 if c[j] >= 0 else -1

    def f(n):
        blk = n // (SNAP * GRP)
        return J * signs.get(blk, 1)
    return f, sum(abs(x) for x in c) / 8


# ---------------------------------------------------------------- sections
def periodic_loss(n_pdu, every_pdu, phase=37):
    return set(range(phase, n_pdu, every_pdu))


def sec_bound_table(out):
    out.append('== bound table: 2J + 601k <= B_k < 10417 - 2J - 601k, J = 1426')
    J = 1426
    for k in range(1, 6):
        lo = 2 * J + 601 * k
        hi = 20833.33 / 2 - 2 * J - 601 * k
        out.append(f'k={k} lo={lo} hi<{hi:.2f} window={"yes" if lo < hi else "none"}')
    # exact rate term: 300 ppm over k*2 ms
    for k in (1, 2):
        rt = 300e-6 * k * GRP_NS
        out.append(f'k={k} rate term at 300 ppm = {rt:.1f} ns; tolerance J at 300 ppm <= {((B1 if k == 1 else B2) - rt) / 2:.1f}, at 0 ppm <= {(B1 if k == 1 else B2) / 2:.1f}')


def sec_random_loss(out):
    out.append('== random loss: restarts per second 500 q^2, q = 1-(1-p)^16; Poisson valid fraction exp(-lambda*4.096)')
    for p in (3e-5, 1e-4, 1e-3, 1.4e-3, 3e-3):
        q = 1 - (1 - p) ** 16
        lam = 500 * q * q
        out.append(f'p={p:g} lost/s={8000 * p:.2f} restarts/s={lam:.4f} mean interval={1 / lam:.1f}s valid~{math.exp(-lam * 4.096):.3f}')
    # simulate p = 1e-3 and 1.4e-3 for 300 s
    for p, seed in ((1e-4, 11), (1e-3, 12), (1.4e-3, 13)):
        n = 8000 * 300
        r = random.Random(seed)
        lost = {i for i in range(n) if r.random() < p}
        ts = talker(n, 0, err_independent(1042, seed + 100))
        m = Meter().run(ts, lost)
        sv = servo(m.events, n, lambda b: 0)
        out.append(f'sim p={p:g} 300s: restarts={m.restarts} valid_frac={sv["valid_frac"]:.3f} drops={sv["drops"]} first_lock={sv["first_lock_s"]}')


def sec_validity_region(out):
    out.append('== validity region: every pair of losses shares a group or is >= 32 PDUs apart')
    # exhaustive two-loss patterns over a 64-PDU window at every offset, ideal ts
    n = 8000 * 6
    bad_ge32 = 0
    first_bad_lt32 = None
    for gap in range(1, 40):
        for ph in range(GRP):
            a = 4096 * 5 // 1 - 200 + ph   # inside the valid region
            lost = {a, a + gap}
            m = Meter().run(talker(n, 100, lambda k: 0.0), lost)
            same_grp = (a // GRP) == ((a + gap) // GRP)
            if m.restarts:
                if gap >= 32 or same_grp:
                    bad_ge32 += 1
                elif first_bad_lt32 is None or gap > first_bad_lt32:
                    first_bad_lt32 = gap
    out.append(f'patterns with gap>=32 or same group that restarted: {bad_ge32}')
    out.append(f'largest gap (<32, different groups) that restarts at some phase: {first_bad_lt32}')


def run_case(args):
    (name, J, ppm, shape, loss, variant, secs, seed) = args
    n = 8000 * secs
    if shape == 'ind':
        ef = err_independent(J, seed)
    elif shape == 'grp':
        ef = err_group_sign(J, seed)
    elif shape == 'worst':
        ef, _ = err_worst_e8(J, target_win=150)
    else:
        ef = lambda k: 0.0
    if loss == 'none':
        lost = set()
    elif loss == '1s':
        lost = periodic_loss(n, 8000)
    elif loss == '0.3s':
        lost = periodic_loss(n, 2400)
    elif loss == 'snap':
        lost = set(range(SNAP * GRP + 5, n, SNAP * GRP))   # PDU 5 of every snapshot group (counting from history start)
    elif loss == '32':
        lost = periodic_loss(n, 32, phase=3)
    elif loss == '5s':
        lost = periodic_loss(n, 40000)
    ts = talker(n, ppm, ef)
    m = Meter(**variant).run(ts, lost)
    true = -(ppm * 1e-6) * 0  # rates compared to the planted rate below
    planted = s32(int(round(NSNAP * WIN_NS * (1 + ppm * 1e-6))) - NSNAP * WIN_NS) >> 3
    rates = [r for _, r in m.events if r is not None]
    worst_rate_err = max((abs(r - planted) for r in rates), default=None)
    sv = servo(m.events, n, lambda b: planted)
    first_valid = next((at for at, r in m.events if r is not None), None)
    fell = False
    seen = False
    for at, r in m.events:
        if r is not None:
            seen = True
        elif seen:
            fell = True
    return (name, m.restarts, m.loss_voids, m.fills, len(rates), worst_rate_err,
            None if first_valid is None else first_valid * PDU_NS / 1e9, fell,
            sv['first_lock_s'], sv['drops'], sv['worst'], round(sv['valid_frac'], 3))


def sec_loss_table(out, pool):
    out.append('== loss table: name restarts loss_voids fills n_rates worst_rate_err_vs_planted first_valid_s valid_fell first_lock_s drops worst_e valid_frac')
    cases = []
    for shape in ('ind', 'grp'):
        for loss in ('none', '1s', '0.3s', 'snap', '32'):
            for rule in ('b', 'restart'):
                cases.append((f'{shape} J1426 300ppm loss={loss} rule={rule}', 1426, 300, shape,
                              loss, dict(loss_rule=rule), 120, 5))
    cases.append(('worst J1426 0ppm loss=none', 1426, 0, 'worst', 'none', {}, 120, 5))
    cases.append(('worst J1426 0ppm loss=snap', 1426, 0, 'worst', 'snap', {}, 120, 5))
    cases.append(('worst J1426 0ppm loss=0.3s', 1426, 0, 'worst', '0.3s', {}, 120, 5))
    cases.append(('ideal 0ppm loss=5s rule=restart', 0, 0, 'ideal', '5s', dict(loss_rule='restart'), 120, 5))
    for r in pool(run_case, cases):
        out.append(' | '.join(str(x) for x in r))


def sec_fill(out):
    out.append('== snapshot fill: ideal ts at +100 ppm, PDU 5 of the snapshot group at 3 x 512 ms lost (history from group 0)')
    n = 8000 * 30
    ts = talker(n, 100, lambda k: 0.0)
    ref = Meter().run(ts, set())
    lost = {3 * SNAP * GRP + 5}
    for fill in ('mid', 'next_less_2ms', 'restart'):
        m = Meter(fill=fill).run(ts, lost)
        r0 = [r for _, r in ref.events if r is not None]
        r1 = [r for _, r in m.events if r is not None]
        diffs = [abs(a - b) for a, b in zip(r0, r1)]
        out.append(f'fill={fill}: restarts={m.restarts} fills={m.fills} n_rates ref/loss={len(r0)}/{len(r1)} '
                   f'max|diff|={max(diffs) if diffs else None} rates_off_by_gt1={sum(1 for d in diffs if d > 1)}')
    # midpoint exactness for any rate: sweep ppm
    worst = 0
    for ppm in (-300, -100, -10.64, 0, 37.3, 100, 300):
        ts = talker(n, ppm, lambda k: 0.0)
        a = [r for _, r in Meter().run(ts, set()).events if r is not None]
        b = [r for _, r in Meter().run(ts, {3 * SNAP * GRP + 5, 9 * SNAP * GRP + 15}).events if r is not None]
        worst = max(worst, max(abs(x - y) for x, y in zip(a, b)))
    out.append(f'midpoint fill, ideal ts at 7 rates from -300 to +300 ppm: max rate diff vs no loss = {worst} LSB')


def sec_bound_rows(out):
    out.append('== bound rows: ideal ts at +100 ppm, 10 s')
    n = 8000 * 10
    ts = talker(n, 100, lambda k: 0.0)
    a = 4096 * 6 + 3 * GRP
    pats = {
        'two losses in adjacent groups': {a + 5, a + GRP + 9},
        'run of 17': set(range(a + 2, a + 19)),
        'run of 2 across a group boundary': {a + 15, a + 16},
        'run of 2 inside a group': {a + 6, a + 7},
        'singles 32 PDUs apart for 10 s': set(range(7, n, 32)),
    }
    for name, lost in pats.items():
        r_page = Meter().run(ts, lost).restarts
        r_mut = Meter(max_k=99).run(ts, lost).restarts
        out.append(f'{name}: restarts page={r_page} mutant(any gap accepted)={r_mut}')


def step_case(args):
    (size, pos, variant, seed, J) = args[:5]
    late = len(args) > 5 and args[5]
    n = 8000 * 30
    g = (40 if late else 6) * SNAP + 37   # 3.1 s (before lock) or 20.5 s (after lock)
    step_pdu = g * GRP + pos
    lost_pdu = g * GRP + (15 if pos != 15 else 0)
    ts = talker(n, 300, err_independent(J, seed), step=(step_pdu, size))
    m = Meter(**variant).run(ts, {lost_pdu})
    rates = [r for _, r in m.events if r is not None]
    planted = s32(int(round(NSNAP * WIN_NS * (1 + 300e-6))) - NSNAP * WIN_NS) >> 3
    sv = servo(m.events, n, lambda b: planted)
    return (size, pos, m.restarts, m.dev_voids, max(abs(r - planted) for r in rates), sv['drops'])


def sec_steps(out, pool):
    out.append('== steps inside a loss-voided group (loss at PDU 15, or PDU 0 when the step is at 15), J=1426 independent, 300 ppm, 30 s')
    sizes = (20833, -20833, 10417, -10417)
    for label, variant in (('page, no deviation check in a lossy group', {}),
                           ('page, deviation checked on received PDUs of a lossy group', dict(dev_in_lossy=True)),
                           ('mutant: no check across the gap', dict(cross_check=False)),
                           ('mutant: no cross check, deviation checked in lossy group', dict(cross_check=False, dev_in_lossy=True))):
        res = pool(step_case, [(s, p, variant, 900 + p, 1426) for s in sizes for p in range(16)])
        once = sum(1 for r in res if r[2] == 1)
        none = sum(1 for r in res if r[2] == 0)
        drops = sum(r[5] for r in res)
        drop_cases = sum(1 for r in res if r[5] > 0)
        out.append(f'{label}: restart exactly once {once}/64, none {none}/64, servo drops total {drops} in {drop_cases} cases')
        res2 = pool(step_case, [(s, p, variant, 900 + p, 1426, True) for s in sizes for p in range(16)])
        out.append(f'   step after first LOCKED (20.5 s): restart once {sum(1 for r in res2 if r[2] == 1)}/64, '
                   f'none {sum(1 for r in res2 if r[2] == 0)}/64, servo drops total {sum(r[5] for r in res2)} '
                   f'in {sum(1 for r in res2 if r[5] > 0)} cases, worst rate error {max(r[4] for r in res2)} ns')
        if 'mutant' in label:
            pos_restart = sorted({r[1] for r in res if r[2] > 0})
            out.append(f'   positions still restarting under the mutant: {pos_restart}')


def sec_tolerance_gap(out):
    out.append('== tolerance across one voided group, worst correlated shape (+J before the gap, -J after), ideal otherwise')
    n = 8000 * 8
    g = 3 * SNAP + 11
    for ppm, Js in ((300, (1940, 1955, 1965, 1980)), (0, (2540, 2555, 2565, 2580))):
        for J in Js:
            # pick g-1 at +J, group g voided (loss), pick g+1 at -J (spacing shrinks by 2J), rest 0
            def ef(k, J=J):
                gg = k // GRP
                if gg == g - 1:
                    return -J if ppm > 0 else J
                if gg == g + 1:
                    return J if ppm > 0 else -J
                return 0.0
            ts = talker(n, ppm, ef)
            m = Meter().run(ts, {g * GRP + 4})
            out.append(f'ppm={ppm} J={J}: restarts={m.restarts}')


def sec_closed_loop(out):
    out.append('== closed loop: l1 gain of estimator error -> e, and E8 worst-case coefficient')
    for gain in (0.8, 1.0, 1.2):
        h = loop_impulse(400, gain)
        l1 = sum(abs(x) for x in h)
        c = sum(abs(h[j] - (h[j - 8] if j >= 8 else 0.0)) for j in range(400)) / 8
        out.append(f'plant gain {gain}: l1={l1:.4f}  E8 coefficient={c:.4f}  at J=1426: {c * 1426:.0f} ns  bound 2*l1/8*J={2 * l1 / 8 * 1426:.0f} ns')


def sec_fill_closed_loop(out):
    out.append('== closed loop, worst E8 shape at J=1426, with and without fills (every snapshot group loses PDU 5), servo phase sweep')
    n = 8000 * 120
    ef, coef = err_worst_e8(1426, target_win=150)
    ts = talker(n, 0, ef)
    for lossname, lost in (('none', set()), ('every snapshot group', set(range(SNAP * GRP + 5, n, SNAP * GRP)))):
        worst = 0
        drops = 0
        for ph in (1, 15, 16, 17, 33, 1000, 2048, 4000):
            m = Meter().run(ts, lost)
            sv = servo(m.events, n, lambda b: 0, phase_pdu=ph)
            worst = max(worst, sv['worst'])
            drops += sv['drops']
        out.append(f'loss={lossname}: worst |e| after lock over 8 phases = {worst} ns, drops={drops}, restarts={m.restarts}, fills={m.fills}')


def sec_servo_row(out):
    out.append('== servo row loss leg: +20 ppm, independent J=1426, one PDU lost every 0.3 s, talker stepped to +24 ppm at leg start (60 s leg after 60 s settle)')
    n = 8000 * 120
    step_pdu = 8000 * 60
    base = err_independent(1426, 77)
    sp20 = PDU_NS * (1 + 20e-6)
    sp24 = PDU_NS * (1 + 24e-6)
    ts = []
    for k in range(n):
        if k < step_pdu:
            t = 1e9 + k * sp20
        else:
            t = 1e9 + step_pdu * sp20 + (k - step_pdu) * sp24
        ts.append(int(math.floor(t + base(k))) & (M32 - 1))
    r20 = s32(int(round(NSNAP * WIN_NS * (1 + 20e-6))) - NSNAP * WIN_NS) >> 3
    r24 = s32(int(round(NSNAP * WIN_NS * (1 + 24e-6))) - NSNAP * WIN_NS) >> 3
    true = lambda b: r20 if b < step_pdu else r24
    lost = set(range(step_pdu + 101, n, 2400))
    for rule in ('b', 'restart'):
        m = Meter(loss_rule=rule).run(ts, lost)
        sv = servo(m.events, n, true)
        out.append(f'rule={rule}: restarts={m.restarts} first_lock={sv["first_lock_s"]} drops={sv["drops"]} worst_e={sv["worst"]} '
                   f'trim residual at end={sv["trim_err_ppm"]:.2f} ppm state={sv["state"]}')


def sec_s1(out):
    out.append('== S1: set of rates consistent with error-free data of slope s under +/-J error over span T')
    J = 1042.0
    T = 512e6
    # brute: rate r is consistent iff a ramp (s-r)x + c fits inside +/-J on [0, T]: |s-r| T <= 2J
    lo = -2 * J / T
    hi = 2 * J / T
    out.append(f'consistent rate offsets: [{lo * T:.0f}, {hi * T:.0f}] ns per window; minimax error = {hi * T:.0f} ns/window = {hi * 1e6:.2f} ppm; pairwise J/T = {J:.0f} ns/window = {J / T * 1e6:.3f} ppm')
    # two-point attains 2J/T; LS slope worst case 3J/T (continuous limit)
    N = 4096
    xs = [i * T / (N - 1) for i in range(N)]
    xm = sum(xs) / N
    sxx = sum((x - xm) ** 2 for x in xs)
    ls = sum(abs(x - xm) for x in xs) / sxx * J
    out.append(f'two-point worst = {2 * J:.0f} ns/window; least-squares worst = {ls * T:.0f} ns/window ({ls * T / J:.3f} J)')


SECTIONS = ['bound_table', 'random_loss', 'validity_region', 'fill', 'bound_rows', 'tolerance_gap',
            'closed_loop', 'fill_closed_loop', 'servo_row', 's1', 'steps', 'loss_table']


def main():
    want = sys.argv[1:] or SECTIONS
    import multiprocessing as mp
    with mp.Pool(8) as p:
        pool = lambda f, xs: p.map(f, xs)
        out = []
        for s in want:
            fn = globals()['sec_' + s]
            if s == 'fstep':
                fn(out)
            elif s in ('loss_table', 'steps'):
                fn(out, pool)
            else:
                fn(out)
            print('\n'.join(out), flush=True)
            out = []



def fstep_case(args):
    dppm, ph = args
    n = 8000 * 40
    sp0 = PDU_NS
    sp1 = PDU_NS * (1 + dppm * 1e-6)
    sp_at = 8000 * 20 + ph * 256       # 16 phases across one 4096-PDU window
    ts = []
    for k in range(n):
        t = 1e9 + (k * sp0 if k < sp_at else sp_at * sp0 + (k - sp_at) * sp1)
        ts.append(int(math.floor(t)) & (M32 - 1))
    r1 = s32(int(round(NSNAP * WIN_NS * (1 + dppm * 1e-6))) - NSNAP * WIN_NS) >> 3
    m = Meter().run(ts, set())
    sv = servo(m.events, n, lambda b: 0 if b < sp_at else r1, base=0, qamp=0)
    return (dppm, ph, sv['drops'])


def sec_fstep(out):
    out.append('== talker frequency step after lock, ideal timestamps, E8, 16 phases across one servo window: phases with a LOCKED drop')
    import multiprocessing as mp
    with mp.Pool(8) as p:
        for d in (4, 7, 7.5, 8, 8.5, 9):
            res = p.map(fstep_case, [(d, ph) for ph in range(16)])
            out.append(f'step {d} ppm: phases dropping LOCKED {sum(1 for r in res if r[2] > 0)}/16')


SECTIONS.append('fstep')

if __name__ == '__main__':
    main()
