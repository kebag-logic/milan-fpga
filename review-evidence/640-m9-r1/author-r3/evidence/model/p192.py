#!/usr/bin/env python3
"""192 kHz talker latency over every placement that starts and stops reach,
at 16 AAF reservations per port (lane evidence, round 3; not a gate).

Uses the round-2 model mixed_stagger.py unchanged (same directory).

Facts this script checks or relies on:
  P1  At 192 kHz there are 24 phases and at most 17 running entities per
      port (16 AAF and one CRF). A start always finds an empty phase, whose
      wire time is 0, so the rule puts it in the lowest-rank empty phase.
      reachable_occupancies() explores every start and stop of that rule
      (formats do not change a placement here) and lists the occupancies
      that hold 16 AAF streams.
  P2  One format: tandem_192 (packetizer as a FIFO queue on both ports, then
      each port's shaper from the ready times) is exact for one
      configuration. It is evaluated on every reachable occupancy and every
      N whose 16 reservations and CRF fit the 75 % cap.
  P3  Mixed formats, upper bound: shaper wait from release times (window
      superset of the model, outside streams one-channel) plus the largest
      packetizer delay over the same superset. A start delayed by ready
      times later by at most D is later by at most D (FIFO recursion), so
      the sum bounds every reachable mix.
  P4  Mixed formats, reached: the top superset windows are built as full
      configurations, placed by an explicit start and stop sequence under
      the rule with the cap checked at every step, and evaluated exactly by
      tandem_192.
Usage: python3 -I p192.py <dir-of-mixed_stagger.py>
"""
import itertools
import sys
from collections import deque
from fractions import Fraction as Fr

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
import mixed_stagger as m  # noqa: E402

r = m.Rate(192)
P = r.P
RANK = r.tie            # rank -> phase
NMAX = m.NMAX
CYC = {n: m.build_cycles(r.ns, n) for n in m.FORMATS}
FIXED = r.t_pin + m.T_CDC + m.T_MAC + m.I_1522


def reachable_occupancies():
    """P1: BFS over (AAF rank bitmask, CRF rank or -1). A start takes the
    lowest empty rank; any running entity may stop."""
    start = (0, -1)
    seen = {start}
    q = deque([start])
    while q:
        aaf, crf = q.popleft()
        used = aaf | ((1 << crf) if crf >= 0 else 0)
        low = (~used & (used + 1)).bit_length() - 1
        nxt = []
        if bin(aaf).count("1") < NMAX:
            nxt.append((aaf | 1 << low, crf))
        if crf < 0:
            nxt.append((aaf, low))
        k = aaf
        while k:
            b = k & -k
            nxt.append((aaf & ~b, crf))
            k &= k - 1
        if crf >= 0:
            nxt.append((aaf, -1))
        for st in nxt:
            if st not in seen:
                seen.add(st)
                q.append(st)
    full = []
    for a, c in seen:
        if bin(a).count("1") == NMAX:
            full.append((tuple(k for k in range(P) if a >> k & 1), None if c < 0 else c))
    full.sort(key=lambda x: (x[1] is None, x[1] if x[1] is not None else -1, x[0]))
    return len(seen), full


def phases_of(aaf_ranks, fmt_of_rank):
    ph = [[] for _ in range(P)]
    for k in aaf_ranks:
        ph[RANK[k]] = [fmt_of_rank[k]]
    return ph


def one_format(occ):
    out = []
    for aaf, crf in occ:
        crf_ph = RANK[crf] if crf is not None else None
        for n in m.FORMATS:
            ph = phases_of(aaf, {k: n for k in aaf})
            if m.idle_slope(r, ph, crf_ph) > m.CAP:
                continue
            t4 = m.tandem_192(r, ph, crf_ph, cycles=4)
            t8 = m.tandem_192(r, ph, crf_ph, cycles=8)
            out.append((t8, t4 == t8, n, aaf, crf))
    return out


def windows(occ_ph, crf_ph):
    """Every window ending at an occupied phase h, d phases back (d < P)."""
    for h in sorted(occ_ph):
        for d in range(P):
            win = [(h - d + i) % P for i in range(d + 1)]
            yield h, d, win


def shaper_superset(aaf, crf):
    occ_ph = {RANK[k] for k in aaf}
    crf_ph = RANK[crf] if crf is not None else None
    best = None
    for h, d, win in windows(occ_ph, crf_ph):
        ahead = [q for q in win[:-1] if q in occ_ph]
        crf_ahead = crf_ph is not None and crf_ph in win[:-1]
        outside = NMAX - len(ahead) - 1
        for combo in itertools.combinations_with_replacement(m.FORMATS, len(ahead)):
            num = sum(r.L[n] for n in combo) + (m.CRF_L if crf_ahead else 0)
            res = (sum(r.res[n] for n in combo) + r.res[1] + outside * r.resmin
                   + (m.CRF_RES if crf_ph is not None else 0))
            if Fr(res, m.INTERVAL) > m.CAP:
                continue
            v = Fr(num * m.INTERVAL, res) - d * r.tph
            if best is None or v > best[0]:
                best = (v, h, d, combo, crf_ahead)
    return best


def packetizer_superset(aaf, crf):
    """Largest ready-minus-release over every frame of both ports: within a
    window the packetizer builds each phase's frames for port 0 then port 1,
    the CRF last in its phase; the frame X ends the window on port 1."""
    occ_ph = {RANK[k] for k in aaf}
    crf_ph = RANK[crf] if crf is not None else None
    best = None
    targets = sorted(occ_ph | ({crf_ph} if crf_ph is not None else set()))
    for h in targets:
        for d in range(P):
            win = [(h - d + i) % P for i in range(d + 1)]
            ahead_aaf = [q for q in win[:-1] if q in occ_ph]
            crf_in_ahead = crf_ph is not None and crf_ph in win[:-1]
            x_is_crf = (h == crf_ph)
            # frames of the final phase up to and including X (port 1)
            last_aaf = (h in occ_ph)
            k_free = len(ahead_aaf) + (1 if last_aaf else 0)
            outside = NMAX - k_free
            for combo in itertools.combinations_with_replacement(m.FORMATS, k_free):
                res = (sum(r.res[n] for n in combo) + outside * r.resmin
                       + (m.CRF_RES if crf_ph is not None else 0))
                if Fr(res, m.INTERVAL) > m.CAP:
                    continue
                cyc = 2 * sum(CYC[n] for n in combo)
                cyc += 2 * m.CRF_CYCLES * (crf_in_ahead + (1 if x_is_crf else 0))
                if not x_is_crf and not last_aaf:
                    continue
                v = cyc * m.CYCLE_US - d * r.tph
                if best is None or v > best[0]:
                    best = (v, h, d, combo, crf_in_ahead, x_is_crf)
    return best


def place(target, crf_rank):
    """P4: an explicit start and stop sequence under the rule that reaches
    target (rank -> N for the 16 AAF ranks) with the CRF at crf_rank (or
    absent). Returns the sequence and the largest reserved bandwidth seen,
    or None when no sequence of this shape keeps the cap."""
    aaf_ranks = sorted(target)
    hole = None
    if crf_rank is None:
        missing = [k for k in range(NMAX + 1) if k not in target]
        hole = missing[0] if missing else None
    temp = hole                        # the CRF stands at the hole, then stops
    state = {}                         # rank -> N or 'crf'
    seq = []
    peak = Fr(0)

    def bw():
        s = sum(m.CRF_RES if v == 'crf' else r.res[v] for v in state.values())
        return Fr(s, m.INTERVAL)

    def low():
        return min(k for k in range(P) if k not in state)

    def start(v):
        nonlocal peak
        k = low()
        state[k] = v
        seq.append(('start', v, k))
        peak = max(peak, bw())
        return k

    def stop(k):
        seq.append(('stop', state[k], k))
        del state[k]

    # 1: one-channel fillers in every AAF rank, the CRF (real or temporary)
    for k in range(NMAX + 1):
        if k in target:
            assert start(1) == k
        elif k == crf_rank or k == temp:
            assert start('crf') == k
    # 2: swap fillers for the target formats, ranks above the hole first
    above = [k for k in aaf_ranks if temp is None or k > temp]
    below = [k for k in aaf_ranks if temp is not None and k < temp]
    for k in sorted(above, key=lambda k: r.res[target[k]]):
        stop(k)
        assert start(target[k]) == k
    if temp is not None:
        stop(temp)
    for k in sorted(below, key=lambda k: r.res[target[k]]):
        stop(k)
        assert start(target[k]) == k
    final = {k: v for k, v in state.items()}
    want = dict(target)
    if crf_rank is not None:
        want[crf_rank] = 'crf'
    assert final == want, (final, want)
    if peak > m.CAP:
        return None
    return seq, peak


def witness(aaf, crf, sup):
    """Build the superset's best window as a full configuration: the ahead
    formats in window order, X one-channel, every other stream one-channel."""
    v, h, d, combo, crf_ahead = sup
    win = [(h - d + i) % P for i in range(d + 1)]
    rank_of_ph = {RANK[k]: k for k in range(P)}
    ahead = [rank_of_ph[q] for q in win[:-1] if rank_of_ph[q] in aaf]
    best = None
    if len(combo) <= 6:
        orders = sorted(set(itertools.permutations(combo)))
    else:
        orders = [tuple(combo), tuple(sorted(combo, reverse=True))]
    for perm in orders:
        target = {k: 1 for k in aaf}
        for k, n in zip(ahead, perm):
            target[k] = n
        pl = place(target, crf)
        if pl is None:
            continue
        ph = phases_of(aaf, target)
        crf_ph = RANK[crf] if crf is not None else None
        t = m.tandem_192(r, ph, crf_ph, cycles=8)
        w = m.lindley_wait(r, ph, crf_ph, cycles=8)
        if best is None or t > best[0]:
            best = (t, w, dict(sorted(target.items())), pl[1])
    return best


def main():
    n_states, occ = reachable_occupancies()
    print(f"P1: {n_states} reachable states; {len(occ)} hold 16 AAF streams")
    expect = set()
    for k in range(NMAX + 1):
        rest = tuple(j for j in range(NMAX + 1) if j != k)
        expect.add((rest, k))
        expect.add((rest, None))
    print("   equal to {ranks 0..16 minus k} with the CRF at k or absent, k = 0..16:",
          set(occ) == expect)
    print(f"   fixed terms at 192 kHz: pin {m.fmt(r.t_pin)}, cdc {m.fmt(m.T_CDC)},"
          f" mac {m.fmt(m.T_MAC)}, interferer {m.fmt(m.I_1522)}; sum {m.fmt(FIXED)} us")

    uni = one_format(occ)
    stable = all(s for _, s, *_ in uni)
    top = max(uni, key=lambda x: x[0])
    print(f"P2: one format over {len(occ)} occupancies and every N within the cap:"
          f" worst total {m.fmt(top[0])} us, N = {top[2]}, CRF rank {top[4]},"
          f" hole {[k for k in range(NMAX + 1) if k not in top[3] and k != top[4]]};"
          f" 4 and 8 simulated intervals agree: {stable}")
    for n in m.FORMATS:
        rows = [x for x in uni if x[2] == n]
        if rows:
            w = max(rows, key=lambda x: x[0])
            print(f"   N = {n}: worst {m.fmt(w[0])} us over {len(rows)} occupancies")
        else:
            print(f"   N = {n}: 16 reservations exceed the cap")

    best_w = best_d = None
    per = []
    for aaf, crf in occ:
        sw = shaper_superset(set(aaf), crf)
        pk = packetizer_superset(set(aaf), crf)
        per.append((aaf, crf, sw, pk))
        if best_w is None or sw[0] > best_w[0]:
            best_w = sw + (aaf, crf)
        if best_d is None or pk[0] > best_d[0]:
            best_d = pk + (aaf, crf)
    W, D = best_w[0], best_d[0]
    print(f"P3: shaper wait superset max {m.fmt(W)} us (CRF rank {best_w[-1]},"
          f" window {best_w[2] + 1} phases, ahead {best_w[3]}, crf ahead {best_w[4]})")
    print(f"   packetizer delay superset max {m.fmt(D)} us (CRF rank {best_d[-1]},"
          f" window {best_d[2] + 1} phases, formats {best_d[3]})")
    print(f"   mixed upper bound = {m.fmt(W)} + {m.fmt(D)} + {m.fmt(FIXED)} = {m.fmt(W + D + FIXED)} us")
    print(f"   before packetizer time (round-2 form): {m.fmt(W + FIXED)} us")

    per.sort(key=lambda x: -x[2][0])
    reached = None
    for aaf, crf, sw, _ in per[:8]:
        wt = witness(set(aaf), crf, sw)
        if wt is None:
            print(f"   CRF rank {crf}: superset {m.fmt(sw[0])} us, no sequence within the cap")
            continue
        print(f"   CRF rank {crf}: superset {m.fmt(sw[0])} us; reached total {m.fmt(wt[0])} us,"
              f" shaper wait {m.fmt(wt[1])} us, peak reserved {m.fmt(wt[3])} Mb/s")
        if reached is None or wt[0] > reached[0]:
            reached = wt + (crf,)
    t, w, target, peak, crf = reached
    print(f"P4: mixed reached {m.fmt(t)} us total (shaper wait {m.fmt(w)} us), CRF rank {crf},"
          f" formats by rank {target}, peak reserved {m.fmt(peak)} Mb/s of {m.fmt(m.CAP)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
