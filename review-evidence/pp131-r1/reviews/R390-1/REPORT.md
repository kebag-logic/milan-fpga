[R390] NEGATIVE - exact head e1ae468f7e237f321ce5fee19e59ae157da4b83d

# R390-1: independent internal review of processor PR #132 (issue #131, D3 lane 1)

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| Head reviewed | `e1ae468f7e237f321ce5fee19e59ae157da4b83d`, tree `817eb235c2f605ba4869bd77b4e3687701c151a7` (verified in the review clone) |
| Base | `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`; eight commits `66267d9`..`e1ae468` |
| Contract | parent `docs/design/SAVED_STATE_MATERIALIZATION.md` at `7a7582f0` §18.1, the §15.2 table and its sweep (sha256 `e26784e1…f077`) |
| Rulings | DR1a-DR6 (issue 70 comment 5862405632); DR2c-carrier (5863247772) as corrected by 5868716535; DR3a/DR4 ratification (5873060660) |
| Verdict | **NEGATIVE**: two MAJOR and two MINOR findings are open; all five lenses are UNCLEAN |

## 1. How the review was reconstructed

1. The repository has no AGENTS.md or CONTRIBUTING.md. The conventions come from `README.md`, `docs/README.md` (single-source rules, editing workflow), `hdl/README.md` (rules 1-5, the consumption contract), `docs/architecture/09_verification.md` §7 and the HDL engineer guide §6 (the mutation record convention).
2. Issue #131: the body, the assignment and scope notes (5868003073), the author's contract STOP (5868697891) and its disposition (5868716919), and the review-ready note (5873035418). PR #132: the body, which declares the parent-visible changes, and the review-start comment. The PR had no reviews and no other comments at this head.
3. The contract's §§3, 3.1, 5.1, 6.1-6.4, 7, 8.1-8.8, 10, 15, 15.1, 15.2 (37 rows and the sweep) and 18.1, plus the four rulings above.
4. `git diff c951a9ff..e1ae468`: 48 files, +4,372/−513. I read every RTL hunk, and the new `KL_aecp_nvm_writer.sv` line by line. I read the D3 section of `tb/pp_top` (`d3_phases.hpp`) in full and the documentation diffs selectively.
5. Public executable evidence at milan-fpga `b657a2de`, `review-evidence/pp131-r1`: MANIFEST.json, MUTANTS.md, d3_mutants.py, SUITES.md, SWEEP.md, TABLE-15.2.md, EVIDENCE.json, FINAL-STATE.json, processor logs. I also took a snapshot of the hosted checks at this head.
6. My own execution at the exact head, in disposable `git archive` copies under the packet's `scratch/`, using Verilator 5.050 (see §8 for the path deviation):
   - `tb/pp_top`, full (both builds): 7,841 checks, 0 failures.
   - `--d3-only`: 86 checks, 0 failures.
   - Focused suites: `acmp_nvm` 353, `nvm_port` 136, `desc_mem_guard` 78, `dyn_state` 118, `desc_store` 584, `lsn_admit` 18, `adp_engine` 533, all PASS.
   - Documentation gates `links`, `matrix`, `modmatrix` and `params`: rc 0.
   - `--dr3a` reproduces the published figures (healthy restore ≤ 2,661 cycles, longest healthy D3 wait 853).
   - Four reviewer probes and four reviewer mutants (§3).

No prior public review findings exist on PR #132 at this head. Only the manager's review-start comment is present, so nothing had to be resolved or retained.

## 2. Findings

### R390-1-F1: MAJOR. Held AECP records starve the shared ingress; ACMP listener work is lost during the D3 hold and permanently in CLOSED

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - The hold is implemented at the AECP engine's pop face: `hdl/aecp/KL_aecp_engine.sv:2425-2426` (`txn_ready_o … && !d3_own_w`), `:2463`, `:2586` and `:2664`. It is driven by `hdl/aecp/KL_aecp_nvm_writer.sv:983` (`own_o = !done_r || …`, which stays 1 forever in CLOSED).
  - Held records keep their dispatch-queue entry and their payload slot. The RX slot pool is shared by every protocol (`hdl/top/protocol_processor_top.sv:86`, `RX_SLOTS_P = 4`; pools at `:1275-1300`, "never fatal, drop + count" at the F03.2 slot gate). The ingress is one normalized stream (`hdl/packet_engine/KL_pp_normalizer.sv:175`, a single output register) into queues whose full policy is "producers STALL, never drop" (`hdl/packet_engine/KL_pp_dispatch.sv:26`).
  - Documentation that states the opposite:
    - `docs/guides/integrator.md:307`: "The ACMP listener is unaffected".
    - `docs/architecture/07_memory_maps.md:654`: "the listener stays released".
    - `docs/architecture/03_packet_engine.md:241-243`, rule (d): commands "are answered after the restore … the restore's own deadlines bound that hold". This is false in CLOSED, and it conflicts with the same section's rule (e): IEEE 1722.1-2021 §9.3.2.6, 240 ms, "never a silent drop".
- **Authority:**
  - D3 §8.1: "ACMP listener work waits for S4's release only, and AECP for the D3 terminal only, whatever the enable says"; "A CLOSED terminal holds AECP and the enable until a reset, and does not take the listener's faces back".
  - D3 §8.8, the dependency table's "Live service" row.
  - D3 §15 item 15: "Test real dispatch …; prototype handshakes are insufficient". The prototype modelled the listener's producers "by their handshakes" (§8.8, model omissions).
  - §18.1 Acceptance ("Hold AECP ownership from reset through the D3 terminal") and Negative controls ("indefinitely delayed inputs").
- **Evidence** (executed; `scripts/probe_hol.hpp`, `scripts/probe_hol_restore.hpp`; receipts `probe-hol.txt`, `probe-hol-restore.txt`):
  - **CLOSED** (the D3O2 image with its magic corrupted): with no AECP traffic, GET_RX_STATE is answered. After the 4th AECP command addressed to the entity (4 = `RX_SLOTS_P`), no GET_RX_STATE is answered again, including one sent and waited on for 2,000 ms. The same flood after COMPLETE drains, and the listener answers again.
  - **During a restore** slowed inside the per-wait deadline (grant held 15,000 of 20,000 cycles), with a GET_RX_STATE sent after the S4 release:
    - 0 or 2 queued AECP commands: answered 167 cycles after it was fed, about 16,000 cycles before the D3 terminal.
    - 6 queued AECP commands: never answered, not even after the D3 terminal. The frame is lost, not delayed.
  - The same slot pool and normalizer carry ADP, MAAP and timer records. I infer from the source that talker ENTITY_AVAILABLE ingress and MAAP defence are equally exposed; I did not execute that separately.
  - D3O2 (`tb/pp_top/d3_phases.hpp:122-144`) queues one command in CLOSED and checks only that it stays queued. No suite grades non-AECP service under a held AECP queue.
- **Impact:** A device whose image cannot be proven ends CLOSED, as the contract intends. But a controller that knew the entity before a reboot then permanently deafens it to ACMP (bind, probe, GET_RX_STATE), and by inference to every other ingress, until reset. The contract promises the listener stays live there. During an ordinary restore, ACMP frames arriving behind a handful of AECP commands are silently dropped. That breaks the "three release points, each its own" rule and rule (e).
- **Required outcome:**
  - Held AECP work must not consume the shared ingress resources that ACMP, ADP and MAAP need, both during the hold from reset and in CLOSED. Options include bounding or isolating AECP's share of RX slots and queue, or refusing or dropping AECP records with a counter while the writer holds from reset. If this cannot be done without a new drop or refusal rule beyond the fixed contract, STOP to the manager with this evidence for a ruling.
  - Correct the three documentation statements.
  - Add a named negative control: CLOSED plus at least `RX_SLOTS_P + 2` AECP commands, after which GET_RX_STATE is still answered; and the same before the D3 terminal of a slowed restore. A mutant restoring the current gating must fail it.
- **Verification:** Rerun both reviewer probes at the fix head: every GET_RX_STATE is answered in both scenarios, and the new control is killed by the gating mutant.

### R390-1-F2: MAJOR. The ratified, enforced 1,000 ms aggregate restore deadline is not implemented (expected in round 2)

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/aecp/KL_aecp_nvm_writer.sv:479-502`: only the per-wait counter (`expire_w`, `:496`).
  - `hdl/top/protocol_processor_top.sv:125-139`: no aggregate parameter.
  - `docs/architecture/08_timing.md:64` ("not enforced by a counter in this processor") and `:61-68`, which still label both DR3a numbers "initial candidate".
  - `docs/architecture/01_overview.md:176` ("a budget, not a parameter").
- **Authority:** The DR3a/DR4 ratification (issue 70 comment 5873060660) came after this head. It rules:
  - The per-wait deadline is ratified at 20 ms.
  - The aggregate is 1,000 ms from accepted `PP_CTRL[1]`, "ratified as an enforced bound, not a measured budget". An aggregate counter starts there, and on expiry takes the terminal path of a per-wait timeout (roll back to DEFAULTS, or CLOSED as the state requires).
  - Its constant is derived from the product clock, not mirrored.
  - A negative control (a device answering just inside every per-wait deadline) must end at the aggregate bound.
- **Evidence:** Source inspection: no counter spans the walks. The PR body itself states that a device answering each wait just inside 20 ms stretches the D3 walk over about 970 waits (about 19 s). The `--dr3a` receipt reproduces the per-wait measurements.
- **Impact:** A slow but live device keeps AECP held and ADP unadvertised for about 19 s or more, and (with F1) exposes ingress for that whole time.
- **Required outcome:**
  - Implement the counter from the accepted restore start through both walks and the roll-back, with a constant derived from `CLK_HZ_P`. Expiry follows the per-wait terminal path.
  - Update F08.1, F01.5 and 08 §2 to the ratified values.
  - Add the ruled negative control and a boundary case, each killed by a mutant that removes the counter.
- **Verification:** A bench case with every wait answered just inside the per-wait deadline ends at the aggregate bound with the ruled terminal. The removal mutant fails it.

### R390-1-F3: MINOR. Four contract rules are not graded by any suite; reviewer mutants survive

- **Lens:** Tests.
- Each mutant was planted in a disposable copy (`scripts/r390_mutants.py`, `scripts/mut_backoff_derivation.sh`; receipts `r390-mutants.txt`, `mut-backoff-derivation.txt`, `probe-gaps.txt`):
  1. **Product backoff derivation.** Changing `hdl/top/protocol_processor_top.sv:139` from `ceil(CLK_HZ_P / 2)` to `CLK_HZ_P / 200` (5 ms) SURVIVES `tb/pp_top` (7,841/7,841) and `tb/timer_map` (1,360/1,360). The bench overrides the parameter (`tb/pp_top/pp_top_wrap.sv:427`, 50,000) and `tb/acmp_nvm` sets its own (`tb/acmp_nvm/Makefile:16`). Authority: D3 §5.1 ("Lane 1 derives both producers' backoff from the top's `CLK_HZ_P`"; "It uses neither debounce ticks nor firmware time") and the 18.1 negative control "Remove backoff". The head's formula is correct by inspection. Only its grading is missing, and the wrap's 50,000 cycles also equal 500 bench ticks, so a tick-counting backoff would pass as well.
  2. **BACKOFF must hold neither the bus nor dispatch** (D3 §6.1). A mutant adding `S_BACKOFF` to `own_o` (`KL_aecp_nvm_writer.sv:983`) SURVIVES the D3 section (86/86). Probe: a READ_DESCRIPTOR sent 1,000 cycles into a backoff is answered after 2,299 cycles at the head, but after 51,237 cycles under the mutant.
  3. **Pass agreement, blank-then-whole direction** (D3 §6.3 `disagree`; §8.6 V18c). A mutant that aborts only on whole-then-blank (`:507-508`) SURVIVES (86/86). Probe: with a record unframed in pass 0 and framed at rest before pass 1, the head aborts (cause 5, rolled back); the mutant applies it (COMPLETE, ptof0 = 1,500,000 with valid 1). D3R4 grades only the other direction.
  4. **Roll-back strobe of at least two cycles** (D3 §6.2/§6.3). A one-cycle mutant (`:699-702`) SURVIVES (86/86).
- **Impact:** Regressions of ruled behaviour would pass every gate.
- **Required outcome:** Add named checks so that each of the four mutants is killed.
- **Verification:** Rerun both reviewer scripts at the fix head. Each mutant is KILLED by its named check, and the head passes.

### R390-1-F4: MINOR. The §18.1 negative-control evidence cannot be reproduced from the repository

- **Lenses:** Tests, Docs.
- **Where:** `tb/pp_top/README.md:71-77` and `:131-139`, and `tb/acmp_nvm/README.md:57` ("they run from the lane's evidence packet"); `docs/architecture/09_verification.md:179` ("mutation record in the lane's evidence packet"). The suite's own `## Mutation record` section (`tb/pp_top/README.md:488`) gains no D3 rows.
- **Authority:**
  - `docs/architecture/09_verification.md` §7 (lines 136-139) and the HDL engineer guide §6 (lines 200-203): each suite README carries a mutation record, "a table of deliberate breakages and how many checks each turned red … If you add checks, add to it."
  - In-tree precedent: `tb/pp_top/gsi_mutants.py`, `tb/pp_top/name_wr_mutant.py`, `tb/acmp_talker/retry_mutants.py`.
  - §18.1: "Each must fail a named … assertion".
- **Evidence:** The 47 mutants and their driver (`d3_mutants.py`) exist only in the external packet. The pin that the parent adopts has neither the driver nor a per-mutant table.
- **Impact:** The negative controls cannot be rerun from the pinned tree, and a later edit can silently remove their teeth.
- **Required outcome:** Commit the driver or an equivalent in-tree runner, add the mutation-record rows (mutant, failing checks) to the suite READMEs, or obtain a manager ruling that the external packet suffices.
- **Verification:** The driver runs from the tree at the fix head, and every listed mutant is KILLED.

### Suggestions (they do not affect the verdict)

- **R390-1-S1** (Docs): Name three more parent-visible changes explicitly in the pin-adoption list:
  - The binding manager's alarm latency changed. Immediate retries became at least `2 × NVM_RETRY_BACKOFF_CYC_P` of backoff before `nvm_alarm_o`.
  - The side-port control word reads busy 0, done 0, fail 1 in CLOSED (`protocol_processor_top.sv` `sp_ctrl` address 1).
  - `NVM_RS_TMO_CYC_P` now also bounds every D3 wait, including the descriptor re-walk.
- **R390-1-S2** (Docs, Conformance): With the ratified 1,000 ms aggregate, a command held through a long restore can exceed the 240 ms response rule that 03 §6 rule (e) quotes. State that exception where rule (e) is written, rather than leaving rule (d) implying a short hold.

## 3. §18.1 judged sentence by sentence

| §18.1 sentence | Judgement | Evidence |
|---|---|---|
| Implement configuration, rates, both formats, clock source and PTOF | met | writer records `0x00`, `0x02+`, `0x0A+`, `0x30+`, `0x40+`, `0x50+` (`KL_aecp_nvm_writer.sv:71-83`, `:323-341`); D3S1/D3R1 byte-exact and GET readback |
| Use the existing arbiter, S1/S3/S4 and S2 guard | met | manager 1 of `KL_pp_nvm_mgr_arb`; port cause consumed (`:433-437`); guard debt wired (`protocol_processor_top.sv` `desc_mem_debt_w`); S4 release is `d3_go_i` |
| Command-side triggers and taint-safe whole-record retirement | met | snoop on the µCPU side (`KL_aecp_engine.sv` `d3_chg_w`); `wr_chg_o` DR2b qualifier; taint, set-over-clear, group+index clear (`:857-887`); mutants TRG_*, taint, same-edge, clear_by_* killed |
| Hold AECP ownership from reset through the D3 terminal | met as a hold; **F1** for its side effect on the shared ingress | `own_o` from reset; D3O1/D3S9; probes |
| Both passes, semantic validation, combined restore outputs | met; one direction ungraded (**F3.3**) | `:505-521`, `:646-723`; SET-rule parity checked against `gen_ucode.py` E_SSRATE/E_SSRWALK/E_SCLKS/E_SCFG; combined verdicts `protocol_processor_top.sv:2584-2595` |
| Stage 1 rolls back dynamic and descriptor stores together | met | `store_rst_n_w` on both stores; D3R4/D3R7/D3R10; mutants dyn/store_not_rolled_back killed |
| Debt survives local rollback; watchdog recovery precedes the re-LOCATE | met | guard on the hard reset only; `W_RB` holds while debt (`:699-702`); D3R10 at 5,000 and 16,000 cycles end DEFAULTS |
| Apply the complete §15.2 table | met, except the statements under **F1** | 37 rows in TABLE-15.2.md; rows spot-checked (07, 08, 01, 02, 03, 04, gen_ucode, integrator/operator guides, diagram 21 inventory); `params` gate 25/25/25 |
| Complete its named contract sweep | met (inventory) | my rerun of the named search at head gives 624 matching source lines, identical to the 624 locations in SWEEP.md (0 missing, 0 extra) |
| DR2c for both producers, including binding retry backoff | met in RTL; product derivation and dispatch freedom ungraded (**F3.1, F3.2**) | shadow `H_FL_BACKOFF`; writer `S_BACKOFF`; 3 attempts, sticky alarm, alarm only on the producer's own exhaustion (DR2c-carrier correction), 08 §2 "One alarm" |
| Measure DR3a per-wait and aggregate; product clocks; submit | measured and submitted; the ratification now requires enforcement (**F2**) | `--dr3a` receipt matches the published figures |
| Validation: tb/pp_top with real AECP commands; all declared scalar indices; cleared values first | met | image declares 1 AU, 1 CD, 2+2 streams, all exercised; `rows_cleared()` at the release through harness taps |
| Validation: nvm_port, acmp_nvm, descriptor-guard suites; #18/#19/#21 reconciled | met | my runs: 136, 353 and 78 PASS; 09 §8 states the three issues stay open |
| Validation: full gates at the final head | manager-owned | the author's suite table is at `81c8a5f`; the head adds only the `tb/dyn_state` tally |
| Negative controls (every listed item) | exercised by the external 47-mutant campaign; **F3**, **F4** | MUTANTS.md: 47/47 KILLED, 2 goldens PASS |

## 4. Parent-visible change audit (for the pin-adoption lane)

A diff of the top's port and parameter lists, base against head (`receipts/top-port-param-diff.txt`):

- Exactly five new outputs: `restore_closed_o`, `restore_rb_o`, `rs_cause_o[2:0]`, `restore_cause_o[1:0]`, `d3_unflushed_o`.
- One new parameter: `NVM_RETRY_BACKOFF_CYC_P`.
- No port removed or resized. All six are declared in the PR body.
- The declared semantic changes match the RTL: combined `restore_done/busy/fail/blank_o`, both producers' `nvm_alarm_o`, ADP driven by `entity_enable_i && restore_done_o` (`:1680`) while the side-port lock keeps the requested enable, the AECP hold, and manager-1 record traffic (27 records read twice per boot at the default shape).
- Undeclared parent-visible behaviour: the ingress starvation of **F1**, plus the items in **S1**.

## 5. IEEE 1722.1 / Milan behaviour the change relies on

- **ADP.** `KL_adp_engine` holds its advertise machine in DOWN until its enable. The top gates that enable by the combined terminal, which is monotonic after boot: the binding walk ignores a later `restore_go_i` and `d3_done` is sticky, so no spurious ENTITY_DEPARTING results. The first ADPDU therefore carries the restored configuration index (Milan §5.6.1; D3 §8.1). D3R1 grades the enable every cycle.
- **AECP.** Commands that arrive before the terminal are held, not answered. That is acceptable for the bounded restore, but see **F1** (silent loss beyond the slot pool, and a permanent hold in CLOSED against the IEEE §9.3.2.6 response rule that the processor's own 03 §6 cites) and **S2**.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | §18.1/§15.2/§§3-8 and the four rulings, against the writer, engine, top, shadow, arbiter, guard, stores and gen_ucode rule parity | R390-1 | `e1ae468f7e237f321ce5fee19e59ae157da4b83d` |
| RTL | UNCLEAN (F1, F2) | the full `KL_aecp_nvm_writer.sv`; engine, top, shadow, dyn_state, desc_store, mgr_arb, port, adp hunks; dispatch, normalizer and RX-slot sharing | R390-1 | `e1ae468f7e237f321ce5fee19e59ae157da4b83d` |
| Robustness | UNCLEAN (F1, F2) | CLOSED and slowed-restore ingress probes; deadline, roll-back and debt paths; DR3a rerun | R390-1 | `e1ae468f7e237f321ce5fee19e59ae157da4b83d` |
| Tests | UNCLEAN (F1, F2, F3, F4) | `tb/pp_top` D3 section in full (86 checks) plus the full suite run; seven focused suites; the published 47-mutant campaign; four reviewer mutants and two gap probes | R390-1 | `e1ae468f7e237f321ce5fee19e59ae157da4b83d` |
| Docs | UNCLEAN (F1, F2, F4) | 01, 02, 03, 04, 07 (spot), 08, 09 diffs; integrator/operator guides (spot); suite READMEs; sweep inventory equality; `links`/`matrix`/`modmatrix`/`params` gates | R390-1 | `e1ae468f7e237f321ce5fee19e59ae157da4b83d` |

## 7. Real limits of this review

- The requested simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, which reports `Verilator 5.050 2026-07-01 rev v5.050`; the wrapper and binary hashes are in `receipts/tool-identity.txt`. The system Verilator 5.052 was not used.
- **Not run:** `scripts/run_suites.sh` (the full bank), `lint_hdl.sh`, Yosys/OOC, `make check`'s `lint`/`wavedrom-check`/`stale`, parent consumer gates, xvlog, and the author's 47-mutant campaign. For that campaign I inspected the published summary and driver rather than rerunning it.
- I did not read all 37 §15.2 rows or all 624 sweep dispositions word for word. I checked that the inventory is complete and spot-checked the dispositions.
- The ADP, MAAP and timer ingress exposure in F1 is inferred from the shared slot pool and normalizer. Only ACMP was executed.
- No physical calibration or hardware was used. Field skips are not hardware proof.
- The hosted checks at this head, snapshotted at 15:47Z: `docs-gates` and `portability` completed successfully in two runs; both `suites` jobs were still in progress. Acceptance of hosted runs is the manager's.

## 8. Pending manager duties

- The full processor bank, lint, Yosys, `make check` and the parent consumer gates at this head, and the final current-dev candidate (live dev `ce550952`) at the merge turn.
- A ruling if F1's remedy needs a contract-level drop or refusal rule.
- Round 2 must carry F2 (the aggregate counter), as the ratification anticipates.
- The DR4 post-place comparison and the 8x8 post-place obligation stay with lane 2 (open and blocked, not waived).

## 9. Receipts and reproduction

- Every publishable file is listed in `MANIFEST.sha256`. Paths are relative to the packet.
- **Clone integrity** (`receipts/clone-integrity.txt`): HEAD and tree verified; porcelain status (including ignored files) empty; index and worktree clean; 0 gitlinks (the repository has no submodules); `ls-files -s` sha256 `3c9af644…84a2`. No probe touched the review clone.
- **Reproduce:** `scripts/run_focused_suites.sh <clone> <out> <verilator>`, `scripts/mut_backoff_derivation.sh <clone> <out> <verilator>`, `python3 scripts/r390_mutants.py <clone> <scratch> <verilator>`, `scripts/run_probe_gaps.sh <packet> <clone> <verilator>` (after the mutants script). For the F1 probes, append `scripts/probe_hol.hpp` and `scripts/probe_hol_restore.hpp` to a copy's `tb/pp_top/d3_phases.hpp`, add the `--probe-hol` and `--probe-hol-restore` switches beside `--dr3a` in its `sim_main.cpp` (as `run_probe_gaps.sh` does for `--probe-gaps`), then `make gsi-build`.

R390-1 FINISHED
