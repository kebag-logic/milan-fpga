#!/usr/bin/env python3
"""Independent re-derivation of the round 3 figures of docs/findings/117_AUDIO_CONTINUITY.md
from the public evidence packet review-evidence/117-b21-r1 (author/ directory).

usage: python3 -I rederive_r3.py <evidence_root> <page.md>

<evidence_root> is the directory holding MANIFEST.json and author/. Reads only; writes to stdout.
The floor test and block test below are re-implemented here from their written definitions (a
stall is a read interval over 15 ms; the deficit D = t*48000 - frames delivered; the floor step
compares min(D) over W+1 reads after a guard of GA reads with min(D) over W+1 reads before a guard
of GB reads); they do not import the packet's tools.
"""
import gzip
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

import numpy as np

FS = 48000


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def manifest(root):
    m = json.load(open(root / "MANIFEST.json"))
    bad = [e["file"] for e in m if sha(root / e["file"]) != e["published_sha256"]]
    red = [e["file"] for e in m if e["path_redacted"]]
    print(f"[manifest] {len(m)} entries, {len(bad)} published-hash mismatches, {len(red)} label-masked")
    return {e["file"]: e for e in m}


def page_hashes(root, page):
    txt = page.read_text().split("\n")
    s = next(i for i, l in enumerate(txt) if l.startswith("### B21 round 3: artifact hashes"))
    rows = [l for l in txt[s:] if l.startswith("| ")]
    rec = (root / "author/raw-retention-receipt-r3.txt").read_text()
    arch = {}
    for ln in rec.splitlines():
        p = ln.split()
        if len(p) >= 4 and p[0] == "OK":
            arch[p[2]] = int(p[1])
    n_ok = n_tool = 0
    for r in rows:
        c = [x.strip() for x in r.strip("|").split("|")]
        hs = re.findall(r"`([0-9a-f]{64})`", r)
        if len(c) == 3 and c[1].isdigit():
            h = hs[0]
            if h in arch:
                ok = arch[h] == int(c[1])
                n_ok += ok
                print(f"[raw] {c[0]}: archived, size {'equal' if ok else 'DIFFERS'}")
            elif h == sha(root / "author/r3/selftest/mst-long/mst-long-reads.u16"):
                n_ok += 1
                print(f"[raw] {c[0]}: published in packet, hash equal")
            else:
                print(f"[raw] {c[0]}: NOT FOUND")
        elif hs:
            n_tool += len(hs)
    print(f"[raw] {n_ok} artifact rows verified; {n_tool} tool hashes on the round 3 tool table")
    print(f"[raw] retention receipt: {len(arch)} OK lines; last line: {rec.strip().splitlines()[-1]}")


def floor_steps(D, W, GB=3, GA=2):
    R = len(D) - 1
    pos = np.arange(GB + W, R - GA - W)
    # sliding minima via strided windows
    from numpy.lib.stride_tricks import sliding_window_view as sw
    mins = sw(D, W + 1).min(axis=1)        # mins[k] = min D[k..k+W]
    after = mins[pos + GA]
    before = mins[pos - GB - W]
    x = after - before
    return pos, x


def groups(pos, x, drift, tol, join):
    big = np.flatnonzero(np.abs(x - drift) > tol)
    g = []
    for i in big:
        if g and pos[i] - g[-1][-1] <= 2 * join:
            g[-1].append(int(pos[i]))
        else:
            g.append([int(pos[i])])
    return big, g


def selftest(root):
    d = root / "author/r3/selftest/mst-long"
    meta = json.load(open(d / "mst-long-reads.json"))
    rec = np.fromfile(d / "mst-long-reads.u16", dtype="<u2").astype(np.int64)
    assert sha(d / "mst-long-reads.u16") == meta["record"]["sha256"]
    R = len(rec)
    t = np.concatenate(([0], np.cumsum(rec))) / 1e6
    F = 480.0 * np.arange(R + 1)
    D = t * FS - F
    print(f"[mst-long] reads {R + 1}, intervals {R}, frames {480 * (R + 1)} (delivered in window {int(F[-1])}); "
          f"window {t[-1]:.3f} s; exact {meta['elapsed_ns_exact'] / 1e9:.6f} s")
    g = rec / 1e3
    print(f"[mst-long] read interval ms min {g.min():.1f} max {g.max():.1f}; over 15 ms {(g > 15).sum()}; over 12 ms {(g > 12).sum()}")
    A = np.vstack([t, np.ones_like(t)]).T
    s, i0 = np.linalg.lstsq(A, D, rcond=None)[0]
    print(f"[mst-long] deficit slope {s:+.4f} frames/s = {1e6 * s / FS:+.2f} ppm")
    for W in (10, 110):
        pos, x = floor_steps(D, W)
        drift = float(np.median(x))
        big, gg = groups(pos, x, drift, 4.0, 3 + 2 + W + 1)
        lg = [max((x[np.searchsorted(pos, r)] for r in grp), key=lambda v: abs(v - drift)) for grp in gg]
        print(f"[mst-long] W={W}: positions {len(pos)}, drift {drift:+.3f}, |step-drift|>4 at {len(big)} in {len(gg)} groups; "
              f"step min {x.min():+.1f} max {x.max():+.1f}; group largest steps {[round(v, 1) for v in lg][:40]}"
              + (f" ... ({len(lg)} groups)" if len(lg) > 40 else ""))
        if W == 110:
            print(f"[mst-long] W=110 group largest steps relative to drift: {[round(v - drift, 1) for v in lg]}")
    blocks = lambda DD: np.array([DD[a:a + 1000].min() for a in range(0, len(DD) - 999, 1000)])
    tc = np.array([t[a] for a in range(0, len(D) - 999, 1000)])

    def block(DD):
        fl = blocks(DD)
        s10, i10 = np.polyfit(tc, fl, 1)
        r = fl - (s10 * tc + i10)
        return r.min(), r.max(), np.abs(np.diff(r)).max()
    b0 = block(D)
    print(f"[mst-long] 10 s block floors: {len(tc)} blocks, residual {b0[0]:+.2f} .. {b0[1]:+.2f}, largest change {b0[2]:.2f}")
    # mutation probe: a capture-path loss after sampling delays every later read by its duration,
    # i.e. raises D by L frames for good from the loss point on
    for L in (6, 12, 24, 48):
        for at in (0.25, 0.5, 0.9):
            k = int(at * R)
            Dm = D.copy()
            Dm[k:] += L
            bm = block(Dm)
            pos, x = floor_steps(Dm, 110)
            drift = float(np.median(x))
            big, gg = groups(pos, x, drift, 4.0, 116)
            hit = any(abs(r - k) < 300 for grp in gg for r in grp)
            print(f"[mst-long probe] loss {L:2d} frames at {at:.2f}: block largest change {bm[2]:.2f} "
                  f"(baseline {b0[2]:.2f}), residual {bm[0]:+.2f}..{bm[1]:+.2f}; W=110 floor test flags the loss: {hit}")


def poll(path):
    txt = open(path, errors="replace").read()
    rows = []
    for b in re.split(r"^### ", txt, flags=re.M)[1:]:
        m = re.match(r"(\S+) cmd='mem_read (0x[0-9a-f]+) (\d+)'", b)
        if not m:
            continue
        base = int(m.group(2), 16)
        data = bytearray()
        for ln in b.splitlines():
            mm = re.match(r"^0x([0-9a-f]{8})\s+((?:[0-9a-f]{2} )+)", ln)
            if mm:
                data += bytes.fromhex(mm.group(2).replace(" ", ""))
        for k in range(len(data) // 4):
            rows.append((m.group(1), base + 4 * k, struct.unpack("<I", data[4 * k:4 * k + 4])[0]))
    by = {}
    for t, a, v in rows:
        by.setdefault(a, []).append((t, v))
    return by


def csr(root, run):
    by = poll(root / f"author/r3/runs/{run}/dut-poll.txt")
    n = {a: len(v) for a, v in by.items()}
    rs = [v for _, v in by[0x900008DC]]
    fill = [v & 0xFF for v in rs]
    pre = {(v >> 8) & 1 for v in rs}
    conv = {(v >> 9) & 1 for v in rs}
    rails = {v >> 16 for v in rs}
    st = {v for _, v in by[0x900006B8]}
    er = {v for _, v in by[0x900006C0]}
    tdm = {v for _, v in by[0x900008D8]}
    lb = {v for _, v in by[0x900008D4]}
    am = {v for _, v in by[0x900008E0]} | {v for _, v in by[0x900008E4]}
    f0, f1 = by[0x90000660][0], by[0x90000660][-1]
    p0, p1 = by[0x90000664][0], by[0x90000664][-1]
    print(f"[{run} csr] samples per word {sorted(set(n.values()))}; first {f0[0]} last {f1[0]}")
    print(f"[{run} csr] SLIP_TDM {sorted(hex(v) for v in tdm)}; SLIP_LB {sorted(hex(v) for v in lb)}; AVTPRX_STAT {sorted(hex(v) for v in st)}; "
          f"AVTPRX_ERR {sorted(hex(v) for v in er)}; AAF clock meter words {sorted(hex(v) for v in am)}")
    print(f"[{run} csr] RENDER_STAT fill {min(fill)}..{max(fill)}, prefill {pre}, converged {conv}, rails {rails}")
    print(f"[{run} csr] AAF_FRAMES +{(f1[1] - f0[1]) % 2**32}, AAF_PAIRS +{(p1[1] - p0[1]) % 2**32}")


def counters(root, run):
    out = {}
    for tag in ("pre", "mid", "post"):
        for ln in open(root / f"author/r3/runs/{run}/counters-{tag}.jsonl"):
            if not ln.startswith("{"):
                continue
            r = json.loads(ln)
            if r.get("cmd") != "GET_COUNTERS" or r.get("status") != "SUCCESS":
                continue
            b = bytes.fromhex(r["payload"])
            dt, di, valid = struct.unpack(">HHI", b[:8])
            w = struct.unpack(">32I", b[8:136])
            out.setdefault((r["role"], dt, di), []).append((r["t_rx"], valid, w))
    for k, v in sorted(out.items()):
        if k[1] not in (5, 6):
            continue
        moved = {i: (v[-1][2][i] - v[0][2][i]) % 2**32 for i in range(32) if v[-1][2][i] != v[0][2][i]}
        print(f"[{run} counters] {k[0]} {'SI' if k[1] == 5 else 'SO'}{k[2]} valid {v[0][1]:#x} span {v[-1][0] - v[0][0]:.1f} s "
              f"moved words {moved}")


def wire(root):
    s = root / "author/r3/summary"
    for run in ("dA", "dB"):
        w = json.load(open(s / f"{run}-wire.json"))
        for tap in ("dutlink", "peerlink"):
            x = w[tap]
            p = x.get("pattern")
            line = (f"[{run} wire] {tap}: {x['packets']} packets over {x['seconds_tap']} s, seq breaks {x['seq_step_not_1']}, "
                    f"ts steps {x['ts_step_ns'] if 'min' in x['ts_step_ns'] else (min(map(int, x['ts_step_ns'])), max(map(int, x['ts_step_ns'])))}, "
                    f"tv_zero {x['tv_zero']}, sdl {x['sdl']}")
            if p:
                ok = (p["region_frames"] == p["valid"] and p["in_order"] == p["valid"] - 1 and p["repeats"] == p["skips"] == p["backward"] == p["torn"] == p["invalid_inside_region"] == 0)
                line += f"; pattern valid {p['valid']} ({p['valid'] / FS:.1f} s), contiguous and in order: {ok}"
            print(line)
        c = w["cross_link"]
        cons = (c["dut_only_before"] + c["common_packets"] + c["dut_only_after"] == w["dutlink"]["packets"]
                and c["peer_only_before"] + c["common_packets"] + c["peer_only_after"] == w["peerlink"]["packets"])
        print(f"[{run} wire] common {c['common_packets']}, header equal {c['header_equal']}, payload equal {c['payload_equal']}, "
              f"partition consistent {cons}; transit minus median (drift included) {c['transit_minus_median_us']['min']} .. {c['transit_minus_median_us']['max']} us")
    m = json.load(open(s / "dB-mcasp.json"))
    print(f"[dB mcasp] frames {m['mcasp_frames']} ({m['mcasp_frames'] / FS:.1f} s), matched {m['matched']}, offset changes {m['offset_changes']}, "
          f"foreign {m['foreign_frames']}, first aligned McASP frame {m['first_aligned_mcasp_frame']}")
    e = json.load(open(s / "dA-ext.json"))
    print(f"[dA ext] valid {e['valid']} ({e['valid'] / FS:.1f} s), region {e['region_frames']}, in order {e['in_order']}, "
          f"repeats {e['repeats']}, skips {e['skips']}, zero inside {e['zero_inside_region']}, torn {e['torn']}, stalls {e['stalls']}, reads {e['reads']}")


def restarts(root):
    r = json.load(open(root / "author/r3/summary/rA-restart.json"))
    for link in ("peerlink", "dutlink"):
        c = r[link]["cycles"]
        rs = np.array([x["restart_s"] for x in c]) * 1e3
        st = np.array([x["last_after_disconnect_s"] for x in c]) * 1e3
        print(f"[rA {link}] cycles {len(c)}, statuses nonzero {sum(1 for x in c if x['connect_resp_status'] or x['disconnect_resp_status'])}, "
              f"restart ms min {rs.min():.1f} median {np.median(rs):.1f} max {rs.max():.1f}, under 1 s {(rs < 1000).sum()}, "
              f"stop ms {st.min():.1f}..{st.max():.1f}, packets in hold {sum(x['packets_in_hold'] for x in c)}, "
              f"first 480 valid {sum(1 for x in c if x['first_480_frames_valid_in_order'])}")
    c = r["peerlink"]["cycles"]
    ex = r["external"]["silences"]
    o = np.array([cc["restart_s"] + e["silence_frames"] / FS - cc["wire_gap_s"] for cc, e in zip(c, ex)]) * 1e3
    print(f"[rA output] recomputed restart + S/48000 - G, ms: min {o.min():.1f} median {np.median(o):.1f} max {o.max():.1f}; "
          f"silences all zero {all(e['silence_zero_frames'] == e['silence_frames'] for e in ex)}; "
          f"ext frames {r['external']['frames']} ({r['external']['frames'] / FS:.1f} s), stalls {r['external']['stalls_over_15ms']}, "
          f"in-run steps not 1 {r['external']['in_run_steps_not_1']}")


def dbreads(root):
    d = root / "author/r3/runs/dB/ana"
    meta = json.load(open(d / "dB-reads.json"))
    raw = gzip.decompress((d / "dB-reads.u32.gz").read_bytes())
    h = hashlib.sha256(raw).hexdigest()
    g = np.frombuffer(raw, dtype="<u4") / 1e3
    print(f"[dB reads] gunzipped record sha256 equals reads.json: {h == meta['record']['sha256']}; intervals {len(g)}, "
          f"over 15 ms {(g > 15).sum()}, longest {g.max():.2f} ms; reads not one period {meta['reads_not_one_period']}; "
          f"stamper: {meta['stamper']}; overruns {meta['arecord_overruns']}")


def main(root, page):
    root, page = Path(root), Path(page)
    manifest(root)
    page_hashes(root, page)
    selftest(root)
    dbreads(root)
    for run in ("dA", "dB"):
        csr(root, run)
        counters(root, run)
    wire(root)
    restarts(root)


if __name__ == "__main__":
    main(*sys.argv[1:3])
