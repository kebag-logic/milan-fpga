from pathlib import Path
from collections import Counter
import hashlib
import importlib.util
import json
import re

w = Path(__file__).resolve().parents[1]
repo = Path('$LANES/645-ring-slip')
out = Path.home()/'milan-fpga-management/2026-09-23/645-a531/round2c/campaigns'
spec = importlib.util.spec_from_file_location('quiet', repo/'tb/verilator/follow_ring/quiet_distributions.py')
quiet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quiet)
margin = re.compile(r'^MARGINS: (.+) empty ([\d.]+) full ([\d.]+) ticks$', re.M)
actions = re.compile(r'settle recentre fired \((\d+) pulse\(s\), render recentre executed (\d+)\); slips before it (\d+), after it (\d+);')
groups = []
receipts = {}
for name, root in [('baseline', w/'baseline'), ('candidate', w/'candidate/campaigns')]:
    assert (root/'all.rc').read_text().strip() == '0', root
    receipt = quiet.grade(root, 2)
    receipts[name] = receipt
    dest = out/name
    dest.mkdir(parents=True, exist_ok=True)
    (dest/'quiet-distributions.json').write_text(json.dumps(receipt, indent=2)+'\n')
    for group in receipt['groups']:
        target = dest/group
        target.mkdir(exist_ok=True)
        inventory = []
        all_margins = []
        counts = Counter()
        for log in sorted((root/group).glob('b8_*_p*.log')):
            text = log.read_text()
            values = margin.findall(text)
            assert len(values) == 3 and {row[0] for row in values} == {
                '[B8]', '[SW] AAF to CRF:', '[SW] CRF to AAF:'}, log
            for window, empty, full in values:
                assert float(empty) >= 1 and float(full) >= 1, (log, window, empty, full)
                all_margins.append(dict(case=log.stem, window=window,
                                       empty=float(empty), full=float(full)))
            action_rows = actions.findall(text)
            assert len(action_rows) == 3, log
            assert all(int(pulses) == 1 and int(render) == 1 and int(post) == 0
                       for pulses, render, pre, post in action_rows), log
            counts['post_settle_windows'] += 3
            counts['late_arrival_law_windows_not_graded'] += text.count('render law not graded:')
            counts['result_lines_with_ambiguous_render_window'] += sum(
                'not gradable' in line for line in text.splitlines() if line.startswith('RESULT-645'))
            for path in [p for p in [log, log.with_suffix('.rc'), log.with_suffix('.command.json')] if p.exists()]:
                data = path.read_bytes()
                assert len(data) <= 200000, path
                portable = data.decode().replace(str(Path.home()), '$HOME').encode()
                assert len(portable) <= 200000
                (target/path.name).write_bytes(portable)
                inventory.append(dict(path=str(path.relative_to(w)), bytes=len(data),
                    sha256=hashlib.sha256(data).hexdigest(),
                    retained_sha256=hashlib.sha256(portable).hexdigest()))
        assert len(all_margins) == 48
        row = dict(campaign=name, group=group, phases=16, windows=48,
                   empty_min=min(all_margins, key=lambda x: x['empty']),
                   full_min=min(all_margins, key=lambda x: x['full']),
                   scope_counts=dict(counts))
        groups.append(row)
        (target/'artifact-inventory.json').write_text(json.dumps(inventory, indent=2)+'\n')
        (target/'margins.json').write_text(json.dumps(all_margins, indent=2)+'\n')
    for path in [root/'all.rc', root/'quiet-distributions.json']:
        (dest/path.name).write_bytes(path.read_bytes())
summary = dict(result='PASS', rc=0, cases=256, histogram_windows=1024,
    candidate_acceptance_cases=128, band_axis_cycles=2,
    worst_quiet_excursion=max(r['quiet_excursion'] for r in receipts.values()),
    note='Baseline is the preserved pre-recovery-qualification model with '
         'the four-band arm. Candidate is the two-cycle arm and recovery '
         'qualification implementation. This baseline is distinct from '
         'the vendor area reference and the manager timing table. '
         'Late-arrival runs grade the listener margins and slips; their '
         'render-law exclusions are reported separately. The strict fine '
         'pull and paired-pull cases grade the INTERNAL render law.',
    measurement_head='132d79e7f38212cedf0e344a39d0f811566a1d1b',
    current_head=__import__('subprocess').check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(), baseline_provenance='56 baseline cases are attested by resume/baseline-recovered-receipts.json (original driver rc line, log SHA-256 re-verified against the graded log, binary SHA-256); 52 of them have no per-case command file. The other 72 have per-case command and rc files from a single driver.',
    identity='../resume/final-doc-merge-identity.json', groups=groups)
(out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
(out/'all.rc').write_text('0\n')
print(json.dumps(summary, indent=2))
