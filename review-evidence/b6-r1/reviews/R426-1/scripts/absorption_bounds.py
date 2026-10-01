#!/usr/bin/env python3
"""Per-case bound on the three attribution absorption paths (F1), from the packet's summaries.
Usage: absorption_bounds.py <evidence-root>/author/summary"""
import csv, json, os, sys
root = sys.argv[1]
print("Per-case bound on the three absorption paths the probe demonstrated")
for c in ['a0', 'a1', 'a2', 'bint', 'bcrf']:
    ev = list(csv.DictReader(open(os.path.join(root, c, 'events.csv'))))
    g = json.load(open(os.path.join(root, c, 'grade.json')))
    beats = sorted(int(e['capture_frame']) for e in ev if e['cause'] == 'DUT beat')
    sp = [b - a for a, b in zip(beats, beats[1:])]
    close = [s for s in sp if s < 1000]
    odd = [(cl['cluster'], s, s % 48) for cl in g['skip_clusters'] if cl['capture_path'] for s in cl['steps']
           if s > 0 and s % 48 != 12 and abs(abs(s) - 24000) > 200 and cl['whole_loops_added'] == 0]
    spoiled = [cl['cluster'] for cl in g['skip_clusters'] if cl['basis'] == 'read gap and 48 n + 12 size']
    rgap = [(cl['cluster'], cl['steps']) for cl in g['skip_clusters'] if cl['basis'] == 'read gap']
    bigloss = [(cl['cluster'], cl['lost_ms']) for cl in g['skip_clusters'] if cl['whole_loops_added'] > 0]
    print(f"{c}: beat teeth closer than 1000 frames: {len(close)} (min spacing {min(sp) if sp else None}); "
          f"capture-path skips off 48n+12 outside replay edges and >loop losses: {odd}; "
          f"spoiled-rise clusters: {spoiled}; rise-unmeasurable clusters: {rgap}; >loop losses: {bigloss}")
