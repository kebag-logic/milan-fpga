[R948] NEGATIVE - exact head 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4

Round R948-1, external independent review of PR #1019, relating to issue #1008.
Tree: `d0508027199923e8d3464eb9d55ef185af10b6f5`.
Source base: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`.

All five lenses were applied independently. Two MINOR findings remain. Neither is a functional failure of the scheduling code. The quantitative policy inconsistency and incomplete retained execution evidence prevent a clean ledger. There are no RESIDUE findings: the first finding changes figures, and the second concerns executable evidence.

## Authorities and reconstruction

Read AGENTS.md, CONTRIBUTING.md, docs/README.md, the frozen [issue](https://github.com/kebag-logic/milan-fpga/issues/1008) and its two scope comments, REQUIREMENTS.md (particularly REQ-VER-01 through REQ-VER-04), and the CI policy and gate/receipt interfaces. The corrected [timing decision](https://github.com/kebag-logic/milan-fpga/pull/1003#issuecomment-7164094739) requires re-keying from two complete hosted runs and restoring the regular-worker bound.

Independently reviewed all fourteen changed files and the eight commits before reading the public evidence and PR discussion. The [published packet](https://github.com/kebag-logic/milan-fpga/tree/6be24f180ccc2c0ddda4b5d3ffa40ba09d7885e3/review-evidence/cicd4-r1/author) supplied the execution records. Verified the published SHA-256 values of all 232 extracted evidence files. No private author material or other reviewer's report was read. The PR discussion fetched after the independent diff pass contained only two review-start notices; there were no prior public findings or verdicts to resolve or retain.

## Findings

### R948-1-D1 | MINOR | Docs

**Artifact:** `docs/testing/CI_WORKFLOWS.md:3450` and `docs/testing/CI_WORKFLOWS.md:3503`.

**Authority/evidence:** REQ-VER-04 and AGENTS.md's Documentation lens require the changed scheduling contract to be reflected accurately. The updated table gives `docs-gates-0` 738 seconds and `docs-gates-1` 1302 seconds. The following present-tense paragraph still identifies worker 0 as the slowest at 1395 seconds and derives 1665 seconds, 27.8 minutes and 135 seconds of margin. These describe the superseded schedule, not the table immediately above. See `schedule-audit.log`.

**Impact:** The authoritative policy gives contradictory bottleneck and total-duration figures for this change. This is a quantitative claim, so it is not wording-only residue.

**Required outcome:** Reconcile the explanatory paragraph and its arithmetic with the final table. If retaining its stated 270-second downstream allowance, the table's maximum is worker 1 at 1302 seconds, giving 1572 seconds, 26.2 minutes and 228 seconds of margin. Keep the separate fact that worker 1 exceeds the 1276-second slow-runner target explicit; do not present the workflow calculation as satisfying that per-job target.

**Verification:** Recompute the maximum from the final rows, then its downstream total and margin; confirm the prose names the same worker and values. Re-run the relevant documentation gates at the corrected head.

### R948-1-T1 | MINOR | Conformance, Tests, Docs

**Artifact:** Published `author/receipts/local/census/`, `author/receipts/tools/plant_census.py:6`, and `sw/mailbox/census_legs.py:134`.

**Authority/evidence:** Issue #1008 acceptance 2 requires preserved verdicts and receipts. AGENTS.md requires publicly reconstructible execution evidence. The published packet includes leg logs, a union log and the seven-fault transcript, but no `census-leg-*.json` files. The published fault script loads precisely those files, and the production union consumes their source, selection, exit status and per-arm `ok`/`through` values. `evidence-identity.log` records zero such receipts in the packet after verifying its published manifest. The prose transcript cannot reconstruct all these typed values.

**Impact:** A cold reviewer can verify the printed serial/leg verdicts, but cannot replay the claimed successful union or the seven fault probes against the actual execution receipts. The independently passing synthetic probes validate the checker; they do not supply the missing original execution records.

**Required outcome:** Publish the five original JSON receipts with hashes and their source identity, together with the exact successful union and fault-probe commands. Preserve the recorded execution head; the census execution was at `530149b5dd1a94cc5011b17c9bb28af54bc79be3`, not the review head. If the records are unavailable, regenerate and retain them at an identified clean committed head. Do not manufacture receipts from the printed summaries or relabel their head.

**Verification:** At the recorded source identity, replay the original receipt set successfully and replay the seven documented corruptions with nonzero outcomes. Verify receipt identities, exact inventory/selection coverage and correspondence with the retained leg/union logs. This finding can be addressed by public evidence; it does not prescribe a source change.

## Results by lens

**Conformance:** Reviewed the frozen acceptance criteria against the generated graph, campaign dispatch, census union and timing evidence. The eight implementation commits preserve the tested verdict populations. All seven required context carriers remain: `rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites`, `yosys-portability`. No existing job timeout increased. Acceptance 2 remains partly unverified because of R948-1-T1. Acceptance 1 is not complete: the packet contains projections, not two completed hosted observations of this schedule, and the PR expressly leaves several jobs outside its partial scope. That is not a completion of #1008.

[R948] PASS RTL - `reviewed-delta.txt`; `sw/firmware/ctrl/test/test_ctrl_firmware.py:236`; `scripts/ci_gate_workflows.py:406` - no production RTL, firmware implementation, clock/reset, CDC, interface or gitlink change. Reviewed the architectural effect on validation: SRP retains all three table populations and restores the complete table in `finally`; census shape comparisons remain whole on leg 0, riders remain with their original hosts, and the serial rule-removal judge is unchanged. Both census and elaboration restore the same exact Yosys key/path with miss refusal and a dependency on the producer. This is scoped architecture review, not a fresh hardware qualification.

[R948] PASS Robustness - `sw/mailbox/census_legs.py:74`; `scripts/ci_fast_legs_selftest.py:105`; `probe-receipts.log`; `cancel-controls.log`; `runtime-controls.log` - rejected 851 independently planted synthetic receipt faults over 164 arms, covering missing/duplicate legs, wrong source, invalid scalar types, each missing/failed arm and each applicable failed rule removal. Every SRP subcampaign failure propagates while later subcampaigns execute; an exception restores the table. Existing controls execute the required-context shell with failing/cancelled matrix results, including a skipped census judge. Cancellation/fork controls pass. Triggers, concurrency, selectors and permission grants remain unchanged; no new privileged job appears.

**Tests:** Reviewed both new self-test files, modified generator/contract controls, real campaign dispatch and the published execution logs. Independent multiset comparison matches 844 control verdicts and 398 AECP verdicts. SRP matches 662 defect verdicts plus its two original dependency-pin controls; each new leg repeats those controls as intended. Census leg 0 matches 22 serial check lines after duration normalization. The union matches 222 arm/rule lines in order after normalization of one heap address; it reports zero failures among 164 arms and 57 rules. The serial reference's `sw/`, `hdl/`, `configs/` and all submodule inputs equal the base's. Campaign/census source files are unchanged from the later execution snapshot to this head. Full source banks were not rerun. R948-1-T1 leaves this lens unclean.

**Docs:** Reviewed the complete changed policy text and generated workflow changes against the public PR claims, issue and evidence. The policy explains the new matrices, census judge and shared restore. Newly introduced source comments contain no forbidden bench labels, lane names, review-round identities or issue-comment identifiers. R948-1-D1 and R948-1-T1 remain open. No privacy finding was observed.

## Timing, cost and acceptance boundaries

Re-ran the published projection and runner-minute calculations over their retained measurements. These reproduce estimates, not new hosted measurements:

| Split job | Largest projected leg, seconds | At 1.41x, rounded seconds |
|---|---:|---:|
| Control mutation campaign | 739 | 1042 |
| AECP mutation campaign | 892 | 1257 |
| SRP mutation campaign | 1017 | 1434 |
| Publication census workers | 498 | 703 |
| Firmware unit leg 0 | 1027 | 1448 |
| Firmware unit leg 1 | 503 | 709 |
| Firmware unit leg 2 | 811 | 1144 |

Docs' changed table projects workers 0/2/3/4 at 738/981/1237/879 seconds. Worker 1 remains 1302 seconds and is expressly unfinished work. The campaign projections allocate the old hosted step window using the concurrently measured local leg shares; census removes the old in-job Yosys build. Those assumptions still need the required hosted observations.

The two published raw worker logs re-derive `gptp_shadow=517` seconds, the maximum of 478 and 517. The live inventory and deal reproduce all 27 policy rows: the largest regular worker is 1275 seconds, below 1276. The dedicated continuous-history worker remains the separately documented 1530-second exception. The after-cost arithmetic reproduces rtl-fast 263.9 to approximately 269.2 runner-minutes, and docs 91.2 to approximately 94.5. These estimates retain baseline watcher costs and estimated repeated setup/judge costs; they are not measured after-change consumption.

The PR explicitly leaves cache-miss work, the single builder bottleneck and other named long jobs for follow-up, including `firmware-verilator`, elaborate workers and `docs-gates-1`. The issue's two-run timing criterion therefore remains open. Neither the PR body nor this review silently changes the frozen acceptance criteria.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #1008 body/comments; required context graph; timing receipts; census source/receipt union; R948-1-T1; hosted acceptance still pending | R948-1 applied, not banked | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |
| RTL | CLEAN | Fourteen-file diff; unchanged production RTL/firmware/gitlinks; campaign dispatcher; census grouping; shared restore | R948-1 | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |
| Robustness | CLEAN | Census union and 851 fault probes; SRP failure/exception probes; generated aggregate shell; cancellation and runtime controls | R948-1 | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |
| Tests | UNCLEAN | Generator/contract/dispatch controls; raw serial and leg logs; public manifest; missing original census receipts, R948-1-T1 | R948-1 applied, not banked | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |
| Docs | UNCLEAN | CI policy table/prose; PR/issue and public receipt index; R948-1-D1 and R948-1-T1 | R948-1 applied, not banked | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |

## Execution and limits

All eight focused command groups passed (each rc=0): generator byte check, generator controls, event contract check, complete event mutation self-test, suite-shard controls, firmware dispatch controls, runtime evidence controls and cancellation controls. `checks.json` records commands and elapsed times. The complete event self-test passed 2390 contract items and 6161 mutation arms in 503.206 seconds. The separate independent probes passed 851 census fault cases, all SRP table-failure/exception cases, exact workflow rendering and shared-restore checks. The published evidence identity, timing re-key and arithmetic checks also passed; their limits are stated above.

`reproduce.sh`, `run_checks.py`, `inspect_evidence.py`, `probe_receipts.py`, `audit_schedule.py` and `verify_tree.py` provide portable reproduction from an isolated clone. All four workflow files equal the generator's rendered bytes. The packet's raw receipts and scripts are listed in `MANIFEST.sha256`; extracted public material and disposable files under `scratch/` are not publishable packet contents.

No full parent, processor, gPTP, synthesis or builder bank was run. No host local-replica orchestrator, its self-test, container, privileged operation, shared installation or hardware was used. No source fix, commit, push, GitHub write, author contact, sub-agent or other checkout edit occurred. The focused checks produced two temporary dispatch configuration files; these were moved into this packet's scratch directory and the clone was verified clean. Direct final verification checks every tracked blob and executable mode, each index entry, and all five initialized dependency gitlinks and their tracked contents. The intentionally uninitialized external dependency's gitlink is retained. See `tree-integrity.json`.

There is no manager source-bank result at this exact head. The author's published gate receipts are the source execution evidence. The one hosted-state read observed docs/elaborate in progress and rtl-fast/rtl-full queued; it did not establish successful executed required contexts. No skipped context is claimed as an executed gate. Hosted/local-replica acceptance, two timing observations, the final merge-candidate builder/native banks, exact candidate identity, hosted evidence reconciliation and post-merge containment remain manager duties. The stated live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`; the manager must use the then-current dev at merge time. This source review does not validate that future merge result or authorize a merge.

Physical calibration is NOT RUN. Field skips and desk evidence provide no hardware proof.

R948-1 FINISHED
