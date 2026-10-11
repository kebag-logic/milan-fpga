[R599] NEGATIVE - exact head 988ec7f653d0a21e0f7b40b03b8c74155d8962cf

# R599-1: external review of PR #722 (issue #640, Mark II lane M5, plan L8)

- Round: R599-1, external cleared-context reviewer, started at https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105204716.
- Head: `988ec7f653d0a21e0f7b40b03b8c74155d8962cf`, tree `8c80b6e209e642e4e345d0d7c0cda0b70702057d`. Source base: dev `e8454e2751d05b02ee8e5a571857589ab358ab86`. The measured product commit is `1abe18eb`, and `git diff 1abe18eb 988ec7f6 -- hdl` is empty.
- Diff reviewed: `git diff e8454e27..988ec7f6`, 10 files, +4,484 / -43, 7 one-line commits.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs (all five).
- Verdict: **NEGATIVE**. Two MINOR findings are open: F1 (Docs, Conformance) and F2 (Docs). RTL, Robustness and Tests are CLEAN at this head. The read-path restructuring itself is functionally sound: I found no RTL, robustness or test defect.

## Reconstruction (public state only)

- `AGENTS.md`, `CONTRIBUTING.md` (sections 1, 3 and 6), `docs/README.md`.
- Issue #640 body (frozen acceptance) and these public comments: the M5 lane assignment 6098404907 (scope, proof list and target of 600 LUT, range 400-1,000), the executor's TAKEN 6098441921 and REVIEW READY 6104904445.
- `REQUIREMENTS.md` REQ-CSR-01 to 04. `docs/design/MARK_II_AREA_PLAN.md` (L8, the ledger, the cumulative tables). `docs/design/AREA_BUDGET.md` (resource gate policy: the 0.25 ns timing fall and the 0.03 ns WNS floor). `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` ("Integrated measurements"). `syn/ooc/pp_resource_gate.py` and `pp_resource_baseline.json` (endpoints and scope definitions). `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` (the per-stream basis L8 cites).
- Public evidence tree `review-evidence/640-m5-r1` at `648503cf`: `author/HANDOFF.md` (sha256 `f45a1b97...`) and `author/PR-BODY.md` (sha256 `b4010338...`, equal to the live PR body).
- No other reviewer's report was read before this verdict and ledger were written. When this round started, the PR held no public review findings. R598-1 posted during this round, and it is read only in the addendum at the end.

## What I executed (exact head bytes; receipts listed in MANIFEST.sha256)

All simulation used the scoped Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`). The CSR, `tcam_csr`, lockstep and mutant runs used a `git archive` export of the head, with the three pinned submodule trees at their gitlinks. `milan_dp_mclk`, `milan_dp ax1x1`, Yosys and the docs and ratchet gates ran in the clone, and every build output was removed afterwards.

| Run | Result | Receipt |
|---|---|---|
| CSR suite, `MAKEFLAGS=w make -C tb/verilator/csr` (6 legacy legs, `lock1`, `lock8`, reset bits, `lock_mutants.py`) | rc 0. 1,815 checks, 0 failures. lock1 5/5: 340,861 cycles, 28,167 random-traffic reads, 0 mismatching cycles. lock8 5/5: 374,265 cycles, 22,750 reads, 0 mismatching cycles. `lock_mutants.py` 8/8 (control plus 7 planted defects, each failing its named check). Figures identical to the author's. | `receipts/csr_suite.log`, `.rc` |
| Reviewer-planted defects, `r599_mutants.py` (independent of `lock_mutants.py`) | 5 caught, 2 survived; both survivors are equivalent (table below) | `receipts/r599_mutants.log`, `receipts/r599_mutant_runs/r0..r6.run.log` (r0 = R1 ... r6 = R7) |
| `make -C tb/verilator/milan_dp_mclk` | rc 0, 31/31. Mutant 13 ("the read-window terms missing") caught at this head. | `receipts/milan_dp_mclk.log` |
| `make -C tb/verilator/milan_dp ax1x1` (the shipping Alinx 1x1 integration leg) | rc 0, 233 checks, 0 failures | `receipts/milan_dp_ax1x1.log` |
| `make -C tb/verilator/tcam_csr` | rc 0, 2 checks, 0 failures | `receipts/tcam_csr.log` |
| `python3 scripts/lint_rtl.py --check` (pinned Verilator on PATH) | rc 0, `LINT GATE: PASS (90 <= ratchet 90)`, no `milan_csr` finding | `receipts/lint_rtl_check.log` |
| `syn/yosys/run.sh --top milan_csr` (Yosys 0.66, sv2v 0.0.13) | rc 0, `[PASS] milan_csr cells=69288`; tied-input and tap-purity gates PASS | `receipts/yosys_milan_csr.log` |
| `python3 scripts/measure_test_evidence.py --check` | rc 0, ratchet PASS (69 <= 77; 0 unexplained DUT-source readers) | `receipts/measure_test_evidence_check.log` |
| `python3 scripts/docs_check.py` | rc 0, 0 findings | `receipts/docs_check.log` |
| Added-line U+2014 scan and `git diff --check e8454e27..HEAD` | 0 added em dashes; diff-check rc 0 | inline, this report |
| Clone integrity after every probe, `verify_clone.sh` | rc 0, CLONE VERIFIED. Head, tree, index equal to the tree (all stage 0), every tracked file's bytes and mode, no hidden index flags, no leftovers. `protocol-processor`, `gptp-processor` and `third_party/verilog-axis` sit at their pins and are clean. | `receipts/verify_clone.log` |
| Hosted checks at the exact head, read-only snapshot taken 2026-10-11T04:14Z | `rtl-fast`, `verilator-lint`, `elaborate`, `firmware-unit`, `docs-check`, `bdd-conformance`, `yosys-elaboration`, Yosys shards 0-3 and Verilator shards 0, 2 and 3: success. Verilator shards 1/5 and 4/5: still in progress. Physical gPTP: skipped (nightly/manual; not hardware proof). | `receipts/hosted_checks_988ec7f6.txt` |

Reviewer-planted defects (each one exact text replacement in a copy of `hdl/common/csr/milan_csr.sv`, built through the suite Makefile's own `lock1`/`lock8` recipe):

| # | Defect | Leg | Outcome |
|---|---|---|---|
| R1 | shadow word served under a live claim (`shadow_rd_w` drops `!live_hit`) | lock1 | CAUGHT: reset-values, decode, lockstep |
| R2 | stage-1 gate `(strm_hit \|\| rd_in_window)` removed | lock1 | Survived, as predicted. In today's map every live arm at or above 0x800 has a `rd_in_window` term (checked by hand: `milan_csr.sv:2609-2629` against every `A_*` localparam in 0x7F8-0x93F), so the change is unobservable by construction. The gate's only guard is `milan_dp_mclk` mutant 13, which I ran and which is caught at this head. The author states this limit in the HANDOFF (open item 7). |
| R3 | out-of-range SNAP leaves the CNT kinds unchanged | lock1 | CAUGHT: snapshot-freshness, lockstep |
| R4 | extra talker context does not pre-POISON the kinds | lock8 | CAUGHT: decode, snapshot-coherence, lockstep |
| R5 | CNT kind read one word off (`snap_kind_r[coff]`) | lock1 | CAUGHT: decode, snapshot-coherence, snapshot-freshness, lockstep |
| R6 | listener burst arm elaborated only above 8 listeners | lock8 | CAUGHT: decode, snapshot-coherence, snapshot-freshness, lockstep |
| R7 | `shadow_qq` loads every cycle, not only on `rd_pend` | lock1 | Survived; my prediction was wrong. Proven equivalent: `shadow_qq` is consumed only on `rd_pend2`, exactly one edge after the `rd_pend` load (`milan_csr.sv:1158-1159, 2636-2660`), so a later reload can never reach `r_data`. This is not a harness gap. |

## Findings

### F1 MINOR: Docs, Conformance

- **Location:** `docs/design/MARK_II_AREA_PLAN.md:1023`, "#649's 211 LUTs per stream do not reproduce; out of context the block grows about 12 per stream."
- **Authority and evidence:** The assignment (issue #640 comment 6098404907, Proof) requires the measured saving to be reported "against the plan's estimate, honestly". L8 (`MARK_II_AREA_PLAN.md:535-536`) builds that estimate on #649's per-stream model.
  - #649's 211 LUT/stream (`docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:650-657`) is the `milan_csr` hierarchy inside the `milan_datapath` synthesis. It is fitted over N = 1, 2 and 4 of one shape line (RMS 119), and #649 excludes the tracked 8x8 configuration from that line as a different audio shape (`:647`).
  - The lane's 12 LUT/stream is a different scope. It is `milan_csr` alone with every input free, measured between `ax7101_1x1_tdm8` and `ax7101_8x8`, the base block (2,955 -> 3,038; HANDOFF section 1).
  - The lane's own closer model, the integration proxy that the HANDOFF calls "the closer model of the shipping instance", grows about 62 LUT/stream at base (2,058 -> 2,494). The M5 block itself grows about 49 alone and about 56 in the proxy (HANDOFF section 4: 2,515 -> 2,859; 1,903 -> 2,295).
  - So the sentence picks the least comparable and smallest of the lane's four slopes, describes the pre-M5 block in the M5 ledger entry, and states a non-reproduction that no like-for-like measurement shows. The in-datapath per-stream figure was not re-measured: the 8x8 integrated synthesis was stopped.
- **Impact:** The authoritative ledger tells later lanes and the week-4 re-measure that the plan's per-stream basis is wrong by a factor of about 18. The scope evidence does not support that. 8x8 and per-stream estimates built on the ledger would inherit the understatement.
- **Required outcome:** The sentence states each figure with its scope, or makes no reproduction claim. For example: "#649 measured 211 LUTs per stream inside the datapath synthesis; that scope was not re-measured here. Out of context the base block grows about 12 per stream alone and about 62 in the integration proxy (M5: about 49 and 56)."
- **Verification:** Re-read `MARK_II_AREA_PLAN.md` at the new head against HANDOFF sections 1 and 4 and #649 `:647-657`; the docs gates (`docs_check.py`, `check_em_dash.py --base <merge-base>`, `gen_toc.py --check`) stay rc 0.

### F2 MINOR: Docs

- **Location:** PR #722 body, Description, "Measured" list, bullet **Saving against the plan**: "The routed whole image moved -690 LUT, but about -686 of that is in untouched blocks (`u_pp`, the processor wrapper) and is not credited." The same "-686" appears in `review-evidence/640-m5-r1/author/HANDOFF.md` section 7 item 3.
- **Authority and evidence:**
  - The gate's `wrapper` scope is the hierarchical root that contains `u_pp`. `syn/ooc/pp_resource_gate.py:253-270` names the root `wrapper` and keys children relative to it. In the recorded route-1x1 scopes (`syn/ooc/pp_resource_baseline.json`), `wrapper` holds 23,345 LUT ≈ `u_pp` 22,794 + `u_nvm` 486 + `ctl_fifo` 71.
  - The HANDOFF's -344 (`u_pp`) and -342 (wrapper) are therefore nested, not additive. The untouched-block movement is about -690 - (-121) = -569: the wrapper's -342 (almost all of it in `u_pp`), plus about -227 elsewhere.
  - As written, "-686 of -690 in untouched blocks", together with the credited `csr` -121, exceeds the whole-image delta. This is a wrong figure in the review evidence, not wording only.
- **Impact:** A cold reviewer cannot reconcile the attribution, and roughly 227 LUTs of movement in other untouched blocks are hidden. The credited saving (`csr` scope -121/-127) is unaffected, and the plan text (`MARK_II_AREA_PLAN.md:1016`, "mostly the processor wrapper") is correct.
- **Required outcome:** The PR body's attribution states non-overlapping figures. For example: "-121 in `csr` (credited), -342 in the processor wrapper (nearly all in `u_pp`), about -227 in other untouched blocks." Alternatively it drops the sum.
- **Verification:** Read the corrected PR body and check that its parts sum to -690 against the scope tree in `pp_resource_baseline.json`.

### RESIDUE (wording only; does not affect the verdict or lens coverage)

- **RES-1**, `hdl/common/csr/milan_csr.sv:1066-1067`. A comment-only, netlist-neutral defect. The banner above `rd_pend2` still says "the final four-way select into r_data runs a cycle later on rd_pend2". Stage 2 is now an OR (`:2660`), and the next comment (`:1076-1077`) says so. Exact fix: replace "and the final four-way select into r_data runs a cycle later on rd_pend2" with "and stage 2 (an OR of the two stage-1 words since lane M5 of #640) loads r_data a cycle later on rd_pend2". The same stale phrase "the old four-way select's shadow arm" at `:2633` is accurate as history and needs no change.
- **RES-2**, `docs/design/MARK_II_AREA_PLAN.md:538`. "M5 measured 121 LUTs routed and 127 post-synthesis in its scope" reads as the block's size. Exact fix: "M5 saved 121 LUTs routed and 127 post-synthesis in its scope".
- **RES-3**, PR #722 body, `tb/verilator/csr/` table row. "the dev `e8454e27` block byte for byte" should be "the dev `e8454e27` block byte for byte apart from the module name" (`gen_lockstep.py:21-23`; `diff` shows only line 97, `module milan_csr_ref #(`).

### SUGGESTION (optional)

- **S1**, the route evidence (PR body "Measured"; recipe `PP_SHADOW_BASELINE_RECIPE.md:142-181`). Only the primary placement directive was routed at base and head. The 0.202 ns WNS fall uses about 80 % of the 0.25 ns timing-fall tolerance, and its worst path is in the untouched DMA bridge, so it is most likely placement variation. Running the recipe's two alternate directives (`AltSpreadLogic_high`, `ExtraTimingOpt`) from the same synthesis checkpoints would show that before later lanes inherit the reduced margin. The gate does not require this.

## Per-lens results (clean lenses in the findings format)

- [R599] UNCLEAN Conformance: F1. All other conformance items hold:
  - Identical function, including addresses, widths, reset values, access semantics and AXI-Lite latency. The lockstep compares every output, including `s_axi_rvalid` and `s_axi_rdata`, on every cycle at both shipping parameter sets (`tb/verilator/csr/gen_lockstep.py:100-131`, `sim_lock.cpp:270-324`). Reproduced with 0 mismatching cycles. Latency is three cycles after AR (`milan_csr.sv:1158-1161`).
  - `docs/reference/REGISTER_MAP.md` is unchanged in the diff.
  - Snapshot coherence and freshness (REQ-CSR-02): harness-derived expectations pass.
  - The four required planted-defect classes are present and caught, with three more.
  - Gate arithmetic: +0.097 ns >= max(0.03 floor, 0.299 - 0.25 = 0.049) per `AREA_BUDGET.md:396-405`. No record re-recorded (D7).
  - Both placements: `milan_csr` has no placement input, and `--ctrl-mailbox` only adds the SoC mailbox (`sw/litex/milan_soc.py:3326-3327`; `dp_params` at `:921-940` carry no placement term).
- [R599] PASS RTL. Artifacts: `hdl/common/csr/milan_csr.sv:1078, 2289-2298, 2300-2505, 2526-2600, 2609-2664, 2923-3053` at `988ec7f6`.
  - Checked by hand: `live_mux` is 0 wherever `live_hit` is 0 (`:2304-2305, 2492-2493`; the PP override `:2501-2504` sets both). No `read_mux` case arm or earlier range lies in 0x800-0x86F: every `A_*` localparam was enumerated, and `pp_read` decodes the full address at `:2253-2282`. So the new stage 1 plus the zeroed shadow equals the old four-way select arm for arm.
  - SNAP kinds: each kind is written in the same cycle and branch as the old word, and the `N_LISTENERS_P > 1` guard is unreachable-only at N = 1 because `win_in_range_w` (`:1106-1107`) admits listener index 0 alone.
  - Kind value 3 falls to `default` (zero) and is never written.
  - Declarations precede first use (#193): `strm_mux`/`strm_hit` `:2292-2293`, `snap_kind_r`/`SK_*` `:1463-1469`, `shadow_rd_w` `:2635`.
  - No declaration with an initialiser was moved: `rst_epoch_r` `:2297` is unchanged.
  - Single clock domain, no CDC touched.
  - Lint ratchet PASS, Yosys synthesis of `milan_csr` PASS. The routed checkpoint is not re-examined here; see limits.
- [R599] PASS Robustness. Artifacts: `tb/verilator/csr/sim_lock.cpp:435-457` (reset with a read in flight, then a full sweep), `:603-631` (out-of-range SNAP wipe, talker then listener then talker SNAP order), `:647-676` (random AXI traffic, random inputs on every free port, resets every 20,011 cycles, engine model on and off). Reviewer defects R3, R4 and R6 (config-dependent kind paths at N = 1 and N = 8) were all caught. The slow engine-read path (`milan_csr.sv:2661-2662`) and its `rds_done_w` handshake are unchanged and exercised by the decode sweeps under in-range selections.
- [R599] PASS Tests. Artifacts:
  - `tb/verilator/csr/sim_lock.cpp`, `gen_lockstep.py`, `lock_mutants.py`, `Makefile:64-163` and `README.md:81-96` at `988ec7f6`, plus receipts `csr_suite.log` and `r599_mutants.log`.
  - Each named check fails for its planted defect (author 7/7, re-run). The reviewer's five non-equivalent defects are caught. Both survivors are shown equivalent; R2's only guard, `milan_dp_mclk` mutant 13, is caught at this head.
  - The oracle is the frozen base block, checked by SHA-256 with the name read back (`gen_lockstep.py:89-97`). The top is generated from the port list, with a short parse refused (`:64-86`). The coherence and freshness expectations come from the harness, not from the reference.
  - The `lockstep` check fails when random traffic completes no read (`sim_lock.cpp:713-718`).
  - Existing regressions stay green: CSR legacy legs, `tcam_csr`, `milan_dp_mclk` and `milan_dp ax1x1`. `measure_test_evidence.py --check` passes with the new reader disposition (`scripts/measure_test_evidence_readers.py:174-178`).
- [R599] UNCLEAN Docs: F1 and F2 (plus RES-1 to RES-3, which do not affect coverage). Clean otherwise:
  - `hdl/common/csr/doc/milan_csr.md:147-169` matches the RTL: signals `snap_shadow_r`/`snap_kind_r`, processes `read_mux`, `strm_read_mux`, `shadow_out_reg` and `read_data_reg`, three cycles after AR.
  - `tb/verilator/csr/README.md` describes the legs and the five checks accurately.
  - The ledger's figures (`MARK_II_AREA_PLAN.md:1004-1030`) match HANDOFF sections 4 and 5. The saving is stated below the 600 (400-1,000) estimate, only the `csr` scope is credited, and the cumulative tables keep the planning figure explicitly.
  - `docs_check.py` rc 0; no added em dash.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #640 assignment 6098404907; `milan_csr.sv` read path; lockstep legs (all outputs, every cycle); `REGISTER_MAP.md` unchanged; `AREA_BUDGET.md:389-405`; HANDOFF section 5 gate figures; `milan_soc.py:921-940, 3326` | R599-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |
| RTL | CLEAN | `hdl/common/csr/milan_csr.sv:1078-1164, 2289-2664, 2923-3053`; lint ratchet; Yosys `milan_csr` synthesis | R599-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |
| Robustness | CLEAN | `sim_lock.cpp` reset, out-of-range, ordering and random-reset phases; reviewer defects R3, R4 and R6; slow-read path unchanged | R599-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |
| Tests | CLEAN | `tb/verilator/csr/{sim_lock.cpp,gen_lockstep.py,lock_mutants.py,Makefile,README.md}`; CSR suite 1,815/0; author defects 7/7; reviewer defects 5 caught, 2 proven equivalent; `milan_dp_mclk` 31/31; `milan_dp ax1x1` 233/0; `tcam_csr` 2/0; `measure_test_evidence.py --check` | R599-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |
| Docs | UNCLEAN (F1, F2) | `docs/design/MARK_II_AREA_PLAN.md:538, 992-1030`; `hdl/common/csr/doc/milan_csr.md`; `tb/verilator/csr/README.md`; PR #722 body; `review-evidence/640-m5-r1/author/*`; `docs_check.py` | R599-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |

## Real limits of this round

- No route, synthesis or resource-gate run was reproduced. The integrated figures (49,577 / +0.097 ns against 50,267 / +0.299 ns, gate PASS, `csr` scope 3,037 -> 2,916) and the OOC figures are the author's published receipts, read for arithmetic and consistency only. The 8x8 integrated synthesis was not completed by the author (disclosed), and the recipe's alternate-directive implementations were not run (S1).
- The split-placement route is not measured (M0s step-1 STOP). I checked parity only by source reading, not by elaboration.
- Not run by me: the full `milan_dp` suite (only the shipping `ax1x1` leg), `milan_dp_render`, `capture_coherence`, `follow_ring`, `pp_shadow`, `milan_dp_gptp`, firmware host tests, builder, `behave` register-map checks, `xvlog_gate.py`, `check_em_dash.py` and `gen_toc.py` (the pinned cmark-gfm binding is not installed here). For these I rely on the author's receipts and on the hosted `docs-check`, `firmware-unit`, `bdd-conformance` and `elaborate` successes at this head.
- Hosted Verilator shards 1/5 and 4/5 were still in progress at the snapshot; I did not inspect the shard-to-suite mapping.
- No manager source bank exists at this exact head, and none is claimed or inferred. Physical calibration was NOT RUN; skipped field and physical contexts are not hardware proof.

## Pending manager duties

- Hosted acceptance at this head: Verilator shards 1/5 and 4/5; manager-owned act replication.
- At the merge turn, the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks, and publication of those receipts.
- Carry RES-1 to RES-3 to the residue checklist.
- The executor's decision item: the saving is below the estimate, and the cumulative tables keep 600 until the week-4 re-measure.
- The 8x8 integrated synthesis and post-merge boot readback on the bench (plan L8), which are outside this desk review.

## Addendum: other public findings on this PR (read after the verdict and ledger above were written)

R598-1 (https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105288411, NEGATIVE at this same head) was posted during this round. Nothing in it changes the verdict or ledger above.

- **R598-1-F1** (MINOR, Docs: the PR body's "-686" double-counts the nested `wrapper` and `u_pp` scopes). **Retained.** It is the same defect as this round's F2, found independently, with the same arithmetic (-121 + -342 + about -227 = -690). It cannot be resolved at this head.
- **R598-1-S1** (SUGGESTION, Docs: name what the measured L8 figure does to the partial-central scenario, about 38,436 against 38,040). I agree it is optional. The ledger discloses that its tables carry the planning figure, and this round raises no finding on it.
- **R598-1 observations.** The stage-1 gate is unobservable in the lockstep and guarded by `milan_dp_mclk` mutant 13; this agrees with R2 above. The reference copy's em dashes are verbatim base bytes outside the Markdown gate's scope; I agree.
- **Difference in lens coverage.** R598-1 covers Conformance clean. This round holds Conformance and Docs UNCLEAN on F1 (`MARK_II_AREA_PLAN.md:1023`, the #649 per-stream non-reproduction claim stated across non-comparable scopes), which R598-1 does not raise. F1 stays open under this round's ledger.

R599-1 FINISHED
