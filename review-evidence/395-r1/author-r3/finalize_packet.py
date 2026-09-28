"""Finish the author handoff only after every assigned gate succeeds."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path('$LANES/395-timing-grade')
OUT = Path('$MANAGEMENT/2026-09-23/395-a393')
HEAD = '3b5603e3d16a164c35329efeb633800fe4fe9f95'
BASE = '8bc97021f28fb7f729418d3a00851c84ea0b50fd'


def git(*args: str) -> str:
    """Read final lane identity and cleanliness."""
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=60).strip()


assert git('rev-parse', 'HEAD') == HEAD
assert git('status', '--porcelain') == ''
assert git('remote', 'get-url', 'origin') == 'https://github.com/kebag-logic/milan-fpga.git'
gates = json.loads((OUT / 'gate-results.json').read_text())
assert len(gates) == 21 and all(r['returncode'] == 0 and r['head'] == HEAD for r in gates)
table = '\n'.join(f'| `{r["gate"]}` | 0 | {r["seconds"]} | `gates/{r["gate"]}.log` |' for r in gates)
state = dict(head=HEAD, base=BASE, branch=git('branch', '--show-current'),
             remote=git('remote', 'get-url', 'origin'), status=git('status', '--porcelain'),
             submodules=git('submodule', 'status'), commit_message=git('log', '-1', '--format=%B'))
(OUT / 'candidate-state.json').write_text(json.dumps(state, indent=2) + '\n')
handoff = f'''[A393] Round 3 author handoff

Status: assigned implementation and local validation complete; independent review pending.
Head: `{HEAD}`. Branch: `395-timing-grade`.
Starting head: `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`.
Base: `{BASE}`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Physical worktree: `$LANES/395-timing-grade`.
Relates to #395. Items 3 and 4 remain open.
Executor: [A393]. Independent reviewers: [R372] and [R373].

Assignment: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860820812
Owner grade decision: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5789765635
Margin decision: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860418611
Margin correction: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860783553

## Per-item changes and reviewer responses

| Item | Change and file:line | How it answers the review |
|---|---|---|
| Required blocker | `docs/findings/COMMERCIAL_TIMING_395.md:117` | R372-2 F1 and R373-2 R2-F1: uses Ethernet-to-system wording while retaining unbounded false paths in both directions. The unchanged bare-metal check scans every tracked first-party file, including every new PR line, and returns zero findings. Its 700-arm self-test passes. |
| S1 | `docs/findings/COMMERCIAL_TIMING_395.md:119` | R372-2 S1: names shipping XDC 566's MultiReg exception and 568's AsyncResetSynchronizer exception. The table distinguishes 13/12 data D endpoints from 4/8 reset PRE endpoints, names FDPE_14/PRE and FDPE_18/PRE, and leaves the reset-assertion decision explicitly with #607. The fresh probe reproduces the review receipt byte for byte. |
| S2 | `sw/builder/test_timing_grade.py:190` | R372-2 S2 and R373-2 S-F: the standalone entry now invokes the PLL test alongside its platform test when supplied the platform interpreter. The real entry passes unchanged and fails at the changed-part assertion when the derived speed grade is replaced in memory by the old literal. |
| S3 | `sw/litex/milan_soc.py:207`; `docs/integration/BUILDING.md:33,49,72,540,626`; `docs/testing/RUNNING_TESTS.md:155`; `docs/litex/LITEX_SOC.md:161`; `docs/findings/COMMERCIAL_TIMING_395.md:65` | R372-2 S3 and R373-2 S-E: the PLL comment describes derivation from the declared part. The release wording consistently requires WNS >= +0.03 ns and WHS >= 0 at every corner, and states that enforcement is not automatic and sweep seed selection is manual. The margin correction is linked. |
| S4 | `docs/findings/COMMERCIAL_TIMING_395.md:143` | R372-2 S4: direct links locate the published crossing script and results under `fa9b0b5373abcb31b2ca6b20c3616b069d8672c4:review-evidence/395-r1/author-r2`. Both targets were verified through the repository API; metadata is in `public-evidence-locators.json`. |
| Retained S4 | `docs/findings/README.md:11` | R372-1 S4, retained in round 2: the current findings index now links the timing record and states its scope and remaining limits. |

The executable reporting chain, platform declaration and bare-metal gate remain
byte-identical to round 2. The SoC executable syntax tree is unchanged: its only
edit is the PLL comment. `unchanged-contracts.json` records these comparisons.
No firmware, RTL, constraint or timing fix is included.

## Gates at the committed head

All 21 accepted commands returned rc 0 at `{HEAD}`.
Every gate ran in the foreground with an explicit timeout and no pipeline.
`gate-results.json` records exact argv, cwd, head, UTC start, duration, exit code,
and each full log's size and SHA-256. `run_gates.py` retains the sequence.
The full logs are under `$VALIDATION_STORAGE/395-a393-work/gates-{HEAD[:9]}`;
small copies are included below. Concurrency is capped at sixteen CPUs;
the corner report uses sixteen threads and the crossing probe uses eight.

| Gate | Exit | Seconds | Receipt |
|---|---:|---:|---|
{table}

Compiler-present command:
`python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`.
Compiler-absent command: `python3 -B <packet>/run_builder_absent.py`.
That wrapper runs the full entry with `--require-elaboration`, hides exactly
the three RV32 compiler candidates, and asserts all three were probed.
Host compilers remain available. Both banks execute the timing-grade platform
and PLL arms and retain required elaboration.
`builder-present-summary.txt` and `builder-absent-summary.txt` list all skips.
Both record gate 11's unavailable historical Arty calibration report.
The absent mode additionally records its expected compiler-dependent skips.
These skips provide no validation of the omitted arms.

The bare-metal commands are
`python3 -B scripts/check_baremetal_only.py --check` and
`python3 -B scripts/check_baremetal_only.py --selftest`.
The unchanged check reports zero findings across 919 tracked first-party files.
The standalone PLL control returns 0; its deliberately wrong literal returns
1 at `test_pll_grade`, as required. The grading wrapper returns 0.

The first external mutation wrapper had a quoting error before loading the
mutated module. That non-acceptance attempt is retained separately in
`preliminary-gate-results.json` and `preliminary-standalone-pll.log`.
The corrected wrapper passed at the same repository head. Already successful
static checks were retained, and no repository change was needed for that repair.

## Fresh read-only timing evidence

The nominated shipping image remains `build_ax7101_eto_tdm8dev9e9954e9`.
The corner reporter returned 0 in 59.27 seconds; the endpoint-classification
probe returned 0 in 55.47 seconds. Exact commands and logs are in the gate table.

| Fixed model | Junction endpoints C | WNS ns | TNS ns | WHS ns | THS ns |
|---|---|---:|---:|---:|---:|
| Slow | 0 and 85 | 0.123 | 0.000 | 0.101 | 0.000 |
| Fast | 0 and 85 | 1.429 | 0.000 | 0.036 | 0.000 |

Every row meets WNS >= +0.03 ns and WHS >= 0 for the applied constraints.
The worst WNS surplus is 0.093 ns; minimum WHS is +0.036 ns.
These are two fixed timing models repeated at power metadata endpoints.
The fresh crossing receipt, `reports/crossings-r2-results.txt`, equals the
round-2 internal review's receipt byte for byte. All four directions meet the
diagnostic 8 ns bound at both models; minimum slack remains +2.560 ns.
Reset paths are included only after clearing the false paths in memory.
This diagnostic repairs no constraint and proves no CDC contract.

All seven shipping input size/hash pairs remain unchanged.
The checkpoint remains 115715651 bytes with SHA-256
`5f7a442b6a9327ad5d41aa0b10e18c84d9ca4c0aacd573d2ad25d444f5b2f5d1`.
See `shipping-inputs-before.json`, `shipping-inputs-after.json`,
`timing-metrics.json`, the five timing-summary excerpts and `report-artifacts.json`.
Reports over 200000 bytes remain under `$VALIDATION_STORAGE/395-a393-work/reports-{HEAD[:9]}`,
with sizes and SHA-256 recorded instead of copies. No checkpoint or bitstream
was written. All files in this packet are at most 200000 bytes.

## Remaining boundaries and handoff

The retained ten Critical CDC diagnostics, two unsafe clock pairs, and 46 input
and 87 output ports without delay constraints remain unwaived. #607 owns the
constraint repair and the reset-assertion policy decision. Margin enforcement
is still manual. Items 3 and 4 still need physical temperature and oscillator
measurements. No hardware or bench access occurred.

The worktree is clean. Only this assigned worktree and branch were used.
No push, PR edit, merge, additional checkout or independent review was performed.
The manager owns publication, hosted acceptance and candidate-merge validation;
the reviewers own the new verdicts and any clean-lens ledger.
`PR-BODY.md` contains the Round 3 update and retains its original first line.
`REVIEW-READY.md` is the public handoff text; its posted URL is recorded separately.
'''
(OUT / 'HANDOFF.md').write_text(handoff)
path = OUT / 'PR-BODY.md'
body = path.read_text()
start = body.index('Round-3 validation at ')
end = body.index('\nItems 3 and 4 remain open.', start)
body = body[:start] + f'''Round-3 validation at `{HEAD}`: the full builder bank in
both compiler modes with required elaboration, the bare-metal check and
self-test, CI scope self-test, documentation and idiom gates, and whitespace
checks all returned 0. The standalone PLL control passes and the restored
literal fails at the expected assertion. Fresh read-only checkpoint reports
reproduce every corner value and crossing endpoint class; all seven shipping
input hashes remain unchanged. Both banks retain the historical calibration
skip, and the absent mode records expected compiler-dependent skips.
''' + body[end:]
assert body.startswith('[A387] Relates to #395.') and '/home/' not in body
path.write_text(body)
print('Final handoff, local PR body and candidate identity written.')
