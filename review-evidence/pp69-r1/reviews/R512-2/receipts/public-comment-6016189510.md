https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165#issuecomment-6016189510

[R512] NEGATIVE - exact head cb730a2f9dd7e4f60a03a38d4b47b569e68da8df

# R512-1 independent internal review: issue #69 / PR #165

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #165 ("Closes #69").
- Exact head `cb730a2f9dd7e4f60a03a38d4b47b569e68da8df`, tree `f18d266c67b8b0f79341168ecdac8b4655b50b06`
  (the author's head `d723574a` plus the manager's `--no-ff` merge of main `86a7b0c5`, #134 and #22).
- Source base `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`.
- Round R512-1, internal reviewer, cleared context, own detached clone.

## Verdict

**NEGATIVE.** Three MINOR findings are open (F1 to F3). All five lenses are unclean.

The core of the PR is sound, and most of its claims reproduce at this head:

- The top threads the interface count to the ADP engine.
- The frame's interface rides the header beat with correct alignment.
- The registry stores the port, and the AVB_INTERFACE counter-notification slots are keyed.
- At count 1, every cell count is identical.
- Every planted arm plants, and all 25 #69 controls are killed.
- Every graded suite passes.

The defects are all in the two-interface configuration that this PR makes legal:

- **F1:** a command that should save a controller registered on both interfaces cancels only one of its two live availability probes.
- **F2:** the top-level checks do not grade where the registry port comes from, although the documents say they do.
- **F3:** at two interfaces, the shared 16-row registry is below the repository's own Milan 5.3.4.2 requirement of at least 16 per interface. F01.5 and REQ-SCP-003 do not say so.

## Scope reconstructed (public sources only)

- **Guidance.** `README.md` and `docs/README.md`: single-source rules (F01.5 parameters, F08.1 timing), figure rules and editing workflow. `hdl/README.md`: tool floor, Verilator plus sv2v/Yosys for every module; every RTL commit carries its testbench. The repository has no AGENTS.md or CONTRIBUTING.md at this head.
- **Issue #69 body (frozen acceptance 1 to 7).**
  - The top exposes P-N-AVB-INTERFACES and passes it to `KL_adp_engine`.
  - `KL_aecp_notify` stores the port per row when the count is above 1, or the seam is closed by decision.
  - One suite or lint builds N_IF_P = 2.
  - The REQ-SCP-003 Arch cell names what is and is not keyed.
- **Assignment comment 6010216843 (public scope decision).** The owner's standing rule is to keep the redundancy path open, so the seam is threaded through, not closed. Items:
  1. A top parameter, plus an interface-index input "only at the top", default 0.
  2. The registry port (the Milan v1.2 5.3.4.2 tuple) at count above 1, not generated at 1.
  3. AVB_INTERFACE counters keyed per interface; anything unkeyed named with its reason.
  4. No change at count 1: Yosys statistics, suite records, OOC 1x1 delta of 0 LUT / 0 FF.
  5. Elaborations at two interfaces, including a planted index-collapse mutant.
  6. The banner, 01 section 7 and the REQ-SCP-003 cell.
  7. A pre-edit grep, and every arm still plants.
- **Mark II note 6009640296.** The fabric part of the ticket stays valid for the all-fabric build.
- **Diff and history.**
  - `git diff e6a759de..cb730a2f`, separated into the PR's own commits (`e6a759de..d723574`: 42 files, 2 RTL files) and the merged main.
  - The merge is clean: no file is changed on both sides. A recomputed `git merge-tree d723574 86a7b0c` gives exactly the published tree `f18d266c` (`receipts/merge-check.txt`).
- **Public evidence tree** (`kebag-logic/milan-fpga@83221a43:review-evidence/pp69-r1`). It holds the author's HANDOFF, the PR body and a parent test patch; no manager bank receipts were in it (see limits). The PR description carries the manager's merge note. The issue and PR carry no other manager evidence comments.
- **Prior public review findings on PR #165.** None exist: no reviews and no review comments; the only PR comments are the two review-start notices. Nothing needs to be resolved or retained.

## Findings

### F1 - MINOR - one command cancels only one of two live availability probes of the same controller at two interfaces

- **Lenses:** RTL, Robustness, Tests.
- **Where:**
  - `hdl/aecp/KL_aecp_notify.sv:571-593` (`monitor_pick`): `ca_cancel_ok_w` and `ca_cancel_ix_w` select one row per cycle.
  - `:653-665` (`ca_request`): one `ca_cancel_owner_o` per cycle.
  - `:1170-1176`: a command clears `ca_probe_r` of every hit row.
  - `:1193-1198`: a reported failure removes its row whether or not that row's probe flag is still set.
- **Authority:**
  - The module's own rule at `:1168-1169`: "Any valid command from a registered controller supersedes an old monitor deadline".
  - The PR's claim in the banner `:27-29`, REQ-SCP-003 and 06 section 7: "the availability monitor matches {Entity ID, MAC} on any interface, since a command on either proves the controller alive".
  - Before this PR no two rows could share an {Entity ID, MAC}. With `N_IF_P` = 2 they can, so the single-row cancel path is now reachable with two hits.
- **Evidence:** probe P3 (`scripts/probes.sh`, `scripts/probe_ca_dual.hpp`, `receipts/public/probe-ca-dual.summary.txt`), run on tb/aecp_notify's third build at the head, with no RTL edit:
  1. E is registered on ports 0 and 1.
  2. Both monitor deadlines expire and both probes are issued (owner mask 0x3).
  3. One command from E produces one cancel strobe, for owner 0 only (mask 0x1).
  4. The failure of owner 1's un-cancelled exchange then takes the rows from 2 to 1 and presents a DEREGISTER notification to E.
- **Impact:**
  - At `N_AVB_IF_P` = 2 only; the shipping count-1 build is unaffected.
  - A controller registered on both interfaces, which has just proved itself alive, can lose one entry and be sent a DEREGISTER. The uncancelled exchange also stays in the originator's in-flight table.
  - No count-2 check or control covers two probing rows of one controller.
- **Required outcome:**
  - Every hit row with a live probe has its exchange cancelled; for example, a per-row cancel-pending bit drained one per cycle. Alternatively, an orphaned exchange's response or failure cannot drain a row whose probe a command has already superseded, and no owner can then have two exchanges in flight.
  - Add a count-2 check of this case with a control that fails it.
  - If the author and manager instead choose to accept it, name it as a count-2 limitation in the banner, 06 section 7 and REQ-SCP-003.
- **Verification:** probe P3 shows a cancelled mask equal to the probing mask and no row removed. The new check passes at head and fails under its control.

### F2 - MINOR - the top-level checks do not grade the registry port's source, though the README and 09 say they do

- **Lenses:** Tests, Docs.
- **Where:**
  - `tb/pp_top/interface_phases.hpp:171-193` (IF3, IF3b and the IF3b check text at `:189-191`).
  - `tb/pp_top/README.md:2592-2594`: "IF3b ... at interface 0's 2 and 3: the registry port comes from the command's interface".
  - `docs/architecture/09_verification.md:429`, section 8.9 row: "the registry port comes from the command's interface".
  - The RTL under test: `hdl/top/protocol_processor_top.sv:4005-4017` (`aecp_cmd_if_latch`) and `:4052`.
- **Authority:**
  - The PR's design statement: the port is "latched on the handshake that loads the engine's `cmd_r`".
  - Assignment item 5 asks that the seam be graded so that it cannot rot.
  - `hdl/README.md` rule 3 requires the suite to prove what its README states.
- **Evidence:**
  - **Probe P1** (`receipts/public/probe-rgyport-hdr.summary.txt`) drives `u_notify.rgy_port_i` from `hdr_if_r`, the most recent received frame's interface, instead of the command's handshake latch. All six IF checks pass: "IF: 6 checks, 0 failures". The bench never receives a frame on the other interface between a REGISTER or DEREGISTER and its execution, so this alignment is graded nowhere.
  - **Probe P2** (`receipts/public/probe-dereg-other-port*.summary.txt`) makes DEREGISTER match the other port's entry. IF3 and IF3b pass, because both entries hold sequence_id 2 when the DEREGISTER arrives. Only the module-level PT6 kills it.
  - So the IF3b text "removes interface 1's entry ... at interface 0's sequence_id 2 and 3" is not observed by the check.
- **Impact:** a plausible defect survives every check. Taking the port from the latest frame would store the wrong port whenever traffic on the other interface (an ENTITY_AVAILABLE, for example) lands between a registry command's reception and its execution. Two documents state a property that the suite does not establish.
- **Required outcome:**
  - Add a top-level check in which a frame on the other interface is received after the REGISTER or DEREGISTER and before the engine runs it, so that the stored port must be the command's own.
  - Make IF3b distinguish which entry remains; for example, give the two entries unequal sequence IDs before the DEREGISTER, or follow it with a DEREGISTER on interface 0 that must leave none.
  - Plant P1-style and P2-style controls that must fail.
  - Otherwise, narrow the README, 09 section 8.9 and the check text to what IF grades.
- **Verification:** P1 and P2 fail at the top level; the new checks pass at head.

### F3 - MINOR - at two interfaces the 16-row shared registry falls below the documented Milan 5.3.4.2 minimum, and F01.5 and REQ-SCP-003 do not say so

- **Lenses:** Conformance, Docs.
- **Where:**
  - `docs/architecture/01_overview.md:162`: the F01.5 P-N-CONTROLLERS range is "≥16 per interface (Milan §5.3.4.2)".
  - `:147`, Δ12: "≥16 per interface".
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:428`, REQ-AEM-016: "≥16/interface", Cov C.
  - Against these, `docs/architecture/01_overview.md:159` (the F01.5 P-N-AVB-INTERFACES row) and `docs/00_MILAN_COMPLIANCE_REVIEW.md:523` (the REQ-SCP-003 Arch cell) list "the registry depth" only as "not keyed".
  - Only `docs/architecture/06_aecp_engine.md:969-971` sets "≥ 16 entries per AVB interface" beside "16 entries in all: at two interfaces they are shared".
  - The F08.4 map at two interfaces reserves `2 * n_ctrl * n_if` monitor slots (`hdl/common/pp_pkg.sv:201`) for a per-interface depth that the RTL does not build.
- **Authority:**
  - `docs/README.md` section 2: parameter ranges live in F01.5, and a value or range stated elsewhere is a review finding.
  - The repository's own reading of Milan v1.2 5.3.4.2 as at least 16 entries per AVB interface.
- **Impact:**
  - `N_AVB_IF_P` = 2 is now a legal elaboration (the top accepts it, and the suites and lint build it). It ships with `P-N-CONTROLLERS` = 16 in all, which violates the F01.5 range of the companion parameter.
  - The seam's defining rows (01 section 7, REQ-SCP-003) name the depth as unkeyed but do not state the conformance consequence. REQ-AEM-016's ≥16/interface claim is unscoped.
  - This touches a conformance claim, so it is not wording-only RESIDUE.
- **Required outcome:** either key the depth at two interfaces, or state the consequence where the seam is defined:
  - In F01.5 (the P-N-AVB-INTERFACES row or the P-N-CONTROLLERS range) and in REQ-SCP-003, say that at 2 the registry holds `P-N-CONTROLLERS` in all, below Milan 5.3.4.2's ≥16 per interface, so a two-interface build does not meet that clause.
  - Scope REQ-AEM-016's ≥16/interface to the one-interface build.
- **Verification:** `make check` passes; F01.5, REQ-SCP-003 and REQ-AEM-016 agree with 06 section 7 and the RTL.

### Suggestion (does not affect the verdict)

- **S1** (Tests): the PR body's "96 of 96" other exact-text arms.
  - My enumeration, through each driver's own counting rule, finds 94: retry 70, gsi 20, srp_admission 3, name_wr 1.
  - All 94 plant at base, at the author head and at this head, so the property claimed holds.
  - State the enumeration so that the figure can be reproduced.

## Acceptance and assignment, item by item (at this head)

| Item | Result | Evidence |
|---|---|---|
| #69 acc. 1 / asg. 1: the top exposes `N_AVB_IF_P` (default 1, 1 or 2 enforced) and passes it to `KL_adp_engine` (`:1973`); `rx_if_index_i` drives the normalizer from the frame's interface above 1 (`:1546-1564`, `:1720`) | met | RTL read. The alignment matches the validator's `hdr_valid_o` at t_end+3 (`KL_pp_rx_validator.sv:194,509,695-697`) and the header latch's own acceptance condition. The integrator guide's complete-frame contract excludes runts. `if-top-ingress-*` controls killed |
| #69 acc. 2/5 / asg. 2: port per registry row above 1, not generated at 1 | met, with F1 | `g_port`/`g_no_port` (`KL_aecp_notify.sv:521-539`). Yosys cell counts identical at 1 |
| asg. 3: counters keyed / unkeyed named | met | Notification slots per AVB_INTERFACE (`:415`, `:736-745`, `:1151-1158`). Unkeyed items named in the banner, 01 section 7 and REQ-SCP-003 |
| asg. 4: no change at 1 | met (see deviation) | Yosys `stat -json` (the run.sh recipe) for KL_aecp_notify, KL_adp_engine and protocol_processor_top at base, author head, main `86a7b0c5` and this head. Every cell count identical; ADP byte-identical. Only differences: `rx_if_index_i` and `rgy_port_i` (2 bits each, 6 port/wire counters) and two derived names. The SRP FSM cell changes at this head against base come from merged main (#134) and are identical between main and this head (`receipts/yosys/compare-*.txt`). Pre-existing suite records identical (`receipts/public/diff-*.records`). OOC 1x1 not re-measured (limits) |
| #69 acc. 3/6 / asg. 5: builds at 2, planted index-collapse mutant | met, with F2 | `tb/adp_engine` 1359 (IF 11), `tb/aecp_notify` 56 (PT/CK 11), `tb/pp_top` 10450 (IF 6), `if-guards` 4 of 4, all rc 0. Yosys also elaborates the top at `N_AVB_IF_P=2` and notify at `N_IF_P=2`. Index-collapse controls killed |
| #69 acc. 4/7 / asg. 6: banner, 01 section 7, REQ-SCP-003 | met, with F3 | Read against RTL. `make check` rc 0. Diagram 21 rendered and inspected (no overlap) |
| asg. 7: every arm plants | met | Patches plus `plant()` arms: 476/476 at base, 500/500 at `d723574`, 506/506 at this head (the 6 extra are #134's srp_top patches). Other exact-text arms 94/94 at all three. 0 refusals (`receipts/plant-*.txt`) |

**The `rgy_port_i` deviation is needed and acceptable.**

- Item 2 requires the registry module to know each REGISTER's interface. The module runs serially and is separate from the engine, so the value must cross a module boundary. A new internal input is the least invasive way; widening the engine's registry face would change the engine, which this PR leaves byte-identical.
- I read "an interface-index input port only at the top" as a limit on the integrator-visible boundary, and that boundary gains exactly one port (`rx_if_index_i`, default 0, unread at 1).
- The statistics deviation is inherent: item 1's own new top port already moves the top's port counters.
- Measured: every cell count is identical at count 1, and the only differences are the two 2-bit ports and their wires.

## Executed evidence (all with Verilator 5.050 through the pinned wrapper, identity in `receipts/tools.txt`)

| What | Result | Receipt |
|---|---|---|
| Suites `adp_engine`, `aecp_notify`, `pp_top`, `timer_map` at base and head | all rc 0. head 1359 / 56 / 10450 / 1360; base 1348 / 45 / 10444 / 1360. Pre-existing build tallies identical | `receipts/public/*-*.summary.txt`, `*.rc`, `diff-*.records` |
| `make check` (disposable git clone at head), `gen_matrix.py --check` | rc 0, rc 0 | `receipts/make-check-head.log`, `receipts/gen-matrix-check-head.log` |
| Planting: every `tb/**/*.patch` (`git apply --check`), every `plant()` arm, every other exact-text arm | 0 refusals at base, `d723574` and head | `scripts/plant_check.py`, `receipts/plant-plant-*.txt`, `receipts/patch-plant-head.txt` |
| ADP campaign, the 16 `if-` arms plus 3 controls, at head | 19/19 (16 KILLED) | `receipts/campaigns/adp-if.*` |
| Notify campaign, the 9 #69 arms plus 2 goldens, at head | 9/9 KILLED, goldens PASS | `receipts/campaigns/notify-69.*` |
| Yosys count-1 identity and count-2 elaboration | as in the table above | `scripts/yosys_stat.sh`, `scripts/stat_compare.py`, `receipts/yosys/` |
| Reviewer probes P1 to P3 | P1 survives, P2 survives at the top (killed by PT6), P3 shows F1 | `scripts/probes.sh`, `receipts/public/probe-*` |
| Clone restored | HEAD, tree, index and worktree equal the exact head; no gitlinks at this head | `receipts/clone-integrity.txt` |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | Issue #69 acceptance, assignment 6010216843; Milan 5.3.4.2, 5.6.3 and Table 5.22 as quoted by 00, 01 and 06; REQ-SCP-003, REQ-AEM-016, Δ12, F01.5; ADP per-interface machines; registry tuple; counter rows; the talker's interface check | R512-1 | cb730a2f9dd7e4f60a03a38d4b47b569e68da8df |
| RTL | UNCLEAN (F1) | `protocol_processor_top.sv` (parameter, guard, `hdr_if_latch`, normalizer index, ADP instance, `aecp_cmd_if_latch`, notify instance, debug buses, timer map); `KL_aecp_notify.sv` (`g_port`, walk, counter slots, availability monitor, CA cancel/fail paths); `KL_pp_rx_validator.sv` commit timing; `KL_aecp_engine.sv` `cmd_r` handshake; `KL_aecp_ca_originator.sv`; `KL_pp_originator.sv` cancel/CAM; `pp_pkg.sv` timer map; Yosys at counts 1 and 2 | R512-1 | cb730a2f9dd7e4f60a03a38d4b47b569e68da8df |
| Robustness | UNCLEAN (F1) | Back-to-back frame alignment versus t_end+3 and the RX complete-frame contract; header-latch overrun mirroring; reset of the new registers; duplicate {EID, MAC} rows against the monitor, the CA builder and the originator's in-flight table (probe P3); out-of-range counts (guard) | R512-1 | cb730a2f9dd7e4f60a03a38d4b47b569e68da8df |
| Tests | UNCLEAN (F1, F2) | `sim_if2.cpp`, `port_tuple.hpp`, `interface_phases.hpp`, `if_guards.py`, the three Makefiles and wraps; suites at base and head; the #69 campaign arms; planting of every arm; probes P1 and P2 | R512-1 | cb730a2f9dd7e4f60a03a38d4b47b569e68da8df |
| Docs | UNCLEAN (F2, F3) | Banners; 00 REQ-SCP-003; 01 F01.5; 02; 06 sections 6.6 and 7 and the storage table; 09 section 8.9; integrator guide; diagram 21 (rendered); three suite READMEs; `make check` | R512-1 | cb730a2f9dd7e4f60a03a38d4b47b569e68da8df |

## Real limits

- **Not re-measured:** the OOC 1x1 Vivado delta, the parent consumer set of 17 and the hosted jobs. Neither Vivado nor parent banks are permitted here. My count-1 evidence is the Yosys cell identity, which supports but does not replace the Vivado census.
- **Not run:**
  - The full processor sweep (`run_suites.sh`), `lint_hdl.sh` and the full Yosys `run.sh` bank. Only the four suites that build a changed module ran, plus the top's lint at counts 0 to 3 through `if-guards`.
  - The pre-existing arms of the ten campaigns. Their planting was checked, not their simulation.
- **Manager evidence:** the public evidence path named for this round contains only author material. I found no executable manager receipts there for this head.
- **Milan PDF:** not available. Clause references rely on the repository's own quotations (00, 01, 06).
- **Hardware:** physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry F1 to F3 to the author. Re-review is required after the fixes, at a new exact head.
- Publish or link the manager's full source static/builder and native bank receipts at this head. Before merge, build the final current-dev candidate on source base `e6a759de` against live dev `bd884631`.
- Own hosted/act acceptance, the OOC 1x1 Vivado delta and the parent consumer set at the final candidate.
- Two independent positive reviews are still required for merge.

R512-1 FINISHED

