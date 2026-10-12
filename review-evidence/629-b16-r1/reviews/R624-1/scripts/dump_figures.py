#!/usr/bin/env python3
"""Print the receipt figures behind the B16b/B16c tables, from the published packet.

usage: dump_figures.py <author-r1 dir>
"""
import json, os, sys

root = sys.argv[1]
S = lambda *p: os.path.join(root, "summary", *p)


def tone_lines(path):
    out = []
    lines = open(path).read().splitlines()
    for l in lines:
        if l.startswith("{"):
            d = json.loads(l)
            for k in ("tone_997", "tone_9973"):
                if k in d:
                    t = d[k]
                    out.append(f"ch{d['channel']} {k}: lvl {t['level_dbfs']} f {t['f_hz']} ppm {t['ppm']} thdn {t['thdn_db']} snr {t['snr_db']}")
            if "tone_997" not in d and "tone_9973" not in d:
                out.append(f"ch{d['channel']} min {d['min']} max {d['max']} rms {d['rms_dbfs']}")
        else:
            out.append(l[:120])
    return out


for run in ["pts1", "pts2", "pts3", "b0", "b0-2", "bcrf", "baaf"]:
    print(f"===== {run}")
    for pt in ("a", "b", "c"):
        p = S(run, f"{pt}.stdout")
        if os.path.exists(p):
            print(f" ({pt})")
            for l in tone_lines(p):
                print("   ", l)
    for pt in ("a-peer-tap", "b-dut-tap", "c-mcasp"):
        p = S(run, f"{pt}.json")
        if os.path.exists(p):
            d = json.load(open(p))
            keys = {k: d[k] for k in d if not isinstance(d[k], (list, dict))}
            print(f" {pt} scalars: {json.dumps(keys)[:400]}")
            for ch in d.get("channels", [])[:2] if isinstance(d.get("channels"), list) else []:
                pass
    p = S(run, "c-b9-grade.stdout")
    if os.path.exists(p):
        g = json.loads(open(p).read())
        print(" b9:", {k: g[k] for k in ("blocks", "event_free_blocks", "blocks_at_floor", "skips", "repeats", "inserts", "glitches", "silent_frames", "effective_offset_ppm", "phase_net_frames")})
        for ch in ("ch0_floor", "ch0_all", "ch1_floor", "ch1_all"):
            c = g[ch]
            print(f"   {ch}: n {c['n']} med {c['thdn_db_median']} worst {c['thdn_db_worst']} snr {c['snr_db_median']} ppm_med {c['ppm_median']:.6f} ppm_maxabs {c['ppm_maxabs']:.4f} lvl {c['level_dbfs_median']}")
        deg = g["degraded_event_free_blocks"]
        runs, s = [], None
        for i, b in enumerate(deg):
            if s is None:
                s = p0 = b
            elif b == p0 + 1:
                p0 = b
            else:
                runs.append((s, p0)); s = p0 = b
        if s is not None:
            runs.append((s, p0))
        print(f"   degraded {len(deg)} in runs {runs}")
    for al in ("align-a-c", "align-b-c"):
        p = S(run, f"{al}.stdout")
        if os.path.exists(p):
            d = json.loads(open(p).read())
            print(f" {al}: {d['verdict']} compared {d['compared_equal']} differ {d['frames_differing']} slips {d['slips']} covered {d['covered_recording_frames']} seq_gaps {d['seq_gaps']} stream_frames {d['stream_frames']}")
    p = S(run, "d-loop-decode.stdout")
    if os.path.exists(p):
        print(" d:", open(p).read().strip()[:600])
