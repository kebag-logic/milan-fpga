#!/usr/bin/env python3
"""Re-derive the Mark II class A shaper schedule (IEEE 802.1Q-2022 8.6.8.2).

Event-exact credit-based shaper over several 125 us intervals, one port,
idleSlope = sum of Milan v1.2 Table 4.4 reservations.  Frames of a phase
are all ready at the phase time; within a phase the smaller frame goes first.
Optionally one maximum-size lower-priority frame starts just before a phase.
"""
import itertools, sys

R = 1e9                       # portTransmitRate, b/s
AAF = 258 * 8                 # 8-channel AAF frame on the wire, bits
CRF = 88 * 8                  # CRF frame on the wire (Table 4.4 note: F=68, W=88)
BE = (1522 + 20) * 8          # interfering maximum frame
PER = 125e-6
PH = PER / 6

def run(loads, crf_phase, n_aaf_bw=16, crf=True, interfere=None, periods=6, idle=None):
    if idle is None:
        idle = (n_aaf_bw * 16576e3 + (5632e3 if crf else 0))
    send = idle - R
    # frames: (ready, bits, label)
    frames = []
    for p in range(periods):
        for ph in range(6):
            t = p * PER + ph * PH
            fl = []
            if crf and ph == crf_phase:
                fl.append(CRF)
            fl += [AAF] * loads[ph]
            for b in fl:
                frames.append((t, b, (p, ph)))
    # event-exact CBS for one queue, FIFO, with optional blocking frame
    t = 0.0; credit = 0.0; out = []
    block = []  # (start, end) intervals when the wire is held by lower priority
    if interfere is not None:
        for p in range(periods):
            for ph in interfere:
                s = p * PER + ph * PH - 1e-12
                block.append((s, s + BE / R))
    last_t = 0.0
    qi = 0
    while qi < len(frames):
        ready, bits, lab = frames[qi]
        # advance to ready if queue empty
        if t < ready:
            # queue empty from t to ready: credit rises at idle up to 0 if negative; positive resets to 0
            dt = ready - t
            credit = min(0.0, credit + idle * dt) if credit < 0 else 0.0
            t = ready
        # wait until credit >= 0 and wire free
        while True:
            busy = [b for b in block if b[0] <= t < b[1]]
            if busy:
                end = busy[0][1]
                credit += idle * (end - t)  # frames waiting: credit accrues (may go positive)
                t = end
                continue
            if credit < -1e-9:
                need = -credit / idle
                # check if a block would start in between
                nb = [b for b in block if t < b[0] < t + need]
                if nb:
                    credit += idle * (nb[0][0] - t); t = nb[0][0]; continue
                credit = 0.0; t += need
                continue
            break
        start = t
        dur = bits / R
        credit += send * dur
        t = start + dur
        out.append((lab, ready, start))
        qi += 1
    # wait per frame, steady-state from period 2 on
    worst = 0.0
    for (p, ph), ready, start in out:
        if p >= 2:
            worst = max(worst, start - ready)
    return worst, out

def main():
    pref = [3, 3, 2, 3, 3, 2]
    w, out = run(pref, 2)
    print("preferred 3,3,2,3,3,2 CRF@2: worst shaper wait %.3f us" % (w * 1e6))
    for (p, ph), r, s in out:
        if p == 2:
            print("  phase %d ready %.3f start %.3f" % (ph, (r - 2 * PER) * 1e6, (s - 2 * PER) * 1e6))
    res = []
    for light in itertools.combinations(range(6), 2):
        loads = [2 if i in light else 3 for i in range(6)]
        for c in range(6):
            w, _ = run(loads, c)
            res.append((w, loads, c))
    res.sort(reverse=True)
    print("orders evaluated:", len(res))
    for w, l, c in res[:5]:
        print("  wait %.3f us loads %s CRF@%d" % (w * 1e6, l, c))
    wi = max(run(pref, 2, interfere=[ph])[0] for ph in range(6))
    print("preferred with one interfering max frame just before a phase: %.3f us" % (wi * 1e6))
    wl, l, c = res[0]
    wi2 = max(run(l, c, interfere=[ph])[0] for ph in range(6))
    print("worst order with one interfering max frame: %.3f us (bound %.3f)" % (wi2 * 1e6, wl * 1e6 + BE / R * 1e6))
    # smaller loads: k co-phased streams alone (idleSlope from k reservations, no CRF)
    for k in (1, 2, 3):
        loads = [k, 0, 0, 0, 0, 0]
        w, _ = run(loads, 0, n_aaf_bw=k, crf=False)
        wc, _ = run(loads, 0, n_aaf_bw=k, crf=True)
        print("k=%d co-phased alone: wait %.3f us (with a CRF reservation and frame: %.3f us)" % (k, w * 1e6, wc * 1e6))

if __name__ == "__main__":
    main()
