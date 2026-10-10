[R558] NEGATIVE - exact head d1b18b3fa0b476a9b534c88466b163e15f469004

Round R558-7, internal cleared-context review of issue #696 / PR #706. Tree `32c6c80f62e026070ca11b8e3dba8178667b0e13`. Source base `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. The lane's own change is `git diff e8454e275..d1b18b3fa` (17 files; `e8454e27` is the last dev tip merged into the branch). The rest of the `6aa25dec..d1b18b3f` diff is dev content from PRs #672, #698-#702.

## 1. Verdict

**NEGATIVE: one MINOR is open (R558-7-F1, Tests).** No BLOCKER and no MAJOR.

- **What R558-7-F1 is.** The M2 checks cannot tell "echo the PROBE's requested_start" apart from "echo the overlap start". In every fixture where requested_start is graded, the PROBE starts at or above this station's offset, so the two values are equal. A planted defect that writes the overlap start into the DEFEND's requested_start passes all 177 unit checks.
- **The RTL is correct.** One added check passes on the clean RTL and fails on that defect.
- **Other lenses.** Conformance, RTL and Robustness are clean. Docs is clean, with one new RESIDUE (R558-7-R1) and the retained earlier residues.
- **R558-6-F1 is resolved at this head.** The first Begin! offset and first probe interval now fold the full 32-bit seed one generator step on. I verified the documented guarantees exhaustively, independently of the suite. R558-6's p7 is caught in both harnesses.

## 2. Scope reconstructed (public sources only)

- **Issue #696 acceptance (frozen):**
  1. Each of M1-M8 is either conformed, with a suite check and a planted defect, or justified by clause in `MAAP_FABRIC.md`.
  2. M4 is fixed in RTL, seeding at enable or at MAC programming, with a datapath check that two MACs draw different intervals.
  3. OOC area and one shipping route stay within budget, and the records are re-recorded through the recipe.
  4. Bench interop.
- **Assignment 6076750392 and rulings:**
  - 6076940309: M8 discards without counting, and the missing count is a documented B.2 deviation.
  - 6079087547: the +60 LUT / +60 FF ceiling applies to the `g_maap.maap_engine` OOC row. M6 uses one shared buffer, and M3 fits within the remaining headroom.
  - 6079463350: the differential stimulus update is authorized.
  - 6080332335: the consumer documentation pages are authorized.
  - 6089712293: merge dev and re-measure, with no floor exception.
  - 6097504752 (round 6): the first draw steps the full seed; adds checks, p7 in the campaign, re-measurement and records.
  - Acceptance 4 is assigned to a post-merge bench lane.
  - The lane has no register-map, filter or mailbox scope. The lane diff touches none of them.
- **Authorities:** IEEE 1722-2016 Annex B, as cited by the issue, `MAAP_FABRIC.md` and `KL_maap.md`. `REQUIREMENTS.md` FR-MAAP-01 via `docs/reference/FR_NFR.md:167`. `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`.

## 3. Findings

### R558-7-F1 - MINOR - Tests - `tb/verilator/maap/sim_main.cpp:383-384`, `:389-391`, `:403-404`, `:419-421`, `:508-510`; `tb/verilator/maap/mutants.py:107-110` - the M2 requested_start check cannot fail for an echo of the overlap start

- **Authority:**
  - Issue #696 M2 (B.3.6.6): "DEFEND echoes the PROBE's requested start address and count".
  - Acceptance 1 requires a suite check and a planted defect for each conformed item.
  - `AGENTS.md` section 6, Tests lens: "Each new test can fail for the defect it claims to detect."
  - `docs/design/MAAP_FABRIC.md:65` states "Its requested_* fields echo the triggering PROBE (B.3.6.6)".
- **Evidence:**
  - The RTL stores `tx_defend_off_r <= rx_start_r` (`hdl/ieee1722/maap/KL_maap.sv:439`). The overlap start is `conf_start_w = max(rx_start_r, offset_r)` (`:250`).
  - requested_start is graded in four places:
    - `sim_main.cpp:383` (PROBE at `off0+4`);
    - `:404` (`off0+7`);
    - `:419-421` and `:508-510` (`off0+1`, `off+2`).
  - Every one of those PROBEs starts at or above this station's offset, so the PROBE's requested_start equals the overlap start.
  - The only fixture whose PROBE starts below the station's offset is `[4b]` at `:389-391`, at `off0-4`. Its DEFEND's requested_start is never read.
  - The campaign's M2 start plant, `m2_own_requested_start` (`mutants.py:107`), writes `offset_r`, which differs from `off0+4`. It does not cover the overlap-start variant.
  - Probe `q1_m2_echo_overlap_start` writes `conf_start_w` into `tx_defend_off_r`. It **escapes**: rc 0, 177 checks, 0 failures (`receipts/reviewer_probes.log`, `receipts/probes/q1_m2_echo_overlap_start.log`).
  - Adding one check to a scratch copy of the harness at `[4b]` (requested_start == pool | `off0-4`) gives:
    - clean RTL: 178 checks, 0 failures;
    - q1: 1 failure, at that check (`scripts/echo_gap_demo.sh`, `receipts/echo_gap_demo.log`, `receipts/echo_demo/`).
- **Impact:**
  - A plausible regression puts the conflict range's start into the requested_start field of every DEFEND whose prober's range begins below this station's block, which is a B.3.6.6 wire defect. The suite reports it green.
  - The value sits next to `tx_conf_start_r <= conf_start_w` (`KL_maap.sv:441`) and is one identifier away from it.
  - M2's acceptance 1 evidence holds for the own-offset defect class only.
- **Required outcome:**
  - A named M2 check reads the DEFEND's requested_start for a PROBE whose requested_start is below this station's offset.
  - A planted defect echoing the overlap start (`conf_start_w`) joins the default campaign and must fail that named check.
  - No RTL change is needed.
- **Verification:**
  - The default MAAP target is rc 0, with the new campaign row `[ok]` at its named check.
  - `scripts/reviewer_probes.py <clone> <work> q1_m2_echo_overlap_start` reports CAUGHT.

### R558-7-R1 - RESIDUE - Docs - `docs/design/MAAP_FABRIC.md:257` - the interval-check sentence names more pairs than the check grades

- **Evidence:**
  - The sentence says the "adjacent and bit 16..31 pairs" must give different first probe intervals.
  - The preceding sentences define the bits 16..31 set as all pairs differing only in bits 16..31. The check grades 139 of those pairs for disjoint blocks.
  - The interval check (`sim_main.cpp:1043-1061`, `:1076`) grades 52 pairs:
    - 33 adjacent pairs;
    - R558-6's three high pairs;
    - the 16 single-bit pairs in bits 16..31.
  - The property itself holds for every carry run (`receipts/fold_claims.log`, C5), so no design claim is wrong.
- **Why RESIDUE:**
  - The fix is prose only. It changes no test, code, figure, verdict or clause claim, and the PR body already states "52 first-interval pairs".
- **Exact fix:**
  - Replace "Clocks one power of two apart must give different first offsets, and the adjacent and bit 16..31 pairs different first probe intervals." with "Clocks one power of two apart must give different first offsets. The adjacent pairs, R558-6's pairs and the 16 single-bit pairs in bits 16..31 must give different first probe intervals."
- **Verification:** reread the line, then run `docs_check.py` and `check_em_dash.py`.

### Suggestions (optional; no lens effect)

- **R558-7-S1 - Tests - `KL_maap.sv:202`; `sim_main.cpp:1076`.** This extends the author's disclosed open risk.
  - Probe `q3_probe_fold_unstepped` folds `lfsr_r` instead of `lfsr_next_w` and escapes the suite (177/0).
  - Algebraically, the unstepped probe fold gives equal first probe draws for 3 of the 528 carry runs (`receipts/unstepped_fold.log`). The step therefore carries part of the guarantee at `MAAP_FABRIC.md:115`.
  - Either extending the interval check to all 528 carry runs or one golden first-interval value would grade it.
  - No clause requires distinct first intervals, so this stays optional.
- **R558-7-S2 - Tests - `KL_maap.sv:337-339`; `MAAP_FABRIC.md:110`.**
  - Probe `q4_every_begin_refolds` makes every Begin!, not only the first, re-fold MAC plus clock. It escapes (177/0).
  - The documented "later Begin! events draw the running generator" is therefore ungraded.
  - A check that two consecutive Release!/Begin! cycles at a frozen clock claim different offsets would grade it.

## 4. Prior public findings on this PR, at this head

| Finding | Status at `d1b18b3f` | Evidence |
|---|---|---|
| R558-6-F1 (MINOR; Conformance, RTL, Robustness, Tests): raw low 16 seed bits in the first draw; p7 escapes | **Resolved** | `KL_maap.sv:154`, `:337-339`: `rand_offset(offset_fold(lfsr_step(seed)))`. Probe interval `probe_fold(lfsr_next_w)` (`:202`); at the first PROBE that is the stepped seed (traced: seed loads at `:383-386`, first PROBE at the next cycle `:477-495`). Five named unit checks pass (`receipts/unit.log` [12]). Datapath checks 5/0 (`receipts/integration_run.log`). p7 caught in both harnesses: `m4_first_offset_ignores_seed`, `m4_datapath_first_offset_ignores_seed` (`receipts/mutants.log`). R558-6's four pairs modelled from the RTL rows give the PR body's offsets, all disjoint (`receipts/r558_6_pairs_model.log`). Exhaustive guarantees in section 5 |
| R558-6-R1 (RESIDUE): PR body stale head | **Resolved** | The body names `d1b18b3f…` under Status and the state commands, and its round table covers rounds 1-6 |
| R558-6-S1, R558-6-S2 (SUGGESTION) | Retained, optional | Not applied (author statement); no lens effect |
| R558-5-F1 (MINOR, Docs) | Resolved at `6de3904e`; still resolved | `AREA_BUDGET.md:371`, `MARK_II_AREA_PLAN.md:654` name #696's current 50,013-LUT record as the anchor |
| R558-5-R1 (RESIDUE): M0s "records unchanged" lines | **Retained** (residue checklist) | Now `AREA_BUDGET.md:362`, `:379`, `MARK_II_AREA_PLAN.md:666`; text unchanged |
| R558-2-R1 / R559-2-R1 (RESIDUE): baseline sentences point at the live record file | **Retained** (residue checklist) | `MARK_II_AREA_PLAN.md:66-67`, `:317`, `:1007` unchanged. The live record's notes now identify `bee1b0d7`; the published exact fix still applies |
| R558-4-R1 (RESIDUE, PR body head) | Resolved (via R558-6-R1) | As above |
| R558-3-F1 = R559-3-F1 (BLOCKER, `integration.mk` make 4.3 capture) | Resolved at `30073ee9`; still resolved | `integration.mk` unchanged since `30073ee9`. The integration build derives the sources and runs 5/0 here. Hosted shards at this head are not all complete (section 5) |
| R558-1-F1, R559-1-F1/F2/F3 (MINOR) | Resolved; still resolved | `MAAP_FABRIC.md:159-167` states every area step. The `sim_main.cpp` M5 loss check passes, and `m5_restart_on_link_loss` is caught. The MARK_II inventory rows match the recorded scopes (spot-checked). The zero-seed fixture is named `02:00:00:00:00:00` |
| R558-1-S1 (applied); R559-1-S1..S4, R558-3-S1/S2, R559-3-S1, R558-4-S1/S2, R559-4-S1/S2, R559-5-S1 (SUGGESTION) | Retained, optional | No lens effect |

## 5. Executed evidence (this round, exact head, pinned simulator 5.050 verified by `--version`)

| What | Command (scripts in `scripts/`) | Result | Receipt |
|---|---|---|---|
| Unit harness | `make -j8 -C tb/verilator/maap run MDIR=<scratch>` | rc 0; **177 checks, 0 failures**; [12] reports 33 / 139 / 360 / 34 / 52 pairs | `receipts/unit.log`, `unit.rc` |
| Real datapath | `make -C tb/verilator/maap integration-build DP_MDIR=<scratch>` then `./maap_integration` | rc 0; **5 checks, 0 failures**; first offsets 0x7029 / 0x9821 (adjacent MACs) and 0xf229 / 0xf1cd (PHC); link return reprobes 4 | `receipts/integration_build.log`, `integration_run.log`, `integration.rc` |
| Coverage | `make -C tb/verilator/maap coverage COV_MDIR=<scratch>` (5.050 reader) | rc 0; `KL_maap.sv` **225/225** lines, gate 95 % PASS | `receipts/coverage.log`, `coverage.rc` |
| Planted-defect campaign | `tb/verilator/maap/mutants.py` (unchanged, run under a distinct process name) | rc 0; **59 rows, 0 escapes**: 57 defects at their named checks, 2 clean controls | `receipts/mutants.log`, `mutants.rc` |
| (first attempt) | same | Terminated externally by SIGTERM (rc 143) after 5 rows; superseded by the full rerun above, not used | `receipts/mutants_attempt1_sigterm.*` |
| Firmware MAAP differential | `maap_differential.py --self-test` | rc 0; clean **12/12**, parent 5172..5810 cycles; **17/17** defects caught; the MAC-ignoring parent draws 5230..5801 and fails the draw-coverage check | `receipts/differential.log`, `differential.rc` |
| Fold guarantees (independent; reads the rows from the RTL) | `python3 -I scripts/fold_claims.py KL_maap.sv` | rc 0. C1: x^32+x^22+x^2+x+1 has order 2^32-1. C2: 22 rows have rank 22. C3: bits 16..31 map one-to-one onto the offset word. C4: **all 528 carry runs × 65,536 words × count 1..8 give disjoint blocks** through the pool fold and the clip. C5: all 528 runs give different first probe draws. C6: non-power-of-two pairs overlap 15.9 per 65,024 (documented "about 15") | `receipts/fold_claims.log` |
| Without-step control | `scripts/unstepped_fold.py` | Unstepped offset fold violates C4 in 2/528 runs; unstepped probe fold violates C5 in 3/528 runs | `receipts/unstepped_fold.log` |
| Reviewer probes (10) | `scripts/reviewer_probes.py --jobs 5` | 7 CAUGHT (q2, q6, q7, q11, q12, q13, q14); 3 ESCAPED: q1 (F1), q3 (S1), q4 (S2) | `receipts/reviewer_probes.log`, `receipts/probes/` |
| F1 closability | `scripts/echo_gap_demo.sh` | clean 178/0; q1 178/1 at the added check | `receipts/echo_gap_demo.log`, `receipts/echo_demo/` |
| Record policy and gate | `pp_resource_gate.py check-baseline`; policy comparison vs `30073ee9` | `baseline PASS: 3 endpoints`. Only `record` and `measured` changed; tolerance, floor, ceiling, schema and identity are unchanged. All three input digests changed | `receipts/record_policy_and_check_baseline.txt` |
| Hosted snapshot | `gh api …/commits/d1b18b3f…/check-runs` (read only) | 20 contexts when read: 12 success, 1 skipped (physical gPTP), 7 in progress (Verilator shards 0, 1, 2, 4, firmware-unit, docs-check, elaborate) | `receipts/hosted_checks_d1b18b3f.txt` |
| Restore | `git status --ignored`, `diff-index`, `diff-files`, `ls-tree` of gitlinks | Clean. HEAD and tree exact. Gitlinks: protocol-processor `2ad2f845`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`, lwSRP `9197193e`, external `efeb541a`. Submodules clean | `receipts/restore_verify.txt` |

Receipt logs had the pinned image's absolute root replaced by `<PINNED_IMAGE_ROOT>`. No other byte was changed.

## 6. Results per lens

- `[R558] PASS Conformance - hdl/ieee1722/maap/KL_maap.sv:146-154,163-178,202,315-339,383-386,432-444; hdl/milan/milan_datapath.sv:7171-7172; receipts/fold_claims.log, integration_run.log, differential.log, record_policy_and_check_baseline.txt - each acceptance item against the issue and rulings:`
  - **M1:** compare_MAC in rProbe!/PROBE and rDefend!/DEFEND (`:315-320`). Equal MAC yields; q11 caught.
  - **M2:** the RTL echoes `rx_start_r` and all 16 count bits (`:439-440`). Demo check passes on clean RTL. The test gap is F1, under Tests only.
  - **M3:** period 2^32-1 (C1); seed is MAC plus PHC at first enable (`:150`, `:383-386`).
  - **M4:** sampled at first enable, not reset. Datapath: two MACs draw different intervals and disjoint first blocks (acceptance 2).
  - **M5:** rising `eff_link_w` restarts; a falling level is no event (B.3.5.9).
  - **M6:** shared buffer, with its capacity deviation recorded per ruling.
  - **M7:** Table B.9 bounds (`:331-333`); q12 caught.
  - **M8:** discard with no effect; counting withdrawn by ruling and recorded (`MAAP_FABRIC.md:184-186`).
  - **Acceptance 3:** MAAP 490/340, +51/+60, is within the ruled ceiling (author measurement). All three records are rewritten with policy unchanged, and `check-baseline` passes.
  - **Acceptance 4:** assigned to the post-merge bench lane.
  - The lane makes no register-map, filter or mailbox change (`git diff --stat e8454e275..HEAD`).
- `[R558] PASS RTL - KL_maap.sv:141-203,337-339,341-507; milan_datapath.sv:2165,3000-3001,7168-7172 - widths, clocks and FSM:`
  - Fold functions are pure combinational parity over 32 bits, so no flop is added.
  - `probe_iv_w` is at most 581 in 16 bits. `new_off_w` selects the fold only while `rng_seeded_r` is 0, which is the first-enable cycle only.
  - The all-zero seed takes the fallback (`:151`). The LFSR step is invertible, so the generator never reaches 0 from a nonzero seed.
  - `port_operational_r` resets to 0, and the edge is harmless in IDLE.
  - Both new inputs come from axis-domain nets that existing logic already consumes synchronously: `eff_link_w` at `:3589-3615` and `:8174`, and `ptp_now_w` under the `gtx_clk == axis_clk` contract (`:2934-2935`). No new crossing is added.
  - FSM default arm unchanged; `MAAP_P = 0` tie-off unchanged.
  - The first-draw path depth is reported at +3.906 ns in the route (author measurement, not re-run).
- `[R558] PASS Robustness - tb/verilator/maap/sim_main.cpp:846-892 (M8 lengths 1..41 and each missing byte 0..41, all message types), :825-844 (seeds 0, limit, limit+1, 0xFE00, 0xFF00, 0xFFFF at counts 1/8/255), :732-757 (disable, link flap, conflicting ANNOUNCE and reset during a pending response), :787-823 (outage longer than a walk), :396-421 and :487-517 (backpressure at 0/2/4/7 beats); receipts/fold_claims.log C4 (counts 1..8, pool fold and clip edges); probes q6/q7/q12/q13/q14 caught - truncation, boundaries, reset during activity, repeated and long link events, and backpressure all graded and passing at this head`
- `[R558] MINOR Tests - sim_main.cpp:383-404; mutants.py:107-110 - R558-7-F1`. Also examined, clean:
  - the [12] first-claim checks and their pair generators (`sim_main.cpp:979-1077`);
  - the datapath checks (`sim_integration.cpp:129-187`);
  - every campaign row (59/0);
  - the differential's either-end needle (`maap_differential.py:65-84`), where the clean run still requires both ends;
  - coverage 225/225;
  - S1 and S2 recorded.
- `[R558] PASS Docs - docs/design/MAAP_FABRIC.md:82-127,153-186,209-261; hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5,22-29; sw/firmware/ctrl/maap/README.md:189-192; docs/design/AREA_BUDGET.md:10,106-160,371,410,466-469; docs/design/MARK_II_AREA_PLAN.md:56,108-142,654; docs/findings/234_PP_SHADOW_AREA_BASELINE.md:1-107; docs/findings/README.md:25; docs/testing/TESTING.md:606; docs/reference/FR_NFR.md:167; PR #706 body - every first-draw, fold, seed, link and area statement checked:`
  - Fold claims were checked exhaustively (section 5).
  - The record table and arithmetic were recomputed: 50,013/63,400 = 78.88 %; 11,973 over; 97 slices free; wrapper 22,993 - 11,973 = 11,020; WNS fall 0.203; deltas -217/-2/-70/+0.119/-0.019.
  - MARK_II rows were spot-checked against the recorded scopes.
  - The PR body's datapath offsets match `receipts/integration_run.log`.
  - Clean apart from RESIDUE R558-7-R1 and the retained residues.

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue acceptance 1-4, rulings, `KL_maap.sv`, datapath wiring, fold proofs, records | R558-7 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |
| RTL | CLEAN | `KL_maap.sv` (full), `milan_datapath.sv:7168-7172` and the link and PHC sources | R558-7 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |
| Robustness | CLEAN | M5/M6/M7/M8 fixtures, exhaustive fold edges, probes q6, q7, q12, q13, q14 | R558-7 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |
| Tests | **UNCLEAN** (R558-7-F1 open) | Unit 177/0, datapath 5/0, campaign 59/0, coverage 225/225, differential 12/12 and 17/17, 10 probes | R558-7 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |
| Docs | CLEAN (RESIDUE R558-7-R1; retained R558-5-R1 and R558-2-R1 / R559-2-R1) | Design, findings, area and consumer pages, PR body | R558-7 | `d1b18b3fa0b476a9b534c88466b163e15f469004` |

## 8. Real limits

- **Area, timing and records.** No synthesis or route was run by this review. The MAAP 490/340 figure, the three endpoint figures and the claim that only `KL_maap.sv` differs in measured inputs rest on the author's receipts, which are not published for round 6. I verified:
  - the record's internal consistency and unchanged policy;
  - `check-baseline`;
  - that the RTL-relevant tree difference `0df48637..bee1b0d7` touches only `KL_maap.sv` (plus its doc and dev's `syn/ooc` tooling).
- **Banks not run.** The parent suite bank, processor, gPTP, Yosys and builder banks, behaviour scenarios and the full firmware bank were not run (not permitted). Their evidence is the author's at `30242308` and the head.
- **No manager source bank.** No manager source bank exists at this exact head, and none is claimed.
- **Hosted checks.** Hosted contexts were read once, and seven were still in progress. No act replica was run.
- **Hardware.** Physical calibration was NOT RUN. Bench interop (acceptance 4) is not proven, and field skips are not hardware proof.
- **Annex B text.** The standard's text was not available in the repository. Clause readings follow the issue, the rulings and `MAAP_FABRIC.md` as published.

## 9. Pending manager duties

- Route R558-7-F1 to the author: one named M2 check and one campaign plant. No RTL change, so no re-measure is needed.
- Carry RESIDUE R558-7-R1, R558-5-R1 and R558-2-R1 / R559-2-R1 on the residue checklist.
- Confirm the in-progress hosted contexts at the final head, and run hosted and act acceptance.
- Build and validate the current-dev merge candidate (source base `6aa25dec`, live dev `1fb0ed9a`). The builder and native banks run at the merge turn; publish their receipts.
- Assign acceptance 4 to the post-merge bench lane.

## 10. Packet

`REPORT.md`, plus every file listed in `MANIFEST.sha256`: `scripts/` (portable, with paths passed as arguments) and `receipts/`. The `scratch/` directory is not published.

R558-7 FINISHED
