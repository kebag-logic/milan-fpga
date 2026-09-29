[R391] NEGATIVE - exact head 84572585ea76214c9f15f199590b8fc91f8c7edc

# R391-4: independent external review of processor PR #132 (issue #131, D3 lane 1), round 4

- **Repository.** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #132, issue #131, round R391-4.
- **Head.** Exact head `84572585ea76214c9f15f199590b8fc91f8c7edc`, tree `41df0c439cc64b1ee71c13644f2917a7c76d81eb`. The PR's live head reads the same sha. Base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`.
- **Delta reviewed.** `cbbb5acc..84572585`, three commits (`014e679`, `8610ab3`, `8457258`), 16 files (+672 / -46), plus the PR body's round-4 section and its consolidated parent-visible list.
  - RTL: `KL_pp_nvm_mgr_arb` (the issue-cycle drain), plus comment-only edits in `KL_acmp_nvm_shadow` and `KL_aecp_nvm_writer`.
  - Tests: D3R18-D3R21 in `tb/pp_top`, N10 in `tb/acmp_nvm`, seven new controls in `d3_mutants.py`.
  - Docs: 02, 07, 08 and 09, both guides, and the suite READMEs.
- **Authorities.**
  - The round-4 assignment (issue #131, 5880658258), including its ruling on round-3 item 4: no write is lost, and a SET lost to a power cut inside the DR2c backoff is admitted when it was reported at the cut.
  - The DR3a clarification (5876655419), the hold-admission ruling (5873580386), and the manager's bank note (5880274287).
  - Parent contract milan-fpga `docs/design/SAVED_STATE_MATERIALIZATION.md`. It is byte-identical at `b5c0f69d` and at live dev `eaa88a32`. I used §6.2, §6.3 (`blank`), §6.4, §8.1, §8.7, §8.8 and §18.1.
- **Reconstruction order.**
  1. Processor README, docs/README and hdl/README. There is still no AGENTS.md or CONTRIBUTING.md.
  2. Issue #131's comments through the round-4 assignment and the author's REVIEW READY, the manager's bank comment, and the PR body (rounds 1-4).
  3. The parent contract sections above.
  4. `git diff c951a9ff..84572585`, then the round-4 delta per commit.
  5. Public evidence:
     - milan-fpga `b657a2de` `review-evidence/pp131-r1`;
     - the author's round-4 packet `author-r4` on branch `pp131-review-evidence` (`0472e2f3`);
     - the hosted check runs at the exact head.
- **Inputs from my earlier rounds.** My round-3 packet (`pp131-r391-3-packet`) supplied my own scripts and findings. No private material was read. The other reviewer's round-4 archive on the evidence branch was not opened. That reviewer's prior public findings were read only after the verdict, findings and ledger below were written.

## Verdict

NEGATIVE, on one new MINOR in the parent-visible list (item 3). Everything else holds at this head.

**Item 1, `014e679`: the issue-cycle drain.**
- **RTL.** `KL_pp_nvm_mgr_arb.sv:156-160` arms the drain on an abort presented with a READ strobe in the cycle the arbiter issues it, for either manager. There is no port change. Lint of all five touched modules gives 0 findings.
- **No drain of a READ that was not abandoned.**
  - Each issue-cycle term ties a manager's abort to *that manager's own* issue (`iss0_w`/`iss1_w` are mutually exclusive), and to that strobe's own `we`.
  - The binding manager raises `nvm_abort_o` only in `H_RS_STREAM` (`KL_acmp_nvm_shadow.sv:576`). Its registered strobe is out only in the first `H_RS_STREAM` clock after `H_RS_REQ` (`:762-767`). So an abort meeting a strobe always belongs to that same READ.
  - The writer drives `m_req_o` in `W_RQ` or, after `done_r`, for service WRITEs. It drives `m_abort_o` only in `W_RD` (`KL_aecp_nvm_writer.sv:1089`, `:1095`). `done_r` is set only together with `ws_r <= W_DONE`. The two can therefore never coincide, and the writer never presents a WRITE strobe with an abort.
  - Measured: across 17,406 sweep runs, 0 clocks had the writer's request and abort together.
- **A WRITE strobe with an abort** is ignored, per the D3 rule that only reads are abandoned (`:157`, `:159`). No in-tree manager can present one.
- **Tests.**
  - D3R18 (`d3_phases.hpp:2084`) and N10 (`tb/acmp_nvm/sim_main.cpp:2513`) are cycle-exact.
  - The in-tree head-arbiter controls are KILLED: `drain_misses_issue_cycle` and `drain_misses_issue_cycle_m1`.
  - My strengthened sweep (P9, below) sees 42 binding READs abandoned in their issue clock. All 42 are drained, the port comes idle, and every one that ends DONE persists a later SET.
  - Under the pre-fix arbiter, 21 of those runs wedge the port, and in the 14 that end DONE the SET is lost.

**Item 2, `8610ab3`.**
- The in-tree `d3_mutants.py` reports **76 of 76 KILLED, goldens PASS** in my own run.
- My three round-3 survivors are KILLED at this head:
  - `proof_default_only_from_img` by D3R19 (both arms) and D3R20 `W_IMGLOC`;
  - `proof_past_bound_needs_fired` by D3R20 (both arms);
  - `agg_o_pulse` by D3R18 and D3R21.
- **My own mutants against the issue-cycle drain.** Of six, three are KILLED:
  - `issue_arm_m1_only` (manager 0's issue term dropped) by D3R18;
  - `issue_arm_m0_only` by N10;
  - `issue_arm_one_clock_late` by D3R18 and N10.
- The other three pass every graded suite and the whole default build: `issue_arm_stale_we`, `issue_arm_cross_intent` and `issue_arm_write_too`. Each changes behaviour only for an input no in-tree manager can present, so each is equivalent in the product. See S1.

**Item 3, the consolidated parent-visible list.**
- The list is sufficient on everything I ran in a scratch parent at live dev `eaa88a32` with the author's `parent_edits.py`. It applies cleanly: dev moved only in builder/LiteX clock-constraint files, and none of the edited files changed.
  - nvm_cosim quick: 315/315, with 0 PINMISSING.
  - pp_shadow: four builds, 0 failures.
  - milan_dp_render: 65/65, 152/152 and 5/5.
  - milan_dp legs `main`, `nxn` and `notify`: all pass.
  - Eight static gates, including the evidence classifier: rc 0.
- Every declared parent harness edit is a legitimate consequence of the ruled D3 behaviour. None hides a processor change that §6.2 or §8.1 forbids.
- But the declared `sim_nxn.cpp` edit silently removes the wedged-response-memory arm from the `notify` leg. That is the shipping 1x1 shape: 6 checks disappear there. The PR body says the arm runs after the restore. This is **F1**.

**Item 4, S1-S3.** All taken, with accurate wording.

**Item 5, DR3a.**
- Unchanged on every earlier path. D1's five arms are identical to round 3 (+4, +545, +44, +4,105, +545).
- The 17,406-run sweep matches round 3 run for run, apart from the new issue-clock tags.
- DR4's +1,031 LUT / +559 FF is in the PR body, inside the 2,500 / 1,400 ceiling. A single-module cross-check shows the arbiter at +2 LUT6 / 0 FF. The DR4 instrument itself is not available here (Limits).

## Findings

### F1 - MINOR - Conformance, Tests, Docs - the declared `sim_nxn.cpp` edit drops `[AECP-WTMO]` from the `notify` leg (the shipping 1x1 shape); the PR body says the arm runs after the restore

- **Where.**
  - PR #132 body, round 4, "Parent-visible for pin adoption", the `milan_dp` pool-legs bullet: "They must run the wedged-response-memory arm after the restore; its heal now answers SUCCESS."
  - Its implementation: `author-r4/parent_edits.py` (sha256 `a56d2977...`, branch `pp131-review-evidence` `0472e2f3`), the `sim_nxn.cpp` edit. It moves `prove_a_wedged_response_memory_reports_and_heals()` from before `if (prove_the_shipped_descriptor_image_enumerates()) return ...;` to after it.
  - Parent `tb/verilator/milan_dp/sim_nxn.cpp` at `eaa88a32`:
    - `:8021-8025` is the call order;
    - `:2466-2482`: under `NOTIFY_TIMED_TB`, `prove_the_shipped_descriptor_image_enumerates()` runs the notification and GSI sections and returns true;
    - `Makefile:290-300` builds the `notify` leg with `-DNOTIFY_TIMED_TB=1` on the shipping 1x1 shape.
- **Authority.**
  - Round-4 assignment item 3: the parent-visible list "must be complete". This review's item 3 asks whether each declared parent harness edit is legitimate and whether any hides something.
  - The arm's own banner (`sim_nxn.cpp:2382-2397`): it guards the 2026-08-13 board defect, a response memory that never acks must yield ENTITY_MISBEHAVING and then heal with no reset.
- **Evidence.** `receipts/parent-focused-summary.txt` and `receipts/parent/eaa88a32-*-dp-{notify,r391-nxn}.log`. Scratch parent at `eaa88a32`; `scripts/parent_scratch.sh`.

  | Leg | Base `c951a9ff`, unedited | Head with the declared edits | `[AECP-WTMO]` checks |
  |---|---|---|---|
  | `notify` (timed, 1x1) | 381 checks, 0 failures | 372 checks, 0 failures | 6 → **0** |
  | `nxn` (untimed, 4x4) | 1,844 checks, 0 failures | 1,841 checks, 0 failures | 6 → 6 |

  - In both legs the five `[AECP]` no-descriptor-memory degrade checks are replaced by two hold checks. That replacement is legitimate: with no image, §8.1 steps 1, 6 and 9 hold AECP from reset, and CLOSED keeps holding it.
  - Only in `notify` does the wedged-memory arm vanish as well. Every leg still passes, so no gate reports the loss.
- **Impact.**
  - The processor behaviour is still graded: the untimed `sim_nxn` legs and pp_shadow `[N]` both cover it.
  - But a pin-adoption lane that follows the declared list, as written and as its script applies it, loses this regression guard on the shipping 1x1 shape without being told. The PR body states the opposite for every `sim_nxn` leg.
  - The list is also silent that the `[AECP]` degrade arm is retired in every `sim_nxn` leg: `prove_read_descriptor_degrades_with_no_descriptor_memory()` stays defined but is no longer called.
- **Required outcome.** One of these two:
  - the declared `sim_nxn.cpp` edit keeps the wedged-memory arm in the timed leg, for example by running it inside the image arm after the restore and before the `NOTIFY_TIMED_TB` return; or
  - the PR body names the loss, and the pin-adoption lane records its disposition.

  In either case the list should state that the `[AECP]` degrade arm (5 checks) is retired and replaced by the two hold checks.
- **Verification.**
  - Apply the corrected edit in a scratch parent at `eaa88a32`: `notify` prints its six `[AECP-WTMO]` checks and passes.
  - Or re-read the PR body for the declared loss.

### S1 - SUGGESTION - Tests - pin the arbiter's own contract for inputs no in-tree manager presents

Three of my issue-cycle mutants survive `tb/pp_top` (7,868 checks) and `tb/acmp_nvm` (355). All three are equivalent in the product (Verdict, item 1):
- `issue_arm_write_too`: a WRITE strobe with an abort arms the drain, which would stall the write for ever;
- `issue_arm_cross_intent`: either manager's abort drains whichever READ is issued;
- `issue_arm_stale_we`: the issue cycle is judged by the previous operation's `we_r`, so an issue-cycle abort after a WRITE is lost. The binding walk issues no WRITE before its READs, because `H_FL_*` follows the walk.

N10 already drives a synthetic manager 1. Three short arms would pin the block's banner rules (`KL_pp_nvm_mgr_arb.sv:53-65`) should a third manager, or a change to either manager, make these inputs reachable:
- a WRITE strobe with an abort, which must not drain and must complete;
- manager 1's abort in the cycle manager 0's READ is issued, which must not drain that READ;
- an issue-cycle abort after a WRITE, which must still drain.

## Items of this round

1. **`014e679`.** Met, as under Verdict.
   - The comments at `KL_acmp_nvm_shadow.sv:161-166` and `:553-558`, 07 §5.3's row (`07_memory_maps.md:615`) and 02 §8.2 (`02_interfaces.md:596`) state the issue-cycle drain.
   - I did not run the other reviewer's E1 probe. Its case, a binding READ strobe on `agg_o`'s first clock, is exactly D3R18's. My sweep reaches it 42 times, at the aligned clock in several scenarios, with drain, idle port and a persisted SET.
2. **`8610ab3`.** Met.
   - D3R19 grades the §8.1 product order: no image at reset, and the image loaded before `PP_CTRL[1]`. It ends DEFAULTS, cause 3, 546 clocks after the bound, with 0 record READs. Its second arm places the bound inside the LOCATE.
   - D3R20 grades both on-clock proofs.
   - D3R21 grades a binding byte in hand on the expiry clock.
   - 76/76 KILLED. The README counts match the driver: 76 rows, and `acmp_nvm` 355 checks.
3. **Parent list.** Sufficient and legitimate, edit by edit, against §6.2, §6.3, §8.1 and §8.7:
   - **`gmstep`, `gptp`, `gptp-lat`: start the walk.** This is §8.1 step 3, the firmware's order.
   - **Image-less `main`, `nolpf`, `ax1x1`, `aclk`: accept CLOSED.**
     - With no image, §8.1 step 6 and §6.2's IMAGE row give CLOSED, which releases the listener and holds AECP and the enable.
     - I ran `main`: without the edit, only its one walk check fails (233 of 234 pass); with the edit, 234/234. Nothing else in the leg needs AECP or ADP.
     - The new predicate `done | (fail & !busy)` accepts exactly the terminals, because combined busy stays 1 from the binding walk's end until done or CLOSED (`protocol_processor_top.sv:2612-2614`).
     - These legs do not prove an image. The image legs (`sim_nxn`) still reject CLOSED, because they grade answered READ_DESCRIPTORs.
   - **`sim_nxn` legs: start the walk once the descriptor memory answers.** This is §8.1 steps 2-3, image before `PP_CTRL[1]`. Grading the held READ_DESCRIPTOR and its answer at the release is the hold-admission ruling. The coverage defect in this edit is F1.
   - **`milan_dp_render` T8: wait one commit-to-pin bound.**
     - The harness's own T14 law bounds commit-to-pin at `kFrameAxis + kCdcFloorAxis + kBitAxis` (`sim_tdm8_render.cpp:2065-2068`).
     - T8's "physical keys read disabled" check already proves that the removal committed by the answer. A frame committed earlier can still reach the pins inside that bound.
     - So the edit fixes a phase dependence the D3 walk's added boot time exposed. It does not mask a later commit.
   - **pp_shadow.**
     - K, K10 and K12 start the walk before the enable (§8.1 steps 3 and 10).
     - M2 starts it after the memory handover (§8.1 steps 2-3).
     - P3's blank 1 → 0 is *required* by the contract: blank = done AND NOT fail AND no record validated (`SAVED_STATE_MATERIALIZATION.md:737`, §8.7 "a failed product restore is never blank").
   - **nvm_cosim.** `rs_agg_i`, `wr_chg_o`, the derived backoff, the ceil `RS_TMO_CYC_P` and a 2,000 ms B1-B4 window give 315/315 at `eaa88a32`. The measured attribution (308 → 311 → 315) matches my round-3 variants and the ruling.
   - **Evidence classifier line.** `measure_test_evidence.py --check` returns rc 0.
   - **Firmware.** The persistence-disabled boot path and the bounded wait are declared. They are not applicable to a consumer gate.
4. **S1-S3 (my round 3).** Taken:
   - "plus a few clocks" and the 1,060 ms margin in 07 (`:657`), 08 (`:45`), the integrator guide (`:434-440`) and the writer banner;
   - both terminal-table points: the integrator's row `:91`, and 07's new row `:669` with its guide notes;
   - the direct-instantiator banner at `KL_acmp_nvm_shadow.sv:38-46`, comment only.
5. **DR3a / DR4.** As under Verdict.

## Judgement per section 18.1 sentence (delta only)

| Sentence | Judgement at 84572585 | Evidence |
|---|---|---|
| Measure its 1,000 ms aggregate ... both walks and roll-back | met; earlier paths unchanged, new paths +1 to +546 | D1 identical to round 3; P9 golden identical run for run |
| Exercise zero, boundary, corrupt, refused and indefinitely delayed inputs | met, now including every pre-proof variant and the issue-clock abort | D3R18-D3R21; P9 (42 issue-clock aborts) |
| Each must fail a named ... assertion | met in the tree (76/76); three arbiter-contract mutants are equivalent in the product | `receipts/d3_mutants-intree.log`; S1 |
| Release AECP/ADP early (negative control) | met | D1: 0 early enable cycles; D3R19 AECP released only at DEFAULTS |
| Re-run the processor's full required gates | the author's claim and the manager's bank; I re-ran the delta's suites and gates | Limits |

## IEEE 1722.1 / Milan behaviour relied on

- **Milan §5.6.1, via F07.9.** ADP may start only once the restore is done. It holds in every D1 arm and D3R19. In CLOSED the image-less parent legs keep the enable held, as the contract requires.
- **IEEE 1722.1-2021 AECP.** A command held by the admission is answered at the release, and further ones are dropped for the controller to retry. The parent `sim_nxn` edits grade this. The processor side is unchanged from round 3 (D3O5-D3O7 pass).

## Hosted evidence (read-only)

Workflow `hdl` ran at the exact head on `push` (run 36512813594) and on `pull_request` (run 36512816353). Both completed with success. Six jobs executed and none were skipped: `docs-gates`, `portability` and `suites`, twice each (`receipts/hosted-check-runs-head.txt`). The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | the round-4 assignment items 1-4 and its ruling; §6.2, §6.3, §6.4, §8.1, §8.7 against the arbiter (`KL_pp_nvm_mgr_arb.sv:53-65, 150-170`), the binding manager (`KL_acmp_nvm_shadow.sv:553-576, 750-770, 966`) and the writer (`KL_aecp_nvm_writer.sv:650-670, 1089-1095`); the PR body's consolidated list against `parent_edits.py` and the parent harnesses at `eaa88a32` | R391-4 | 84572585ea76214c9f15f199590b8fc91f8c7edc |
| RTL | CLEAN | full read of the RTL delta; the arm terms' intent binding, WRITE exclusion, drain end; the writer's request/abort exclusivity; combined status (`protocol_processor_top.sv:2611-2620`); lint of 5 modules, 0 findings; single-module LUT6 delta +2 / 0 FF | R391-4 | 84572585ea76214c9f15f199590b8fc91f8c7edc |
| Robustness | CLEAN | D1 (5 arms, the top's own derivations); P9 strengthened: 17,406 runs, port idle after every terminal, 42 issue-clock aborts drained with SETs persisted, 0 writer request+abort clocks, pre-fix arbiter 21 wedges; parent legs at `eaa88a32` | R391-4 | 84572585ea76214c9f15f199590b8fc91f8c7edc |
| Tests | UNCLEAN (F1) | D3R18-D3R21, N10; `d3_mutants.py` 76/76; my 26 mutants (22 fail the graded suites, `bind_agg_ignores_byte_in_hand` and 3 arbiter-contract mutants equivalent in the product, S1); pp_top `make run` 7,888/7,888, acmp_nvm 355/355, rx_validator 437/437; parent `notify`/`nxn`/`main` A/B, nvm_cosim, pp_shadow, render | R391-4 | 84572585ea76214c9f15f199590b8fc91f8c7edc |
| Docs | UNCLEAN (F1) | 02 §8.2, 07 §5.3 (row `:615`, `:657`, new row `:669`), 08 `:45`, 09 (two new rows, 76), integrator (`:91`, `:409-440`), operator (`:252-257`), both suite READMEs' mutation records, the arbiter and binding-manager banners; `make check` and `gen_matrix.py --check` rc 0; the PR body (rounds 1-4) | R391-4 | 84572585ea76214c9f15f199590b8fc91f8c7edc |

## Real limits

- **Simulator.** The path named in the brief, `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`, does not exist on this host.
  - I used a copy of the byte-identical sibling wrapper (sha256 `905795b9...`, identical across all 179 sibling wrappers).
  - It executes a binary with sha256 `fb2cc573...` that reports `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/verilator-identity.txt`), the same identity as rounds 1-3.
- **Not run:**
  - the full processor bank: `run_suites.sh` over 33 suites, full `lint_hdl.sh`, Yosys, `srp_top` mutants, `nvm_port` figures;
  - any builder, gPTP or Yosys bank;
  - xvlog;
  - `sw/builder/test_builder.py`;
  - the full `milan_dp` target: only its `main`, `nxn` and `notify` legs, through scratch-only make targets that reuse the recipe's own lines. The `nolpf`, `ax1x1`, `aclk`, `nxndv`, `nxn8` and `nxn4c` legs, `gmstep`, `gptp`, `gptp-lat` and both mutation campaigns are the manager's consumer bank.
- **DR4 not re-measured.** The instrument, Vivado out-of-context, is not on this host. The Yosys LUT6 figure is a single-module cross-check, not DR4.
- **Parent copies.** These are `--shared` local clones of the public milan-fpga at dev `eaa88a32`:
  - `protocol-processor` at the named sha;
  - `gptp-processor` and `third_party/verilog-axis` at the parent's gitlinks, from their public remotes;
  - `external` not fetched; no leg I ran needs it.

  The only edits are the author's `parent_edits.py` (sha256 recorded), two scratch-only make targets, and, for five static gates, a scratch index gitlink at the head plus `git submodule init`. Those five gates first REFUSED on unregistered submodules and returned rc 0 once registered. Both rows are in `receipts/parent/eaa88a32-headedits-static.log`.
- **Simulation only.** P9 overrides `NVM_RS_AGG_CYC_P` to 2,800 in disposable copies; D1 runs the top's own derivations. Physical calibration was NOT RUN, field skips are not hardware proof, and nothing here is hardware proof.
- **Receipt form.** The first D3-section mutant runs used a script revision that did not print `rc=` for failing runs. Their `FAIL:` lines and `D3: 133 checks, N failures` tallies are complete. The published `run_r391_4.sh` prints `rc=` in every case, and the `acmp_nvm` receipts come from it.
- **Clone hygiene.** Every build, probe and mutant ran on `git archive` exports or `--shared` clones under this packet's `scratch/`.
  - One stray empty `abc.history` was written into the clone's work tree by the single-module synthesis (its working directory). It was removed.
  - At the end, HEAD, the tree and the index agree. All 312 work-tree blobs rehash to their tree blobs, and the modes match. Status, ignored files included, is empty. There are no gitlinks and no `.gitmodules`, so no submodule gitlinks are required (`receipts/clone-integrity.txt`).

## Pending manager duties

- Adjudicate F1 into the next round. It is a PR-body and `parent_edits.py` correction, with no processor source change.
- Consider S1 (three short N10 arms).
- Run the donor full bank and the parent consumer bank at dev `eaa88a32`, including the `milan_dp` legs and campaigns I did not run.
- Build the final current-dev candidate at the merge turn (source base `c951a9ff`).
- Carry into the pin-adoption lane: the consolidated list, F1's disposition, and the firmware persistence-disabled boot path with its host test.
- Own hosted and act acceptance, and record that physical calibration is NOT RUN.

## Prior public findings, resolved or retained at this head

These were read after the verdict, findings and ledger above were written. The other reviewer's round-4 report (R390-4) is concurrent with this one, not prior, and was not read.

**My own earlier findings.**

| Finding | Status at 84572585 | Evidence |
|---|---|---|
| R391-3 F1 MINOR, the parent list omits the nvm_cosim backoff binding and misattributes the 7/315 | **Resolved** | The body names `rs_agg_i`, `wr_chg_o`, the derived `RETRY_BACKOFF_CYC_P`, the ceil `RS_TMO_CYC_P` and the 2,000 ms B1-B4 window. The attribution matches my round-3 variants (308 → 311 → 315). 315/315 with 0 PINMISSING at `eaa88a32`. F1 of this report is a new finding on the round-4 `sim_nxn` edit, not a retention. |
| R391-3 F2 MINOR, three pre-proof variants unguarded | **Resolved** | D3R19-D3R21. `proof_default_only_from_img`, `proof_past_bound_needs_fired` and `agg_o_pulse` are KILLED by my own script and in the tree. |
| R391-3 S1-S3 | **Taken** | Items 4 above |
| R391-1 F1-F4, R391-2 F1-F2, R391-2 S1 | stay **resolved or taken** | pp_top `make run` 7,888/7,888 (D3O5-D3O7, D3R13-D3R17); my 26 mutants include R391-2's set, and 19 of R391-3's 20 fail the D3 section as in round 3 |

**The other reviewer's findings.**

| Finding | Status at 84572585 | Evidence |
|---|---|---|
| R390-3-F1 MAJOR, an abort in the arbiter's issue cycle is lost and the port wedges | **Resolved** | `KL_pp_nvm_mgr_arb.sv:156-160`. D3R18 and N10. Head-arbiter controls KILLED, plus my `issue_arm_m1_only`, `issue_arm_m0_only` and `issue_arm_one_clock_late`. P9: 42 aligned aborts all drained, SETs persisted; pre-fix, 21 wedges. Comments at `KL_acmp_nvm_shadow.sv:161-166, 553-558`, 07 `:615` and 02 `:596` corrected. That reviewer's E1 probe was not run by me; D3R18 is the same case. |
| R390-3-F2 MINOR, expiry during the proof and on the proof clock ungraded | **Resolved** | D3R19 "inside the LOCATE" (the bound 271 clocks in) and D3R20. `agg_closes_during_proof` and `proof_past_needs_fire` are KILLED in my in-tree run. |
| R390-3-F3 MINOR, the pin-adoption list incomplete and the B1-B4 attribution inexact | **Resolved** as to every point it named: `wr_chg_o`, the backoff derivation, the B1-B4 window, the PP_CTRL[1] harness and firmware obligations, and the attribution as measured | PR body round 4. My F1 is a new defect in how the newly declared `sim_nxn` edit is described, not a retention. |
| R390-3-S1, firmware-wait wording | **Taken** | same wording as my S1: "plus a few clocks", 1,060 ms margin |
| R390-3-S2, D3R15's re-LOCATE arm grades CLOSED over an image a healthy LOCATE would prove; asks for a manager confirmation | **Open for the manager, unchanged** | The round-4 assignment did not rule it. The RTL and D3R15 are unchanged. §6.2's "ABORT during the roll-back → CLOSED" admits the head's reading. |
| R390-2-S1, no `RX_SLOTS_P >= 2` floor, carried | **Not taken (not assigned)** | no check or statement at head |
| R390-1 F1-F4, S1, S2; R390-2 F1-F3, S2 | stay **resolved or taken** | as recorded in R391-3. D3O5/D3O6 pass, `d3_mutants.py` 76/76 includes their controls, and `agg_ignores_in_hand`'s case is D3R17 (pass). |

## Receipts and reproduction

Every file below is listed in `MANIFEST.sha256`. The scripts take a processor checkout, a scratch directory and a directory holding a Verilator 5.050 `verilator`. None of them writes into the checkout.

**Scripts.**

- `scripts/run_r391_4.sh <checkout> <rev> <scratch> <verilator dir> <probe> [args]` runs these probes:
  - `d1 [MUTANT]`: D1 (`scripts/r391_4_d1.hpp`);
  - `sweep AGG STEP SCENS [MUTANT]`: the strengthened P9 (`scripts/r391_4_sweep.hpp`);
  - `d3 [MUTANT]` and `full [MUTANT]`: the pp_top D3 section, or the default build;
  - `acmp [MUTANT]`: `tb/acmp_nvm`.

  Mutants come from `scripts/r391_4_mutants.py`.
- `scripts/parent_scratch.sh <parent clone> <parent rev> <checkout> <rev> <scratch> <verilator dir> <name> <edits|none> <target> [args]` builds a scratch parent and runs one focused target. It needs `GPTP` and `VAXIS` (local clones of those public remotes).
- The in-tree campaign was run as `python3 tb/pp_top/d3_mutants.py --output DIR --verilator V --jobs 4 --only <chunk>` from a `git archive` export, in five chunks, with builds at `-j 2`.

**Receipts.**

- **Gates and suites:**
  - `receipts/make-check-head.log`, `gen-matrix-check-head.log`, `lint-touched-head.log`;
  - `suite-pp_top-head.log` (7,868 + 20), `suite-acmp_nvm-head.log` (355), `suite-rx_validator-head.log` (437).
- **Mutants:**
  - `receipts/d3_mutants-intree.log` and `d3_mutants-intree-results.json` (76/76);
  - `mutants-r391-4-d3only.log` (my 26);
  - `mutants-r391-4-acmp_nvm.log` (6);
  - `mutants-r391-4-survivors-fullsuite.log`.
- **Probes:** `receipts/probe-D1-head.log`, `probe-P9-aggsweep-golden.log`, `probe-P9-aggsweep-mutant-issue_arm_m1_only.log`.
- **Parent:**
  - `receipts/parent-focused-summary.txt`;
  - `receipts/parent/eaa88a32-*.log` (base, headonly and headedits legs; nvm_cosim; pp_shadow; render; static gates);
  - `receipts/parent/author-r4-parent_edits.sha256`.
- **Environment:** `receipts/hosted-check-runs-head.txt`, `clone-integrity.txt`, `verilator-identity.txt`, `yosys-arb-lut6-delta.txt`.

R391-4 FINISHED
