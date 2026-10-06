import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--evidence', type=Path, required=True)
parser.add_argument('--directive', required=True)
args = parser.parse_args()
work = args.work
directive = args.directive
gate = work / 'route' / ('ax7101/gateware' if directive == 'ExtraPostPlacementOpt'
                        else 'ax7101-' + directive)
out = args.evidence / 'timing-base' / directive
out.mkdir(parents=True, exist_ok=True)


def scrub(text):
    text = text.replace(str(Path.home()), '$HOME')
    return re.sub(r'^\| Host\s+:.*$', '| Host         : build host', text, flags=re.M)


def receipt(path):
    data = path.read_bytes()
    result = {'path': '$WORK/' + str(path.relative_to(work)), 'bytes': len(data),
              'sha256': hashlib.sha256(data).hexdigest()}
    if len(data) <= 200000 and path.suffix not in ('.dcp', '.bit', '.v', '.sv', '.init'):
        retained = scrub(data.decode(errors='replace')).encode()
        assert len(retained) <= 200000
        (out / path.name).write_bytes(retained)
        result.update(retained=path.name,
                      retained_sha256=hashlib.sha256(retained).hexdigest())
    return result


process_rc = int((work / (directive + '.rc')).read_text())
assert process_rc == 0, process_rc
rows = []
for corner in ('Slow', 'Fast'):
    for temp in (0, 85):
        path = gate / f'alinx_ax7101_signoff_{corner}_{temp}C_timing.rpt'
        lines = path.read_text().splitlines()
        header = next(i for i, line in enumerate(lines)
                      if 'WNS(ns)' in line and 'WHS(ns)' in line)
        values = next(line.split() for line in lines[header + 1:header + 6]
                      if re.match(r'^\s*-?\d+\.\d+', line))
        row = {'corner': corner, 'power_temperature_C': temp,
               'WNS_ns': float(values[0]), 'TNS_ns': float(values[1]),
               'setup_failing_endpoints': int(values[2]),
               'WHS_ns': float(values[4]), 'THS_ns': float(values[5]),
               'hold_failing_endpoints': int(values[6]),
               'WPWS_ns': float(values[8]), 'TPWS_ns': float(values[9]),
               'speed_file': next(line.strip() for line in lines if 'Speed File' in line),
               'report': path.name}
        row['passes_margin'] = row['WNS_ns'] >= .030 and row['WHS_ns'] >= 0
        rows.append(row)

spec = importlib.util.spec_from_file_location(
    'constraints', work / 'base/sw/litex/clock_constraints.py')
constraints = importlib.util.module_from_spec(spec)
spec.loader.exec_module(constraints)
constraints.check_implementation_log(gate / 'baseline.log')
(out / 'constraint-check.rc').write_text('0\n')
log = (gate / 'baseline.log').read_text(errors='replace').splitlines()
census = [(i, line) for i, line in enumerate(log, 1)
          if line.startswith('CRITICAL WARNING:')]
codes = Counter(re.search(r'\[([^]]+)\]', line)[1] for _, line in census)
(out / 'critical-warnings.tsv').write_text('original_log_line\tdiagnostic\n' + ''.join(
    f'{i}\t{scrub(line)}\n' for i, line in census))
summary = {'base_head': 'fa450d301805881ad713b67521477bf042ddadfd',
           'directive': directive, 'required_WNS_ns': .030, 'required_WHS_ns': 0,
           'rows': rows, 'process_rc': process_rc, 'constraint_check_rc': 0,
           'critical_warning_count': len(census), 'critical_warning_codes': dict(codes),
           'passes_margin': all(row['passes_margin'] for row in rows)}
grade_rc = 0 if summary['passes_margin'] else 1
summary['margin_grade_rc'] = grade_rc
(out / 'timing-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
(out / 'margin-grade.rc').write_text(str(grade_rc) + '\n')
paths = set(gate.glob('alinx_ax7101_signoff*'))
for name in ('alinx_ax7101_route.dcp', 'alinx_ax7101_synth.dcp', 'baseline.log',
             'baseline_hierarchy.rpt', 'baseline_utilization.rpt', 'baseline_timing.rpt',
             'baseline_images.json', 'alinx_ax7101_drc.rpt', 'alinx_ax7101_exceptions.rpt',
             'alinx_ax7101_utilization_route.rpt', 'alinx_ax7101_route_status.rpt',
             'baseline_integrated.tcl', 'baseline_implementation.tcl'):
    path = gate / name
    if path.exists():
        paths.add(path)
paths.add(work / (directive + '.log'))
paths.add(work / (directive + '.rc'))
(out / 'artifact-receipts.json').write_text(
    json.dumps([receipt(path) for path in sorted(paths)], indent=2) + '\n')
print(json.dumps(summary, indent=2))
raise SystemExit(grade_rc)
