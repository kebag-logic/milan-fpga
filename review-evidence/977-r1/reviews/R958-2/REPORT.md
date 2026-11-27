[R958] NEGATIVE - exact head 25ff0632c4ed312d57cad78783474308c92dd21f

All five lenses were applied. The prior blocking findings are closed at this head. One new MINOR documentation finding remains open, so Docs is UNCLEAN and the verdict is NEGATIVE. Conformance, RTL, Robustness and Tests are CLEAN within the scope below. Three wording-residue items and one suggestion are recorded separately.

Reviewed tree: `a5fa7c04b11c14c919f821f0075888a0633532c9`. This is a source-head review of [PR #993](https://github.com/kebag-logic/milan-fpga/pull/993), not approval of a future merge candidate. No source files were changed.

**Scope and authority.** I reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, [issue #977](https://github.com/kebag-logic/milan-fpga/issues/977) and its public decisions, REQUIREMENTS.md, FR_NFR.md §3.4.1, MAILBOX_SPLIT.md and the relevant SPLIT_CONTROL_MEMORY.md contracts before the independent diff pass. I examined the requested source-base diff and history, concentrating on `095995243bc354b8a41755f3fdfae343511cc668..25ff0632c4ed312d57cad78783474308c92dd21f` and dependencies changed by that delta. The fetched dev-soft-core tip was `0b5940237e8de8bd5912db87e5e036a78f59b5a6`; the PR's recorded base was `71bad8c0b973a15ee5f993a74f893ff7ff947c33`. Neither replaces final current-dev candidate validation.

The operative scope includes the November 27 [population ruling](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7210763364), [delivery/S14 ruling](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7212897415), [alone-record/base/SETTLE ruling](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7216582862), [0.77 load ceiling](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7213594113), and [80 ms TRANSMIT decision](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7217388999), together with the earlier registration and notice decisions. The original slice-only acceptance is amended by the alone-record ruling; 80 ms is authorized. No acceptance criterion was changed by this review.

The independent pass and a preliminary verdict/ledger were written before reading prior findings. I then reconciled both [internal round 1](https://github.com/kebag-logic/milan-fpga/pull/993#issuecomment-7210480305) and [external round 1](https://github.com/kebag-logic/milan-fpga/pull/993#issuecomment-7210572249). Unchanged code retains its earlier assessment only where the new population, scheduling, pin and measurement dependencies do not affect it.

**Prior findings, checked at their causes.**

| Prior finding | Disposition | Cause-level evidence at this head |
|---|---|---|
| R958-1-F1, MAJOR, all five lenses: mixed population undercharged | CLOSED | `srp_mbx.h:166` states V=4/9. `srp_mbx.c:327,565` counts bound sinks and limits retained interests to the remaining population; `rx_charge` at 1013–1053 charges V in vectors and the conservative length fallback. `srp_mbx.cpp:2601` reaches real registrations for bound plus kept Talkers. Both native shape runs pass; final shard-3 mutations remove the population controls and fail intended assertions. The campaign includes swap and more-than-eight-Message cases. |
| R958-1-F2, MINOR, Docs: obsolete fixture ledger numbers | CLOSED | Harness `README.md:425` now gives 62.5/58.5 for current fixture entries and identifies older values as history. F1 below concerns the separate platform entry changed by this delta. |
| R958-1-F3, RESIDUE, Docs: comment labels | CLOSED at prior sites | Earlier replacements are present. New delta instances are R958-2-R1. |
| R957-1-F1, MAJOR, Conformance/RTL/Robustness/Tests: zero-value LeaveAll stopped charge traversal | CLOSED | `srp_mbx.c:1049` recognizes only a zero VectorHeader as EndMark. Zero-value LeaveAll advances over FirstValue and continues. `srp_mbx.cpp:473,523` tests that shape, vectors carrying values and fallback. Native charge tests pass at both shapes; final shard 3 records the charge reversals caught. |
| R957-1-F2, MAJOR, Conformance/Docs: unpublished lwSRP pin | CLOSED | PR #22 is merged at exact gitlink `e27b34c9231abaa862bdb73f807238b330aa4c51`, fetchable and used by the native builds. tsn-c-stack PR #41 is merged at current gitlink `5a07d9b7d87298f04b15aa28f0304ec88b0aef81`. See `public-state.json`. |
| R957-1-F3, MINOR, Tests: missing alone-admission guards | CLOSED | `test_port_loop.cpp:1603–1643` separates centisecond and tier-1 inhibition; `loop_step_mutants.py:61,65` independently removes each condition. Final shard 1 lines 1649/1651 report both caught. My 53-test native loop run passes. |
| R957-1-F4, MINOR, Docs: missing public ADP decision | CLOSED | The STOP and [delegated decision](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7210516620) are public. Full #1015 integration and #1017/#1019 from dev-soft-core are present. The previously reported additional merge conflict is resolved in this source tree. |
| R957-1-R1, RESIDUE, Docs: comment labels | CLOSED at prior sites | New delta instances are R958-2-R1. |
| R957-1-R2, RESIDUE, Docs: stale PR title | CLOSED | Live title describes the registration/drain work; the unrelated old title is gone. |

**R958-2-F1 — MINOR — Docs — `docs/design/SPLIT_CONTROL_MEMORY.md:172`: stale platform refusal threshold.**

Authority/evidence: the active table at line 140 and `sw/litex/ctrl_memory.py:397` set `platform-8x8-one-interface` to 61.0 RAMB36. The new delivery paragraph records its accepted 147,712-byte ROM. The unqualified sentence at line 172 nevertheless says each image is refused half a tile past its entry, ending with platform thresholds “65.5 and 61.0”. The accepted image occupies 61.0; its half-tile-past refusal threshold is 61.5. The final ledger receipt reports that 61.0 image PASS.

Impact: the authoritative document gives a contradictory numerical acceptance boundary. This changes a figure and therefore is MINOR, not wording residue. No resource-overflow defect is inferred.

Required outcome: change the current platform thresholds to **65.5 and 61.5**. If retaining the old sentence as history, explicitly bind it to the older 60.5 entry and separately state the current threshold.

Verification: compare with `LEDGERED`, existing memory-gate boundary cases and the final platform ledger. A prose correction does not require rebuilding unchanged images. Docs remains UNCLEAN until corrected and re-reviewed.

**R958-2-R1 — RESIDUE — Docs — new source comments contain review/bench labels.**

Authority/evidence: the owner's comment rule requires behavior, reason and issue/requirement references without review rounds or bench labels. The delta adds “round 9's STOP” at these artifacts:

- `sw/firmware/ctrl/app/ctrl_app.h:107`
- `sw/firmware/ctrl/app/ctrl_app_srp.c:143`
- `sw/firmware/ctrl/plat/ctrl_split_hot.txt:17`
- `sw/firmware/ctrl/test/srp_binding.hpp:235,376`
- `sw/firmware/ctrl/test/srp_deliver_mutants.py:3`
- `sw/firmware/ctrl/test/test_plat_sinks.cpp:1626`
- `tb/verilator/ctrl_service_budget/load_grade.py:363`
- `tb/verilator/ctrl_service_budget/register_window.py:247,287`

The merged delta also adds comment prefixes `B25`, `B27`, `B26` at `sw/firmware/ctrl/test/test_plat_boot.cpp:1353,1372,1410`.

Impact: comment wording only. Exact fix: replace “ruling on round 9's STOP” with “delivery-bound ruling of 2026-11-27”, preserving #977 and item/clause references; where the date is already adjacent, use “delivery-bound ruling” without repeating it. Remove those three B-number comment prefixes while retaining behavior and requirement references. Test identifiers and diagnostics need not change. Verification: inspect added comments/docstrings against the reviewed base. This residue does not unclean a lens.

**R958-2-R2 — RESIDUE — Docs — PR #993 Pins row and `author-r10/PR-BODY.md:77`: incorrect explanation of unchanged lwSRP images.**

Authority/evidence: “the `LWSRP_LEAN_COPY` 0 restore arm, which no image builds” is incorrect. `sw/firmware/ctrl/srp/srp_entity.py:26–30` enables the option only for the two one-interface shapes; others use the zero default at `third_party/lwSRP/src/core/mrp_mad.c:99`. Two-interface images build that arm. The independently compared public hash lists still establish 80/80 ELF identity across the pin move.

Impact: correcting the explanation changes no source, image, hash, measurement, test outcome or conformance claim. Exact fix: replace “which no image builds” with “used by the default-option shapes; the published ELF comparisons cover those images too”. Verification: check option generation/defaults and the same 80-path maps. No new build is needed for that prose correction.

**R958-2-R3 — RESIDUE — Docs — obsolete pending-owner and reviewer-assignment prose.**

Artifacts: PR #993 Status, TRANSMIT row, outstanding-items/checklist and reviewer placeholders; `docs/design/SPLIT_CONTROL_MEMORY.md:2548`; published final `author-r10/REVIEW-READY.md:3,37`, `PR-BODY.md:7,18,49,50,62,141,150`, `HANDOFF-r10d.md:6`.

Authority/evidence: owner comment 7217388999 approves 80 ms; public review-start comments identify the review roles. Impact: procedural wording only; the numerical bound and executable acceptance are unchanged. Exact fix in current prose: “80 ms approved by the owner's 2026-11-27 decision”, linked to that decision, and replace reviewer placeholders with public assignments. Preserve historical packet bytes; append a dated supersession note to its published index. Verification: compare the current prose with those public decisions. No lens is unclean solely for this residue.

**R958-2-S1 — SUGGESTION — Conformance, Tests, Docs — `load_grade.py:5–9,550–589`, `rows_tiers.py:487`, SPLIT_CONTROL_MEMORY.md:2548: explain both accounting measures together.**

Authority/evidence: the approved ruling retains bounded delivery inside the 350 µs base. Load deliberately excludes a pass's own base; response rows charge it per counted ordinary pass. My in-memory probe (`probe_load.py`, `load-base-probe.txt`) changes only the base: 300→350 µs leaves source-term load at 0.7661365 while raising TRANSMIT from 77.89→79.49 ms. All 32 counted passes receive the additional 50 µs. At an impossible 10,000 µs base, load remains unchanged but no row solution exists under the search limit. Load alone is not a schedulability verdict or measured total utilization.

Impact: the two baseline-subtracted additions without this explanation invite treating 0.780 as a measured ceiling violation, or 0.768 as a proven alternative utilization. Neither follows. Suggested outcome: append the accounting explanation and retain a small sensitivity check showing base growth detected by the row gate. Verification: the probe and existing flip checks reproduce the distinction. Optional; no lens is unclean.

**Judgment on the requested open points.**

1. **Deferred binding load: accepted under the approved partition.** Neither dearest-base nor median-base subtraction is an extra load term to add mechanically. Delivery remains in the polls' base after explicit heavy items are removed, bounded at 350 µs and charged per ordinary pass in response rows. Its final reported maximum is 33,565 cycles, below 35,000. `ctrl_app_srp.c:134–205` bounds work, alternates binding/loss when both are owed, retains pending work and makes no binding change in an alone-record pass. The base increase is visible in the independently reproduced 79.49 ms row. SETTLE separately appears in the opening-row term and prescribed registration cost. No extra 0.0019 or 0.0136 is required by this model. This accepts the public model/ruling, not a claim that measured total utilization is 0.766.
2. **61.0 RAMB36: authorized debt.** The [November 15 owner rule](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6892332745) permits the measured next half tile as S14 debt while retaining device-fit/timing obligations. 147,712−147,456 = 256 bytes; 60.5→61.0 follows it. Final ledger and route receipts support the image. F1 concerns only the written refusal threshold.
3. **Logged slips: superseded, not erased.** The initial 8x8 route/link refusal at 60.5 and first TX-figure comparison's missing platform image are not passes. I used the later e59cf6ea route, corrected `tx80-elf-identity-e59cf6ea.txt`, and final-head identity receipt. Earlier D6 shape selection, mutation sites, coverage and memory-expectation failures have final passing receipts and D7 coverage. Removal of an intermediate scratch copy before its removal note is a disclosed process slip, not evidence of success. No unresolved product failure was found in these superseded attempts; their disclosure remains public.

**Independent lens evidence.**

[R958] PASS Conformance — `srp_mbx.c:1013`, `srp_mbx.h:166`, `ctrl_app_srp.c:134`, `register_window.py:238`, FR_NFR §3.4.1 and public rulings — V, zero-value LeaveAll traversal, fallback, delivery limits, alone-record exception and unchanged SRP unit agree with amended scope. Load/row gates use authorized 0.77/80 ms. S14 at `test_plat_sinks.cpp:1562,1628` matches the all-bound/one-unbound ruling; its former stronger expectation was changed by public decision.

[R958] PASS RTL — `ctrl_loop.c/.h`, `ctrl_app_srp.c:134–205`, `srp_mbx.c:327,565,1013`, shape generation, hot/linker lists, `ctrl_memory.py:396`, pinned interfaces — checked ordering, turn/index bounds, pending progression, reset/count updates, charge widths and resource/timing effects. No HDL, CDC or constraint implementation changes in this delta. Protocol/gPTP pins are unchanged. #1015 and dev-soft-core integrations were examined at touched application/build interfaces. Physical evidence is limited to published route summaries and ELF identity.

[R958] PASS Robustness — `srp_mbx.cpp:473,2601`, `srp_binding.hpp:381–517`, `test_port_loop.cpp:1556`, `register_window.py` and mutation definitions — malformed/truncated/vector-end cases, LeaveAll, more than eight Messages, mixed populations, reset/rebind/reclaim, repeated requests, pending loss and alternating delivery were checked. The default/two-interface paths are represented in final published firmware gates. Both one-interface native SRP tests use the real pinned participant.

[R958] PASS Tests — changed assertions and mutations, campaign groups, `slice_grade.py`, `rows_grade.py`, `rows_tiers.py`, load/flip gates and final receipts — tests address prior causes and new delivery branches. Standalone kept/bound refusals are distinguished from paired acceptance. I executed 53 loop tests, 24 charge/early-Talker tests at each shape, and 20 binding tests at 8x8/1if: **121 tests, all pass**. Load check/self-test, both held-point flip checks, shape and hot-list checks pass. Native builds ran concurrently, four compiler jobs each; model checks ran concurrently. No full bank was run.

[R958] MINOR Docs — SPLIT_CONTROL_MEMORY.md:172 — F1 leaves Docs UNCLEAN. Examined changed firmware/interface READMEs, harness README, FR_NFR, SUBMODULES, diagram/pin documentation, comments, public scope and evidence provenance. Prior population/README/publication findings close; all new wording residue is listed above.

**Evidence verification.** The [immutable public packet](https://github.com/kebag-logic/milan-fpga/tree/da2acce94a7d069b16930642124a2fff7a2e9586/review-evidence/977-r1) supplies the author receipts. Paths below are relative to `author-r10/receipts/`. `check_packet.py` verified **216** author/author-r10/author-text files against `published_sha256`, without reading the packet's reviews directory (`packet-integrity.json`). The evidence commit is **unsigned**: public metadata reports `verified=false`, `reason=unsigned` (`packet-signature.json`). Hash integrity is established; a cryptographic packet signature is not. This is a provenance limit, not a new acceptance gate.

`audit_receipts.py` parses the hash lists, campaign CSV and route summaries independently; see `receipt-audit.json`.

| Claim | Verified receipt result |
|---|---|
| Pin moves preserve images | `pins/elf-identity.txt`: three maps of exactly 80 paths, identical across lwSRP 73007b48→e27b34c9 and tsn-c-stack 0f72ca69→5a07d9b7. Both merged pins are public; local tsn tree comparison is empty. |
| 80 ms preserves images | Corrected `r10d/tx80-elf-identity-e59cf6ea.txt`: 80/80 equal with 70468e2a applied/reverted, including the re-ledgered platform image. Hold-off remains 8 cs. |
| Final head matches measurements | `r10d/elf-identity-final.txt`: 25ff0632/e59cf6ea maps each contain 80 identical paths. Routed platform-image identifiers match named final ELF hashes. This verifies published receipts, not an independent rebuild of 80 binaries. |
| Campaign completion | `r10d/meas/groups-e59cf6ea.csv`: 578 standalone runs, 570 rc=0 and eight expected kept/bound pairing refusals. Four paired reruns supply eight group rows, all rc=0. Completed campaign passes; “all 578 exit zero” would be inaccurate. No statement exceedance is recorded. |
| Longest passes | CSV maxima 155,676 cycles = 1.55676 ms and 193,036 = 1.93036 ms, both below 200,000 cycles/2 ms. Paired maxima are lower. |
| Polls and slices | Bases 19,847/33,565 cycles against 22,500/35,000; walks 3,260/14,108 against 3,500/15,000. SRP pass-to-record maxima 87,826/171,622 fit max(slice, alone), 95,000/184,000. Build/round maxima fit their statements. |
| Registration/SETTLE | `r10d/meas/regcost-*.txt`, `settle-every-log.txt`: 17,578/17,921 cycles per Talker yield 185/190 µs by the margin/rounding rule. SETTLE statements 105/425 µs; the latter covers 40,049 cycles. |
| Model | My load/flip receipts reproduce loads 0.524/0.766, TRANSMIT 33.89/79.49 ms; 1x1 ACMP 29.51, txL 48.08, last notice 133.91 ms. These are model bounds, not measured longest passes. |
| Routes | `r10d/routes/route-1x1-1if-c63e9d58.txt`, `route-8x8-1if-e59cf6ea.txt`: four corners each meet WNS≥+0.030 ns, WHS≥0; worst WNS +0.159/+0.092 ns, worst WHS +0.036 ns, zero routing errors. Complete-design BRAM 82/100.5 fits 135 tiles. |
| Final gates | `r10d/gates/final/`: four firmware shards identify 25ff0632 and end PASS/rc=0; coverage 40 files PASS; memory/ledger/hot checks pass. Self-tests report 28 load, 628 flip, 25 shape, 33 kept controls. Twin and final documentation receipts are published. These are author source-head receipts. |

**Reviewer-owned completion ledger.** CLEAN refers to the examined source delta and unaffected earlier assessments, not fulfillment of merge duties.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Public rulings; FR_NFR §3.4.1; population/charge; delivery/alone; registering groups; load/row probe | R958-2 | 25ff0632c4ed312d57cad78783474308c92dd21f |
| RTL | CLEAN | Loop/app/SRP delta; shape/hot/linker; memory; pinned interfaces; integrations; route/ELF receipts | R958-2 | 25ff0632c4ed312d57cad78783474308c92dd21f |
| Robustness | CLEAN | LeaveAll/fallback/mixed population; reset/reclaim; L23b; D1–D7; new groups/plants | R958-2 | 25ff0632c4ed312d57cad78783474308c92dd21f |
| Tests | CLEAN | 121 native tests; model checks/probe; assertions/mutations; reconciled campaign/four-shard/identity receipts | R958-2 | 25ff0632c4ed312d57cad78783474308c92dd21f |
| Docs | UNCLEAN — F1 | SPLIT_CONTROL_MEMORY.md:172/current ledger; changed authority/interface/README/pin docs; comments; public evidence | R958-2 applied; no clean covering round | 25ff0632c4ed312d57cad78783474308c92dd21f |

**Limits and manager duties.** Timing was reconciled from public summaries/CSV; full CPU traces, all rebuilt ELFs and raw implementation databases were not replayed. No full parent/protocol/gPTP/builder/synthesis bank, hardware or calibration run was performed. Physical calibration is **NOT RUN**; field skips are not hardware proof. Exact-head public workflow/check-runs queries returned empty lists (`public-state.json`): no executed hosted validation is established, and no skipped context is represented as a pass. Hosted/local-replica acceptance remains the manager's responsibility.

There is **no manager source bank at this head**, and none is inferred. The manager must obtain correction/re-review of F1, carry R1–R3 to the residue checklist, finish the independent-review bar, validate the actual current-dev merge candidate with builder/native banks and publish receipts. Supplied live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`; the merge turn must use its then-current required base. Candidate validation, protected contexts, explicit merge authorization, post-merge containment and issue/project completion remain outstanding. This review made no GitHub write or merge.

**Reproduction and integrity.** Supply the checkout path to `check_packet.py`, `run_native.py`, `run_checks.py`, `probe_load.py`, `audit_checkout.py`; run `audit_receipts.py` after packet extraction. Disposable builds/extractions remain under this packet's `scratch/`. The native driver uses at most 16 compiler jobs. Every driver was invoked in the foreground and waited for children. The initial hot check used a wrong script path and exited 2 before execution; `hot-check-initial.log/.rc` retains it. The corrected check exits 0.

`checkout-audit.json` verifies **3,373 tracked blobs** across root and five initialized dependencies, their modes, each index against HEAD, and every gitlink oid. The `external` gitlink remains uninitialized and unchanged. All audited worktrees are clean. No task remains running. Only REPORT.md and files listed in MANIFEST.sha256 are publishable; scratch is excluded.

R958-2 FINISHED
