[R738] NEGATIVE - exact head ee1c0be0b99f0131eb10908a19f080299aa0cbb8

External independent review R738-1, issue #665 / PR #812. Tree `48581b5296086a3ba87d35b76d6e986ad9a15dc3`. Reviewed all seven commits and all 17 changed files against `f4c9ad4f06f185378fd2646298aab51dd108e86f`, targeting `dev-soft-core`.

One MINOR remains: generated timing reports omit their clock provenance. No flash-write escape, restore-order defect, or exceeded F1 step bound was found in the reviewed implementation and evidence. This verdict does not reject option (c) or reinstate a total capture bound.

Authorities and scope

- [Frozen S4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6493622258): generated target flash map, real state owners, journal guard, target boot cases, D3 order and existing co-simulation/capture gates.
- [Owner's option (c), 2026-10-29](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6504551000): F1 steps bounded by T_svc; capture CPU and elapsed time recorded without a separate bound; D5's 24.5 ms stays on the current writer.
- [Approved budget](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6495692075), FR_NFR 3.4.1, REQUIREMENTS section 1 and REQ-VER-04; `SAVED_STATE_MATERIALIZATION.md` 8.1/8.6; `ctrl_nvm/README.md` Boot and Write-back; `ARCHITECTURE_HW_SW_SPLIT.md` section 2.
- [Public clock direction](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6508235352), consistent with this review's explicit clock criterion: product split CPU 50 MHz, bus 100 MHz; timing figures identify their CPU clock.
- [Immutable source evidence](https://github.com/kebag-logic/milan-fpga/tree/970c3e41d037c8e0ce58af7241a05078218c28ac/review-evidence/665s4-r1). The historical `author-r1/STOP-COMMENT.md` is superseded on the capture-bound question by option (c). The revised plan is `author/receipts/plan/plan-s4-section.md`.

Finding

**R738-F1 | MINOR | Conformance, Tests, Docs | `tb/verilator/nvm_split_target/run.py:118-142,189-191`; generated `table.md` and `results.json` | Generated timing evidence drops the clock used for its figures.**

Authority/evidence: the explicit review criterion requires every timing figure to state its CPU clock; the public direction above distinguishes the 50 MHz product from a labelled 100 MHz experiment. REQ-VER-04 requires generated artifacts and documentation to satisfy policy. `run_cases` has `cpu_hz`/`sys_hz`, but neither is retained in its results. `table` accepts only results and the shape label. Both persisted outputs therefore lose those clocks. `probe_evidence.py` invokes the actual generator on the published 8x8 results and reproduces the omission in `generated-timing-table.md`: 103.227 ms CPU, 1,638.061 ms elapsed, and per-phase verdicts, without a clock. The JSON likewise has no clock field. `target_selftest.py:124-139` checks report wording but not clock provenance. The architecture summary at `docs/ARCHITECTURE_HW_SW_SPLIT.md:223` and the PR's F1 timing table also lack a local clock label; the target README correctly states 50 MHz near its beginning.

Impact: standalone exported results cannot identify whether their conversion and T_svc grading used the product or an experimental clock. This matters at the shared service-budget harness boundary. The inspected figures agree numerically with 50 MHz; this finding does not allege measurement at 100 MHz.

Required outcome: retain measured `cpu_hz` and `sys_hz` in machine-readable results and render the actual clocks beside generated tables. Label the corresponding architecture/PR figures. Use the recorded build clocks, not an unconditional 50 MHz string. Check missing/incorrect provenance. This requires generated-output/code changes, not solely prose wording, so it is MINOR under the assigned residue rule.

Verification: regenerate both points with 50,000,000 Hz CPU and 100,000,000 Hz bus; use a synthetic differently clocked input to prove rendering follows the input. Keep existing timing boundaries and D5 removal controls passing. Re-review the corrected head.

Lens evidence

- **Conformance:** examined `gen_flash_port.py:92-364`, `ctrl_srp_image.py:55-89`, `split_soc.py:93-108,353-378,442-500`, `target_cases.py:43-237`, and `target_grade.py:146-379` against the authorities above. Generated headers precede stand-ins; timer clock equality, journal geometry and image-slot overlaps are checked. Independent placement probes reject changes to all nine used register addresses and the flash window. The existing 10 ms value is conservatively below the approved family bounds; its acknowledged sequencing with S2b is not a relaxation. R738-F1 leaves this lens unclean.
- **[R738] PASS RTL - `split_soc.py:329-378,442-500`, `sim_main.cpp:258-339`, `milan_soc.py:167-172,3124`, and both target shape configurations.** The command master is in the product-shaped LiteSPI bank, timer0 counts the 100 MHz system clock, and the CPU uses the configured 50 MHz Milan clock. Observers report committed entries/returns without driving protocol state. No product HDL or gitlink changes occur. The actual owner chain is `ctrl_aecp_image.c:102-104`, `acmp_nvm.c`, `aecp_nvm.c`, and `nvm_store.c:316-368,420-428`; binding restore precedes D3, settle precedes names, and rollback ownership remains separate.
- **[R738] PASS Robustness - `nvm_flash_litespi.c:188-237`, generator rules, `target_cases.py:54-116,218-237`, `target_grade.py:281-379`, and published invalid-slot/guard traces.** The subtraction-based journal guard avoids unsigned end-wrap; page and erase-block checks remain intact. Absent/wrong-version slots apply no saved state; the newer torn slot leaves the accepted older state. All seven outside-journal calls are counted; only the permitted erase reaches the device. Guard removal reaches the independent device rejection. The focused 1x1 suite additionally exercised rollback, read faults, timeouts, power cuts and boundary behavior. Zero simulated media waits remain a limit.
- **Tests:** examined all new graders/self-tests and shared budget changes. Independently ran the three portable self-tests, current-writer capture gate, record-space gate, focused 1x1 store suite, map probes and public-log rechecks. Both apply reorders fail the intended rule; the real slow step fails at 30.2139 ms at 50 MHz. Removing D5's check in a disposable imported copy makes the unchanged current-writer gate exit 1 with `OFF timing limit was ignored`. R738-F1 leaves report-provenance coverage unclean.
- **Docs:** examined every documentation delta, the PR body and public scope/evidence trail, including the revised plan and historical STOP. F1 CPU/elapsed timing, no capture-wide bound, retained current-writer D5 bound, fixture-only composition and physical limits are distinguished. Source-comment additions contain no new prohibited review identity or bench-lane label. R738-F1 remains open.

Execution receipts

| Evidence | Result |
|---|---|
| Reviewer `flash-map-selftest.log` | 33 checks, zero failures |
| Reviewer `target-selftest.log` | 41 checks, including 12 grader mutants, zero failures |
| Reviewer `budget-selftest.log` | Zero failures |
| Reviewer `current-capture-gate.log` | Census, clocks, both timing arms and receipt agree |
| Reviewer `record-space.log` | Zero findings across five configurations |
| Reviewer `nvm-1x1.log` | 93 tests pass, required RV32 compilation passes; host timer model 100 MHz, not target CPU timing |
| Reviewer `map-placement.log` | Correct map accepted; nine moved registers and old window placement refused |
| Reviewer `probe-evidence.log` | 8x8 raw trace checks pass; reorders/slow step caught; D5 removal rejected; clock omission reproduced |
| Author exact-head short/long gate summaries | 97 + 11 gates recorded at this head; author executions, not reviewer reruns |
| Author target results | Both points pass; 50 MHz CPU, 100 MHz bus: capture 27.223 ms CPU / 534.905 ms elapsed at 1x1; 103.227 ms / 1,638.061 ms at 8x8; maximum step 2.639 ms |
| Author current-writer 8x8 on/off measurements | 50 MHz CPU, 100 MHz bus: maxima 13.86328 / 13.68956 ms, below D5's 24.5 ms |
| Author co-simulation/campaign/coverage receipts | 465 checks, 39/39 co-simulation mutants; 1,006 firmware plants, no escape; coverage PASS |

`public-inputs.json` records immutable URLs and published hashes. Probes and raw outputs accompany this report. Independent portable checks ran concurrently within one foreground process; the compiled suite used `--jobs 16`. Disposable files stayed in the packet's `scratch/`. No source file was edited.

Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: R738-F1 | Generator, target cases/grader, owner decisions, timing outputs | R738-1 applied; no clean covering round | ee1c0be0b99f0131eb10908a19f080299aa0cbb8 |
| RTL | CLEAN | `split_soc.py`, `sim_main.cpp`, `milan_soc.py`, adapters, shape clocks, no-HDL diff | R738-1 | ee1c0be0b99f0131eb10908a19f080299aa0cbb8 |
| Robustness | CLEAN | Journal guard/geometry, invalid-slot/guard traces, focused store suite | R738-1 | ee1c0be0b99f0131eb10908a19f080299aa0cbb8 |
| Tests | UNCLEAN: R738-F1 | Self-tests, target traces, D5 removal, report checks, public receipts | R738-1 applied; no clean covering round | ee1c0be0b99f0131eb10908a19f080299aa0cbb8 |
| Docs | UNCLEAN: R738-F1 | All documentation deltas, PR, public scope and evidence | R738-1 applied; no clean covering round | ee1c0be0b99f0131eb10908a19f080299aa0cbb8 |

Limits and pending manager duties

Target traces were inspected/rechecked, not regenerated by a fresh CPU build here. The public packet omits the large commit log and journal binaries, retaining hashes and commit-step CSV; full independent commit replay was therefore not performed. Focused host/portable probes are the reviewer's own executions. No full parent, processor, gPTP, synthesis, builder or target bank is claimed. Physical calibration was NOT RUN; field skips and zero-wait models supply no hardware proof.

There is no manager source bank at this head. Hosted/local workflow acceptance remains the manager's duty; this report claims neither executed hosted jobs nor acceptance from skipped contexts. The manager must validate the final current-dev merge candidate and publish its builder/native receipts. Source base: `f4c9ad4f`; supplied live dev: `1e80128f0a467b58bf884b7d9bf62e013a2fb141`. This source review does not validate that future merge result.

The shared `ctrl_srp_image.py`, `ctrl_configs.py`, and service-budget files retain existing options/defaults in this delta, adding generated-map support and passive observations. S2b's per-family budget and clock work must survive semantic integration. No S2b merge was tested here. Fix/re-review R738-F1, obtain independent reviews, reconcile exact-head coverage after changes, finish candidate and hosted/local acceptance, then follow maintainer merge authorization and post-merge containment. Issue #665 is broader than this S4 PR.

`checkout-integrity.log` proves head/tree, all tracked raw blobs, executable modes, complete index, and the five populated submodule pins/contents. The `external` gitlink remains unchanged and unpopulated. No restoration was necessary. No GitHub write, commit, push or merge was performed.

Prior public finding reconciliation: checked after this independent verdict and ledger were written. PR #812 has no submitted reviews and no review threads. Its two public comments are review-start notices, not findings. There are therefore no earlier PR findings to resolve or retain. No other reviewer's report was read. The earlier author STOP is reconciled by the owner's option (c), as recorded above.

R738-1 FINISHED
