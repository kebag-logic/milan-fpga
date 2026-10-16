#!/usr/bin/env python3
"""Per-cycle stream, counter and outage facts from bench/cycleNN/analysis.json.
Usage: check_cycle_streams.py <author-dir>"""
import json, os, sys
auth = sys.argv[1]
for c in range(1, 7):
    a = json.load(open(os.path.join(auth, 'bench', 'cycle%02d' % c, 'analysis.json')))
    e = a['cycle_edges']
    lic = [x for x in a['crf_ctrl']]
    print('cycle', c, 'off_hold %.2f' % a['off_hold_s'], 'epochs', a['reset_epochs'],
          'crf_ctrl', lic, 'media_locked', a['media_locked_at'],
          'stream start/stop', e.get('dut_crf_stream_start_stop_delta'),
          'gm_changed', e['gm_changed_delta'], 'link', e['link_delta'],
          'tucnt', e['clkv_tucnt_delta'], 'crf first after on', e.get('crf_first_after_on'),
          'tu', e.get('crf_first_after_on_tu'), 'tu1 after on', e.get('crf_tu1_after_on'),
          'last far frame', a['last_far_frame_before_on'], 'far frames 5s..on', a['far_frames_during_off_after_5s'],
          'carrier', a['carrier'], 'max gap', round(a['max_console_gap_s'], 3),
          'avail_idx', a['peer_available_index'], 'bindings', a['bindings'])
