#!/usr/bin/env python3
"""Independently recompute B0's figures from the packet's per-block grade,
alignments and (a)'s tap grade; do not reuse the author's receipt tool.
usage: recompute_b0.py <packet author-r2 root>"""
import json, statistics, sys
R = sys.argv[1]
g = json.load(open(f'{R}/summary/b0-2/c-b9-grade.json'))
bl = g['blocks']
deg = sorted(g['summary']['degraded_event_free_blocks'])
deg_idx = [b if isinstance(b, int) else b['block'] for b in deg]
floor = [b for b in bl if b['block'] not in deg_idx]
out = {'blocks': len(bl), 'events': g['summary']['events'], 'degraded': len(deg_idx), 'at_floor': len(floor)}
# check the floor rule ourselves: event-free and within 3 dB of the all-block median, per channel
for ch in ('ch0', 'ch1'):
    med = statistics.median(b[ch]['thdn_db'] for b in bl)
    out[f'{ch}_all_median'] = round(med, 2)
    out[f'{ch}_all_worst'] = round(max(b[ch]['thdn_db'] for b in bl), 2)
    out[f'{ch}_floor_median'] = round(statistics.median(b[ch]['thdn_db'] for b in floor), 2)
    out[f'{ch}_floor_worst'] = round(max(b[ch]['thdn_db'] for b in floor), 2)
    out[f'{ch}_rule_off'] = sorted(b['block'] for b in bl if b[ch]['thdn_db'] > med + 3)
rule = sorted(set(out['ch0_rule_off']) | set(out['ch1_rule_off']))
out['rule_reproduces_degraded_set'] = rule == deg_idx
del out['ch0_rule_off'], out['ch1_rule_off']
runs = []
for i in deg_idx:
    if runs and runs[-1][1] == i - 1:
        runs[-1][1] = i
    else:
        runs.append([i, i])
out['runs'] = runs
a = json.load(open(f'{R}/summary/b0-2/align-a-c.json'))
b = json.load(open(f'{R}/summary/b0-2/align-b-c.json'))
cover = min(a['covered_recording_frames'][1], b['covered_recording_frames'][1])
assert a['covered_recording_frames'][0] == 0 and b['covered_recording_frames'][0] == 0
whole = cover // 48000
out['overlap_frames_a_b'] = [a['compared_equal'], b['compared_equal'], a['frames_differing'], b['frames_differing']]
out['overlap_seconds'] = round(cover / 48000, 4)
out['whole_blocks_inside'] = [0, whole - 1]
inside = [i for i in deg_idx if i < whole]
partial = [i for i in deg_idx if i == whole]
beyond = [i for i in deg_idx if i >= whole]
out['inside'] = len(inside); out['partial_degraded_block'] = partial; out['beyond'] = len(beyond)
out['beyond_runs'] = sum(1 for r in runs if r[0] >= whole)
for ch in ('ch0', 'ch1'):
    wi = max((bl[i] for i in inside), key=lambda x: x[ch]['thdn_db'])
    wb = max((bl[i] for i in beyond), key=lambda x: x[ch]['thdn_db'])
    out[f'{ch}_worst_inside'] = [wi['block'], round(wi[ch]['thdn_db'], 2)]
    out[f'{ch}_worst_beyond'] = [wb['block'], round(wb[ch]['thdn_db'], 2)]
out['phase_net_frames'] = g['phase_net_frames']; out['effective_offset_ppm'] = g['effective_offset_ppm']
out['ppm_maxabs_ch0_ch1'] = [round(g['summary']['ch0_all']['ppm_maxabs'], 3), round(g['summary']['ch1_all']['ppm_maxabs'], 3)]
ta = json.load(open(f'{R}/summary/b0-2/a-peer-tap.json'))
out['a_keys'] = list(ta)[:20]
print(json.dumps(out, indent=1))
