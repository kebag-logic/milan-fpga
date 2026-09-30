#!/usr/bin/env python3
"""Re-derive the round-2 torn-count qualification from the published
grade.json. usage: check_edge_frames.py <author/runs/din-long/grade.json>"""
import json, sys
g = json.load(open(sys.argv[1]))
r = g['region']; F = g['frames']
first, last = r['first_frame'], r['last_frame']
before, after = first, F - 1 - last   # zero-based frame indices
out = g['outside_region_words']
pat = lambda w: 1 <= (int(w, 16) >> 24) <= 8 and (int(w, 16) & 0xff) == 0
print(f'frames {F}; region {first}..{last} = {last - first + 1} (page 3,360,036)')
print(f'zero-based: {before} frames precede the region (indices 0..{first - 1}), {after} follow it; outside {before + after} (page 1,191,588)')
print(f'outside words: {out}; sum {sum(out.values())} = 8 x {(before + after)}: {sum(out.values()) == 8 * (before + after)}')
print(f'ffffff00 is a pattern word: {pat("ffffff00")}; fffff000: {pat("fffff000")}; 00000000: {pat("00000000")}')
for k, v in g['edge_frames'].items():
    print(f'edge frame {k}: {v} pattern words {sum(map(pat, v))}')
print(f'frames_after_region_before_idle {g["frames_after_region_before_idle"]} (page 777); zero words 6 + 776*8 + 3 = {6 + 776 * 8 + 3} (census {out["zero"]})')
print('reading of page line 159 "45,587 before the region": as a frame index it names the frame just before the region;'
      f' as a count it is one short of the {before} frames that precede the region')
