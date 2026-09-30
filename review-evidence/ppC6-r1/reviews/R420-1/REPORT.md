[R420] NEGATIVE - exact head 5e806296b73d04ccf095ad00e081cb790fbbaf8d

# R420-1: internal independent review of processor PR #139 (lane C6, issue #80)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #139, closing #54, #58, #80, #86.
- Exact head `5e806296b73d04ccf095ad00e081cb790fbbaf8d`, tree `ebe7b48fe653437d1bed59f510c15d5d62163144`; base (processor main) `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff`; five commits `018ee6c`, `b5beed6`, `4ce963e`, `5cf99f7`, `5e80629`.
- Reviewer: [R420], internal role, cleared context, own detached clone. Round R420-1.
- Verdict: **NEGATIVE**. Two MINOR findings are open (R420-1-F1, R420-1-F2). F1 is attributable to all five lenses, so no lens is covered clean at this head. Apart from F1 and F2, every acceptance item and every ruling condition I checked is met, and every gate and entry point I re-ran returned rc 0 (section 6).

## 1. How the task was reconstructed

Public sources, read in this order:

1. The processor repository has no `AGENTS.md` or `CONTRIBUTING.md`. The parent (milan-fpga) `AGENTS.md` sections 6 and 7 at `2c532827` supplied the reviewer procedure, the five lenses, the severity scale and the ledger rule. I then read the processor `README.md` and `docs/README.md` (conventions, single-source rules, identifier registries).
2. Issue bodies: #80 (acceptance 1-4), #54 (1-4), #58 (1-3), #86 (1-4). On #80: the assignment 5915639621, the executor's design-gate STOP 5915752457, and the manager ruling 5915765717. The ruling authorizes `identify_button_i` and `EN_IDENTIFY_NOTIF_P` under four conditions: default 0 with zero area and the OOC cost at 0 and 1; synchronized/debounced, or an integrator debounce contract; a declared parent tie-off plus port-contract/naming and guide/diagram-21 edits; both settings graded.
3. Authorities, as cited by the diff and the issues: IEEE 1722.1-2021 §7.4.39 / Figure 7-61, §7.4.15.1 / Figure 7-40, §7.5.1, §7.5.1.2.1, §7.5.1.3 / Figure 7-142, §7.5.2; Milan v1.2 §5.4.5.1-§5.4.5.4, Table 5.22, §5.4.2.9 / §5.4.2.10. Architecture: 01 F01.5, 02 §1/§2/§6, 03 §4/§5, 06 §2/§7, 08 F08.1/F08.4, 09 §8.3, and the three guides.
4. `git diff 0451d83d..5e806296` (26 files, +2533/-99) and each commit.
5. Public evidence: `kebag-logic/milan-fpga@2c532827:review-evidence/ppC6-r1`. I read MANIFEST.json, both parent adoption patches (including the one rebased at dev `e4b771f9`), the NP3 failing-arm log and the two equivalence summaries. I did not open the published `author/HANDOFF.md`. Neither #80 nor #139 carried a manager evidence comment beyond the review-start notices. Hosted checks at the exact head are in section 7.

**Prior public review findings on this PR:** none. When this round ran, #139 carried only the two review-start comments (`5921034846`, `5921039530`) and no review objects, so there is nothing to resolve or retain.

## 2. Findings

### R420-1-F1 MINOR: a TX stall mid-burst bunches IDENTIFY_NOTIFICATION frames, while the RTL, the docs and a test name claim it never can

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/aecp/KL_aecp_notify.sv:726-728`: frames 2 and 3 are armed at the absolute deadlines `t0 + 150` and `t0 + 300`, both measured from the first frame.
  - `hdl/aecp/KL_aecp_notify.sv:155-159` (banner): "each is armed only once the frame before it has gone, so a held engine delays a burst but never bunches it".
  - `docs/architecture/08_timing.md:30` (F08.1 T-IDENT-BURST row).
  - `docs/architecture/09_verification.md:224` ("three frames spaced `T-IDENT-BURST` (never less)").
  - `tb/pp_top/notify_phases.hpp:387-407` (ID6, `a_held_engine_never_bunches_a_burst`).
  - `tb/pp_top/README.md:1223-1226` (ID6 bullet).
  - PR body section 1.
- **Authority and evidence:** IEEE 1722.1-2021 §7.5.1 / §7.5.1.2.1, as the bench quotes it (`notify_phases.hpp:149-152`): "sent three times with a 150 ms delay between transmissions". The timer service fires an already-past deadline on the next sweep (`hdl/common/KL_pp_timer_service.sv:18-19`). So if frame 2 leaves late, nothing holds frame 3 back 150 ms after it. The reviewer probe `scripts/probe_bunch.py` ran on an isolated copy of the head's `tb/pp_top`, third build, with no RTL change. It holds the MAC's `tx_ready_i` low right after frame 1 of a press and measures the wire gaps (`receipts/probe_bunch_run.log`, 100 clocks = 1 ms):

  | TX stall after frame 1 | gap 1->2 | gap 2->3 |
  |---|---|---|
  | 100 ms | 15,264 clk (152 ms) | 15,000 clk (150 ms) |
  | 250 ms | 25,060 clk (250 ms) | 5,204 clk (52 ms) |
  | 400 ms | 40,060 clk (400 ms) | 63 clk (< 1 ms) |

  ID6 holds the engine only before the first frame (from reset to the restore terminal), so the check named for this property never covers a hold between frames. All 62 section-ID checks pass at the head, and the probe build's own tally stays green (65 checks, 0 failures).
- **Impact:** any TX back-pressure or lane starvation of about 150 ms or more inside a burst makes the remaining frames leave closer than 150 ms, down to back-to-back. That defeats the temporal spacing that §7.5.1 gives the three copies. It also contradicts the design statement in the RTL banner, F08.1, 09 §8.3, the suite README and the PR body. The feature is a "should", it defaults to 0, and the stall is abnormal, so this is MINOR and not higher.
- **Required outcome:** one of the following, applied consistently in RTL, docs and tests:
  - (a) each later frame goes at least T-IDENT-BURST after the previous frame actually retired, so the spacing holds under any stall, and a mid-burst stall is graded; or
  - (b) the t0-anchored schedule stays, and every "never bunches" / "never less" / "each armed once the frame before it has gone, so ..." statement is corrected to the real bound, which a mid-burst stall check then grades.
- **Verification:** a directed check with `tx_ready_i` (or the UNS lane) held low between frames 1 and 2 and between frames 2 and 3, grading the gaps against the chosen contract, plus a mutant the check kills. The reviewer probe can be re-run unchanged.

### R420-1-F2 MINOR: the HDL engineer's contract still says no CDC lives inside the modules

- **Lenses:** Docs.
- **Where:**
  - `docs/guides/hdl-engineer.md:64`: "CDC | none is inside these modules. ... the synchroniser is the integrator's".
  - `hdl/README.md:24-25`: "There is **no CDC primitive** ... in this tree: every clock crossing is the integrator's".
- **Authority and evidence:** ruling condition 2 put the synchroniser inside the core. The lane placed a 2FF synchroniser inside `KL_aecp_notify` (`hdl/aecp/KL_aecp_notify.sv:700, 754-755`) and updated the integrator guide (`docs/guides/integrator.md:32-40`, "No clock-domain crossing lives inside this processor but one"), 02 §2 rule 3 (`docs/architecture/02_interfaces.md:90-93`) and diagram 21. The two statements above were left as they were, and they are the ones addressed to someone modifying a module.
- **Impact:** the authoritative HDL rule table now contradicts the RTL and the other three documents. An engineer who follows it will take the in-core synchroniser for a rule violation, or reject a correct design in review on the strength of the stale rule.
- **Required outcome:** both statements name the one exception, `identify_button_i`'s 2FF inside `KL_aecp_notify`, present only with `EN_IDENTIFY_NOTIF_P` = 1, consistently with the integrator guide and 02 §2.
- **Verification:** read both lines at the new head; `make check` stays rc 0.

### Suggestions (do not affect coverage)

- **R420-1-S1 SUGGESTION (Tests, RTL):** `hdl/aecp/KL_aecp_notify.sv:722` (`&& !core_arm_w`) and `:785` (`gen_r <= !gen_r`) are not exercised by any check. Reviewer mutants that remove each one survive all 62 section-ID checks (`receipts/extra_mutants/`, SURVIVED, run rc 0).
  - The arm arbitration looks unreachable in practice: the engine is single-threaded and reaches a registry op only several cycles after an identify job retires.
  - The REARM generation guards a window of about two cycles after a first frame retires.

  Either record both as equivalence/defensive controls in the mutation record, or add directed checks. The third reviewer mutant, removing the synchroniser's second flop, is a CDC-hygiene control and is expected to survive simulation.
- **R420-1-S2 SUGGESTION (RTL):** the in-core synchroniser flops (`KL_aecp_notify.sv:700`) carry no placement/metastability attribute. The integrator guide says the pin "may come straight from a pin", and the tree already uses synthesis attributes (`(* ram_style = ... *)`). Add an `ASYNC_REG`-style attribute on `btn_q1_r`/`btn_q2_r`, or state the constraint the integrator must add.
- **R420-1-S3 SUGGESTION (Docs, PR evidence):** the PR body attributes the head-at-0 LUT delta (+320, whole top) to mapper variance, citing "`KL_aecp_notify` alone maps 6,598 vs 8,002 LUT at the same 1,721 FF". No flow is given for that figure. My block-level run (sv2v, `synth_xilinx -family xc7 -flatten`, default parameters) gives 6,454 LUT (main) vs 6,549 LUT (head at 0), with FF 1,721, CARRY4 249 and RAM32M 1,048 identical (`receipts/ooc_notify_gold.stat`, `receipts/ooc_notify_gate.stat`). That supports the zero-area claim better than the quoted pair. State the flow, or replace the numbers.
- **R420-1-S4 SUGGESTION (Conformance, pre-existing):** ST2b accepts GET_COUNTERS rounds 99,994 clocks apart (999.94 ms on the compressed timebase), one limiter tick under Milan Table 5.22's "at most once per second". The limiter predates this lane. Either measure from a sub-ms-safe reference, or record the one-tick tolerance as a decision.

## 3. Acceptance and ruling, item by item

Every item below is met at this head, except where F1 is noted.

| Item | Result | Evidence |
|---|---|---|
| Ruling cond. 1: default 0, zero area, OOC at 0 and 1 | Met | `protocol_processor_top.sv:182`, `KL_aecp_notify.sv:199`, `KL_aecp_engine.sv:321`, all default 0. At 0, `gen_no_ident` (`KL_aecp_notify.sv:823-839`) leaves no flop. Reviewer equivalence, `KL_aecp_notify` head@0 vs main: 6,930 `$equiv` proven, 0 unproven; the negative control fails with 36 unproven (`receipts/equiv_notify*.log`). Engine at 0: an 18-line diff whose only behavioural change is the SET_STREAM_INFO µPC; the new kind-15 arm yields exactly the default arm's `{0, UPC_NOSEND}` (`KL_aecp_engine.sv:1383-1388`); the author's engine summary shows 21,481 proven (evidence). Block OOC: FF, CARRY and RAM equal at 0; at 1, +64 FF, +22 CARRY4, +451 LUT (`receipts/ooc_notify_gate_en1.stat`). The PR reports whole-top figures (yosys; Vivado pending at the parent). |
| Ruling cond. 2: sync / debounce contract, ignored at 0 | Met | 2FF at `KL_aecp_notify.sv:754-755`. Integrator debounce contract at `protocol_processor_top.sv:226-233`, `integrator.md:295-303`, 02 F02.1/§6. Unread at 0: the equivalence above, ID0/ID0b, and mutant `ident_built_at_default` KILLED. The docs residue is F2. |
| Ruling cond. 3: parent-visible list | Met (declared) | PR body section 5. The evidence patch `parent-adoption-c6-e4b771f9.patch` holds exactly the two parent edits: the `KL_pp_shadow` tie-offs `.identify_button_i(1'b0)` and `.EN_IDENTIFY_NOTIF_P(1'b0)`, each with a `//!` rationale, and the `DUT_READER_DISPOSITIONS` entry for `notify_mutants.py`. The disposition is accurate: the script reads HDL text only to plant exact edits into an isolated copy and reads no expected value, like the `d3_mutants.py` precedent. The integrator guide §1/§2/§6 and diagram 21 carry the parameter; `make check` reports parameters 27 = 27 = 27. I did not run the parent gates (not allowed). |
| Ruling cond. 4: both settings graded | Met, with F1 | At 1: section ID, 62 checks, 11 identify mutants KILLED. At 0: ID0, the unchanged default build (7,996) and the equivalence above. |
| #54 acc. 1-4 | Met, with F1 | Frames byte-exact (`notify_phases.hpp:176-198`): DA 91-E0-F0-01-00-01, controller 90-E0-F0-FF-FE-01-00-01, u = 1, CONTROL/`identify_index_i`, cdl 16. Spacing through the IDENT-BURST singleton; re-arm from the first frame (ID2d); A6 BAD_ARGUMENTS unchanged (ID4); 06 §7 and GAP-06 updated. |
| #80 acc. 1 | Met, with F1 | as #54 |
| #80 acc. 2 (STORM) | Met | ST1: 16 rows, 15 byte-exact frames at per-entry sequence_ids 0, 1 and 2. ST2: `ctr_change_i` at 10 Hz on five descriptors, at most one round per second. ST3: every solicited probe answered within T-BUDGET-AECP-WC / T-BUDGET-ACMP-RESP, counted in clocks. `counter_limit_500ms` and `fan_out_skips_row_0` KILLED. S4 is a note only. |
| #80 acc. 3 (RND) | Met | RN: seed 0xC6A46301, 720 steps from 20 controllers against `RndPhase::Model`, which is written from the clauses, not the RTL; zero divergence; anti-vacuity check RN b; README mutation record; seven RN mutants KILLED. |
| #80 acc. 4 | Met | GAP-06 "Landed 2026-09-30" paragraph in `docs/00_MILAN_COMPLIANCE_REVIEW.md`; 06 §7 "Identify (lane C6)". |
| #58 acc. 1 | Met | NP1-NP9b cover SET_CONFIGURATION (both ways), SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CONTROL (255/0), SET_SAMPLING_RATE and STOP/START_STREAMING. Each pushes one byte-exact u = 1 response to the second controller at its wire-modelled sequence_id and none to the requester; unchanged SETs push nothing. |
| #58 acc. 2 | Met | `enq_dropped_configuration`, `enq_dropped_stream_info`, `class_4_mapped_to_rate` and `class_9_mapped_to_control` each KILLED on the named NP checks; recorded in `tb/pp_top/README.md`. |
| #58 acc. 3 (second arm) | Met | 06 §7 trigger class (2), the REQ-NOT-002 row, 03 §5 item 4 and GAP-17 all state that MGMT-origin changes are not supported. I checked this against the RTL: the side-port image window's write outputs are left unconnected at the top (`protocol_processor_top.sv:4440-4443`), and `KL_aecp_dyn_state` is written only through the µcode store face and the D3 restore. |
| Item 3: SET_STREAM_INFO fix | Met | `KL_aecp_engine.sv:1372-1375` and `gen_ucode.py:2065-2098` (`E_SINFOUNS`): the 84-byte Figure 7-40 body, cdl 96, per-output `SEL_PTOFF` (the dyn store indexes by the job's descriptor index). Failing-before arm: the evidence log shows NP3 got 94 B / cdl 0x44 vs expected 122 B / cdl 0x60, and my run KILLED `stream_info_get_body` (the old mapping put back) on NP3. |
| #86 acc. 1 and 4 | Met | 03 §4/§5 now describe the landed shape: RX-only dispatch, the expiry bus, engine-internal SELF jobs, CONTROLLER_AVAILABLE through the originator, the listener owning the PROBE_TX retry (`PROBE_SLOTS_P = 0`), MGMT not supported. Top tie-off comments at `protocol_processor_top.sv:1509-1522`. |
| #86 acc. 2 | Met, with F1 | as #54 |
| #86 acc. 3 | Met | `tb/originator` R: seed 0x86A46301, 4,000 steps, 16 owners, up to eight live exchanges, responses, expiries and cancels in random order against `IflModel`; four inflight mutants KILLED. |
| `notify_mutants.py` 30 of 30 | Reproduced | The author's entry point returned rc 0 with "30 of 30 KILLED; goldens PASS". A separate driver using the script's own `judge()` also gave 30 of 30 KILLED with no named check missing (`receipts/mutants/`, `receipts/notify_mutants_entry*`). |

## 4. Lens results (artifact-specific)

- **Conformance: UNCLEAN (F1).** Checked:
  - IDENTIFY_NOTIFICATION frame bytes and header fields against §7.4.39.1 / §7.5.1: the `ident()` expectation (`notify_phases.hpp:176-184`) against `E_IDNOTIF` (`gen_ucode.py:949-956`);
  - identifySequenceID per burst and the Figure 7-142 re-arm from the first frame (`KL_aecp_notify.sv:771-806`);
  - the Figure 7-40 body layout of `E_SINFOUNS`, offsets @24 to @108;
  - Milan §5.4.5.1/.2 requester exclusion and per-entry sequence (NP, ST1, RN);
  - the command-form refusal (ID4).

  No other conformance defect found.
- **RTL: UNCLEAN (F1).** Checked the whole identify sequencer (`KL_aecp_notify.sv:677-839`):
  - face hand-over only outside `N_EMIT_WAIT`, and the `core_done_w` masking;
  - the withdrawal path while the identify job owns the face;
  - arm-output sharing: every registry arm site is `N_IDLE && rgy_new_w` or `N_APPLY` (`:1081-1124`, `:1219-1270`), so `core_arm_w` is complete;
  - owner tags 0xB1/0xB2/0xB3 and the top's overlap guard (`protocol_processor_top.sv:846-849`);
  - modular deadlines and synchronous reset;
  - the engine's kind-15 map;
  - µcode placement inside the 2048-word ROM, under the overlap assert (`gen_ucode.py:358-369`).

  Lint is clean at `EN_IDENTIFY_NOTIF_P` = 1 for `KL_aecp_notify`, `KL_aecp_engine` and the top (`receipts/lint_en1.txt`).
- **Robustness: UNCLEAN (F1).** Checked:
  - back-pressure (the reviewer probe);
  - a fan-out in progress (ID5) and an engine held from reset (ID6);
  - a release and a press inside a burst (ID3);
  - the reset restart of identifySequenceID (ID6c);
  - feature-disabled behaviour (ID0 and the equivalence);
  - stale REARM expiries (the generation logic; S1).
- **Tests: UNCLEAN (F1).** Checked every new section (ID, ID0, NP, ST, RN, originator R, ucpu N6/N7) for independence of its expectations from the DUT: expectations are built from clause offsets and wire-counted sequence models. All 30 lane mutants were killed again. Three reviewer mutants were run (S1). RN and R carry anti-vacuity counters.
- **Docs: UNCLEAN (F1, F2).** Checked the 00 GAP-06/GAP-17 and REQ rows, 01 F01.5, 02, 03 §4/§5, 06 §2/§7, 08 F08.1/F08.4, 09 §8.3, the three guides, diagram 21, and both suite READMEs; `make check` rc 0.

## 5. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 open) | `KL_aecp_notify.sv:677-839`, `gen_ucode.py:936-956, 2062-2098`, `KL_aecp_engine.sv:1349-1390`, `notify_phases.hpp` ID/NP/ST/RN, reviewer stall probe | R420-1 | 5e806296b73d04ccf095ad00e081cb790fbbaf8d |
| RTL | UNCLEAN (F1 open) | `KL_aecp_notify.sv` (whole sequencer, registry arm sites, withdrawal), `KL_aecp_engine.sv` kind map and job acceptance `:2729-2810`, `protocol_processor_top.sv` ports/params/guard/tie-offs, `pp_pkg.sv:248-285`, `KL_pp_timer_service.sv` semantics, lint at 1, equivalence at 0, block OOC at 0 and 1 | R420-1 | 5e806296b73d04ccf095ad00e081cb790fbbaf8d |
| Robustness | UNCLEAN (F1 open) | reviewer mid-burst stall probe; ID3/ID5/ID6/ID0; REARM generations; reset path | R420-1 | 5e806296b73d04ccf095ad00e081cb790fbbaf8d |
| Tests | UNCLEAN (F1 open) | `tb/pp_top/notify_phases.hpp` (all sections), `tb/pp_top/notify_mutants.py`, `tb/originator/sim_main.cpp` R, `tb/ucpu/sim_main.cpp` N6/N7, 30/30 kill reproduction, 3 reviewer mutants, 33 suites rc 0 | R420-1 | 5e806296b73d04ccf095ad00e081cb790fbbaf8d |
| Docs | UNCLEAN (F1, F2 open) | `docs/00_MILAN_COMPLIANCE_REVIEW.md`, `docs/architecture/01,02,03,06,08,09`, `docs/guides/{integrator,operator,hdl-engineer}.md`, `hdl/README.md`, diagram 21, `tb/pp_top/README.md`, `tb/originator/README.md`, PR body | R420-1 | 5e806296b73d04ccf095ad00e081cb790fbbaf8d |

## 6. What I executed

All runs used pinned Verilator 5.050 with at most 8 parallel jobs, in the foreground unless noted.

| Command (on an exact-head extraction under scratch/) | rc | Result |
|---|---:|---|
| `python3 scripts/check_upc_map.py` | 0 | 58 constants and 82 entry points agree |
| every `tb/*/` suite with a Makefile (33), one `make` each | 0 each | 1,017,309 checks, 0 failing; pp_top 8,078 = 7,996 + 20 + 62; originator 107; ucpu 396. `tb/common` has no Makefile and is not a suite |
| `./scripts/lint_hdl.sh` | 0 | every module LINT OK |
| lint of the three changed modules at `EN_IDENTIFY_NOTIF_P=1` | 0 | 0 warnings |
| `make check` | 0 | mermaid, wavedrom, links, matrices, parameters 27 = 27 = 27 |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `python3 tb/pp_top/notify_mutants.py --output ... --jobs 4` | 0 | 30 of 30 KILLED; goldens PASS |
| reviewer driver over the same 30 mutants + 4 goldens | - | 30 KILLED, 4 PASS, no named check missing |
| `make -C tb/pp_top identify` | 0 | ID 62/0, ID0 3/0 |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected; golden and restored PASS. Past its 600 s foreground window the harness moved it to the background; it finished rc 0 and its receipt is complete |
| `python3 tb/pp_top/d3_mutants.py --only <first 28 of 83> --jobs 4` | 0 | 28 of 28 KILLED; goldens PASS. It also outgrew the foreground window, was moved to the background by the harness and finished rc 0. The other 55 D3 mutants were not re-run |
| yosys equivalence, `KL_aecp_notify` head@0 vs main, plus a negative control | 0 / 1 | proven (6,930 cells) / fails as it must (36 unproven) |
| yosys `synth_xilinx` block OOC, notify main / head@0 / head@1 | 0 | LUT 6,454 / 6,549 / 6,905; FF 1,721 / 1,721 / 1,785 |
| reviewer probe: mid-burst MAC stall (copy of the third build) | 0 | the F1 table |
| reviewer extra mutants (3) | - | all SURVIVED (S1) |

Not run, by this round's rules: the full parent, PP, gPTP, Yosys (`syn/yosys/run.sh`) and builder banks; the parent consumer gates; Docker/act; hardware. Also not re-run: the `adp_engine`, `srp_top` and `acmp_talker` campaigns. The diff does not touch those modules, and the manager's banks cover them.

## 7. Real limits and pending manager duties

- The Verilator wrapper named in the assignment (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I used a wrapper with the identical script hash under `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/`, which reports Verilator 5.050 (`receipts/00_tool_identity.txt`), behind a local shim that caps build parallelism (`scripts/verilator-cap*.sh`).
- The IEEE 1722.1-2021 and Milan v1.2 texts were not available to me. Conformance was judged against the clauses as quoted in the issues, the repository and the tests, and by internal consistency (the unsolicited SET_STREAM_INFO equals the solicited answer).
- I did not formally re-prove the engine at 0. It was judged from its complete 18-line diff plus the author's published summary.
- OOC figures are yosys only. A Vivado out-of-context figure at the parent is authoritative (manager duty).
- Hosted checks at the exact head, as queried: `docs-gates` success, `portability` success, `suites` still `in_progress` with no conclusion; combined status `pending` (`receipts/hosted_check_runs.txt`). Hosted/act acceptance is the manager's.
- Physical calibration NOT RUN; no hardware; simulation evidence only.
- Manager duties: the parent adoption (the two edits at dev `e4b771f9`), the parent consumer set, and the final current-dev candidate at the merge turn. The later composition with processor main `d5f73bac` (C2) is a separate delta review and was not judged here.
- Clone integrity after this round: HEAD `5e806296`, tree `ebe7b48f`; worktree and index clean; the index mode/blob/path digest equals HEAD's tree digest; the repository has no gitlinks and needs none (`receipts/clone_integrity.txt`). Every probe ran in extractions under `scratch/`, which is not published.
- In the published receipts the local home-directory prefix was replaced by `~`. Nothing else was edited.

R420-1 FINISHED
