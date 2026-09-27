"""Finalize the review packet after all assigned committed-head gates pass."""
from pathlib import Path
import json
import subprocess

ROOT=Path('$LANES/395-timing-grade')
OUT=Path('$MANAGEMENT/2026-09-23/395-a390')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
gates=json.loads((OUT/'gate-results.json').read_text())
assert len(gates)==19 and all(r['head']==head and r['returncode']==0 for r in gates)
assert not subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()
rows=['| Gate | Exit | Seconds | Evidence |','|---|---:|---:|---|']
for row in gates:
    rows.append(f"| `{row['gate']}` | {row['returncode']} | {row['seconds']} | `gates/{Path(row['log']).name}` |")
section=f"""## Gates at committed head

All nineteen commands returned rc 0 at `{head}`.
Each command ran in the foreground with an explicit timeout and no pipeline.
`gate-results.json` records full argv, cwd, head, times, exit codes, log sizes
and SHA-256 hashes; `run_gates.py` preserves the sequence.

"""+'\n'.join(rows)+"""

Compiler-present command:
`python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`.
Compiler-absent command: `python3 -B run_builder_absent.py`. That retained
wrapper runs the full entry point with `--require-elaboration`, hides exactly
three RV32 compiler candidates, and asserts all three were probed. Host
compilers stay available. Both modes executed the timing-grade platform and
PLL arms; neither skipped required elaboration.

Both modes record gate 11's unavailable historical Arty calibration report.
The absent mode also records expected compiler-dependent stand-downs.
Those skips are limits, not coverage; see `builder-*-summary.txt`.

## Limits and retained evidence"""
p=OUT/'HANDOFF.md'
s=p.read_text()
a=s.index('## Gates at committed head')
b=s.index('## Limits and retained evidence',a)+len('## Limits and retained evidence')
s=s[:a]+section+s[b:]
s=s.replace('Status: committed; assigned gates running in the foreground.',
            'Status: implementation and assigned validation complete; ready for independent review.')
s=s.replace('Gate receipts update incrementally\nin `gate-results.json`; final evidence inventory and public handoff pending.',
            'All final-head gate receipts are in `gate-results.json`.\nSeven shipping input size/hash pairs remain unchanged. Report sizes and hashes\nare in `report-artifacts.json`; larger reports remain under the physical data\npath. All retained packet files are at most 200000 bytes.\n`MANIFEST.sha256` inventories this packet. The worktree is clean.\nPublic review-ready notice: prepared for posting after final packet checks.')
p.write_text(s)
p=OUT/'PR-BODY.md'
s=p.read_text()
old=f'Round-2 validation at `{head}`: pending.'
new=f"""Round-2 validation at `{head}`: the full builder bank
in both compiler modes with required elaboration, CI scope self-test,
documentation gates and whitespace checks all returned 0. Fresh checkpoint
reports reproduce the corner metrics. All five required faults fail through
the full builder entry point; the broader 21-fault campaign has no unexpected
outcomes, and the unmodified control passes. The PLL literal control also
fails as intended. Both builder modes retain the historical calibration skip;
the absent mode records its expected compiler-dependent stand-downs.

Clearing all false paths exposes fourteen milan-to-Ethernet endpoints,
including reset paths. Their worst Slow/Fast slack is +4.056/+5.878 ns.
The review's six-endpoint measurement retained generic false paths and gave
+7.066/+7.538 ns. The record distinguishes both path populations."""
assert old in s
s=s.replace(old,new)
assert s.splitlines()[0]=='[A387] Relates to #395.'
assert '/home/' not in s
p.write_text(s)
by_name={r['gate']:r for r in gates}
ready=f"""[A390] REVIEW READY
Commit: `{head}`
Branch: `395-timing-grade`, base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.

Changed: round-2 responses to R372-1 F1/F2/F3 and R373-1 F1/S2. The timing record names rejected crossing constraints, warning/source/log locations, the clock-prefix cause, unbounded Ethernet/sys false paths, measured intended-bound slack and #607. BUILDING retains the critical-warning census. The builder exercises hook-level refusals and report arguments; the PLL speed grade derives from the declared part.

Validation at this head, all rc 0:
- Full builder bank: `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration` ({by_name['builder-present']['seconds']} s).
- Full builder bank with exactly the three RV32 compiler candidates hidden and required elaboration retained ({by_name['builder-absent']['seconds']} s).
- `python3 -B scripts/ci_scope.py --selftest`.
- `python3 -B scripts/docs_check.py`, `python3 -B scripts/check_doc_paths.py`, contents, punctuation, feature-status, documentation-style and solution-documentation gates; Python idiom gate/self-test; committed and worktree `git diff --check`.
- Foreground checkpoint reports ({by_name['timing']['seconds']} s, 16 threads) and crossing diagnostic ({by_name['crossings']['seconds']} s, 8 threads). All seven shipping input size/hash pairs remain unchanged.
- All five required faults fail with timing-grade assertions through the full builder entry point. The reviewer's 21-fault campaign returns `unexpected=0`; its unmodified control passes. All four hook refusal probes return 1. Restoring the PLL literal fails its changed-part control.

The recorded margin is WNS >= +0.03 ns and WHS >= 0 at every corner. Slow WNS/WHS is +0.123/+0.101 ns; Fast is +1.429/+0.036 ns. Both repeat at 0 and 85 C; TNS/THS are zero. The intended 8 ns crossing bound is met in all four directions at both models, with worst slack +2.560 ns. Clearing all false paths exposes fourteen milan-to-Ethernet endpoints, including reset paths: Slow/Fast worst slack +4.056/+5.878 ns. The review's narrower six-endpoint measurement was +7.066/+7.538 ns; the record distinguishes both.

The shipping log has 14 emitted critical warnings; its fifteenth substring match is echoed source, not another warning. #607 owns the constraint fix. No timing or constraint fix is included. CDC diagnostics and missing I/O delays remain unwaived. Both builder modes record the unavailable historical Arty calibration; the absent mode additionally records expected compiler-dependent stand-downs. No timing-grade or required-elaboration arm was skipped.

Acceptance: items 1, 2 and 5 and the assigned round-2 responses are delivered for independent review. Items 3 and 4 remain open. Relates to #395.

HANDOFF.md and PR-BODY.md are updated in the assigned packet, with per-item file/line responses, crossing and planted-fault tables, exact gate receipts and evidence hashes. Worktree clean. No push, PR edit, merge, hardware access or firmware/RTL edit occurred. Independent reviewers remain [R372] and [R373].
"""
(OUT/'REVIEW-READY.md').write_text(ready)
print('Final handoff, Round 2 PR body and review-ready notice prepared at',head)
