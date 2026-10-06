import hashlib
import json
import os
from pathlib import Path
import re

work = Path(__file__).parent
out = Path(os.environ['EVIDENCE'])
for directive in ['ExtraPostPlacementOpt', 'AltSpreadLogic_high', 'ExtraTimingOpt']:
    gate = work / 'route' / ('ax7101/gateware' if directive == 'ExtraPostPlacementOpt'
                            else 'ax7101-' + directive)
    report = gate / 'alinx_ax7101_signoff_Slow_0C_timing.rpt'
    raw = report.read_bytes()
    text = raw.decode()
    starts = list(re.finditer(r'^Slack\s.*?(-?\d+\.\d+)ns\b[^\n]*$', text, re.M))
    assert starts, report
    paths = []
    for i, match in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        block = text[match.start():end]
        fields = {}
        for name in ['Source', 'Destination', 'Path Group', 'Path Type', 'Data Path Delay', 'Logic Levels']:
            value = re.search(r'^\s*' + re.escape(name) + r':\s*(.+)$', block, re.M)
            if value:
                fields[name] = value[1].strip()
        if not fields.get('Path Type', '').startswith('Setup'):
            continue
        paths.append({'slack_ns': float(match[1]),
                      'source_line': text.count('\n', 0, match.start()) + 1,
                      'fields': fields, 'block': block})
    worst = sorted(paths, key=lambda row: row['slack_ns'])[:5]
    assert len(worst) == 5
    summary = json.loads((out / 'timing-current' / directive / 'timing-summary.json').read_text())
    minimum = next(row['WNS_ns'] for row in summary['rows']
                   if row['corner'] == 'Slow' and row['power_temperature_C'] == 0)
    assert worst[0]['slack_ns'] == minimum, (worst[0]['slack_ns'], minimum)
    receipt = {'report': '$WORK/' + str(report.relative_to(work)),
               'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
               'head': summary['candidate_head'],
               'paths': [{key: value for key, value in row.items() if key != 'block'} for row in worst]}
    target = out / 'timing-current' / directive
    (target / 'worst-five.json').write_text(json.dumps(receipt, indent=2) + '\n')
    excerpt = ''.join(f"Original report line {row['source_line']}\n{row['block']}\n" for row in worst)
    excerpt = excerpt.replace(str(Path.home()), '$HOME')
    assert len(excerpt.encode()) <= 200000
    (target / 'worst-five.rpt').write_text(excerpt)
    print(directive, 'worst five extracted, minimum', minimum)
