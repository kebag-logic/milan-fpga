[R886] NEGATIVE - exact head e816c74da53a5822f2ddc1661e5ffae297f1b3aa

Round R886-2, external independent delta review of issue #969 / PR #971. All five lenses were applied. The prior firmware defects, campaign omission and memory-document findings are resolved. One new MINOR in the standalone measurement grader remains open; two wording items are RESIDUE.

Examined tree: `e2b9b5f88b2c9ffb5aff42996c34150c2afda190`. The full scope is `dd163e41..e816c74d`; this round concentrates on `f863258d..e816c74d` and every named previous finding at its cause. Unchanged implementation retains its previous results, subject to checking changed dependencies. No source fix, commit, GitHub write, full build bank, local workflow replica or hardware operation was performed.

**Authority and evidence.** I read AGENTS.md / CONTRIBUTING.md, docs/README.md, the [frozen issue and public decisions](https://github.com/kebag-logic/milan-fpga/issues/969), relevant requirements and interfaces, and then the source delta and history. After that independent pass I read the prior public findings in [R886-1](https://github.com/kebag-logic/milan-fpga/pull/971#issuecomment-7080351329) and [R885-1](https://github.com/kebag-logic/milan-fpga/pull/971#issuecomment-7080730113). No current-round peer report, private handoff or author scratchpad was used.

The authorities examined include REQUIREMENTS.md's placement/ordering obligations; FR_NFR.md 3.4.1; the SRP integration contract and pinned lwSRP callback, visit and reclaim contracts; Milan v1.2 5.3.8.5, 5.5.3.5.18 step 4 and Tables 5.9/5.10 as cited by the public task; the #925 latest-kind decision; the #930 walk policy; the memory exceptions; and #818's timing floor. This review checks the cited interpretations against public decisions and executable behavior, not a fresh reading of the complete licensed standards.

The [option-1 ruling](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7083542634) and this round's explicit scope leave the pre-existing registration cost and the bound reference's over-share pass to #977. They do not authorize an unchecked kept pass or a missing comparison. No SRP unit, source-cost table or solved row was restated in this delta (`source-scope.txt`).

All 119 files under the immutable [second-round receipts](https://github.com/kebag-logic/milan-fpga/tree/1cd9d3fd3e46aaeeff6650f1bc60cce139645f0e/review-evidence/969-r1/author-r2/receipts), plus the three reused probe/integrity source artifacts, match the published SHA-256 manifest (`evidence-verification.txt`). The evidence commit has signature status `N`: no commit signature is present. This is a verified hash/provenance audit, not cryptographic signature verification (`evidence-provenance.txt`). Public source execution evidence is the author's receipts; no manager source bank is claimed or inferred.

**R886-2-F1 - MINOR - Conformance, Robustness, Tests, Docs - standalone kept grading can pass without current measurement evidence.**

Artifacts: `tb/verilator/ctrl_service_budget/kept_grade.py:101`, `:123`, `:225`; its documented conditions at `README.md:777`; the producer's refusal behavior at `run.py:681`; `probe_kept_grade.py`, `grader-probe-results.json` and `grader-stale-result-regrade.json` in this packet.

Authority/evidence: the ruling requires kept <= bound on the same image and no kept work pass over THE SHARE. This round explicitly requires a group without a graded result to be a finding. The final commit checks whether a JSON file is absent, but does not establish that it grades the current log. `over_share` defaults missing share data to an empty overrun list. The standalone entry point parses logs without rejecting their failed completion status. Independently, `held` silently continues when a kept probe has no matching bound-interface record.

The portable probe uses controlled synthetic logs in the repository self-test format and the real `grade.pass_share`, `run.graded` and standalone entry point. Results:

| Case | Observed result |
| --- | --- |
| Complete within-share control | PASS, exit 0 |
| Kept pass of 250,000 cycles at 100 MHz, complete current share result | FAIL, exit 1 |
| Same over-share log, graded-result file absent | FAIL, exit 1; the final commit's check works |
| Same log, result `{}` or a result without `passes.share` | PASS, exit 0 |
| All three kept probes on if0, bound reference only on if1 | PASS, exit 0, with no kept <= bound comparisons |
| Failed rerun, with an earlier within-share JSON still present | `run.graded` refuses it and returns no fresh result, retaining the old JSON; standalone `kept_grade.py` then reports PASS, exit 0 |

The last case is not merely an invented JSON schema: `run_group` overwrites a reused output directory's log, while `graded` leaves the previous JSON in place when the new run is refused. The probe demonstrates that path directly. The ordinary aggregate run still refuses that failed run; this finding is bounded to the new standalone grader and the missing prerequisites in its shared comparison helper. It does not assert that the published successful timing receipts have these corruptions or that #977's accepted debt is a new regression.

Impact: failed, absent or unmatched measurements can be promoted into a standalone PASS and the conditional #977 disposition without proving its conditions. The README's promise that any breach is a finding is consequently too strong. This affects a verdict and test evidence, so it is not wording residue.

Required outcome: a standalone PASS must require successful current logs and a share measurement attributable to those logs, and every required kept record must have its same-interface bound reference. Missing evidence must fail closed rather than becoming an empty list or a skipped comparison. Preserve the ruling's OWED treatment of valid #977 records and the unchanged SRP unit.

Verification: retain the passing control; reject failed/stale-result, empty/missing-share and missing-reference controls by name, as well as the already rejected absent-file and actual-over-share cases. Add these to the grader's executable checks, then regrade both published points. Fixing this finding does not require another firmware or route build if their inputs stay unchanged.

**R886-2-R1 - RESIDUE - Docs - review-round identifier in a new source comment.**

Artifact: `tb/verilator/ctrl_service_budget/kept_grade.py:48`. The new comment says `#969's STOP of round 2`. The owner's comment rule prohibits review rounds in source comments. Replace that comment with `#: The owner's disposition of the registration cost (#969, ruled 2026-11-22, option 1).` No executable behavior, figure, measurement or clause claim changes. Verify the added-line comment diff; this item leaves no lens unclean.

**R886-2-R2 - RESIDUE - Docs - stale helper name in explanatory prose.**

Artifact: `tb/verilator/ctrl_service_budget/kept_window.py:30`. Its module prose names `kept_grade.disposed`, which does not exist; `run.py` uses `kept_grade.Disposition`. Replace only that name with `kept_grade.Disposition`. The prose's intended behavior and all executable results remain unchanged. Verify against the class declaration and caller; this item leaves no lens unclean.

**Prior findings, explicitly reconciled.**

| Prior finding | Disposition at this head and evidence |
| --- | --- |
| R886-1-F1 = R885-1-F3, stale kept count | RESOLVED. `srp_mbx.c:287,486,817,951,968,1339` cover registration end, new kept admission, binding changes, a counted MT attribute, returned blocks and reset zeroing. Both reviewers' original probes plus the current early suite pass: 26/26 at each of 1x1 and 8x8, with one and two interfaces. With only the adapter replaced by f863258d's bytes, the same seven reset/reclaim/never-registered cases fail at every arm; fresh-vector, refresh, flood and UNBIND/BIND controls pass. |
| R886-1-F2 = R885-1-F4, omitted 8x8 campaign | RESOLVED. `test_ctrl_firmware.py:232` includes the early prefix and `srp_mutants.py:986` attributes each result to its shape. Published shard 3 contains 48 caught early results: all 16 at 1x1/1if, 1x1/2if and 8x8/1if. I reran the five trigger plants at all three points: 15/15 caught, including reset zeroing after the test refresh. |
| R886-1-F3 = R885-1-F2, memory figures | RESOLVED. Checked every named line: `SPLIT_CONTROL_MEMORY.md:188,189,190,305,307,311`, `plat/README.md:147` and `ctrl_memory_ledger.py:10`. Current entries are 63.5/58.5, debt 7.5/2.5 tiles and 30,720/10,240 B; plants use 64.0/63.5/59.0. ROM additions now agree with the final ledger receipts; historical figures remain labelled as history. |
| R885-1-F1, changed paths never measured | RESOLVED as a measurement omission under the ruling. `kept_window.py` now exercises Advertise retention, reclaim/recount and excess rejection, reset/Failed retention, LeaveAll encodings, and the bound reference. Both groups execute on the same image at each required point. The published records and builds meet the conditional comparison below. Registration-cost and bound-share debt remain OWED #977. New F1 above concerns the grader's handling of missing evidence, not the old absence of stimuli or the accepted cost debt. |

**Architectural and functional checks.** The fixed-block budget and `SRP_KEPT_TALKERS = CTRL_SRP_SINKS` remain enforced by static assertions. Bound StreamIDs bypass kept admission; unbound excess retains the documented first-come limit. `count_kept` visits outside callbacks, immediately before receive; indication callbacks only mark due state. A binding change requests a recount, while possible reclamation requires both pending state and a returned block. Reset zeroes occupancy with the destroyed participants. The kept list, latest-kind policy, replay boundary and unbound no-walk policy remain consistent with their contracts. No RTL, CDC, mailbox contract or dependency pin changed. The RTL lens includes these firmware accounting and layout effects, not just the absence of RTL files.

The unchanged platform S13/S14 tests still cover saved-binding restore through successful ACMP probing, BIND_RX while bound, the next MSRP transmission, every input and GET_STREAM_INFO's REGISTERING/REGISTERING_FAILED. Their public shard-0 results are 14/14 at both product shapes. This round independently reran the adapter's relevant boundary paths, not the entire platform or hardware campaign.

**Measurement and gate audit.**

| Evidence | Examined result and limit |
| --- | --- |
| Changed-path CPU records | At 1x1/1if, kept Advertise/recount/Failed cost 34,497 / 32,224 / 36,859 cycles versus bound 38,956. At 8x8/1if, 137,352 / 68,692 / 142,909 versus 153,208. Every over-unit record is explicitly OWED #977, with no restatement. |
| THE SHARE and builds | No kept work pass exceeds 200,000 cycles; the bound 8x8 pass of 224,540 is explicitly OWED #977. Kept build-one maxima are 39,123/73,500 and 82,768/147,500; bound maxima 53,970/73,500 and 101,786/147,500. LeaveAll output includes 2 and 9 kept values. Zero dual-build maxima are not presented as dual-build executions. |
| Hot section | `hot-section-f02d44cd.txt` shows reset_interface grows 16 B, subsequent hot functions shift 16 B, and no other hot function changes size. `per-probe-base-vs-f02d44cd.txt` and the six-group summaries measure the five prior groups plus kept at both points. Seven existing backlog-owed misses remain and no work pass exceeds THE SHARE there. Those older summaries return 1 for pre-disposition kept-unit overruns; they are not claimed as green runs. The later paired-group run and final grader explicitly apply #977's ruling. This is scoped measurement, not a full cost survey. |
| Firmware gates | Published shard 0 at 5dba2089: 88 arms; shards 1/2 at f02d44cd: 827/827 and 385 caught; shard 3 at ecd5bf41: 591 caught, including the 48 early results. All end PASS. The earlier escaped zeroing plant is retained as failed evidence and superseded by the refresh-corrected test/run. Later source changes do not alter those relevant firmware inputs. |
| Coverage | Published ecd5bf41 check passes for 40 files. SRP: 861/861 lines, 779/782 raw branches; the three existing exclusions give 779/779 effective branches. The ratchet matches. |
| Images and ledgers | Platform ROM/SRAM needs: 127,376/56,736 B, 128,984/59,104 B, 140,136/98,288 B and 141,720/115,760 B at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if. Their plans are 45.5, 46, 58.5 and 63.5 RAMB36. The 8x8/1if size-fixture stand-in is separately 56.0, with 112 B ROM margin; it is not the 58.5 product image. Published ledger and boundary-plant tests pass. |
| Twin and routes | Published twin, twin-plants, twin-maps and map plants pass at f02d44cd. Routes at that final firmware source use AreaOptimized_high / ExploreArea / ExtraPostPlacementOpt. All four listed corners meet WNS >= +0.030 ns and WHS >= 0; worst WNS/WHS +0.128/+0.032 ns and +0.096/+0.036 ns at 1x1/1if and 8x8/1if. Zero routing errors and image-identity PASS are recorded. Other placement directives were not run. No route was rerun here or promoted into current-dev candidate proof. |
| Graders and documentation | My exact-head kept self-test, both flip checks, load check and shape-cost check return 0. These are grader executions, not new timing measurements. Held figures remain last 127.31/130 ms, ACMP 29.06/30 ms, txL 47.88/49 ms; 8x8 transmit 76.81/77 ms and load 0.744/0.75. Published exact-head docs table has 99 successful commands and four environment refusals; it is not 103 passes. The two residue items were found by manual added-comment review. |

Final firmware implementation sources match f02d44cd; the later delta changes tests, the ratchet, prose, ledger reason strings and the CPU harness. Route receipts name their actual build revision. No independent final ELF rebuild or cryptographic binary-equivalence proof is claimed.

**Reviewer-owned lens ledger.**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN - F1 | #969 acceptance/ruling; SRP README; srp_mbx.c admission, recount and reset; platform early tests; kept_grade.py conditional measurement claims and grader probes | R886-2 applied; no clean coverage | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |
| RTL | CLEAN | Scoped diff; srp_mbx.c:29,287,968,1294; srp_mbx.h pool/layout bounds; pinned lwSRP interfaces; hot-section, ledger and route receipts | R886-2 | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |
| Robustness | UNCLEAN - F1 | Both published probe sources; eight reset/reclaim/control runs; five trigger plants at three points; kept_grade.py missing/failed-result and missing-reference probes | R886-2 applied; no clean coverage | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |
| Tests | UNCLEAN - F1 | srp_mbx.cpp; srp_early_mutants.py; test_ctrl_firmware.py; 48 published plants; 15 independent plants; firmware/coverage/twin receipts; probe_kept_grade.py | R886-2 applied; no clean coverage | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |
| Docs | UNCLEAN - F1 | All prior named memory lines; SRP/platform READMEs; CPU README:777; public ruling and evidence claims; new source comments | R886-2 applied; no clean coverage | e816c74da53a5822f2ddc1661e5ffae297f1b3aa |

[R886] PASS RTL - `sw/firmware/ctrl/srp/srp_mbx.c:968`, `srp_mbx.h:136`, scoped diff and published layout receipts - recount/reset accounting, fixed storage, callback boundaries and unchanged hardware interfaces checked against the stated contracts; no open finding in this lens.

**Limits and manager duties.** Physical calibration and the bench rerun are NOT RUN here. Field skips and simulation results are not hardware proof. Hosted job status was not independently polled this round; executed jobs, skipped contexts and hosted/local acceptance remain the manager's responsibility. No manager source-head builder/native run exists or is inferred. The manager must separately construct and validate the actual current-dev merge candidate, publish its builder/native receipts, complete hosted/local acceptance and containment, obtain merge authorization, and perform the physical qualification. The supplied live-dev reference `e275d7950ef3385753e6a15d2e191ba855b171ed` is not a candidate built by this review. #977 remains owed before qualification closure. This verdict does not authorize merge or close #969.

**Reproduction and packet.** Scripts accept `CHECKOUT PACKET`. `audit_evidence.py` verifies immutable public receipts; `run_probes.py` runs both prior probe sets and current early tests against head and the old adapter in disposable trees; `run_plants.py` runs the five trigger plants concurrently at three points; `run_graders.py` repeats the lightweight checks; `probe_kept_grade.py` reproduces F1; `verify_tree.py` checks every tracked blob, mode, index entry and required submodule gitlink. Run the build drivers sequentially relative to one another; they join their own concurrent work, at most 16 compiler jobs. All disposable trees stay under `scratch/` and are excluded from publication. Old-adapter nonzero results are expected failing-first evidence; mutation logs contain intended failures.

`tree-integrity.json` verifies the exact requested head/tree and all five required initialized submodules after the probes. No tracked source or index bytes were changed. `MANIFEST.sha256` lists the publishable receipts and portable scripts with relative paths; unlisted public snapshots and scratch are not part of the publication.

R886-2 FINISHED
