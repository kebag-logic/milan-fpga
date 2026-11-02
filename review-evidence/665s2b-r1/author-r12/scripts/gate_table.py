#!/usr/bin/env python3
"""Write receipts/gates/TABLE.md from the kept logs: each row's rc is read from its log's rc file, never typed.
usage: gate_table.py"""
import json
import re
from pathlib import Path
T = Path('$VALIDATION_STORAGE/665s2b-a683o')
O = Path('$MANAGEMENT/2026-09-23/665s2b-a683o/receipts/gates')
L = T / 'lane-logs'
head = lambda p: (re.search(r'[0-9a-f]{40}', p.read_text(errors='replace').splitlines()[0]) or [''])[0][:8]
rows = ['| Gate | Command | Head | rc | Result | Receipt |', '|---|---|---|---:|---|---|']
def tail(p, pat):
    lines = [l for l in p.read_text(errors='replace').splitlines() if re.search(pat, l)]
    return lines[-1].strip()[:150] if lines else ''
for gid, cmd, pat in (
    ('diffcheck', '`git diff --check f4c9ad4f HEAD` (the merge base)', r'.'),
    ('diffcheck_merge', '`git diff --check a68536fa HEAD`', r'.'),
    ('py_idiom', '`scripts/check_py_idiom.py`', r'RESULT|PASS|<='),
    ('cpp_idiom', '`scripts/check_cpp_idiom.py`', r'RESULT|PASS|<='),
    ('harness_selftest', '`tb/verilator/ctrl_service_budget/run.py --self-test`', r'^self-test'),
    ('fw_coverage', '`sw/firmware/gtest/fw_coverage.py --check`', r'firmware coverage'),
    ('fw_rv32_selftest', '`sw/firmware/gtest/fw_rv32_selftest.py --require-rv32`', r'self-test|checks'),
    ('gen_mailbox', '`sw/mailbox/gen_mailbox.py --check --crosscheck`', r'finding|OK'),
    ('gen_mailbox_selftest', '`sw/mailbox/gen_mailbox.py --selftest`', r'selftest'),
    ('census', '`sw/mailbox/publication_census.py --check --selftest`', r'RESULT|mutations'),
    ('lint_rtl', '`scripts/lint_rtl.py --check`', r'LINT GATE'),
    ('soc_options', '`sw/builder/test_soc_options.py`', r'RESULT'),
    ('ctrl_memory', '`sw/litex/test_ctrl_memory.py`', r'RESULT'),
    ('boundary_a', '`ctrl_boundary.py --require-rv32 --selftest --without verilator`', r'ctrl_boundary: '),
    ('boundary_b', '`ctrl_boundary.py --require-rv32 --selftest --only verilator`', r'ctrl_boundary: '),
    ('behave', '`cd tests && behave --no-capture -f plain`', r'scenarios passed'),
    ('test_builder', '`sw/builder/test_builder.py --require-rv32`', r'ALL GATES'),
    ('boot_1x1', '`tb/verilator/ctrl_split_boot/run.py`, 1x1', r'^BOOT'),
    ('boot_8x8', '`tb/verilator/ctrl_split_boot/run.py --shape endstation_ax7101_8x8`', r'^BOOT'),
    ('boot_native', '`... --native-controls`', r'native controls'),
    ('boot_plants', '`... --self-test`', r'self-test'),
):
    p = L / f'{gid}.log'
    rc = (L / f'{gid}.rc').read_text().strip()
    rows.append(f"| {gid} | {cmd} | `{head(p)}` | {rc} | {tail(p, pat)} | `gates/lane/{gid}.log` |")
for k in range(4):
    p = T / 'logs' / f'fwfinal-{k}.log'
    text = p.read_text(errors='replace').splitlines()
    rc = text[-1].removeprefix('rc=')
    verdict = tail(p, r'^test_ctrl_firmware|mutants: ')
    extra = tail(p, r'mutants: \d+ of')
    rows.append(f"| firmware self-test, shard {k}/4 | `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard {k}/4` | `{head(p)}` | {rc} | {extra or verdict} | `gates/fw/fwfinal-{k}.log` |")
p = T / 'logs/nvmself.log'
rows.append(f"| store's plants | `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test` | `{head(p)}` | {p.read_text().splitlines()[-1].removeprefix('rc=')} | {tail(p, 'saved-state store gate')} | `gates/fw/nvmself.log` |")
tally = []
for s in range(4):
    d = T / 'sweep2' / f'shard-{s}'
    c = json.loads((d / 'spec/complete.json').read_text())
    log = (d / 'spec/01.log').read_text(errors='replace')
    su = re.search(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)', log)
    ch = re.search(r'checks: (\d+)\s+in-suite failures: (\d+)', log)
    tally.append((su.groups(), ch.groups(), c['exit_code']))
    rows.append(f"| sweep, shard {s}/4 | `bash scripts/run_all_suites.sh <logs> --wait --shard {s}/4`, pinned Verilator 5.050, sv2v v0.0.12, `--no-print-directory` | `{c['head'][:8]}` | {c['exit_code']} | {su.group(1)} suites, {su.group(2)} passed, {ch.group(1)} checks, {ch.group(2)} failures | `gates/sweep/shard-{s}/` |")
sweep = f"{sum(int(t[0][0]) for t in tally)} of {sum(int(t[0][1]) for t in tally)} suites, {sum(int(t[1][0]) for t in tally):,} checks, {sum(int(t[1][1]) for t in tally)} failures"
Path('/tmp/sweep_tally.txt').write_text(f'the full sweep as four shards, {sweep}.')
(O / 'TABLE.md').write_text('\n'.join(rows) + '\n')
print('\n'.join(rows)[-800:])
print(sweep)
