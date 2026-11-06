"""Cross-check the figures the pages state at the head against the published round-6 receipts.

usage: figures_check.py <tree> <author-r6 receipts dir>
Each check names a page sentence's figure and the receipt it must come from. Exit 1 on a mismatch.
"""
import json
import re
import sys
from pathlib import Path

tree, rec = Path(sys.argv[1]), Path(sys.argv[2]) / 'runs'
bad = 0


def fmt(n):
    return f'{n:,}'


def want(page, text, what):
    """Report whether the page's text holds `what`."""
    global bad
    ok = what in text
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {page}: {what}")


readme = (tree / 'tb/verilator/nvm_split_target/README.md').read_text()
nvm = (tree / 'sw/firmware/ctrl_nvm/README.md').read_text()
arch = (tree / 'docs/ARCHITECTURE_HW_SW_SPLIT.md').read_text()
tables = {p: (rec / f'target-{p}-table.md').read_text() for p in ('1x1', '8x8')}
for point, table in tables.items():
    cap = re.search(r'(\d+) records in (\d+) steps; CPU time ([\d,]+) cycles, ([\d.]+) ms; elapsed [\d,]+ cycles, '
                    r'([\d.,]+) ms; longest step ([\d,]+) cycles, ([\d.]+) ms', table)
    records, steps, cyc, ms, elapsed, long_c, long_ms = cap.groups()
    row = f'{steps} | {cyc} | {ms} | {float(elapsed.replace(",", "")):,.3f} | {long_ms} |'
    want('nvm_split_target capture row ' + point, readme, row)
    want('ctrl_nvm cycles ' + point, re.sub(r'\s+', ' ', nvm), cyc)
    for phase, n, c, m in re.findall(r'^\| (capture|erase|idle|poll|program|read|seal) \| (\d+) \| ([\d,]+) \| '
                                     r'([\d.]+) \| yes', table, re.M):
        want(f'phase {phase} {point}', readme, f'{n}, {c} ({m})')
    for case, entries, boot in re.findall(r'^\| (valid|absent|torn|version) \| pass \| (\d+) apply entries, boot '
                                          r'([\d,]+) CPU cycles', table, re.M):
        ms = int(boot.replace(',', '')) / 50e3
        want(f'boot {case} {point}', readme, f'{entries}, {boot} ({ms:.1f})')
    slow = re.search(r'slow-step \| caught \| (.+?) \|', table).group(1)
    want(f'slow-step {point}', readme, slow)
want('architecture', arch, '103.4 ms of CPU time over 1.64 s elapsed')

boot = (tree / 'tb/verilator/ctrl_split_boot/README.md').read_text()
for shape in ('1x1', '8x8'):
    rows = {}
    for stage, log in (('staged', f'splitboot-{shape}.log'), ('none', f'control-none-{shape}.log')):
        text = (rec / log).read_text()
        ready = re.search(r'BOOT ready at bus cycle \d+ \((\d+) CPU cycles\): ([\d.]+) ms', text)
        uart = re.findall(r'^UART (milan_\w+): \d+ bytes; span ([\d.]+) ms; to the first byte ([\d.]+) ms; '
                          r'longest gap between bytes ([\d.]+) ms', text, re.M)
        status = next(u for u in uart if u[0] == 'milan_status')
        gets = [u for u in uart if u[0] == 'milan_gettime']
        worst = [max(float(g[i]) for g in gets) for i in (1, 2, 3)]
        row = (f'| {stage} | {ready.group(2)} ms | {fmt(int(ready.group(1)))} | 18 of 18 equal | '
               f'{status[1]} / {status[2]} / {status[3]} ms | {worst[0]:.3f} / {worst[1]:.3f} / {worst[2]:.3f} ms |')
        want(f'ctrl_split_boot {shape}', boot, row)
        rows[stage] = int(ready.group(1))
    want(f'stage cost {shape}', boot, f'{rows["staged"] - rows["none"]}')
print('mismatches:', bad)
raise SystemExit(1 if bad else 0)
