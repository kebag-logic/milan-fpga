#!/usr/bin/env python3
"""Lane B21 round 3: analysis of the McASP capture path's per-read timing record (offline).

usage: b21_mcasp_ana.py <raw_run_dir> <name> <out_dir>

Inputs from the board (b21stamp, mcasp_selftest_b21.sh or the direction runs): <name>.ts
(<q frames_after_read, d realtime, q monotonic_ns> per read), <name>.arecord.log, <name>.stamp.log
and <name>.samp (1 Hz: /proc/uptime, the McASP DMA interrupt rows, /proc/stat's cpu line).

Definitions are lane B5's (b5_attrib.py, imported unchanged): a stall is a read interval over
15 ms; the delivery deficit D = t * 48000 - frames delivered; the floor step across a read
compares the deficit's floor over W reads on each side (GB, GA guards); a step "matches" within
TOL frames. As in round 1, the deficit counts the frames each read delivered, and the drift over
one floor test is the median step. A loss inside the capture path after sampling raises the floor
for good; ALSA reports it as an overrun, which arecord logs.

Writes <out_dir>/<name>-reads.u16|u32 (round 1's derived-record encoding), <name>-reads.json and
<name>-analysis.txt.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b5_attrib as b5  # noqa: E402

FS, PER, STALL_MS, W, GB, GA, TOL, MS1 = b5.FS, b5.PER, b5.STALL_MS, b5.W, b5.GB, b5.GA, b5.TOL, b5.MS1


def main(raw, name, out):
    raw, out = Path(raw), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    src = raw / f"{name}.ts"
    ts = np.fromfile(src, dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
    F, MONO = ts["f"].astype(np.int64), ts["mono"].astype(np.int64)
    dF = np.diff(np.concatenate(([0], F)))
    lines = []
    p = lines.append
    p(f"== {name}: inputs")
    p(f"read-time record {src.name}: {src.stat().st_size} B sha256 {b5.sha256(src)}; {len(ts)} reads, {int(F[-1])} frames")
    vals, cnts = np.unique(dF, return_counts=True)
    p(f"frames per read: {dict(zip(vals.tolist(), cnts.tolist()))}")
    full = np.flatnonzero(dF == PER)
    j0, j1 = int(full[0]), int(full[-1])
    odd = [(int(i), int(dF[i])) for i in range(j0 + 1, j1 + 1) if dF[i] != PER]
    p(f"window: reads {j0} .. {j1} ({j1 - j0} intervals), frames {int(F[j0])} .. {int(F[j1])}; reads not of one period inside: {len(odd)} {odd[:20]}")
    cum_us = np.rint((MONO[j0:j1 + 1] - MONO[j0]) / 1000.0).astype(np.int64)
    d = np.diff(cum_us)
    assert d.min() >= 0
    enc = "<u2" if d.max() < 65536 else "<u4"
    rec = out / f"{name}-reads.{'u16' if enc == '<u2' else 'u32'}"
    d.astype(enc).tofile(rec)
    alog = (raw / f"{name}.arecord.log").read_text(errors="replace")
    over = re.findall(r"overrun!!! \(at least ([0-9.]+) ms long\)", alog)
    slog = (raw / f"{name}.stamp.log").read_text(errors="replace").strip()
    meta = dict(source=dict(file=src.name, bytes=src.stat().st_size, sha256=b5.sha256(src)),
                window_frames=[int(F[j0]), int(F[j1])], window_read_indices=[j0, j1], reads=int(len(d)),
                reads_not_one_period=odd, frames_per_read=PER, clock="board monotonic", unit="us",
                encoding=("uint16" if enc == "<u2" else "uint32") + " LE: differences of the cumulative time rounded to 1 us",
                elapsed_ns_exact=int(MONO[j1] - MONO[j0]),
                record=dict(file=rec.name, bytes=rec.stat().st_size, sha256=b5.sha256(rec)),
                arecord_overruns=len(over), arecord_overrun_ms=over, stamper=slog,
                b5_attrib_sha256=b5.sha256(Path(b5.__file__)))
    json.dump(meta, open(out / f"{name}-reads.json", "w"), indent=1)
    p(f"derived record {rec.name}: {rec.stat().st_size} B sha256 {meta['record']['sha256']}; b5_attrib.py sha256 {meta['b5_attrib_sha256']}")
    p(f"arecord overruns: {len(over)} {over[:20]}; stamper: {slog}")

    R = len(d)
    t = np.concatenate(([0], np.cumsum(d))) / 1e6
    Fw = (F[j0:j1 + 1] - F[j0]).astype(np.float64)
    D = t * FS - Fw
    g = np.concatenate(([np.nan], d / 1e3))
    dur = t[-1]
    p("== window and rate")
    p(f"window {dur:.3f} s on the board's monotonic clock ({dur / 60:.2f} min); {int(Fw[-1])} frames delivered")
    A = np.vstack([t, np.ones_like(t)]).T
    slope, icpt = np.linalg.lstsq(A, D, rcond=None)[0]
    p(f"deficit D(R) - D(0) = {D[-1]:.1f} frames; linear fit slope {slope:+.4f} frames/s = {1e6 * slope / FS:+.2f} ppm "
      f"(the DUT's TDM clock against the board's monotonic clock, uncalibrated)")
    res = D - (slope * t + icpt)
    p(f"deficit residual after the linear fit, frames, percentiles 0/1/50/99/100: {b5.pct(res, (0, 1, 50, 99, 100))}")
    p("== read intervals and stalls (read interval over 15 ms)")
    p(f"read interval ms, percentiles 0/0.01/1/50/99/99.99/100: {b5.pct(g[1:], (0, 0.01, 1, 50, 99, 99.99, 100))}; "
      f"over 12 ms: {(g[1:] > 12).sum()}, over 15 ms: {(g[1:] > STALL_MS).sum()}")
    st = np.flatnonzero(g[1:] > STALL_MS) + 1
    p(f"stalls {len(st)}" + (f"; longest {g[st].max():.2f} ms" if len(st) else ""))
    for k in st[:40]:
        p(f"  stall at read {k}, t {t[k]:.3f} s, interval {g[k]:.2f} ms")
    if len(st) > 1:
        sp = np.diff(t[st])
        p(f"stall spacings of 2.99 to 3.02 s: {int(((sp >= 2.99) & (sp <= 3.02)).sum())}")
    p("== delivery-deficit floor steps (lane B5's floor test)")

    def step(a):
        lo, hi = a - GB - W, a + GA + W
        if lo < 0 or hi > R:
            return None
        return float(D[a + GA:hi + 1].min() - D[lo:a - GB + 1].min())

    pos = list(range(GB + W, R - GA - W))
    x = np.array([step(r) for r in pos])
    drift = float(np.median(x))
    p(f"positions {len(pos)}; drift over one floor test (median step) {drift:+.3f} frames; step percentiles 0/0.01/1/50/99/99.99/100: "
      f"{b5.pct(x, (0, 0.01, 1, 50, 99, 99.99, 100))}")
    big = np.flatnonzero(np.abs(x - drift) > TOL)
    grp = []
    for i in big:
        if grp and pos[i] - grp[-1][-1] <= 2 * b5.JOIN:
            grp[-1].append(pos[i])
        else:
            grp.append([pos[i]])
    gmax = [max((x[pos.index(r)] for r in gg), key=lambda v: abs(v - drift)) for gg in grp]
    p(f"positions with |step - drift| > {TOL:.0f} frames: {len(big)}, in {len(grp)} groups")
    for gg, v in zip(grp[:60], gmax[:60]):
        p(f"  group at reads {gg[0]} .. {gg[-1]} (t {t[gg[0]]:.3f} s): largest step {v:+.1f} frames")
    p(f"sum of the positive group steps: {sum(max(0.0, v - drift) for v in gmax):.1f} frames")
    # a loss after sampling raises the floor for good: the floor over consecutive 10 s blocks
    # (1,000 reads), less a straight line fitted to those floors, shows any permanent step
    wn = 1000
    starts = list(range(0, len(D) - wn + 1, wn))
    fl = np.array([D[a:a + wn].min() for a in starts])
    tc = np.array([t[a] for a in starts])
    if len(fl) > 2:
        s10, i10 = np.polyfit(tc, fl, 1)
        r10 = fl - (s10 * tc + i10)
        p(f"== permanent-step check: floors of {len(fl)} consecutive 10 s blocks, less their linear fit "
          f"({s10:+.4f} frames/s): residual min {r10.min():+.2f}, max {r10.max():+.2f} frames; "
          f"largest block-to-block change {np.abs(np.diff(r10)).max():.2f} frames")

    sp_ = raw / f"{name}.samp"
    if sp_.exists():
        txt = sp_.read_text(errors="replace").splitlines()
        up, ch = [], {"chan0": [], "chan1": []}
        cur = None
        for ln in txt:
            m = re.match(r"^([0-9.]+) [0-9.]+$", ln)
            if m:
                cur = float(m.group(1))
                up.append(cur)
                continue
            m = re.search(r"^\s*\d+:\s+(\d+).*Edge\s+485c0100\.dma-controller (chan[01])$", ln)
            if m and cur is not None:
                ch[m.group(2)].append((cur, int(m.group(1))))
        p("== board sampler (1 Hz): McASP DMA edge interrupt rows (CPU0 count)")
        for k, v in ch.items():
            if len(v) > 2:
                a = np.array(v)
                rate = np.diff(a[:, 1]) / np.diff(a[:, 0])
                p(f"{k}: {len(v)} samples; per-second rate percentiles 0/1/50/99/100 {b5.pct(rate, (0, 1, 50, 99, 100))}")
    text = "\n".join(lines) + "\n"
    (out / f"{name}-analysis.txt").write_text(text)
    print(text)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
