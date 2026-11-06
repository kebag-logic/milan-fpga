#!/usr/bin/env python3
"""Each figure the delta restated, against the published receipts of the head. Usage: figure_check.py RECEIPT_RUNS CLONE."""
import json, re, sys
from pathlib import Path

runs, clone = Path(sys.argv[1]), Path(sys.argv[2])
read = lambda p: (clone / p).read_text()
res = {p: json.loads((runs / f'target-{p}-results.json').read_text()) for p in ('1x1', '8x8')}
cases = {p: {r['case']: r for r in res[p]['results']} for p in res}
bad = 0
def want(page, text, label):
    global bad
    ok = text in read(page)
    bad += not ok
    print(('ok  ' if ok else 'MISS'), label, repr(text))
tgt, nvm, arch, boot = ('tb/verilator/nvm_split_target/README.md', 'sw/firmware/ctrl_nvm/README.md',
                        'docs/ARCHITECTURE_HW_SW_SPLIT.md', 'tb/verilator/ctrl_split_boot/README.md')
for p in ('1x1', '8x8'):
    c = cases[p]['commit']; cap = c['capture']; d = cap['decomposed']
    want(tgt, f"| {cap['steps']} | {cap['cycles']:,} | {cap['ms']:.3f} | {cap['elapsed_ms']:,.3f} | {cap['longest_ms']:.3f} | "
              f"{d['per_step_cycles']:,} | {d['per_byte_cycles']} | {d['idle_step_cycles']:,} |", f'capture {p}')
    for ph, v in c['phases'].items():
        want(tgt, f"{v['steps']}, {v['longest_cycles']:,} ({v['longest_ms']:.3f})", f'phase {p} {ph}')
    table = (runs / f'target-{p}-table.md').read_text()
    for case in ('valid', 'absent', 'torn', 'version'):
        m = re.search(rf'\| {case} \| pass \| (\d+) apply entries, boot ([\d,]+) CPU cycles', table)
        cyc = int(m.group(2).replace(',', ''))
        want(tgt, f"{m.group(1)}, {m.group(2)} ({cyc / 50000:.1f})", f'boot {p} {case}')
    m = re.search(r'step 0 \(idle\) takes ([\d.]+) ms', table)
    want(tgt, f"`step 0 (idle) takes {m.group(1)} ms of CPU time, over T_svc 10.0 ms`", f'slow-step {p}')
    m = max(float(x) for x in re.findall(r'\| (?:valid|absent|torn|version) \| \d+ \| [\d,]+ \| ([\d.]+) \|', table))
    print('    longest boot-case step', p, m)
for t in ('1,367,366 CPU cycles (27.35 ms)', '5,168,647 (103.37 ms)', '0.54 s and 1.64 s', 'about 11,066', '16,533',
          'about 266 and 206'):
    want(nvm, t.replace('\n', ' '), 'ctrl_nvm')
want(arch, '103.4 ms of CPU time over 1.64 s', 'architecture')
for name, rows in (('splitboot-1x1', '| 1x1, one interface | staged |'), ('splitboot-8x8', '| 8x8, one interface | staged |'),
                   ('control-none-1x1', '| 1x1, one interface | none |'), ('control-none-8x8', '| 8x8, one interface | none |')):
    log = (runs / f'{name}.log').read_text()
    m = re.search(r'BOOT ready at bus cycle \d+ \((\d+) CPU cycles\): ([\d.]+) ms', log)
    u = re.findall(r'UART (\S+): \d+ bytes; span ([\d.]+) ms; to the first byte ([\d.]+) ms; longest gap between bytes ([\d.]+) ms', log)
    st = [x for x in u if x[0] == 'milan_status'][0]
    gt = [x for x in u if x[0] == 'milan_gettime']
    worst = [max(float(x[i]) for x in gt) for i in (1, 2, 3)]
    row = next(l for l in read(boot).splitlines() if l.startswith(rows))
    expect = (f"{m.group(2)} ms | {int(m.group(1)):,} | 18 of 18 equal | {st[1]} / {st[2]} / {st[3]} ms | "
              f"{worst[0]:.3f} / {worst[1]:.3f} / {worst[2]:.3f} ms |")
    ok = expect in row
    bad += not ok
    print('ok  ' if ok else 'MISS', name, expect, '' if ok else row)
print('figure check:', bad, 'mismatches')
