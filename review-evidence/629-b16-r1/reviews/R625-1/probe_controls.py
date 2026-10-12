#!/usr/bin/env python3
"""Independent, offline controls against the published analysis functions.

Usage: probe_controls.py <published-author-evidence>
No subprocess, network, hardware, candidate edit or capture file is used.
"""
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np

p = Path(sys.argv[1])
sys.path.insert(0, str(p / 'tools'))


def load(name):
    spec = importlib.util.spec_from_file_location(name, p / 'tools' / (name+'.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


a = load('align_b16')
b = load('b9_thdn')
checks = {}
rng = np.random.default_rng(625)
source = rng.integers(-(1 << 22), 1 << 22, (16000, 4), dtype=np.int64)
clean = source[1000:9000].copy()
checks['clean_full_values'] = a.compare(source, clean, 4, 0)['compared_equal'] == 8000
changed = clean.copy()
changed[600, 0] += 256
r = a.compare(source, changed, 4, 0)
checks['high_byte_change'] = r['verdict']=='DIFFERENT' and r['frames_differing']==1
# Destroy every hash discriminator: equality must still compare full values.
a.key = lambda x: np.zeros(len(x), dtype=np.uint64)
r = a.compare(source, changed, 4, 0)
checks['hash_collision_cannot_hide_high_byte'] = r['verdict']=='DIFFERENT' and r['frames_differing']==1
swapped = clean[:, [1,0,2,3]]
checks['channel_swap_rejected'] = a.compare(source, swapped, 4, 0)['verdict']=='NO MATCH'
checks['truncated_overlap_counted_only'] = a.compare(source[:5000], clean, 4, 0)['compared_equal']==4000
# Challenge the receipt summarizer with independently specified blocks.
blocks = []
for i in range(5):
    val = -124.0 if i < 3 else -80.0
    blocks.append({'block':i, 'events':0, **{ch:{'thdn_db':val, 'snr_db':-val, 'ppm':0., 'level_dbfs':-14.}
                                         for ch in ('ch0','ch1')}})
g = {'blocks':blocks, 'events':[], 'effective_offset_ppm':0., 'phase_offset_ppm':0.,
     'phase_net_frames':0., 'silent_frames':0}
s = b.summarize(g)
checks['degraded_block_inventory'] = s['blocks_at_floor']==3 and s['degraded_event_free_blocks']==[3,4]
print(json.dumps({'checks':checks, 'all_pass':all(checks.values())}, indent=2))
sys.exit(0 if all(checks.values()) else 1)
