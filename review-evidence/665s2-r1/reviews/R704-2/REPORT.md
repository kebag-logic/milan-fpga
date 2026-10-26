[R704] NEGATIVE - exact head cd3525c3ddcbdb5d78bf8fccdab354c468926997

External independent review R704-2 of issue #665 / PR #792. All five lenses were applied. One MAJOR and one MINOR remain open, plus previously identified wording residue. The expected T_svc miss is the measurement result, not a finding.

Tree: `8880067ab9fbfc65736fea8e245a2e748c1df279`. Source base: `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. This review judges the single commit after `d58c8e22e9bd96237b9a28ea1ddd55b0426380c4`: eleven changed files, all within `tb/verilator/ctrl_service_budget/`. The round-1 ledger remains a statement about its own head; unchanged implementation is not treated as new work.

Reconstruction followed AGENTS/CONTRIBUTING, docs/README, frozen public scope/decisions, requirements/interfaces, full source range and delta/history, then executable evidence. Authorities include the [original assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409745905), [owner decisions](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409738976), [measurement STOP disposition](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6413711129), [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6415127884), FR_NFR.md 3.4.1/3.4.2, MAILBOX_SPLIT.md service/backlog tables, mailbox.yaml and KL_mbx_rx admission. Prior public findings were read only after the independent delta pass. No other round-2 reviewer report or private author material was read.

**R704-2-F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs**

Artifact: `tb/verilator/ctrl_service_budget/scenario.py:676`, `:684`, `grade.py:555`, `README.md:276`, `:314`, `:318`; PR body, Description/load row.

Authority/evidence: round-2 item 1 requires every backlog window, including the owed row, to carry every channel's admitted burst. For the selected GET_RX_STATE frame, admission is `min(16, floor(256/20)) = 12` ACMP records. `owed_group` excludes ACMP from `composed_load`, supplies seven commands plus its probe, and declares only eight. Both fresh native owed windows reproduce ACMP=8, while the PR body claims ACMP=12 in every backlog window. `delta-probes.json` independently compares generated populations with admission and identifies this shortfall at both points. The other channels now include MAAP=7 and SRP=32 as required.

The coverage guard compares observations with `group.load`, which the stimulus itself increments. It does not establish that the declaration meets the required population. An in-memory plant removing SRP from backlog stimulus and its declaration leaves all 51 self-test checks passing (`scenario-control.json`, `probe_scenario_control.py`). The fixture's missing-commit test protects a log against its declaration; it does not catch an omitted channel in the actual backlog scenarios.

Impact: the owed-row figures still do not measure the required composed load. Shortened stimulus can redefine its coverage expectation and pass. This retains the load-completeness cause of R704-1-F1 and R703-1-F1. The RTL lens applies to admitted-load/backpressure characterization; no new shipping RTL defect is alleged.

Required outcome: measure the owed row with the full required admitted population while preserving and proving the intended seven responses ahead of the measured response. Check scenario coverage against an independently specified contract-derived population, so omitting background work cannot silently reduce the expectation. Re-measure affected rows and update README/PR claims without bypassing ingress admission.

Verification: at both points, require twelve admitted ACMP commands and the other stated channel populations in the owed window, with causal/queue evidence for the measured response. Omitting SRP, MAAP, or the missing ACMP work must fail a named coverage check. `probe_native_delta.py` supplies a disposable twelve-command falsification probe; it is not a source fix.

**R704-2-F2 - MINOR - Conformance, Tests, Docs**

Artifact: `tb/verilator/ctrl_service_budget/scenario.py:760`, `:765`, `:768`; `run.py:48`; `README.md:161`.

Authority/evidence: round-2 item 6 requires distinct path counts and probe-instance counts. `shutdown_groups` explicitly describes its control as “the same path”. Both groups start at `entry:adp_mbx_set_enable`, end at the same interface's DEPARTING commit, and report identical timing. But the control lacks the canonical path override used for `control.discover`; it becomes `control.shutdown`, distinct from `adp.shutdown`.

`receipt-audit.json` reproduces the published counters: S1 reports two paths/two instances, although one path/interface is measured twice. S8 reports three paths/three instances, although there are two distinct interfaces and the interface-0 control is repeated. Canonicalizing that duplicate changes path denominators to one and two, preserving instance totals, times and zero misses.

Impact: the new arm overstates distinct path coverage. This changes a generated numeric result and is not wording residue. The SHUTDOWN measurement and its over-budget control remain valid.

Required outcome: give repeated control instances the same canonical path/interface identity as their functional instances. Regenerate counts and tables, including README; keep controls as separate probe instances.

Verification: S1 reports one path/two instances; S8 reports two paths/three instances. A test using the real shutdown groups must detect splitting the control into a fictitious path. Worst-instance selection and miss counts must remain correct when duplicate instances differ in latency.

**R704-2-R1 - RESIDUE - Docs; retained R703-1-R-4**

Artifact: `docs/testing/TESTING.md:518`.

Authority/evidence: the suite index still calls `nvm_capture_cpu` the sole manual Makefile exception. The author explicitly leaves this earlier finding for the manager's residue checklist because this document is outside the lane's file map.

Impact: wording only, changing no execution, measurement or acceptance claim; it does not make a lens unclean.

Exact required fix: replace “The manual `nvm_capture_cpu` measurement is the Makefile exception.” with “The manual `nvm_capture_cpu` and [`ctrl_service_budget`](../../tb/verilator/ctrl_service_budget/README.md) measurements are the Makefile exceptions.”

Verification: inspect the sentence/link; executable files and results remain unchanged.

**Prior-finding dispositions**

| Prior finding | Disposition at this head | Evidence |
|---|---|---|
| R704-1-F1 / R703-1-F1: incomplete composition; burst presented as bound | Partially resolved; retained as F1 | MAAP uses each interface's announced range; SRP is offered; burst observations are distinguished from ring-room bounds; refill leg and occupancy added. Owed ACMP remains 8/12. |
| R704-1-F2 / R703-1-F3: first-recipient endpoint | Resolved | `grade.py:276` matches command/descriptor and controller/interface. Unchanged prior traces now give 14 ms/MISS for a late recipient and `no end` for a missing one. Duplicates, wrong recipients and unrelated notices are tested. |
| R703-1-F2: unprotected headline figures | Resolved | 51 checks pass; 36 mutants caught. Independent conversion, pass-origin and composition plants change headline/bound values and fail named checks (`delta-probes.json`). |
| R704-1-F3 / R703-1-F5: unattested reused inputs | Resolved | An unchanged copied build reuses. Both CLI modes reject changed/deleted ELF, every init file, SoC Verilog and CPU netlist. Unresolved basename refused. Self-test also covers unrecorded ROM, firmware and executable changes. |
| R704-1-F4 / R703-1-F6: missing selected logs dropped | Resolved | One absent log among an intact group, and all selected logs absent, return 1 and name the missing groups, with/without recorded findings. An intact explicit subset returns 0. |
| R704-1-F5 / R703-1-F7: SHUTDOWN unmeasured | Resolved | Labelled test-only entry, passive committed-entry observation, published S1/S8 measurements and delay control; source inspected. F2 concerns counting only. |
| R703-1-F4: omitted worst instance and ambiguous counts | Prior cause resolved; new F2 remains | A1/A8 aggregation yields 10/61 paths and 11/78 instances; 37/106 paths and 45/125 instances. README includes the worst fixture H-DISC row. |
| R704-1-R1 / R703-1-R-1: lane/round source comments | Resolved | Specified comments retain issue/requirement IDs without lane/reviewer labels; added comments inspected. |
| R703-1-R-2/R-3: attribution and composed-group wording | Resolved | README names module totals and distinguishes a group's maximum from the overall maximum. Current PR wording checked; historical comments remain historical. |
| R703-1-R-4 | Retained as R1 | Exact fix above. |
| R703-1-S1/S2 | Applied | WIRE parser stores channel/interface in declared order; tables expose timed-out waits; flash cost range is 15 to 29 times. |

The prior `probe_graders.py` was rerun unmodified and is retained byte-for-byte. It now stops at the corrected API's refusal of a notification declaration without recipients (`prior-unmodified.log`); that script asserted the old defects and cannot be presented as a passing new regression. Its original raw fault traces were rerun without byte changes, supplying only the now-mandatory selector/recipient metadata through a separate adapter. The prior native fan-out stimulus is also unchanged. No timing or recipient expectation was weakened.

**Execution evidence**

The [immutable publication](https://github.com/kebag-logic/milan-fpga/tree/33750832853802892619b60c16d7fa37d3911ccc/review-evidence/665s2-r1) matches its publication manifest: 227 round-2 author entries and 217 own prior-round entries, 444 total (`publication-check.json`). Fourteen available public raw traces regrade identically. Published broad gate receipts identify this head and report success; they remain the author's source-head evidence. No manager source bank is claimed or inferred.

No detached signature is present in the supplied publication; its commit reports signature status `N`. Verification establishes published digest consistency and immutable commit identity, not cryptographic signature authentication.

Fresh focused builds reproduce the published ELF, ROM-bank bytes, cached CPU netlist and relevant configuration (`build-audit.json`). Generated SoC text and runtime archives differ in raw hash, so whole-build byte identity is not claimed. Cached netlists were copied into scratch and generation disabled. The pinned simulator identity was verified before use. Builds used sixteen compile jobs; independent campaigns ran concurrently under foreground drivers, with no more than thirteen simulations active. No full parent, processor, builder or synthesis bank was run.

Each point freshly ran `backlog`, `backlog-adp`, `backlog-adp-refill`, `backlog-owed` and `aecp`. All ten complete graded results match published results exactly, including every cycle, endpoint, pass, population and occupancy field (`receipt-audit.json`, `measurements/`). Both runs return 0 with budget findings recorded and zero refusals. The selected sets contain five misses among 30 instances at 1x1 and six among 44 at 8x8; these are not the full-campaign totals.

| Fresh arm-A measurement | 1x1, ms | 8x8, ms |
|---|---:|---:|
| Composed maximum | 31.31606 | 44.18616 |
| Event backlog | 15.48672 | 44.65077 |
| ACMP receive backlog | 63.30384 | 108.71184 |
| ADP burst backlog, observed | 67.93215 | 83.50583 |
| ADP refill leg, observed | 88.33429 | 118.80743 |
| Owed row, with only eight ACMP commands | 125.78931 | 151.91561 |

The portable self-test has zero failures: 51 checks, 36 caught mutants (`selftest.log`). Published shutdown times are 0.58170 ms at 1x1 and 0.58370/1.17496 ms across two interfaces. The planted shutdown delay measures 24.90262 ms and is caught. These shutdown native runs were assessed through public receipts and source, not independently rebuilt here.

The unchanged prior native fan-out stimulus now measures 7.70397 ms through the last required recipient. Adding four ACMP commands behind the original owed probe preserves its seven preceding responses and changes the owed figure to 126.29163 ms at 1x1 and 161.10225 ms at 8x8 (`native-probes/`). These disposable variants demonstrate sensitivity to the omitted work; they do not substitute for a corrected, independently guarded published scenario. All three native probes exit 0.

**Reviewer-owned delta ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | Frozen items 1-6; FR_NFR.md 3.4.1/3.4.2; MAILBOX_SPLIT.md rows; scenario.py, grade.py, run.py; endpoint/load/count probes | R704-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |
| RTL | UNCLEAN: F1 | KL_mbx_rx.sv:597-631; mailbox.yaml depths; sim_main.cpp per-interface reply selection and entry observer; build/netlist identity; owed-ring/backpressure stimulus | R704-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |
| Robustness | UNCLEAN: F1 | Recipient controls; changed/missing/unresolved inputs; absent/partial logs; backlog/refill/owed windows; missing-channel plant | R704-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |
| Tests | UNCLEAN: F1, F2 | selftest.py, selftest_mutants.py, fixture.log/oracle.json; fresh native runs; unchanged prior traces; CLI probes; shutdown count audit | R704-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |
| Docs | UNCLEAN: F1, F2 | README tables/claims; public PR body/issue decisions; hashed author receipts; suite-index residue | R704-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |

The prior architecture conclusion remains valid for unchanged CPU/memory/clock placement. The current RTL-lens finding concerns changed admitted-load/backpressure coverage, not a new shipping RTL or default-placement defect.

**Limits and pending duties**

These are source-head simulation measurements at one phase per probe. Phase bounds are conditional on the same passes; burst observations are not sustained-arrival bounds. The disclosed test fixture, placeholder map, decode cover, unavailable observation ports, zero flash device wait, idle DMA, absent datapath/DDR and unmeasured START_STREAMING remain limits. Mailbox commitment does not prove wire/network deadlines. Physical calibration was NOT RUN; field skips are not hardware proof.

The manager must publish this packet, obtain fixes and independent re-review, and carry R1 to the residue checklist. Hosted/act acceptance, final current-dev candidate builder/native banks and receipts, authorized merge and post-merge containment remain manager duties. This source review does not validate a merge with live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee` or authorize a merge.

No source fix, commit, push, GitHub write, author contact, other-checkout edit, hardware access or prohibited bank was performed. Disposables are under scratch. `identity-final.json` verifies raw tracked bytes, types/modes, index and required submodule gitlinks. `MANIFEST.sha256` lists publishable receipts; scratch is excluded. `receipt-index.json` records original and published digests for path-normalized receipts. Numerical simulation traces and the original prior scripts are unchanged; local paths in driver/build metadata are replaced with role-based placeholders.

R704-2 FINISHED
