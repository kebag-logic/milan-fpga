[R687] NEGATIVE - exact head 5f0d5bf931c87f3e6e3b813e042c64a61f9cb13e

# R687-1: internal cleared-context review of PR #778 (issue #774)

- Head under review: `5f0d5bf931c87f3e6e3b813e042c64a61f9cb13e`, tree `97c252045acefc7dec86d0615f23fe05f1c13852`.
- Source base and live dev: `a032c6d6e3775f145349d5a495c1e1ad12294936`. Diff reviewed: `git diff a032c6d6..5f0d5bf9`, three commits (`e70a99ba` the change, `124adf7e` the regenerated module matrix, `5f0d5bf9` three table rows rewritten without em dashes).
- Submodule gitlinks are unchanged by the PR. The processor stays at `93fb0b2d`, which carries PR #194's per-source `cfg_tspec_max_frame_i[N_STREAM_OUT_P*16-1:0]` (`protocol-processor/hdl/top/protocol_processor_top.sv:303`, consumed per source at `:2701`). gPTP stays at `55680bff`.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md (sections 1, 3 and 6), docs/README.md, the issue #774 body, the assignment (issuecomment-6379902807), TAKEN and REVIEW READY, the PR #778 body, and the processor's integrator guide section 6 and `docs/architecture/10_srp_engine.md:136`. Then the diff, then the author's published receipts at `0b7d22cc`, then the hosted check runs at this head.
- Prior public review findings on PR #778: none. There are no PR reviews, no inline comments, and the only PR comment is the review-start notice. Nothing to resolve or retain.

Verdict: NEGATIVE. One BLOCKER and two MINORs are open, so RTL, Tests and Docs are unclean. Conformance and Robustness are covered clean.

## Findings

### F1 BLOCKER - Tests, RTL - `hdl/ieee1722/crf/KL_crf_tx.sv:233` against `tests/steps/crf_class_a_steps.py:59-80` - the rtl-fast `bdd-conformance` gate fails at this head, caused by this PR

- **Authority / evidence:**
  - AGENTS.md section 7 requires a successful `rtl-fast` verdict on the current PR head. The Tests lens requires that existing regressions remain green.
  - At this head the hosted `bdd-conformance` job fails 1 of 406 scenarios: `features/crf_sr_class_a.feature:48 The tag replaces pad, it does not resize the frame`, `ASSERT FAILED: no localparam int found` (run 40080623205, job 120833220222; `receipts/bdd/hosted-head-bdd-conformance-job-120833220222.log`). The same job passed at dev `a032c6d6` (job 120672347517; `receipts/bdd/hosted-dev-a032c6d6-checks.tsv`).
  - Reproduced locally at the exact head: `cd tests && behave --no-capture -f plain` gives rc=1, "405 scenarios passed, 1 failed" (`receipts/bdd/behave-head-5f0d5bf9.log`, `.rc`).
  - Cause: the PR rewrote `CRF_PDU_C` as `CRF_HDR_C + int'(CRF_DLEN_C)`. The step's resolver strips only sized casts such as `16'(` (`crf_class_a_steps.py:72`), so it reads `int` as a localparam name. Its docstring also states that nothing beyond `+ - * /` and parentheses should be hiding in a frame-size constant.
  - `scripts/bdd_frame_bytes_probe.py` applies the step's own resolver at both commits (`receipts/bdd/frame_bytes_probe.log`): dev gives `CRF_PDU_C = 28` and `FRAME_BYTES = 60`; head gives `ASSERT FAILED: no localparam int found` for both constants.
  - The author's gate list (REVIEW READY, PR "How to validate") does not include `bdd-conformance` or an `rtl-fast` replica. The PR's "GREEN" status therefore does not cover this gate.
- **Impact:**
  - `rtl-fast` is red at the head; the hosted run shows `rtl-fast` cancelled after `bdd-conformance` failed. The merge bar cannot be met.
  - The specification-facing regression that holds the CRF frame at one 60-octet shape (IEEE 802.1Q 9.5, tag replaces pad) no longer reads the RTL at all. A later change that resized the frame would therefore not be caught by it.
- **Required outcome:**
  - At a new head, the scenario passes against the real RTL arithmetic. Either write the AVTPDU length so the existing resolver reads it, still derived from the header and crf_data_length with no new literal, or teach the resolver the `int'(...)` cast with a fixture that proves it still refuses non-arithmetic.
  - The scenario must not be weakened or skipped.
  - `bdd-conformance` and `rtl-fast` evidence for that head is published.
- **Verification:**
  - `cd tests && behave --no-capture -f plain` rc 0.
  - `python3 bdd_frame_bytes_probe.py <repo> <new-head>` prints `FRAME_BYTES = 60`.
  - Hosted or replica `bdd-conformance` succeeds at the new exact head.
  - `obj_crflic` and `obj_tspec8` still report 29 for the CRF output.

### F2 MINOR - Docs - `docs/traceability/MODULE_MATRIX.md:67,98,173` (generated from `docs/traceability/ieee8021q.md:154`) - the matrix now lists the Milan version "1.2" as a clause of three modules

- **Authority / evidence:**
  - The generator's `clause_refs()` (`docs/traceability/gen_module_matrix.py:239,252`) keeps the first three tokens matching `§?\d+\.\d+...` from every traceability row.
  - The PR's SRP-10 row adds "(Milan v1.2 4.3.3.2 Table 4.4)" after `35.2.2.8.4` and `802.3`. "1.2" out of "v1.2" therefore becomes the third token, and the real clause `4.3.3.2` falls outside the cap (`receipts/docs/matrix_clause_probe.log`).
  - The regenerated matrix now shows `1.2` for `KL_aaf_packetizer`, `KL_crf_tx` and `milan_datapath`. On dev no module listed `1.2`.
  - `milan_datapath`'s four displayed clauses drop `802.1` in favour of `1.2`.
  - `gen_module_matrix.py --check` still passes (`receipts/docs/gen_module_matrix_check.log`), because the matrix faithfully reflects the bad extraction.
- **Impact:** a generated traceability artifact attributes a non-clause to three modules and hides a real one. This is a clause claim in a generated artifact, so it is not RESIDUE.
- **Required outcome:** the matrix lists only clause identifiers for these rows, with no `1.2` from a version string. Either reword the row so its version token is not read as a clause, or make the generator skip version strings and add a generator control for it. Then regenerate.
- **Verification:**
  - `python3 matrix_clause_probe.py <repo> <new-head>` shows no `1.2` among the kept tokens.
  - `python3 docs/traceability/gen_module_matrix.py --check` rc 0.
  - The three matrix rows carry no `1.2`.

### F3 MINOR - Tests - `ci/image/command-table.json` (`scripts["tb/verilator/milan_dp/crflic_mutants.py"].sha256`, `commands`) - this PR adds two inventory refusals of its own on top of dev's pre-existing one

- **Authority / evidence:**
  - `docs/testing/CI_IMAGE.md` (Inputs): "Changed declared scripts refuse generation until reviewed again", and unknown commands refuse generation.
  - `scripts/ci_tool_inventory.py --check`, run with the checksum-pinned shfmt v3.11.0 (sha256 `1904ec6b...` verified against `ci/image/sources.lock.json`), refuses identically at dev `a032c6d6` and at this head: `REFUSED: changed declared script 'sw/builder/endstation_builder.py'` (`receipts/inventory/dev-a032c6d6-check.log`, `head-check.log`). That refusal predates this PR and is not caused by it.
  - Walking past it on disposable copies (`scripts/inventory_walk.py`), the next refusal on both trees is a further dev drift: undeclared `avdecc/gen_aemi_image.py` (`receipts/inventory/walk-*.log`).
  - What this PR adds (`receipts/inventory/pr-additions.txt`):
    - `crflic_mutants.py` now hashes `baec486a...` against its declared pin `ce4c4ff1...`. That pin matched at dev.
    - The new `Vmilan_dp_tspec8` runtime command that the Makefile recipe executes has no `commands` entry, while `Vmilan_dp_crflic` does.
  - Reviewer re-review of the changed declared script: `crflic_mutants.py` at this head still only runs `make` targets of this suite and the built executables, writes only into a temporary directory, installs nothing and uses no network. Its "reviewed non-installing" class remains true.
- **Impact:** once dev's drift is cleared, generation still refuses on this PR's two entries, so the CI image cannot be regenerated from a tree containing this change without a further edit. The author disclosed this as an open risk, but the contract is left unmet.
- **Required outcome:** this PR records its own two entries in `ci/image/command-table.json`: the re-pinned `crflic_mutants.py` digest, its class confirmed above, and a `Vmilan_dp_tspec8` command entry shaped like `Vmilan_dp_crflic`'s. Regenerating `tool-inventory.json` stays blocked by dev's pre-existing drift; that is a manager item, not this PR's.
- **Verification:** `scripts/inventory_walk.py` on a disposable copy of the new head shows no refusal naming `crflic_mutants.py` or `Vmilan_dp_tspec8`, and `pr-additions.txt` regenerated at that head shows MATCH for `crflic_mutants.py`.

### R1 RESIDUE - `docs/traceability/ieee8021q.md:103` (Q-10) - stale source description

- The PR does not touch the row, but it still reads "MaxFrameSize still derives from real AAF geometry in [`milan_datapath`](...), passed as `cfg_tspec_max_frame_i`."
- Since #774 the CRF slot derives from the CRF framer's PDU shape. This is pure wording: no figure, verdict, clause or generated artifact changes.
- Exact fix: "MaxFrameSize still derives from real frame geometry in [`milan_datapath`](../../hdl/milan/milan_datapath.sv), one slot per source: each AAF talker's channel count and the CRF output's PDU shape (#774), passed as `cfg_tspec_max_frame_i`."
- The fix adds no backticked module and no dotted number, so the generated matrix is unchanged. Confirm with `gen_module_matrix.py --check`.

### S1 SUGGESTION - Tests - `hdl/milan/milan_datapath.sv:9057` / `tb/verilator/milan_dp/sim_crf_licence.cpp:1270` - the per-AAF-talker slot index is not observable at the graded shapes

- The probe `aaf_slots_read_talker0` (every AAF slot reads `tctx_maxf_w[0]`) survives on both `obj_crflic` and `obj_tspec8` (`receipts/probes/tspec_probes.out`).
- Every AAF talker in an elaboration has the same width, and the TCTX `chans` field is the only per-talker lever. Per the in-tree note at `milan_datapath.sv:6689`, no board software writes it, and talker-side SET_STREAM_FORMAT is not wired. So silicon cannot reach a mixed-width state today, and the frozen acceptance (the talker-0 control fails on both shapes) is met.
- Optional: in `obj_tspec8`, write one AAF talker's TCTX w0 `chans` to a narrower even width before the probes, and grade 24*N + 24 + 1 per talker from the harness's own table.

## Clean lenses

- [R687] PASS Conformance - `hdl/milan/milan_datapath.sv:9046-9060`, `hdl/ieee1722/crf/KL_crf_tx.sv:221,232-246`, `hdl/milan/KL_pp_shadow.sv:294-303,1284`, `receipts/legs/crflic-run.log` and `tspec8-run.log` - checked against the issue #774 acceptance criteria, Milan v1.2 Table 4.4 as cited in-tree and in the issue, and IEEE 802.1Q-2018 35.2.2.8.4 a) and 35.2.2.8.
  - **AC1:** the wrapper port is `[N_STREAM_OUT_P*16-1:0]` and is passed straight to the processor's per-source port. The every-slot copy is gone.
  - **AC2:** each AAF slot is `tctx_maxf_w[t]` = 24 + 1 + 6*4*chans. The CRF slot is `tspec_max_frame_o` = (CRF_HDR_C 20 + crf_data_length 8) + 1 = 29. There is no literal, and the "scratch only" comment is removed.
  - **AC3, at this head:** `obj_crflic` gives 427 checks, 0 failures. uid 0 declares 217 and uid 1 declares 29 over 27 and 102 Talker Advertise values, each equal to the emitted AVTPDU + 1. `obj_tspec8` gives 61 checks, 0 failures: nine sources, 217 x 8 and 29.
  - **Talker-0 control:** fails got=217 exp=29 on both shapes, both in my probe and in the full `make crflic-mutants` campaign (10/10; `receipts/legs/crflic-mutants.log`).
  - **Cross-checks:**
    - The processor's per-format list gives "CRF → 29" (`protocol-processor/docs/architecture/10_srp_engine.md:136`).
    - Its Milan four-step admission recipe (`protocol-processor/hdl/srp/KL_srp_admission.sv:19-25`) prices 29 as 51 → 68 → 88 octets, which is 5632 kb/s, the figure it cites as mandated for CRF.
    - The builder already budgets CRF as `28 + MILAN_TSPEC_HEADROOM_B` (`sw/builder/endstation_builder.py:341-347`), so RTL and build budget now agree.
    - A packed vector's later values are attributed FirstValue's TSpec (`sim_crf_licence.cpp` `on_mrpdu`). With CRF at the next consecutive Unique ID and DA, the passing CRF grade proves the processor puts the CRF output in its own vector.
  - **AC4:** checked from the author's receipts, see "Focus items" below.
- [R687] PASS Robustness - `hdl/milan/milan_datapath.sv:1675-1694,9053-9058,9246,9272`, `protocol-processor/hdl/top/protocol_processor_top.sv:2701`, `docs/traceability/ieee8021q.md:103`, `receipts/probes/tspec_probes.out` - checked against configuration-dependent shapes, widths, clocking, failure paths and planted faults.
  - **No-CRF shapes:** at `ACMP_SRC_C == N_STREAMS` the shapes get no `g_maxf_crf` branch (`CRF_TUID_C = N_STREAMS` is out of range), so every slot is an in-range `tctx_maxf_w`. The elaboration guard refuses any other source count.
  - **Widths and clocking:** `pp_src_maxf_w` is `ACMP_SRC_C*16` against `N_STREAM_OUT_P = ACMP_SRC_C`. The processor runs on `axis_clk`, like `tctx_maxf_w`, so there is no new crossing.
  - **Capture timing:** the processor samples slot s at the gate-open capture, as before. A runtime TCTX `chans` write remains the pre-existing quasi-static case, now per talker rather than talker 0's.
  - **Shaper effect:** no shaper is programmed from the slope in the shipping datapath (Q-10), so a smaller CRF declaration changes reservation and admission only. The CRF slope falls from 16.576 to 5.632 Mb/s, the Milan figure.
  - **Planted faults** (`scripts/tspec_probes.py`, 6 probes x 2 shapes, 12 parallel builds; per-run logs in `receipts/probes/`):
    - All 10 catch runs are caught by the named checks: talker 0 on every slot; the CRF slot dropping the table's octet (28); the CRF slot declaring the padded MSDU (42); the AAF slots dropping the table's octet (216); and `KL_pp_shadow` driving slot 0 into every slot.
    - The 2 expected-survivor runs are S1's equivalence.
  - **Harness scope:** the harness grades Talker Advertise only (type 1), excludes the staged TSpecs of [G]-[J] by the explicit `corner_phase` latch, and requires at least one value per source, so a silent source fails.

## Unclean lenses: what was applied

- **RTL** (applied: `KL_crf_tx.sv:221-246`, `KL_pp_shadow.sv:294-303,1284`, `milan_datapath.sv:1961,2405,6714-6733,7427,9046-9060,9407`): naming, `//!` port documentation, widths and casts (`16'(CRF_PDU_C + 1)`) are sound. `FRAME_BYTES` stays 60 by arithmetic (14 + 28 + 18). `lint_rtl.py --check` PASS, 89 <= 89 (`receipts/gates/lint_rtl_check.log`). The `crf_tx` suite builds with the new output left unconnected and passes 129/0 (`receipts/gates/crf_tx.log`). Unclean only by F1.
- **Tests** (applied: `sim_crf_licence.cpp` diff, `Makefile` legs and recipes, `crflic_mutants.py`, `test_sim_pool.py` 17/17 PASS, the BDD suite, the CI inventory): unclean by F1 and F3. S1 is optional.
- **Docs** (applied: CHANGELOG, compliance matrix 4.3.3, REGISTER_MAP `LWSRP_TSPEC`, SUBMODULES #190 row, TESTING.md, milan_dp README leg table, `[TSPEC]` and failing-arm rows, ieee8021q SRP-10 and Q-10, the generated MODULE_MATRIX and README-tests rows, source comments): `docs_check.py` reports 0 findings (`receipts/gates/docs_check.log`). There are no em dashes in the 310 added lines. The source-comment rule shows no lane label, review round, reviewer ID or comment ID in the delta; `[B]`, `[E]` and `[G]-[J]` are the harness's own phase names (`receipts/hygiene/`). Unclean by F2; R1 is residue only.

## Focus items

1. The `KL_pp_shadow` port is one 16-bit value per stream output, `[16*s +: 16]`, passed straight through. No every-slot copy remains (`KL_pp_shadow.sv:303,1284`). The planted slot-0 copy in the wrapper is caught on both shapes.
2. `g_pp_maxf` assigns AAF talker t `tctx_maxf_w[t]`, which is 24 x N + 24 + 1 (with N = 8 here, 217). The CRF slot gets `KL_crf_tx.tspec_max_frame_o` = 20 + 8 + 1 = 29.
   - There is no literal: the header is `CRF_HDR_C` (IEEE 1722-2016 10.4) and the data length is `CRF_DLEN_C` (10.4.11), matching `pdu[16..19]` and the 28-octet `pdu[]`.
   - The derivation form is what breaks F1's oracle, not its value.
3. `[TSPEC]` grades every Talker Advertise value per source, FirstValue's TSpec included for packed values, on `obj_crflic` (1x1) and `obj_tspec8` (8x8, nine sources, `ADP_TALKER` checked). The talker-0 control fails on both shapes.
4. The gates are confirmed from the author's receipts at the stated heads (I did not re-run them):
   - Sweep at `5f0d5bf9`: 4 shards with rc 0, and the tallies sum to 2,189,325 checks with 0 failures.
   - `tsn_fuzz` re-run: 899/0.
   - Yosys at `e70a99ba`: 60/60.
   - Lint at `5f0d5bf9`: rc 0. I reproduced lint at the head.
   - Docs gates at `5f0d5bf9`: 44 steps, 0 failed.
   - Resource gate at `e70a99ba` against the record: route-1x1 PASS (SLICE 15,835 → 15,831, -4; WNS 0.281 ns), ooc-1x1 PASS and ooc-8x8 PASS.
   - `e70a99ba..5f0d5bf9` touches Markdown only (verified), so the design-dependent receipts carry to the head.
   - The gate list omits `bdd-conformance` (F1).
5. The inventory refusal on `sw/builder/endstation_builder.py` is pre-existing at dev `a032c6d6` and is not caused by this PR. This PR adds the `crflic_mutants.py` digest drift (`ce4c4ff1` → `baec486a`) and an unregistered `Vmilan_dp_tspec8` command (F3).

## Ledger (reviewer-owned)

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:9046-9060,9407`; `KL_crf_tx.sv:221-246`; `KL_pp_shadow.sv:303,1284`; processor `protocol_processor_top.sv:303,2701`, `10_srp_engine.md:136`, `KL_srp_admission.sv:19-25`; `crflic-run.log`, `tspec8-run.log`, `crflic-mutants.log` | R687-1 | `5f0d5bf931c87f3e6e3b813e042c64a61f9cb13e` |
| RTL | UNCLEAN (F1) | `KL_crf_tx.sv:221-246`; `KL_pp_shadow.sv:294-303,1284`; `milan_datapath.sv:1675-1694,6714-6733,9046-9060,9246,9407`; lint receipt; `crf_tx` 129/0 | R687-1 | `5f0d5bf931c87f3e6e3b813e042c64a61f9cb13e` |
| Robustness | CLEAN | no-CRF generate path, widths and clocking (`milan_datapath.sv:1675-1694,9053-9058,9246,9272`); processor capture (`protocol_processor_top.sv:2701`); `tspec_probes.out` (10 catch runs caught, 2 expected survivors) | R687-1 | `5f0d5bf931c87f3e6e3b813e042c64a61f9cb13e` |
| Tests | UNCLEAN (F1, F3) | `sim_crf_licence.cpp`, `Makefile`, `crflic_mutants.py`, `test_sim_pool.py`; behave head and dev receipts; inventory receipts | R687-1 | `5f0d5bf931c87f3e6e3b813e042c64a61f9cb13e` |
| Docs | UNCLEAN (F2) | CHANGELOG, MILAN_COMPLIANCE_MATRIX, REGISTER_MAP, SUBMODULES, TESTING, milan_dp README, `ieee8021q.md:103,154`, MODULE_MATRIX, README-tests; `docs_check` 0 findings; matrix probe | R687-1 | `5f0d5bf931c87f3e6e3b813e042c64a61f9cb13e` |

## Real limits

- The Milan v1.2, IEEE 802.1Q-2018 and IEEE 1722-2016 texts were not available to this round. Table 4.4's rows (24*N + 24 + 1; CRF 28 + 1) and the clause numbers were checked against the issue, the processor's SRP engine document and admission recipe, and the builder, not against the standards themselves.
- Not re-run here, by rule: the full sweep, Yosys, the Vivado resource gate, the builder and docs-gate banks. Their results are the author's published receipts, with route-1x1, ooc-1x1 and ooc-8x8 built at `e70a99ba`, which is design-identical to the head.
- The dev side of F1 is shown by the hosted dev `bdd-conformance` success and by the step's resolver applied to dev's `KL_crf_tx.sv`, not by a full local behave run on a dev tree.
- Simulation only. No bench and no hardware; physical calibration was NOT RUN.
- The other hosted failures at this head are consequences of the fail-fast cancellation that followed `bdd-conformance`: the union jobs report owners cancelled, and `docs-check`/`elaborate` report dependent jobs cancelled. They are not independent signals, and their real results at this head are unknown.

## Pending manager duties

- Hosted and act acceptance at the next head. At this head `rtl-fast` is cancelled and the union, `docs-check`, `elaborate` and portability contexts are cascade failures.
- Current-dev candidate merge validation (builder and native banks) at the merge turn.
- Carry R1 to the residue checklist.
- Track regeneration of `tool-inventory.json`, which is blocked by dev's pre-existing `endstation_builder.py` and `avdecc/gen_aemi_image.py` drift.
- After the fix commit, re-cover RTL, Tests and Docs at the new head. Conformance and Robustness need re-covering too if the fix touches `KL_crf_tx.sv` or the per-source path.

## Receipts

Every published file is listed in `MANIFEST.sha256`:
- `scripts/`: `bdd_frame_bytes_probe.py`, `inventory_walk.py`, `matrix_clause_probe.py`, `run_gates.sh`, `tspec_probes.py`.
- `receipts/bdd`: local behave run at head; resolver probe; hosted check lists and the failing job log.
- `receipts/legs`: clean builds, the two leg runs, the full `crflic-mutants` campaign.
- `receipts/probes`: the 12 planted-fault runs.
- `receipts/gates`: lint, `test_sim_pool`, `docs_check`, `crf_tx`.
- `receipts/inventory`: the checks at dev and head, the walks and the PR additions.
- `receipts/docs`: the matrix probe and `--check`.
- `receipts/hygiene`: added-line scans.
- `receipts/restore`: clone state after the probes. HEAD and tree are as above; the worktree and index are clean; the index (mode, blob, path) equals the HEAD tree; all six gitlinks match HEAD; the protocol-processor and gptp-processor checkouts are at their gitlinks and clean. Only ignored build and cache entries remain.

R687-1 FINISHED
