#!/usr/bin/env python3
"""Mark II talker latency at 32x32 under mixed base formats (lane evidence).

Question: with the packet-boundary phase chosen at connect time as the
phase with the least wire time (ties in a fixed spread order), never
re-phasing a running stream, what is the worst talker latency over every
legal base-format mix at 16 reservations per port?

Inputs, each from the clause named:
  Milan v1.2 6.2      AAF PCM32, N in {1,2,4,6,8}; NS = 6/12/24 samples per
                      PDU at 48/96/192 kHz; one timestamp per PDU.
  Milan v1.2 Table 4.4 and its notes: MaxFrameSize = NS*4*N + 24 + 1,
                      F = MFS + 22 (at least 68), W = F + 20; bandwidth =
                      W * 8 * 8000. CRF: MFS 29, so W = 88, 5,632 kb/s.
  IEEE 802.1Q-2022 34.6.1.1  class idleSlope = sum of the stream idleSlopes
                      on the port; per-stream queues shaped at their own rate.
  IEEE 802.1Q-2022 8.6.8.2   credit rules (event-exact simulation below).
  IEEE 802.1Q-2022 34.3.1    75 % default deltaBandwidth for class A.
  IEEE 802.1Q-2022 L.3.1.1   one maximum interfering frame.

Exact facts the search relies on (each checked by this script):
  F1  Without interference, credit is never positive at a frame's start, so
      class-A start times follow s_k = max(a_k, s_{k-1} + L_{k-1}/idleSlope)
      (a FIFO server of service time L/idleSlope). The wait of frame X is
      max over windows of (bits queued ahead of X since the window start)
      / idleSlope - (window length). check_lindley() compares this with the
      event-exact 8.6.8.2 simulation on random configurations.
  F2  One lower-priority frame of duration I delays any class-A start by at
      most I: credit gained while blocked is spent by later frames.
      check_interference() runs the 8.6.8.2 simulation with a saturated
      best-effort queue of maximum frames and checks the additive bound.
  F3  The least-loaded rule implies, for every phase p and the stream j
      added to it last: when j was added, every other phase held at least
      load(p) - L_j. With at most 16 streams at any time this bounds every
      phase, jointly, over some order of last additions (feasible()). The
      search maximises over that superset, so its result is an upper bound;
      witnesses() then reaches the top configurations with the exact rule.

No timing here is a measurement. Usage: python3 -I mixed_stagger.py
"""
from fractions import Fraction as Fr
import itertools
import random
import sys

R = 1000                       # port rate, bits per microsecond (1 Gb/s)
INTERVAL = 125                 # class A measurement interval, microseconds
NMAX = 16                      # AAF reservations per port at 32x32
CAP = Fr(3, 4) * R             # 75 % class A cap, bits per microsecond
FORMATS = (1, 2, 4, 6, 8)
NS_OF = {48: 6, 96: 12, 192: 24}
CRF_L = 8 * 88                 # CRF frame on the wire, bits
CRF_RES = 8 * 88               # CRF reservation per interval, bits
I_1522 = Fr((1522 + 20) * 8, R)  # one 1522-octet frame plus preamble and IFG
I_2000 = Fr((2000 + 20) * 8, R)  # the 802.1BA 6.3 ceiling, for comparison
T_CDC = Fr(2, 10)              # allowance; four 50 MHz cycles are 0.080 us
T_MAC = Fr(1)                  # MAC launch and PHY, allowance
CYCLE_US = Fr(1, 50)           # one 50 MHz cycle


def aaf_l(ns, n):
    """Frame on the wire, bits (Table 4.4 note, without the extra octet)."""
    return 8 * (max(24 + ns * 4 * n + 22, 68) + 20)


def aaf_res(ns, n):
    """Reservation per interval, bits (Table 4.4, with the extra octet)."""
    return 8 * (max(24 + ns * 4 * n + 1 + 22, 68) + 20)


def build_cycles(ns, n):
    """Packetizer cycles for one frame: context 4, headers 5 + 6, payload,
    turnaround 1 (the stream-engine page's estimate)."""
    return 16 + ns * n


CRF_CYCLES = 22


class Rate:
    def __init__(self, khz):
        self.khz = khz
        self.ns = NS_OF[khz]
        self.P = self.ns
        self.tph = Fr(INTERVAL, self.P)
        self.L = {n: aaf_l(self.ns, n) for n in FORMATS}
        self.res = {n: aaf_res(self.ns, n) for n in FORMATS}
        self.L8 = self.L[8]
        self.Lmin = self.L[1]
        self.resmin = self.res[1]
        # pin to capture: release at the TDM frame end, a stream mapped only
        # to slot 0 waits 7 of 8 slots of one sample period
        self.t_pin = Fr(7, 8) * Fr(1000, khz)
        # spread tie order: bit-reversal-like, phases far apart first
        self.tie = spread_order(self.P)
        self.rank = {p: i for i, p in enumerate(self.tie)}


def spread_order(P):
    if P == 6:
        return [0, 3, 1, 4, 2, 5]
    order, seen = [], set()
    k = 1
    while len(order) < P:
        for j in range(k):
            p = (j * P) // k
            if p not in seen:
                seen.add(p)
                order.append(p)
        k *= 2
    return order


# ---------------------------------------------------------------- shaper ---

def frames_of(rate, phases, crf_phase):
    """One interval's frames: (release, bits, is_aaf), smallest first within a
    phase, the CRF last in its phase."""
    out = []
    for p in range(rate.P):
        for n in sorted(phases[p], key=lambda n: rate.L[n]):
            out.append((p * rate.tph, rate.L[n], True, p))
        if crf_phase == p:
            out.append((p * rate.tph, CRF_L, False, p))
    return out


def idle_slope(rate, phases, crf_phase):
    s = sum(rate.res[n] for ph in phases for n in ph)
    if crf_phase is not None:
        s += CRF_RES
    return Fr(s, INTERVAL)


def lindley_wait(rate, phases, crf_phase, cycles=4):
    """Worst AAF wait, start minus release, by the FIFO recursion F1."""
    a = idle_slope(rate, phases, crf_phase)
    fr = frames_of(rate, phases, crf_phase)
    if not fr:
        return Fr(0)
    prev_end = None
    worst = Fr(0)
    for c in range(cycles):
        for rel, bits, aaf, _ in fr:
            r = rel + c * INTERVAL
            s = r if prev_end is None else max(r, prev_end)
            prev_end = s + Fr(bits) / a
            if aaf and c >= cycles - 2:
                worst = max(worst, s - r)
    return worst


def cbs_sim(rate, phases, crf_phase, be_bits=None, cycles=4, be_phase=0):
    """Event-exact IEEE 802.1Q-2022 8.6.8.2 for the class A queue, with an
    optional saturated best-effort queue of be_bits frames (strict lower
    priority, non-preemptive). Returns the worst AAF wait."""
    a = idle_slope(rate, phases, crf_phase)
    fr = frames_of(rate, phases, crf_phase)
    arr = [(rel + c * INTERVAL, bits, aaf, c) for c in range(cycles)
           for rel, bits, aaf, _ in fr]
    arr.sort(key=lambda x: x[0])
    t = Fr(0)
    credit = Fr(0)
    q = []
    i = 0
    worst = Fr(0)
    be_next = Fr(be_phase) if be_bits else None
    while i < len(arr) or q:
        # admit arrivals at or before t
        while i < len(arr) and arr[i][0] <= t:
            q.append(arr[i])
            i += 1
        if q and credit >= 0:
            rel, bits, aaf, c = q.pop(0)
            if aaf and c >= cycles - 2:
                worst = max(worst, t - rel)
            dur = Fr(bits, R)
            credit += (a - R) * dur
            t += dur
            continue
        if q:
            # waiting for credit; a best-effort frame may start meanwhile
            need = -credit / a
            if be_bits and be_next is not None and be_next <= t:
                dur = Fr(be_bits, R)
                credit += a * dur
                t += dur
                continue
            t += need
            credit = Fr(0)
            continue
        # queue empty
        nxt = arr[i][0]
        if be_bits and be_next is not None and be_next <= t:
            dur = Fr(be_bits, R)
            end = t + dur
            # the queue is empty until the next arrival: credit rises to zero
            # and stays there; from the arrival on it rises without a cap
            upto = min(end, nxt)
            credit = min(Fr(0), credit + a * (upto - t)) if credit < 0 else Fr(0)
            if nxt < end:
                credit += a * (end - nxt)
            t = end
            continue
        gap = nxt - t
        credit = min(Fr(0), credit + a * gap) if credit < 0 else Fr(0)
        t = nxt
    return worst


def check_lindley(rate, trials=300, seed=1):
    rnd = random.Random(seed)
    for _ in range(trials):
        phases = [[] for _ in range(rate.P)]
        for _ in range(rnd.randint(1, NMAX)):
            phases[rnd.randrange(rate.P)].append(rnd.choice(FORMATS))
        crf = rnd.choice([None] + list(range(rate.P)))
        if idle_slope(rate, phases, crf) > CAP:
            continue
        x = lindley_wait(rate, phases, crf)
        y = cbs_sim(rate, phases, crf)
        if x != y:
            return False, (phases, crf, x, y)
    return True, None


def check_interference(rate, trials=200, seed=2):
    rnd = random.Random(seed)
    worst_gap = Fr(-10 ** 9)
    for _ in range(trials):
        phases = [[] for _ in range(rate.P)]
        for _ in range(rnd.randint(1, NMAX)):
            phases[rnd.randrange(rate.P)].append(rnd.choice(FORMATS))
        crf = rnd.choice([None] + list(range(rate.P)))
        if idle_slope(rate, phases, crf) > CAP:
            continue
        base = lindley_wait(rate, phases, crf)
        for off in (Fr(0), Fr(1, 3), Fr(7, 2), Fr(rnd.randint(0, 1240), 100)):
            w = cbs_sim(rate, phases, crf, be_bits=(1522 + 20) * 8,
                        be_phase=off)
            worst_gap = max(worst_gap, w - base)
            if w > base + I_1522:
                return False, (phases, crf, base, w, off), worst_gap
    return True, None, worst_gap


def per_stream_spacing_ok(rate):
    """34.6.1.1 per-stream level: frames are released 125 us apart; the
    stream's shaper never holds one when L / stream idleSlope <= 125 us."""
    worst = Fr(0)
    for n in FORMATS:
        worst = max(worst, Fr(rate.L[n] * INTERVAL, rate.res[n]))
    worst = max(worst, Fr(CRF_L * INTERVAL, CRF_RES))
    return worst <= INTERVAL, worst


# ------------------------------------------------------------ the rule ---

def load(rate, ph):
    return sum(rate.L[n] for n in ph)


def greedy_add(rate, phases, n, crf_phase=None):
    loads = [load(rate, phases[p]) + (CRF_L if crf_phase == p else 0)
             for p in range(rate.P)]
    p = min(range(rate.P), key=lambda q: (loads[q], rate.rank[q]))
    phases[p].append(n)
    return p


# ---------------------------------------------------- superset search ---

def ceil_div(v, d):
    return 0 if v <= 0 else -(-v // d)


def saving(reqs, bonus):
    """The CRF sits in one phase: it can stand in for scaffold there only."""
    if not bonus:
        return 0
    return 1 if any(ceil_div(r, L8G[0]) > ceil_div(r - bonus, L8G[0])
                    for r in reqs) else 0


L8G = [0]


def triples(rate, bonus):
    """Per-phase contents allowed by F3 alone, summarised as
    (streams, wire bits, largest frame, reservation bits, cycles)."""
    L8G[0] = rate.L8
    out = {}
    for k in range(1, NMAX + 1):
        for combo in itertools.combinations_with_replacement(FORMATS, k):
            W = sum(rate.L[n] for n in combo)
            Lm = max(rate.L[n] for n in combo)
            D = W - Lm
            cost = k + (rate.P - 1) * ceil_div(D, rate.L8) - saving([D], bonus)
            if cost > NMAX:
                continue
            res = sum(rate.res[n] for n in combo)
            cyc = sum(build_cycles(rate.ns, n) for n in combo)
            key = (k, W, Lm, res)
            out.setdefault(key, (k, W, Lm, res, cyc, combo))
    return list(out.values())


def feasible(rate, win, bonus, want_order=False):
    """F3 jointly: some order of last additions satisfies every phase.
    win: list of (k, W, Lm, ...). Subset dynamic programme; the CRF may
    stand in for scaffold in one other phase per condition."""
    L8G[0] = rate.L8
    m = len(win)
    D = [w[1] - w[2] for w in win]
    ok = {0: ()}
    for mask in range(1 << m):
        if mask not in ok:
            continue
        before = [i for i in range(m) if mask >> i & 1]
        for k in range(m):
            if mask >> k & 1 or (mask | 1 << k) in ok:
                continue
            nb = len(before)
            reqs = [D[k] - win[i][1] for i in before]
            cost = win[k][0] + sum(win[i][0] for i in before)
            cost += sum(ceil_div(r, rate.L8) for r in reqs)
            others = rate.P - 1 - nb
            cost += others * ceil_div(D[k], rate.L8)
            cost -= saving(reqs + ([D[k]] if others else []), bonus)
            if cost <= NMAX:
                ok[mask | 1 << k] = ok[mask] + (k,)
    full = (1 << m) - 1
    if want_order:
        return ok.get(full)
    return full in ok


def window_objective(rate, win, n_total, crf_mode):
    """Wait of the last AAF frame of the window's final phase, outside
    streams all one-channel (they only raise idleSlope). crf_mode:
    'none', 'ahead' (in an earlier window phase), 'other'."""
    nw = sum(w[0] for w in win)
    out = n_total - nw
    if out < 0 or (out > 0 and len(win) >= rate.P):
        return None
    Wsum = sum(w[1] for w in win)
    res = sum(w[3] for w in win) + out * rate.resmin
    num = Wsum - win[-1][2]
    if crf_mode != 'none':
        res += CRF_RES
    if crf_mode == 'ahead':
        if len(win) < 2:
            return None
        num += CRF_L
    if Fr(res, INTERVAL) > CAP:
        return None
    a = Fr(res, INTERVAL)
    return Fr(num) / a - (len(win) - 1) * rate.tph


def superset_search(rate, n_total, crf_mode, dmax, top=8):
    bonus = CRF_L if crf_mode != 'none' else 0
    tri = triples(rate, bonus)
    tri.sort(key=lambda t: -t[1])
    best = []

    def consider(win):
        v = window_objective(rate, win, n_total, crf_mode)
        if v is None:
            return
        if len(best) < top or v > best[-1][0]:
            if not feasible(rate, win, bonus):
                return
            best.append((v, tuple(t[5] for t in win)))
            best.sort(key=lambda x: -x[0])
            del best[top:]

    def dfs(win, nw):
        consider(win)
        if len(win) > dmax:
            return
        for t in tri:
            if nw + t[0] > n_total:
                continue
            nwin = [t] + win
            if len(nwin) > 1 and not feasible(rate, nwin, bonus):
                continue
            dfs(nwin, nw + t[0])

    for t in tri:
        if t[0] <= n_total:
            dfs([t], t[0])
    return best


def superset_search2(rate, n_total, crf_mode, dmax, top=8):
    """The same superset as superset_search, searched exactly but faster:
    F3 and the window objective depend only on the multiset of the phases
    ahead of the final phase, so those are enumerated as multisets, with
    feasibility cached and an optimistic cut that cannot drop a better
    window."""
    bonus = CRF_L if crf_mode != 'none' else 0
    tri = triples(rate, bonus)
    tri.sort(key=lambda t: -t[1])
    wmax = max(t[1] for t in tri)
    cache = {}
    best = []

    def feas(keys):
        if keys not in cache:
            cache[keys] = feasible(rate, [tri[i] for i in keys], bonus)
        return cache[keys]

    def theta():
        return best[-1][0] if len(best) >= top else None

    def bound(num, res, nw, d):
        hi = None
        crf_add = CRF_L if crf_mode == 'ahead' and d == 0 else 0
        for e in range(1, rate.P - d):
            for r in range(0, n_total - nw + 1):
                X = min(r * rate.L8, e * wmax)
                den = res + X - r * rate.Lmin
                if den <= 0:
                    continue
                v = Fr((num + X + crf_add) * INTERVAL, den) - (d + e) * rate.tph
                hi = v if hi is None or v > hi else hi
        return hi

    for hi_i, th in enumerate(tri):
        if th[0] > n_total:
            continue

        def dfs(ahead, start, nw):
            win = [tri[i] for i in ahead] + [th]
            v = window_objective(rate, win, n_total, crf_mode)
            if v is not None and (theta() is None or v > theta()):
                if feas(tuple(sorted(ahead + [hi_i]))):
                    best.append((v, tuple(t[5] for t in win)))
                    best.sort(key=lambda x: -x[0])
                    del best[top:]
            if len(ahead) >= dmax:
                return
            out = n_total - nw
            res = sum(t[3] for t in win) + out * rate.resmin + (
                CRF_RES if crf_mode != 'none' else 0)
            num = sum(t[1] for t in win) - th[2] + (
                CRF_L if crf_mode == 'ahead' and ahead else 0)
            t0 = theta()
            if t0 is not None:
                b = bound(num, res, nw, len(ahead))
                if b is None or b <= t0:
                    return
            for j in range(start, len(tri)):
                if nw + tri[j][0] > n_total:
                    continue
                if not feas(tuple(sorted(ahead + [j, hi_i]))):
                    continue
                dfs(ahead + [j], j, nw + tri[j][0])

        dfs([], 0, th[0])
    return best


def optimistic_bound(rate, n_total, crf_mode, d):
    """Upper bound for windows of d+1 phases from the per-phase sets alone
    (no joint condition): a knapsack over (streams, bits)."""
    bonus = CRF_L if crf_mode != 'none' else 0
    tri = triples(rate, bonus)
    # best[(nw)] = max (Wsum - resdelta) is not separable; enumerate the
    # Pareto front of (nw, Wsum, ressum) per phase count
    front = {(0, 0, 0)}
    for _ in range(d + 1):
        nxt = set()
        for nw, Ws, rs in front:
            for t in tri:
                if nw + t[0] <= n_total:
                    nxt.add((nw + t[0], Ws + t[1], rs + t[3]))
        # prune dominated: same nw, keep max Ws per rs bucket roughly
        keep = {}
        for nw, Ws, rs in nxt:
            k = (nw, rs - Ws)
            if keep.get(k, -1) < Ws:
                keep[k] = Ws
        front = {(k[0], Ws, k[1] + Ws) for k, Ws in keep.items()}
    best = None
    for nw, Ws, rs in front:
        out = n_total - nw
        if out < 0 or (out > 0 and d + 1 >= rate.P):
            continue
        res = rs + out * rate.resmin + (CRF_RES if crf_mode != 'none' else 0)
        if Fr(res, INTERVAL) > CAP:
            continue
        num = Ws - rate.Lmin + (CRF_L if crf_mode == 'ahead' else 0)
        v = Fr(num) * INTERVAL / res - d * rate.tph
        best = v if best is None or v > best else best
    return best


# ------------------------------------------------------------ witnesses ---

def construct(rate, window, order, h0, n_total, crf_first):
    """Reach a configuration whose phases h0.. hold `window` using only the
    exact rule. Window phases are filled in `order`; eight-channel scaffold
    keeps the other phases at least as loaded; scaffold is then removed and
    the outside refilled with one-channel streams. Returns (phases, crf) or
    None when this order does not get there."""
    m = len(window)
    tgt = [(h0 + i) % rate.P for i in range(m)]
    phases = [[] for _ in range(rate.P)]
    crf = None
    if crf_first:
        crf = rate.tie[0]

    def dest_of():
        loads = [load(rate, phases[q]) + (CRF_L if crf == q else 0)
                 for q in range(rate.P)]
        return min(range(rate.P), key=lambda q: (loads[q], rate.rank[q]))

    finished = set()
    for idx in order:
        p = tgt[idx]
        phases[p] = []
        pending = sorted(window[idx], key=lambda n: rate.L[n])
        guard = 0
        while pending:
            guard += 1
            if guard > 400:
                return None
            d = dest_of()
            total = sum(len(x) for x in phases)
            if d == p:
                if total >= NMAX:
                    return None
                n = pending.pop(0)
                greedy_add(rate, phases, n, crf)
                continue
            if d in finished:
                return None
            if total >= NMAX:
                # free a slot from the most loaded scaffold phase if it stays
                # above the target phase
                cand = [q for q in range(rate.P) if q not in finished
                        and q != p and phases[q]]
                if not cand:
                    return None
                q = max(cand, key=lambda q: load(rate, phases[q]))
                after = load(rate, phases[q]) - rate.L[phases[q][-1]]
                if after < load(rate, phases[p]) + rate.L[pending[0]]:
                    return None
                phases[q].pop()
                continue
            greedy_add(rate, phases, 8, crf)
        finished.add(p)
    for q in range(rate.P):
        if q not in finished:
            phases[q] = []
    while sum(len(x) for x in phases) < n_total:
        q = dest_of()
        if q in finished:
            return None
        greedy_add(rate, phases, 1, crf)
    if not crf_first:
        crf = dest_of()
    return phases, crf


def witnesses(rate, window, n_total, crf_mode):
    """Best exact wait over every start phase and fill order."""
    best = None
    m = len(window)
    for order in itertools.permutations(range(m)):
        for h0 in range(rate.P):
            for crf_first in ((False,) if crf_mode == 'none' else (False, True)):
                got = construct(rate, window, order, h0, n_total, crf_first)
                if not got:
                    continue
                phases, crf = got
                if crf_mode == 'none':
                    crf = None
                if idle_slope(rate, phases, crf) > CAP:
                    continue
                w = lindley_wait(rate, phases, crf)
                if best is None or w > best[0]:
                    best = (w, [list(x) for x in phases], crf)
    return best


def exact_192(rate, n_total=NMAX):
    """192 kHz: every phase holds at most one stream (F3 with 23 other
    phases), so a new stream always takes the first empty phase in the tie
    order and the occupied set is a subset of its first 16 phases. With 16
    reservations all 16 are occupied. Enumerate windows and format counts."""
    F16 = set(rate.tie[:NMAX])
    best = None
    occ = sorted(F16)
    for h in occ:
        for d in range(rate.P):
            win = [(h - d + i) % rate.P for i in range(d + 1)]
            if win[0] not in F16:
                continue
            ahead = [q for q in win[:-1] if q in F16]
            outside = n_total - len(ahead) - 1
            for crf_ahead in (False, True):
                if crf_ahead and not ahead:
                    continue
                for combo in itertools.combinations_with_replacement(
                        FORMATS, len(ahead)):
                    num = sum(rate.L[n] for n in combo) + (CRF_L if crf_ahead else 0)
                    res = (sum(rate.res[n] for n in combo) + rate.res[1]
                           + outside * rate.resmin + CRF_RES)
                    if Fr(res, INTERVAL) > CAP:
                        continue
                    v = Fr(num * INTERVAL, res) - d * rate.tph
                    if best is None or v > best[0]:
                        best = (v, h, d, combo, crf_ahead)
    return best


# ----------------------------------------------------------------- run ---

def fmt(x):
    return f"{float(x):.3f}"


def pkt_max(rate, bonus):
    """Largest packetizer time of one phase, both ports, with a CRF each."""
    worst = 0
    for t in triples(rate, bonus):
        worst = max(worst, t[4])
    return 2 * (worst + CRF_CYCLES) * CYCLE_US


def uniform_reachable(rate, n, with_crf=True):
    """Exact: every state reachable by starts and stops of one-format
    streams (at most 16) and one CRF stream, both placed by the rule.
    Returns the worst exact wait over states with 16 streams."""
    P = rate.P
    start = (tuple([0] * P), -1)
    seen = {start}
    todo = [start]
    worst = None

    def place(counts, crf, bits):
        loads = [counts[q] * rate.L[n] + (CRF_L if crf == q else 0)
                 for q in range(P)]
        return min(range(P), key=lambda q: (loads[q], rate.rank[q]))

    while todo:
        counts, crf = todo.pop()
        tot = sum(counts)
        nxt = []
        if tot < NMAX:
            q = place(counts, crf, rate.L[n])
            c = list(counts); c[q] += 1
            nxt.append((tuple(c), crf))
        for q in range(P):
            if counts[q]:
                c = list(counts); c[q] -= 1
                nxt.append((tuple(c), crf))
        if with_crf:
            if crf < 0:
                nxt.append((counts, place(counts, crf, CRF_L)))
            else:
                nxt.append((counts, -1))
        for st in nxt:
            if st not in seen:
                seen.add(st)
                todo.append(st)
    for counts, crf in seen:
        if sum(counts) != NMAX:
            continue
        phases = [[n] * counts[q] for q in range(P)]
        c = None if crf < 0 else crf
        if idle_slope(rate, phases, c) > CAP:
            continue
        w = lindley_wait(rate, phases, c)
        if worst is None or w > worst[0]:
            worst = (w, counts, c)
    return worst, len(seen)


def churn_search(rate, seconds=60, seed=5, with_crf=True):
    """Random starts and stops under the exact rule; the worst 16-stream
    state found is a reachable witness (a lower bound)."""
    import time
    rnd = random.Random(seed)
    t0 = time.time()
    best = None
    while time.time() - t0 < seconds:
        phases = [[] for _ in range(rate.P)]
        crf = rate.tie[0] if with_crf and rnd.random() < 0.5 else None
        for _ in range(NMAX):
            greedy_add(rate, phases, 8, crf)
        keep = rnd.randint(1, 4)
        h = rnd.randrange(rate.P)
        hold = {(h + i) % rate.P for i in range(keep)}
        for q in range(rate.P):
            if q not in hold:
                phases[q] = []
        for step in range(60):
            tot = sum(len(x) for x in phases)
            if tot < NMAX and (rnd.random() < 0.7 or tot == 0):
                greedy_add(rate, phases, rnd.choice((1, 1, 2, 8, 8, 6, 4)), crf)
            else:
                q = rnd.choice([q for q in range(rate.P) if phases[q]])
                phases[q].pop(rnd.randrange(len(phases[q])))
            if sum(len(x) for x in phases) == NMAX:
                c = crf
                if with_crf and c is None:
                    loads = [load(rate, phases[q]) for q in range(rate.P)]
                    c = min(range(rate.P), key=lambda q: (loads[q], rate.rank[q]))
                if idle_slope(rate, phases, c) > CAP:
                    continue
                w = lindley_wait(rate, phases, c)
                if best is None or w > best[0]:
                    best = (w, [list(x) for x in phases], c)
    return best


def exact_192b(rate, n_total=NMAX):
    """192 kHz with the CRF placed by the rule too. Case 'last': the CRF
    starts after the AAF streams and takes the first empty tie phase; the
    AAF set is the first 16 tie phases. Case 'first': the CRF starts on an
    idle port and takes tie phase 0; the AAF set is the next 16. Case
    'none': no CRF. Every phase holds at most one stream (F3)."""
    out = {}
    for case in ('none', 'last', 'first'):
        if case == 'first':
            occ, crf = rate.tie[1:NMAX + 1], rate.tie[0]
        else:
            occ = rate.tie[:NMAX]
            crf = None if case == 'none' else rate.tie[NMAX]
        occ = set(occ)
        best = None
        for h in sorted(occ):
            for d in range(rate.P):
                win = [(h - d + i) % rate.P for i in range(d + 1)]
                ahead = [q for q in win[:-1] if q in occ]
                crf_ahead = crf is not None and crf in win[:-1]
                outside = n_total - len(ahead) - 1
                for combo in itertools.combinations_with_replacement(FORMATS, len(ahead)):
                    num = sum(rate.L[n] for n in combo) + (CRF_L if crf_ahead else 0)
                    res = (sum(rate.res[n] for n in combo) + rate.res[1]
                           + outside * rate.resmin + (CRF_RES if crf is not None else 0))
                    if Fr(res, INTERVAL) > CAP:
                        continue
                    v = Fr(num * INTERVAL, res) - d * rate.tph
                    if best is None or v > best[0]:
                        best = (v, h, d, combo, crf_ahead)
        out[case] = best
    return out


def tandem_192(rate, phases, crf, cycles=4):
    """192 kHz: one packetizer frame takes up to 4.16 us per port, against a
    5.208 us phase, so it is modelled as a queue: the shared packetizer
    builds each phase's frames for port 0 then port 1 (FIFO), and each port's
    shaper (F1) starts from the ready times. Returns the worst port-1 AAF
    latency, pin to first bit, with the fixed terms and one interferer."""
    a = idle_slope(rate, phases, crf)
    fr = frames_of(rate, phases, crf)
    cyc = {n: build_cycles(rate.ns, n) for n in FORMATS}
    pk_free = None
    ready = {0: [], 1: []}
    for c in range(cycles):
        for rel, bits, aaf, p in fr:
            r = rel + c * INTERVAL
            n = next((n for n in FORMATS if rate.L[n] == bits), None) if aaf else None
            b = (cyc[n] if aaf else CRF_CYCLES) * CYCLE_US
            for port in (0, 1):
                start = r if pk_free is None else max(r, pk_free)
                pk_free = start + b
                ready[port].append((pk_free, r, bits, aaf, c))
    worst = Fr(0)
    for port in (0, 1):
        prev = None
        for rd, r, bits, aaf, c in sorted(ready[port], key=lambda x: x[0]):
            s0 = rd if prev is None else max(rd, prev)
            prev = s0 + Fr(bits) / a
            if aaf and c >= cycles - 2:
                worst = max(worst, s0 - r)
    return worst + rate.t_pin + T_CDC + T_MAC + I_1522


def main():
    sec = sys.argv[1] if len(sys.argv) > 1 else 'checks'
    if sec == 'checks':
        for khz in (48, 96, 192):
            rate = Rate(khz)
            print(f"== {khz} kHz: {rate.P} phases of {fmt(rate.tph)} us, tie order {rate.tie}")
            print("   frame bits", rate.L, "reservation bits", rate.res)
            ok, sp = per_stream_spacing_ok(rate)
            print("   34.6.1.1 per-stream level never holds a frame:", ok,
                  "(largest L / stream idleSlope", fmt(sp), "us)")
            good, bad = check_lindley(rate)
            print("   F1 window form equals 8.6.8.2 simulation, 300 random mixes:", good)
            good, bad, gap = check_interference(rate)
            print("   F2 saturated best effort adds at most one 1522-octet frame:", good,
                  "(largest excess", fmt(gap), "us, frame", fmt(I_1522), "us)")
            T_pk = pkt_max(rate, CRF_L)
            print("   pin", fmt(rate.t_pin), "cdc", fmt(T_CDC), "packetizer, largest phase",
                  fmt(T_pk), "mac", fmt(T_MAC), "interferer", fmt(I_1522))
        r = Rate(48)
        ph = [[8, 8, 8], [8, 8, 8], [1, 1], [1, 1, 1], [1, 1, 1], [1, 1]]
        print("R758-1-F2 case, CRF in phase 1:", fmt(lindley_wait(r, ph, 1)))
        ph = [[8, 8, 8], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1], [1, 1]]
        print("R757-1-F4 case, CRF in phase 0:", fmt(lindley_wait(r, ph, 0)))
    elif sec == 'uniform':
        for khz in (48, 96):
            rate = Rate(khz)
            for n in FORMATS:
                w, cnt = uniform_reachable(rate, n, with_crf=True)
                if w is None:
                    print(f"{khz} kHz uniform {n} ch: no legal 16-stream state")
                    continue
                print(f"{khz} kHz uniform {n} ch, starts and stops, {cnt} states:"
                      f" worst wait {fmt(w[0])} us, counts {w[1]}, crf {w[2]}")
    elif sec in ('s48', 's96'):
        khz = 48 if sec == 's48' else 96
        rate = Rate(khz)
        modes = sys.argv[2:] or ['ahead', 'other', 'none']
        for mode in modes:
            best = superset_search2(rate, NMAX, mode, rate.P - 1, top=6)
            v, win = best[0]
            print(f"{khz} kHz superset, crf {mode}, all windows: worst wait {fmt(v)} us, window {win}")
            for vv, ww in best[:6]:
                wit = witnesses(rate, ww, NMAX, mode)
                print(f"   {fmt(vv)} {ww} ->",
                      f"reached {fmt(wit[0])} us {wit[1]} crf {wit[2]}" if wit else "not reached by the constructor")
    elif sec in ('c48', 'c96'):
        khz = 48 if sec == 'c48' else 96
        rate = Rate(khz)
        for crf in (True, False):
            w = churn_search(rate, seconds=int(sys.argv[2]) if len(sys.argv) > 2 else 60,
                             with_crf=crf)
            print(f"{khz} kHz random starts and stops, crf {crf}: reached wait {fmt(w[0])} us,"
                  f" phases {w[1]}, crf {w[2]}")
    elif sec == 'e192':
        rate = Rate(192)
        res = exact_192b(rate)
        for case, (v, h, d, combo, ca) in res.items():
            print(f"192 kHz exact, CRF {case}: worst wait {fmt(v)} us, final phase {h},"
                  f" window {d + 1} phases, ahead formats {combo}, crf ahead {ca};"
                  f" total without packetizer time {fmt(v + rate.t_pin + T_CDC + T_MAC + I_1522)} us")
        F16 = rate.tie[:NMAX]
        for n in FORMATS:
            phases = [[] for _ in range(rate.P)]
            for q in F16:
                phases[q] = [n]
            worst = None
            for c in [None] + [q for q in range(rate.P) if q not in F16]:
                if idle_slope(rate, phases, c) > CAP:
                    continue
                t = tandem_192(rate, phases, c)
                worst = t if worst is None or t > worst else worst
            print(f"   uniform {n} ch x 16 in the first 16 tie phases, packetizer as a queue:",
                  "above the 75 % cap" if worst is None else f"total {fmt(worst)} us")
        load_max = Fr(0)
        for m8 in range(NMAX + 1):
            res = m8 * rate.res[8] + (NMAX - m8) * rate.res[1] + CRF_RES
            if Fr(res, INTERVAL) <= CAP:
                cycles = 2 * (m8 * build_cycles(rate.ns, 8) + (NMAX - m8) * build_cycles(rate.ns, 1) + CRF_CYCLES)
                load_max = max(load_max, cycles * CYCLE_US / INTERVAL)
                best_m8 = m8
        print(f"   at most {best_m8} eight-channel streams per port under the cap;"
              f" packetizer load then {fmt(100 * load_max)} %")
    return 0


if __name__ == "__main__":
    sys.exit(main())
