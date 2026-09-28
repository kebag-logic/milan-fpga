[R391] NEGATIVE - exact head e1ae468f7e237f321ce5fee19e59ae157da4b83d

# R391-1: independent external review of processor PR #132 (issue #131, D3 lane 1)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #132, issue #131, round R391-1.
- Exact head `e1ae468f7e237f321ce5fee19e59ae157da4b83d`, tree `817eb235c2f605ba4869bd77b4e3687701c151a7`; base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` (eight commits `66267d9` .. `e1ae468`).
- Contract: milan-fpga `docs/design/SAVED_STATE_MATERIALIZATION.md` at `7a7582f03ce5ba7863a90ac342c21be18d90db0b`, section 18.1 (Acceptance, Validation, Negative controls, Prerequisites), the section 15.2 table and its named sweep, with sections 3, 3.1, 5.1, 6.1-6.4, 7, 8.1-8.8 and 10 as the referenced rules. Rulings: DR1a-DR6 (milan-fpga #70 comment 5862405632), DR2c-carrier (5863247772) as corrected (5868716535), DR3a/DR4 ratification (5873060660).
- Reconstruction order followed: processor README, docs/README and hdl/README (the processor repository has no AGENTS.md or CONTRIBUTING.md; the parent's AGENTS.md section 6 reviewer procedure was applied); issue #131 body and the manager's assignment and STOP disposition; the parent contract and rulings; `git diff c951a9ff..e1ae468f` and per-commit history; then public evidence (milan-fpga `b657a2de` `review-evidence/pp131-r1`, the manager's bank comment 5873371256). No private material was read. Another reviewer's report and the manager's ruling on it were read only after this verdict, the findings and the ledger below were written (section "Other public review at this head").

## Verdict

NEGATIVE. Two MAJOR and two MINOR findings are open at this head, and all five lenses are unclean. Most of the lane is well built and well tested. Ownership from reset, the command-side triggers with change qualification, taint and same-edge precedence, both passes with record-by-record agreement, the SET-rule validation, the combined verdicts, the roll-back of both stores held on guard debt, and DR2c for both producers all behave as section 18.1 requires in every case I ran, and the author's mutation campaign reproduces. The findings are:

1. **F1 MAJOR.** The ratified 1,000 ms aggregate restore deadline is absent. This was expected: the ratification postdates the head. It is recorded here against the ratification, as instructed.
2. **F2 MAJOR.** New in this lane. While the D3 writer holds AECP dispatch, AECP frames occupy the shared RX slot pool. As few as `RX_SLOTS_P` = 4 held AECP frames stop ACMP listener service, permanently in CLOSED. That contradicts the separate release points the contract and this PR's own documentation state.
3. **F3 MINOR.** Four indefinitely-delayed and boundary behaviours of the writer have no killing test.
4. **F4 MINOR.** The parent port-contract ratchet regresses (111 to 114, reproduced), and the unit-naming gate is red (manager evidence).

## Findings

### F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - the ratified DR3a aggregate restore deadline is not implemented

- **Where.**
  - `hdl/aecp/KL_aecp_nvm_writer.sv:479-502`: the only restore deadline is `wd_r`, which counts consecutive cycles without progress and resets on every event. No counter starts at the accepted restore start.
  - `docs/architecture/08_timing.md:63-67` ("aggregate restore budget ... 1,000 ms ... **initial candidate** (DR3a); not enforced by a counter in this processor").
  - `docs/architecture/01_overview.md:176` ("the 1,000 ms aggregate ... is a budget, not a parameter").
  - `docs/architecture/03_packet_engine.md:243` ("the restore's own deadlines bound that hold").
  - `docs/architecture/08_timing.md:44,63` and `01_overview.md:176` still label the 20 ms per-wait deadline an "initial candidate", which the ratification has now ratified.
- **Authority.** DR3a/DR4 ratification (milan-fpga #70 comment 5873060660):
  - "1,000 ms from accepted `PP_CTRL[1]`, ratified as an enforced bound, not a measured budget ... Processor #131 therefore adds an aggregate deadline counter";
  - "on expiry it takes the D3 terminal path the walk would take on a per-wait timeout";
  - "Its constant is derived from the product clock, not mirrored";
  - "A negative control (a device answering just inside every per-wait deadline) must end at the aggregate bound."
  - Contract section 8.8: "These budgets never permit early enable".
- **Evidence (reviewer probe P5, `receipts/probe-P1-P5.log`).** Every D3 device READ was granted 19,800 cycles late, inside the bench's 20,000-cycle per-wait deadline. The walk ends COMPLETE 1,268,895 cycles after the admission release, which is 63.4 times the per-wait deadline. The ratified aggregate is 50 times the per-wait value (1,000 ms / 20 ms). Throughout, AECP stays held and ADP stays gated.
- **Impact.** A slow-but-answering persistence device keeps the entity dark and deaf to AECP for an unbounded multiple of the per-wait deadline. The ratification's own example is about 970 waits, roughly 19 s. The docs state an unenforced budget as the bound.
- **Required outcome.** The ratification is met:
  - An aggregate deadline starts at the accepted restore start and is derived from `CLK_HZ_P`.
  - Expiry takes the per-wait-timeout terminal path, with rollback as the state requires.
  - The named negative control ends at the aggregate bound, with a mutant that removes the counter killed.
  - 08/01/03, the integrator guide and the F01.5/F08.1 rows record both ratified values.
  - Any new parameter is declared as a parent-visible change.
- **Verification.** Re-run a P5-style stimulus: terminal at or before the aggregate bound, with the expected cause and terminal. Mutant killed by its named check. `make check` and `scripts/check-integrator-params.py` pass. Re-read the listed doc rows.

### F2 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - held AECP frames exhaust the shared RX slots and stop ACMP listener service (permanently in CLOSED)

- **Where.**
  - `hdl/aecp/KL_aecp_engine.sv:2425-2427` (`txn_ready_o ... && !d3_own_w`) and `:2585-2586`: A_IDLE takes no head while `d3_own_w`. It does not even drop a response or a non-target frame, because `drop_w` (`:1245`) is judged only in A_IDLE.
  - `hdl/top/protocol_processor_top.sv:86` (`RX_SLOTS_P = 4`, the product default).
  - `hdl/packet_engine/KL_pp_dispatch.sv` banner: a full queue stalls its producer and never drops; the RX slot is returned only when its engine retires the record.
- **Authority.**
  - Contract section 8.1, "Three release points, each its own": "ACMP listener work waits for S4's release only, and AECP for the D3 terminal only"; "A CLOSED terminal holds AECP and the enable until a reset, and does not take the listener's faces back".
  - The same promise at this head: `docs/architecture/05_acmp_engine.md:192-197` ("AECP dispatch and the ADP enable wait for the D3 terminal, the listener does not ... A CLOSED D3 terminal ... leaves the listener released"), `docs/architecture/07_memory_maps.md:592`, `hdl/top/protocol_processor_top.sv:441-444`, and `docs/diagrams/23-bringup-decision.svg`/`.png` step 3 ("AECP and ADP stay held until reset; ACMP still answers").
- **Evidence (reviewer probes P1/P2 on the real top, `receipts/probe-P1-hol.log` and `receipts/probe-P1-P5.log`).**
  - P1, CLOSED by an unprovable image. An ACMP GET_RX_STATE is answered in 168 cycles. After 0 or 3 held AECP READ_DESCRIPTOR commands it is still answered. After 4, 5, 6 or 8 it is never answered (two further attempts, 200 bench-ms each). AECP is never released in CLOSED, so this is permanent until reset.
  - P2, a healthy restore whose first D3 read is granted 18,000 cycles late, so the walk runs about 18,000 cycles after S4's release. With 8 AECP commands sent after the release, a GET_RX_STATE sent during the walk is never answered and is lost. Only 4 of the 8 held AECP commands are answered after the terminal. After the terminal, ACMP answers again in 168 cycles. With no AECP backlog the same GET_RX_STATE is answered in 168 cycles during the walk.
  - The threshold equals `RX_SLOTS_P`. Any AECP PDU the validator admits (own MAC, or the AVDECC multicast `91:E0:F0:01:00:00`) consumes a slot while held, including a response or a command for another entity id, which the engine would otherwise drop at once.
  - The bench suite never sends more than one AECP command while the writer owns (D3O1, D3O2, D3R9).
- **Impact.**
  - Four AECP frames arriving during the D3 walk, or at any time after a CLOSED terminal, stop the listener's live ACMP work: commands are lost, and bound sinks cannot be queried or rebound. Because the stall is on the shared RX path, other protocol traffic behind it is starved too.
  - In CLOSED this lasts until reset. A controller that still knows the entity (for example, one retrying after a device reboot) is enough.
  - The documented three independent releases do not hold under ordinary controller traffic, and the ACMP response budgets (08 `T-BUDGET-ACMP-RESP`) are not met.
- **Required outcome.** While the D3 writer owns AECP dispatch, from reset through the walk and for ever in CLOSED, held or undeliverable AECP traffic cannot deny RX, dispatch or timer resources to ACMP, ADP or the other protocols. The mechanism is the author's choice (for example, draining or refusing frames the engine would drop, bounding what the hold may retain, or reserving capacity).
  - The documents state what happens to AECP commands that arrive while held: how many are kept, and whether the rest are dropped and counted.
  - `03_packet_engine.md:236-244` ("commands that arrive then are answered after the restore") is corrected to match.
- **Verification.** A pp_top case with at least `RX_SLOTS_P + 1` AECP frames held, both during a stretched walk and after CLOSED, that grades an ACMP command answered within its budget. A mutant that restores the current behaviour is killed by that check. P1/P2 re-run (`scripts/run_probes.sh`) shows ACMP answered for every AECP count.
- **Manager ruling.** The ruling recorded after this finding was written (issue #131 comment 5873580386; see the last section) fixes the mechanism as a bounded share with counted drops, and names the two controls. Round 2 is verified against that ruling.

### F3 - MINOR - Conformance, Tests - four indefinitely-delayed and boundary behaviours of the writer are unguarded by any test

- **Where.** `tb/pp_top/d3_phases.hpp`:
  - D3R8 (`:1402-1421`) delays only the first pass-0 READ.
  - D3R5 (`:1080-1108`) silences only pass 0.
  - No case silences the format judge.
  - The bench image lists two sampling rates (`tb/pp_top/sim_main.cpp:487-490`), so the writer's rate-list walk never reads past its first list lane or meets its eight-entry bound.
- **Authority.** Section 18.1, Negative controls: "Exercise zero, boundary, corrupt, refused and indefinitely delayed inputs ... Each must fail a named ... assertion". Section 8.8 lists the judge among the watched waits and requires a pass-1 abandoned read to be drained. The writer re-implements the SET program's rate walk (`KL_aecp_nvm_writer.sv:454-477, 662-676`) independently of the microcode.
- **Evidence (`receipts/mutants-r391.log`, `receipts/mutants-r391-fullsuite.log`).** Each mutant below survives both the D3 section and the full pp_top suite (7,841 of 7,841 checks pass):
  - `pass1_read_not_drained` (`m_abort_o` only in pass 0);
  - `judge_wait_unwatched` (`W_JUDGE: stall_w = 0`);
  - `rate_walk_stuck_on_first_lane`;
  - `rate_walk_unbounded`.

  The first two are real defects when present (`receipts/probe-P3P4-*.log`). With the drain removed, the device's late answer never frees the port and a later SET is never written (golden: 1 WRITE, unflushed 0; mutant: 0 WRITEs, unflushed 1). With the judge unwatched, a silent judge never reaches a terminal and AECP stays held (golden: DEFAULTS, cause 3, 21,454 cycles; mutant: no terminal, own 1). The unmutated RTL behaves correctly in both probes (P3, P4).
- **Impact.** A regression in the pass-1 containment, the judge deadline or the rate walk would pass every gate.
- **Required outcome.** Named checks exercise:
  - a pass-1 NVM read held past the deadline, with the later SET persisting once the device answers;
  - a silent format judge;
  - a rate walk that must read past the first list lane and reach the eight-entry bound, on a bench image with more than two rates or an equivalent unit-level case.

  Each of the four mutants above is killed by its named check.
- **Verification.** Re-run `scripts/r391_mutants.py --only pass1_read_not_drained judge_wait_unwatched rate_walk_stuck_on_first_lane rate_walk_unbounded`: 4 of 4 KILLED; the unmutated suites pass.

### F4 - MINOR - Docs, RTL - the parent port-contract ratchet regresses, and the unit-naming gate fails on new boundary parameters

- **Where.**
  - `hdl/aecp/KL_aecp_nvm_writer.sv:198-200`: `sb_rvalid_i`, `sb_rdata_i` and `sb_err_i` carry no `//!` contract.
  - Naming (manager evidence): `KL_aecp_engine.NVM_RETRY_BACKOFF_CYC_P` (`hdl/aecp/KL_aecp_engine.sv:312-314`), `KL_aecp_nvm_writer.DEB_TICKS_P` (`:146-147`) and `protocol_processor_top.NVM_RS_TMO_CYC_P` (`hdl/top/protocol_processor_top.sv:125-133`).
- **Authority.** Issue #131's gates include the parent consumer gates. The parent `scripts/check_port_contracts.py` ratchets undocumented processor ports and allows the count only to fall. The parent `scripts/measure_naming.py --check` ratchets boundary names whose unit is not stated.
- **Evidence.**
  - `receipts/port-contract-count.log` uses the parent's own parser (`sv_ports.declarations`, milan-fpga `ce550952`) on the processor `hdl/`: 111 undocumented at base, 114 at head, and exactly those three ports are new.
  - The manager's bank comment (PR #132 comment 5873371256) reports the same 114-against-111 failure and the naming failure for the three parameters. The naming gate was not reproduced here, because it needs the full parent tree.
- **Impact.** Two parent consumer gates are red at this head for processor-side reasons, so the pin cannot be adopted as is.
- **Required outcome.** Both gates are at or under their ratchets at the next head, without weakening either gate.
- **Verification.** The manager's parent consumer gates, or `scripts/r391_port_doc_count.py` showing no count above 111.

### S1 - SUGGESTION - Docs - one conversion, two roundings

`docs/architecture/08_timing.md:63` gives the per-wait deadline as `ceil(P-CLK-HZ x 20 / 1000)` clocks. The top parameter and F01.5 compute `CLK_HZ_P / 50`, which is floor (`protocol_processor_top.sv:133`, `01_overview.md:176`). The two agree at 50 and 100 MHz and differ by one clock at clocks that are not multiples of 50 Hz. State the one the RTL implements.

## Judgement per section 18.1 sentence

| Sentence | Judgement | Evidence |
|---|---|---|
| Implement configuration, rates, both formats, clock source and PTOF | met | `KL_aecp_nvm_writer.sv` records 0x00, 0x02+, 0x0A+, 0x30+, 0x40+, 0x50+ with F07.8 framing. D3S1 (every group at its first and last index, byte-exact) and D3R1 (all nine rows restored with valid flags) pass in my run |
| Use the existing arbiter, S1/S3/S4 and S2 guard | met | manager 1 of `KL_pp_nvm_mgr_arb`. Port cause consumed (`rd_blank_w`/`rd_dev_w`). `go_i` = `lsn_released_w`. Guard debt routed (`protocol_processor_top.sv` `desc_mem_debt_w`) with its hard reset only |
| Command-side triggers and taint-safe whole-record retirement | met | `d3_chg_w = dyn_chg_w && !d3_bus_w` (µCPU side). `wr_chg_o` gives DR2b change qualification. Clear by group and index, taint after the latch, set outranks clear. D3S1-S8 pass; the author's TRG_*, taint, same-edge, group/index, IDENTIFY and validity mutants are killed (subset re-run: 13 of 13) |
| Hold AECP ownership from reset through the D3 terminal | met, with F2 | `own_o = !done_r || ...`. `txn_ready_o`/`rsp_open_w`/A_IDLE gated. D3O1/D3O2 pass. F2 is a side effect of the hold on shared RX resources |
| Both passes, semantic validation, combined restore outputs | met | whole0 agreement (cause 5); the SET rules for cfg, rate, clock source, formats (judge bit 0) and PTOF bit 31. Combined done/busy/fail/blank/closed/rb/causes at the top. D3R1-R6 pass; P3/P4 behave |
| Stage 1 rolls back dynamic and descriptor stores together | met | `store_rst_n_w` drives both stores. D3R4, R7, R10 and R11 pass |
| Debt survives local rollback; watchdog recovery precedes the re-LOCATE | met | the guard is on `rst_n` only. W_RB is held two cycles and while debt is owed, then W_RELOC. D3R10 (5,000 and 16,000 give DEFAULTS; 30,000 gives CLOSED) passes; the `rollback_ignores_debt` and `store_not_rolled_back` mutants are killed in my re-run |
| Apply the complete processor contract table in section 15.2 | met at this head, except the lines F1/F2 make stale | spot-checked rows: 01, 02, 03, 05, 06, 07, 08, the integrator guide, diagrams 20/21/23/24, `gen_ucode.py` (ROM byte-identical to base, `receipts/ucode-rom-identity.txt`), MODULE_MATRIX (`gen_matrix.py --check` rc 0), the integrator parameter check (25 = 25 = 25) |
| Complete its named contract sweep | met | the named search on the clean clone gives 624 matching lines; the author's SWEEP.md dispositions exactly those 624, none missing and none extra (`receipts/sweep-compare.txt`). The dispositions I sampled are sound, except the 03 rule (d) and 05/07 statements covered by F1/F2 |
| DR2c for both producers, including binding retry backoff | met | three attempts, `NVM_RETRY_BACKOFF_CYC_P = (CLK_HZ_P/2)+(CLK_HZ_P%2)` to both producers, backoff counted from the err in `clk_i` cycles, alarm only on own exhaustion, reset-sticky, OR-ed at the top. D3S10 and acmp_nvm E8-E11 pass; the no-backoff, fourth-attempt and alarm-forgiven mutants for both producers are killed in my re-run |
| Measure DR3a per-wait and aggregate; include both walks and rollback; record product clocks; submit | met as a measurement; the ratification now requires enforcement (F1) | printed DR3a mode; the ratification cites the measurements |
| Validation: tb/pp_top real AECP commands; all declared scalar indices; cleared-first; nvm_port, acmp_nvm and descriptor-guard suites; full gates | met, with gaps F2/F3 | my focused runs: pp_top 7,841/7,841, acmp_nvm 353, dyn_state 118, nvm_port 136, desc_mem_guard 78, desc_store 584, lsn_admit 18, adp_engine 533, all pass (`receipts/suite-*.log`); `make check` rc 0 |
| Negative controls, each failing a named assertion | met for every listed control except the indefinitely-delayed and boundary inputs of F3 | the author's campaign (47 of 47); my re-run of 13 of those kills every one; my 4 additional mutants survive (F3) |

## Parent-visible changes (pin-adoption lane)

- Declared and complete. The mechanical diff of the top's port and parameter lists, base against head, shows exactly five new ports: `d3_unflushed_o`, `restore_cause_o[1:0]`, `restore_closed_o`, `restore_rb_o` and `rs_cause_o[2:0]`. It shows exactly one new parameter, `NVM_RETRY_BACKOFF_CYC_P`. No existing port changed width or direction; only trailing comments changed.
- The behavioural changes are declared in the PR body:
  - combined `restore_done_o`/`busy`/`fail`/`blank`;
  - `nvm_alarm_o` from either producer;
  - ADP enable = `entity_enable_i && restore_done_o`, with the side-port lock keeping the requested level;
  - AECP held from reset to the D3 terminal;
  - manager-1 record traffic on the device face;
  - the firmware AEM-before-restore requirement.
- The side-port control word 1 now reports the combined verdicts. That falls under the declared "combined restore status".
- Nothing parent-visible is undeclared, with two caveats. The F2 behaviour, ACMP starvation while AECP is held, is parent-observable and not declared. The DR3a aggregate (F1) will add a declaration in round 2 if it adds a parameter.

## IEEE 1722.1 / Milan behaviour relied on

- **ADP gating.** Holding ADP advertising until both walks end is consistent with Milan 5.6.1 and IEEE 1722.1 ADP: the advertise state machine stays in DOWN, where ENTITY_DISCOVER is not answered. `restore_done_o` is sticky once reached, because the binding manager never returns to H_WAIT and `done_r` and the admission release are one-way. So the gated enable never falls after rising, and no spurious ENTITY_DEPARTING results.
- **Restored configuration index.** The first ADPDU after the terminal carries the restored configuration index.
- **AECP dispatch hold.** Holding AECP dispatch while the entity is not advertised is permitted.
- **CLOSED and AECP availability.** Answering commands only after the terminal is the contract's accepted fail-closed choice. F2 is the part that breaks ACMP, which the contract keeps separate.
- **AECP responses.** They are unchanged, and the response to a held command is byte-exact (D3O1, D3O4).

## Hosted evidence (read-only)

- At the exact head, check runs `docs-gates` and `portability` report completed/success. Two `suites` runs were still in progress when I read them. The combined status is `pending`, with 0 statuses.
- Not relied on. Hosted and act acceptance belong to the manager.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | contract §18.1 sentence by sentence (table above); §3/3.1/5.1/6.1-6.4/7/8.1-8.8/10 against `KL_aecp_nvm_writer.sv`, `KL_aecp_engine.sv` (D3 wiring, dispatch hold, gsi share), `protocol_processor_top.sv` (combined verdicts, ADP gate, arbiter wiring), `KL_acmp_nvm_shadow.sv` (DR2c); rulings DR2c-carrier (corrected) and DR3a/DR4; the IEEE 1722.1 ADP/AECP reliance | R391-1 | e1ae468f7e237f321ce5fee19e59ae157da4b83d |
| RTL | UNCLEAN (F1, F2, F4) | full read of `KL_aecp_nvm_writer.sv` (FSMs, deadline, abort priority, rollback, rate walk, framing/crc, service latch, backoff); engine state-bus 2:1 selection, snoop, `prog_busy`, gsi sharing; dyn_state `wr_chg_o`; desc store error sources (only LOCATE errs); port done/byte timing; top port and parameter diff | R391-1 | e1ae468f7e237f321ce5fee19e59ae157da4b83d |
| Robustness | UNCLEAN (F1, F2) | probes P1-P5 (CLOSED and walk AECP backlog, pass-1 silent read, silent judge, slow-but-inside device); D3R4-R12 fault cases re-run; the drain/quarantine path | R391-1 | e1ae468f7e237f321ce5fee19e59ae157da4b83d |
| Tests | UNCLEAN (F1, F2, F3) | `tb/pp_top/d3_phases.hpp` (D3O/D3S/D3R), `tb/acmp_nvm` E8-E11, `tb/dyn_state` H; 8 focused suites re-run; 13 author mutants re-run (13 killed, goldens pass); 4 reviewer mutants (4 survive the full suite) | R391-1 | e1ae468f7e237f321ce5fee19e59ae157da4b83d |
| Docs | UNCLEAN (F1, F2, F4) | 15.2 rows spot-checked in 01/02/03/05/06/07/08, integrator and operator guides, diagrams 20/21/23/24 (PNG 23 inspected), `gen_ucode.py`, suite READMEs; named sweep 624/624 reconciled; `make check`, `check-integrator-params.py`, `gen_matrix.py --check` rc 0; parent port-contract count reproduced | R391-1 | e1ae468f7e237f321ce5fee19e59ae157da4b83d |

## Real limits

- **Verilator.** The Verilator path named in the brief (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I used the sibling wrapper `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`, which is identical to the other managers' wrappers. It reports `Verilator 5.050 2026-07-01 rev v5.050`. The binary it executes has sha256 `fb2cc573b1055cf096c90e1efc9966fe56bdb4b265c83590cf2a49f7a0defcdf`.
- **What I did not run.** No full processor bank (`run_suites.sh` over all 33 suites), lint, Yosys, srp_top mutants, nvm_port figures, parent consumer gates, `xvlog_gate` or the evidence classifier. Only the eight focused suites and the gates named above were run.
- **Naming gate.** The parent naming gate was not reproduced (F4 rests on the manager's evidence for that part).
- **Figures not re-measured.** The DR4 area figures and the DR2a/DR3a numbers were not re-measured.
- **Mutation coverage.** I re-ran 13 of the author's 47 mutants.
- **Simulation only.** All probes are bench-model simulations with compressed time (the bench's 1 ms is 100 cycles, and its backoff and deadline are overridden). Physical calibration was NOT RUN, and nothing here is hardware proof.
- **Diagrams.** Diagrams were checked by source text and one PNG view, not re-rendered.
- **Reproducibility.** Probes and mutants ran on exported copies of the head under this packet's `scratch/`. The clone was never modified. At the end, HEAD, the index tree, the work-tree blob hashes and the file modes all equal the head, the status is empty, and the repository has no gitlinks (`receipts/clone-integrity.txt`).

## Pending manager duties

- Run the donor full bank and the parent consumer gates at this head (already reported in 5873371256) and at the round-2 head.
- Own hosted and act acceptance. The `suites` check runs were still in progress when read.
- Adjudicate F1-F4 into round 2 alongside the round-2 items already named (the port-contract and naming fixes, and the DR3a aggregate counter).
- Build the final current-dev candidate at the merge turn (source base `c951a9ff`, live dev `ce550952`).
- Record that physical calibration is NOT RUN.

## Receipts and reproduction

Every file below is listed in `MANIFEST.sha256`.

- `scripts/run_probes.sh <processor checkout> <scratch> <verilator dir>` exports the head and rebuilds and runs every probe and the reviewer mutants.
- `scripts/r391_probe.hpp` holds probes P1-P5.
- `scripts/r391_probe_mut.hpp` holds the P3/P4 golden-versus-mutant variant.
- `scripts/r391_mutants.py` holds the reviewer mutants and the cross-check mutants.
- `scripts/r391_port_doc_count.py` counts undocumented ports with the parent's own parser.

Receipts:

- `receipts/suite-*.log`: the eight focused suites.
- `receipts/probe-P1-hol.log`, `receipts/probe-P1-P5.log`, `receipts/probe-P3P4-golden.log`, `receipts/probe-P3P4-mutant.log`.
- `receipts/mutants-r391.log`, `receipts/mutants-r391-fullsuite.log`, `receipts/mutants-r391-crosscheck.log`.
- `receipts/author-mutants-rerun.md` and `.log`: the subset of the author's campaign re-run with the author's published driver.
- `receipts/sweep-rg.txt`, `receipts/sweep-compare.txt`.
- `receipts/ucode-rom-identity.txt`, `receipts/port-contract-count.log`, `receipts/check-integrator-params.log`, `receipts/gen-matrix-check.log`, `receipts/make-check.log`, `receipts/clone-integrity.txt`.

## Other public review at this head

This section was written after the verdict, findings and ledger above. It covers:

- the internal reviewer's R390-1 (PR #132 comment 5873569558, NEGATIVE at this same head), posted while this review was running;
- the manager's ruling on R390-1 F1 (issue #131 comment 5873580386).

No review findings predate this round. Each R390-1 item is resolved or retained at `e1ae468f` below.

| R390-1 item | Disposition at e1ae468f | Basis |
|---|---|---|
| F1 MAJOR, held AECP starves the shared ingress | **Retained (open).** It is the same defect as this review's F2, found independently. | My P1/P2 probes reproduce it: threshold `RX_SLOTS_P` = 4 in CLOSED, and an ACMP command lost behind 8 AECP commands during a stretched walk. The manager's ruling (one AECP record at most while held, further ones dropped and counted, a new parent-visible counter, non-AECP latency unchanged, two named controls) refines F2's required outcome, and F2 is verified against that ruling. |
| F2 MAJOR, DR3a aggregate deadline not implemented | **Retained (open).** It is the same as this review's F1. | My P5 probe: a slow-but-inside device ends at 63.4x the per-wait deadline, with no aggregate counter. |
| F3 MINOR, four rules ungraded (top backoff derivation; BACKOFF holding dispatch; blank-then-whole disagreement; one-cycle roll-back strobe) | **Retained (open)** and corroborated. It sits beside this review's F3, whose four mutants are different. | `receipts/mutants-r391-crosscheck.log`: my planting of items 2-4 survives the D3 section (86 of 86). Item 1 holds by inspection: `tb/pp_top/pp_top_wrap.sv:427` overrides `NVM_RETRY_BACKOFF_CYC_P` to 50,000, and `tb/acmp_nvm` sets its own, so the top's `ceil(CLK_HZ_P / 2)` is never exercised. |
| F4 MINOR, negative-control driver and mutation record outside the tree | **Retained (open).** | `docs/guides/hdl-engineer.md:200-203` says of a suite's mutation record: "If you add checks, add to it". `tb/acmp_nvm/README.md` keeps dated "Mutation-proven" sections per issue, while its line 57 and `tb/pp_top/README.md:77` send this lane's controls to "the lane's evidence packet". No D3 rows exist in-tree. |
| S1 and S2 (Docs, suggestions) | **Agreed** as suggestions. | The binding alarm latency change, the CLOSED side-port reading and the per-wait parameter's wider scope are worth naming explicitly for the pin-adoption lane. The long-hold exception to rule (e) follows from F1. |

The combined open set for round 2 is: F1 (= R390-1 F2), F2 (= R390-1 F1, per the manager's ruling), F3, F4, R390-1 F3 and R390-1 F4. My verdict and ledger are unchanged: NEGATIVE, all five lenses unclean.

R391-1 FINISHED
