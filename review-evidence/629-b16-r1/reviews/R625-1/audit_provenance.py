#!/usr/bin/env python3
"""Inventory the public inputs needed to reproduce detailed bench claims."""
import json
from pathlib import Path
import sys

p = Path(sys.argv[1])
result = {}
for run in ('bcrf','baaf'):
    events = [json.loads(s) for s in (p/'runs'/run/'events.jsonl').read_text().splitlines()]
    poll = next(e for e in events if e['kind']=='poll-summary')
    result[run] = {
        'published_poll_history': (p/'runs'/run/'poll-run.jsonl').exists(),
        'span_summary_fields': sorted(poll['spans']['window-start..window-end']),
        'clock_word_summary': {k:poll['spans']['window-start..window-end'][k]['0x8f8'] for k in ('first','last','distinct')},
        'window_extrema_recoverable_from_summary': False,
        'individual_slip_timestamps_present_in_summary': False,
    }
# Two possible traces with identical retained summaries and different extrema.
# This does not assert either is the real trace; it shows the lost information.
trace_a = [0xff9f0034,0xffa00034,0xff9e0034,0xff9f0074,0xffa00074]+[0xff9f0034]*591
trace_b = trace_a.copy()
trace_b[2] = 0xff800034
def retained(trace):
    return {'polls':len(trace),'first':trace[0],'last':trace[-1], 'distinct':len(set(trace)),
            'servo':{'LOCKED':sum((v&7)==4 for v in trace)}}
def extrema(trace):
    values = [(v>>16)-65536 if v>>31 else v>>16 for v in trace]
    return [min(values)/16,max(values)/16]
assert retained(trace_a)==retained(trace_b)
assert extrema(trace_a)!=extrema(trace_b)
result['summary_information_loss_control'] = {'same_retained_summary':True,
                                             'possible_trim_ranges_ppm':[extrema(trace_a),extrema(trace_b)]}
result['source_setting_evidence'] = {
    'published_measurement_files': [str(f.relative_to(p)) for d in ('runs','restore','summary','soc')
                                    for f in sorted((p/d).rglob('*')) if f.is_file()],
    'scope': 'Inventory excludes narrative handoffs, reports and tool source. No reduced source-setting or meter receipt is present.',
}
print(json.dumps(result,indent=2))
