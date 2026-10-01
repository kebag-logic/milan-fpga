#!/usr/bin/env python3
"""Independent group-level model of the #629 AAF meter under independent PDU
loss, driving a model of KL_mmcm_drp_servo's PI and lock rule.

Written from the design page's rules at head f4f0ecb4 (Lost PDUs, rules 1-4;
E8; the servo lines 562-579 and 609-648), not from the author's model.

Exactness argument for the group-level reduction: with independent timestamp
error of +/-1,042 ns at 0 ppm no deviation void (2J = 2,084 < 4,096), no
adjacent spacing failure (< 4,096) and no k = 2 failure (< 5,120) can occur,
so only the loss pattern restarts the history. A group is voided with
probability q = 1 - (1 - p)^16, independently of every other group, which is
exactly what PDU-level Bernoulli(p) loss gives. A run of >= 2 voided groups
restarts the history at the next valid pick; one voided group is skipped and,
when it is a snapshot group, filled by the midpoint of its neighbours.

Servo: windows every 512 ms from phase PHI; e = locerr - rate, locerr =
L0 - u (plant gain 1, the command set at a boundary applies over the next
window) + uniform +/-20 ns; integ += e >> 1, u = integ + (e >> 2); lock_cnt
counts |e| < 1,024, LOCKED at 4, ACQUIRE when it falls to 0; an invalid rate
holds PI and lock_cnt.

Usage: random_loss_model.py <lost_per_s> <seconds> <seeds> [phi] [seed_base]
"""
import sys
import numpy as np

J = 1042.0
L0 = 5448  # 10.64 ppm x 512 ms
PER_S = 500  # groups per second
GROUP_NS = 2_000_000


def run(p, secs, seed, phi):
    rng = np.random.default_rng(seed)
    G = int(secs * PER_S)
    q = 1.0 - (1.0 - p) ** 16
    void = rng.random(G) < q
    err = np.floor(rng.uniform(-J, J, (G, 16)).mean(axis=1))
    pick = np.arange(G, dtype=np.int64) * GROUP_NS + err.astype(np.int64)

    # history start/restart groups: first valid group, then the first valid
    # group after each run of >= 2 voided groups
    restart_at = np.full(G, -1, dtype=np.int64)
    starts = []
    first = int(np.argmax(~void))
    starts.append(first)
    # run lengths of voided groups ending right before a valid group
    v = void.astype(np.int8)
    idx = np.flatnonzero(~void)
    # for each valid group, length of the voided run before it
    prev_valid = np.empty_like(idx)
    prev_valid[0] = -1
    prev_valid[1:] = idx[:-1]
    runlen = idx - prev_valid - 1
    restarts = idx[(runlen >= 2) & (idx > first)]
    starts.extend(restarts.tolist())
    marks = np.zeros(G, dtype=np.int64) - 1
    marks[np.array(starts)] = np.array(starts)
    last_start = np.maximum.accumulate(marks)

    def snap(s):
        if not void[s]:
            return int(pick[s])
        a, b = int(pick[s - 1]), int(pick[s + 1])
        return a + ((b - a) >> 1)

    # servo
    t = phi
    u = 0
    integ = 0
    lock = 0
    state = "ACQ"
    first_locked = None
    drops = 0
    valid_n = 0
    win_n = 0
    while True:
        t += 0.512
        if t >= secs - 0.01:
            break
        # last completed pick at time t: group g completes at (g+1)*2ms-125us
        g_now = int((t + 125e-6) / 2e-3) - 1
        if g_now < 0:
            continue
        g_r = int(last_start[g_now])
        valid = False
        rate = 0
        if g_r >= 0:
            cnt = g_now - g_r
            m = cnt // 256
            s = g_r + 256 * m
            if void[s] and s == g_now:
                m -= 1  # fill written one group later
                s -= 256
            if m >= 8:
                valid = True
                rate = (snap(s) - snap(s - 2048) - 8 * 512_000_000) >> 3
        if t >= 8.4:
            win_n += 1
            valid_n += valid
        locerr = L0 - u + int(rng.integers(-20, 21))
        e = locerr - rate
        if valid:
            integ = integ + (e >> 1)
            u = integ + (e >> 2)
            if -1024 < e < 1024:
                lock = min(lock + 1, 4)
            else:
                lock = 0
            if state == "ACQ" and lock >= 4:
                state = "LOCKED"
                if first_locked is None:
                    first_locked = t
            elif state == "LOCKED" and lock == 0:
                state = "ACQ"
                drops += 1
    return dict(restarts=len(restarts), secs=secs, valid=valid_n / max(win_n, 1),
                locked=first_locked, drops=drops)


def main():
    lost = float(sys.argv[1])
    secs = float(sys.argv[2])
    seeds = int(sys.argv[3])
    sys.argv = [a for a in sys.argv if a != '--raw'] + (['--raw'] if '--raw' in sys.argv else [])
    phi = float(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != '--raw' else 0.13
    p = lost / 8000.0
    base = int(sys.argv[5]) if len(sys.argv) > 5 else 1000
    res = [run(p, secs, base + s, phi) for s in range(seeds)]
    rr = sum(r["restarts"] for r in res) / (secs * seeds)
    val = np.mean([r["valid"] for r in res])
    lk = np.array([r["locked"] if r["locked"] is not None else np.inf for r in res])
    nolock = int(np.sum(~np.isfinite(lk)))
    drops = sum(r["drops"] for r in res)
    fl = lk[np.isfinite(lk)]
    q25, med, q75 = np.percentile(fl, [25, 50, 75]) if len(fl) else (np.nan,) * 3
    if "--raw" in sys.argv:
        print("RAW", " ".join(f"{x:.3f}" for x in lk))
    print(f"lost/s {lost:g} p {p:.2e} secs {secs:g} seeds {seeds} phi {phi}: "
          f"restarts/s {rr:.4f}; valid {val:.4f}; LOCKED median {med:.1f} s, "
          f"middle half {q25:.1f}-{q75:.1f} s, slowest {fl.max() if len(fl) else float('nan'):.1f} s; "
          f"never locked {nolock}; LOCKED drops {drops}")


if __name__ == "__main__":
    main()
