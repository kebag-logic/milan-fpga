[R406] POSITIVE - exact head 20ec92b7b190d03c46e40be89d236bc9a0702a59

# R406-2: internal independent review of PR #136 (lane C3, ADP), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #40, PR #136.
- Exact head `20ec92b7b190d03c46e40be89d236bc9a0702a59`, tree `a3d4eb5a6e6b8bf770b683d9ab5bd71a916dab6d`. Source base `main` `b2db3a970cedbbff2f8ba813acb96122c442bc58`. Round-1 head `9185c491`.
- Review start: PR #136 comment 5903328034. Round-2 assignment: #40 comment 5893098818.
- Clone: a detached clone at the exact head. After every run, its tracked bytes, modes and index equal the head (receipt 99).

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. All five lenses are CLEAN.

- **R406-1 F-1 (MINOR) is RESOLVED.**
  - AD7 grades the flag's reset.
  - `cfg-valid-no-reset` is KILLED by AD7, with 5 failures.
  - Both mutation tables carry the row.
- **The merge is correct.** The configuration-valid flag is, by construction, the store's own `cfg_v_r`: the same decode of the same post-selection bus into one flop, under the same reset. I checked this three ways:
  - by reading the two decodes side by side;
  - by an every-clock comparator over the whole default pp_top run: 0 split clocks, while the store's flag rose 22 times and fell 21 times;
  - by a positive control of that comparator under a planted mutant: 1,180,811 split clocks.
- **Refused SETs cannot set the flag.** A refused SET_CONFIGURATION never issues a `WRITE_ST`. A reviewer probe grades refused SETs on an unset and on a set row.

Two new SUGGESTIONs and four carried SUGGESTIONs are listed below. None affects the verdict.

## How the review was reconstructed

1. **Contributor rules.** The processor repository has no `AGENTS.md` and no `CONTRIBUTING.md`. The contributor rules are `README.md` ("Building and checking") and `docs/README.md` (single-source rules, citation rules, and the editing workflow: `make check` before commit).
2. **Scope.** Issue #40's body (acceptance 1-4) and the manager comments:
   - 5888002660, the lane assignment: acceptance 3 via the overlay with no port change, STOP before any port or parent-visible change;
   - 5893098818, round 2: merge `b2db3a97` by merge commit, the flag on the post-selection bus (`dyn_didx_w`, `d3_bus_w`), a restored-configuration arm, R406-1 F-1 items 1-3, and the parent-visible list re-read.
3. **Authorities.**
   - IEEE 1722.1-2021 §6.2.2.18: the ADPDU carries the current configuration.
   - IEEE 1722.1-2021 §7.4.7.1: a refused SET echoes the current value.
   - IEEE 1722.1-2021 §7.4.8.2: GET_CONFIGURATION answers the current configuration.
   - Milan v1.2 §5.6.2 note (REQ-ADP-005) and §5.4.2.5, as cited in the RTL and microcode.
   - The interface documents 02 §2 rule 4, 04 §3, 07 §5.3 (the D3 restore) and `docs/guides/integrator.md` §6.
4. **The diff and the merge.**
   - `git diff b2db3a97..20ec92b7`: 45 files, of which 9 are RTL, CI or docs.
   - I recomputed the merge with `git merge-tree --write-tree 9185c491 b2db3a97` and compared it with the merge commit `cae0988`. Only the two conflicted files differ, and the difference is the conflict resolution alone (receipt 41).
5. **Public evidence.**
   - The evidence tree `review-evidence/ppC3-r1` at `c2424a3`: the round-2 author packet (`HANDOFF.md`, `PR-BODY.md`, the combined parent adaptation patch).
   - The manager comments on #40 and #136.
   - The hosted check runs at the exact head.
6. **Prior findings.** The R406-1 and R407-1 findings were read only after my own pass over the diff and my runs. They are resolved or retained below.

## Round-2 items, judged

### (1) The merge resolution

**The resolution, `hdl/aecp/KL_aecp_engine.sv`.**
- Main's `u_dyn_didx_w` and `dyn_didx_w` replace the branch's `dyn_ix_w` (`:1782-1785`). The store's `desc_index_i` takes `dyn_didx_w` (`:1839`).
- The flag block `dyn_cfg_valid` (`:1803-1812`) now decodes `st_req_w && dyn_sel_w && st_we_w && region == RGN_DYN_C && selector == 0 && dyn_didx_w == 0`. `st_*_w` is the post-selection bus (`:1554-1559`).
- The flag resets on `store_rst_n_w = rst_n && !d3_rb_rst_w` (`:1545`, `:1804`).

**The store's own flag, `KL_aecp_dyn_state.sv`.**
- It sets `cfg_v_r` on `take_wr_w = st_req_i && st_we_i && region == RGN_DYN_C && in_range_w` (`:266`), with `SEL_CFG_C = 0` (`:145`) and `count_w = 1` (`:206`), so the row must be 0.
- `st_req_i` is `st_req_w && dyn_sel_w`, `desc_index_i` is `dyn_didx_w`, and `.rst_n` is `store_rst_n_w` (engine `:1824-1839`).
- Both resets are synchronous. The two expressions are term for term the same, on the same clock edge.

**Case by case:**

| Case | Outcome |
|---|---|
| Hard reset | Both clear. |
| D3 roll-back | Both clear. `rb_rst_o = (ws_r == W_RB)`, `KL_aecp_nvm_writer.sv:1106`. W_RB is reachable only in pass 1, before `done_r`: `:662-670` and `:785-795`. |
| Restore of record 0x00 | Both set. W_APPLY drives `sb_we_o` only while `!done_r` (`:1084`), address `{RGN_DYN_C, selector 0}` (`:847`) and `sb_didx_o = ridx_w = 0` (`:1087`), with `bus_o` selecting the writer (`:1078`). |
| µCPU SET | Both set. `u_dyn_didx_w = scfg_r ? 0 : desc_ix_r` (`:1784`). |
| Refused SET | Neither moves. `gen_ucode.py:1660-1747`: CHECK_LOCK, CHECK_ARG against RGN_NCFG, and the engine's STREAM_IS_RUNNING dispatch all branch before the only `WRITE_ST` (`:1678`). |

ADP is enabled only after the restore (`protocol_processor_top.sv:1709`, `adp_enable_w = entity_enable_i && restore_done_o`). So the first advert is built after any restore write or roll-back.

**`tb/pp_top/sim_main.cpp` `main()`.**
- Main's `--d3-only` and `--dr3a` sit beside the branch's `--adp-only`, and each single-section flag runs exactly its section.
- `Vpp_top_sim --dr3a` rc 0 (receipt 50), and `--d3-only` is exercised by all 83 D3 arms and their goldens (receipt 30).

**Auto-merged files.** They are byte-equal to the automatic merge (receipt 41). The one ADP engine change, a port comment, comes from main.

### (2) The restore path: AD5 and AD6

- **Test structure.** `reboot()` is a power cycle through both restore walks. `graded_step()` compares, in every clock from the reset to the first advert, the published flag (new wrap tap `dbg_adp_cfg_v_o = u_dut.aecp_cur_cfg_v_w`) with the store's (`dbg_dyn_cfg_v_o = u_dyn.cfg_v_r`). `first_advert_agrees()` grades the first ENTITY_AVAILABLE byte-exact, then GET_CONFIGURATION and ENTITY.current_configuration.
- **AD5 premises:** the device holds `d3_record(0x00, 0, 2)`, and after the restore the row is valid with configuration 0.
- **AD6 premises:** configuration applied, then cause 5, rolled back, the flag clear.
- Both pass at the head: AD 55/0 in the full default run (receipt 12).
- **Mutants.**
  - `cfg-valid-ucpu-bus` is KILLED: 3 failures, AD5 twice and AD6.
  - `cfg-valid-hard-reset` is KILLED: 2 failures, AD6 twice.
  - I ran both myself (receipt 20).
- **The comparator itself has teeth.** It is live beyond section AD: with `cfg-valid-hard-reset` planted, D3 alone stays 133/0 while the flag splits for 1,180,811 clocks (receipt 22). That is why AD6 and not D3 is the arm that kills it.

### (3) R406-1 F-1

- **AD7.** SET_CONFIGURATION(0) SUCCESS. Premise: GET reads 0, the flag is set, the device is idle. Then `reboot(erase=true)`. Premise: `restore_blank_o`, the row unset. Then the first advert byte-exact at the image default 1, GET 1, ENTITY 1, and 0 split clocks.
- **Why the erased device is right.** A kept device would restore record 0x00 (AD5) and hide the flop's reset.
- **The mutants.**
  - `cfg-valid-no-reset` is KILLED with 5 failures: AD7 twice, AD6 twice, AD5 once.
  - `cfg-valid-hard-reset` and `cfg-valid-ucpu-bus` are KILLED as above.
  - The four regenerated patches plant the same defects as in round 1. The diffs move only their context, and each is KILLED: `cfg-valid-any-selector` 1, `cfg-valid-not-sticky` 7, `cfg-overlay-only` 4, `cfg-nonzero-for-valid` 3.
- **The full campaign:** 30 of 30 KILLED by the named check, and every count equals `tb/adp_engine/README.md` (receipt 21, 0 mismatches). The PR's Round 2 table agrees.

### (4) Composition at the merged head

- **Suites.** All 33 `tb/` suites pass: 1,017,162 checks, 0 failing, gated by `check_upc_map.py` (receipt 11). pp_top is 7,944 = 7,924 (default build) + 20 (fixture build).
- **#132's campaign.** D3 83 of 83 KILLED, with the three goldens (pp_top, acmp_nvm, rx_validator) PASS (receipt 30).
- **srp_top.** 11 controls PASS, all 78 entries (73 labels) KILLED, assertion coverage 65/65 (receipt 31).
- **The other campaigns and entry points:**
  - GSI: golden, 20 variants detected by their named checks, restored.
  - Name-write: decode killed, golden and restored pass.
  - Retry: 62 killed, 7 equivalence and 1 performance control.
  - Admission: 12 of 12.
  - `desc_mem_guard/mutate.py`: hold-deleted mutant detected.
  - `make -C tb/desc_mem_guard baseline`: rc 2 by design, 17 PASS 1 FAIL, `third locate late_beats_never_served`, wrong bytes `00060000deadbeef cafef00d01234567` as its README records.
  - Receipts 32-36.
- **Static gates.** `lint_hdl.sh` rc 0 (41 modules), `make check` rc 0, `gen_matrix.py --check` rc 0 (94 rows, 0 untested), and `git diff --check` over `b2db3a97..HEAD` and `c951a9ff..HEAD` rc 0 (receipt 50).
- **The gate mutant's record.** The full default pp_top run under `gate-enable-dropped` fails exactly AD0 twice, AD1b and D3R14. That is 4 failures of the default build's 7,924, as `b27e038` and the README state (receipt 23).
- **Hosted checks at the exact head, read only.** Two runs: push 36663287500 and pull_request 36663286949.
  - `docs-gates`, `portability` and `suites` succeed in both. `suites` executed "ADP mutation campaign" and every other test step.
  - Only "Build Verilator" was skipped, a cache hit and not a test (receipt 60).

### (5) The PR body's Round 2 section and the parent-visible list

- **Port lists.** The comment-stripped module headers against `main` `b2db3a97` are identical for `protocol_processor_top`, `KL_aecp_dyn_state`, `KL_acmp_nvm_shadow`, `KL_pp_nvm_port`, `KL_pp_nvm_mgr_arb`, `KL_aecp_nvm_writer` and `KL_adp_engine`. `KL_aecp_engine` gains only `output logic dyn_cur_config_v_o` (receipt 40).
- **The parent.** A read-only shallow fetch of the parent at dev `ec0cc0c1` shows no instantiation of `KL_aecp_engine` (receipt 42). `tests/steps/aecp_engine_steps.py` parses the engine's `OP_*` constants only, which this lane does not touch.
- **The list's content.**
  - The list names what the merge brings: #132's consolidated list, #133's section 4, and #133's composed-head note.
  - It states that this lane adds no parent edit.
  - Its `current_cfg_i` statement matches the RTL: the image default while the row is unset, from reset and after a roll-back.
- **The counts in the Round 2 validation tables** match my runs: suites, ADP campaign, D3, srp_top, GSI, name-write, retry, admission and desc_mem_guard.

## Five lenses

- **Conformance, CLEAN.**
  - REQ-ADP-005 with IEEE §6.2.2.18 and §7.4.8.2: the ADPDU index equals GET_CONFIGURATION and ENTITY.current_configuration in every graded state. Those states are the unset row, a µCPU SET, a restore, a roll-back, a reset, and my refused SETs on both rows.
  - Refusal echoes follow §7.4.7.1: the probe's PR1 echoes 1 and PR2 echoes 0.
  - The AEM_CONFIGURATION_INDEX_VALID question stays with the manager (carried S-1).
- **RTL, CLEAN.**
  - The merge resolution matches the store term for term. The reset domain is shared, and there is no new port on any parent-instantiated module.
  - The writer can touch the row only before `done_r`, and ADP waits for `restore_done_o`.
  - Lint is zero-tolerance clean.
- **Robustness, CLEAN.**
  - Every-clock equality holds across the whole default run: 0 splits in 22 rises and 21 falls, spanning W18 SETs, D3 restores and roll-backs, resets, and the fixture build.
  - Refused SETs on an unset and on a set row move neither flag.
  - The index is sampled at build (round 1's P11c holds).
- **Tests, CLEAN.**
  - AD5, AD6 and AD7 have explicit premises, and the flag comparator has teeth.
  - 30/30 ADP arms are KILLED with README-exact counts. Every #132 and C1 campaign passes at the merged head.
  - SUGGESTION S-1 below asks to pin the refused-SET leg.
- **Docs, CLEAN.**
  - `integrator.md` §6, 02 §2 rule 4, 04 §3, 09 §8.1, `protocol_processor_top.sv` (port and selection comments), the `KL_aecp_engine` port and block comments, `tb/pp_top/README.md` AD, `tb/adp_engine/README.md`, and the PR Round 2 section are all consistent with the RTL and the measurements.
  - `make check` passes.

## Findings

No open BLOCKER, MAJOR or MINOR finding.

### S-1: SUGGESTION. Pin the refused-SET leg in section AD

- **Lenses:** Tests, Conformance.
- **Where:** `tb/pp_top/sim_main.cpp` `AdpConfigPhase::run()` (`:10285-10319`).
- **Authority:** IEEE 1722.1-2021 §7.4.7.1 (a refusal echoes the current value and changes nothing), REQ-ADP-005, and the round-2 brief's "a refused SET".
- **Evidence:**
  - The head is correct. The microcode refuses before its only `WRITE_ST` (`gen_ucode.py:1660-1747`).
  - My probe (`probes/apply_probes.py --refused`) adds PR1 and PR2 to section AD, and both pass (receipt 22, AD 64/0):
    - PR1: SET(5) on the unset row is BAD_ARGUMENTS echoing 1, both flags stay clear, GET reads 1, and the next advert carries 1.
    - PR2: after a SUCCESS SET(0), SET(9) is BAD_ARGUMENTS echoing 0, both flags stay set, GET reads 0, and the next advert carries 0.
  - The suite itself grades only SUCCESS SETs, restores, roll-backs and resets. R407-1 S2's refused-SET leg is still not taken.
- **Impact:** none today. A later µprogram change that writes before its range or lock check would split the ADPDU from the echo without a red check.
- **Suggested outcome:** adopt PR1 and PR2, or equivalents, in AD, with a campaign arm that moves the `WRITE_ST` ahead of `CHECK_ARG`.
- **Verification:** `make -C tb/pp_top adp-config` green, and the new arm KILLED by PR1 or PR2.

### S-2: SUGGESTION. Default the mutation logs to a private directory

- **Lenses:** Robustness, Tests.
- **Where:**
  - `tb/adp_engine/Makefile:4`, `MUTANT_OUTPUT ?= /tmp/adp-mutants`, new in this lane;
  - the same pattern pre-exists at `tb/srp_top/Makefile:4`, default `/tmp/srp-leaveall-mutants`.
- **Evidence:** a fixed shared `/tmp` path is overwritten by any concurrent or later run on the same host. On this host, a run of the srp_top target with the default path overwrote 57 logs of an earlier run (receipt 98).
- **Impact:** evidence loss or cross-contamination between runs. The verdicts themselves are unaffected, because the drivers build in private temporary trees.
- **Suggested outcome:** default `MUTANT_OUTPUT` to a per-run directory, for example under the suite's `obj_dir` or via `mktemp -d`, and print it.
- **Verification:** two concurrent `make mutants` runs keep separate logs.

### Prior public findings, resolved or retained at this head

| Finding | Status at `20ec92b7` | Evidence |
|---|---|---|
| R406-1 F-1 (MINOR, Tests and Robustness): the flag's reset is ungraded | **RESOLVED** | AD7, plus `cfg-valid-no-reset` KILLED with AD7 named (5 failures). README and PR tables carry it. Receipts 12, 20 and 21 |
| R406-1 S-1 (SUGGESTION): AEM_CONFIGURATION_INDEX_VALID | RETAINED, manager decision | PR "Round 2: what remains". `ADP_ENTITY_CAPS_C` is unchanged |
| R406-1 S-2 (SUGGESTION): scope "no longer reads `current_cfg_i`" to reset | **RESOLVED** | `integrator.md:254-263`, 02 §2 rule 4, 04 §3, and the top's port comment name the reset and the roll-back |
| R406-1 S-3 (SUGGESTION): non-tautological cell counts | RETAINED, not taken | The unit walk is unchanged since round 1 |
| R407-1 S1 (SUGGESTION): F04.3 "domain mismatch, index > last" row | RETAINED, not taken | The unit walk is unchanged since round 1 |
| R407-1 S2 (SUGGESTION): refused-SET and reset legs in AD | Reset leg **RESOLVED** (AD5 to AD7). Refused-SET leg RETAINED as S-1 above | Receipt 22 |
| R407-1 S3 (SUGGESTION): "until reset", and a blank line in 09 | "Until reset" **RESOLVED**. The blank line is RETAINED: `09_verification.md:142-143` still runs the MTXW paragraph into the next one, which is cosmetic | `make check` passes |
| R407-1 O1 (observation): AEM_CONFIGURATION_INDEX_VALID | RETAINED, the same decision as R406-1 S-1 | |

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #40 acceptance 1-4 and the round-2 brief items 1-3. IEEE §6.2.2.18, §7.4.7.1 and §7.4.8.2, and the Milan §5.6.2 note. `gen_ucode.py:1647-1754` (SET/GET refusal and echo). Every flag case: reset, roll-back, restore, µCPU SET, refused SET. Receipts 12, 20 and 22 | R406-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |
| RTL | CLEAN | `KL_aecp_engine.sv:645-654`, `:1522-1559`, `:1782-1853`. `KL_aecp_dyn_state.sv:145-330`. `KL_aecp_nvm_writer.sv:600-850`, `:1078-1106`. `protocol_processor_top.sv:208-216`, `:1705-1753`. `KL_adp_engine.sv` (the merge delta). The merge `cae0988` against a recomputed merge-tree. Port lists. Lint. Receipts 40, 41 and 50 | R406-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |
| Robustness | CLEAN | The every-clock flag comparator over the full default run and its mutant control. Refused SETs on both rows. The roll-back and reset paths. The ADP enable gate on `restore_done_o`. The gate mutant's full run. Receipts 22 and 23. S-2 is a SUGGESTION | R406-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |
| Tests | CLEAN | `tb/pp_top/sim_main.cpp` section AD (AD0-AD7, `reboot`, `graded_step`, `first_advert_agrees`), the `main()` dispatch, `pp_top_wrap.sv` taps. `tb/adp_engine/mutants.py` and all 30 patches. All 33 suites. The ADP 30/30, D3 83/83, srp_top 78+11+coverage, GSI, name-write, retry, admission and desc_mem_guard runs. The hosted jobs. Receipts 11-36 and 60. S-1 is a SUGGESTION | R406-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |
| Docs | CLEAN | `integrator.md` §6. `02_interfaces.md` §2 rule 4. `04_adp_engine.md` §3. `09_verification.md` §8.1 and the MTXW paragraph. `tb/pp_top/README.md` AD. `tb/adp_engine/README.md` (counts checked mechanically, receipt 21). The top's and the engine's comments. The PR body's Round 2 section and parent-visible list. The round-2 author packet. `make check` | R406-2 | 20ec92b7b190d03c46e40be89d236bc9a0702a59 |

## Real limits

- **Verilator path.** The assigned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host.
  - I used the pinned wrapper `$VALIDATION_STORAGE/ppC3-manager-20ec92b7/pinned-tool-bin/verilator`. Its identity is verified as Verilator 5.050 rev v5.050, with the wrapper's sha256 recorded (receipt 00).
  - It ran through a reviewer wrapper that caps the suites' `-j 0` (2 per build under the 4-job D3 driver, otherwise 8).
- **Split campaigns.** Every command ran in the foreground within a 10-minute call limit, so these campaigns ran split with each driver's own functions and verdict rules. The slicing scripts are in `scripts/`.
  - D3: `--only`, 6 batches.
  - srp_top: `--only`, 5 batches, with coverage recomputed over the union exactly as the unsliced driver does.
  - ADP: `--only`, 3 calls.
  - GSI: 2 slices.
  - Admission: the 12th step run alone after the full driver stopped at the limit with 11 of 12 PASS.
  - Two runs overran a call and continued detached. I waited for both in the foreground before reading their results. One was the aborted srp_top attempt below; the other was srp_top batch 1, whose output went to this packet's scratch.
- **A write outside my scratch.** My first srp_top attempt used the Makefile default `MUTANT_OUTPUT=/tmp/srp-leaveall-mutants`. That directory existed before this review, and 57 of its log files were overwritten before I stopped the run. The list is in receipt 98, and the directory is otherwise untouched. Nothing else was written outside the clone and this packet, apart from the processes' own temporary trees, which were under this packet's scratch. My own module imports created two `__pycache__` directories in the clone, which I removed (receipt 99).
- **Not run by me:**
  - Yosys and the builder bank (excluded by the assignment).
  - `make -C tb/nvm_port figures`, which needs PR #13's objects fetched. The hosted step "nvm_port README figures agree with the tree" passed at the exact head.
  - The parent consumer bank and the donor full bank (manager duties).
- **Manager bank evidence.** I found no manager bank receipt for this exact head in the evidence tree at `c2424a3`: it holds the round-1 reviews and the round-2 author packet. I also found none among the #40 and #136 comments as of my read. My composition verdict rests on my own runs and on the hosted jobs above.
- **Parent read.** The parent was read only through a shallow read-only fetch of dev `ec0cc0c1` into scratch, for a grep. I built and ran nothing from it.
- **No hardware.** Physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof.

## Pending manager duties

1. Run and post the donor full bank, and the parent consumer bank (the 16 commands) at milan-fpga dev `ec0cc0c1`, with the combined #132 + C1 parent adaptation applied and the gitlink at this head.
2. At the merge turn, build the final current-dev candidate (source base `b2db3a97`, live dev `ec0cc0c1`), distinct from this source validation.
3. Own hosted and act acceptance. The hosted runs at this head are green (receipt 60).
4. Decide AEM_CONFIGURATION_INDEX_VALID (R406-1 S-1, R407-1 O1).
5. Route S-1 and S-2 at your discretion. Neither affects this verdict.
6. Note the `/tmp/srp-leaveall-mutants` overwrite (receipt 98) if another lane relied on those logs.

## Packet contents

- `REPORT.md` (this file).
- `MANIFEST.sha256` lists every published receipt, script and probe.
- `receipts/`:
  - 00: tool identity;
  - 10-12: suites;
  - 20-23: ADP campaign, README counts, probes, and the gate mutant's full run;
  - 30-36: the #132, C1 and pre-existing campaigns;
  - 40-42: ports, merge and parent grep;
  - 50: static gates;
  - 60: hosted checks;
  - 98: the `/tmp` overwrite record;
  - 99: clone integrity.
- `scripts/`: environment, Verilator job cap, suite runner, campaign slicers and mergers, port-list and README-count comparators.
- `probes/apply_probes.py`: the flag comparator and the refused-SET arms.

R406-2 FINISHED
