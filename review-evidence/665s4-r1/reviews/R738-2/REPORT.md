[R738] NEGATIVE - exact head ac45db8f18a5fde87c84be2225cc1be7d709eae9

External independent review R738-2, #665 / PR #812. Tree `158ec1f4835ba66973eb381f98904aa675d0855c`. Scope: three commits after `ee1c0be0b99f0131eb10908a19f080299aa0cbb8` and their dependencies against PR base `f4c9ad4f`. All five lenses applied. This independent verdict and ledger were saved before reading other reviewers' reports or PR comments.

The clock fields, conversions, labels and documentation requested by R738-F1 are implemented. One MINOR remains in the new refusal path: a refused rerun leaves an earlier successful table beside a new invalid record. This changes generated artifacts, not merely wording.

Authorities

- [Frozen S4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6493622258).
- [Owner option (c)](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6504551000): F1 steps meet T_svc; total capture CPU/elapsed time is recorded without a separate bound; current-writer D5 stays 24.5 ms.
- [Clock-provenance acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6511289316), FR_NFR 3.4.2 (record core clock), REQUIREMENTS section 1 and REQ-VER-04 (generated artifacts and documentation).
- `docs/ARCHITECTURE_HW_SW_SPLIT.md:140-175,217-225`; `sw/firmware/ctrl_nvm/README.md:276-367`; target harness `README.md:43-47` specifies refusal with exit 2 and no table.

Finding

**R738-F2 | MINOR | Conformance, Robustness, Tests, Docs | `tb/verilator/nvm_split_target/run.py:273-287`; `target_selftest.py:192-209`; target README:47 | Clock refusal leaves a stale success table beside a replaced invalid record.**

Authority/evidence: the public clock-provenance acceptance requires refusal of wrong provenance; the implemented output contract explicitly promises exit 2 and no `table.md`. `main` writes JSON before checking provenance and never invalidates an existing table. `probe_clocks.py` uses the same producer substitutions as the repository self-test, calling the actual `main` twice on the same output directory. The first call succeeds at CPU 62.5 MHz / bus 125 MHz. The second plants clocks different from its builds and returns 2, but the table remains byte-identical to the successful table while the replaced JSON claims CPU 50 MHz / bus 100 MHz. `clock-probes.log` records this. The built-in checks use a new temporary directory per call and miss repeated output use. A second probe uses the seven real fresh builds: deleting `cpu_hz` from the capture build causes the supported `--regrade` to return 2 while retaining its previous success table (`target-validation.log`). The disposable build record was restored byte-for-byte.

Impact: a supported reused output directory holds apparently successful evidence from another run beside a refused record. An exported table cannot identify that failure. Exit 2 is correct; the generated artifact pair is inconsistent. The new write-before-validation ordering introduces this mixed pair in the reviewed delta.

Required outcome: a refused run must leave no apparently current success table, and accepted JSON/table artifacts must represent one validated run. A diagnostic failed record is acceptable if clearly distinguished. Add a success-then-refusal test in the same output directory for missing/wrong build clocks and misconverted results, retaining the fresh-directory controls.

Verification: repeat the probe after correction; require exit 2 without a current success table and confirm accepted artifacts retain the actual build clocks. Run the target self-test/mutants, regenerate one point and retain unchanged step/D5 controls. This MINOR leaves every attributable lens unclean.

Prior finding disposition

**R738-F1: original omission resolved at its cause.** `run.py:92-105,137-232` retains both build clocks, checks conversion and renders three clock lines. Both published 50/100 MHz points and a synthetic 62.5/125 MHz input reproduce correctly. Architecture:223, store README:339-354, target README Results and the PR body label their figures. R738-F2 separately records the new repeated-output failure; the reporting/refusal area remains unclean overall.

Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: R738-F2 | Owner acceptance/option (c), FR_NFR 3.4.1/3.4.2, run.py:92-232,273-287, both timing records/tables | R738-2 applied | ac45db8f18a5fde87c84be2225cc1be7d709eae9 |
| RTL | CLEAN | Delta inventory, unchanged split_soc.py:449-486, sim_main.cpp, target configurations and generated-map/firmware paths | R738-2 delta; retained R738-1 baseline | ac45db8f18a5fde87c84be2225cc1be7d709eae9 |
| Robustness | UNCLEAN: R738-F2 | Clock validity/agreement/conversion checks, repeated-output probe, unchanged target boot/guard and step controls | R738-2 applied | ac45db8f18a5fde87c84be2225cc1be7d709eae9 |
| Tests | UNCLEAN: R738-F2 | target_selftest.py:145-280,420-588; self-test/mutants; independent conversion and D5 probes | R738-2 applied | ac45db8f18a5fde87c84be2225cc1be7d709eae9 |
| Docs | UNCLEAN: R738-F2 | All three Markdown deltas, PR body, public scope, receipt manifest and exact-head author gate summaries | R738-2 applied | ac45db8f18a5fde87c84be2225cc1be7d709eae9 |

[R738] PASS RTL - `git diff ee1c0be0..ac45db8f` and `tb/verilator/ctrl_service_budget/split_soc.py:449-486`: no HDL, firmware, shared simulator, target cases/grader, D5 gate or gitlink changes. CPU/bus assumptions remain 50/100 MHz. Build clocks derive from shape constraints; the new common-clock check requires agreement before grading. The clean R738-1 baseline remains applicable, with the delta clock dependency independently checked here.

Robustness checks cover absent, zero, nonintegral and mismatched clocks, empty build sets, wrong conversions and repeated output. No new source-comment lane/reviewer residue was found. No additional suggestion or prose-only residue is filed.

Execution evidence

- `target-selftest.log`: 61 checks, zero failures: 41 ordinary checks and 20 mutants, including eight new clock mutants. Exactly T_svc passes, one cycle over fails in all seven phases. D5 boundary/removal controls pass unchanged.
- `clock-probes.log`: both immutable published tables reproduce byte-for-byte; independent cycle/ms arithmetic agrees with 50 MHz; three clock lines per report. Missing/relabelled clocks are refused. Synthetic 62.5/125 MHz rendering follows its input. Repeated-output defect reproduced.
- `d5-probes.log`: unchanged current-writer gate passes. Deleting only its 24.5 ms comparison in a disposable imported copy causes exit 1: `OFF timing limit was ignored`.
- `public-verification.log`: 182 current-round author receipts match the published SHA256 manifest at `707462eaa175afedaeb6acd2e3fded6073e0d51d`. All 97 short and 11 long gate commands record the exact head and success. Store, co-simulation, campaign and coverage receipts spot-checked. These are author source executions, not manager banks or reviewer bank reruns.
- `target-validation.log`, `build-clock-receipt.json`, and `target-1x1/`: fresh complete 1x1 target run, exit 0, all cases pass and controls are caught. Its complete result record equals the published record, including all cycle counts. All seven build records agree on CPU 50,000,000 Hz and bus 100,000,000 Hz. Capture: 1,361,143 cycles / 27.223 ms CPU time, 534.905 ms elapsed. Real slow step: 30.2216 ms, rejected against 10 ms; all seven per-phase step controls pass unchanged. Raw scripts, logs and journals are included. The real missing-clock regrade returns 2 but retains the old table, confirming R738-F2 independently of synthetic producers.
- `checkout-integrity.log`: exact head/tree, raw tracked blob bytes and executable modes, complete stage-0 index and all five populated submodule pins/contents match. The external gitlink remains unchanged and unpopulated. No tracked restoration was needed.

Portable reproduction scripts are included: `verify_public.py`, `probe_clocks.py`, `probe_d5.py`, `run_target.py`, `collect_target.py`, and `verify_checkout.py`. Run from the reviewed checkout; the target wrapper accepts the existing dependency locations as arguments. The focused target driver used `--jobs 16`, native builds used `-j16`, and all commands remained foreground processes. The simulation compiler identity was verified before use (`compiler-identity.log`). Full parent/processor/gPTP/synthesis/builder banks were not rerun. The 8x8 evidence was re-rendered and checked, not freshly built this round.

Limits and pending manager duties

The [immutable public evidence](https://github.com/kebag-logic/milan-fpga/tree/707462eaa175afedaeb6acd2e3fded6073e0d51d/review-evidence/665s4-r1) commit reports signature status `N` (unsigned). Published hashes were verified; signer authentication is not claimed. Some large public logs/journals are represented only by hashes. Physical calibration is NOT RUN; field skips and simulated media waits are not hardware proof.

T_svc remains the 10 ms proposal at this base. Approved 20 ms belongs to S2b and is not a finding here. F1 has no total capture bound. D5 remains on the current writer.

There is no manager source bank at this head. Hosted/local workflow acceptance belongs to the manager; no executed job is inferred from skipped contexts. The manager must build the final current-dev candidate and publish builder/native receipts at merge time. Source base `f4c9ad4f`; supplied live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`. Neither that candidate nor S2b integration was validated here. Re-review R738-F2, obtain independent positive reviews, finish candidate/workflow acceptance, then follow explicit merge authorization and post-merge containment. Issue #665 is broader than S4.

No source fixes, commits, pushes, GitHub writes, hardware runs, shared installs or other-checkout edits. Disposable trees stay under packet `scratch/`, which is excluded from publication. `MANIFEST.sha256` lists every publishable receipt using packet-relative paths. Public prior-finding reconciliation (performed after the independent verdict and ledger were saved): PR #812 has five public comments, no submitted reviews and no review-thread comments. All findings on the two published round-1 reports were reconciled:

| Prior ID | Disposition at this head |
|---|---|
| R738-F1 | Original omitted clocks resolved, as detailed above; new failure-path defect R738-F2 remains |
| R737-1-R1 (RESIDUE, Docs) | Resolved: architecture line 223 now names CPU 50 MHz and bus 100 MHz |
| R737-1-S1 (SUGGESTION, Tests/Docs) | Resolved: results keep CPU/bus clocks and every generated table labels them |
| R737-1-S2 (SUGGESTION, Tests/Robustness) | Retained optional: committed negative controls for map placement and map-clock refusal remain absent; those files and their self-tests are untouched by this delta |
| R737-1-S3 (SUGGESTION, Robustness) | Retained optional: zero-size flash-region modulo still raises an unnamed refusal at gen_flash_port.py:246; unchanged and outside the delta |
| R737-1-S4 (SUGGESTION, Tests) | Retained optional: portable target/map self-tests remain outside hosted workflows; workflow files are unchanged |

Retained suggestions do not affect cleanliness; R738-F2 does. No other earlier findings were found. No manager source execution receipt was supplied or inferred.

R738-2 FINISHED
