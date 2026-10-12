[R607] NEGATIVE - exact head 8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d

External independent delta review, round R607-4, issue #640 / PR #721. Tree `9c57147d7f2535836e260540372cac0cae7d7049`. One MINOR remains open under Conformance, Tests and Docs. RTL and Robustness are CLEAN. The memory implementation passes the focused functional checks; the merged firmware invalidates the claimed current fit figures and the unchanged-input basis for carrying forward the mapping receipts.

Reconstruction followed the requested order: AGENTS.md / CONTRIBUTING.md; docs/README.md; the issue body and public scope decisions; requirements and interface authorities; `c6bd08c6..8ab2b539` and history; public executable evidence. The independent verdict and five-lens ledger were written before reading the prior public reviewer findings. No concurrent round-4 report was consulted.

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100371426), [M8a-1 ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101485877), [round-2 scope](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105011666) and [round-3 scope](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6107088105) govern this lane. M8a-1 covers the split memory map and instantiation, four-point fit, ledger, named controls and unchanged all-fabric default. M8a-2 owns split boot, service checks and the integrated route after F-INT PR 2. This review does not claim completion of issue #640's 38,040-LUT target.

**R607-4-F1 - MINOR - Conformance, Tests, Docs - merged firmware outgrows the published fit inputs**

Artifacts: `docs/design/SPLIT_CONTROL_MEMORY.md:146` and `:155`; `docs/design/MARK_II_AREA_PLAN.md:824` and `:829`; `docs/design/AREA_BUDGET.md:260`; the four current linked fixtures and previous-source controls in `fit-comparison.log`, `fit-comparison.json`, `fit-*.json` and `previous-fit-*.json`.

Authority/evidence: ruling 6101485877 requires four-point linked spans, out-of-context primitive mapping and measured ledger rows. AGENTS.md section 7 ties coverage to the artifacts actually examined. The merge changes firmware through F-INT and the lwSRP adoption even though the M8a memory planner and mapping recipe themselves are unchanged. With the same compiler and byte-identical runtime archives, rebuilding `ce10328c` reproduces every published old span and planned tile count. Rebuilding the reviewed head changes all four spans:

| Shape / interfaces | Previous ROM / SRAM bytes | Head ROM / SRAM bytes | Previous planned tiles | Head planned tiles |
|---|---:|---:|---:|---:|
| 1x1 / 1 | 95,032 / 45,520 | 96,624 / 45,776 | 35.0 | 35.5 |
| 1x1 / 2 | 96,320 / 56,880 | 98,056 / 57,152 | 38.0 | 38.0 |
| 8x8 / 1 | 108,680 / 86,080 | 110,344 / 86,336 | 48.5 | 48.5 |
| 8x8 / 2 | 110,056 / 112,208 | 111,848 / 112,464 | 54.5 | 55.0 |

The largest ROM gains a 2 KiB bank: 64 + 32 + 8 + 4 + 2 KiB. Its current real SoC export contains that fifth ROM bank (`split-inspection.log`). The largest allocation has one tile / 4 KiB of planned allocation headroom, rather than the documented 1.5 tiles / 6 KiB. The shipping 1x1 ROM changes from five banks to two. Therefore unchanged mapping inputs cannot justify carrying the old mapped RAM/LUT figures forward. This is a measurement/evidence defect, not wording-only RESIDUE.

Impact: the fit table describes the previous composition while presenting current reproduction commands and headroom. The old 53 mapped tiles and derived mapped ledger remain historical measurements; they are not measurements of the merged images. All four newly linked images still pass the 56-tile planner limit, and the largest exports successfully. No actual over-budget or functional failure is asserted, and no new mapped primitive count is inferred from the planner.

Required outcome: refresh the four linked-image and isolated mapping receipts for the merged composition; reconcile the fit table, affected memory ledger rows and headroom statements with those receipts. Retain older figures only with explicit source attribution. An equivalent proof of unchanged mapped outcomes must account for the changed image contents and bank structures. This requests no integrated route or boot in M8a-1.

Verification: rerun the four `ctrl_srp_image.py --with-aecp --layout split` points with a recorded runtime; confirm their spans, bank plans and staging sizes; run `syn/ooc/ctrl_memory_ooc.py` and its focused synthesis recipe on those images; reconcile the resulting RAMB36/RAMB18/LUT figures and ledger arithmetic. `run_fit.py` and `compare_fit.py` reproduce the source delta without any source edit.

The runtime comparison used the established independent workaround for the separately assigned runtime stack-protector issue: `runtime_probe.py` adds only `-fno-stack-protector` to runtime compilation. Both source revisions used the exact same archives: libc SHA-256 `2fab1665a10d42c1e0a76984d6f2dc83abc2bd2e16bc6c3ff1ad4186afff5fb5`, compiler runtime `e32cb0d0d61e4f3e0fe8829367233370b45c7754931299ebff7a3c6ed49ef9aa`. The previous-source control matching all four published rows isolates the new difference from that workaround.

**Applied lenses and executed evidence**

| Lens | Artifacts and result |
|---|---|
| Conformance | Ruling 6101485877 against `ctrl_memory.py:43`, `:264`, `:294`; `ctrl_split.ld:13`; `milan_soc.py:2732`, `:2762`, `:4038`, `:4337`. Budget, reset ownership, flag pairing, shape refusal and default preservation pass. Four-point current mapping acceptance remains open as F1. |
| RTL | `milan_soc.py:2732` bank decode, read-only ROM, error pulse and CPU origins; `ctrl_split_start.S:10` copy/clear/reset layout; `CtrlMailbox` publication outputs at `milan_soc.py:2694`. Real split export and M2 crossing simulations pass. No latency, CDC or memory-alias regression was observed. |
| Robustness | `test_ctrl_memory.py:303`, `:473`, `:559`, `:729`: exact budget boundary, writable/NOBITS ROM, empty/short loads, truncation, overlaps, wrong shape, lone flags, full decoded-window holes, byte lanes and immediate post-error access. All standing controls and mutations pass. |
| Tests | `test_ctrl_memory.py:629`, `:928`: no firmware-data import dependency; baseline must pass before mutation grading. 123 successful checks, 44/44 mutants; stage-call removal fails the stage-size assertion, and shipping-library insertion fails its own library check. M2's 91 checks include seven caught controls. Prior mapping inputs are not the merged inputs, so F1 leaves this lens unclean. |
| Docs | Both architecture conflict sentences are preserved. All seven automatically merged overlap files retain both contributions. The docs, classifier, event and test-evidence gates pass. Both memory ledgers add up on their historical rows; F1 prevents treating their firmware measurement as current. |

| Check | Result / receipts |
|---|---|
| Merge reconstruction | `audit-before.log`, `audit-final.log`: `git merge-tree --write-tree ce10328c c6bd08c6` differs from the published tree at exactly `docs/ARCHITECTURE_HW_SW_SPLIT.md`. Removing its conflict markers while retaining both sides yields the exact published bytes. No other deviation from the automatic merge. |
| M8a source preservation | Planner, memory tests, linker, startup, fixture linker and OOC recipe have identical Git blobs to `ce10328c`. The firmware composition they consume does not. |
| All-fabric default | `export-comparison.log`, `export-digests.json`: both shipping configurations export at base and head; 18/18 emitted artifacts match per shape. Only output roots, generated Date lines and the single hierarchy comment are normalized. No RTL statement, initialization word, constraint or source-list entry is removed. Software make-input generation is suppressed equally on both sides; firmware is not compiled. |
| Memory tests | `ctrl-memory.log`, rc 0: 123 checks, 17 rules, 44 mutants, `RESULT: PASS`; includes the real SoC arm and genuinely linked probe. |
| M2 interaction | `retained-cdc.log`, rc 0: 91 checks, seven controls caught; all seven MAC/CSR arrays checked at two clock ratios for storage, handshake/order, capacity, reset and emitter behavior. Driver ran with `--jobs 8`. |
| Current largest split image | `export-head-split-8x8.log`, `split-inspection.log`, rc 0: five ROM and five SRAM banks, no BIOS ROM/SRAM, both regions 229,376 bytes, all eleven F-INT publication outputs present. This is elaboration/export, not boot or target execution. |
| Firmware links | Eight builds: four current and four previous-source controls, all rc 0. `fit-comparison.log` independently checks granule-rounding arithmetic and identical runtime archives. See F1. |
| Ledger arithmetic | `ledger.log`, rc 0: both published tables agree row by row; 124 before conditional release, 113 after it, 116 at the 56-tile limit, partial placement 130. The measured M2/M5/M6 replacement computes `37,957 + (200-34) + (600-121) + (600-418) = 38,784`, 744 over 38,040. These checks do not remeasure the mapped firmware debit. |
| Focused documentation/evidence gates | `checks.json` and individual logs: docs wording/self-test, style, paths, TOC, anchors, em-dash against c6bd08c6, Python idiom, module matrix, resource baseline, test-evidence check/self-test, diff whitespace and LiteX runner self-test pass. `docs-no-git.log` passes with its declared inventory-parity skip because Git is intentionally absent. |
| Classifier/events | `ci-scope.log` and `ci-scope-memory.log`: self-test passes; memory page classifies `true`. `ci-events-retry.log`: 1,821 contract items pass. `ci-events-selftest-retry.log`: 2,530 arms pass. Initial event invocations exited 2 because the docs interpreter lacked PyYAML; retry used the existing LiteX interpreter with PyYAML. Both attempts are retained; no failed attempt is called a pass. |

The local interpreter is the existing patched Python 3.14.7 stack, recorded in `environment.log`. This is not a fresh hosted Python 3.12 installation. The memory SoC child actively refuses firmware-data imports, and its real baseline and targeted mutations passed here. The CPU data tree was copied under unpublished `scratch/` before export, so generated CPU artifacts stayed isolated. The scoped simulator's 5.050 identity and wrapper hash were verified; no full simulation bank used it in this round.

The [published author evidence](https://github.com/kebag-logic/milan-fpga/tree/b68338bfdaf0535576335d7fae6a877c2bbe6d7d/review-evidence/640-m8a-r1) was downloaded selectively, with Git blob verification (`public-evidence/sources.json`). No handoff files were read. The [round-3 author receipt](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6107961867) and retained logs establish the earlier source results: builder `--require-elaboration --require-rv32` with one NOT RUN calibration arm, LiteX aggregate 7/7 and docs-parity 83/83. Those receipts concern `ce10328c` or the earlier named source heads, not execution of a manager source bank at `8ab2b539`. The reviewer did not run the full builder bank.

**Prior public findings: resolved or retained**

The [round-1 internal](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6104999232), [round-1 external](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6105008317), [round-2 internal](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6107064124), [round-2 external](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6107065061), [round-3 internal](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6112081957) and [round-3 external](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6112082969) findings were reconciled after the independent verdict and ledger were written.

| Prior ID / lenses | Disposition at this head | Evidence |
|---|---|---|
| R606-1-F1 / Robustness, Tests | RESOLVED, preserved | Writable initialised ROM is refused by rule; genuine link plant and removal mutant pass. |
| R606-1-F2, R607-1-F1 / Tests | RESOLVED, preserved | Budget edges, missing entry, NOBITS/LMA overlap, full-window holes, alias protection and post-error access run; corresponding mutants caught. |
| R606-1-F3, R607-1-S1 / Tests, Robustness | RESOLVED, preserved | Real main-path controls, lone flags, split export, absent BIOS and missing stage-call mutation run successfully. |
| R606-1-F4, R607-1-F2 / Docs | RESOLVED as reported | Both ruled-limit calculations give 116 / 5.5 and the lane row names 56. New stale source-input measurements are F1, not a recurrence of the old addition error. |
| R606-1-F5, R607-1-R2 / Docs | RESOLVED as attribution | 231 explicitly denotes ROM region LUT cells with decode/multiplexer, and 220 denotes Slice LUTs. Their historical counting basis is correct; current mapping applicability is F1. |
| R607-1-F3, R606-1-R2 / Docs | RESOLVED as historical attribution | PR body identifies its round-3 head, previous dev merge and seven-member aggregate. Current review-start notice identifies 8ab2b539. The present-tense dev sentence remains residue below. |
| R607-1-R1 / Docs | Original wording applied; current figures covered by F1 | The old mapped/planned distinction is explicit. Its 54.5 / 6 KiB values now require refresh after the firmware merge. |
| R607-1-S2, R606-1-S3 / Robustness, Tests | RESOLVED for reported truncations | Named header/segment/name truncation arms and mutants pass. Complete malformed-ELF validation is not claimed. |
| R606-2-F1 / Conformance, Tests, Docs | RESOLVED, preserved | Gate-read registry and classifier case are present; isolated self-test passes and page returns true. |
| R606-2-F2 / Tests, Docs | RESOLVED, preserved | Firmware-data imports refused; include hook and baseline-before-mutation rule remain; real SoC baseline passes, no ImportError credited as a kill. |
| R607-2-F1 / Conformance, RTL, Robustness, Tests, Docs | RESOLVED, preserved | Reset/load coverage runs before export; empty reset, short reset and missing data controls are refused, including linked and real-SoC controls. Four load-related mutants caught. |
| R606-2-F3 / Docs | RESOLVED as arithmetic | Both tables yield 124 + 6 = 130, 8.5 over the ceiling, and name the 56-tile basis. Changed firmware mapping applicability is separately F1. |
| R606-1-R1 / Docs | RESOLVED | Both exact sentences identify M2's unused +2 allowance. |

Optional findings remain optional and are not reported as fixed:

| Retained ID / severity / all lenses | Artifact, impact, optional outcome and verification |
|---|---|
| R606-2-S1 / SUGGESTION / Robustness | `ctrl_memory.py:264`, `ctrl_split_start.S:12`: orphan SRAM sections outside the startup copy/clear ranges are not checked. Optionally verify those ranges against linker symbols with orphan-section links. |
| R606-2-S2 / SUGGESTION / Robustness | `ctrl_memory.py:204`: invalid table indices or zero symbol-entry size can fail unnamed. Optionally add named malformed-table refusals and controls. |
| R606-2-S3 = R606-1-S1 / SUGGESTION / RTL, Robustness | `ctrl_split_start.S:10`: no trap vector installed here. Optional definition/installation and trap verification remain for the boot vehicle. |
| R606-2-S4 = R606-1-S2 / SUGGESTION / RTL, Robustness | `milan_soc.py:2753`, `ctrl_memory.py:316`: no separate bound on surplus initialization words. Optional assertion plus oversized-load control. |
| R606-2-S5 = R607-1-S3 / SUGGESTION, pre-existing / Tests, Docs | `ctrl_image_runtime.py:35`: runtime stack-protector handling remains separately assigned under 6105011666. The isolated compiler-flag workaround above does not fix or close it. |
| R606-3-S-a / SUGGESTION / Tests | `test_ctrl_memory.py:950`: first failing check need not match the mutant's declared property. BIOS duplicates still die through real module-name assertions. Optional per-property kill matching remains. |
| R606-3-S-b / SUGGESTION / Robustness | `ctrl_memory.py:246`: address coverage does not compare section-file bytes against conflicting segment-file bytes. Optional inconsistent-ELF control remains; genuine linked image comparison passes. |
| R606-3-S-c / SUGGESTION / Tests | `test_ctrl_memory.py:579`: objcopy naming assumes a compiler name containing gcc. Optional explicit tool selection/named refusal remains. |

**R607-3-R1 = R606-3-R1 - RESIDUE - Docs (retained)**

Artifact: PR #721 body, Status, second bullet. Evidence: it still says “The live `dev` tip is still `ac2c5e77`.” Historical evidence remains explicitly bound to round 3; current review-start metadata names the new head. Impact: stale present-tense wording only, with no change to a measurement, verdict or clause claim.

Exact fix: replace that sentence with “That merge used dev `ac2c5e77`; the current-dev merge candidate is validated separately at merge time.” Required outcome and verification: apply the sentence while preserving the historical evidence heads and results. The manager carries this to the residue checklist; it does not itself leave a lens unclean.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: R607-4-F1 | #640 ruling 6101485877; `ctrl_memory.py:264`; all four current/previous links; `SPLIT_CONTROL_MEMORY.md:146`; source mapping receipts | R607-4 | 8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d |
| RTL | CLEAN | `milan_soc.py:2732`, `:2762`, `:2694`; linker/startup; exact merge reconstruction; default exports; current largest split export; M2 crossing checks | R607-4 | 8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d |
| Robustness | CLEAN | `test_ctrl_memory.py:303`, `:473`, `:559`, `:729`; rule/refusal boundaries, linked/SoC controls, 44 mutants; retained crossing reset/order/depth | R607-4 | 8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d |
| Tests | UNCLEAN: R607-4-F1 | `test_ctrl_memory.py:629`, `:928`; 123 checks and 44 mutations; seven M2 controls; current/previous fit comparison; published historical mapping receipts | R607-4 | 8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d |
| Docs | UNCLEAN: R607-4-F1 | `SPLIT_CONTROL_MEMORY.md:146`, `MARK_II_AREA_PLAN.md:824`, `AREA_BUDGET.md:260`; all merged overlap docs; classifier/event/docs/evidence gates; PR body | R607-4 | 8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d |

**Limits, pending duties and packet**

No manager source bank ran at this exact head, and none is claimed or inferred. Source execution evidence consists of the explicitly dated author receipts plus this review's focused checks. The manager validates the final current-dev merge candidate with builder and native banks at the merge turn and links its receipts on the PR. Assigned source base and live dev are both `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`; their equality is not a completed validation run.

`hosted-checks.json` records the observation time and exact-head check metadata. Executed successes include the selector, lint, behavior checks, wire accountability, no-Git docs and three synthesis shards. Other jobs, including elaborate and docs-check, were still in progress; exhaustive/fast aggregate success is not inferred. The physical job was skipped. The manager owns hosted and local-replica acceptance; neither the host orchestrator nor its self-test was run here.

Physical calibration **NOT RUN**. Field skips and skipped hosted contexts are not hardware proof. No fresh OOC synthesis, integrated route, CPU boot, service timing, hardware run or complete parent/processor/gPTP/synthesis/builder bank was performed. Current fixture elaboration does not qualify the split release. M8a-2 still owns boot, service, wrapper/DDR3 removal and routed timing/fit.

The manager must arrange F1's correction and re-review, retain the optional findings and residue, finish both independent review rounds, accept exact-candidate gates, obtain merge authorization and prove post-merge containment. This review authorizes no merge and no closure of the umbrella issue.

All launched campaigns and builds had foreground parents that awaited their children. Independent tasks overlapped within the 16-job and 12 GB limits; no synthesis run overlapped a build. There were no source fixes, commits, pushes, GitHub writes, author contact or delegated agents. The review clone retains the exact head/tree. `audit-final.log` verifies every tracked blob's bytes and mode, the index, and the required processor/axis pins; the additionally initialized lwSRP pin and bytes are checked too. The external submodule remains uninitialized and unused. Ignored generated files from repository tests are not source changes; disposable checkouts, CPU files, runtime, builds and fixture images remain under unpublished `scratch/`.

Portable scripts: `audit_merge.py`, `ledger_check.py`, `run_checks.py`, `export_probe.py`, `run_exports.py`, `compare_exports.py`, `runtime_probe.py`, `run_fit.py`, `compare_fit.py`, `inspect_split.py`, `fetch_public_evidence.py`, `publish_receipts.py`. Commands and return codes are recorded alongside the logs. Run check/link scripts from the desired exact checkout. `run_fit.py PACKET PYTHON [PREFIX]` takes the runtime archives from `PACKET/scratch/runtime`; use `previous-` from an isolated ce10328c checkout with its pinned submodules. `runtime_probe.py` accepts the original runtime recipe's source/output arguments. Set `TMPDIR` under packet scratch, `PYTHONDONTWRITEBYTECODE=1`, and `MILAN_RV32_CC` to the compiler. `run_exports.py` expects an isolated copy of the CPU data package under `PACKET/scratch/cpu`; run it from an exact-head disposable checkout under scratch, since the builder generates its normal outputs there.

Receipts preserve command output with local path substitutions only: `$PACKET`, `$REVIEW_CLONE`, `$HOME`, `$TOOLS`. Original local outputs remain unpublished under scratch. The selected public author receipts retain their original verified bytes. `MANIFEST.sha256` is the publication allowlist, with packet-relative paths; no scratch file or prior reviewer report is listed.

R607-4 FINISHED
