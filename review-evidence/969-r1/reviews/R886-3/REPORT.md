[R886] POSITIVE - exact head c113018d3cd4e70a7d3b66940a3a88fb93f0421a

Round R886-3, external independent delta review of issue #969 / PR #971. All five lenses are CLEAN. Every prior MINOR is resolved; earlier functional resolutions stand on unchanged inputs. One new wording-only RESIDUE is recorded below. No open BLOCKER, MAJOR, MINOR or SUGGESTION was found in this delta. This is a source review, not merge authorization or validation of a future merge candidate.

Examined tree: `2a032e207225763bb455c62ba77ec39ed5f8b008`. Full source scope: `dd163e41438acb86e0c4d4e76df90f3f91ace1c0..c113018d3cd4e70a7d3b66940a3a88fb93f0421a`; this round judges the delta from `e816c74da53a5822f2ddc1661e5ffae297f1b3aa` and named prior findings at their causes. The four changed files are `docs/design/SPLIT_CONTROL_MEMORY.md`, and the CPU budget harness's `README.md`, `kept_grade.py`, `kept_window.py`. The last changes only module prose: its executable syntax tree is identical. Firmware, RTL, configuration, budget bounds and dependency pins are unchanged (`source-scope.txt`).

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the frozen issue and public scope decisions, linked requirements/interfaces, then diff/history and public evidence. The independent delta verdict and ledger were written before reading prior public finding bodies. Afterwards I reconciled [R885-2](https://github.com/kebag-logic/milan-fpga/pull/971#issuecomment-7091817175), [R886-2](https://github.com/kebag-logic/milan-fpga/pull/971#issuecomment-7091818363), and both first-round finding lists. No private author material, private management material, or current-round peer report was used.

Authorities include REQUIREMENTS.md section 1; FR_NFR.md 3.4.1; MAILBOX_SPLIT.md's loop/share/ownership contract; Milan v1.2 5.3.8.5, 5.5.3.5.18 step 4 and Tables 5.9/5.10 as cited in the frozen task; the pinned applicant-state implementation of IEEE 802.1Q-2018 Table 10-3; and the [option-1 ruling](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7083542634). The [#977 addendum](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7086032855) explicitly retains the bound path's share overrun as debt. That accepted debt is not a passing original budget. The complete licensed standards were not freshly obtained or reread.

**Prior findings, explicitly reconciled at this head**

| Finding and attributable lenses | Disposition and evidence |
|---|---|
| R885-2-F1 / R886-2-F1; Conformance, Robustness, Tests, Docs | RESOLVED. `kept_grade.py:93` reads `grade.pass_share(log)` directly and separates work starts from idle-run indices. `:110` refuses failed/incomplete/trapped/bus-error logs; `:115` checks required probes; `:134` names a missing same-interface bound record. `:205` handles absent logs and parser refusals. Neither entry point reads result JSON. Thus absent/empty/stale JSON cannot conceal a log's overrun; complete clean logs may legitimately pass without JSON. The standalone and Disposition paths share `held`. Independent probes, published original-probe reruns and the regrades support closure. |
| R885-2-F2; Docs | RESOLVED. `SPLIT_CONTROL_MEMORY.md:693`, PR Known limitations and `author-r3/receipts/budget/hot-section-census.txt` agree: of 261 platform hot functions, 152 change, comprising one resized reset function and 151 shifted functions; 109 remain unchanged. The separate budget images have 266 functions, 155 changed = 1 resized + 154 shifted, 111 unchanged. The published position-based census script avoids conflating repeated static symbol names. No new binary measurement is claimed here. |
| R885-2-F3; Docs | RESOLVED. `kept_window.py:17` and harness `README.md:771` now distinguish the LeaveAll from the following In-carrying MRPDU and retain the separate LeaveAll owner/deadline check. The decoded receipt gives 14.213/14.404 s at 1x1 and 14.253/14.443 s at 8x8, with two/nine kept values in the second frame. The pinned `third_party/lwSRP/src/core/mrp_mad.c:178` and `:185` support the TX-from-LO and TXLA observer transitions. |
| R885-2-F4; Tests, Docs | RESOLVED. `kept_grade.py:275` and `:338` now exercise held conditions, paired Disposition, standalone file handling and build-one overruns. Exact-head self-test passes 19/19. Published guard-removal receipts show 20 caught, zero escaped, with failing check names; the three formerly escaping guards are explicitly caught. Inspection confirms the plants alter the intended guards and the unmodified control passes. |
| R885-2-R1 / R886-2-R1 / R886-2-R2; Docs, RESIDUE | RESOLVED. `kept_grade.py:58` uses the issue and ruling date without a review-round label; `kept_window.py:33` names `kept_grade.Disposition`. No new prohibited source-comment label was found. |
| R886-1-F1 / R885-1-F3; all five lenses | Earlier RESOLVED disposition retained. Recount/reclamation at `srp_mbx.c:968` and reset zeroing at `:1339` remain unchanged. The earlier reset/reclaim/control executions and trigger-plant evidence remain applicable; this grader delta changes none of their inputs. |
| R886-1-F2 / R885-1-F4; Tests, Docs | Earlier RESOLVED disposition retained. `test_ctrl_firmware.py:232` still selects the early campaign at 8x8/1if. Earlier evidence contains 16 early plants at each of three points, 48 caught. No campaign source or test changed. |
| R886-1-F3 / R885-1-F2; Docs | Earlier RESOLVED disposition retained. Named memory-entry/plant/debt locations are outside the delta and still state 63.5/58.5 entries, 64.0/63.5/59.0 plants and 7.5/2.5 tile debts. The new hot-function sentence is reconciled separately above. |
| R885-1-F1; RTL, Robustness, Tests, Docs | Earlier measurement-omission resolution retained under the public ruling. Both groups' stimuli and all measurement inputs remain unchanged. The new grader regrades their existing runs; no changed path is newly asserted to have been remeasured. Registration cost and the bound share overrun remain OWED #977. |

**R886-3-R1 - RESIDUE - Docs - reconnect the memory-addition sentence**

Artifact: `docs/design/SPLIT_CONTROL_MEMORY.md:693`.

Authority/evidence: the edited paragraph now ends its ROM sentence before the hot-function census, but leaves the subsequent RAM addition attached as `the 109 before it do not move; and to` followed by the `ctrl_plat` figures. The inherited conjunction no longer has its governing verb in that sentence.

Impact: grammar only. Every figure, measurement, behavior, test, verdict and clause claim remains unchanged; no privacy rule is involved.

Required exact fix: replace `the 109 before it do not move; and to` with `the 109 before it do not move. The change adds to`. Keep the following `ctrl_plat` figures verbatim.

Verification: inspect that prose-only substitution and confirm all numbers and claims remain identical. Under the owner residue rule this does not make the verdict NEGATIVE or any lens UNCLEAN. The manager may carry it to the residue checklist.

**Execution and published evidence**

The immutable [public packet](https://github.com/kebag-logic/milan-fpga/tree/e6835fbaa3942f3c2ad0dc5f8a1968a118e45a55/review-evidence/969-r1) contains 245 author receipt files across the three rounds. Every checked byte matches `published_sha256` in MANIFEST.json (`receipt-integrity.txt`). The commit has no embedded signature, and no detached signature artifact was found in the packet inventory. This is content-integrity verification at the named public commit, not cryptographic signer verification.

| Check | Result and scope |
|---|---|
| Independent exact-head self-test | `python3 -B tb/verilator/ctrl_service_budget/kept_grade.py --selftest`: exit 0, 19/19 (`selftest.log`, `selftest.rc`). |
| Independent focused inputs | `probe_logs.py CHECKOUT PACKET`: 19/19, exit 0 (`probes.log`, `probes.rc`, raw `probe-results.json`). Clean one/two-interface controls pass; absent, empty, stale and syntactically invalid sidecars cannot hide an over-share log. Both groups reject failed/incomplete logs, traps, bus errors and idle overruns. Missing bound log, missing mate at two interfaces and unknown log syntax fail by name. |
| Published guard plants | 20/20 caught; zero escaped, unplanted 19/19. The unchanged original external probe and adapted internal probes have the required positive/negative outcomes. Verified scripts and receipts, not a new mutation campaign. |
| Published complete harness self-test | Exact-head receipt ends `self-test: 0 failures`; published 295-mutant claim remains execution evidence from the author. No full harness rerun here. |
| Published documentation checks | Exact-head table: 99/103 commands return zero; four environment-dependent refusals remain refusals. This is not 103 passes or manager acceptance. |
| Checkout integrity | 1,938 root blobs and 1,362 blobs across five initialized required submodules match exact bytes, modes and index entries; gitlinks match the requested head. Unused external remains uninitialized. See `tree-integrity.json`. No tracked file was edited. |

The paired regrade receipts explicitly identify images at `5dba2089`, with firmware unchanged since `f02d44cd`. They are regrading, not fresh timing runs. `reviewed-receipts.txt` retains the examined public results and census.

| Point | Kept Advertise / recount / Failed cycles | Bound cycles | Kept work passes / idle runs | Kept / bound build-one maximum; limit |
|---|---:|---:|---:|---:|
| 1x1/1if | 34,497 / 32,224 / 36,859 | 38,956 | 1,910 / 1,862 | 39,123 / 53,970; 73,500 |
| 8x8/1if | 137,352 / 68,692 / 142,909 | 153,208 | 1,911 / 1,863 | 82,768 / 101,786; 147,500 |

Both standalone receipts return 0, with zero kept work or idle overruns. Both bound idle populations also have zero overruns. The 8x8 bound work pass of 224,540 cycles is explicitly OWED #977. Disposition retains five/seven STATED lines and zero/one SHARE lines as owed, with zero findings. The SRP units remain 285/375 us. Zero dual-build maxima are not evidence of dual-build execution. Original full simulation logs and ELF inputs are not included among these public receipts, so I checked receipt hashes, consistency, producer/grader code and focused synthetic inputs rather than independently recreating the measured runs or symbol census.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #969 ruling and #977 addendum; `kept_grade.py:102` prerequisites; both regrade receipts; independent log probes. F1's conditional share/comparison proof restored. | R886-3 delta; untouched functional coverage retained from R886-2 | c113018d3cd4e70a7d3b66940a3a88fb93f0421a |
| RTL | CLEAN | Four-file diff; unchanged firmware/interfaces/pins; `srp_mbx.c:968,1339`; corrected census and paired-cost receipts. No changed architectural dependency invalidates the earlier clean result. | R886-3 delta plus R886-2 clean coverage at e816c74da53a5822f2ddc1661e5ffae297f1b3aa | c113018d3cd4e70a7d3b66940a3a88fb93f0421a |
| Robustness | CLEAN | `kept_grade.py:93,110,134,205`; failed/incomplete/trap/bus-error, stale-result, idle and two-interface missing-mate cases in `probe-results.json`. | R886-3 | c113018d3cd4e70a7d3b66940a3a88fb93f0421a |
| Tests | CLEAN | `kept_grade.py:275,338`; 19/19 self-test; 19 independent cases; published 20/20 guard-removal and original-probe receipts. | R886-3 | c113018d3cd4e70a7d3b66940a3a88fb93f0421a |
| Docs | CLEAN | `SPLIT_CONTROL_MEMORY.md:693`; harness `README.md:765`; `kept_window.py:17,33`; census, decoded-frame receipt and public PR claims. All numerical/behavioral findings resolved; R1 is wording-only. | R886-3 | c113018d3cd4e70a7d3b66940a3a88fb93f0421a |

**Limits and pending manager duties**

Physical calibration and the bench acceptance rerun are NOT RUN. Field skips, host tests and desk receipts are not hardware proof. No manager source-head bank exists or is inferred. Source evidence is the author's published receipts plus the focused checks above. Hosted status was not polled; no skipped context is counted as execution. Hosted/local-replica acceptance remains the manager's.

The source base is dd163e41. The supplied live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`; no candidate against it was built here. At merge time the manager must construct the actual current-dev candidate, run builder/native and required gates, publish receipts, apply the owner's MINOR-only delta review rule and complete the independent review bar, obtain merge authorization, and finish containment and issue/board closure. #977 remains owed before qualification closure. This report does not close #969 or approve a merge.

No full bank, hardware operation, container, host CI orchestrator, source fix, commit, push, GitHub write, shared install, privilege operation or sub-agent was used. All executions completed in the foreground; generated inputs stayed under packet `scratch/`. Portable `audit_packet.py`, `probe_logs.py` and `verify_tree.py` accept `CHECKOUT PACKET`. Only REPORT.md and files in MANIFEST.sha256 are publishable; scratch is excluded.

R886-3 FINISHED
