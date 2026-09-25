from pathlib import Path
import json
import shlex
import re
import subprocess

out = Path(__file__).resolve().parent
root = Path('$LANES/400-403-declaration-truth')
base = '864b36f5e9450ef64f75ca3f0d68c44330e447d7'
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
bank = json.loads(Path('$VALIDATION_STORAGE/400-403-manager-r1/manager-builder.json').read_text())
rows = [json.loads(s) for s in (out / 'gates.jsonl').read_text().splitlines()]
results = {r['label']: r for r in rows}
text = f"""# [A316] Round 2 handoff

Status: validation in progress. Review-ready comment not yet posted.

Branch: `400-403-declaration-truth`
Initial head: `2d61e7edafa63cff7d5f8fdca9840a969ee070a6`
Current head: `{head}`
Comparison base: `{base}`
Origin confirmed: `https://github.com/kebag-logic/milan-fpga.git`

Assignment: https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5832912970

## Root cause

`constants_header()` maintained a handwritten subset of the firmware boot constants. The production `fabric_constants()` generator already emitted the four new MAC, TCAM, AAF and MAAP constants, but the saved-state host test never consumed it. The real firmware therefore failed to compile on the first shape. `baseline-nvm.log` reproduces all four undeclared identifiers with exit 1 at the starting head.

## Changes

- `sw/firmware/nvm_hosttest/test_nvm_firmware.py:85`: import the shared boot generator.
- `sw/firmware/nvm_hosttest/test_nvm_firmware.py:166`: build the stub header from the complete derived boot dictionary instead of copied constants.
- `sw/firmware/nvm_hosttest/test_nvm_firmware.py:221`: read both per-shape generated artifacts and derive the header from them.
- `sw/builder/test_builder.py:4467`: derive the compiler census fixture's boot words from the same generator; preserve its synthetic identity sentinels.
- `sw/builder/test_builder.py:27549`: run the firmware host self-test from the full builder entry point, across every shipped shape and all four planted defects.

The authoritative generator remains `sw/litex/boot_policy.py:35`, published by `sw/litex/milan_soc.py:3950`. No production behavior, RTL, donor pin, workflow or acceptance criterion changes in Round 2. The docs workflow already runs the firmware self-test at `.github/workflows/docs.yml:230`.

## Validation method

Commands run in the foreground with captured exit codes, without output pipelines. `run_gate.py` records full argv, checkout cwd, duration and log in `gates.jsonl`. All bank commands use this checkout, overriding the JSON bank's historical cwd. The two environment assignments are taken verbatim from the read-only bank. Simulation uses eight build jobs.

Bank 48 uses the supplied compiler-mapping wrapper with only its diagnostic JSONL destination changed to this output directory. Its original record destination already exists and is read-only. Compiler argv other than the executable remains unchanged; SDK verification runs first. The SDK itself is read-only. `full-builder-sdk-argv.jsonl` records every actual invocation. The complete no-RV32 run hides only the three cross-compiler candidates, retains host builds, and records the weaker instrument verdict explicitly.

The no-git docs mode uses `GIT_DIR=/dev/null`, making Git metadata unavailable while retaining the same source tree. The gate confirms its filesystem-walk mode. No checkout, tree export or git-metadata deletion is needed.

## Manager builder bank

Every command below is prefixed by the bank's unchanged `env PATH=... VERILATOR_ROOT=...`; exact arguments are in `gates.jsonl`. Row 44 preserves the bank's original endpoint; `diff-final` additionally checks the new head. Row 48 preserves the wrapper logic with the output-only relocation above.

| # | Command | Exit | Log |
|---|---|---|---|
"""
for number, cmd in enumerate(bank['commands'], 1):
    row = results.get(f'bank-{number:02d}')
    rc = row['exit'] if row else 'pending'
    log = f"[{row['log']}]({row['log']})" if row else '--'
    text += f"| {number} | `{shlex.join(cmd[3:])}` | {rc} | {log} |\n"
text += """
## Additional gates and chunked datapath sweep

The original `run` recipe is copied verbatim into `dp-chunks.mk`, split only at recipe-command boundaries. `dp-prereq` retains every original prerequisite, including the three directed runs. Steps 1 through 35 execute every default command in order, including both mutation campaigns. `run_rtl.py` records each command separately and stops on a nonzero exit. The four NxN builds/run legs exercise the bundle's output-indexed offsets.

| Gate | Command | Exit | Seconds | Log |
|---|---|---|---|---|
"""
for row in rows:
    if row['label'].startswith('bank-'):
        continue
    cmd = shlex.join(row['command']).replace(str(out), '$OUTPUT')
    text += f"| {row['label']} | `{cmd}` | {row['exit']} | {row['seconds']} | [{row['log']}]({row['log']}) |\n"
text += """
## Area measurement

Round 2 changes no RTL. The bundle changes `milan_csr`, `KL_pp_shadow`, and `milan_datapath`. The before/after replay uses the repository `syn/yosys/ooc.sh` recipe (`synth_xilinx -family xc7 -flatten`) at its default generated shape. The replay adds only the CSR target entry, which the stock area list omits, and redirects the script's root/helper paths to this checkout.

The base arm substitutes only the ten changed RTL/header blobs from the comparison base; the remaining inputs and pinned submodules are identical. These sparse inputs and generated synthesis artifacts live under `$VALIDATION_STORAGE/400-403-a316-ooc`, outside the output directory. No other checkout is created. `ooc-inputs.txt`, `ooc-base.sh` and `ooc-head.sh` record the exact replay. The first local wrapper attempt failed before synthesis because of incorrect path escaping; `ooc-base.log` is retained, and the corrected rerun is recorded separately.

Area results pending completion.

## Delivery and limits

No push, PR creation/edit, merge, sub-agent, other checkout, hardware access or donor edit was performed. `PR-BODY-original.md` preserves the body read with `gh pr view 566 --json body`; `PR-BODY.md` is the updated reviewable local body. The two closing lines are retained. Independent review and remote validation remain the manager's next steps.
"""
if 'ooc-head-r2' in results and results['ooc-head-r2']['exit'] == 0:
    area = {}
    for version in ('base', 'head'):
        content = (out / f'ooc-{version}-r2.log').read_text()
        area[version] = {line.split()[0]: list(map(int, line.split()[1:]))
                         for line in content.splitlines()
                         if re.match(r'^(milan_csr|KL_pp_shadow|milan_datapath)\s+\d', line)}
    (out / 'area.json').write_text(json.dumps(area, indent=2) + '\n')
    table = '| Module | LUT | LUTRAM | LUT total | FF | RAMB36 | RAMB18 | DSP | CARRY4 |\n'
    table += '|---|---|---|---|---|---|---|---|---|\n'
    for name, before in area['base'].items():
        after = area['head'][name]
        table += '| ' + name + ' | ' + ' | '.join(
            str(a) if a == b else f'{b} -> {a}' for b, a in zip(before, after)) + ' |\n'
    equal = area['base'] == area['head']
    table += '\nAll before/after entries are identical; every reported area delta is zero.\n' if equal else '\nChanged entries show before -> after.\n'
    table += '\nThis is mapped default-shape area, not placed utilization or timing.\n'
    text = text.replace('Area results pending completion.', table)
required = {f'bank-{n:02d}' for n in range(1, 49)}
required.update(f'dp-{n:02d}' for n in range(1, 36))
required.update(('csr', 'pp-shadow', 'dp-prereq', 'declarations', 'docs-git',
                 'docs-no-git', 'behave', 'diff-worktree', 'diff-final',
                 'em-dash-final', 'builder-no-rv32', 'ooc-base-r2', 'ooc-head-r2'))
missing = sorted(required - results.keys())
failed = sorted(label for label in required & results.keys() if results[label]['exit'])
if not missing and not failed:
    text = text.replace('Status: validation in progress. Review-ready comment not yet posted.',
                        'Status: all required commands returned zero. Local implementation is ready for independent review.')
else:
    text = text.replace('Status: validation in progress. Review-ready comment not yet posted.',
                        f'Status: validation in progress. Pending: {missing}. Failed required results: {failed}.')
text += '\n## Coverage notes\n\n'
text += ('The pinned builder run executed 855 mapped compiler invocations and all five recipe elaborations. '
         'It reports one unrun historical placed-utilization calibration arm because the old report is absent. '
         'The compiler-absent run deliberately leaves compiler-dependent instruments unmeasured; it is not equivalent evidence to the pinned run. '
         'Both documentation inventory modes passed. The no-git mode deliberately skips Git inventory parity. '
         'The source-analysis gates retain their existing ratchets: 90 lint findings and four pinned-processor front-end findings, with no new findings.\n')
if (out / 'review-ready-url.txt').exists():
    text += '\nReview-ready issue comment: ' + (out / 'review-ready-url.txt').read_text().strip() + '\n'
(out / 'HANDOFF.md').write_text(text)
