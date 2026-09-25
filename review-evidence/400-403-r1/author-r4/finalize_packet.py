from pathlib import Path
import json
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/400-403-declaration-truth')
START = '7463ab0889da9a95fce7c921e386d6035d69778e'
BASE = '864b36f5e9450ef64f75ca3f0d68c44330e447d7'
HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT)
records = [json.loads(line) for line in (OUT / 'gates.jsonl').read_text().splitlines()]
latest = {row['label']: row for row in records}
required = [f'bank-{i:02}' for i in range(48)]
required += [f'dp-{i:02}' for i in range(33)]
required += [f'sweep-{i}-of-5' for i in range(5)]
required += ['builder-no-compiler', 'nvm-quick', 'nvm-full', 'docs-git',
             'docs-no-git', 'behave', 'lint-check', 'declaration-gate',
             'ooc-base', 'ooc-head-main', 'ooc-head-csr',
             'final-cold-pp_shadow', 'final-cold-csr',
             'final-restored-pp_shadow', 'final-restored-csr']
assert all(latest[label]['exit_code'] == 0 for label in required)
assert all(latest[f'final-mutant-{n}']['exit_code'] == 2 for n in (41, 43, 35))

expected = set((OUT / 'sweep-inventory.log').read_text().splitlines())
seen = []
sweep_rows = []
for index in range(5):
    label = f'sweep-{index}-of-5'
    log = (OUT / (label + '.log')).read_text()
    names = re.findall(r'^PASS\s+(\S+)', log, re.M)
    seen.extend(names)
    summary = re.search(r'^suites: (\d+)\s+passed: (\d+)\s+failed: 0\s+timed out: 0$', log, re.M)
    assert summary and int(summary[1]) == int(summary[2]) == len(names)
    sweep_rows.append(f'| {index}/5 | {len(names)} | {latest[label]["seconds"]:.3f} | 0 | [{label}.log]({label}.log) |')
assert len(seen) == len(set(seen)) and set(seen) == expected
assert len(expected) == 55

cold = {suite: latest['final-cold-' + suite]['seconds'] for suite in ('pp_shadow', 'csr')}
assert all(value < 1800 for value in cold.values())
timing_rows = []
for suite, before in (('pp_shadow', 'before-pp-shadow-cold'), ('csr', 'before-csr-cold')):
    timing_rows.append(f'| {suite} | {latest[before]["seconds"]:.3f} | {cold[suite]:.3f} | 1800 |')
area = json.loads((OUT / 'area.json').read_text())
area_table = (OUT / 'area-delta.md').read_text()
area_absolute = '\n'.join(f'- `{top}`: LUT_TOT {row["base"]["LUT_TOT"]} -> {row["head"]["LUT_TOT"]}; FF {row["base"]["FF"]} -> {row["head"]["FF"]}.' for top, row in area.items())
commits = subprocess.check_output(['git', 'log', '--reverse', '--format=%H %s', START + '..HEAD'], cwd=ROOT, text=True).strip()
dp_seconds = sum(latest[f'dp-{i:02}']['seconds'] for i in range(33))
changes = (OUT / 'change-summary.md').read_text()
review_source = (OUT / 'review-source.txt').read_text()
handoff = f'''[A319] Round 3 handoff

Status: local author validation complete; independent re-review remains required.
Head: `{HEAD}`
Starting head: `{START}`
Area and added-line base: `{BASE}`
Branch: `400-403-declaration-truth`
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`

Assignment: https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5834690477
Review findings: PR #566 comments 5834667344 and 5834684851.
Decisions: #400 comments 5770922734 and 5770922898.
Items 1-3 are addressed. S1 suggestions remain outside scope under #495.

## Commits

```
{commits}
```

Both subjects are one line, with no body or trailers.

{changes}
## Mutants

Each exact reviewer mutation was applied to the final head, run against the
suite's default target, and restored byte-for-byte. Restored defaults passed.

| Receipt | Mutation | Default target | Exit | Verdict |
|---|---|---|---:|---|
| 41 | Remove wrapper startup-VID binding | pp_shadow | 2 | DETECTED: three VID checks fail |
| 43 | Remove datapath startup-VID binding | pp_shadow | 2 | DETECTED: three VID checks fail |
| 35 | Mask both live cold-reset admission bits | csr | 2 | DETECTED: two real-output checks fail |

Exact mutation text and restoration: `run_final_mutants.py`.
Receipts: `final-mutant-41.log`, `final-mutant-43.log`, `final-mutant-35.log`.

## Wall clock

Both measurements use clean object directories, default targets and the
same tool selection. The final run enforces the unchanged deadline.

| Suite | Before, seconds | Final head, seconds | Budget, seconds |
|---|---:|---:|---:|
{chr(10).join(timing_rows)}

No changed suite exceeded its budget. No deadline was raised.

## Default sweep

All 55 default suites ran exactly once across the five native chunks.
No native chunk failed or timed out.

| Chunk | Suites | Seconds | Exit | Receipt |
|---|---:|---:|---:|---|
{chr(10).join(sweep_rows)}

The separate expanded datapath default recipe also passed all 33 commands,
totaling {dp_seconds:.3f} seconds. `dp-commands.json` records the exact expansion.
Every command exit appears below. No gate command was piped.

## Area

Repository recipe: `bash syn/yosys/ooc.sh`, default Arty shape,
`synth_xilinx -family xc7 -flatten`, with no parameter override.
The CSR measurement adds only its top entry to the temporary recipe list.
For the base arm, the ten changed HDL/header inputs were read from `{BASE}`
into this checkout, then restored byte-for-byte. No other checkout or donor
edit was used. `run_ooc.py` records that procedure and verifies restoration.

{area_absolute}

All measured counter deltas:

{area_table}

Full counts: `area.json`. Receipts: `ooc-base.log`, `ooc-head-main.log`,
`ooc-head-csr.log`; executable identities: `tool-versions.log`.

## Validation notes and limits

- All 48 manager bank entries returned 0. Entry 47 uses the read-only
  helper's exact logic with only its compiler-argv receipt destination
  relocated into this packet. The pinned SDK was verified read-only.
- Both complete builder modes returned 0. The compiler-absent adapter makes
  the three cross-compiler candidates unavailable while retaining host
  compilers. Its compiler-dependent arms are explicitly unmeasured; the
  separate SDK run covers them.
- Co-simulation quick: 315 checks passed. Full: 465 checks passed and
  39/39 named mutants killed. The native sweep repeats the full target.
- All 344 behavior scenarios passed, with 1,739 steps and no skipped scenario.
- Both documentation inventory modes passed. The no-git mode uses an
  absent `GIT_DIR` to select the same filesystem walk without removing metadata.
- The installed HDL analysis front end ran: four existing pinned-processor
  findings match its ratchet; no first-party finding was added.
- An initial C++ recipe-style check failed because added flag groups did
  not individually spell both warning flags. The second commit fixes this;
  the repeated gate passes. Its initial failure remains recorded.
- Historical placed-utilization calibration was NOT RUN: its report is
  absent. Field-campaign arms report their absent generator. No hardware,
  field measurement, hosted result or candidate-merge proof is claimed.
- The changed-signature caller census is recorded in `caller-census.log`.

## Gates

Pending table rendering.

## Remaining duties

The manager must publish the local head and evidence, run the trusted local
workflow replica and required hosted checks, obtain independent re-review
and reviewer-owned lens coverage, then follow authorized merge and containment.
No push, PR edit, merge, hardware operation or donor edit was performed here.
`PR-BODY.md` is the complete current PR body with the Round 3 update prepared.
The final public action is the requested `[A319] REVIEW READY` issue comment.

## Public evidence source

```
{review_source.rstrip()}
```
'''
(OUT / 'HANDOFF.md').write_text(handoff)
subprocess.run(['python3', str(OUT / 'render_gate_table.py')], check=True)

body = json.loads(subprocess.check_output(['gh', 'pr', 'view', '566', '--json', 'body'], cwd=ROOT, text=True))['body']
body = re.sub(r'^\[[AR]\d+\]', '[A319]', body, count=1)
assert body.startswith('[A319]')
body = re.sub(r'\n## Round 3\n.*?(?=\n## |\Z)', '', body, flags=re.S).rstrip()
body += f'''

## Round 3

The saved-state co-simulation header now uses the shared boot-policy derivation. Default protocol-wrapper and register suites generate committed fixtures for a distinct startup VID, a declared CRF output, and nonzero admission reset bits. Headers come from the builder. Reset, allocation, pruning, presentation-row and declaration-count text now matches the implemented contracts.

Local validation at `{HEAD}` passed: all 48 manager-bank entries, both complete builder modes, all 55 default suites in five chunks, all 33 explicit datapath recipe commands, quick and full co-simulation, documentation and source gates, and 344 behavior scenarios. Full co-simulation killed all 39 named mutants. Review mutants 41, 43 and 35 fail the default targets with three, three and two checks respectively; restored targets pass.

Clean default-target wall clocks changed from 18.502 to {cold['pp_shadow']:.3f} seconds for the protocol-wrapper suite and from 30.480 to {cold['csr']:.3f} seconds for the register suite. Both remain below their unchanged 1,800-second budgets. The repository area recipe reports zero change in every measured counter for all three changed RTL modules at the default shape.

Compiler-dependent arms are explicitly unmeasured in the compiler-absent mode and covered by the separate SDK run. The historical placed-utilization report and field-campaign generator remain unavailable; no hardware or field result is claimed. Hosted exact-head validation and independent re-review remain required.
'''
assert all(all(value == 0 for value in row['delta'].values()) for row in area.values())
assert body.count('Closes #400') == body.count('Closes #403') == 1
assert '/home/' not in body and '/Users/' not in body
assert not re.search(r'\b(?:Co-authored-by|Generated by)\b', body, re.I)
(OUT / 'PR-BODY.md').write_text(body)
print('Final packet assembled for ' + HEAD)
