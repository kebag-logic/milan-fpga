#!/usr/bin/env python3
"""Source-level mutants of the round 2 rules: each edits one expression in a scratch copy of the harness directory
and runs the harness's own self-test. Usage: source_mutants.py <clone-root> <scratch-dir> [jobs]
A mutant SURVIVES when the self-test still exits 0."""
import concurrent.futures, shutil, subprocess, sys
from pathlib import Path
root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
H = 'tb/verilator/ctrl_service_hooks'
M = [  # id, file, old, new, count-expected
 # held_row, missing branch
 ('hm-group', 'run.py', "return dict(hook='H-COUNTERS', group='hooks-counters', probe=held['probe'], path='counters.held',\n                    row='GET_COUNTERS push, held '", "return dict(hook='H-COUNTERS', group='hooks-x', probe=held['probe'], path='counters.held',\n                    row='GET_COUNTERS push, held '"),
 ('hm-path', 'run.py', "path='counters.held',\n                    row='GET_COUNTERS push, held '", "path='counters.x',\n                    row='GET_COUNTERS push, held '"),
 ('hm-interface', 'run.py', "'(H-COUNTERS)', interface=0, family='notify', ms=0.0", "'(H-COUNTERS)', interface=1, family='notify', ms=0.0"),
 ('hm-family', 'run.py', "'(H-COUNTERS)', interface=0, family='notify', ms=0.0", "'(H-COUNTERS)', interface=0, family='aecp', ms=0.0"),
 ('hm-ms', 'run.py', "family='notify', ms=0.0, cpu_cycles=0, wait_ms=0.0,", "family='notify', ms=1.0, cpu_cycles=0, wait_ms=0.0,"),
 ('hm-cycles', 'run.py', "family='notify', ms=0.0, cpu_cycles=0, wait_ms=0.0,", "family='notify', ms=0.0, cpu_cycles=1, wait_ms=0.0,"),
 ('hm-wait', 'run.py', "family='notify', ms=0.0, cpu_cycles=0, wait_ms=0.0,", "family='notify', ms=0.0, cpu_cycles=0, wait_ms=9.0,"),
 ('hm-bound', 'run.py', "bound_ms=hooks.bound_ms('notify'), within=False, unbounded=True, loaded=False,", "bound_ms=18.0, within=False, unbounded=True, loaded=False,"),
 ('hm-loaded', 'run.py', "within=False, unbounded=True, loaded=False,", "within=False, unbounded=True, loaded=True,"),
 ('hm-margin', 'run.py', "normative_ms=hooks.COUNTERS_NORMATIVE_MS, margin_ms=0.0, ahead=0, missing=True", "normative_ms=hooks.COUNTERS_NORMATIVE_MS, margin_ms=5.0, ahead=0, missing=True"),
 ('hm-ahead', 'run.py', "margin_ms=0.0, ahead=0, missing=True", "margin_ms=0.0, ahead=3, missing=True"),
 # held_row, measured branch
 ('hp-eligible-end', 'run.py', "-(-(held['end'] - held['eligible']) * spec['cpu_hz'] // spec['sys_hz'])", "-(-(held['end']) * spec['cpu_hz'] // spec['sys_hz'])"),
 ('hp-hz-swap', 'run.py', "* spec['cpu_hz'] // spec['sys_hz'])\n    return dict(hook='H-COUNTERS'", "* spec['sys_hz'] // spec['cpu_hz'])\n    return dict(hook='H-COUNTERS'"),
 ('hp-interface', 'run.py', "interface=0, family='notify', ms=held['ms'],", "interface=1, family='notify', ms=held['ms'],"),
 ('hp-family', 'run.py', "interface=0, family='notify', ms=held['ms'],", "interface=0, family='aecp', ms=held['ms'],"),
 ('hp-ms', 'run.py', "family='notify', ms=held['ms'], cpu_cycles=cycles", "family='notify', ms=held['ms'] + 1, cpu_cycles=cycles"),
 ('hp-margin-ms', 'run.py', "hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 5)", "hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'], 5)"),
 ('hp-margin-round', 'run.py', "hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 5), ahead=0)", "hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 0), ahead=0)"),
 ('hp-ahead', 'run.py', "- held['ms'], 5), ahead=0)", "- held['ms'], 5), ahead=3)"),
 ('hp-group', 'run.py', "return dict(hook='H-COUNTERS', group='hooks-counters', probe=held['probe'], path='counters.held',\n                row='GET_COUNTERS push, held until", "return dict(hook='H-COUNTERS', group='hooks-x', probe=held['probe'], path='counters.held',\n                row='GET_COUNTERS push, held until"),
 ('hp-row-ms-zero', 'run.py', "family='notify', ms=held['ms'], cpu_cycles=cycles", "family='notify', ms=0.0, cpu_cycles=cycles"),
 # summary
 ('s-narrow-within', 'run.py', "narrow = sum(r['within'] and r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES for r in mine)", "narrow = sum(r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES for r in mine)"),
 ('s-narrow-le', 'run.py', "narrow = sum(r['within'] and r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES for r in mine)", "narrow = sum(r['within'] and r['slack_cycles'] <= hooks.LAYOUT_SWING_CYCLES for r in mine)"),
 ('s-misses-unbounded', 'run.py', "misses=sum(not r['within'] for r in mine)", "misses=sum(not r['within'] and not r['unbounded'] for r in mine)"),
 ('s-loaded-only', 'run.py', "for loaded in (False, True):", "for loaded in (True,):"),
 ('s-alone-only', 'run.py', "for loaded in (False, True):", "for loaded in (False,):"),
 ('s-key-wait', 'run.py', "key=lambda r: (r['unbounded'], r['ms'] - r['wait_ms']))", "key=lambda r: (r['unbounded'], r['ms'] + r['wait_ms']))"),
 ('s-key-min', 'run.py', "top = max(part, key=lambda r: (r['unbounded'], r['ms'] - r['wait_ms']))", "top = min(part, key=lambda r: (r['unbounded'], r['ms'] - r['wait_ms']))"),
 ('n-finding-le', 'run.py', "elif r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES:", "elif r['slack_cycles'] <= hooks.LAYOUT_SWING_CYCLES:"),
 # the plant rule
 ('p-no-colon', 'run.py', "finding.startswith(plant_wanted(plant) + ':')", "finding.startswith(plant_wanted(plant))"),
 ('p-contains', 'run.py', "finding.startswith(plant_wanted(plant) + ':')", "(plant_wanted(plant) + ':') in finding"),
 ('p-rc-escape', 'run.py', "return 0 if caught else 1\n    unapplied", "return 0 if caught else 2\n    unapplied"),
 ('p-main-reads-words', 'run.py', "caught = plant_findings(plant[1], graded['findings'])", "caught = [x for x in graded['findings'] if x.startswith(plant[1].words + ':')]"),
 ('p-wrong-probe-disc', 'hooks.py', "'H-DISC', 'hooks-late-disc.entity_departing.if0'", "'H-DISC', 'hooks-disc-aging.available.if0'"),
 ('p-arm-dropped', 'hooks.py', "'hooks-counters', 'LATE H-COUNTERS', 'answering', 'counters.first.if0'", "'hooks-counters', 'LATE H-COUNTERS', 'idle', 'counters.first.if0'"),
 ('p-counters-probe-all', 'hooks.py', "'hooks-counters', 'LATE H-COUNTERS', 'answering', 'counters.first.if0'", "'hooks-counters', 'LATE H-COUNTERS', 'answering', 'counters.all.if0'"),
 # the amended column: a verdict reading it with bound_ms left as written
 ('a-within-reads-column', 'run.py', "bound_ms=bound, within=not unbounded and row['ms'] <= bound, unbounded=unbounded,", "bound_ms=bound, within=not unbounded and row['ms'] <= bound + (hooks.AMENDED_SRP_MS - hooks.bound_ms('srp') if row['family'] == 'srp' else 0), unbounded=unbounded,"),
 ('a-queued-within-reads-column', 'run.py', "bound_ms=bound, within=not unbounded and row['ms'] <= bound, unbounded=unbounded,", "bound_ms=bound, within=not unbounded and row['ms'] <= (60.0 if row['path'][0].startswith('counters.all') else bound), unbounded=unbounded,"),
 ('a-finding-reads-column', 'run.py', "        elif not r['within']:\n            what =", "        elif r['ms'] > hooks.amended_ms(r, 2) or r['unbounded']:\n            what ="),
 ('a-summary-reads-column', 'run.py', "misses=sum(not r['within'] for r in mine)", "misses=sum(r['ms'] > hooks.amended_ms(r, 2) for r in mine)"),
 ('a-exit-reads-column', 'run.py', "lates = [x for x in graded['findings'] if x.startswith(('LATE ', 'NARROW '))]", "lates = [r for r in graded['rows'] if r['ms'] > hooks.amended_ms(r, spec['interfaces'])]"),
 ('a-slack-reads-column', 'run.py', "        r['slack_cycles'] = slack_cycles(r, spec['cpu_hz'])", "        r['slack_cycles'] = slack_cycles(dict(r, bound_ms=hooks.amended_ms(r, 2)), spec['cpu_hz'])"),
 ('a-hook-srp-all', 'hooks.py', "    if r['hook'] == 'H-SRP':\n        return AMENDED_SRP_MS", "    if r['hook'] in ('H-SRP', 'H-MAAP'):\n        return AMENDED_SRP_MS"),
 ('a-order', 'hooks.py', "    if r['path'].startswith(QUEUED_PATH):\n        return AMENDED_QUEUED_CEILING_MS[interfaces]\n", ""),
 ('a-loaded-queued', 'hooks.py', "QUEUED_PATH = 'counters.all'", "QUEUED_PATH = ('counters.all', 'counters.loaded')"),
 ('a-held-queued', 'hooks.py', "QUEUED_PATH = 'counters.all'", "QUEUED_PATH = ('counters.all', 'counters.held')"),
 ('a-notify-queued', 'hooks.py', "QUEUED_PATH = 'counters.all'", "QUEUED_PATH = ('counters.all', 'aecp_fanout')"),
 ('a-cell-bound', 'run.py', "bounds = {hooks.amended_service_ms(r, interfaces) for r in graded['rows'] if r['hook'] == name}", "bounds = {hooks.bound_ms(r['family']) for r in graded['rows'] if r['hook'] == name}"),
 ('a-cell-gone', 'run.py', "f\"{cell(s['worst'].get('loaded'))} | {amended_cell(name, graded, interfaces)} | \"", "f\"{cell(s['worst'].get('loaded'))} | - | \""),
 ('a-row-cell-interfaces', 'run.py', "{hooks.amended_ms(r, interfaces):g}", "{hooks.amended_ms(r, 1):g}"),
 ('a-row-cell-bound', 'run.py', "{hooks.amended_ms(r, interfaces):g}", "{r['bound_ms']:g}"),
 ('a-table-interfaces', 'run.py', "    interfaces = spec['interfaces']\n", "    interfaces = 1\n"),
 # the ALL rows
 ('c-row-recipients', 'hooks.py', "[notify_end(k, n)], recipients=everyone, path=f'counters.all.t{k}.i{n}'), [])", "[notify_end(k, n)], recipients=everyone[:1], path=f'counters.all.t{k}.i{n}'), [])"),
 ('c-whole-last', 'hooks.py', "entries = [(whole, []), *rows]", "entries = [*rows, (whole, [])]"),
 ('c-first-row-dropped', 'hooks.py', "            for k, n in others]\n    whole =", "            for k, n in others[1:]]\n    whole ="),
 ('c-wait-count', 'hooks.py', "[f'tx {aecp} {len(everyone) * len(others)} within {900 * MS}'])", "[f'tx {aecp} {len(everyone)} within {900 * MS}'])"),
 ('c-row-family', 'hooks.py', "f'GET_COUNTERS push, descriptor {k} {n} of ALL (H-COUNTERS)',\n                   'notify',", "f'GET_COUNTERS push, descriptor {k} {n} of ALL (H-COUNTERS)',\n                   'aecp',"),
 ('c-row-name', 'hooks.py', "Probe(f'counters.all.t{k}.i{n}.if0'", "Probe(f'all.t{k}.i{n}.if0'"),
]
def one(m):
    name, file, old, new = m
    d = scratch / name
    shutil.rmtree(d, ignore_errors=True)
    (d / H).mkdir(parents=True)
    for p in (root / H).iterdir():
        if p.is_file(): shutil.copy(p, d / H / p.name)
    # every other path of the checkout by link, read only: the harness finds its siblings through ROOT.
    for top in root.iterdir():
        if top.name not in ('tb', '.git'): (d / top.name).symlink_to(top)
    (d / '.git').symlink_to(root / '.git')
    tb = d / 'tb'; ver = tb / 'verilator'
    for sib in (root / 'tb').iterdir():
        if sib.name != 'verilator': (tb / sib.name).symlink_to(sib)
    for sib in (root / 'tb/verilator').iterdir():
        if sib.name != 'ctrl_service_hooks': (ver / sib.name).symlink_to(sib)
    f = d / H / file
    text = f.read_text()
    if text.count(old) != 1:
        return name, 'ANCHOR', f'{text.count(old)} matches'
    f.write_text(text.replace(old, new))
    r = subprocess.run([sys.executable, '-B', str(d / H / 'run.py'), '--self-test'], capture_output=True, text=True, timeout=300)
    fails = [l[:150] for l in r.stdout.splitlines() if l.startswith('FAIL ')]
    esc = [l[:150] for l in r.stdout.splitlines() if 'ESCAPED ' in l and l.startswith('MUTANT')]
    tail = r.stderr.strip().splitlines()[-1][:150] if r.returncode and not fails and not esc and r.stderr.strip() else ''
    shutil.rmtree(d, ignore_errors=True)
    return name, 'SURVIVED' if r.returncode == 0 else 'killed', ' ; '.join(fails[:2] + esc[:1] + ([tail] if tail else []))
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    out = list(pool.map(one, M))
for n, s, w in out: print(f'{s:9s} {n:28s} {w}')
print('total', len(out), 'killed', sum(s == 'killed' for _, s, _ in out), 'survived', sum(s == 'SURVIVED' for _, s, _ in out), 'anchor', sum(s == 'ANCHOR' for _, s, _ in out))
