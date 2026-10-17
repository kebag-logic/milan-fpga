#!/usr/bin/env python3
"""Lane B21 step 1 analysis: the capture-path self-test's read record, with lane B5's definitions.

usage: b21_selftest_ana.py <raw_run_dir> <out_dir>

Imports b5_attrib.py (lane B5 round 2, unchanged) for its definitions: a stall is a read interval
over STALL_MS (15 ms, grade_a.py's); the delivery deficit D(r) = t(r) * 48000 - 480 r frames; the
floor step across reads a .. b is min D[b + GA .. b + GA + W] - min D[a - GB - W .. a - GB]; a
step "matches" within TOL frames.

Writes <out_dir>/<run>-reads.u16 (b5_attrib's derived-record encoding: uint16 LE differences of the
monotonic time since the window's first read, rounded to 1 us), <run>-reads.json and
<run>-selftest.txt. The window is every read that delivered exactly one period (480 frames),
from the first such read to the last.

Host evidence (host-samples.bin, host_sampler_b21.py): for each stall, the change in summed steal
time and in each interrupt row across the stall against the median over clear 0.05 s samples.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b5_attrib as b5  # noqa: E402

FS, PER, STALL_MS, W, GB, GA, TOL, MS1 = b5.FS, b5.PER, b5.STALL_MS, b5.W, b5.GB, b5.GA, b5.TOL, b5.MS1


def pct(x, q=(0, 1, 50, 99, 100)):
    return b5.pct(x, q)


def main(raw, out):
    raw, out = Path(raw), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    name = raw.name
    src = raw / "cap-ts.bin"
    ts = np.fromfile(src, dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
    F, RT, MONO = ts["f"].astype(np.int64), ts["rt"], ts["mono"].astype(np.int64)
    dF = np.diff(np.concatenate(([0], F)))
    full = np.flatnonzero(dF == PER)
    j0, j1 = int(full[0]), int(full[-1])
    # the window: reads j0 .. j1; every read inside must be one period
    odd = [(int(i), int(dF[i])) for i in range(j0 + 1, j1 + 1) if dF[i] != PER]
    lines = []
    p = lines.append
    p(f"== {name}: inputs")
    p(f"read-time record {src.name}: {src.stat().st_size} B sha256 {b5.sha256(src)}; {len(ts)} reads, {int(F[-1])} frames")
    p(f"reads not of one period inside the window: {len(odd)} {odd[:20]}")
    p(f"window: reads {j0} .. {j1} ({j1 - j0} intervals), frames {int(F[j0])} .. {int(F[j1])}")
    cum_us = np.rint((MONO[j0:j1 + 1] - MONO[j0]) / 1000.0).astype(np.int64)
    d = np.diff(cum_us)
    assert d.min() >= 0
    # b5_attrib.py's uint16 encoding when every interval fits; uint32 otherwise (a read interval of
    # 65.536 ms or more)
    enc = "<u2" if d.max() < 65536 else "<u4"
    rec = out / f"{name}-reads.{'u16' if enc == '<u2' else 'u32'}"
    d.astype(enc).tofile(rec)
    meta = dict(source=dict(file=f"{name}/cap-ts.bin", bytes=src.stat().st_size, sha256=b5.sha256(src)),
                window_frames=[int(F[j0]), int(F[j1])], window_read_indices=[j0, j1], reads=int(len(d)),
                reads_not_one_period=odd,
                frames_per_read=PER, clock="monotonic", unit="us",
                encoding=("uint16" if enc == "<u2" else "uint32") + " LE: differences of the cumulative time rounded to 1 us (b5_attrib.py's, widened when needed)",
                elapsed_ns_exact=int(MONO[j1] - MONO[j0]), elapsed_us_record=int(cum_us[-1]),
                record=dict(file=rec.name, bytes=rec.stat().st_size, sha256=b5.sha256(rec)),
                b5_attrib_sha256=b5.sha256(Path(b5.__file__)))
    json.dump(meta, open(out / f"{name}-reads.json", "w"), indent=1)
    p(f"derived record {rec.name}: {rec.stat().st_size} B sha256 {meta['record']['sha256']}")
    p(f"b5_attrib.py sha256 {meta['b5_attrib_sha256']}")

    R = len(d)
    t = np.concatenate(([0], np.cumsum(d))) / 1e6
    # the deficit uses the frames each read actually delivered (one read after a stall may
    # deliver two periods), not 480 per read as in b5_attrib.py, whose window had none
    Fw = (F[j0:j1 + 1] - F[j0]).astype(np.float64)
    D = t * FS - Fw
    g = np.concatenate(([np.nan], d / 1e3))
    dur = t[-1]
    p("== window and rate")
    p(f"window {dur:.3f} s on the monotonic clock ({dur / 60:.2f} min); {int(Fw[-1])} frames delivered")
    A = np.vstack([t, np.ones_like(t)]).T
    slope, icpt = np.linalg.lstsq(A, D, rcond=None)[0]
    p(f"deficit D(R) - D(0) = {D[-1]:.1f} frames; linear fit slope {slope:+.3f} frames/s "
      f"= {1e6 * slope / FS:+.2f} ppm (capture clock against this host's monotonic clock, uncalibrated)")
    res = D - (slope * t + icpt)
    p(f"deficit residual after the linear fit, frames, percentiles 0/1/50/99/100: {pct(res)}")

    p("== read intervals and stalls (read interval over 15 ms)")
    p(f"read interval ms, percentiles 0/1/50/99/100: {pct(g[1:])}; over 12 ms: {(g[1:] > 12).sum()}, over 15 ms: {(g[1:] > STALL_MS).sum()}")
    st = np.flatnonzero(g[1:] > STALL_MS) + 1
    if len(st):
        ex = (g[st] - 10.0) * FS / 1000
        p(f"stalls {len(st)}; excess over the 10 ms period {ex.sum():.1f} frames; interval {g[st].min():.2f} .. {g[st].max():.2f} ms")
        if len(st) > 1:
            sp = np.diff(t[st])
            p(f"recurrence: spacing median {np.median(sp):.4f} s, min {sp.min():.3f} s, max {sp.max():.3f} s")
        for k in st[:40]:
            p(f"  stall at read {k}, t {t[k]:.3f} s, interval {g[k]:.2f} ms")
    else:
        p("stalls 0")

    p("== delivery-deficit floor steps (lane B5's floor test)")

    def step(a, b):
        lo, hi = a - GB - W, b + GA + W
        if lo < 0 or hi > R:
            return None
        return float(D[b + GA:hi + 1].min() - D[lo:a - GB + 1].min())

    pos = list(range(GB + W, R - GA - W))
    x = np.array([step(r, r) for r in pos])
    # the clocks' drift over one floor test, taken as the median step over all positions (robust to
    # the steps themselves, which pull a whole-window linear fit)
    drift = float(np.median(x))
    p(f"positions {len(pos)}; drift over one floor test (median step) {drift:+.3f} frames; step percentiles 0.01/1/50/99/99.99: "
      f"{pct(x, (0.01, 1, 50, 99, 99.99))}")
    big = np.flatnonzero(np.abs(x - drift) > TOL)
    grp = []
    for i in big:
        if grp and pos[i] - grp[-1][-1] <= 2 * b5.JOIN:
            grp[-1].append(pos[i])
        else:
            grp.append([pos[i]])
    gmax = [max((x[pos.index(r)] for r in gg), key=lambda v: abs(v - drift)) for gg in grp]
    p(f"positions with |step - drift| > {TOL:.0f} frames: {len(big)}, in {len(grp)} groups; "
      f"{sum(1 for v in gmax if abs(v - drift - MS1) <= TOL)} of them a 1 ms (48-frame) step")
    for gg, v in zip(grp[:60], gmax[:60]):
        p(f"  group at reads {gg[0]} .. {gg[-1]} (t {t[gg[0]]:.3f} s): largest step {v:+.1f} frames")
    loss_frames = sum(max(0.0, v - drift) for v in gmax)
    p(f"sum of the positive group steps: {loss_frames:.1f} frames")

    # content of the two AES channels (any input; reported only)
    lr = raw / "cap-lr.raw"
    b = np.fromfile(lr, dtype=np.uint8)
    n = len(b) // 6
    w = b[:n * 6].reshape(n, 2, 3).astype(np.int64)
    w = w[:, :, 0] | (w[:, :, 1] << 8) | (w[:, :, 2] << 16)
    p("== content of the two AES channels (any input; not graded)")
    p(f"{lr.name}: {lr.stat().st_size} B sha256 {b5.sha256(lr)}; frames {n}; all-zero frames {int(((w[:, 0] == 0) & (w[:, 1] == 0)).sum())}; "
      f"distinct words ch0 {len(np.unique(w[:, 0]))}, ch1 {len(np.unique(w[:, 1]))}")

    hs = raw / "host-samples.bin"
    if hs.exists() and len(st):
        p("== host evidence around each stall (host_sampler_b21.py, 20 Hz)")
        S = [json.loads(l) for l in open(hs)]
        sm = np.array([s["m"] for s in S], dtype=np.int64)
        steal = np.array([s["cpu"][7] for s in S], dtype=np.int64)
        labels = sorted(set().union(*[s["irq"].keys() for s in S[:5]]))
        irq = {k: np.array([s["irq"].get(k, 0) for s in S], dtype=np.int64) for k in labels}
        dsteal = np.diff(steal)
        base = np.median(dsteal)
        mono_read = MONO[j0:j1 + 1]
        rows = []
        for k in st:
            a_ns, b_ns = mono_read[k - 1], mono_read[k]
            i0 = max(0, int(np.searchsorted(sm, a_ns)) - 1)
            i1 = min(len(sm) - 1, int(np.searchsorted(sm, b_ns)) + 1)
            dst = int(steal[i1] - steal[i0])
            exp = base * (i1 - i0)
            hot = []
            for lab, v in irq.items():
                dv = int(v[i1] - v[i0])
                med = float(np.median(np.diff(v))) * (i1 - i0)
                if dv - med >= 3:
                    hot.append((lab[-38:], dv, round(med, 1)))
            rows.append((k, round(float(g[k]), 2), dst, round(float(exp), 1), hot[:6]))
        p(f"steal-time ticks per 0.05 s sample, median {base}; per stall: read, interval ms, steal ticks across it, expected, irq rows over their median")
        for r in rows[:60]:
            p(f"  {r}")
    if hs.exists():
        # the USB controller's interrupt row (one per 1 ms USB frame): 50 per 0.05 s sample;
        # a shortfall that is not made up later means USB frame events missing on the host side
        S = [json.loads(l) for l in open(hs)]
        sm = np.array([s["m"] for s in S], dtype=np.int64)
        tt = (sm - MONO[j0]) / 1e9
        usb = [k for k in S[0]["irq"] if "xhci" in k]
        p("== USB controller interrupts (host_sampler_b21.py, 20 Hz)")
        for k in usb:
            v = np.array([s["irq"].get(k, 0) for s in S], dtype=np.int64)
            dv = np.diff(v)
            rate = (v[-1] - v[0]) / (tt[-1] - tt[0])
            p(f"{k[-34:]}: {rate:.1f} per s; per-sample counts percentiles 0/1/50/99/100 {pct(dv)}")
            if rate < 100:
                continue
            exp = rate * np.diff(tt)
            cum = np.cumsum(dv - exp)
            # sustained shortfall: the cumulative excess falls by 5 or more over 1 s and stays down 1 s later
            for T in [t[k2] for k2 in st] + [t[gg[0]] for gg in grp]:
                i = int(np.searchsorted(tt[1:], T))
                a, b = max(0, i - 20), min(len(cum) - 1, i + 40)
                p(f"  at t {T:8.3f} s: cumulative interrupt excess from 1 s before to 2 s after {cum[b] - cum[a]:+.1f}; "
                  f"slice counts {list(dv[max(0, i - 2):i + 4])}")
        if "psi" in S[0]:
            p("== pressure and vmstat counters around stalls and steps (from 1 s before to 1 s after)")
            for T in [t[k2] for k2 in st] + [t[gg[0]] for gg in grp]:
                i = int(np.searchsorted(tt, T))
                a, b = max(0, i - 20), min(len(S) - 1, i + 20)
                dpsi = {kk: S[b]["psi"][kk] - S[a]["psi"][kk] for kk in S[a]["psi"] if S[b]["psi"][kk] != S[a]["psi"][kk]}
                dvm = {kk: S[b]["vm"][kk] - S[a]["vm"][kk] for kk in S[a]["vm"] if S[b]["vm"][kk] != S[a]["vm"][kk]}
                p(f"  t {T:8.3f} s: psi us {dpsi}; vmstat {dvm}")
    if hs.exists():
        # per event class: the USB controller's interrupt shortfall over 2 s (1 s before to 1 s after)
        # and, when sampled, the pressure rates over the same span, against clear control times
        S = [json.loads(l) for l in open(hs)]
        sm = np.array([s["m"] for s in S], dtype=np.int64)
        tt = (sm - MONO[j0]) / 1e9
        usb = [k for k in S[0]["irq"] if "xhci" in k]
        uk = max(usb, key=lambda k: S[-1]["irq"][k] - S[0]["irq"][k])
        uv = np.array([s["irq"][uk] for s in S], dtype=np.float64)
        urate = (uv[-1] - uv[0]) / (tt[-1] - tt[0])
        has_psi = "psi" in S[0]
        def at(T):
            i = int(np.searchsorted(tt, T))
            a, b = max(0, i - 20), min(len(S) - 1, i + 20)
            short = urate * (tt[b] - tt[a]) - (uv[b] - uv[a])
            r = dict(usb_short=short)
            if has_psi:
                for kk in ("io_full", "memory_full", "cpu_some"):
                    r[kk] = (S[b]["psi"][kk] - S[a]["psi"][kk]) / (tt[b] - tt[a]) / 1e3   # ms per s
            return r
        gpos = {gg[0]: v for gg, v in zip(grp, gmax)}
        lossy = [t[a] for a, v in gpos.items() if v - drift > MS1 + TOL]
        onems = [t[a] for a, v in gpos.items() if abs(v - drift - MS1) <= TOL]
        stall_only = [t[k2] for k2 in st if not any(gg[0] - 20 <= k2 <= gg[-1] + 20 for gg in grp)]
        rng = np.random.default_rng(21)
        evt = sorted(set(lossy + onems + [t[k2] for k2 in st]))
        clear = [T for T in rng.uniform(2, t[-1] - 2, 4000) if all(abs(T - e) > 3 for e in evt)][:300]
        p("== event classes against clear times (2 s spans; USB interrupt shortfall in interrupts, pressure in ms per s)")
        for nm, ts_ in (("floor steps over 1 ms (losses)", lossy), ("1 ms floor steps", onems),
                        ("stalls with no floor step", stall_only), ("clear control times", clear)):
            if not ts_:
                p(f"{nm}: 0")
                continue
            rs = [at(T) for T in ts_]
            line = f"{nm}: {len(ts_)}; USB shortfall median {np.median([r['usb_short'] for r in rs]):+.1f}, max {max(r['usb_short'] for r in rs):+.1f}"
            if has_psi:
                for kk in ("io_full", "memory_full", "cpu_some"):
                    v = [r[kk] for r in rs]
                    line += f"; {kk} median {np.median(v):.2f}, p90 {np.percentile(v, 90):.2f}"
            p(line)
        for nm, ts_ in (("losses", lossy),):
            for T in ts_:
                r = at(T)
                p(f"  loss at t {T:8.3f} s: step {gpos[[a for a in gpos if abs(t[a] - T) < 1e-9][0]]:+.1f} frames, USB shortfall {r['usb_short']:+.1f}"
                  + (f", io_full {r['io_full']:.1f}, memory_full {r['memory_full']:.1f}, cpu_some {r['cpu_some']:.1f} ms/s" if has_psi else ""))
    text = "\n".join(lines) + "\n"
    (out / f"{name}-selftest.txt").write_text(text)
    print(text)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
