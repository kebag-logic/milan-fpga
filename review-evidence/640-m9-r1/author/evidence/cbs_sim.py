"""Byte-time stepped model of one talker port (8 ns per tick at 1 Gb/s).

Class A: credit-based shaper per IEEE 802.1Q-2022 8.6.8.2 (credit rises at
idleSlope while transmit is FALSE, falls at sendSlope while TRUE, is set to
zero when the queue is empty and credit is positive; a frame is eligible when
credit >= 0). Best effort: strict priority below class A (8.6.8.1), optionally
saturated. Sizes are wire bytes including preamble, SFD and IFG.
Reports, per stream, the worst wait from eligibility to first bit.
"""
import random
import sys

R = 1_000_000_000            # portTransmitRate, bit/s
TICK_NS = 8                  # one byte time
T_INT = 125_000              # class A interval, ns
T_SMP = T_INT / 6            # 48 kHz sample period, ns


def aaf_wire(n):
    return 24 * n + 24 + 22 + 20          # AVTPDU + Ethernet/VLAN/FCS + preamble/IFG


def aaf_w(n):
    return 24 * n + 24 + 1 + 22 + 20      # Milan v1.2 Table 4.4 W, bandwidth basis


CRF_WIRE = 88                              # 28-octet AVTPDU, padded to 68, plus 20
CRF_W = 88
BE_MAX = 1522 + 20                         # largest tagged frame plus preamble and IFG


def simulate(streams, cycles=24, be=None, seed=0, be_offset_ns=0):
    """streams: list of (phase, wire_bytes, w_bytes, extra_offset_ns).
    be: None, 'max' (saturated 1542-byte frames) or 'rand' (random sizes).
    Returns (worst wait ns per stream, idleSlope bit/s)."""
    rnd = random.Random(seed)
    idle = sum(w * 8 * 8000 for (_, _, w, _) in streams)
    send = idle - R
    arr = []
    for c in range(cycles):
        for i, (ph, wire, _w, off) in enumerate(streams):
            t_ns = c * T_INT + ph * T_SMP + off
            arr.append((int(-(-t_ns // TICK_NS)), i, wire))
    arr.sort(key=lambda a: (a[0], a[2], a[1]))     # ties: smaller frame first
    end_tick = cycles * T_INT // TICK_NS + 20_000
    q = []
    ai = 0
    credit = 0.0                 # bits
    cur = None                   # 'A' or 'BE'
    left = 0                     # bytes left on the wire for the current frame
    be_start = be_offset_ns // TICK_NS
    waits = {}
    d_idle = idle * TICK_NS / 1e9
    d_send = send * TICK_NS / 1e9
    for now in range(end_tick):
        while ai < len(arr) and arr[ai][0] <= now:
            q.append(arr[ai])
            ai += 1
        if left == 0:
            cur = None
            if q and credit >= 0:
                at, i, wire = q.pop(0)
                # only measure after the warm-up cycles
                if at * TICK_NS >= 4 * T_INT:
                    waits[i] = max(waits.get(i, 0), (now - at) * TICK_NS)
                cur, left = 'A', wire
            elif be and now >= be_start:
                size = BE_MAX if be == 'max' else rnd.choice((84, 84, 600, 1100, BE_MAX, BE_MAX))
                cur, left = 'BE', size
        if cur == 'A':
            credit += d_send
        else:
            credit += d_idle
            if not q and credit > 0:
                credit = 0.0
        if left:
            left -= 1
        if ai >= len(arr) and not q and left == 0 and now * TICK_NS > cycles * T_INT:
            break
    return waits, idle


def full_load(groups, n_ch=8, crf_phase=None):
    """groups: streams per phase, e.g. (3, 3, 2, 3, 3, 2)."""
    s = []
    for ph, k in enumerate(groups):
        for _ in range(k):
            s.append((ph, aaf_wire(n_ch), aaf_w(n_ch), 0))
    if crf_phase is not None:
        s.append((crf_phase, CRF_WIRE, CRF_W, 0))
    return s


def report(name, streams, be=None, seeds=1, offsets=(0,)):
    worst = 0
    idle = 0
    for seed in range(seeds):
        for off in offsets:
            w, idle = simulate(streams, be=be, seed=seed, be_offset_ns=off)
            worst = max(worst, max(w.values()))
    print(f"{name}: streams={len(streams)} idleSlope={idle/1e6:.3f} Mb/s "
          f"({100*idle/R:.2f} %) worst wait={worst/1000:.3f} us be={be}", flush=True)
    return worst


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    offs = tuple(range(0, 20_000, 1_000))
    if mode in ("all", "full"):
        for g in ((3, 3, 3, 3, 2, 2), (3, 3, 2, 3, 3, 2), (3, 2, 3, 2, 3, 3)):
            report(f"full {g}", full_load(g))
            report(f"full {g} +CRF@2", full_load(g, crf_phase=2))
            report(f"full {g} +CRF@2 BEmax", full_load(g, crf_phase=2), be='max', offsets=offs)
            report(f"full {g} +CRF@2 BErand", full_load(g, crf_phase=2), be='rand', seeds=8, offsets=offs[::4])
    if mode in ("all", "partial"):
        report("lone pair, phase 0", full_load((2, 0, 0, 0, 0, 0)))
        report("lone triple, phase 0", full_load((3, 0, 0, 0, 0, 0)))
        report("pair, phases 0 and 1", full_load((1, 1, 0, 0, 0, 0)))
        report("pair, phases 0 and 3", full_load((1, 0, 0, 1, 0, 0)))
        report("lone triple BEmax", full_load((3, 0, 0, 0, 0, 0)), be='max', offsets=offs)
