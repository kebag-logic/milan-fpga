[R406] NEGATIVE - exact head 9185c491b56358d6bc15b5069b612bfaa95316f3

# R406-1: independent internal review of PR #136 (lane C3, ADP)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan
- **PR:** #136. It closes #40 and #41 and relates to #85.
- **Head:** `9185c491b56358d6bc15b5069b612bfaa95316f3`, tree `93ec21cf2788017b578a83cb6c1c376cca2eee30`. Five commits on base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`.
- **Assignment:** #40 comment 5888002660. Review start: PR #136 comment 5891050559.
- **Reviewer:** internal, in a cleared context and an isolated detached clone.
- **Simulator:** Verilator 5.050, the CI pin. Identity is in `receipts/00-tool-identity.txt`.

## Verdict

**NEGATIVE, on one MINOR finding (F-1).**

Everything else holds at this head:
- all acceptance items reviewed here, each checked against its issue's own list;
- the manager's three route questions (a) to (c);
- every processor suite and every entry point this lane added or touched.

F-1 is a test gap, not a defect. The new configuration-valid flop in `KL_aecp_engine` has a reset clause, and that clause alone decides what the ADPDU carries after a warm reset. No suite or campaign grades it. With the reset removed, the whole functional bank stays green.

My own probe shows the head RTL behaves correctly across a reset. The required outcome is a regression arm plus a mutation arm, about 30 lines of test code. No RTL change is needed.

## How the review was reconstructed

1. **Repository rules.** This repository has no AGENTS.md or CONTRIBUTING.md. I read `README.md` and `docs/README.md` (conventions, ID registries, single-source rules), and `.github/workflows/hdl.yml`.
2. **Frozen scope.**
   - The bodies of #40, #41 and #85.
   - The assignment (#40 comment 5888002660) and the lane notices on #41 and #85.
   - The PR body, and the manager's route ruling in the review brief.
3. **Authorities.**
   - Milan v1.2 §5.6.1, the §5.6.2 note, §5.6.3.5, Table 5.51, §5.6.4.5 and Table 5.54.
   - IEEE 1722.1-2021 §6.2.2.18 and §7.4.7/§7.4.8.
   - These are cited through the repository's architecture documents (04 §3, F04.2, F04.3, F04.6; 02 §2; 09 §3). The specification PDFs are not distributed, so I read no clause text directly (see Limits).
4. **Diff.** `git diff c951a9ff..9185c491`: 41 files, +1662/-36. I read all of it: RTL, workflow, docs, both testbenches, the driver and all 27 patch files.
5. **Public evidence**, read after my own pass over the diff:
   - `kebag-logic/milan-fpga@795bda4c:review-evidence/ppC3-r1`. PR-BODY.md equals the live PR body apart from one trailing newline. HANDOFF.md is the author's published handoff.
   - Manager comment 5891619124: donor full bank 9/9, parent consumer bank 16/16 at dev `79c36963`.
   - Hosted checks at the exact head.

**Prior public review findings on #136:** none existed before this round. The PR carried only the two review-start notices and the manager's bank comment. The other reviewer's round-1 verdict comment appeared during this round, and I did not read it before writing this verdict and ledger.

## Acceptance, item by item

### #40: ADPDU invariance across SET_CONFIGURATION (REQ-ADP-005)

| Item | Judgement | Evidence |
|---|---|---|
| 1. After a SUCCESS SET_CONFIGURATION, the next ENTITY_AVAILABLE is byte-exact to the previous one except available_index and current_configuration_index | MET | `tb/pp_top` AD2/AD3 (`AdpConfigPhase`, `tb/pp_top/sim_main.cpp:9798`). The image default is 1 and the SET goes to 0 and back, so the test separates the default, the overlay's reset value and a frozen index. `make adp-config` 34/34 at head. Under `cfg-frozen-at-top` (the pre-lane wiring) AD2 and AD4 fail (receipt 12). |
| 2. An `adp_engine` arm changes `current_cfg_i` between adverts and only bytes 64..65 move | MET | P11a/b (and c/d/e: tear-proofing and DEPARTING). The unit suite has 1367 checks, rc 0. |
| 3. Feed the engine from the dynamic overlay, or state a loopback duty | MET, preferred route | `protocol_processor_top.sv:1643`. The flag is `KL_aecp_engine.sv:1683-1694`. See route questions (a) to (c) below. |
| 4. Mutation record | MET | 8 cfg arms, all KILLED by the named check in my run (receipt 12). Counts equal the README table. |

**RTL defect fixed in the lane.** The builder read `current_cfg_i` live while writing wire bytes 64..65. The index is now sampled in `B_SAMPLE` (`bld_cfg_r`). The `cfg-read-live` arm reproduces the old read and fails only P11c, as claimed.

### #41: pre-enable quiescence over the full T-ADP-DELAY span (REQ-ADP-006)

| Item | Judgement | Evidence |
|---|---|---|
| 1. Unit test: enable low, link up and one bounce, more than 4000 ms modeled; no draw, no arm, no frame, DOWN | MET | P12, `tb/adp_engine/sim_main.cpp:618-642`: 4100 + 20 + 4100 ms, timer service live, PRNG seed proves the stimulus is live. |
| 2. pp_top holds more than 4 s with enable low and `q_adp` empty | MET, through "a new phase" | AD0: 4200 + 20 + 4200 ms, a sample every 100 ms. The added S3 pre-flush check sees a span shorter than T-ADP-DELAY. The README says so honestly, and AD0 is the check with teeth. |
| 3. Mutation record: the gate is removed from the DOWN exit | MET | `gate-enable-dropped`: 30 unit failures including all four P12 checks. `gate-enable-dropped-top`: 3 failures. I re-ran the full default pp_top under this mutant: exactly 3 of 7,766 fail, all AD, as claimed (receipt 23). |

### #85: the F04.2/F04.3 MTXW walk (items 1-3; item 4 stays open)

| Item | Judgement | Evidence |
|---|---|---|
| 1. Every F04.2 cell from an independent table, ending in a cell-count check | MET | The `ADV[9][5]` table is transcribed from Milan Table 5.51 and §5.6.3.5, not from RTL. It adds the §5.6.1 not-started column and both DELAY phases. The walk ends with `CHECK(adv_cells == 45)` (`sim_main.cpp:1559`), and the run prints N 12 / I 20 / S 6 / C 7. |
| 2. DOWN x {DISCOVER, GM_CHANGE, SHUTDOWN} inert; DELAY x LINK_DOWN cancels with no DEPARTING; DELAY x SHUTDOWN departs and resets the index | MET | Each cell grades state, draw requests, every timer operation with its deadline, the frame byte-exact, available_index, GM ticks, discovery events and RX frees (`walk_advertise_cell`, `sim_main.cpp:1322-1407`). Both DELAY phases are covered. |
| 3. Every F04.3 arc in the same walk; the named mutations turn red | MET | `DISC[11][3]` (33 cells) with `F043_ARCS` 8 of 8. The issue-named `walk-down-answers-discover` (16 failures) and `walk-delay-ignores-link-down` (4 failures) are KILLED, as are 15 further walk arms. |
| 4. available_index interop against a live controller | OPEN, as scoped | The README limit is restated as open with its reason. The PR says "Relates to #85". |

### The manager's route questions

- **(a) Holds.** `protocol_processor_top` parameter and port declarations are identical to base once comments are stripped (245 lines, receipt 40).
  - `KL_adp_engine` ports are identical.
  - `KL_aecp_engine` gains exactly one output, `dyn_cur_config_v_o`, and only `protocol_processor_top` instantiates it under `hdl/`. The parent at dev `79c36963` has no instantiation of it (receipt 41).
  - None of the modules the parent instantiates by name is touched.
- **(b) Holds.** The new meaning of `current_cfg_i` (the image-default fallback) is stated correctly in four places: the PR body's parent-visible list item 2, `docs/guides/integrator.md:251-257` (§6), `02_interfaces.md:91-97` (§2 rule 4), and the 04 §3 field row. It is harmless to the parent (receipt 41):
  - The parent drives `current_cfg_i` from `ADP_IDX0[15:0]`, which resets to 0 (`milan_csr.sv:1586,2819` → `milan_datapath.sv:7602`).
  - Its builder test pins `configurations_count == 1` (`sw/builder/test_builder.py:25328`).
  - So the only legal SET is 0, and the wire is unchanged while ADP_IDX0 is 0.
- **(c) Holds on the head RTL.**
  - **After a SUCCESS SET:** AD2 and AD3 check SET, GET, the ENTITY descriptor and the next ADPDU in one arm.
  - **After a rejected SET:** the µprogram's refusal arms (`gen_ucode.py:1656-1685` (the only `WRITE_ST` of the row is at :1674), CHECK_LOCK and CHECK_ARG before `WRITE_ST`, and the dispatch-level STREAM_IS_RUNNING) never reach the store write. The flag decode (`KL_aecp_engine.sv:1683-1692`) is term-for-term the store's `take_wr_w && sel==SEL_CFG` (`KL_aecp_dyn_state.sv:252,294-295`) on the same bus. So a refusal moves neither the flag nor the overlay.
  - **Across a reset:** both the flag and `cfg_r` clear on `rst_n`, and the ADPDU returns to `current_cfg_i`. GET returns the image default; no dynamic-state restore exists at this head.
  - A reviewer probe confirms all three on the wire (receipt 20; probe RP1/RP2/RP3, 51/51 at head):
    - RP1: BAD_ARGUMENTS on a written row.
    - RP2: SET(0), reset, then the first ADPDU and GET both read the image default 1.
    - RP3: BAD_ARGUMENTS on the unset row.
  - The probe has teeth: it fails under a reviewer mutant that drops the flag's reset (2 failures, receipt 21-probe-pm-flag-survives-reset) and under one that removes SET_CONFIGURATION's range check (6 failures, receipt 21-probe-pm-scfg-no-range-check).
  - The in-repo bank grades the reset leg nowhere. That is F-1.

### Entry points and gates at the head (reviewer runs, 8 parallel jobs at most)

| Command | rc | Result | Receipt |
|---|---:|---|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,016,684 checks, 0 failing (adp_engine 1367, pp_top 7786). Matches the PR. | 02 |
| `make -C tb/adp_engine mutants` (new; the CI step runs this exact command) | 0 | 2 controls pass, 27/27 arms KILLED by their named checks, counts equal the README | 12 (also 10, 11 split runs) |
| driver negative control (a neutral patch added in a scratch copy) | 1 | UNPROVEN, as required: the driver does not credit an arm that fails nothing | 13 |
| `make -C tb/pp_top adp-config` (new) | 0 | AD 34/34 | 20 (with the probe) |
| `make -C tb/pp_top gsi-internal` / `name-writes` (dispatch in `main()` changed) | 0 / 0 | 6182 / 85 checks | 50 |
| `tb/pp_top/gsi_mutants.py` | 0 | 20 detected, golden and restored pass | 52 |
| `tb/pp_top/name_wr_mutant.py` | 0 | decode killed, golden and restored pass | 51 |
| `tb/desc_mem_guard/mutate.py` | 0 | hold-deleted detected | 54 |
| `./scripts/lint_hdl.sh` | 0 | 40 modules | 30 |
| `make check` / `gen_matrix.py --check` | 0 / 0 | all docs gates; 92 rows, 0 untested | 32, 31 |
| `git diff --check c951a9ff..9185c491` | 0 | | 33 |
| parent `scripts/measure_test_evidence.py --check`, scratch parent at dev `79c36963` | 0 / 0 | base gitlink: 75 <= 77. Head gitlink: **74 <= 77**; `tb/adp_engine` is credited for its `mutants` driver and 0 unexplained readers. The PR's ratchet claim holds. | 42, 43 |
| Hosted `hdl` run 36571814541 (push) at the exact head | success | docs-gates, portability, suites. The ADP mutation campaign step **executed** from 13:41:16Z to 13:48:07Z. The only skipped step is the Verilator build (cache hit). | 60 |

## Findings

### F-1: MINOR. The new configuration-valid flop's reset is graded by no test or mutation arm

- **Lenses:** Tests, Robustness.
- **Where:**
  - `hdl/aecp/KL_aecp_engine.sv:1683-1692`, `dyn_cfg_valid`, whose reset branch is line 1685;
  - consumed at `hdl/top/protocol_processor_top.sv:1643`;
  - the test gap is `tb/pp_top/sim_main.cpp` `AdpConfigPhase::run()` (:9944-9975) and `tb/adp_engine/mutants.py` `MUTANTS`.
- **Authority:**
  - REQ-ADP-005 with IEEE 1722.1 §6.2.2.18 and §7.4.8.2: the ADPDU's current_configuration_index is the current configuration, the value GET_CONFIGURATION answers.
  - The flop's own contract (`KL_aecp_engine.sv:1675-1680`: "only reset clears it"), and the PR's "exactly the store's flag".
  - The manager's brief, question (c), "across a reset".
- **Evidence:**
  - With the flop's reset removed (`probes/probe_mutants.py pm-flag-survives-reset`), the full default pp_top run is 7786/7786 PASS (receipt 22). pp_top is the only functional suite that elaborates `KL_aecp_engine`; `tb/timer_map` only elaborates the top's shapes.
  - The ADP campaign has no reset arm, so its 27 arms pass or kill exactly as at head.
  - The same mutant fails the reviewer probe's RP2/RP3 (receipt 21-probe-pm-flag-survives-reset). After SET(0) and a reset, the ADPDU carries the overlay's reset value 0 while GET answers the image default 1.
  - The write side of the same flag is well armed: `cfg-valid-not-sticky`, `cfg-valid-any-selector` and `cfg-nonzero-for-valid`. Only the clearing path is blind.
- **Impact:**
  - No defect at this head; the probe shows the head RTL correct.
  - A later edit that loses the reset would ship silently. After any warm reset that follows a SET_CONFIGURATION, the ADPDU would disagree with GET_CONFIGURATION and the ENTITY descriptor. That is exactly the invariance #40 exists to grade.
  - The risk grows at the merge turn: PR #132 adds a restore writer to the same store, and the author's own merge-train note says the flag's set and clear paths must track the store's.
- **Required outcome:**
  1. A pp_top arm, for example AD5, in `AdpConfigPhase`. It does a SUCCESS SET to a non-default index, pulses `rst_n` and re-boots the phase's processor. It then checks that the first ENTITY_AVAILABLE and GET_CONFIGURATION both carry the image default.
     - Optionally, the arm also covers a refused SET on the unset row keeping the ADPDU at `current_cfg_i`.
  2. A campaign arm in `tb/adp_engine/mutants.py`, with a patch under `mutations/`, that removes the flop's reset and is KILLED by that check.
  3. The README mutation table and the PR's mutation table gain the row.
- **Verification:**
  - `make -C tb/pp_top adp-config` passes at the new head, and `make -C tb/adp_engine mutants` reports 28/28 KILLED with the new arm named.
  - Reviewers can reproduce the gap at this head with `probes/probe_mutants.py <scratch tree> pm-flag-survives-reset` and a full `make -C tb/pp_top`, which today is green.

### SUGGESTIONS (they do not affect the verdict)

- **S-1 (Conformance, Docs): AEM_CONFIGURATION_INDEX_VALID.** The PR discloses that IEEE 1722.1-2021 §6.2.2.18 transmits current_configuration_index as 0 unless AEM_CONFIGURATION_INDEX_VALID is set. The advertised capabilities `ADP_ENTITY_CAPS_C = 0x0000C588` (`hdl/adp/pp_adp_pkg.sv:53`) leave it clear.
  - The field row at `docs/architecture/04_adp_engine.md:80` now cites §6.2.2.18 for carrying the current configuration without that condition.
  - The frozen #40 acceptance requires the index to move, and the parent's single-configuration image keeps it 0 on the parent's wire. So this is a manager or spec-owner decision, not a lane defect.
  - Suggestion: record the decision in 04 (the F04.6 note, or a Δ entry if Milan's §5.6.2 note is read as overriding), so the citation stays accurate.
- **S-2 (Docs): scope "from then on" to the next reset.** `docs/guides/integrator.md:255` says the processor "no longer reads `current_cfg_i`" after a SET. That is true until the next reset, which clears the overlay's flag and falls back to `current_cfg_i` again (and, after #132, until a restore). Saying so in §6 and in 02 §2 rule 4 would prevent an integrator from treating `current_cfg_i` as dead after the first SET.
- **S-3 (Tests): make the cell counts non-tautological.** `CHECK(adv_cells == 45)` and `CHECK(disc_cells == 33)` count iterations of loops whose bounds are the table dimensions, so they cannot fail. That meets the acceptance, which asked for acmp_listener's shape. A count of cells actually graded (N/I/S cells applied plus C preconditions checked), compared with the per-class totals the walk already prints, would give the count teeth.

## Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Acceptance of #40 1-4, #41 1-3 and #85 1-3 against the issue bodies. Route questions (a) to (c), including the parent at dev `79c36963`. The refusal and reset semantics of SET_CONFIGURATION (`gen_ucode.py:1643-1700`, `KL_aecp_dyn_state.sv`). The Table 5.51/5.54 transcriptions against F04.2/F04.3 and the RTL arcs. S-1 is raised as a suggestion. Receipts 12, 20, 21, 40, 41. | R406-1 | 9185c491b56358d6bc15b5069b612bfaa95316f3 |
| RTL | CLEAN | `KL_adp_engine.sv` builder sampling (`bld_cfg_r`, B_SAMPLE → write). `KL_aecp_engine.sv` flag decode against the store's `take_wr_w`, which is term-for-term equal, same edge as `cfg_r`, and has no one-cycle window. The top mux (`protocol_processor_top.sv:1643`). Port lists (receipt 40), lint 40/40 (receipt 30). Hosted suites success. | R406-1 | 9185c491b56358d6bc15b5069b612bfaa95316f3 |
| Robustness | UNCLEAN (F-1) | Mid-build index change (P11c). Rejected SET and warm reset (reviewer probe, receipts 20 and 21). Pre-enable link bounce (P12/AD0). Stray-expiry cells. Driver kill criterion and negative control (receipt 13). The reset leg of the new flag is ungraded (receipt 22). | R406-1 | 9185c491b56358d6bc15b5069b612bfaa95316f3 |
| Tests | UNCLEAN (F-1) | All new test code (P11, P12, P13, AD0-AD4, S3). The 27 patches and the driver. The full campaign at head (receipt 12). The full pp_top run under `gate-enable-dropped` (receipt 23) and under the reviewer reset mutant (receipt 22). run_suites (receipt 02). Other pp_top entry points (receipts 50-52). The ratchet at base and head (receipts 42, 43). S-3 is raised as a suggestion. | R406-1 | 9185c491b56358d6bc15b5069b612bfaa95316f3 |
| Docs | CLEAN | `integrator.md` §6, `02_interfaces.md` §2 rule 4, `04_adp_engine.md` §3 row, `09_verification.md` (the MTXW paragraph and the current_configuration row). `tb/adp_engine/README.md` (tables, mutation record against receipt 12, the restated #85 item 4 limit). `tb/pp_top/README.md` (S3, AD). The PR body's parent-visible list against receipts 40, 41 and 43. `make check` (receipt 32). S-1 and S-2 are raised as suggestions. | R406-1 | 9185c491b56358d6bc15b5069b612bfaa95316f3 |

## Real limits

- **Simulator path.** The brief's simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used a copy of the byte-identical 319-byte wrapper from a sibling manager directory. It reports `Verilator 5.050 2026-07-01 rev v5.050`, the CI pin; the wrapper and binary hashes are in receipt 00. The host default is 5.052 and was not used.
- **Specification text.** The specification PDFs are not available to this review. The Table 5.51 and 5.54 transcriptions and the §6.2.2.18 reading were checked against the repository's own architecture tables (F04.2, F04.3, 04 §3) and the RTL, not against the printed clauses.
- **Not run by this reviewer:**
  - `syn/yosys/run.sh` (a disallowed bank).
  - The donor full bank and the parent consumer bank (manager duties; the manager reports PASS 9/9 and 16/16 in comment 5891619124).
  - `make -C tb/srp_top mutants` and `make -C tb/nvm_port figures`; the hosted suites job at the exact head executed both with success.
  - `tb/acmp_talker/retry_mutants.py`.
  - `tb/srp_admission/mutants.py` was stopped by my 250 s cap after 8 of its arms passed (receipt 53, partial and not a result).
  - These entry points cover modules this lane does not touch.
- **Session limit.** `gsi_mutants.py` overran the session's 600 s foreground limit and was moved off the foreground by the session. I kept polling it in the foreground until it wrote its exit line, rc 0 (receipt 52).
- **Parent read-only.** The parent was inspected read-only in a disposable blobless clone, with the processor gitlink moved to this head in that scratch index only. Only `measure_test_evidence.py --check` was run there.
- **Hardware.** No hardware was used, and physical calibration was NOT RUN. Field or hardware skips are not hardware proof.
- **Merge-turn composition not judged.** Main is now at `d352bbaa` (PR #132). Composing this branch with it, including the valid-flag decode against #132's restore writer, is not judged here.
- **Clone integrity.** The review clone was never modified; every run used a byte-verified `git archive` export (receipt 98). Before and after this review the clone showed:
  - head `9185c491`, tree `93ec21cf`;
  - index-stage hash `b7308a65…`;
  - 0 status entries (ignored files included);
  - worktree equal to HEAD, and no gitlinks in this repository (receipts 01 and 99).

## Pending manager duties

1. Publish this report. Route F-1 to the executor, then run a delta round at the fixed head.
2. Decide S-1: the AEM_CONFIGURATION_INDEX_VALID capability, or a recorded Milan-over-IEEE reading.
3. At the merge turn:
   - merge main (`d352bbaa`, PR #132) into the branch;
   - keep the valid-flag decode on the bus the store actually takes, including #132's restore writer;
   - build the final current-dev candidate from base `c951a9ff` and live dev `79c36963`;
   - queue the delta review.
4. Own hosted and act acceptance. The hosted run at this head is success; act was not run by this reviewer.
5. #85 item 4, the live-controller available_index interop, goes to a bench lane. #85 stays open.

## Packet contents

- **Scripts** (portable, and they take a scratch tree as an argument):
  - `run-suite.sh`
  - `probes/apply_probe_ad.py`: inserts RP1-RP3 into a scratch `tb/pp_top/sim_main.cpp`.
  - `probes/probe_mutants.py`: `pm-flag-survives-reset`, `pm-scfg-no-range-check`.
  - `probes/port_list.py`
- **Receipts:** `receipts/*.txt`. Home-directory paths inside the simulator root are redacted to `<pinned-tool-root>`.
- **Manifest:** `MANIFEST.sha256`.

R406-1 FINISHED
