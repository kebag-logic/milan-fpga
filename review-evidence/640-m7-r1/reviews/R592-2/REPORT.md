[R592] POSITIVE - exact head 2cc2ba0b8b08010df5ee12c1fc228851fa9a8444

# R592-2: internal review of PR #713 (issue #640, Mark II lane M7, plan L10a), round 2

Exact head `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444`, tree `bf74cb10132fb94dc1d75b798f0f1a87a80e2d19`.
The gPTP processor gitlink is `18dd997b2459699e41e5ce9bceca1181e41fa5fe`. That commit is published, and it is the head of donor PR FPGA-gPTP #78.
The diff examined is `e8454e2751d05b02ee8e5a571857589ab358ab86..2cc2ba0b`: 16 parent commits and 5 donor commits (`5dce647a..18dd997b`).

## Summary

- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs. All five are clean. No BLOCKER, MAJOR or MINOR is open.
- Open items: one SUGGESTION (S1, Tests) and one RESIDUE (RES1, PR body wording).
- Every prior finding is resolved at this head except R593-1-S-03. S-03 is a pre-existing SUGGESTION that the manager kept out of this round and sends to #495 at merge.
- The product RTL preserves behaviour as far as this round could test it. Three slice suites print byte-identical check output at the base and at this head. The new lockstep suite passes, and so do its 17 controls. Seven of this round's eight independent fault probes were caught by the expected named check. The eighth exposes a documented reach limit (S1).

## Reconstruction

Sources, in this order: AGENTS.md and CONTRIBUTING.md; the issue body (owner decision, NFR-RES-01 acceptance); the lane M7 assignment (issue comment 6097272538) and its round-2 assignment (6100980189); the executor's TAKEN (6097298086) and both REVIEW READY comments (6100339945, 6103827621); the published round-1 evidence at `3e0f36b8:review-evidence/640-m7-r1` (`HANDOFF.md`, `PR-BODY.md`); the PR body; the gate record `syn/ooc/pp_resource_baseline.json`; then the diff and history.

The lane scope is frozen in the assignment:
- Move eligible fabric gPTP plane tables into block RAM, or narrow their indices.
- Keep dual-read operand files.
- Target about 500 LUTs (300-700).
- BRAM may grow only within the firmware ledger.
- A read-latency change needs deterministic bounds.
- No change to gPTP behaviour, the register map or the timestamp path.

Proof, also from the assignment:
- the gPTP suites in both shapes, plus the timestamp and CDC checks;
- per-table lockstep with planted wrong-depth, wrong-read-latency and index-aliasing defects, each failing a named check;
- the integrated route and the resource gate through the M0s recipe;
- an honest statement of the measured saving against the estimate.

Issue-level acceptance (at most 38,040 LUTs, gate re-recorded) belongs to the milestone, not to this lane. D7 holds the record until M9.

## Independent executions at this head

All runs used the pinned Verilator 5.050 (`verilator --version`: `Verilator 5.050 2026-07-01 rev v5.050`), each with its own log and rc file. The base runs used an extraction of `e8454e27` with its own submodule pins (gptp-processor `5dce647a`).

| Execution | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/gptp_tables` (suite + `mutants.py`) | rc 0; 24/24 checks over 32,100,038 cycles; `results: 11377 compared, heads 0xff, 3 deep, 110 written behind a waiting result`; `tx_fifo decode: counts 0x1ff driven, 0 decoded wrong`; `ledger: ... tags 0x2, 3 deep`; `timer: ... slots 0x3f`; 17/17 controls caught, each by its own named check | `receipts/logs/head_gptp_tables.log`, `.rc` |
| `gptp_shadow` (lifecycle + run + mutants), head | rc 0; 309/309; lifecycle PASS; 9/9 controls | `receipts/logs/head_gptp_shadow.log` |
| `gptp_txts` (run + mutants), head | rc 0; 85/85; 6/6 controls | `receipts/logs/head_gptp_txts.log` |
| `gptp_plane`, head | rc 0; 29/29 | `receipts/logs/head_gptp_plane.log` |
| Timestamp and CDC suites, head: `ptp_ts` (run, mux SVA, SVA campaign), `ptp_sync`, `ptp`, `clkvalid`, `cdc` | each rc 0, every tally 0 failures | `receipts/logs/head_{ptp_ts,ptp_sync,ptp,clkvalid,cdc}.log` |
| Base `e8454e27`: `gptp_shadow`, `gptp_txts`, `gptp_plane` `run` | rc 0; 309, 85 and 29 checks. Check output at the head is byte-identical to the base (shadow: all 38 result lines; txts and plane: whole result block) | `receipts/logs/base_*.log` |
| Eight reviewer fault probes (`scripts/probe.py`, private copies) | 7 caught by the expected check: TX count off by one, RX lowest lane instead of highest, RX bad-frame bit moved to the lane field, TX decode `<=`, ledger tag stuck at 0, result sequence copied from the ledger tail, timer write-slot alias. 1 GREEN: ledger RAM written on every `alloc_i`, even when full (S1) | `receipts/probes_summary.json`, `receipts/logs/probe_*.log` |
| Per-reset-segment probe (`scripts/segment_probe.py`, harness-only print) | After reset 1 and after reset 2 the plane runs programs again (10,234 and 3,673), the result and timer comparisons keep growing, frames leave, and flags return to `0xd` | `receipts/logs/segment_probe.log` |
| 32 documentation, source and lint gates (`scripts/gates.sh`) | every one rc 0, including `docs_check` (with and without git), `check_em_dash --base e8454e27`, `gen_module_matrix --check`, `check_gptp_docs` (+`--with-submodule`, `--selftest`), both diagram `--check`s, `check_diagram_pngs`, `measure_test_evidence --check`, `lint_rtl --check` (90 <= ratchet 90), `pp_resource_gate check-baseline`, `make -C gptp-processor contract lint`, `git diff --check e8454e27 HEAD` | `receipts/logs/gates.tsv`, `receipts/logs/gate_*.log` |
| Restoration check | rc 0: HEAD and tree exact; index equals HEAD; 1,277 tracked blobs re-hashed equal; no untracked file; gptp-processor, protocol-processor and verilog-axis at their gitlinks and clean | `receipts/logs/verify_clean.log`, `.rc` |
| Public state | PR not draft; 0 check runs and 0 workflow runs at the head; donor commit published, donor PR #78 open at it; #714 and #495 open | `receipts/public_state.txt` |

## Findings

### R592-2-S1: SUGGESTION (Tests). The ledger's full-table write guard is never exercised

- **Location:**
  - `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:637`, the RAM write enable `led_we_w = alloc_i && (n_led_r != TXTS_CAP_N_P)`;
  - `tb/verilator/gptp_tables/README.md:30`, which states that the ledger reaches 3 of 8 entries.
- **Evidence:**
  - Probe `ledger_ram_write_when_full` drops the guard from the RAM write (`KL_gptp_txret.sv:640`) and leaves all 24 checks green (`receipts/logs/probe_ledger_ram_write_when_full.log`).
  - The RTL is right. `led_we_w` drives both the RAM write and the `led_live_r` set, so the two cannot drift, and it copies the base guard exactly.
  - The README already states the reach limit honestly.
- **Impact:** a later change to the guard would be caught only by review, not by this suite.
- **Suggested outcome (optional):** a directed full-ledger case, or a control that fails a named check once the ledger is held full.

### R592-2-RES1: RESIDUE (Docs). The PR body calls the PR a draft

- **Location:** the PR #713 body, Status section: "Green, review ready at `2cc2ba0b` (round 2). Draft until both reviews are positive."
- **Evidence:** the PR is not a draft (`isDraft: false`, `receipts/public_state.txt`).
- **Impact:** wording only. It changes no measurement, figure, verdict, test, code, generated artifact or clause claim.
- **Exact fix:** replace "Draft until both reviews are positive." with "Marked ready for review; merge waits for both reviews to be positive." Alternatively, convert the PR to draft, which is the manager's call.

## Prior public review findings at this head (read after this round's own pass)

This round's own verdict and ledger were written to `receipts/own_pass_before_prior_findings.md` before the R592-1 and R593-1 report bodies were opened.

| Prior item | Status at this head | Basis |
|---|---|---|
| R592-1-F1 MINOR (Tests): the result queue never held two results; a write-index defect was undetected | **Resolved** | Results reach 3 deep under lockstep (`head_gptp_tables.log`). Named coverage `results coverage: two or more results outstanding` (`sim_main.cpp:535`). Control `results_write_index` is caught by `results lockstep`. The "filled" claim is narrowed per table (`sim_main.cpp:10-23`, `README.md:26-32`), and each stated reach matches the printed output |
| R592-1-F2 RESIDUE = R593-1-R-02: three FIFO-output comments | **Resolved** | `KL_gptp_shadow.sv:238-242`, `:258-261` and `:878-880` carry the exact replacement texts. Round 2 changed no compiled RTL: `9d42762c..2cc2ba0b` touches only comments in `hdl/` |
| R592-1-F3 RESIDUE = R593-1-R-01: the plan's eligibility sentence | **Resolved** | `MARK_II_AREA_PLAN.md:690-691` is the exact replacement, including the `tsf_r` option |
| R592-1-F4 SUGGESTION: TX lane counts 1, 3, 5, 6, 7 never decoded | **Resolved** | `decode_check()` (`sim_main.cpp:450`), check `tx_fifo decode` (`:513`), control `tx_fifo_decode_odd_counts` caught. This round's `tx_decode_le` probe is also caught by `tx_fifo decode` |
| R592-1-F5 RESIDUE: "40/40 engine mutants" | **Resolved** going forward | The round-2 REVIEW READY (6103827621) carries "40/40 donor mutants (engine 33, gaskets 4, tsngen 3)". The round-1 comment and the published round-1 hand-off stay unchanged as history |
| R593-1-S-01 SUGGESTION: the ledger tag column is one-valued | **Resolved** | `README.md:56-60` states it, and the run prints `tags 0x2`. This round's `ledger_tag_stuck0` probe is caught by `ledger lockstep` |
| R593-1-S-02 SUGGESTION: no per-reset-segment coverage | **Resolved as documented** | `README.md:61-67` names #714 and defers per-segment coverage to its fix. Its claim that the plane stays live after both warm resets at this seed is verified by `segment_probe.log` |
| R593-1-S-03 SUGGESTION: the lane guard admits widths the classifier and gearbox cannot serve | **Retained**, pre-existing | Out of this round by the round-2 assignment; goes to #495 at merge. The guard at `KL_gptp_shadow.sv:271` is correct for the lane fields it protects. The base had no guard |

## Lens results

- **[R592] PASS Conformance** - examined: lane assignment 6097272538 and round-2 assignment 6100980189 against the diff.
  - Five tables change storage only. RX now carries the highest lane, which is what the serializer reads (`KL_gptp_shadow.sv:321-327, 599`). TX carries the lane count, rebuilt to contiguous `tkeep` (`:821, 882-885`). The ledger and results move to RAM fields with combinational reads (`KL_gptp_txret.sv:339-357, 639-645, 699-707`). The timer deadlines move to RAM (`KL_gptp_timer.sv:80-94`).
  - Dual-read files are untouched. No read latency changes: the FIFO `RAM_PIPELINE` default is kept, and every RAM read stays asynchronous. No register map or timestamp path changes.
  - Block RAM goes 74/27 to 74/25, inside the ledger.
  - Function is unchanged where measured: the base and head slice outputs are identical.
  - Route figures re-checked against `pp_resource_baseline.json`. The record equals the base; route #2 WNS +0.122 is above the 0.03 floor and its fall 0.177 is within 0.25; RAMB tolerance 0 means no growth; the record is not re-recorded (D7). The route itself is the author's published measurement.
  - The saving is below the plan's range (107-253 against 300-700). It is reported plainly in the PR, the plan and the area budget, as the assignment's "report honestly" requires.
- **[R592] PASS RTL** - examined: the three RTL diffs at this head, against the pinned `axis_fifo.v`.
  - `:137` ADDR_WIDTH with KEEP_ENABLE=0 equals the old byte-depth form; depths 256 beats are unchanged.
  - `:236` gives the `tkeep` default. `status_depth` (`:254`) changes scale, but both instances leave it unconnected (`KL_gptp_shadow.sv:471-472, 872-873`).
  - The bad-frame mask and value stay on tuser bit 0.
  - Every converted array has one write port gated as before (`rst_n` and the old enable) and one asynchronous read: ledger head, result head, sweep slot.
  - FIFO data widths are 69 bits, so each fits one 72-bit RAMB36.
  - No CDC is touched. Lint ratchet 90/90; `gp_lint` and `gp_contract` rc 0.
- **[R592] PASS Robustness** - examined: removing the reset clears, against every reader.
  - The ledger head is used only behind `have_entry_w` (`KL_gptp_txret.sv:552, 581`; `tag_ok_w` at `:539` is masked by it).
  - Results are sampled only on an accepted beat (`KL_gptp_engine.sv:349-350, 484-489`; `txts_valid_o` at `KL_gptp_txret.sv:735`).
  - A deadline is read only for an armed slot, and arming writes it in the same cycle.
  - `gptp_tables` drives malformed, runt, oversize and foreign frames, corrupted `tkeep`, overflow bursts, long stalls, held records and two warm resets mid-traffic. The plane is live in every segment (`segment_probe.log`).
  - The pre-existing fence pop (`KL_gptp_shadow.sv:864`) is #714 and is unchanged from the base.
- **[R592] PASS Tests** - examined: `tb/verilator/gptp_tables/{gptp_tables_wrap.sv,sim_main.cpp,mutants.py,Makefile,README.md,waivers.vlt}`.
  - Every oracle is the previous storage form, written from untouched signals (`gptp_tables_wrap.sv:208-250, 275-332, 370-396, 422-431`). The compare gates are the consumers' sampling conditions (`:262, 340, 403, 412, 442`).
  - The test-only forces (`:181-197`) only withhold transfers and drive the decode while the plane is held in reset.
  - The 17 controls are caught, each by its own name. Seven of 8 independent probes are caught by the expected check; S1 is optional.
  - The suite is in the default sweep (`run_all_suites.sh --list`: 62 entries including `gptp_tables`).
- **[R592] PASS Docs** - examined: `MARK_II_AREA_PLAN.md:560, 672-717, 852`; `AREA_BUDGET.md:197-200, 267-268`; `TESTING.md:150, 409-410, 601`; suite README; regenerated `MODULE_MATRIX.md` and README-tests; donor `docs/MANAGER.md`; the pin-link pages; `rom_digests.tsv`. Every figure was re-derived:
  - routed delta -369 = -229 - 414 + 274; FF -1,193; WNS -0.177; WHS -0.012;
  - FIFO widths 74/73 to 69 bits;
  - RAM32M/RAM32X1D counts consistent with 21, 89 and 32 bits;
  - donor -105 LUT, -256 FF, LUTRAM +24 = 5x4 + 2x2;
  - firmware tiles 87.5 to 86.5.

  The README's reach table matches the printed run. All 32 gates are rc 0. RES1 (PR body) is wording only.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 6097272538 and 6100980189; the diff; `pp_resource_baseline.json` `route-1x1`; `base_*.log` against `head_*.log`; route figures in `MARK_II_AREA_PLAN.md:694-700` and published `HANDOFF.md` §6 | R592-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |
| RTL | CLEAN | `KL_gptp_shadow.sv`, `KL_gptp_txret.sv`, donor `KL_gptp_timer.sv`; `axis_fifo.v:137,236,254`; `KL_gptp_engine.sv:349-350,484-489`; `gate_lint.log`, `gate_gp_lint.log`, `gate_gp_contract.log` | R592-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |
| Robustness | CLEAN | reader guards cited above; `head_gptp_tables.log`; `segment_probe.log`; `head_gptp_shadow.log`; #714 (pre-existing) | R592-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |
| Tests | CLEAN (S1 SUGGESTION) | `tb/verilator/gptp_tables/*`; `head_gptp_tables.log` (24/24, 17/17); `probes_summary.json`, `probe_*.log`; `head_gptp_shadow.log`, `head_gptp_txts.log` | R592-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |
| Docs | CLEAN (RES1 RESIDUE carried) | `MARK_II_AREA_PLAN.md`, `AREA_BUDGET.md`, `TESTING.md`, suite README, generated matrix and README-tests, donor `docs/MANAGER.md`, pin links, PR body; `gates.tsv`, `gate_*.log` | R592-2 | `2cc2ba0b8b08010df5ee12c1fc228851fa9a8444` |

## Real limits of this round

- **Not run here:**
  - `milan_dp` (N=4/N=8) and `milan_dp_gptp`, so "both shapes" rests on the author's round-1 receipts at heads whose compiled RTL equals this head;
  - `tsn_fuzz`, Yosys portability, the xvlog gate, the builder, and the donor's `make tb`;
  - any synthesis, route or out-of-context mapping.

  The route, the per-table primitive census and the post-synthesis and out-of-context deltas are the author's published measurements. They were re-checked here for arithmetic and against the gate record, not re-measured.
- No manager source bank ran at this exact head, and none is claimed. Exact-head hosted evidence does not exist: 0 check runs and 0 workflow runs (`public_state.txt`). Nothing hosted is inferred.
- The idiom gates ran on the host interpreter, not on CPython 3.12.3 as hosted.
- The lockstep reaches the ledger and results only 3 of 8 deep, TX FIFO 27 of 256 beats, and timer slots 0-5. That is documented in the README; S1 shows one consequence.
- The base-against-head differential covers the slice suites only. The author's 29.1 M-cycle full-plane differential is unpublished scratch and was not relied on.
- A first launch of the suite campaign failed in this round's own runner: an exported variable re-entered the simulator wrapper. It was discarded unpublished and re-run; every result above comes from the re-run.
- Physical calibration was NOT RUN. No field or hardware evidence was involved, and no skip is treated as proof.

## Pending manager duties

- Validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks, and link its receipts. Own hosted and act acceptance at the exact head; none exists yet.
- Rule on the below-range saving (107-253 against 300-700) and on the untaken `tsf_r` option. Both are reported, not hidden.
- Publish donor branch `640-m7` / FPGA-gPTP #78 (`18dd997b`, already public) before the parent merges. Apply the #621 merge round if #621 lands first.
- Carry RES1 to the residue checklist, and R593-1-S-03 to #495 at merge. #714 stays open as filed.

R592-2 FINISHED
