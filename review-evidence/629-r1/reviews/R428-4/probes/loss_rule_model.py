#!/usr/bin/env python3
"""Reviewer's independent desk model of the #629 AAF meter loss rule (PR #631,
design page docs/design/MEDIA_CLOCK_FOLLOWING.md, section "Lost PDUs"), written
from the page's text only. Standard library only, deterministic seeds.

Rules modelled (as the page states them):
  * PDU n has sequence_num n mod 256 and a 32-bit timestamp; nominal spacing
    125,000 ns at the talker's rate; groups of 16 by sequence_num mod 16.
  * A fully received group: deviation d_i = ts_i - ts_0 - i*125,000; any
    |d_i| > 4,096 is a deviation void and restarts the history; otherwise the
    pick is ts_0 + floor(sum d_i / 16) mod 2^32.
  * A group missing any PDU is a loss void: it restarts nothing.
  * The next valid pick is checked against the last one across k group
    intervals, k = (seq[7:4] difference) mod 16: k = 1 needs 2 ms +/- 4,096 ns,
    k = 2 needs 4 ms +/- 5,120 ns, any other k (including 0) restarts.
  * The history counts group intervals k at a time from its first pick; a
    snapshot is written when the count reaches a multiple of 256, or, when the
    count steps over one (the snapshot group was loss-voided), the midpoint
    last + ((new - last) >> 1) mod 2^32 is written.
  * E8: rate = (S_now - S_8_ago - 4,096,000,000) >> 3 (signed, mod 2^32), valid
    once the count has reached 2,048.
Mutants: restart on any loss (round 3); no check across a gap; k >= 3 accepted
(k-scaled bound); fill taken as the next pick less 2 ms; a voided snapshot
group restarting the history; a wider k = 2 bound.
"""
import math, random, sys

M32 = 1 << 32
NOM = 125_000
HALF = 10_417
ONE = 20_833


def s32(x):
    x &= M32 - 1
    return x - M32 if x >= 1 << 31 else x


class Meter:
    def __init__(self, mutant=None, b1=4096, b2=5120):
        self.mut = mutant
        self.b1, self.b2 = b1, b2
        self.restarts = 0
        self.fills = 0
        self.rates = []          # (group index, rate) for each valid rate update
        self._restart(None)

    def _restart(self, why):
        if why is not None:
            self.restarts += 1
        self.last = None         # (group index, pick)
        self.count = 0
        self.snaps = []          # snapshot values, oldest first

    def _snapshot(self, g, val):
        self.snaps.append(val)
        if len(self.snaps) > 9:
            self.snaps.pop(0)
        if self.count >= 2048 and len(self.snaps) == 9:
            r = s32(val - self.snaps[0] - 4_096_000_000) >> 3
            self.rates.append((g, r))

    def group(self, g, ts, received):
        """g: absolute group index; ts: 16 timestamps; received: 16 flags."""
        if not all(received):
            if self.mut == "restart_any_loss":
                self._restart("loss")
            return
        d = [s32(ts[i] - ts[0] - i * NOM) for i in range(16)]
        if any(abs(x) > 4096 for x in d):
            self._restart("deviation")
            return
        pick = (ts[0] + (sum(d) // 16)) % M32
        if self.last is None:
            self.last = (g, pick)
            self.count = 0
            self._snapshot(g, pick)
            return
        gl, pl = self.last
        k = (g - gl) % 16            # what seq[7:4] can show
        sp = s32(pick - pl)
        ok = False
        if k == 1:
            ok = abs(sp - 2_000_000) <= self.b1
        elif k == 2:
            if self.mut == "no_gap_check":
                ok = True
            else:
                ok = abs(sp - 4_000_000) <= self.b2
        elif k >= 3 and self.mut == "accept_k3":
            ok = abs(sp - k * 2_000_000) <= self.b1 + (k - 1) * 1024
        elif k >= 3 and self.mut == "no_gap_check":
            ok = True
        if not ok:
            self._restart("spacing")
            self.last = (g, pick)
            self._snapshot(g, pick)
            return
        prev = self.count
        self.count += k
        if self.count // 256 > prev // 256 and self.count % 256 != 0:
            # the snapshot point was stepped over: the snapshot group was voided
            if self.mut == "voided_snapshot_restarts":
                self._restart("snapshot")
                self.last = (g, pick)
                self._snapshot(g, pick)
                return
            self.fills += 1
            if self.mut == "fill_next_less_2ms":
                fill = (pick - 2_000_000) % M32
            else:
                fill = (pl + (s32(pick - pl) >> 1)) % M32
            self._snapshot(g, fill)
        if self.count % 256 == 0:
            self._snapshot(g, pick)
        self.last = (g, pick)


def run(n_groups, ppm=0.0, err=None, lost=frozenset(), mutant=None, step=None,
        b2=5120, t0=123_456_789):
    """err(n) -> ns error of PDU n; step = (pdu index, ns) added from there on."""
    m = Meter(mutant, b2=b2)
    per = NOM / (1.0 + ppm * 1e-6)
    for g in range(n_groups):
        ts, rx = [], []
        for i in range(16):
            n = g * 16 + i
            t = t0 + n * per + (err(n) if err else 0.0)
            if step and n >= step[0]:
                t += step[1]
            ts.append(int(math.floor(t)) % M32)
            rx.append(n not in lost)
        m.group(g, ts, rx)
    return m


def shape(kind, J, seed):
    rng = random.Random(seed)
    cache = {}
    if kind == "independent":
        return lambda n: cache.setdefault(n, rng.uniform(-J, J))
    if kind == "random_sign_group":
        return lambda n: cache.setdefault(n // 16, J if rng.random() < 0.5 else -J)
    if kind == "periodic_10ms":
        return lambda n: J * math.sin(2 * math.pi * n * NOM / 10e6)
    if kind == "alternate_group":
        return lambda n: J if (n // 16) % 2 else -J
    if kind == "block_512ms":
        return lambda n: cache.setdefault(n // (16 * 256), J if rng.random() < 0.5 else -J)
    raise ValueError(kind)


def out(*a):
    print(*a)
    sys.stdout.flush()


def section_bound():
    out("== 1. The continuity bound per k (page: 2J + 601k <= B_k < 10,417 - 2J - 601k)")
    J = 1426
    for k in range(1, 6):
        lo, hi = 2 * J + 601 * k, HALF - 2 * J - 601 * k
        out(f"k={k} voided={k-1}: lower {lo} upper(excl) {hi} window {'%d..%d' % (lo, hi - 1) if lo < hi else 'none'}"
            f"; 4096 in: {lo <= 4096 < hi}; 5120 in: {lo <= 5120 < hi}")
    out(f"tolerance per timestamp across one voided group: 300 ppm {(5120 - 1202) / 2:.1f} ns, 0 ppm {5120 / 2:.1f} ns;"
        f" adjacent: 300 ppm {(4096 - 601) / 2:.1f}, 0 ppm {4096 / 2:.1f}")


def section_fill_exact():
    out("== 2. Midpoint fill against the true pick, ideal timestamps, rates -300..+300 ppm")
    worst = 0
    for ppm in [-300, -100, -10.64, 0, 0.66, 10.64, 100, 300]:
        for t0 in [0, 7, 999_999_999, M32 - 3_000_000, 4_294_000_000]:
            per = NOM / (1 + ppm * 1e-6)
            picks = []
            for g in range(3):
                ts = [int(math.floor(t0 + (g * 16 + i) * per)) % M32 for i in range(16)]
                d = [s32(ts[i] - ts[0] - i * NOM) for i in range(16)]
                picks.append((ts[0] + sum(d) // 16) % M32)
            fill = (picks[0] + (s32(picks[2] - picks[0]) >> 1)) % M32
            e = s32(fill - picks[1])
            worst = max(worst, abs(e))
    out(f"largest |fill - true pick| over 40 cases (incl. 2^32 wrap): {worst} ns")


def section_periodic_and_region():
    out("== 3. Validity region: lost PDUs pairwise in one group or >= 32 apart")
    J, ppm = 1426, 300
    n_groups = 500 * 30   # 30 s
    for kind in ["independent", "random_sign_group", "periodic_10ms", "block_512ms"]:
        for spacing in [32, 33, 40, 48, 2400, 8000]:
            for phase in range(0, 16, 5):
                lost = frozenset(range(phase, n_groups * 16, spacing))
                m = run(n_groups, ppm, shape(kind, J, 11 + phase), lost)
                bad = max(abs(r - 0) for _, r in m.rates) if m.rates else None
                # planted rate in ns per 512 ms
                planted = 512e6 * (1 / (1 + ppm * 1e-6) - 1)
                worst = max(abs(r - planted) for _, r in m.rates)
                out(f"{kind:18s} 1 in {spacing:5d} phase {phase:2d}: restarts {m.restarts} fills {m.fills}"
                    f" rates {len(m.rates)} worst |rate - planted| {worst:.0f} ns (2J/8 = {2 * J / 8:.0f})")
    out("-- tightness: two lost PDUs 31 apart (adjacent groups possible)")
    for phase in range(16):
        lost = frozenset([4000 + phase, 4000 + phase + 31])
        m = run(1000, 0, None, lost)
        out(f"pair 31 apart, first at position {(4000 + phase) % 16}: restarts {m.restarts}")
    out("-- densest pattern the region allows: random losses, each >= 32 PDUs after the last (about 250/s at the minimum)")
    rng = random.Random(5)
    lost, n = set(), 0
    while n < n_groups * 16:
        lost.add(n)
        n += 32 + rng.randrange(0, 3)
    m = run(n_groups, ppm, shape("random_sign_group", J, 3), frozenset(lost))
    planted = 512e6 * (1 / (1 + ppm * 1e-6) - 1)
    out(f"{len(lost) / 30:.0f} losses/s: restarts {m.restarts} fills {m.fills}"
        f" worst |rate - planted| {max(abs(r - planted) for _, r in m.rates):.0f} ns")


def section_mutants():
    out("== 4. Test-row mutants (page Test plan, meter suite)")
    J, ppm = 1426, 300
    n_groups = 500 * 120
    for per_s in [1.0, 0.3]:
        step = int(round(per_s * 8000))
        for kind in ["independent", "random_sign_group"]:
            lost = frozenset(range(4321, n_groups * 16, step))
            for mut in [None, "restart_any_loss"]:
                m = run(n_groups, ppm, shape(kind, J, 21), lost, mut)
                planted = 512e6 * (1 / (1 + ppm * 1e-6) - 1)
                worst = max((abs(r - planted) for _, r in m.rates), default=None)
                out(f"1 PDU per {per_s} s, {kind}, {mut or 'design'}: restarts {m.restarts}"
                    f" valid rates {len(m.rates)} worst {worst if worst is None else round(worst)}")
    out("-- snapshot-group loss, ideal, +100 ppm, PDU 5 of the snapshot group at 3 x 512 ms")
    base = run(500 * 12, 100)
    sg = 3 * 256
    lost = frozenset([sg * 16 + 5])
    for mut in [None, "fill_next_less_2ms", "voided_snapshot_restarts"]:
        m = run(500 * 12, 100, None, lost, mut)
        diffs = [r1 - r0 for (_, r0), (_, r1) in zip(base.rates, m.rates)]
        out(f"{mut or 'design'}: restarts {m.restarts} fills {m.fills} rates {len(m.rates)} vs {len(base.rates)};"
            f" rates differing by > 1 LSB: {sum(abs(x) > 1 for x in diffs)}, largest {max(map(abs, diffs), default=0)} ns")
    out("-- the bound row, +100 ppm, ideal")
    cases = {
        "two lost PDUs in adjacent groups": [1000 * 16 + 9, 1001 * 16 + 3],
        "a run of 17": list(range(1000 * 16 + 7, 1000 * 16 + 24)),
        "a run of 2 across a group boundary": [1000 * 16 + 15, 1001 * 16],
        "a run of 2 inside a group": [1000 * 16 + 4, 1000 * 16 + 5],
        "single losses 32 apart for 10 s": list(range(1000 * 16, 1000 * 16 + 80000, 32)),
    }
    for name, l in cases.items():
        for mut in [None, "accept_k3"]:
            m = run(500 * 12 + 5000, 100, None, frozenset(l), mut)
            out(f"{name}, {mut or 'design'}: restarts {m.restarts}")
    out("-- alias: a gap of exactly 16 voided groups + 1 (k mod 16 = 1), and of 15 (k = 0)")
    for ng in [15, 16, 17]:
        l = frozenset(range(1000 * 16 + 16, 1000 * 16 + 16 + ng * 16))
        m = run(1200, 0, None, l)
        out(f"{ng} whole groups lost: restarts {m.restarts}")


def section_steps():
    out("== 5. Steps inside a loss-voided group (PDU 15 lost; PDU 0 when the step is at 15), design point")
    J, ppm = 1426, 300
    for mut, b2 in [(None, 5120), ("no_gap_check", 5120), (None, 8192), (None, 6400)]:
        caught = tot = 0
        for size in [ONE, -ONE, HALF, -HALF]:
            for pos in range(16):
                for seed in range(4):
                    g = 2000
                    lostp = g * 16 + (0 if pos == 15 else 15)
                    m = run(2100, ppm, shape("random_sign_group", J, 100 + seed), frozenset([lostp]),
                            mut, step=(g * 16 + pos, size), b2=b2)
                    tot += 1
                    caught += (m.restarts >= 1)
        out(f"{mut or 'design'} B2={b2}: steps restarting {caught} of {tot}")


def section_random_loss():
    out("== 6. Independent loss at rate p per PDU: restarts, valid fraction, cold-start lock")
    out("   group-level Monte Carlo: each group voided w.p. q = 1-(1-p)^16; two voided groups in a row restart;")
    out("   rate valid from 2,048 groups after a restart; 'lockable' = a restart-free run of >= 7.3 s (the page's")
    out("   cold-start LOCKED time from first PDU).")
    T = 600.0
    G = int(T * 500)
    for p in [3e-5, 1e-4, 1e-3, 1.4e-3, 2e-3, 3e-3, 4e-3, 5e-3]:
        q = 1 - (1 - p) ** 16
        lam = 500 * q * q
        vals, rs, lockable_t = [], [], []
        for seed in range(8):
            rng = random.Random(seed * 7919 + int(p * 1e7))
            prev_void = False
            since = 0
            valid = 0
            restarts = 0
            first_lock = None
            for g in range(G):
                v = rng.random() < q
                if v and prev_void:
                    restarts += 1
                    since = 0
                    prev_void = False   # history restarts at the next good pick
                    continue
                prev_void = v
                since += 1
                if since >= 2048:
                    valid += 1
                if first_lock is None and since >= int(7.3 * 500):
                    first_lock = g / 500
            vals.append(valid / G)
            rs.append(restarts)
            lockable_t.append(first_lock)
        lk = [x for x in lockable_t if x is not None]
        out(f"p={p:.1e} ({8000 * p:5.1f} lost/s): restarts/s model {sum(rs) / 8 / T:.3f} vs 500q^2 {lam:.3f};"
            f" valid fraction {sum(vals) / 8:.3f} (renewal e^-4.096L = {math.exp(-lam * 4.096):.3f});"
            f" seeds reaching a 7.3 s run {len(lk)}/8, median first at {sorted(lk)[len(lk) // 2] if lk else None} s")
    out("-- round 3's rule (restart on any loss): lambda = 8000 p")
    for p in [3e-5, 1e-4]:
        lam = 8000 * p
        out(f"p={p:.1e}: restarts/s {lam:.3f}, renewal valid fraction {math.exp(-lam * 4.096):.3f}")


def section_loop_gain():
    out("== 7. l1 gains of the servo loop as the page describes it (e = x - r_err; u = I + e/4, I += e/2; plant gain g one window late)")
    for g in [0.8, 1.0, 1.2]:
        def imp(est_taps, n=400):
            x = [0.0] * n
            e = [0.0] * n
            u = [0.0] * n
            I = 0.0
            r = [0.0] * n
            for i, w in est_taps:
                r[i] += w
            for t in range(n):
                xt = -(g * u[t - 1]) if t else 0.0
                e[t] = xt - r[t]
                I += e[t] / 2
                u[t] = I + e[t] / 4
            return e
        e1 = imp([(0, 1.0)])
        e8 = imp([(0, 1 / 8), (8, -1 / 8)])
        l1_1, l1_8 = sum(map(abs, e1)), sum(map(abs, e8))
        out(f"g={g}: l1 gain from rate error {l1_1:.3f}; E8 composite from snapshot error {l1_8:.4f}"
            f" -> worst |e| at J=1426: {l1_8 * 1426:.0f} ns; product bound 2.125*2J/8 = {2.125 * 2 * 1426 / 8:.0f}")


if __name__ == "__main__":
    which = sys.argv[1:] or ["bound", "fill", "region", "mutants", "steps", "random", "gain"]
    for w in which:
        {"bound": section_bound, "fill": section_fill_exact, "region": section_periodic_and_region,
         "mutants": section_mutants, "steps": section_steps, "random": section_random_loss,
         "gain": section_loop_gain}[w]()
