[R558] POSITIVE - exact head 32582421bbf095a7b5a7d4b953c4d737b86fe54b

# R558-8 - issue #696 / PR #706 - internal cleared-context review

- **Head:** `32582421bbf095a7b5a7d4b953c4d737b86fe54b`, tree `08c6b95847c5b9b354d0894ef893ee0abb483620`.
- **Source base:** `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. The lane's own changes were read against its last dev merge, `e8454e275` (17 files).
- **Verdict: POSITIVE.**
  - All five lenses are covered clean at this head.
  - No BLOCKER, MAJOR or MINOR is open.
  - One new SUGGESTION is recorded, R558-8-S1. Earlier RESIDUE items and SUGGESTIONs are retained, as listed in section 4.
- **Order of work:** I wrote my verdict and ledger (`receipts/own_verdict_before_prior.txt`) before I read any prior review on this PR. I read no other reviewer's report for this round.

## 1. Scope reconstructed from public state

I read `AGENTS.md`, `CONTRIBUTING.md` (workflow and verification bar), `docs/README.md`, the issue body and every assignment and ruling on #696. The scope is set by these:

- Assignment 6076750392.
- Rulings 6076940309, 6079087547, 6079463350, 6080332335 and 6089712293.
- Round assignments 6093171536, 6097504752 and 6102832618. 6102832618 is the recorded first-draw separation criterion, which narrows 6097504752 item 2.

Frozen acceptance:

1. Each of M1-M8 is either conformed, with a suite check and a planted defect, or justified by clause in `MAAP_FABRIC.md`. Ruling 6076940309 withdraws M8 counting.
2. M4 is fixed in RTL first: the seed is taken at enable, not at `axis_resetn`. A datapath check shows that two MACs draw different intervals, and a reset-time-sampling plant fails it.
3. The `g_maap.maap_engine` OOC growth stays within +60 LUT / +60 FF against `6aa25dec` (ruling 6079087547). `route-1x1`, `ooc-1x1` and `ooc-8x8` are re-recorded through the recipe with no floor exception (ruling 6089712293).
4. Bench interop is assigned to the post-merge bench lane (assignment item 6). It is outside this lane.

There must be no register-map, filter or mailbox change. Documentation corrections are authorised by ruling 6080332335.

## 2. Executed evidence at this head (this round, isolated clone)

Toolchain:
- Verilator 5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050/verilator --version` gives `Verilator 5.050 2026-07-01 rev v5.050`).
- The matching `verilator_coverage` comes from the same root.
- Host python3.

Every build directory was under the packet's `scratch/`. Each job wrote its own log and rc file.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/maap run` | **186 checks, 0 failures**, rc 0 | `receipts/unit.log`, `unit.rc` |
| `make -C tb/verilator/maap integration-build` + `maap_integration` | **5 checks, 0 failures**, rc 0. Stations :01/:02 claim first offsets 0x7029/0x9821. PHC trials claim 0xf229/0xf1cd | `receipts/integ.log` |
| `make -C tb/verilator/maap coverage` | `KL_maap.sv` **225/225** lines, gate PASS | `receipts/coverage.log` |
| `python3 mutants.py` (default campaign) | **65 rows, 0 failures**: 63 planted defects rejected at their named check, plus the unit and datapath clean controls | `receipts/mutants.log` |
| `maap_differential.py --self-test` | clean 12/12, **17/17** differential mutants caught, rc 0 | `receipts/differential.log.gz`, `differential.rc` |
| The PR body's p7 reproduction | **186 checks, 9 failures**, at exactly the nine names the PR body lists | `receipts/p7_copy.log` |
| `lint_rtl.py --check` | 90 <= 90, PASS | `receipts/lint.log` |
| `pp_resource_gate.py check-baseline` | `baseline PASS: 3 endpoints` | `receipts/baseline.log` |
| `docs_check.py`; `gen_toc.py --check`; `check_em_dash.py` (base `6aa25dec` and `e8454e27`); `measure_test_evidence.py --check` | 0 findings; TOC OK; 0 findings (2,727 and 339 added lines); ratchet PASS | `receipts/docs_check.log`, `gen_toc.log`, `em_dash*.log`, `evidence.log` |
| Independent C model of the first draw, with constants transcribed from `KL_maap.sv:147,151,163-178,193-198` | offset map rank 16; bits 16..31 rank 16; joint rank 22. All 528 carry runs x 65,536 words x counts 1..8 are disjoint, with least spare 1. No carry run gives equal first probe draws. The 64 zero-sum fallback pairs are disjoint too. A direct, non-linear check of 6.4 M sampled pairs 2^i apart found 0 overlaps. All four R558-6 pairs match the documented offsets | `scripts/fold_model.c`, `receipts/fold_model.log` |
| Reviewer fault probes (12) | 11 CAUGHT at named checks, including three datapath wiring faults. `u1` ESCAPES, which reproduces retained R558-6-S1 | `scripts/reviewer_probes.py`, `receipts/reviewer_probes.log` |
| Exact-head hosted check runs (snapshot) | 8 success, 1 declared skip (`Physical gPTP`), 11 queued or in progress at the time of reading | `receipts/hosted_check_runs.tsv` |
| Tree restore | Index equals the `HEAD` tree byte for byte (blob, mode, path). No worktree or index diff, no stray ignored files. Gitlinks: `protocol-processor` `2ad2f845`, `gptp-processor` `5dce647a`, `verilog-axis` `48ff7a7e` | `receipts/tree_restore_check.log` |

No manager source bank ran at this head, and I claim none. The parent sweep, portability, firmware bank, field campaigns and Vivado were not run by me. The author reports them at `30242308`, `d1b18b3f` and `bee1b0d7`; see section 7.

## 3. Findings of this round

No BLOCKER, MAJOR, MINOR or RESIDUE.

### R558-8-S1 - SUGGESTION - Docs - `docs/testing/TESTING.md:606` - the suite-index row for `tb/verilator/maap` does not mention #696's real-datapath arm

- **Evidence:**
  - Since #696, the default `make` of this suite also builds `milan_datapath` through `integration.mk`.
  - It runs `sim_integration.cpp` as the clean datapath control and as five datapath plants (`mutants.py:191-208`, `DATAPATH_MUTANTS`).
  - The row still describes only the #686 shape: "every check grades an IEEE 1722-2016 Annex B clause, and `mutants.py` plants at least one defect per #686 item".
  - Some #696 checks, such as "M3 Release/Begin retains the generator sequence" and "M4 first-draw maps learned from the RTL are linear in the seed", grade a property rather than naming a clause.
- **Impact:** none on any verdict. A reader planning shard wall time would not learn from the index that this suite elaborates the full datapath.
- **Optional change:** add one sentence to the row, for example: "Since #696 its default target also builds the real `milan_datapath` CSR-to-MAAP path (`sim_integration.cpp`) and plants its M3, M4 and M5 datapath defects there."

### Reviewer probe observations (no new finding)

- **u1 (own requested_count follows live `count_i`).** This probe escapes. It is the same gap as retained **R558-6-S1**.
  - No contract is broken: `MAAP_FABRIC.md:71-72` leaves reconfiguration during a frame unprotected.
  - The 8-bit `tx_own_cnt_r` snapshot (`KL_maap.sv:272,282,480`) is part of the +60 FF that fully uses the MAAP FF allowance.
  - Either a check or dropping the snapshot remains optional.
- **Caught probes:**
  - Beat-4 acceptance (`u2`) and a one-byte conflict_count requirement (`u3`): both M8 checks.
  - Link return ignored while probing (`u4`): M5.
  - Count echo losing its high byte (`u5`): M2 and M6.
  - Reseeding at every Begin! (`u6`): M3 continuity and the probe-draw range.
  - A pending DEFEND surviving link return (`u7`): M6.
  - A link return counted as a conflict (`u8`): M5.
  - The generator not loaded with the seed (`u9`): M3/M4, eight checks.
  - The datapath tying `port_operational_i` high (`d1`): M5 datapath.
  - The datapath feeding PHC bits 63:32 (`d2`) or zero (`d3`): both M3 datapath checks.

## 4. Prior public findings on this PR, resolved or retained at this head (read after my own pass)

| Finding | Status at `32582421` | Evidence |
|---|---|---|
| R558-7-F1 (MINOR, Tests): M2 requested_start not graded below this station's offset | **Resolved** | Named check "M2 B.3.6.6 requested start echoes a PROBE starting below ours" passes (`receipts/unit.log`). Plant `m2_echo_overlap_start` is rejected at that check (`receipts/mutants.log`) |
| R559-6-F1 (MINOR, Tests, Conformance): first-draw checks named for an unmet property; criterion needed narrowing | **Resolved** | Manager comment 6102832618 records the criterion. `sim_main.cpp:1126-1136` names each check for what it grades, and the fixed pairs are named as fixed pairs. Anchors follow (`mutants.py:58-89`). `MAAP_FABRIC.md:112` cites the comment |
| R559-6-F2 (MINOR, Tests, Docs): universal first-draw claims had no failing check | **Resolved** | Section [13] (`sim_main.cpp:1180-1276`) learns both maps from the RTL. q3 (`m4_offset_row0_bit_drop`) and q9 (`m4_offset_row6_bit_drop`) fail their named checks. My independent model confirms every documented universal claim at the head constants (`receipts/fold_model.log`) |
| R558-7-R1, R559-6-R1 (RESIDUE, Docs) | **Resolved** | The exact texts appear at `MAAP_FABRIC.md:260` and `:117`, and in the PR body's "What the folds guarantee" third bullet |
| R558-7-S1 = R559-6-S1 (unstepped probe fold escapes) | **Resolved** (applied) | `m4_probe_fold_unstepped` is rejected at "M4 B.3.4 every seed pair 2^i apart draws different first probe intervals" |
| R558-6-F1 (MINOR; Conformance, RTL, Robustness, Tests) | Resolved at `30242308`; **still resolved** | `KL_maap.sv:154,202,337-339` unchanged since the measured head. p7 copy fails 9 checks; both p7 plants rejected |
| R558-6-R1, R558-4-R1 (RESIDUE, PR body head) | **Still resolved** | The PR body names `32582421…` under Status and the state commands |
| R558-5-F1 (MINOR, Docs) | **Still resolved** | `AREA_BUDGET.md:371` names #696's 50,013-LUT record as the anchor |
| R558-3-F1 = R559-3-F1 (BLOCKER, `integration.mk`) | **Still resolved** | `integration.mk` unchanged since `30073ee9`. The integration build derives its sources and runs 5/0 here |
| R558-1-F1, R559-1-F1/F2/F3 (MINOR) | **Still resolved** | `MAAP_FABRIC.md:159-169` area steps; the M5 loss check passes and `m5_restart_on_link_loss` is rejected; the MARK_II inventory follows the record |
| R558-2-R1 / R559-2-R1 (RESIDUE) | **Retained** on the residue checklist | `MARK_II_AREA_PLAN.md:66-67`, `:317`, `:1007` unchanged |
| R558-5-R1 (RESIDUE) | **Retained** on the residue checklist | `AREA_BUDGET.md:362`, `:379`; `MARK_II_AREA_PLAN.md:666` unchanged |
| R558-6-S1 (SUGGESTION) | **Retained**, optional; my probe `u1` reproduces it | `receipts/reviewer_probes.log` |
| R558-6-S2, R558-7-S2, R559-6-S2, R559-6-S3, R559-5-S1, R558-3-S1/S2, R559-3-S1, R558-4-S1/S2, R559-4-S1/S2, R559-1-S1..S4 (SUGGESTION) | **Retained**, optional, no lens effect | Cited sources unchanged where applicable; the PR body lists S2/S3 as known limitations |

## 5. Lens results (same format as findings)

- `[R558] PASS Conformance - KL_maap.sv:146-154,163-178,202,222-225,281-282,315-339,383-386,402,424-425,432-443,464-471; milan_datapath.sv:7171-7172; issue #696 acceptance 1-3 and comment 6102832618`
  - Each item was checked against its cited clause, as the issue states it:
    - M4: seed at first enable from the programmed MAC plus PHC; the datapath check and its reset-time plant are in the default campaign.
    - M2: requested_start and all 16 count bits are echoed (B.3.6.6).
    - M7: a supplied range must lie inside 0..0xFE00, with the boundary kept (Table B.9).
    - M8: truncation or a missing keep strobe through byte 41 is discarded with no effect (B.2); counting is withdrawn by ruling and recorded at `MAAP_FABRIC.md:186-188`.
    - M1: compare_MAC in the rProbe!/PROBE and rDefend!/DEFEND cells (Table B.7 note d).
    - M5: a rising `eff_link_w` revokes and re-probes, and a falling one is no event (B.3.5.9).
    - M6: one shared response buffer; its capacity limit is justified at `MAAP_FABRIC.md:171-185`.
    - M3: a 32-bit generator `x^32+x^22+x^2+x+1` with period 2^32-1, checked from the RTL map. The pool-fold bias is justified at `:158-170`.
  - The recorded separation criterion holds for every seed (independent model).
  - Acceptance 3: MAAP 490/340, +51/+60, within the ceiling; three records re-written with `check-baseline` PASS.
  - Acceptance 4 is not this lane's.
- `[R558] PASS RTL - KL_maap.sv:137-203,248-253,268-276,341-507; milan_datapath.sv:2934-2935,3000-3001,7168-7178; receipts/lint.log`
  - The new inputs are synchronous to `axis_clk`: the PHC is on `gtx_clk == axis_clk`, and `eff_link_w` is already consumed synchronously at `:3589-3615`.
  - Every new flop has a synchronous reset value (`:349-373`).
  - The 17-bit range ends cannot overflow, and the `seed_end_w` and `req_end_w` widths are correct.
  - In priority order (disable, Restart!/PortOperational!, DEFEND, timer), `save_probe_w` and `defend_w` are mutually exclusive, and the pending buffer is cleared on every allocation loss.
  - The first draw's added logic is in the recorded route with +3.906 ns incoming slack (`234_PP_SHADOW_AREA_BASELINE.md:34-108`).
  - Lint stays at 90 <= 90. There is no register-map, filter or mailbox change; the datapath diff since `e8454e27` is two port connections and one comment.
- `[R558] PASS Robustness - sim_main.cpp:781-941; receipts/reviewer_probes.log (u2-u5,u7,u8); receipts/fold_model.log (zero-sum pairs)`
  - Exercised and passing:
    - truncated lengths 1..41 and every single missing byte 0..41 for each message type, cycle-matched against idle RX;
    - reset, disable, link return and conflicting ANNOUNCE while a DEFEND is pending;
    - link outage longer than a walk;
    - supplied-seed boundaries for counts 1, 8 and 255;
    - backpressure across a pending DEFEND.
  - Six of my robustness plants are rejected.
  - The one-response capacity limit is documented, not hidden. A count of 0 makes the `< POOL_SIZE_C` term reachable only for an empty range, which never conflicts.
- `[R558] PASS Tests - receipts/unit.log (186/0), integ.log (5/0), coverage.log (225/225), mutants.log (65 rows, 63 named rejections, 2 controls), differential.log.gz (12/12, 17/17), p7_copy.log (186/9); sim_main.cpp:1083-1276; mutants.py:43-224`
  - Each new check failed for its claimed defect in the campaign.
  - Section [13] derives its constants from the RTL (`POOL_SIZE_C`, `PROBE_MIN_MS_C`, learned maps), so a constant change is graded as it stands.
  - Real integration wiring is graded by three of my datapath probes.
  - The one escape (`u1`) is an ungraded implementation detail that no contract states. It is retained as R558-6-S1.
- `[R558] PASS Docs - docs/design/MAAP_FABRIC.md:50-76,96-129,142-188,211-273; hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5,22-29; KL_maap.sv:12-56; sw/firmware/ctrl/maap/README.md:189-192; docs/design/AREA_BUDGET.md:10,104-129,143-152,371,410,460-470; docs/design/MARK_II_AREA_PLAN.md:56,107-147,650-654; docs/findings/234_PP_SHADOW_AREA_BASELINE.md:1-180; PR #706 body`
  - Every statement about the first draw, the folds, the zero-sum exclusion, the MAC low-32-bit scope and PortOperational! matches the RTL and my model.
  - I recomputed every figure against `pp_resource_baseline.json` (50,013 = 50,230 - 217; 15,753 = 15,823 - 70; WNS 0.233 = 0.114 + 0.119; 11,973 over; wrapper 11,020 / 52 %; MAAP +51/+60).
  - Documentation gates pass. The PR body's p7 command reproduces its stated 9 failures.
  - Wording: SUGGESTION R558-8-S1 only. The open RESIDUE items are prior and retained.

## 6. Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_maap.sv` and the datapath instance against #696 acceptance 1-3, rulings and comment 6102832618; independent first-draw model | R558-8 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |
| RTL | CLEAN | `KL_maap.sv` full read; `milan_datapath.sv:2934-3001,7168-7178`; lint; recorded route slack | R558-8 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |
| Robustness | CLEAN | M5/M6/M7/M8 harness sections; 6 robustness probes; zero-sum fallback pairs | R558-8 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |
| Tests | CLEAN (SUGGESTION R558-6-S1 retained) | unit 186/0, datapath 5/0, coverage 225/225, campaign 65 rows, differential 17/17, p7 copy, 12 reviewer probes | R558-8 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |
| Docs | CLEAN (SUGGESTION R558-8-S1; prior RESIDUE R558-2-R1 / R559-2-R1, R558-5-R1 retained) | 8 pages and the PR body; figures recomputed; documentation gates | R558-8 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |

## 7. Real limits

- **Hardware.** No physical calibration, bench or hardware run, so acceptance 4 is not exercised. Field-campaign skips are not hardware proof.
- **Vivado.** I ran no Vivado measurement.
  - The three records are verified by `check-baseline` and by recomputing their arithmetic, not by re-measurement.
  - The `inputs_sha256` values cannot be recomputed without measurement directories.
  - What I did check: no file under `hdl/` (and no `KL_maap.sv` byte) changed between the measured head `bee1b0d7` and this head (`git diff --stat bee1b0d7 HEAD`).
- **Banks not run.** No parent sweep, portability, firmware bank, field campaigns or processor banks at this head. Those numbers are the author's reports at `30242308` and `d1b18b3f`.
- **Public evidence.** The public archive at `97f433d6` predates rounds 5-7. It does not contain the round-6 Vivado receipts or the round-7 receipts the REVIEW READY cites, so I could not inspect them.
- **Hosted checks.** At the time of reading, 11 of 20 exact-head checks were still queued or in progress.
- **Linearity.** Section [13]'s every-seed claim rests on linearity confirmed on 256 seeds plus the learning pairs. A nonlinearity confined to a few seeds could escape, as the author discloses. My model checks the head constants directly and agrees.
- **Probe toolchain.** The probes and campaigns ran under host GNU make and python3 3.14, not the hosted 3.12 / make 4.3 image.

## 8. Pending manager duties

- Accept the hosted `rtl-fast`, `verilator-suites` and `yosys-portability` contexts at this exact head once they complete; the act replica is also the manager's.
- Validate the current-dev merge candidate:
  - source base `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`;
  - live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`;
  - builder and native banks.
- Decide whether the candidate's resource records need a merge-result re-measure, since dev has moved past `e8454e27`.
- Publish the round-6 measurement and round-7 author receipts with the evidence packet.
- Carry RESIDUE R558-2-R1 / R559-2-R1 and R558-5-R1 on the residue checklist.
- Route acceptance 4 to the post-merge bench lane.
- Obtain the external review verdict. This report is the internal review only.

## Packet

- `REPORT.md` (this file).
- `MANIFEST.sha256` lists every publishable receipt and script.
- **Scripts.** `scripts/run_focused.sh`, `scripts/run_static.sh` and `scripts/run_probes.sh` take `<clone> <packet>`. They expect a pinned-5.050 `verilator` and `verilator_coverage` wrapper in `<packet>/scratch/bin`.
- **Model.** `scripts/fold_model.c` builds with `cc -O2`.
- **Sanitising.** Home-directory paths in three logs were replaced with `<pinned-verilator-root>` / `<home>`. The 13 MB differential log is gzip-compressed.

R558-8 FINISHED
