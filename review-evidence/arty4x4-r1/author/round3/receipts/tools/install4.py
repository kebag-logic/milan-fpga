"""Install the rule's Arty 4x4 (1,5,5) row at 100 MHz from a derived model (derive4.py), in place; no other shape or
point is touched (round 9's install7.py, aimed at arty-4x4).

usage: python3 install4.py MODEL.json   (run from the checkout root)
"""
import json
import math
import re
import sys
from pathlib import Path

root = Path.cwd()
model = json.loads(Path(sys.argv[1]).read_text())
assert model['status'] == 'CANDIDATE MODEL' and model['cpu_hz'] == 100_000_000 and model['shape'] == [1, 5, 5]
choice, c = model['choices'][0], model['costs']
assert not choice['owner_findings']
base = root / 'tb/verilator/ctrl_service_budget'


def sub(path, pattern, repl, flags=re.S):
    text = path.read_text()
    new, n = re.subn(pattern, lambda m: repl(m), text, flags=flags)
    assert n == 1, (path, pattern, n)
    path.write_text(new)


def flat(d):
    return ', '.join(f'{k!r}: {v!r}' for k, v in d.items())


# 1. THE SHAPES row in ctrl_loop.h.
values = dict(CTRL_LOOP_SLICE_US=choice['slice_us'], CTRL_LOOP_BUILD_PASS_US=c['build'],
              CTRL_LOOP_BUILD_ONE_PASS_US=c['build_one'], CTRL_LOOP_SRP_UNIT_US=c['record.srp'],
              CTRL_LOOP_RETRY_COLD_US=model['retry_us'][0], CTRL_LOOP_RETRY_ATTEMPT_US=model['retry_us'][1],
              CTRL_LOOP_QUEUED_MS=choice['queued_ms'], CTRL_LOOP_TX_MS=math.ceil(choice['rows_ms']['tx'] - 1e-9),
              CTRL_LOOP_STEP_PASS_US=c['step'], CTRL_LOOP_TICK_US=c['centisecond'],
              AECP_NOTICE_US=model['retry_us'][2], AECP_PACE_MS=choice['pace_ms'])
head = '#elif CTRL_LOOP_SHAPE(1u, 5u, 5u)      // Arty FPGA 4x4: one interface, four AAF and the CRF each way, 100 MHz\n'
sub(root / 'sw/firmware/ctrl/loop/ctrl_loop.h', re.escape(head) + r'(?:#define \w+ \d+u\n)+',
    lambda m: head + ''.join(f'#define {k} {v}u\n' for k, v in values.items()))

# 2. The polls' statements at (1,5,5).
poll = dict(base=c['base'], withdraw=c['item.withdraw'], rebuild=c['item.rebuild'], walk=c['item.walk'],
            reclaim=c['item.reclaim'], retained=c['record.srp'], mrpdu=0, acmp=c['item.acmp'], aecp=c['item.aecp'],
            aecp_long=c['item.aecp_long'], acmp_declined=c['item.acmp_declined'])
items = ', '.join(f'{k!r}: {v}' for k, v in poll.items())
cut = items.index("'acmp': ")
sub(base / 'poll_grade.py', r"STATED_US\[shape_costs\.Shape\(1, 5, 5\)\] = (?:dict\([^\n]*\)|\{\n[^}]*\})\n",
    lambda m: 'STATED_US[shape_costs.Shape(1, 5, 5)] = {\n    ' + items[:cut].rstrip() + '\n    ' + items[cut:] + '}\n')

# 3. The load model's two columns, identical at this point.
keys = ['record.srp', 'record.aecp', 'record.acmp', 'record.adp', 'record.maap', 'event.ADP', 'event.ACMP',
        'event.MAAP', 'event.AECP', 'event.TICK', 'event.GM', 'centisecond', 'events_none', 'item.retained',
        'item.aecp.notice', 'item.aecp.response', 'item.aecp.probe']
row = {k: c[k] for k in keys}
lines = ['        ' + flat({k: row[k] for k in keys[:5]}) + ',',
         '        ' + flat({k: row[k] for k in keys[5:11]}) + ',',
         '        ' + flat({k: row[k] for k in keys[11:15]}) + ',',
         '        ' + flat({k: row[k] for k in keys[15:]}) + '},']
for table in ('STATED_US', 'STATED_US_DONOR'):
    sub(base / 'load_grade.py', rf"(\n{table} = \{{\n    'arty-1x1': \{{\n.*?\}},\n    'arty-4x4': \{{\n).*?\}},\n",
        lambda m: m.group(1) + '\n'.join(lines) + '\n')

# 4. Event, datapath, long-record and paced-edit statements.
sub(base / 'rows_grade.py', r"('arty-4x4': )\{'event\.LINK': \d+\}",
    lambda m: m.group(1) + repr({'event.LINK': c['event.LINK']}))
sub(base / 'rows_tiers.py', r"('arty-4x4': )\{'AVB_INFO_CHANGED': \d+, 'AS_PATH_CHANGED': \d+, 'AMAP_LIVE_WRITE': \d+\}",
    lambda m: m.group(1) + repr({k: c['event.' + k] for k in ('AVB_INFO_CHANGED', 'AS_PATH_CHANGED', 'AMAP_LIVE_WRITE')}))
sub(base / 'rows_tiers.py', r"('arty-4x4': )\d+(, '1x1/1if')", lambda m: m.group(1) + str(c['record.aecp.long']) + m.group(2))
sub(base / 'edit_rows.py', r"('arty-4x4': )\{'a one-row edit': \d+, 'an accepted SET_CONFIGURATION': \d+\}",
    lambda m: m.group(1) + repr({'a one-row edit': max(c['paced.44'], c['paced.45']),
                                 'an accepted SET_CONFIGURATION': c['paced.6']}))
print(json.dumps(dict(status='INSTALLED RULE ROW; complete census qualification required', constants=values,
                      poll=poll, load_row=row), indent=1))
