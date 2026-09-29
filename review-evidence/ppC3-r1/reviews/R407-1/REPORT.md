[R407] POSITIVE - exact head 9185c491b56358d6bc15b5069b612bfaa95316f3

# R407-1: external independent review of PR #136 (lane C3, ADP)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #136 (`c3-adp-coverage` into `main`). It closes #40 and #41 and relates to #85.
- Exact head `9185c491b56358d6bc15b5069b612bfaa95316f3`, tree `93ec21cf2788017b578a83cb6c1c376cca2eee30`. The diff base is `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`, with five commits on it.
- Review round R407-1, opened by PR comment 5891057748. Assignment: #40 comment 5888002660.
- Role: external independent reviewer, working in a cleared context in an isolated detached clone.

**Verdict: POSITIVE.** Every acceptance item in scope is met at this head: #40 items 1-4, #41 items 1-3, and #85 items 1-3. #85 item 4 correctly stays open. The three route checks the manager asked for, (a), (b) and (c), hold, and (c) was probed beyond the PR's own tests. There are no open BLOCKER, MAJOR or MINOR findings. Three SUGGESTIONs are recorded, and none of them affects the verdict.

## 1. How the review was reconstructed

I read the scope in this order:

1. The repository has no `AGENTS.md` or `CONTRIBUTING.md` of its own. I read `README.md` and `docs/README.md` instead, which cover the ID registries, the single-source rules and the editing workflow.
2. The scope itself:
   - the bodies of issues #40, #41 and #85, with their frozen acceptance lists;
   - the manager's comments: the assignment on #40 (5888002660) and the lane notes on #41 and #85;
   - the author's TAKEN and REVIEW READY comments.
3. The requirement and interface authorities: `docs/00_MILAN_COMPLIANCE_REVIEW.md` rows REQ-ADP-002/005/006/007/012/013 and GAP-16, `04_adp_engine.md` §3, `02_interfaces.md` §2, and integrator guide §6.
4. The whole diff `c951a9ff..9185c491`, commit by commit.
5. The public evidence at milan-fpga `795bda4c` `review-evidence/ppC3-r1`: MANIFEST.json, author/HANDOFF.md and author/PR-BODY.md. The published PR-BODY.md is identical to the live PR body.

When my pass started, the PR carried only the two review-start notices. There were no review threads and no findings from earlier review rounds. This is round 1, so there are no prior findings to resolve or retain.

## 2. Acceptance, item by item

| Item | Judgement | Evidence |
|---|---|---|
| #40.1 top: after a SUCCESS SET_CONFIGURATION, the next ENTITY_AVAILABLE is byte-exact except available_index and current_configuration_index | MET | `tb/pp_top/sim_main.cpp` `AdpConfigPhase`, sections AD2 and AD3 (`only_the_index_moved` plus a byte-exact `avail()`). The section runs in the default run: `AD: 34 checks, 0 failures` in `receipts/gates/suite-pp_top.log` |
| #40.2 unit: `current_cfg_i` changes between two adverts and only bytes 64..65 move | MET | `tb/adp_engine/sim_main.cpp` P11a/b. P11c adds a change in the middle of the build that would tear the index, P11d covers DEPARTING and P11e the restart |
| #40.3 route | MET, preferred route | `hdl/top/protocol_processor_top.sv:1643` and `hdl/aecp/KL_aecp_engine.sv:1683` (`dyn_cfg_valid`). See §3 |
| #40.4 mutation record | MET | 8 `cfg-*` arms, all KILLED by their named checks in my run (`receipts/adp-mutants/`) |
| #41.1 unit: link up and one bounce with enable low for more than 4000 ms, with no draw, arm, frame or DOWN exit | MET | P12: 4100 + 20 + 4100 modeled ms with the timer service live, graded in every clock |
| #41.2 top: more than 4 s with enable low, and `q_adp` empty before S3 flushes it | MET | AD0 is a new phase with 4200 + 20 + 4200 ms and nothing flushing the queue. S3 also gains a check before its flush |
| #41.3 mutation record | MET | `gate-enable-dropped`: 30 failures on the unit, including all four P12 checks. `gate-enable-dropped-top`: AD0 fails. My probe also reproduces the README's full-run statement: 3 failures of 7,766 in the default build, all in AD (`receipts/probe-gate-full.log`) |
| #85.1 every F04.2 cell from an independent table, ending in a cell count | MET | `ADV[9][5]`: 45 cells, `CHECK(adv_cells == 45)`, classes N12/I20/S6/C7. The table is transcribed from the specification, not from the RTL |
| #85.2 DOWN x {DISCOVER, GM_CHANGE, SHUTDOWN} inert; DELAY x LINK_DOWN cancels with no DEPARTING; DELAY x SHUTDOWN departs and resets the index | MET | These cells are walked, with the DELAY rows walked in both hardware phases. Each cell grades the state, draws, timer operations, frames byte-exact, available_index, GM ticks, events and RX frees |
| #85.3 every F04.3 arc in the same walk, with the named mutations red | MET | 33 cells, `CHECK(disc_cells == 33)`, arcs 8 of 8. Both issue-named mutations are KILLED, along with 15 more `walk-*`/`disc-*` arms. See SUGGESTION S1 for a partition gap outside the acceptance text |
| #85.4 live-controller interop | OPEN, as scoped | The README restates the limit as open (bench lane). The PR says "Relates to #85" and does not close it |

## 3. Route checks the manager asked for

**(a) The port and parameter lists of `protocol_processor_top` are unchanged.** I checked this mechanically (`scripts/port_list_compare.py`, `receipts/port-lists.txt`). I compared the comment-stripped module headers at base and head:

- **Identical:** `protocol_processor_top` (978 tokens), `KL_aecp_dyn_state`, and `KL_adp_engine`.
- **One change:** `KL_aecp_engine` gains exactly one output, `dyn_cur_config_v_o`.
- **Other modules the parent instantiates by name:** no source of the NVM, shadow or manager-arbiter modules changes.
- **Instantiation:** within the processor, `KL_aecp_engine` is instantiated only by the top. A read-only `git grep` of the parent at `79c36963` finds no RTL instantiation of `KL_aecp_engine`, only prose mentions (`receipts/parent-readonly-grep.txt`).

**(b) The new meaning of `current_cfg_i` is stated correctly, and it is harmless for the parent.**

- These texts all say the same thing: the port comment (`protocol_processor_top.sv:189-192`), `02_interfaces.md` §2 rule 4, `04_adp_engine.md` §3, `integrator.md` §6, and the PR body's parent-visible list item 2. `current_cfg_i` is the image default, and after SET_CONFIGURATION the overlay is advertised. No loopback is needed.
- In the parent at `79c36963`:
  - `milan_datapath.sv:7602` drives `current_cfg_i` from `cfg_adp_current_config` (ADP_IDX0, reset value 0);
  - `test_builder.py:25328` asserts `configurations_count == 1`.
- So in the parent the only legal SET is 0, and the wire is unchanged while ADP_IDX0 is 0.

**(c) The ADPDU equals what GET_CONFIGURATION answers, after a success, after a refusal, and across a reset.**

*Structural argument:*

- The new flag decodes `st_req && dyn_sel && we && region == DYN && sel == 0 && dyn_ix == 0`. The store's `take_wr_w` (`KL_aecp_dyn_state.sv:252`), specialised to selector 0, has count 1, so its range check is `dyn_ix == 0`. The two conditions are therefore identical, cycle for cycle, and both are reset only by the same `rst_n`.
- On the same edge, `cfg_r` and the flag update together, so a set flag never exposes the stale value.
- The only write is `WRITE_ST ... SEL_CFG` in the SUCCESS path (`gen_ucode.py:1674`). The LOCKED, BAD_ARGUMENTS and STREAM_IS_RUNNING arms (`E_SCFGLK`, `E_SCFGBAD`, `E_SCFGRUN`) never write the store.
- The ADP builder samples the index at `B_SAMPLE` (`KL_adp_engine.sv:909`), so the field cannot tear.

*Executable probe* (`probes/probe_c_rejected_and_reset.py`, `receipts/probe-c-rejected-and-reset.log`; AD grew to 50 checks, 0 failures). In every case below, the ADPDU index, GET_CONFIGURATION and ENTITY.current_configuration were equal:

| Case | Value |
|---|---|
| (a) SET(5) refused BAD_ARGUMENTS on a set row | 1 |
| SUCCESS SET(0) | 0 |
| (b) reset, with the NVM model kept, then restore and re-enable | 1, the image default |
| (c) SET(9) refused after the reboot | 1 |
| (d) SET refused ENTITY_LOCKED under another controller's lock | 1 |

At this head the configuration row is not restored from NVM, so all three views fall back to the image default together. The merge-train note in the PR body, on PR #132's restore writer, is correct and is recorded in §8.

## 4. Executed evidence at the exact head

The pinned simulator identifies itself as 5.050 rev v5.050. The `receipts/*` files hold raw logs, and each rc is recorded in the receipt.

| Command | rc | Result |
|---|---:|---|
| `make -C tb/adp_engine` | 0 | 1367 checks: 1367 PASS, 0 FAIL |
| `make -C tb/pp_top` (both builds) | 0 | 7786 checks, 0 failing; section AD 34/0 |
| `make -C tb/timer_map` (the third suite that compiles changed RTL) | 0 | 1360/1360 |
| `./scripts/lint_hdl.sh`, `check_upc_map.py`, `make check`, `gen_matrix.py --check`, `git diff --check c951a9ff..HEAD` | 0 | lint OK over every top; the UPC map agrees; links, WaveDrom, both matrices and parameters OK |
| `make -C tb/adp_engine mutants` (new) | 0 | 2 controls PASS, 27/27 arms KILLED by their named checks. The per-arm failure counts equal the README table exactly |
| `tb/pp_top/gsi_mutants.py` (compiles the changed top) | 0 | 20 detected by named checks; golden and restored PASS |
| `tb/pp_top/name_wr_mutant.py` (compiles the changed top) | 0 | decode killed; golden and restored PASS |
| Parent `scripts/measure_test_evidence.py --check` in a scratch parent at milan-fpga `79c36963` (gitlink at head; base run for comparison) | 0 / 0 | head: `74 <= 77` suites without an arm, 0 unexplained DUT readers. Base: `75 <= 77`. adp_engine is now counted as armed through `mutants.py`. The "74 <= 77" claim holds |
| Reviewer probes | n/a | refused and reset equality (§3c); the gate mutant on the full default run (3 of 7,766); the F04.3 domain guard (S1) |

**Hosted CI, read only (run 36571814541, head_sha `9185c491`).** These results are from executed jobs, not skipped contexts:

- `docs-gates`: success.
- `portability`: success.
- `suites`, completed steps: "Lint + every suite" success, "SRP LeaveAll mutation campaign" success, the new **"ADP mutation campaign" success**, and "Traceability matrix" success.
- "nvm_port README figures" was still in progress at 13:51Z.
- `Build Verilator` was skipped because the cache hit.

The snapshots are `receipts/hosted-jobs-snapshot{1,2,3}.json`. Hosted and act acceptance stays with the manager.

## 5. Findings

There are no open BLOCKER, MAJOR or MINOR findings.

**S1: SUGGESTION.**

- **Lenses:** Tests, Conformance.
- **Location:** `tb/adp_engine/sim_main.cpp:230` (`DiscRow`) and `:253` (`DISC`); `tb/adp_engine/README.md:122-124`.
- **Evidence:** the F04.3 walk splits the GM-mismatch guard by index relation (`V_GMF` with index > last, `V_GMS` with index <= last), but it walks the domain-mismatch guard only with index <= last (`V_DOMS`). No row exists for "domain mismatch, index > last" x TK_DISCOVERED. By the same §5.6.4.5.2 step-3 reading the README gives for GM ("no GM test on a fresh index"), that cell saves and re-arms. A domain-only analogue of the campaign's `disc-fresh-checks-gm` arm survives the whole suite: it adds `&& (rx_dom_r == dom_slice_f(rxq_if_r))` to the fresh-index branch, and the suite still reports `1367 checks: 1367 PASS` (`receipts/probe-domain-fresh.log`, `probes/probe_mutants.py domain-fresh`).
- **Impact:** a future regression in the domain half of that branch would pass. The shipped RTL is correct, and all 8 arcs and both named mutations are graded, so the acceptance text is met.
- **Suggested outcome:**
  - add the row, making 34 cells, or state the partition choice in the README;
  - optionally add a `disc-fresh-checks-domain` arm.
- **Verification:** the probe edit turns the suite red.

**S2: SUGGESTION.**

- **Lenses:** Tests, Conformance.
- **Location:** `tb/pp_top/sim_main.cpp:9944-9975` (`AdpConfigPhase::run`).
- **Evidence:** section AD grades ADPDU = GET = ENTITY after SUCCESS SETs only. The refused-SET and reset cases hold, both structurally and in my probe (§3c), but the suite does not pin them.
- **Impact:** a later change, such as PR #132's restore writer, could split the advertised index from GET after a refusal or a reboot without a red check. The merge-train note depends on exactly this.
- **Suggested outcome:** add a refused SET (BAD_ARGUMENTS or ENTITY_LOCKED) and a reset-and-re-enable leg to AD, comparing all three views.
- **Verification:** the probe code in `probes/probe_c_rejected_and_reset.py` is a working template.

**S3: SUGGESTION.**

- **Lens:** Docs.
- **Location:** `docs/architecture/09_verification.md:138-143` and `docs/guides/integrator.md:251-257`.
- **Evidence:**
  - In 09, the new MTXW paragraph has no blank line before "Each `tb/<suite>/README.md` states...", so the two topics render as one paragraph.
  - In integrator §6, "from then on ... no longer reads `current_cfg_i`" does not say "until the next reset". At this head a reset, and so a power cycle, returns the advert and GET to the image default (`current_cfg_i`), because the configuration row is not restored.
- **Impact:** cosmetic, plus a small ambiguity for integrators.
- **Suggested outcome:** add the blank line, and add "until reset" or a restore note, which can come with #132.
- **Verification:** read the rendered text.

**Observations.** None of these is a finding against this PR.

- **O1:** IEEE §6.2.2.18 on AEM_CONFIGURATION_INDEX_VALID (F04.6 leaves it clear). The author disclosed this. It predates the lane: the field already carried `current_cfg_i`. #40's frozen acceptance requires the index to move. It is recorded as a manager decision.
- **O2:** the S3 pre-flush check does not detect `gate-enable-dropped` in the full run. The README says so honestly, and AD0 is the check that does detect it. Acceptance #41.2 allows "or a new phase".
- **O3:** AD2 pins "no advert between the SET and the cadence". This is consistent with Milan Table 5.51, which has no configuration-change event.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 and S2 are SUGGESTIONs) | the issue bodies and acceptance lists; REQ-ADP-005/006/007/012/013; the Milan §5.6.1/§5.6.2/§5.6.3.5/§5.6.4.5 citations as the PR and the tables transcribe them; the IEEE §6.2.2.18/§7.4.7/§7.4.8.2 behaviour in the µcode (`gen_ucode.py:1656-1750`, E_GCFG); the ADV and DISC tables against the README and F04.2/F04.3; probe (c) | R407-1 | 9185c491 |
| RTL | CLEAN | `KL_adp_engine.sv` (`bld_cfg_r`, B_SAMPLE, `frame_byte_f`), `KL_aecp_engine.sv:1658-1712` (`dyn_ix_w`, `dyn_cfg_valid`), `KL_aecp_dyn_state.sv:180-334` (the equivalence of the decode), `protocol_processor_top.sv:186-192,1632-1670,3503`; the header comparison; lint | R407-1 | 9185c491 |
| Robustness | CLEAN | same-edge update of value and flag; the refusal arms never write; reset symmetry; the effect of the duplicate `SEL_CFG_C` constant (caught end to end by AD1b/AD2); the #132 merge-train dependency (disclosed; delta review queued by the manager); isolation in `mutants.py` (scratch tree, controls, named-check kill rule, a build failure never counts as a kill) | R407-1 | 9185c491 |
| Tests | CLEAN (S1 and S2 are SUGGESTIONs) | the whole `tb/adp_engine/sim_main.cpp` diff (P11, P12, P13 walk); the `tb/pp_top` AD section and S3; the 27 patch files (all hdl-only); campaign rerun 27/27; GSI 20/20; name-write; the ratchet 74 <= 77; three probes | R407-1 | 9185c491 |
| Docs | CLEAN (S3 is a SUGGESTION) | `02_interfaces.md` §2.4, `04_adp_engine.md` §3, `09_verification.md` §4 and the matrix row, `integrator.md` §6, `tb/adp_engine/README.md` (mutation table checked against my logs), `tb/pp_top/README.md`, the PR body parent-visible list, `make check` | R407-1 | 9185c491 |

## 7. Real limits

- **Simulator.** The assigned simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used the manager lane's sibling pinned wrapper, `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, which reports `5.050 rev v5.050`, the CI pin. Its install root is redacted in the receipts as `<PINNED-SIMULATOR-ROOT>`.
- **Suites not run locally.** I did not run the full processor bank (`run_suites.sh`) or the Yosys, parent, gPTP or builder banks, as the scope forbids. Locally I ran only the three suites that compile the changed RTL, plus the static gates.
  - "Every processor suite rc 0" rests on the hosted `suites` step (lint + every suite, success at the exact head) and on the manager's banks.
  - `tb/srp_top` mutants, `acmp_talker` retry, `srp_admission`, `desc_mem_guard` and `nvm_port` figures were not rerun. They do not compile the changed modules.
- **Parallelism.** The first gate batch ran 4 suite builds at once without CPU pinning, and each build used its Makefile's own build parallelism. Every later run was pinned to 8 CPUs.
- **The parent script.** The ratchet check ran as a single parent script in a scratch, shared-object clone of a local parent checkout at `79c36963`, with `gptp-processor` at its pin `5dce647`. The `external` and `third_party` submodules were absent. No other parent gate ran.
- **The specification.** The specification PDFs are not available here. I judged conformance against the clause text the repository and PR quote, and against the internal consistency of the tables and the RTL.
- **Not run.** No hardware, no physical calibration, and no Docker or act. Field skips are not hardware proof.

## 8. Pending manager duties

- **The donor and parent banks.** After my verdict was written I read the manager's evidence comment 5891619124 (13:48Z). It posts the donor full bank as PASS, 9 of 9, and the parent consumer bank as PASS, 16 of 16, at milan-fpga dev `79c36963` with the gitlink at this head and no parent edits. I did not reproduce either bank; the manager owns them.
- **Hosted acceptance.** At my last snapshot, the `nvm_port` figures step was still running.
- **The merge of main.** Merge main (`d352bbaa`, PR #132) into this branch before the merge, then hold the queued delta review. That review should confirm that `dyn_cfg_valid` still mirrors every writer of the configuration row, including #132's restore path. S2's legs would pin this.
- **O1.** Decide on AEM_CONFIGURATION_INDEX_VALID.
- **#85 item 4.** Keep it open for a bench lane.

**Clone state after the probes.** `scripts/verify_clone_restored.sh` reports: HEAD, HEAD^{tree} and the index tree equal the exact head. All 335 tracked files are byte- and mode-identical to their blobs. There is no tracked or untracked drift, and my build products were removed. The processor tree has no gitlinks. The receipt is `receipts/clone-restored.txt`.

Publishable files are listed in `MANIFEST.sha256`. Everything under `scratch/` is disposable and unpublished.

R407-1 FINISHED
