"""Scratch prototype: replay census commits through the 100 Mb/s transmit queue (see in-tree egress_mii.py later)."""
import bisect, json, sys
from pathlib import Path

SYS_NS, DP_NS, OCTET_NS = 12.5, 20.0, 80.0
WORDS = [128, 256, 512, 128, 512]          # ADP ACMP AECP MAAP SRP
SF_BEATS, SF_FRAMES = 512, 8
GAP_DP = 513                               # tx_ifg_gasket GAP_CYCLES 512: next first beat 513 cycles after tlast
LEAD_NS = 11 * SYS_NS + 3 * DP_NS + 8 * DP_NS   # mailbox IDLE..LOAD, CDC, first beat packed
CTL_BEAT_DP, SR_BEAT_DP = 9, 1
SR_LEN, SR_PERIOD_NS = 90, 125_000.0
PRE, FCS, IFG, MIN = 8, 4, 12, 60


def wire_ns(length):
    return (PRE + max(length, MIN) + FCS) * OCTET_NS


def parse(path):
    txc, wire, holds, polls = [], [], [], []
    for line in open(path):
        f = line.split()
        if f[0] == 'TXC':
            txc.append((int(f[1]), int(f[2]), int(f[3])))
        elif f[0] == 'WIRE':
            wire.append((int(f[1]), int(f[3]), len(f[4]) // 2))
        elif f[0] == 'TXREADY':
            holds.append((int(f[1]), int(f[2])))
        elif f[0] == 'SPAN':
            polls.append((int(f[1]), int(f[3])))
    return txc, wire, holds, polls


def records(txc, wire):
    """Each departed record: (commit sys, ch, words, len, census wire sys), in census service order."""
    per_ch = {c: [] for c in range(5)}
    for t, c, n in wire:
        per_ch[c].append((t, n))
    head, idx, out = [0] * 5, [0] * 5, []
    for t, c, h in txc:
        delta = (h - head[c]) & 0xffff
        head[c] = h
        while delta > 0:
            if idx[c] >= len(per_ch[c]):
                raise ValueError(f'ch {c}: commit at {t} with no departure left')
            w_t, n = per_ch[c][idx[c]]
            idx[c] += 1
            words = 2 + (n + 3) // 4
            if words > delta:
                raise ValueError(f'ch {c}: record of {words} words over a commit of {delta}')
            delta -= words
            out.append(dict(c=t, ch=c, words=words, len=n, census=w_t))
    left = [len(per_ch[c]) - idx[c] for c in range(5)]
    return sorted(out, key=lambda r: r['census']), left


def hold_windows(holds):
    out, start = [], None
    for t, v in holds:
        if v == 0 and start is None:
            start = t * SYS_NS
        elif v == 1 and start is not None:
            out.append((start, t * SYS_NS))
            start = None
    if start is not None:
        out.append((start, float('inf')))
    return out


def replay(recs, holds, phase_ns, span_ns):
    sr = [phase_ns + n * SR_PERIOD_NS for n in range(int(span_ns // SR_PERIOD_NS) + 2)]
    sf = []                     # (wire_end, beats) of frames in the FIFO, by admission
    wire_free = mux_free = 0.0
    ctl_tlast = -1e18
    mbx_free = 0.0
    si = 0

    def admit(ready, beats, spacing, length):
        nonlocal wire_free, mux_free, sf
        f0 = max(ready, mux_free)
        sf = [x for x in sf if x[0] > f0 - 1e-9] if len(sf) > 64 else sf
        live = sorted(x for x in sf if x[0] > f0)
        if len(live) >= SF_FRAMES:
            f0 = live[len(live) - SF_FRAMES][0]
            live = [x for x in live if x[0] > f0]
        occ = sum(b for _, b in live)
        frees = [(e, b) for e, b in live]
        t, k, room = f0, 0, SF_BEATS - occ
        last = None
        for i in range(beats):
            t_i = f0 + spacing * DP_NS * i if last is None else max(last + spacing * DP_NS, f0 + spacing * DP_NS * i)
            while room < 1 and k < len(frees):
                t_i = max(t_i, frees[k][0])
                room += frees[k][1]
                k += 1
            while k < len(frees) and frees[k][0] <= t_i:
                room += frees[k][1]
                k += 1
            room -= 1
            last = t_i
            if i == 0:
                first = t_i
        a = last
        start = max(a, wire_free)
        end = start + wire_ns(length)
        wire_free = end + IFG * OCTET_NS
        mux_free = a + DP_NS
        sf.append((end, beats))
        return first, a, end

    out = []
    for r in recs:
        p0 = max(r['c'] * SYS_NS, mbx_free) + LEAD_NS
        for h0, h1 in holds:
            if h0 <= p0 < h1:
                p0 = h1
        ready = max(p0, ctl_tlast + GAP_DP * DP_NS)
        beats = (r['len'] + 7) // 8
        while si < len(sr) and sr[si] <= max(ready, mux_free):
            admit(sr[si], (SR_LEN + 7) // 8, SR_BEAT_DP, SR_LEN)
            si += 1
        first, a, end = admit(ready, beats, CTL_BEAT_DP, r['len'])
        for h0, h1 in holds:
            if first < h1 and a > h0:
                a += h1 - max(first, h0)
                end += h1 - max(first, h0)
        ctl_tlast = a
        mbx_free = a
        out.append(dict(r, tail=a, end=end, wait=end - r['c'] * SYS_NS))
    return out


def check(out, polls):
    by_ch = {c: [] for c in range(5)}
    for r in sorted(out, key=lambda r: r['c']):
        by_ch[r['ch']].append(r)
    fails = []
    for ch, rs in by_ch.items():
        for k, r in enumerate(rs):
            tau = rs[k - 1]['c'] * SYS_NS if k else 0.0
            # earliest census time with room for r: census tails of earlier records on ch
            used_c = lambda t: sum(x['words'] for x in rs[:k] if x['census'] * SYS_NS > t)
            # census room just after the previous commit; if short, the census passed later
            tc = tau
            if WORDS[ch] - used_c(tc) < r['words']:
                for x in sorted(rs[:k], key=lambda x: x['census']):
                    if x['census'] * SYS_NS > tc:
                        tc = x['census'] * SYS_NS
                        if WORDS[ch] - used_c(tc) >= r['words']:
                            break
            used_r = sum(x['words'] for x in rs[:k] if x['tail'] > tc)
            if WORDS[ch] - used_r < r['words']:
                fails.append(dict(ch=ch, k=k, commit=r['c'], tau=tc, room=WORDS[ch] - used_r, need=r['words']))
    aecp = sorted((r['census'] * SYS_NS, r['tail']) for r in out if r['ch'] == 2)
    moved = 0
    for p, cyc in polls:
        pt = p * SYS_NS
        for w, tl in aecp:
            if w <= pt + 200 and tl > pt:
                moved += 1
                break
    return fails, moved


def main():
    rows = []
    for path in sorted(Path(sys.argv[1]).glob('*.txt')):
        txc, wire, holds, polls = parse(path)
        recs, left = records(txc, wire)
        span = max((r['census'] for r in recs), default=0) * SYS_NS + 1e6
        worst = None
        for ph in range(8):
            out = replay(recs, hold_windows(holds), ph * SR_PERIOD_NS / 8, span)
            fails, moved = check(out, polls)
            w = max((r['wait'] for r in out), default=0)
            cand = dict(phase=ph, wait=w, fails=len(fails), first_fail=fails[:1], moved_polls=moved)
            if worst is None or (cand['fails'], cand['wait']) > (worst['fails'], worst['wait']):
                worst = cand
        rows.append(dict(case=path.stem, records=len(recs), left=left, polls=len(polls), holds=len(holds), **worst))
        print(json.dumps(rows[-1]), flush=True)
    Path(sys.argv[2]).write_text(json.dumps(rows, indent=1))


if __name__ == '__main__':
    main()
