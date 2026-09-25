from pathlib import Path
import json,subprocess
root=Path.cwd();out=Path(__file__).parent
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
receipt=json.loads((root/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
lookup={(a['shape'],a['cpu_hz'],a['traffic']):a for a in receipt['measurements']}
large='endstation_ax7101_8x8';small='endstation_ax7101_1x1_tdm8'
w8=max(lookup[large,50000000,a]['maximum_ms'] for a in ('on','off'))
w1=max(lookup[small,50000000,a]['maximum_ms'] for a in ('on','off'))
w100=max(lookup[large,100000000,a]['maximum_ms'] for a in ('on','off'))
assert w8<=24.5
measure=[]
for a in receipt['measurements']:
 ticks=[r['sys_cycles'] for r in a['rows']]
 measure.append(f"| {'8x8' if a['shape']==large else '1x1'} | {a['cpu_hz']//1000000} / 100 MHz | {a['traffic'].upper()} | {a['captures']} | {min(ticks):,} to {max(ticks):,} | {a['maximum_ms']:.5f} | {a['margin']:.4f}x |")
checks={r['name']:r for r in json.loads((out/'gate-results.json').read_text())}
assert all(r['returncode']==0 for r in checks.values()),checks
checkrows=[]
for name,row in checks.items():
 argv=row['argv']
 command=' '.join(argv)
 checkrows.append(f"| {name} | `{command}` | 0 | `{name}.log` |")
changes=[]
markers={
 '.github/workflows/docs.yml':'      - name: Capture measurement census',
 'scripts/check_nvm_capture.py':'def current_inputs',
 'tb/verilator/nvm_capture_cpu/recipe.py':'CPU_HZ =',
 'tb/verilator/nvm_capture_cpu/run.py':'def grade_rows',
 'tb/verilator/nvm_capture_cpu/soc.py':"    clocks = dict(config['constraints'])",
 'tb/verilator/nvm_capture_cpu/sim_main.cpp':'    // Match the board PLL',
 'tb/verilator/nvm_capture_cpu/measurements.json':'  "measured_for"',
 'tb/verilator/nvm_capture_cpu/README.md':'# Product CPU',
 'docs/testing/TESTING.md':'The directory inventory includes',
 'tb/verilator/README.md':'The [`nvm_capture_cpu`]',
 'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md':'Timing. MEASURED',
}
for path,marker in markers.items():
 line=next(i for i,l in enumerate((root/path).read_text().splitlines(),1) if l.startswith(marker))
 changes.append(f'- `{path}:{line}`')
text=f"""# [A309] Round 2 handoff

Status: implemented and locally validated; ready for independent review.
Branch: `559-capture-copy`.
Initial head: `32076148acb0b9122e8c92a44f8e2ebbc8169280`.
Final local head: `{head}`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112.

## Stop condition and remedy

The maximum over all 32 aligned 50 MHz 8x8 captures is **{w8:.5f} ms**.
It is below 24.5 ms by {24.5-w8:.5f} ms ({100*(24.5-w8)/24.5:.3f}% of the limit).
The STOP condition did not trigger. The nominal hold remains 50 ms; its free-running millisecond tick guarantees a 49 ms floor. The floor-based margin is **{49/w8:.4f}x**. This remedy is conditional on the measured copy and clock remaining unchanged.

No product firmware, product RTL, configuration YAML, donor or builder census list changed. No push, PR edit, merge, hardware access or delegated work was performed. Hosted checks and independent re-review remain with the manager.

## Measurements

Every row below uses aligned CPU/system rising edges and 16 captures. Both 100 MHz arms are labelled non-contract comparisons. The published maximum includes every arm, not only traffic ON.

| Shape | CPU / system | Traffic | Captures | System cycles, min to max | Maximum ms | 49 ms / maximum |
|---|---|---|---|---|---|---|
{chr(10).join(measure)}

Census: 8x8 = 12,634 closed-record bytes / 156 records; 1x1 = 3,218 / 53. Every ordinary capture attested with zero open ownership and zero destination mismatches. ON counts accepted requests, successful responses and shared descriptor-memory reads; OFF has zero in all three counters. Logs and per-arm JSON receipts are adjacent to this handoff; the committed receipt contains all 96 rows, commands, clocks and hashes.

The offered load produces small measured increases at the contract clock, rather than literally zero effect. Section 18 reports the exact ON/OFF differences; it does not assert the unsupported phrase “does not measurably lengthen”. At 100 MHz the OFF arm is slower. Both arms are therefore graded and included in every published maximum. This wording is an evidence-driven correction to the assignment's proposed characterization, not a change to its acceptance limit.

## Reviewer reproduction

The public evidence branch was fetched read-only into temporary scratch at `39ac477dd8f92b16ccb0e3ab1248a50020d48fd9`; that fetch and its extracted files were deleted after use.

| Reviewer probe | Captures compared | Published maximum ms | Reproduced maximum ms | Result |
|---|---|---|---|---|
| R325-1, original-phase 50 MHz ON | 4 | 24.15248 | 24.15248 | every row field identical |
| R325-1, original-phase 50 MHz OFF | 2 | 24.15108 | 24.15108 | every row field identical |
| R324-1, original-phase 50 MHz ON | 2 | 24.15248 | 24.15248 | every row field identical |
| R324-1, original-phase 50 MHz OFF | 2 | 24.15108 | 24.15108 | every row field identical |
| R324-1, aligned 50 MHz ON | 2 | 24.29902 | 24.29902 | every row field identical |

`reviewer-comparison.json` records each compared row; `reviewer-probe-hashes.json` identifies the public scripts and patches. The R325 shell pipeline was adapted to call its unchanged build/compiler/grader functions with an in-memory clock override. The actual R324 `probe_step.py` was executed through a small adapter with that override and its published C++ phase patch. These setup adaptations avoid forbidden checkout copies and YAML edits. R324's aligned reproduction used its scoped simulator version 5.050; the other probes and the final matrix used 5.052. The CPU netlist and instrumented firmware hashes match the public receipts. See `reviewer-probe-adapter.py`, `r324-probe-adapter.py` and reproduction logs.

## Gate design and controls

`python3 scripts/check_nvm_capture.py` runs in the hosted documentation job. It requires ordinary Python gate dependencies and initialized source dependencies, but no RV32 compiler, LiteX import or simulation.

It regenerates both shapes' tables, derives their framed closed-record byte totals and record counts, and compares them with `measurements.json`'s `measured_for` entries. The explicit contract CPU clock comes from `recipe.py`; the gate separately pins each YAML CPU clock and the system clock. Thus the temporary 50 MHz override cannot hide configuration changes while #565 remains open. Any difference, including shrinkage or speedup, refuses the old measurement. Product firmware and harness source hashes also bind the evidence to its inputs.

The gate regrades every recorded row, checks both arms at all three shape/clock points, and recomputes the published maxima. Timing uses integer system ticks against half the 49 ms floor.

Named input controls: `bytes`, `records`, `clock`, `configured-clock`, `system-clock`. Each changes one live derived value and must fail the real comparison. A slower OFF fixture must set the maximum; a planted grader excluding OFF must fail it. Exactly 24.5 ms passes and one additional system tick fails, including OFF. All controls run before each ordinary verdict. The explicit `--mutation bytes`, `records`, `clock` and `ignore-off-timing` invocations each exit 1 for the intended reason; `capture-control-results.json` records the checks.

The live simulation controls also returned 0: skipped stores left every byte poisoned and were caught; disabled traffic left a correct copy with zero counters and passed the same timing check. Their native exits are 1 and 0 respectively, as required by the control oracles.

## Changes

{chr(10).join(changes)}

The harness adds the clock override, aligned edges and normal ON/OFF timing arms. The new hosted gate binds census and clocks to the measurements. Documentation identifies every substituted model, the manual measurement's Makefile exception, the actual writer clock, the 49 ms floor and #565.

## Gate table

Commands ran in the foreground, without pipelines, with generous timeouts. Simulation build trees and test temporary directories live under `$VALIDATION_STORAGE/559-a309-*`; output holds only documents, scripts and receipts. The SDK was read-only. The Markdown gates used the existing locked renderer packages read-only.

| Gate | Command | rc | Receipt |
|---|---|---|---|
{chr(10).join(checkrows)}

The SDK wrapper is the prescribed manager wrapper with only its audit-file destination changed. It executes the full `sw/builder/test_builder.py --require-rv32`, mapping only the selected compiler argv[0] to the pinned SDK compiler. `builder-sdk-argv.jsonl` records actual invocations. The absent wrapper executes the full default builder after hiding only its three cross-compiler candidates; real host compiler probes remain visible. `builder-absent-argv.jsonl` records the intentional absences.

Both builder modes report the missing historical placement-calibration report as NOT RUN. The compiler-absent mode also intentionally reports its compiled census and dependent controls as NOT RUN. The SDK mode executes those compiler-dependent arms. These skips are not executed passes.

`nvm_cosim` reports 465 PASS, 0 FAIL and 39/39 named mutants killed. `nvm_backend` passes both shapes and all four controls. `nvm_hosttest` passes all five shapes and its controls. The parser gate executes and matches its existing four pinned-source findings; it is not a skipped invocation. OOC is inapplicable because no RTL source changed.

Intermediate checks found a missing docstring and needed Contents navigation; both were corrected without weakening budgets. The input gate correctly refused the old receipt during preflight, then passed with the new measurements. The final table records successful runs; expected failing controls are recorded separately.

## Review and remaining limits

This handoff is author evidence, not a review verdict. Both reviewers must re-review the new head. Exact-head hosted acceptance, the candidate merge and merge authorization remain with the manager. No physical DDR calibration, silicon timing, debounce or physical memory-ordering claim is made. The relative phases are deterministic and aligned, not swept.

`PR-BODY.md` contains the full original PR body structure updated for this head, with a Round 2 section and `Closes #559`. The issue receives the authorized `[A309] REVIEW READY` comment with this head; no PR edit is made.
"""
(out/'HANDOFF.md').write_text(text)
body=f"""[A309]

Closes #559

Status: ready for independent review of round 2.

Description: measure the complete saved-state capture on the product CPU and memory buses. Across both traffic arms, with 16 captures each at the contract's aligned 50 MHz clock, the worst 8x8 result is {w8:.5f} ms. This gives {49/w8:.4f}x margin against the guaranteed 49 ms floor of the unchanged nominal 50 ms hold. The 1x1 maximum is {w1:.5f} ms. The hold remains sufficient only while the measured copy and clocks remain unchanged.

How to reproduce: use the full measurement matrix linked from [snapshot ownership section 18](docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md#18-cost). The linked receipt contains all 96 captures, input hashes and the labelled 100 MHz comparison. Every capture checks the complete closed-record copy, attestation, ownership and its traffic condition.

How to validate: all requested local gate commands returned zero, including both builder modes, the backend and firmware suites, both documentation inventory modes and the new capture-input gate. Named changes to bytes, records, clocks and OFF timing are detected. The compiler-absent run intentionally skips its compiled census; both builder modes lack the historical placement-calibration report.

DoD: the runnable harness, conditional hold remedy, section 18 and UNRESOLVED 6 are updated. Physical timing and memory ordering remain open. Independent re-review and exact-head hosted acceptance remain to be completed.

## Round 2

- Both shapes use explicit 50 MHz clock overrides and aligned rising edges. Configuration reconciliation remains in #565.
- Traffic ON and OFF each receive 16 captures and identical timing grading. The 8x8 100 MHz maximum is {w100:.5f} ms, labelled non-contract. Section 18 quantifies the small observed traffic effects.
- The hosted input gate regenerates closed-record bytes and records, checks clocks and source identity, and refuses stale measurements. A planted grader that ignores OFF timing fails its control.
- Test indexes name the manual measurement, its prerequisites and Makefile exception. The harness instructions identify all substituted devices and clock phases.
- Both reviewers' 50 MHz probe figures were reproduced cycle-for-cycle. The stop condition was not triggered; product firmware and hold settings remain unchanged.
"""
assert 'Closes #559' in body and body.startswith('[A309]') and '/home/' not in body
(out/'PR-BODY.md').write_text(body)
print('Final artifacts written for',head)
