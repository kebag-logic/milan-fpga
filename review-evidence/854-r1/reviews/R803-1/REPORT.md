[R803] NEGATIVE - exact head e87f2179f8d84b3eb89dea0148bb63d64319bc38

Review R803-1 (internal, cleared context) of issue #854 / PR #862. Head `e87f2179f8d84b3eb89dea0148bb63d64319bc38`, tree `39de20bda38e32990e0d7482773da768ef9cf54c`, one commit on `dev` `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36` (the live `dev` tip, so the source base is the current `dev`).

**Verdict: NEGATIVE.** The cause is one MINOR finding under `Docs`. The PR body's area section credits the drop counter with LUTs that moved inside the protocol processor, whose RTL this diff does not touch (R803-1-F1). The RTL, the tests and the mutation evidence are clean. The fix is a correction to the PR text only. No source change is needed.

## Reconstruction (public state only)

- **Authority.** AGENTS.md sections 3 and 5 to 8, and CONTRIBUTING.md. Issue #854 body: Defect, Where, Contract broken, Evidence, Required. The issue comments are the lane-open line, `[A756] TAKEN` and `[A756] REVIEW READY`. No maintainer or manager scope decision is recorded beyond these. PR #862 body. `docs/reference/REGISTER_MAP.md` `PP_DIAG` (`:2456`, `:2459-2469`). `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (`:568-610`). `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:76-85`.
- **Interface authority.** `third_party/verilog-axis/rtl/axis_fifo.v` at gitlink `48ff7a7e`: `:137` (depth rounded to a power of two), `:200-204`, `:217` (`s_axis_tready` is constant 1 under `FRAME_FIFO` and `DROP_WHEN_FULL`), `:261-302` (`overflow_reg` is a one-cycle pulse after the last beat of a dropped frame, for full or oversize).
- **Frozen Required items of #854.** (R1) count from the FIFO's own drop or overflow indication, not from `tready`; (R2) saturate at 255; (R3) a self-checking overflow test where frames lost equal the counter; (R4) a mutant that removes the count is caught.
- **Diff.** `git diff ac0a01e3..e87f2179`: 8 files, +396/-18. The files are `KL_pp_shadow.sv`, the `pp_shadow` harness (`sim_main.cpp`, `drops_probes.vlt`, `Makefile`, `drops_mutant.py`, `README.md`), `TESTING.md` and `REGISTER_MAP.md`. There is no submodule or processor change.
- **Prior public review findings.** I listed them only after my own pass and ledger. PR #862 has no review findings, only the two review-start lines. Issue #854 has no review findings. **Nothing to resolve or retain.** I did not read the concurrent external review.

## Focus checks

1. **Exactly once per lost kept frame, never for a kept or refused frame.**
   - `KL_pp_shadow.sv:866-874` sets `last_kept_r` on the last accepted beat of a frame. It is 1 only for `FW_BODY`, or for `FW_HEAD1 && accept_w`.
   - `drop_evt_w = ff_overflow_w & last_kept_r`.
   - `overflow_reg` is registered and rises in the cycle after a dropped frame's last beat (`axis_fifo.v:262,279-283`). `last_kept_r` updates on that same edge. A kept frame has at least two beats, so the next frame's last beat can only update `last_kept_r` after the overflow cycle has been sampled. Pairing is therefore exact.
   - With `DROP_WHEN_FULL`, `fw_ready_w` is constant 1 (`axis_fifo.v:217`), so the qualifier `fw_valid_w && fw_ready_w && fw_last_w` sees every last beat.
   - A refused frame ends at `FW_HEAD1` with `accept_w = 0`, so `last_kept_r = 0`. A one-beat runt ends at `FW_HEAD0`, so `last_kept_r = 0`.
   - The counter is `KL_pp_shadow.sv:1638`, and the `!= 8'hFF` guard holds it at 255.
   - Executed at the head: burst 108 offered, 77 handed out, 31 lost, count 31. Refused burst: 69 kept frames lost, count +69, 158 FIFO overflows. The 89 extra overflows came from refused frames and were not counted.
   - Two pre-existing checks now have a live counter to read: `sim_main.cpp:1939` ("no frame lost to a full FIFO") and `:1953`. They pass.
2. **Saturation.** Flood: 392 frames lost in all, the count reads 255, and it still reads 255 after 8,000 idle cycles. My extra arm `saturates-at-254` fails "DR the count saturates at 255" (got 0xFE), so the check is exact, not a ">= some value" check.
3. **The burst really overflows, and the expected count is derived.**
   - The tap has no ready signal: it is a pure monitor on `rx_axis_fabric` (`milan_datapath.sv`, `pp_shadow` port map near `:9700`).
   - The serializer pops one word only when idle (`KL_pp_shadow.sv:943`) and then sends one byte a cycle (`:953-972`). A full word therefore takes 9 cycles, against 1 beat a cycle in.
   - The harness computes `lost = offered - handed`. `handed` comes from the serializer's own byte stream, through read-only probes (`drops_probes.vlt`). It counts whole frames and checks they are a subsequence of the offered frames (`handed_in_order`). It never reads the counter.
   - The overflow strobes are counted directly: 158 in the refused burst.
   - My `fifo-2048` arm changes the FIFO geometry. The count still equals the independently derived loss (63/63 and 101/101), while the capacity check fails. The expectation therefore follows the DUT's real behaviour and is not a mirrored constant.
4. **The six drops-mutant arms.** `make drops-mutant` at the head gives rc 0, a clean control PASS, and 6 of 6 KILLED, each by its named check. The arms that fail 5 checks are count-removed, count-from-tready and diag-tied-off. counts-refused fails 1, misses-second-beat 2 and wraps 2.
   - Each plant is a real defect, not a cosmetic edit. `count-from-tready` is the original construction. `diag-tied-off` breaks the real `milan_datapath` to `milan_csr` wiring.
   - Three extra reviewer arms were also all KILLED: `refused-at-head1` (accept_w ignored: count +158 against an expected +69), `saturates-at-254`, and `fifo-2048`.
5. **Runts.**
   - `rx_mac_filter.sv:26,239-246` drops every frame whose first beat carries `tlast` (`runt_sof`). The tap sits on `rx_axis_fabric`, which is the filter's output when `RXFILT_P != 0` (`milan_datapath.sv:3294-3330`; the default is `RXFILT_P = 1` at `:309`).
   - Independently of the filter, a one-beat frame cannot be control traffic, because the EtherType is in beat 1. The RTL leaves it uncounted by construction (`last_kept_r` is 0 at `FW_HEAD0`).
   - None of R1 to R4 mentions runts. The narrowed scope still meets every Required item.
6. **Area.** I judged this from the author's public receipts and the repository records. I ran no implementation.
   - The `--shipping-selection` single-route judgement is a sanctioned mode (`PP_SHADOW_BASELINE_RECIPE.md:590`). ExtraPostPlacementOpt is the shipping directive (`syn/ooc/pp_resource_gate.py:133,359`). The receipt gives RESULT PASS with all four signoff corners above the floors and the route complete.
   - **The reported deltas are not attributable to this diff.** They compare an ExtraPostPlacementOpt route against record 15's selected AltSpreadLogic_high route: +106 LUT, +13 FF, -9 slices, -0.044 ns.
   - The repository already holds record 15's same-directive row (`docs/findings/234_PP_SHADOW_AREA_BASELINE.md:82`: 53,383 LUT, 54,837 FF, 15,848 slices, +0.112 ns). Against that row the head reads +151 LUT, +13 FF, -28 slices and +0.054 ns WNS.
   - Only the flip-flop share is cleanly the diff's: +9 FF in the tap's own logic, which is the 8-bit counter plus `last_kept_r`, and +1 FF for `ctl_fifo`'s `overflow_reg`.
   - The LUT share cannot be separated from implementation movement. The processor's own scope moved +27 LUT with no RTL change.
   - **Re-recording: not in this PR.** #854 does not require it. The recipe re-records acceptance from the full three-directive route set through `record --write`, and this head has one route. Record 15 still gates the head correctly within its tolerances. Whether to re-record at the merge candidate with the full set is a maintainer or manager decision, listed under pending duties. See R803-1-F1 for the PR text.
7. **Docs and register map against the RTL.**
   - `REGISTER_MAP.md:2466-2469` (the FIFO drops while holding `tready` high, the count comes from its own overflow indication, one per control frame lost, saturating at 255), the banner (`KL_pp_shadow.sv:70-75`), the port comment (`:752`), the `TESTING.md:748` row and the README section all match the RTL and the executed behaviour.
   - Two items are wording or optional: R803-1-F2 and R803-1-F3.
   - **Comment rule.** The added source lines in `hdl/` and `tb/` contain no bench lane label, lane name, review round, reviewer ID or issue-comment ID (`receipts/comment-rule-scan.txt`). **No new instance.**

## Findings

**R803-1-F1 — MINOR — lenses: `Docs` — PR #862 body, "Area" section, the sentence "Inside the wrapper the change accounts for +35 LUT and +10 FF (the counter and `last_kept_r`), and for +1 LUT and +1 FF in `ctl_fifo`".**
- **Evidence.**
  - The gate's `wrapper` scope is the `KL_pp_shadow` instance total, children included (`syn/ooc/pp_resource_gate.py:286-300`: the root row becomes `wrapper`). Record 15 shows wrapper 25,184 LUT against u_pp 24,464 + ctl_fifo 73 + u_nvm 654.
  - In the head's route hierarchy (public receipt `route/baseline_hierarchy.rpt:180-184`), the +35 LUT / +10 FF wrapper delta includes `u_pp` +27 LUT (`protocol_processor_top`, RTL unchanged by this diff) and `ctl_fifo` +1/+1.
  - The sentence therefore double-counts `ctl_fifo` and credits the processor's implementation movement to the counter. The tap's own logic moved about +8 LUT and +9 FF.
  - The whole-image deltas in the PR's table are cross-directive. The same-directive comparison already recorded in the repository (`docs/findings/234_PP_SHADOW_AREA_BASELINE.md:82`) gives +151 LUT, +13 FF, -28 slices, +0.054 ns, and the PR does not offer it.
  - Derivation: `receipts/area-derivation.txt`.
- **Impact.** A cold reviewer or the maintainer reads a measured area attribution that is wrong by 27 LUT and double-counts one scope. The like-for-like comparison that would show the change's real cost is missing. This is a figure and attribution claim, not pure wording, so it is not RESIDUE.
- **Required outcome.** The PR's area text:
  - presents the wrapper figure as the instance total, including `u_pp` +27 LUT;
  - states the tap's own share (+9 FF, which is the counter plus `last_kept_r`; the LUT share is about +8 or cannot be separated);
  - gives the same-directive comparison against record 15's ExtraPostPlacementOpt row, or says why it is not used.

  No source, test or record change.
- **Verification.** A reviewer re-reads the PR body against `check-route-1x1.log`, `route/baseline_hierarchy.rpt:180-184` and `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:80-83`.

**R803-1-F2 — RESIDUE — lenses: `Docs` — `tb/verilator/pp_shadow/README.md` (section "Control frames lost to a full FIFO (#854)", first bullet: "into a 4,096-byte FIFO that drains one byte a cycle").**
- **Evidence.** The serializer pops a word only when idle and then sends it a byte a cycle, so a full word drains in nine cycles (`KL_pp_shadow.sv:943,953-972`). `sim_main.cpp` says so correctly in its `kDrainCycles` comment.
- **Impact.** Wording only. No check, figure or verdict changes.
- **Exact fix.** Replace "that drains one byte a cycle" with "that drains eight bytes every nine cycles (one byte a cycle into the processor, one cycle to pop each word)".

**R803-1-F3 — SUGGESTION — lenses: `Robustness`, `Docs`, `Tests` — `hdl/milan/KL_pp_shadow.sv:752`, `docs/reference/REGISTER_MAP.md:2456`.**
- A control-classified frame longer than the 4,096-byte FIFO is also lost and counted (`axis_fifo.v:275`, `DROP_OVERSIZE_FRAME`). My reviewer probe offered one 4,200-byte ADP frame to an empty FIFO: 1 overflow, count 1, and the following 64-byte frame was handed out (`receipts/oversize-probe.log`).
- This matches R1, which says to count from the FIFO's own overflow indication. It is not a defect for any legal control frame, which all fit in 4,096 bytes.
- Optional: say "lost to a full FIFO, or longer than the FIFO" in the port comment and the register row, and grade the case in `[DR]`.

**R803-1-F4 — SUGGESTION — lenses: `Tests`, `Robustness`.**
- Neither of these is graded:
  - reset asserted during an overflow burst (only `last_kept_r`'s async reset and the FIFO's sync reset are involved; the reasoning at `KL_pp_shadow.sv:867-873` and `axis_fifo.v` is sound);
  - an `RXFILT_P = 0` build, where runts would reach the tap.
- Neither is required by #854. Both are optional legs.

## Executed at the exact head

Every build used Verilator 5.050 rev v5.050, wrapper sha256 `905795b9...`. Each run used a disposable copy of the clone at the head.

| Command | rc | Result | Receipt |
|---|---|---|---|
| `make -C tb/verilator/pp_shadow run` (base, vid73, crf, pending; `-j2`) | 0 | 730 / 730 / 770 / 317 checks, 0 failures; `[DR]` ran in base, vid73 and crf with 31/31, +69/+69 (158 overflows) and 392 lost / 255 | `receipts/pp_shadow-run.log` |
| `make -C tb/verilator/pp_shadow drops-mutant` | 0 | clean control PASS, 6 of 6 KILLED by named check | `receipts/drops-mutant.log` |
| reviewer `scripts/extra_arms.py` (3 arms) | 0 | refused-at-head1, saturates-at-254 and fifo-2048 all KILLED by named check | `receipts/extra-arms.log` |
| reviewer oversize probe (`scripts/oversize_probe.patch.txt` on a copy, `--drops-only`) | 0 | a 4,200-byte control frame: 1 overflow, count 1 | `receipts/oversize-probe.log` |
| `make -C tb/verilator/pp_shadow reboot-mutant` | 0 | 6 of 6 KILLED (regression for the changed `run()` entry point) | `receipts/reboot-mutant.log` |
| `make -C tb/verilator/pp_shadow pending-mutant` | 0 | late-mark mutant killed by K10 and K12; clean control passes | `receipts/pending-mutant.log` |
| `scripts/lint_rtl.py --check` | 0 | LINT GATE PASS, 89 <= ratchet 89 (no new violation) | `receipts/scripts_lint_rtl_py___check.log` |
| `scripts/docs_inventory.py --check` | 0 | OK | `receipts/scripts_docs_inventory_py___check.log` |
| `scripts/pp_srcs.py --check` | 0 | PASS | `receipts/scripts_pp_srcs_py___check.log` |
| `scripts/measure_test_evidence.py --check` | 0 | TEST-EVIDENCE RATCHET PASS | `receipts/scripts_measure_test_evidence_py___check.log` |
| `git diff --check ac0a01e3 HEAD` | 0 | no output | `receipts/comment-rule-scan.txt` |

An earlier attempt to run `lint_rtl.py` under `python3 -I` stopped at import (`lint_rtl_policy`), because isolated mode drops the script directory from the module path. That is a harness artefact, not a gate result. The rerun above, without `-I`, is the result.

**Hosted checks at the head** are inspected, not accepted (`receipts/hosted-checks-snapshot.txt`). At the time of the snapshot:
- completed with success: bdd-conformance, changes, docs-check-no-git, docs-gates-1, elaborate-gates 0, 2, 3 and 4, full-ci-gate, wire-accountability, Verilator shard 6/19;
- skipped: physical gPTP;
- still running or queued: the other Verilator shards, every Yosys shard, the firmware jobs, verilator-lint, docs-gates-0 and docs-gates-2.

The manager owns hosted and local-replica (act) acceptance.

**Clone integrity** (`receipts/clone-integrity.txt`): HEAD and tree are exact, the index equals the HEAD tree, there is no tracked or untracked change, and all six gitlinks are as recorded. I removed the `__pycache__` written by my lint run. Every probe ran in a disposable copy.

## Reviewer-owned completion ledger (R803-1)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #854 R1-R4 against `KL_pp_shadow.sv:857-874,915,1638`, `axis_fifo.v:217,261-302`, `milan_csr.sv:2278-2279`; executed `[DR]` counts | R803-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |
| RTL | CLEAN | `KL_pp_shadow.sv:792-874` (classify FSM, `last_kept_r` timing against `overflow_reg`), `:1631-1644` (saturating counter), `:943,953-972` (serializer); `rx_mac_filter.sv:239-246`; `milan_datapath.sv:3294-3330,9791`; lint ratchet 89/89 | R803-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |
| Robustness | CLEAN (F3, F4 are SUGGESTION) | refused frames at a full FIFO (158 overflows / 69 counted), runts (filter plus construction), saturation and hold, oversize probe, reset reasoning | R803-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |
| Tests | CLEAN (F3, F4 are SUGGESTION) | `sim_main.cpp:1956-2111` (`[DR]`), `drops_probes.vlt`, `drops_mutant.py` 6/6, reviewer arms 3/3, full suite in 4 legs, reboot and pending mutants | R803-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |
| Docs | **UNCLEAN** (F1 MINOR open; F2 RESIDUE) | `REGISTER_MAP.md:2456,2466-2469`, `TESTING.md:748`, `pp_shadow/README.md` #854 section, banner and port comment, PR #862 body (area section), comment-rule scan of the added lines | R803-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |

## Real limits

- I ran no Vivado, Yosys or OOC build. The area judgement rests on the author's public route receipts at `d4c77810` and on the repository's record 15. The `ooc-1x1` and `ooc-8x8` endpoints were not measured at this head by anyone.
- I ran no full parent, PP, gPTP or builder bank. The full suite sweep, firmware, builder, behave and docs-workflow results are the author's published receipts, which I did not re-execute.
- Not simulated: reset during a burst; an `RXFILT_P = 0` build; hardware. Physical calibration NOT RUN. Field skips are not hardware proof.
- The machine was heavily shared during the runs. That affects wall time only, not results.

## Pending manager duties

- Current-dev merge-candidate validation: builder and native banks at the merge turn, and the act replica.
- Exact-head hosted acceptance. Many contexts were still running at the time of my snapshot.
- The external review.
- After F1 is fixed in the PR text, an internal re-review of the `Docs` lens at the then-current head. If the head changes, the lenses whose scope changed are re-covered.
- A decision on re-recording `syn/ooc/pp_resource_baseline.json` from a full three-directive route set at the merge candidate, or leaving record 15 standing.
- Carry R803-1-F2 to the residue checklist.
- Maintainer authorization for the merge.

R803-1 FINISHED
