[R559] POSITIVE - exact head 32582421bbf095a7b5a7d4b953c4d737b86fe54b

# R559-7 external review: issue #696 / PR #706

- **Head:** `32582421bbf095a7b5a7d4b953c4d737b86fe54b`, tree `08c6b95847c5b9b354d0894ef893ee0abb483620`, in an isolated detached clone.
- **Base:** source base `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.
  - The lane's own change is `git diff e8454e275..32582421` (17 files). `e8454e27` is the last dev tip merged into the branch (merge `941ba746`), and it lies on live dev `ac2c5e77`.
  - The rest of `6aa25dec..32582421` is dev content from #672 and #698-#702.
  - Round 7 itself is `d1b18b3f..32582421`: harness, campaign and documentation only. `KL_maap.sv` and every other design input are byte-identical to the measured head `bee1b0d7`.
- **Verdict: POSITIVE.** All five lenses are clean at this head. No BLOCKER, MAJOR or MINOR is open.
  - This round adds one SUGGESTION (S1) and one RESIDUE (R1). Earlier suggestions and residues are retained as listed in section 4.
  - Every finding still open at `d1b18b3f` (R558-7-F1, R559-6-F1, R559-6-F2, R558-7-R1, R559-6-R1) is resolved at this head. I checked each one by execution.
- **Order of work:** I wrote this verdict and the ledger in section 6 before reading any prior or concurrent review report. I read prior findings only afterwards, to resolve or retain them.

## 1. Scope reconstructed from public state

**Frozen acceptance (issue body):**
1. M1-M8: each is conformed, with a suite check and a planted defect, or justified by clause in `MAAP_FABRIC.md`.
2. M4 is fixed in RTL first: the seed is taken at enable or at MAC programming. A datapath check shows two MACs drawing different intervals.
3. OOC area and one shipping route stay within budget, and the records are re-recorded through the recipe.
4. Bench interop.

**Assignment and rulings on #696:**
- 6076750392: scope; the +60 LUT / +60 FF STOP rule; no register-map, filter or mailbox change; acceptance 4 goes to a post-merge bench lane.
- 6076940309: M8 discards without counting, and the missing count is a recorded B.2 deviation.
- 6079087547: the ceiling applies to `g_maap.maap_engine`; M6 uses one shared buffer; M3 only within headroom.
- 6079463350: the differential stimulus is authorized.
- 6080332335: consumer documentation pages are authorized.
- 6089712293: merge dev and re-measure, with no floor exception.
- 6097504752 (round 6): the first draw steps the full seed.
- **6102832618 (round 7) records the binding first-draw criterion:**
  - seeds 2^i apart, with any carry, claim disjoint first blocks of 1..8 through the pool fold and the clip;
  - seed bits 16..31 map one-to-one onto the offset word;
  - other pairs carry no guarantee.
  - It also requires the R558-7-F1 and R559-6-F1/F2 changes.

**Authorities:**
- IEEE 1722-2016 Annex B, as cited by the issue: B.2, B.3.4 NOTE, B.3.5.9, B.3.6.1, B.3.6.3, B.3.6.4, B.3.6.6, B.4, Tables B.3, B.7 and B.9.
- `MAAP_FABRIC.md`, `KL_maap.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`.

## 2. Findings of this round

### R559-7-S1 - SUGGESTION - Tests, Robustness - `hdl/ieee1722/maap/KL_maap.sv:464-466`, `:332`, `:203`; `docs/design/MAAP_FABRIC.md:124`, `:52-55`, `:99` - three documented details are correct at this head but no check grades them

- **Evidence (probe set run with `scripts/campaign.py`, `receipts/campaign.log`):** each of these probes builds and passes all 186 unit checks (rc 0).
  - `p_m5_link_keeps_offset` keeps `offset_r` on a PortOperational! restart. `MAAP_FABRIC.md:124` says the event "draws a fresh range", and the C core's `restart()` (`sw/firmware/ctrl/maap/maap.c:117-123,237`) also draws afresh. `port_return_reprobes` and `port_loss_is_no_event` walk on `dut->offset_o` and never compare it with the pre-outage range.
  - `p_m7_count0_offset_bound` drops `seed_offset_i < POOL_SIZE_C`. This differs only at count 0, where a supplied `0xFE00` is refused today. `supplied_seed_bounds` uses counts 1, 8 and 255 only.
  - `p_m3_announce_from_fold` draws the announce interval from the probe fold instead of `lfsr_r[9:0]`, which `MAAP_FABRIC.md:99` documents. The draw stays in bounds and random, so no clause is affected.
- **Impact:** a later edit could change these documented behaviours silently. None is an acceptance item, and none is a defect at this head.
- **Optional outcome:** the next harness change can add:
  - an M5 assertion that the post-return range is a fresh draw: with the generator state known, compare it with `rand_offset(lfsr_r[15:0])` at the event;
  - a count-0 supplied-seed boundary row.
- **Verification:** both probes fail a named check.

### R559-7-R1 - RESIDUE - Docs - PR #706 body, "Known limitations / out of scope", last bullet - the sentence is stale now that the head is pushed

- **Evidence:** the body says "Hosted checks and the local workflow replica need the pushed head." The head is now pushed, and hosted contexts are running at it (`receipts/hosted_checks_snapshot.tsv`).
- **Why RESIDUE:** this is PR-body wording only. It changes no figure, check, verdict or clause claim.
- **Exact fix:** replace the sentence with "Hosted checks run at the pushed head `32582421`; hosted and local-replica acceptance belongs to the manager."

### Probe observations that reproduce retained suggestions (no new finding)

- `p_m2_own_count_live` (own requested_count read from live `count_i`) escapes, 186/0. This is retained **R558-6-S1**. `MAAP_FABRIC.md:71-72` disclaims reconfiguration during a frame.
- `p_m4_rebegin_reuses_first_fold` (every Begin! re-folds) escapes, 186/0. This is retained **R558-7-S2 = R559-6-S3**, disclosed in the PR body.
- `p_q8_first_draw_count_fixed_8` (the Begin! draw clipped for 8 whatever `count_i` is) escapes, 186/0 (`receipts/probe_q8_first_draw_count.txt`).
  - This is retained **R559-6-S2**, older than #696 and disclosed in the PR body. Section [13] claims counts 1..8, so it cannot see a fixed-8 clip.
  - The gap only matters for blocks larger than 8. A separate Issue remains the right home.

## 3. Executed evidence (this round, exact head)

Pinned simulator `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/tool_identity.txt`). Builds wrote only to scratch. Commands ran unpiped, and every rc is in its receipt.

| What | Command | Result | Receipt |
|---|---|---|---|
| Unit harness | `make -C tb/verilator/maap run MDIR=<scratch>` | rc 0; **186 checks, 0 failures**. [12]: 32 / 136 / 360 / 32 / 48 sampled pairs plus 4 + 2 fixed. [13]: offset image 16 bits, probe image 6 bits, 65,536 words x 8 counts, least spare 1 | `maap_unit.log` |
| Real datapath | `make -C tb/verilator/maap integration-build DP_MDIR=<scratch>`; `./maap_integration` | rc 0; **5 checks, 0 failures**. First offsets 0x7029 / 0x9821 (adjacent MACs) and 0xf229 / 0xf1cd (PHC). Link return gives 4 to 8 PROBEs | `maap_integration.log` |
| Coverage | `make -C tb/verilator/maap coverage COV_MDIR=<scratch>` | rc 0; `KL_maap.sv` **225/225** lines, gate PASS | `maap_coverage.txt` |
| Campaign plus probes | `python3 -I scripts/campaign.py <clone> <scratch> 12` | rc 0. Replays the suite's own `MUTANTS` and `DATAPATH_MUTANTS` under the suite's kill rule (build rc 0, harness rc 1, `[FAIL] <named check>`). 2/2 controls PASS. **63/63 defects KILLED** at their named checks (58 unit, 5 datapath). Each round-7 plant fails only its section [13] check, and `m2_echo_overlap_start` fails only the new below-offset M2 check. 21 reviewer probes: 6 KILLED at named checks, 10 CAUGHT, 5 ESCAPED (section 2). The killed and caught set includes datapath wiring faults (`port_operational_i` tied high; `realtime_ns_i` tied 0 or the PHC's high word), single-term M6 cancel removals, M8 keep/rearm variants and M1 compare variants | `campaign.log` |
| First-draw proof, independent of the suite | `python3 -I scripts/first_draw_proof.py KL_maap.sv` | rc 0. Constants are parsed from the RTL. A: all 528 carry runs x 65,536 words x counts 1..8 disjoint (least spare 1). B: every run gives a different first probe fold. C: bits 16..31 have rank 16. D: joint rank 22. E: offset map rank 16. Independent-draw overlap rate is 15.4 per 65,024 (documented "about 15") | `first_draw_proof.txt` |
| Proof non-vacuity | `scripts/make_plants.sh`, then the proof on each plant | q9: A fails (32 violations). q3: C fails (rank 15). Repeated probe row: B and D fail. Each rc 1 | `first_draw_proof_negatives.txt` |
| Extra probe | the suite's `build` target on a scratch copy with the Begin! clip count fixed at 8 | 186/0, escapes (retained R559-6-S2) | `probe_q8_first_draw_count.txt` |
| Firmware differential | `maap_differential.py --self-test --keep <scratch>` | rc 0. Clean **12/12**; parent 5172..5810 cycles over 1,024 MAC/phase pairs; **17/17** defects caught, `parent-ignores-mac` included | `differential_summary.txt` |
| Record gate | `syn/ooc/pp_resource_gate.py check-baseline` | rc 0; `baseline PASS: 3 endpoints` | `check_baseline.txt` |
| Plan against the record | inline cross-check of `MARK_II_AREA_PLAN.md` inventory against `pp_resource_baseline.json` scopes | 22 rows, 66 figures, 0 differences | `plan_vs_record.txt` |
| Documentation and static checks | `docs_check.py`; `gen_toc.py --check` and `check_em_dash.py --base e8454e27` (pinned renderer in a scratch venv); `gen_module_matrix.py --check`; `check_doc_paths.py`; `measure_test_evidence.py --check`; `lint_rtl.py --check --jobs 8` | All rc 0. docs_check: 0 findings. Em dash: 0 findings over 339 added lines. Module matrix up to date. 957 paths resolve. Lint 90 <= 90 | `docs_check.txt`, `gen_toc.txt`, `em_dash.txt`, `gen_module_matrix.txt`, `check_doc_paths.txt`, `measure_test_evidence.txt`, `lint_rtl.txt` |
| Hosted contexts (read only) | `gh api .../commits/32582421.../check-runs` | At 00:46Z: 17 completed success, Physical gPTP SKIPPED (not an execution), Verilator shards 1/5, 2/5 and 4/5 in progress | `hosted_checks_snapshot.tsv` |
| Restore | `diff-index`, `diff-files`, `write-tree`, per-blob rehash and mode check, `ls-tree` gitlinks, `submodule status` | HEAD and tree exact; index equals HEAD; 0 blob or mode mismatches; 0 untracked or ignored entries. Gitlinks: protocol-processor `2ad2f845`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`, lwSRP `9197193e`, external `efeb541a`. Submodules clean | `restore_verify.txt` |

Other checks done by reading the source:
- **Design inputs:** `git diff bee1b0d7..32582421` touches only documentation, `pp_resource_baseline.json` (the record write) and the MAAP harness/campaign. No `hdl/*.sv`, `sw/`, `configs/` or submodule change.
- **Record write:** in `b7f342ae` only `record` and the `measured` notes changed. Identity, policy and top-level keys are unchanged.
- **Area arithmetic, recomputed:** 50,013 / 63,400 = 78.88 %; 11,973 LUT over; 97 slices free; wrapper limit 11,020; WNS fall 0.203 ns; deltas -217 / -2 / -70 / +0.119 / -0.019; wrapper +120 / -6.
- **Clock domains:** `gtx_clk` and `axis_clk` are both `ClockSignal(milan_cd)` in `sw/litex/milan_soc.py:811-813`, so `realtime_ns_i` adds no crossing.

## 4. Prior public findings on this PR, at this head (read after my own pass)

| Finding | Status at `32582421` | Evidence |
|---|---|---|
| R558-7-F1 (MINOR, Tests): M2 requested_start not graded for a PROBE starting below this station's offset | **Resolved** | `sim_main.cpp:433-440` reads the DEFEND's requested start at `[4b]`. `m2_echo_overlap_start` (`mutants.py:125-127`) is killed with exactly 1 failure at that check (`campaign.log`) |
| R559-6-F1 (MINOR, Tests, Conformance): first-draw checks named for an unmet property; criterion not narrowed | **Resolved** | Manager comment 6102832618 records the criterion, and `MAAP_FABRIC.md:112` cites it. Checks are renamed to what they grade (`sim_main.cpp:1126-1136`); fixed pairs are named as fixed pairs (also `sim_integration.cpp:158`, `:186`). Campaign anchors follow, and every one of them is killed by name |
| R559-6-F2 (MINOR, Tests, Docs): universal first-draw claims had no check able to fail | **Resolved** | Section [13] (`sim_main.cpp:1180-1276`) learns both maps from the RTL and restates no constant (it reads `PROBE_MIN_MS_C` and `POOL_SIZE_C` from the model). q3 and q9 are each killed by name, alone. My independent proof agrees on every property and fails on q3, q9 and a repeated probe row |
| R558-7-R1, R559-6-R1 (RESIDUE, Docs) | **Resolved** | Exact texts at `MAAP_FABRIC.md:260` and `:117`, and in the PR body's "What the folds guarantee" bullet |
| R558-7-S1 = R559-6-S1 (unstepped probe fold escapes) | **Resolved (applied)** | `m4_probe_fold_unstepped` is killed at "M4 B.3.4 every seed pair 2^i apart draws different first probe intervals" |
| R558-6-F1 (MINOR; Conformance, RTL, Robustness, Tests) | Still resolved | `KL_maap.sv:154,202,337-339` unchanged since `bee1b0d7`; p7 is killed in unit and datapath |
| R558-6-R1, R558-4-R1 (RESIDUE, PR-body head) | Still resolved | The body names `32582421` under Status and in the state commands |
| R558-5-F1 (MINOR, Docs) | Still resolved | `AREA_BUDGET.md:371` names #696's 50,013-LUT route |
| R558-3-F1 = R559-3-F1 (BLOCKER, `integration.mk`) | Still resolved locally | `integration.mk` is unchanged since `30073ee9`, and the integration build derives its sources here (5/0). Hosted shard 1/5, which owns the MAAP suite, was still in progress at my snapshot (manager duty) |
| R558-1-F1, R559-1-F1/F2/F3 (MINOR) | Still resolved | `MAAP_FABRIC.md:161-168` area steps; the M5 loss check passes and `m5_restart_on_link_loss` is killed; the MARK_II inventory equals the record (66/66); the zero-seed fixture is named `02:00:00:00:00:00` |
| R558-2-R1 / R559-2-R1 (RESIDUE) | **Retained** (residue checklist) | `MARK_II_AREA_PLAN.md:66`, `:317`, `:1007` text unchanged |
| R558-5-R1 (RESIDUE) | **Retained** (residue checklist) | `AREA_BUDGET.md:362`, `:379`; `MARK_II_AREA_PLAN.md:666` text unchanged |
| R558-6-S1, R558-7-S2 = R559-6-S3, R559-6-S2 | **Retained**, optional | Reproduced by my probes (section 2) |
| R558-6-S2, R559-5-S1, R558-3-S1/S2, R559-3-S1, R558-4-S1/S2, R559-4-S1/S2, R559-1-S1..S4 | **Retained**, optional, no lens effect | Cited sources unchanged where applicable. R559-1-S3 (first-draw path depth at a 100 MHz Milan clock) still applies: the shipping route is 50 MHz, with +3.906 ns reported in the routed image |
| R558-8 (concurrent, this head, read after my verdict) | POSITIVE; R558-8-S1 is a SUGGESTION | Consistent with my results: its probe `u1` matches my `p_m2_own_count_live`. `TESTING.md:606` does not name the real-datapath arm, as R558-8-S1 says |

## 5. Lens results (same format as findings)

```text
[R559] PASS Conformance - issue #696 acceptance 1-4 and rulings 6076940309, 6079087547, 6089712293, 6102832618; hdl/ieee1722/maap/KL_maap.sv:141-203,248-259,311-339,380-386,430-497; hdl/milan/milan_datapath.sv:7168-7172; receipts/first_draw_proof.txt, maap_integration.log, check_baseline.txt - M1 compare_MAC in rProbe!/PROBE and rDefend!/DEFEND (:315-320; equal MAC yields); M2 DEFEND echoes rx_start_r and all 16 count bits while conflict_* carry the overlap (:436-443, B.3.6.6); M3 x^32+x^22+x^2+x+1 with the period proven by the harness's order test, seeded from MAC[31:0] + PHC at first enable; M4 sampling at first enable, not reset, with datapath intervals and first blocks differing for different MACs (acceptance 2) and the 6102832618 criterion proven for every seed; M5 rising eff_link_w restarts while a fall is no event (B.3.5.9; ruling 6093171536); M6 shared buffer with its capacity deviation recorded; M7 Table B.9 bounds; M8 discard without effect, counting withdrawn and recorded (MAAP_FABRIC.md:186-188); acceptance 3 MAAP 490/340 (+51/+60, author's measurement) and three records rewritten with policy unchanged, check-baseline PASS; acceptance 4 assigned to the bench lane; no register-map, filter or mailbox change in e8454e27..HEAD
```
```text
[R559] PASS RTL - KL_maap.sv (full file at the head); milan_datapath.sv:2124,2165,2934-2956,3000-3001,7168-7172; sw/litex/milan_soc.py:811-813 - widths (seed_end_w 17 bits, probe_iv_w <= 581, announce <= 31511 in 16 bits, conf_cnt 16, tx_own_cnt 8); the first-draw select only while rng_seeded_r = 0; zero-seed fallback; port_operational_r reset to 0 so the post-reset edge is ignored in IDLE; defend_pending cleared on every exit from ANNOUNCE, which makes the ANNOUNCE term of defend_w redundant but harmless; save/defend mutually exclusive; every new register reset; no new clock crossing (axis_clk and gtx_clk are both milan_cd); FSM default arm and MAAP_P=0 tie-off unchanged; lint 90 <= 90
```
```text
[R559] PASS Robustness - tb/verilator/maap/sim_main.cpp:781-806 (disable, link flap, conflicting ANNOUNCE and reset during a pending response), :836-872 (outage longer than a walk), :874-893 (supplied seeds 0, limit, limit+1, 0xFE00, 0xFF00, 0xFFFF at counts 1/8/255), :895-941 (lengths 1..41 and each missing byte 0..41 for all three types in both states), :442-471 and :536-566 (backpressure at 0/2/4/7 beats); receipts/campaign.log probes p_m8_* (3 caught), p_m6_cancel_* (3 killed), p_dp_link_tied_high (killed) - truncation, boundaries, reset during activity, repeated link events and backpressure are graded and pass at this head; ungraded details are recorded as S1 and the retained suggestions
```
```text
[R559] PASS Tests - sim_main.cpp sections [1]-[13], sim_integration.cpp, mutants.py, maap_differential.py, test_maap_differential.cpp; receipts/maap_unit.log, maap_integration.log, maap_coverage.txt, campaign.log, differential_summary.txt, first_draw_proof*.txt - unit 186/0, datapath 5/0, coverage 225/225, 63/63 suite defects killed at their named checks with 2/2 controls; each round-7 plant fails exactly its intended check; section [13] verified as non-vacuous against an independent proof; differential 12/12 and 17/17; 22 reviewer probes, with every escape a correct-but-ungraded detail (S1, R558-6-S1, R558-7-S2/R559-6-S3, R559-6-S2)
```
```text
[R559] PASS Docs - docs/design/MAAP_FABRIC.md:42-188,197-273; hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5,22-29; hdl/ieee1722/maap/KL_maap.sv banner :12-55 and comments :141-203; sw/firmware/ctrl/maap/README.md:189-192; docs/design/AREA_BUDGET.md:10,104-160,368-371,407-411,460-470; docs/design/MARK_II_AREA_PLAN.md:56,107-147,650-655; docs/findings/234_PP_SHADOW_AREA_BASELINE.md:1-107; docs/findings/README.md:25; PR #706 body - every first-draw, fold, seed, link, M6/M8 deviation and area statement checked against the RTL, the executed results, the record file (66/66; arithmetic recomputed) and the 6102832618 criterion; documentation gates rc 0; RESIDUE R559-7-R1 and the retained residues are wording only
```

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue acceptance and rulings incl. 6102832618; `KL_maap.sv` M1-M8; datapath wiring; independent first-draw proof; records and `check-baseline` | R559-7 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |
| RTL | CLEAN | `KL_maap.sv` (full); `milan_datapath.sv` MAAP instance, link and PHC sources; SoC clock binding; lint | R559-7 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |
| Robustness | CLEAN (SUGGESTION S1) | M5/M6/M7/M8 fixtures; backpressure fixtures; 22 probes, including wiring, cancel, truncation and boundary faults | R559-7 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |
| Tests | CLEAN (SUGGESTION S1; retained R558-6-S1, R558-7-S2/R559-6-S3, R559-6-S2) | Unit 186/0; datapath 5/0; coverage 225/225; campaign 63/63 + 2 controls; probes; differential 12/12 and 17/17; proof non-vacuity | R559-7 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |
| Docs | CLEAN (RESIDUE R559-7-R1; retained R558-2-R1 / R559-2-R1, R558-5-R1) | MAAP design and module pages, firmware README, area budget, Mark II plan, #234 finding, findings index, PR body; documentation gates | R559-7 | `32582421bbf095a7b5a7d4b953c4d737b86fe54b` |

## 7. Real limits

- **Area, timing and records.** No synthesis, route or Vivado run was done in this review.
  - These rest on the author's receipts and are not reproduced here: the MAAP 490 LUT / 340 FF instrument figure, the three endpoint figures at `bee1b0d7`, and the statement that only `KL_maap.sv` differs from the preceding record's inputs.
  - What I verified: no design input changed between `bee1b0d7` and the head; the record is internally consistent and its policy unchanged; `check-baseline` passes; the documented arithmetic holds.
- **Banks not run (not permitted):** the parent suite sweep, processor, gPTP, Yosys and builder banks, behaviour scenarios, `tsn_fuzz`, `xvlog` and the full firmware bank. Their evidence is the author's, at `30242308`, `d1b18b3f` and the head.
- **No manager source bank** exists at this exact head, and none is claimed or inferred.
- **Hosted contexts** were read, not owned. Three Verilator shards, including 1/5 which owns the MAAP suite, were in progress at the snapshot. "Physical gPTP" was SKIPPED, which is not an execution. No act replica was run.
- **Hardware:** physical calibration was NOT RUN. Field skips are not hardware proof. Acceptance 4 (bench interop) is unproven and belongs to the post-merge lane.
- **Annex B text:** the standard's text was not available locally. Clause readings follow the issue, the rulings and `MAAP_FABRIC.md`, cross-read against the repository's firmware MAAP core.
- **Section [13] linearity:** its every-seed result assumes the RTL first draw is GF(2)-linear in the seed, which the harness confirms on 256 seeds plus the learning pairs. My proof establishes the claims for the RTL's actual constants independently, but it is a model of the RTL expressions rather than a simulation.

## 8. Pending manager duties

- Confirm the remaining hosted contexts at the exact head (Verilator shards 1/5, 2/5 and 4/5 were in progress), and own hosted and act acceptance.
- Build and validate the current-dev merge candidate (source base `6aa25dec`, live dev `ac2c5e77`) with the builder and native banks, and publish their receipts.
  - Since `e8454e27`, live dev changes `sw/litex` among others, but no `hdl/`, record or submodule pin.
  - Decide whether the candidate's measured inputs still equal the record before accepting the three endpoints.
- Carry RESIDUE R559-7-R1, R558-2-R1 / R559-2-R1 and R558-5-R1 on the residue checklist.
- Hand acceptance 4 (bench interop with the reference peer) to the post-merge bench lane, followed by post-merge containment.
- Optional suggestions (R559-7-S1 and the retained ones) need no action for merge. R559-6-S2 (Begin! clip for counts above 8) is a candidate for its own Issue.

## 9. Packet

`REPORT.md`, and every file listed in `MANIFEST.sha256`: `scripts/` (portable; paths are passed as arguments) and `receipts/`. Receipts had local absolute paths replaced by `<SCRATCH>` and `<PINNED_VERILATOR_DIR>`; no other byte was changed. `scratch/` is not published.

R559-7 FINISHED
