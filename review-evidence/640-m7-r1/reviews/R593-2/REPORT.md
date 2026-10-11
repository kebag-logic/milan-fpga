[R593] NEGATIVE - exact head 2cc2ba0b8b08010df5ee12c1fc228851fa9a8444

# R593-2: external review of PR #713 (issue #640, Mark II lane M7, plan L10a), round 2

- Head `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444`, tree `bf74cb10132fb94dc1d75b798f0f1a87a80e2d19`, source base dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (16 commits; round 2 adds `84910cb4`, `d46d386f`, `270fcbf5`, `2cc2ba0b` on `9d42762c`).
- Gitlinks at the head: `gptp-processor` `18dd997b2459699e41e5ce9bceca1181e41fa5fe` (unchanged this round; donor diff `5dce647a..18dd997b` is `KL_gptp_timer.sv` and `docs/MANAGER.md`), `protocol-processor` `2ad2f845`, `third_party/verilog-axis` `48ff7a7e`; `external` and `third_party/lwSRP` unchanged.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
- **One MINOR is open (F1, Tests and Docs), so the verdict is NEGATIVE.** Conformance, RTL and Robustness are clean.
- Other open items: one RESIDUE (R-01, PR body) and one SUGGESTION (S-01).
- The product RTL is behaviour-preserving at this head, as far as simulation can show. Two dual-instance differentials found no difference between the head plane and the dev-base plane on any compared output: 32.1 M cycles on the `gptp_tables` stimulus and 43.4 M cycles on the `gptp_shadow` stimulus. A planted defect makes each differential fail. F1 is a gap in what the new suite's documentation says its evidence covers, not a product defect.
- All five prior public findings from R592-1 that needed a change are resolved at this head, and so are R593-1's R-01, R-02, S-01 and S-02. R593-1-S-03 is retained as a pre-existing SUGGESTION, routed to #495 by the manager.

## Reconstruction

Read in this order: `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`; then the issue #640 body and the lane M7 assignment (6097272538), the executor's TAKEN (6097298086), REVIEW READY round 1 (6100339945), the round-2 assignment (6100980189) and REVIEW READY round 2 (6103827621); then the PR #713 body; then `git diff e8454e27..2cc2ba0b` with its history and the donor diff `5dce647a..18dd997b`. The interface authorities read were `third_party/verilog-axis/rtl/axis_fifo.v` and the engine's result face and event word (`KL_gptp_engine.sv:338-350,480-519`, `gen_gptp_ucode.py:360-376`). The public evidence read was `3e0f36b8/review-evidence/640-m7-r1` (`MANIFEST.json`, `author/HANDOFF.md`, `author/PR-BODY.md`). Prior public review reports (R593-1, R592-1) were read only after this round's own pass over the diff and all of its probes were complete.

Frozen scope (assignment 6097272538 and round 2 6100980189):
- Move eligible fabric gPTP plane tables into block RAM, or narrow their indices, measuring first. Keep the dual-read operand files. Target about 500 LUT (300-700), reported honestly. Block RAM may grow only within the firmware ledger. A read-latency change needs deterministic bounds. No change to gPTP behaviour, its register map or its timestamp path.
- Proof: the named suites in both shapes; per-table lockstep with planted wrong-depth, wrong-read-latency and index-alias defects, each failing a named check; the integrated route and the resource gate through the M0s recipe; no re-record before M9 (D7).
- Round 2: fill the result queue with named coverage and a write-index control (R592-1-F1). Add a directed TX lane decode check for counts 0-8 (R592-1-F4). State in the README that the tag column is one-valued (R593-1-S-01). Note #714 (R593-1-S-02). Apply residues F2, F3 and F5.

## Independent executions at this head (receipts under `receipts/`)

Every run used the pinned Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`). The clone was restored afterwards (`receipts/clone_integrity.txt`).

| What | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/gptp_tables` in the clone (suite, then the author's `mutants.py`) | rc 0. 24/24 checks over 32,100,038 cycles. Results 3 deep, 110 written behind a waiting result; `tx_fifo decode: counts 0x1ff driven, 0 decoded wrong`; ledger `tags 0x2`; `0 lost results, 0 barriers`. **17/17 controls caught, each by its own named check**, including `results_write_index` by `results lockstep` and `tx_fifo_decode_odd_counts` by `tx_fifo decode` | `gptp_tables_full.log`, `.rc` |
| Dual differential A: the exact-head `gptp_tables` stimulus driving the head plane and a dev-base plane (`e8454e27` shadow and txret, donor `5dce647a` timer) side by side. Compared every cycle: the lane outputs, publication, PHC, debug counters, the engine byte faces, the tap FIFO strobes, the result face while offered, the departure take, the credit hold, the ledger occupancy and the timer events | **0 mismatching cycles** of 32,100,006 compared; 94,787 TX beats; 10,529 results taken; 28/28 | `dual_differential.log` |
| Dual A, first build (kept for transparency) | 40,515 mismatches, all on the bench's raw, unqualified `dbg_eng_txts_{ns,seq,type,ok}` nets while no result was accepted. After a warm reset, the head's un-reset result RAM shows stale words where the dev registers show zero. The engine samples those nets only on an accepted beat (`KL_gptp_engine.sv:349-350,484-489`), so the comparison was qualified by acceptance. The rerun above counts the idle divergence separately (40,515 cycles) | `dual_differential_v1_unqualified_dbg.log` |
| Dual differential B: the exact-head `gptp_shadow` stimulus (record faults, barriers, link guard, PHC load, observer reset), all 73 slice outputs compared every cycle; the raw result-face outputs are compared on acceptance | **IDENTICAL**: 0 mismatching cycles of 43,358,586 compared; 776 TX beats; 79 results accepted; the suite's own 309/309 still passes | `shadow_dual.log` |
| Fault controls for both differentials | Dual A with a timer write alias: 20,708,198 mismatching cycles. Dual B with the result `ok` field stuck at 1: verdict DIFFERENT, 46 outputs differ. Both differentials can fail | `dual_control_timer_write_alias.log`, `shadow_dual_control_results_ok_stuck1.log` |
| Random initial state: `gptp_tables` built `--x-initial unique`, run `+verilator+rand+reset+2`, seeds 11 and 29 | ledger, results and timer locksteps 0 mismatches at both seeds, so no reader samples an unwritten word of the un-reset RAMs. `tx_fifo lockstep` shows 2,431,227 cycles at both seeds; with its idle `tdata`/`tkeep`/`tlast` terms qualified by valid (scratch copy only), it is 0. The divergence is only never-written FIFO words on an idle output: zero-initialised in hardware in both forms, and don't-care under AXI-Stream | `xinit_random_init.log`, `xinit_validonly.log`, `xinit_validonly.note` |
| Reviewer mutation probes in private copies (`scripts/probe_mutants.py`) | Caught by the named check: RX FIFO twice as deep, result `seq` written at the head, ledger `type` written at the head, timer deadline write alias. **Survived `gptp_tables` 24/24:** result `ok` stuck at 1, result `gen` stuck at 1, and ledger tag stuck at 1 (already disclosed) | `probes_summary.txt`, `probes/*.log` |
| The same survivors on the existing suites | `ok` stuck at 1 is caught by `gptp_shadow` (305/309). `gen` stuck at 1 survives `gptp_shadow` 309/309 and `gptp_txts` 85/85. The tag stuck at 1 survives `gptp_shadow` 309/309. `gptp_txts` was built with its stale-chain regeneration check skipped (no LiteX here; the converted chain file is unchanged by this diff); its baseline is 85/85 | `probes/*.gptp_shadow.log`, `probes/*.gptp_txts.{cmd,log}` |
| 28 repository gates the diff touches, plus `sweep_shape` rerun (`scripts/run_gates.sh`) | All rc 0, including `check_gptp_docs` with and without the submodule, `docs_check`, the module matrix, TOC, doc style, `check_em_dash --base`, doc paths, the doc map, submodule docs and diagram, the time-sync diagram, diagram PNGs, the idiom and naming ratchets, test evidence, hygiene, RTL source lists, port contracts, `pp_resource_gate.py check-baseline`, `lint_rtl.py --check`, donor `make contract` and `make lint`, and `git diff --check` base..head. `sweep_shape` was rc 1 under the 3.12 interpreter only because PyYAML is absent there; under the host interpreter with PyYAML it is rc 0 | `gates_summary.txt`, `gates/*` |
| Round-2 RTL change | `git diff 9d42762c..2cc2ba0b -- hdl` changes 0 non-comment lines; no gitlink moves | (command in this row) |
| PR-body checkout command on a fresh clone | `git switch --detach 640-m7` fails (rc 128); `git switch --detach origin/640-m7` works | `pr_body_switch_probe.log` |
| Hosted runs at the exact head | none yet at 01:06Z: 0 check runs, 0 workflow runs, combined status pending with 0 statuses | `hosted_checks_at_head.tsv` |

## Findings

### F1: MINOR (Tests, Docs). The result queue's `ok` and `gen` columns are one-valued in the lockstep, and the suite's stated limits name only the tag column

- **Location:**
  - `tb/verilator/gptp_tables/README.md:54-67` ("Two limits of the evidence") and the `results` rows at `:18` and `:31`;
  - `tb/verilator/gptp_tables/sim_main.cpp:10-24` (the per-table claim) and `:498-499` (the results coverage line, which prints no column values);
  - the comparison at `tb/verilator/gptp_tables/gptp_tables_wrap.sv:412-417`;
  - the table under test: `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:699-707` (`result_ram`, which this lane introduced; `res_ok_r` at `:704`, `res_gen_r` at `:705`).
- **Authority:** AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect" and "Tests do not merely reproduce implementation assumptions"; Docs: "The PR and Issue contain enough evidence for another cold reviewer". The round-2 assignment (6100980189, item 2, R593-1-S-01) set the standard for this suite: a column the lockstep sees with one value only is stated in the README, or the run counts its values.
- **Evidence:**
  - Probes `results_ok_stuck1` (`res_ok_r[res_tail_w] <= 1'b1`) and `results_gen_stuck` (`res_gen_r[res_tail_w] <= TXTS_GEN_W_P'(1)`) leave `gptp_tables` at 24/24 (`probes/results_ok_stuck1.gptp_tables.log`, `probes/results_gen_stuck.gptp_tables.log`). The reference writes `ok` and `gen` from the untouched `res_ok_w` and `gen_r` (`gptp_tables_wrap.sv:388-394`). So every result the lockstep compares is a measurement (`ok` = 1) of generation 1, consistent with the run's own `0 lost results, 0 barriers`.
  - That is exactly the property the README discloses for the ledger tag column, and it holds for two more columns of the converted result queue. The README's list of limits ("Two limits of the evidence") does not include them, and the coverage line prints `tags 0x2` for the ledger but no values for `ok` or `gen`.
  - Coverage elsewhere: `ok` stuck at 1 is caught by `gptp_shadow` (4 failures). `gen` stuck at 1 survives `gptp_shadow` 309/309 and `gptp_txts` 85/85. The engine carries `gen` at event bits 27:24, above `TXQ_MASK_C` (`KL_gptp_engine.sv:513-519`, `gen_gptp_ucode.py:370-376`), and no microcode reads it. So a `gen` defect is behaviourally inert past the engine today, but nothing in the lane's evidence would show one.
  - The product is not wrong at this head: both dual differentials are identical, and differential B compares results with `ok` = 0 (the `ok`-stuck control turns it DIFFERENT).
- **Impact:** a reader of the suite's documentation takes a zero `results lockstep` count as evidence for every column of the converted result queue. For `ok` and `gen`, any value-dependent defect (wrong write source, stuck bit) in the new RAM passes the lane's own suite. `ok` is caught only by a different suite, and `gen` by none. The suite's explicit statement of its limits is incomplete in the same way the round-2 assignment required the lane to correct for the tag column.
- **Required outcome:** one of these two.
  - The README (with the harness header if it keeps a per-table claim) states that the result queue's `ok` and `gen` columns are one-valued under this stimulus: every result is a measurement of generation 1, with no lost results and no barriers. It also states where `ok` is covered (`gptp_shadow`) and that `gen` has no consumer past the engine's masked claim compare. The run prints the `ok` and `gen` values it compared, as it does for the ledger tags.
  - Or the lockstep reaches results with `ok` = 0 and with `gen` other than 1 (for example, a record-fault or barrier phase), grades both as named coverage, and `mutants.py` carries `ok`-stuck and `gen`-stuck controls that fail `results lockstep`.
- **Verification:** the README text and the run's results line. For the second option, `make -C tb/verilator/gptp_tables` with both new controls reported `caught by "results lockstep"`. Either option un-covers Tests and Docs only.

### R-01: RESIDUE (Docs). The PR body's checkout command fails on a fresh clone

- **Location:** PR #713 body, "How to get into the same state": `git switch --detach 640-m7`.
- **Evidence:** on a fresh clone with only the remote branch, that command fails (`fatal: '--detach' cannot be used with '-b/-B/--orphan'`, rc 128), while `git switch --detach origin/640-m7` works (`pr_body_switch_probe.log`).
- **Impact:** wording in the PR body only. No measurement, figure, verdict, test or code changes.
- **Exact fix:** replace `git switch --detach 640-m7` with `git switch --detach origin/640-m7`.
- **Verification:** the command checks out the head on a fresh clone once the branch is published.

### S-01: SUGGESTION (Tests). One coverage check cannot fail

- **Location:** `tb/verilator/gptp_tables/sim_main.cpp:522`, `tx_fifo coverage: decode driven with counts 0 to 8`.
- **Evidence:** `dec_counts` is set by the harness loop itself (`sim_main.cpp:453-459`) for every count, whatever the plane does, so the check is 0x1FF by construction. The directed decode check that can fail is `tx_fifo decode` (`:513`), and its control is caught.
- **Suggested outcome:** drop the tautological line, or derive it from what the plane presented.

## Prior public review findings at this head (read after this round's own pass)

| Prior item | Status at this head | Basis |
|---|---|---|
| R592-1-F1 MINOR (Tests): results queue never held two results; no write-index control | **Resolved** | Slow-engine phase (`gptp_tables_wrap.sv:171-189`, `sim_main.cpp:432-443`); my run: `3 deep, 110 written behind a waiting result`. Graded coverage `results coverage: two or more results outstanding` (`sim_main.cpp:535`). Control `results_write_index` caught by `results lockstep`. My own `results_seq_write_index` probe is also caught. The per-table claim is narrowed (`sim_main.cpp:10-24`, `README.md:26-32`) |
| R592-1-F2 = R593-1-R-02 RESIDUE: three FIFO-output comments | **Resolved** | `KL_gptp_shadow.sv:236-242`, `:258-261`, `:877-879` carry the reviewers' texts |
| R592-1-F3 = R593-1-R-01 RESIDUE: plan eligibility sentence | **Resolved** | `MARK_II_AREA_PLAN.md:690-691` carries the reviewers' text, including the `tsf_r` option |
| R592-1-F4 SUGGESTION: odd TX lane counts never decoded | **Resolved** | Directed decode `sim_main.cpp:450-462`, check `tx_fifo decode`, `counts 0x1ff driven, 0 decoded wrong`; control `tx_fifo_decode_odd_counts` caught |
| R592-1-F5 RESIDUE: "40/40 engine mutants" label | **Resolved** for the current hand-off | REVIEW READY round 2 (6103827621) gives "40/40 donor mutants (engine 33, gaskets 4, tsngen 3)". The round-1 artifact at `3e0f36b8` is historical and unedited, as that comment states |
| R593-1-S-01 SUGGESTION: tag column one-valued | **Resolved** | `README.md:56-60`; the run prints `tags 0x2`. F1 above extends the same property to the result queue's `ok` and `gen` columns, which R593-1 did not report |
| R593-1-S-02 SUGGESTION: no per-reset-segment coverage | **Resolved as a note** | `README.md:61-67` cites #714 (open) and defers per-segment coverage to its fix |
| R593-1-S-03 SUGGESTION: the lane guard admits widths the classifier and gearbox cannot serve | **Retained**, pre-existing | Unchanged at `KL_gptp_shadow.sv:271`; the round-2 assignment routes it to #495 at merge |

## Lens results

```text
[R593] PASS Conformance — assignment 6097272538 and round 2 6100980189 vs KL_gptp_shadow.sv:230-290,316-330,423-473,567-611,777-890, KL_gptp_txret.sv:328-360,530-600,630-740, gptp-processor KL_gptp_timer.sv:73-130, MARK_II_AREA_PLAN.md:557-560,672-719,849-853, AREA_BUDGET.md:197-201,266-268, REVIEW READY 6103827621 — five tables changed storage, none narrowed; rf_r untouched. Widths, depths and read latency unchanged: both FIFOs keep their beat depth (DEPTH = BYTES/KEEP_W_C with KEEP_ENABLE=0), every converted table keeps one write and a combinational read at the same address. No port list, CSR, wire or timestamp file in the diff; dual differentials A and B identical on every compared output, including the result face and the lane. Block RAM freed (RAMB18 27 to 25), never added. Route figures re-derived: -369/-1,193/-6/0,-2/-0.177,-0.012 against route-1x1; D7 respected. The below-range saving (plane 107-253 against 300-700) is stated as not met in the plan, the budget, the PR and the issue; its acceptance is the manager's decision. Round-2 items 1-3 are present; item 4 is n/a (#621 unmerged).
[R593] PASS RTL — KL_gptp_shadow.sv:244-247,271-276,316-326,430-475,567-611,777-890; KL_gptp_txret.sv:339-357,537-541,590-599,633-646,699-740; KL_gptp_timer.sv:76-125; axis_fifo.v:137,223-246; KL_gptp_engine.sv:349-350,484-489,513-519 — the RX highest-lane encoder is the base serializer's rule moved ahead of the FIFO, and the TX count decode equals the base gearbox mask (gb_keep_r was only lanes 0..idx-1; no other path cleared gb_idx_r). CNT_W_C'(gb_idx_r)+1 cannot overflow 4 bits. tuser bit 0 alone judges a bad frame. The RAM writes take the base write conditions, gated by rst_n as the base reset branch was. Every read of an un-reset word is guarded by n_led_r != 0, txts_valid_o with an accept-only consumer, or armed_r; the random-initial-state run confirms it for all three RAMs. Single clock domain, no CDC touched. Lint ratchet and donor lint rc 0.
[R593] PASS Robustness — dual_differential.log, shadow_dual.log, xinit_random_init.log, xinit_validonly.log, gptp_tables_full.log — malformed, runt, oversize and foreign frames, corrupted tkeep, 33,354 overflow and 12,751 bad drops, 12.1 M stalled TX cycles and two warm resets in traffic run in lockstep with zero mismatches. Dual B adds record faults, barriers, link-guard episodes, PHC loads and observer resets with all 73 slice outputs identical over 43.4 M cycles. The un-reset RAMs start random in the random-initial-state run and their consumers still match. The only random-state divergence is never-written FIFO words on an idle output, which are zero in hardware in both forms. Configuration: the new guard refuses more than 8 lanes; pre-existing S-03 retained.
[R593] UNCLEAN Tests — F1 — tb/verilator/gptp_tables/{gptp_tables_wrap.sv,sim_main.cpp,mutants.py,README.md,Makefile,waivers.vlt}; gptp_tables_full.log (24/24, 17/17 controls); probes_summary.txt (4 of 7 reviewer probes caught by the named check; ok-stuck and gen-stuck survive undisclosed, tag-stuck survives as disclosed); probes/*.gptp_shadow.log; probes/*.gptp_txts.log — the oracles are the previous storage forms written from untouched signals; the slow-engine force holds both sides of the result handshake, fabricates nothing, and its lint waiver is scoped to the three forced nets. S-01 is a suggestion.
[R593] UNCLEAN Docs — F1 — tb/verilator/gptp_tables/README.md:54-67; MARK_II_AREA_PLAN.md, AREA_BUDGET.md, TESTING.md:150,409-410,601, regenerated MODULE_MATRIX and README-tests, the eight donor pin-link pages, rom_digests.tsv, KL_gptp_shadow.sv comments; gates/* (all doc gates rc 0) — every figure and comment checked. F1's missing limit statement is in the suite README; R-01 is PR-body wording only.
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 6097272538, round 2 6100980189, D7; shadow, txret and donor timer RTL at the lines above; `MARK_II_AREA_PLAN.md`, `AREA_BUDGET.md`; REVIEW READY 6103827621; `dual_differential.log`, `shadow_dual.log` | R593-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |
| RTL | CLEAN | `KL_gptp_shadow.sv`, `KL_gptp_txret.sv`, `KL_gptp_timer.sv` (pin `18dd997b`), `axis_fifo.v` (pin `48ff7a7e`), `KL_gptp_engine.sv:349-350,484-489,513-519`; `xinit_random_init.log`; `gates/lint.log`, `gates/gp_lint.log` | R593-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |
| Robustness | CLEAN | `gptp_tables_full.log`, `dual_differential.log`, `shadow_dual.log`, both dual fault controls, `xinit_random_init.log`, `xinit_validonly.log` | R593-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |
| Tests | UNCLEAN (F1 open; S-01 suggestion) | `tb/verilator/gptp_tables/*`; `gptp_tables_full.log`; `probes_summary.txt`, `probes/*` | R593-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |
| Docs | UNCLEAN (F1 open; R-01 RESIDUE carried) | suite README; `MARK_II_AREA_PLAN.md`, `AREA_BUDGET.md`, `TESTING.md`, `MODULE_MATRIX.md`, README-tests, pin-link pages, `rom_digests.tsv`; PR body; `gates/*` | R593-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |

## Real limits of this round

- **No integrated route and no Vivado run.** The route figures, the gate `check` PASS against route-1x1, the post-synthesis and out-of-context attributions and the primitive census are the author's. Their files are not public (the hand-off lists digests only). I checked them for arithmetic and against the committed record only.
- **Not run here:** the full sweep, `milan_dp`, `milan_dp_gptp`, `tsn_fuzz`, the Yosys portability bank, the builder, xvlog, the donor's `make tb` and act. The author did not re-run these either at round 2, on the grounds that no compiled RTL changed (round-2 commits touch tests, comments and docs only). I confirmed that the round-2 diff changes only comment lines in `KL_gptp_shadow.sv` and no other `hdl/` file or gitlink. `gptp_shadow` and `gptp_txts` ran here only as unmodified-head baselines and probe hosts, `gptp_txts` without its stale-chain check (no LiteX here). `gptp_plane` was not run this round.
- **Differentials are simulation, on two seeded stimuli.** They are not a formal equivalence proof, and they cover what those stimuli reach. On the path behind the pre-existing post-fence wedge (#714), they show only that both RTL versions behave the same under these two stimuli.
- **Hosted CI:** no hosted run was recorded at the exact head when I looked (01:06Z). That is not hosted acceptance; the manager owns it.
- **No manager source bank** runs at this head, and none is claimed. Physical calibration was NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Close F1 by re-review at the corrected head. A README or harness change un-covers Tests and Docs only.
- Rule on accepting the below-range L10a saving (107-253 against 300-700) and on the offered `tsf_r` option.
- Publish donor PR FPGA-gPTP#78 (`18dd997b`) before the parent. Run the merge round after #621 (PR #707, FPGA-gPTP#77) lands.
- Hosted acceptance at the exact head once runs exist; the manager owns hosted and act acceptance.
- Build and validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`) with the builder and native banks, and link its receipts.
- Carry R-01 to the residue checklist; route R593-1-S-03 to #495 at merge; per-segment coverage follows #714.

R593-2 FINISHED
