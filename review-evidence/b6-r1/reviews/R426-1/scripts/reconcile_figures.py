#!/usr/bin/env python3
"""Recompute the B6 page's per-case figures from summary/<case>/{grade.json,events.csv,blocks.csv}.
Usage: reconcile_figures.py <evidence-root>/author/summary"""
import csv, json, os, sys, statistics as S
root = sys.argv[1]
CASES = ["a0", "a1", "a2", "bint", "bcrf"]
tot_rise_skips = tot_rise_sig = 0
for c in CASES:
    g = json.load(open(os.path.join(root, c, "grade.json")))
    ev = list(csv.DictReader(open(os.path.join(root, c, "events.csv"))))
    bl = list(csv.DictReader(open(os.path.join(root, c, "blocks.csv"))))
    at = g["attribution"]
    L = at.get("listener", {}); B = at.get("DUT beat", {}); C = at.get("capture path", {})
    fr = g["frame_rate_ratio"]; m = fr["mcasp_capture"]
    clean = [b for b in bl if int(b["events"]) == 0 and int(b["invalid"]) == 0]
    off = [b for b in bl if b not in clean]
    th = [float(b["thdn_db_997"]) for b in off] + [float(b["thdn_db_9973"]) for b in off]
    print(f"== {c}: window {g['window']['seconds']} s, frames {g['window']['frames']}, blocks {len(bl)}, at floor {len(clean)} (grade {g['tone']['clean_blocks']})")
    print(f"   listener: skips {L.get('skips',0)} inserts {L.get('silent_inserts',0)} repeats {L.get('repeats',0)}; beat repeats {B.get('repeats',0)}; torn {g['tone']['torn']} invalid {g['tone']['invalid']}")
    lnet = L.get('skips',0) - L.get('silent_inserts',0) - L.get('repeats',0)
    print(f"   listener drops ppm {L.get('skips',0)/g['window']['frames']*1e6:.3f}, net listener ppm {lnet/g['window']['frames']*1e6:.3f}, beat ppm {B.get('repeats',0)/g['window']['frames']*1e6:.3f}")
    print(f"   counted ratio {fr['counted']['ppm']:+.3f} (steps {fr['counted']['steps_non_capture']}), timed {m['ratio_ppm']:+.2f} +- {m['ratio_ppm_halfwidth95']:.2f}, halves {m['ratio_ppm_first_half']:+.2f}/{m['ratio_ppm_second_half']:+.2f}, mcasp board rate {m['rate_board']:.2f}")
    for k in ("clean", "listener", "dut_beat_only"):
        for ch in ("ch0", "ch1"):
            x = g["blocks"][k][ch] if g["blocks"].get(k) else None
            if x: print(f"   blocks.{k}.{ch}: n {x['n']} thdn worst {x['thdn_db_worst']} median {x['thdn_db_median']} snr worst {x['snr_db_worst']} ppm maxabs {x['ppm_maxabs']:.2e}")
    print(f"   off-floor blocks {len(off)}; THD+N range over both tones {min(th) if th else None} .. {max(th) if th else None}")
    print(f"   floor dev max {g['tone']['ch0_clean_max_dev_from_floor_db']:.5f} / {g['tone']['ch1_clean_max_dev_from_floor_db']:.5f} dB")
    bc = g.get("beat_comb")
    if bc:
        print(f"   comb period {bc['period_frames']:.2f} members {bc['members']} teeth {bc['teeth_in_window']:.1f} resid_max {bc['residual_max']:.2f} slip_tdm/s {bc.get('slip_tdm_per_s',0):.4f} comb/s {bc['comb_per_s_at_48k']:.4f} diff {abs(bc['comb_per_s_at_48k']/bc['slip_tdm_per_s']-1)*100:.2f}%")
    cr = g["capture_reads"]
    print(f"   capture: reads {cr['records']} stalls>15ms {cr['stalls']} max gap {cr['read_gap_ms_max']} ms; events {C.get('events',0)} clusters {C.get('clusters',0)} lost {C.get('lost_frames',0)}")
    cl = g["skip_clusters"]
    rise = [x for x in cl if x["basis"] == "read-time rise" and x["capture_path"]]
    sk = [s for x in rise for s in x["steps"] if s > 0]
    sig = [s for s in sk if s % 48 == 12]
    tot_rise_skips += len(sk); tot_rise_sig += len(sig)
    print(f"   rise-matched clusters {len(rise)}, their skips {len(sk)}, 48n+12 {len(sig)}; non-rise clusters {len(cl)-len(rise)}: {[x['basis'] for x in cl if x not in rise]}")
    one = [e for e in ev if e["cause"] == "listener" and e["read_jump_ms"] not in ("", "None")]
    if one:
        r = [float(e["read_jump_ms"]) for e in one]
        big = sorted(r, key=abs)[-3:]
        print(f"   one-frame listener read rise: n {len(r)} median {S.median(r):.3f} maxabs-3 {big}")
print(f"TOTAL skips in rise-matched clusters {tot_rise_skips}, 48n+12 {tot_rise_sig}")
