[R390] NEGATIVE - exact head 84572585ea76214c9f15f199590b8fc91f8c7edc

# R390-4: independent internal review of processor PR #132 (issue #131, D3 lane 1), round 4

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| Head reviewed | `84572585ea76214c9f15f199590b8fc91f8c7edc`, tree `41df0c439cc64b1ee71c13644f2917a7c76d81eb` (verified in the review clone) |
| Delta | `cbbb5acc..84572585`: three commits, `014e679`, `8610ab3` and `8457258` (16 files, +672/−46), plus the PR body's consolidated parent-visible list; base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` |
| Rulings | Round-4 assignment (processor issue 131 comment 5880658258), which also rules round-3 item 4: no write is lost, and a SET lost to a power cut inside the DR2c backoff is admitted when reported at the cut. The DR3a clarification (5876655419), and the ratification and DR2 rulings on parent issue 70 |
| Contract | parent `docs/design/SAVED_STATE_MATERIALIZATION.md`, sha256 `e26784e1…f077`, identical at `7a7582f0`, `b5c0f69d` and dev `eaa88a32`. Read: §§5.1–5.3, 6.2, 6.4, 7 and 8.1 |
| Verdict | **NEGATIVE**: one MINOR finding (Docs) is open. Conformance, RTL, Robustness and Tests are CLEAN; Docs is UNCLEAN. All three of my round-3 findings are resolved. |

## 1. How the review was reconstructed

1. **Conventions.** The repository still has no AGENTS.md or CONTRIBUTING.md. The conventions come from `README.md`, `docs/README.md` and `docs/architecture/09_verification.md` §7, and the suite READMEs' mutation records.
2. **Issue #131 and PR #132.**
   - The round-4 assignment (5880658258) and the author's review-ready note (5882491224).
   - The PR body, including the "Round 4" section and the consolidated "Parent-visible for pin adoption: rounds 1-4" list.
   - The manager's bank at `cbbb5acc` (5880274287), and the R390-4 review-start comment (5882509942).
   - Parent issue 70: the lane-2 scope record (5880276193).
   - When I checked, no manager bank comment at this head had been posted on the issue, the PR or parent issue 70. The only evidence at this head is the author's packet.
3. **The D3 contract, read from a read-only parent clone at dev `eaa88a32`:**
   - §5.1: the Port, Binding walk, Ownership and Exports rows, and the backoff derivation;
   - §5.2: the parent glue, including H8, "restore blank reads 1 only for a restore that did not fail";
   - §5.3: the firmware order;
   - §6.2: the restore table;
   - §6.4: the drain;
   - §7: the clear rule and K18;
   - §8.1: the order and the three release points.
4. **The diff.** I read `git diff cbbb5acc..84572585` hunk by hunk:
   - the arbiter's `arm0_w`/`arm1_w`;
   - the shadow and writer comments;
   - `tb/acmp_nvm` N10;
   - `tb/pp_top` D3R18–D3R21, the new wrap taps and bench knobs;
   - the seven new `d3_mutants.py` rows, the README rows, and every documentation hunk (02, 07, 08, 09, integrator, operator).

   I also re-read the shadow's `rs_tmo_w`/`nvm_abort_o`/`nvm_req_o` and the writer's `m_req_o`/`m_abort_o`. Those two managers are the only drivers of the new arm.
5. **Public executable evidence.**
   - `kebag-logic/milan-fpga@b657a2de` `review-evidence/pp131-r1` is the round-1 author packet.
   - The round-4 author packet is `author-r4/` on branch `pp131-review-evidence` at `9e9dbd3d`, of which `b657a2de` is an ancestor. From it I used `parent_edits.py`, `parent-edits.diff`, the gate result lists, `dr3a-8457258.txt` and `d3r18-d3r21-values-8457258.txt`.
   - I did not open the other reviewer's archived reports on that branch.
   - Hosted checks at this head: §7.
6. **My own execution at the exact head.** Every run used disposable `git archive` copies under the packet's `scratch/`, with the pinned simulator named in §7:
   - **`tb/pp_top`, full (both builds):** 7,888 checks, 0 failures. The D3 section has 133 checks, 13 more than in round 3 (`receipts/pp_top-full-head.txt`).
   - **Focused suites, all PASS:** `acmp_nvm` 355, `nvm_port` 136, `desc_mem_guard` 78, `dyn_state` 118, `desc_store` 584, `lsn_admit` 18, `adp_engine` 533, `rx_validator` 437.
   - **Lint:** `lint_hdl.sh` rc 0, 41 modules.
   - **Documentation gates, all rc 0:** `links` 968, `matrix`, `modmatrix`, `params` 26/26/26, `stale`.
   - **DR3a:** `--dr3a` is byte-identical to my round-3 receipt and to the author's.
   - **The in-tree `d3_mutants.py`**, from an exact-head copy with 8 jobs: **76 of 76 KILLED**, goldens PASS. Every README record equals my run.
   - **My round-3 probe scripts, rerun:** E1, E2, D1 and the round-1/2 probes.
   - **Mutants:** my 18 earlier mutants, rerun, plus four new mutants of the issue-cycle drain.
   - **New probes:** an arbiter unit probe, and an arbiter monitor over the whole `pp_top` and `acmp_nvm` runs.
   - **Scratch parents at dev `eaa88a32`:** the author's `parent_edits.py` applied, then focused parent runs (§5).

## 2. Findings

### R390-4-F1: MINOR. The consolidated parent-visible list leaves out one parent harness that exercises AECP without starting the restore walk: `milan_dp`'s `ax1x1gptp` leg, the nightly physical gPTP suite

- **Lenses:** Docs.
- **Where:**
  - The PR body, "Parent-visible for pin adoption: rounds 1-4, consolidated". The harness part is headed "Parent harnesses, all found by the consumer set". Its first item names the `PP_CTRL[1]` obligation for `sim_gmstep.cpp` and `sim_gptp.cpp` only.
  - The author's `parent_edits.py`, the list's sufficiency demonstration, does not touch the harness.
  - At parent dev `eaa88a32`, `tb/verilator/milan_dp/sim_ax1x1gptp.cpp`:
    - `:672-690`, `:716-719` and `:930`: every CSR write the harness makes. None is to PP_CTRL (`0x920`), and no restore-walk helper exists in the file;
    - `:918`: it serves the built AEM image, `obj_ax1x1gptp/aemi.bin`;
    - `:774-786` and `:936-938`: it grades GET_AVB_INFO and GET_AS_PATH answered SUCCESS, including a pre-acquisition GET_AVB_INFO.
  - How it runs: `tb/verilator/milan_dp_gptp/Makefile:9` runs `make -C ../milan_dp ax1x1gptp`, the scheduled physical job in `.github/workflows/rtl.yml` (cron `17 1 * * *`, `:366`). The default `milan_dp` sweep, and so the consumer set, does not build it.
- **Authority:**
  - The round-4 assignment, item 3: the list "must be complete", and names every parent-visible item.
  - The lane-2 scope record (5880276193), item 1: "Every parent harness that exercises AECP must set PP_CTRL[1] as firmware does".
  - Contract §5.1, Ownership: `own` is 1 from reset until the restore's terminal. §8.1 step 9: AECP runs only from the D3 terminal.
- **Evidence** (`receipts/parent/ax1x1gptp-harness-facts.txt`; derived, not executed):
  - The code facts above.
  - The processor's hold from reset, graded at this head by D3O1 (my D3 run, 133/133).
  - The manager's bank at `cbbb5acc` measured the same mechanism in the sibling harness `sim_gptp.cpp`: GET_AVB_INFO and GET_AS_PATH unanswered, 93/179, bisected to `66267d9` (5880274287).
  - The survey in the same receipt: every other parent harness that builds the processor and speaks AECP either starts the walk, or is edited by `parent_edits.py`.
  - I did not run `milan_dp_gptp`. It is a physical gPTP suite with a 5,400 s budget, outside what this review may run.
- **Impact:**
  - A pin-adoption lane working from the list gets a green consumer set (15/15, as the author measured).
  - Once the pin moves, dev's nightly physical gPTP suite fails: its AECP commands are held for ever, because nothing ever writes PP_CTRL[1].
  - The list's framing ("all found by the consumer set") is accurate about where the list came from. The list is still not complete.
- **Required outcome:**
  - The PR body names `sim_ax1x1gptp.cpp` (`milan_dp` `ax1x1gptp`, run by `milan_dp_gptp`, nightly) under the `PP_CTRL[1]` harness obligation. The walk starts after its image is served and before its first AECP command.
  - The body states that this harness is outside the consumer set, and whether the edit was measured.
  - This is a body edit only.
- **Verification:**
  - Compare the PR body with this finding.
  - At adoption, the manager's `milan_dp_gptp` run (nightly or manual) with the edit applied.

### Suggestions (they do not affect the verdict)

- **R390-4-S1 (Tests, RTL):**
  - **Two properties of the new arm are ungraded in the tree.** The issue-cycle arm is scoped per manager, and to READs only. Two of my mutants pass every processor suite:
    - `issue_arm_cross_intent`: the issue-cycle term takes either manager's abort;
    - `issue_arm_ignores_we`: the issue-cycle term drops the `!mX_we_i` guard.
  - **Only my unit probe kills them.** `pp_top` D3 is 133/133 and `acmp_nvm` 355/355; my arbiter unit probe kills them in cases B, D, E, F and G (`receipts/r390-4-mutants-issue-drain.txt`).
  - **They are equivalent at this head.** Neither in-tree manager ever presents those input combinations. My monitor counts 0 such cycles over the whole `pp_top` suite (589 manager-0 issues, 2,923 manager-1 grants) and the whole `acmp_nvm` suite (`receipts/arb-monitor-head.txt`).
  - **Suggested action.** Add an `acmp_nvm` N-case, which drives manager 1 freely as N10 does. It would grade a WRITE granted with an abort, and a READ issued while only the other manager presents an abort. Then a future manager cannot meet an ungraded rule.
- **R390-4-S2 (Docs, Tests; for the pin-adoption lane):** Two refinements to the scratch parent edits. Neither hides a processor behaviour (§5).
  - **(a) The image-less legs' walk check should name the terminal it expects.** They now accept "either terminal", under the unchanged label "PP_STAT[2] the restore walk sequenced". The terminal they actually reach is CLOSED, with PP_STAT[2] 0: my `ax1x1` run reads `0x5b000808`, busy 0, done 0, fail 1. Asserting CLOSED keeps the check meaningful.
  - **(b) The timed `notify` leg no longer runs the `[AECP-WTMO]` arm.** The arm now follows `prove_the_shipped_descriptor_image_enumerates()`, which returns early under `NOTIFY_TIMED_TB`. My run shows 0 WTMO lines, against 2 before the edits. The body says the arm runs after the restore. That holds for the four `nxn` legs, where my `nxn` run grades it with a SUCCESS heal.
  - **(c) A lint note.** `.wr_chg_o ()` trades the PINMISSING for one PINCONNECTEMPTY: 85 warnings against the base's 84, lint rc 0.
- **R390-2-S1 (RTL, Docs), carried:** No `RX_SLOTS_P >= 2` floor is checked or stated (`protocol_processor_top.sv:86`, unchanged).

## 3. Round-4 assignment items verified

| Item | Result | Evidence |
|---|---|---|
| (1) `014e679`: the arbiter arms the drain for an abort presented with a READ strobe in the issue cycle, for either manager, without a port change. It cannot drain a READ that was not abandoned. A WRITE strobe with an abort is not cut. The D3 writer cannot present both, and N10 drives manager 1 through the case. D3R18 and my E1 show the drain, and a later SET that persists | **met** | See the item (1) detail below this table. |
| (2) `8610ab3`: D3R19–D3R21; 76/76 KILLED; one reviewer mutant against the issue-cycle drain | **met** | See the item (2) detail below this table. |
| (3) The consolidated parent-visible list is complete and sufficient; every declared parent harness edit is judged against the contract | **sufficient for the consumer set, and every edit is a legitimate consequence of the ruled D3 behaviour. Not complete: F1** | §5 |
| (4) R391-3 S1–S3 wording | **taken** | See the item (4) detail below this table. §9 holds my disposition of R391-3, written after this section. |
| (5) DR3a unchanged on earlier paths; DR4 lane 1 +1,031 LUT / +559 FF | **DR3a confirmed; DR4 declared, not re-measured** | See the item (5) detail below this table. |

**Item (1) detail.**

- **The RTL.** `KL_pp_nvm_mgr_arb.sv:157-160` adds `(iss0_w && !m0_we_i && m0_abort_i)` and `(iss1_w && !m1_we_i && m1_abort_i)` to the owned-READ terms. No port or parameter changed.
- **Same intent.** The shadow raises `nvm_abort_o` only in `H_RS_STREAM` (`KL_acmp_nvm_shadow.sv:576`). Its READ strobe is registered, is out only in the first `H_RS_STREAM` clock, and has `we` 0 (`:761-767`). In `H_RS_REQ` the deadline branch comes before the issue branch, so a failing walk issues nothing. So a manager-0 abort that meets a manager-0 issue is always the abandonment of that very READ.
- **Different intents.** Neither arm reads the other manager's abort. In an issue cycle the owner is `O_NONE`, so the owned terms are false.
- **The writer never presents both.** `m_req_o` is `W_RQ`'s in the restore and `S_REQ`'s in service. `m_abort_o` is `expire_w && (ws_r == W_RD)`, and `done_r` sends `ws_r` to `W_DONE` for good (`KL_aecp_nvm_writer.sv:1089`, `:1095`, `:666-667`, `:774-816`). The claim is true.
- **Executed, the arbiter unit probe** (`receipts/arb-unit-probe.txt`), 9 cases:
  - at the head, 9/9. The READ strobe with its own abort is drained from issue+1, for both managers (A, C);
  - a WRITE strobe or grant with an abort is not drained and completes (B, D);
  - a strobe while only the other manager aborts is served whole (E, F);
  - a tie, with the loser presenting an abort, drains nothing, and both READs are served (G);
  - the owned path is unchanged (H), and an abort alone arms nothing (I).
  - The round-3 arbiter fails A and C.
- **Executed, the monitor** (`receipts/arb-monitor-head.txt`):
  - over the full `pp_top` suite the manager-0 issue-cycle arm fires once (D3R18) and the manager-1 arm never. Over `acmp_nvm` the manager-1 arm fires once (N10);
  - there are 0 cross-intent cycles, 0 WRITE-with-abort cycles and 0 aborts with nothing owned or strobed.
- **E1 at this head** (`receipts/probe-e1-e2-head.txt`, my unchanged round-3 script):
  - **Aligned.** Strobe 1, abort 1, owner 0 on `agg_o`'s first clock. DEFAULTS at clock 1,000,004, cause 3, the READ drained for 3,005 clocks. Then the port is not idle for only 27 of 100,000 clocks, one WRITE of 0x50, the record persisted, and `d3_unflushed_o` 0.
  - **Round 3.** 100,000 of 100,000 busy, 0 WRITEs.
  - **±1 clock controls:** unchanged.
- **The in-tree checks.** D3R18's three checks pass. `drain_misses_issue_cycle` and `drain_misses_issue_cycle_m1` are KILLED.
- **The comments and rows** are corrected: the shadow at `:161-166` and `:553-558`, 07 §5.3 row `:615`, and 02 §8.2.

**Item (2) detail.**

- **The new checks.** The D3 section grows by 13 checks, which pass: D3R18 3, D3R19 4, D3R20 4, D3R21 2. My printed values equal the author's receipt: +546, +272, +1, +1, +5.
- **The in-tree campaign.** 76/76 KILLED, with every named check failing (`receipts/d3-mutants-from-tree.txt`), and README records equal (`receipts/readme-record-vs-run.txt`).
- **My earlier mutants** (`receipts/r390-3-mutants-rerun.txt`):
  - `agg_closes_during_proof` is KILLED by D3R19 inside the LOCATE (it ends CLOSED);
  - `proof_past_needs_fire` is KILLED by D3R20 in both arms (COMPLETE 2,168 clocks after the bound in `W_IMG`);
  - the other 14 fail the D3 section as before;
  - `hold_after_release` is KILLED by the full suite (W21dd2, W21ee, U11g; `receipts/mutant-hold_after_release-full-pp_top.txt`);
  - `held_gate_ignores_da` has no effect, as judged in round 2.
- **My own mutant against the issue-cycle drain.** `issue_arm_one_clock_late` registers the issue-cycle arm, so the drain starts one clock late. It is KILLED three times over:
  - by D3R18, "drained from the next clock (0, owner 1)";
  - by N10;
  - by the unit probe's cases A and C.

  Three more edits bound the rule. `issue_arm_m1_dropped` is killed only by `acmp_nvm` N10 and the unit probe, as expected. `issue_arm_cross_intent` and `issue_arm_ignores_we` are S1.
- **E2 at the head** is identical to round 3 (`probe-e1-e2-head.txt`), and D1's arms are identical (`probe-d1-head.txt`).

**Item (4) detail.**

- **The firmware wait.** `integrator.md` step 3, 07 §5.3, 08 F08.1 and the writer banner now give 1,000 ms plus two per-wait deadlines plus a few clocks, with 1,060 ms stated as a margin. This takes my R390-3-S1.
- **Checked from the code:**
  - the pre-proof path ends within one per-wait deadline, the proof's own LOCATE;
  - a roll-back after the bound adds its debt wait and its re-LOCATE, each bounded by one;
  - the drain does not delay the writer's terminal (E1: DEFAULTS at +4 while the drain runs);
  - the parent's `MILAN_NVM_RESTORE_TIMEOUT_MS` is 3,000 (`scripts/nvm_shape.py:160`).
- **The terminal tables.**
  - The integrator's `NVM_RS_AGG_CYC_P` row names both roll-back CLOSED cases.
  - 07 §5.3 gains the image-proof LOCATE's own per-wait deadline: CLOSED, cause 3, no roll-back. That agrees with contract §6.2 ("any restore wait … ABORT (cause 3)"; "ABORT before the image was proven → CLOSED"). The guides call it reachable only by misconfiguration.
  - The integrator's `NVM_RS_TMO_CYC_P` row does require sizing above the image walk. A silent descriptor memory is answered first by the store's own watchdog, cause 7 (DR3a "descriptor memory silent": 8,188 clocks, cause 7).
- **The banner.** `KL_acmp_nvm_shadow`'s banner states the direct instantiator's derivation of both clock-referenced parameters. Only comments changed in that file.

**Item (5) detail.**

- **DR3a.** The `--dr3a` output is identical to round 3 (`receipts/dr3a-head.txt`), so every earlier path is unchanged. The new paths' offsets, +4 (E1), +546/+272, +1 and +5, are all within one per-wait deadline of the bound.
- **DR4.** It is declared as +1,031 LUT / +559 FF / 0 BRAM / 0 DSP, round 4 adding +1 LUT, inside the 2,500/1,400 ceiling. I did not re-measure it.
- **A diagnostic only.** An out-of-context synthesis of the arbiter alone with the host's own synthesiser, not the DR4 instrument (`receipts/arb-yosys-diagnostic.txt`): the same 4 flip-flops, and 52 LUTs at `cbbb5acc` against 47 at the head. That is mapping variation, and consistent with a negligible change.

## 4. My earlier findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R390-3-F1 (MAJOR, the issue-cycle abort lost, the port wedged) | **RESOLVED** | The arbiter fix as ruled; E1 aligned drains and persists; D3R18 and N10 kill the round-3 arbiter; my `issue_arm_one_clock_late` is KILLED; comments, 07 and 02 are true (§3 item 1) |
| R390-3-F2 (MINOR, the pre-proof edges ungraded) | **RESOLVED** | `agg_closes_during_proof` KILLED by D3R19; `proof_past_needs_fire` KILLED by D3R20, both arms |
| R390-3-F3 (MINOR, the pin-adoption list incomplete, the B1–B4 attribution inexact) | **RESOLVED** | The body names `wr_chg_o`, the derived `RETRY_BACKOFF_CYC_P`, the 2,000 ms window, the measured attribution and the PP_CTRL[1] harness and firmware items. The 308/311/315 figures match my round-3 experiments A and B and my runs at `eaa88a32` (§5). F1 is a new, separate omission. |
| R390-3-S1 (firmware wait wording) | **TAKEN** | §3 item (4) |
| R390-3-S2 (a bound inside a healthy re-LOCATE ends CLOSED) | **stated; the ruling is open** | The integrator row and 07 state it ("the bound falls inside a roll-back another fault had started"). The round-4 assignment does not rule it: §8 |
| R390-2-S1 (RX_SLOTS_P floor) | **not taken**; carried | unchanged |
| R390-2-F1…F3, S2; R390-1-F1…F4, S1, S2 | **still RESOLVED/TAKEN** | The round-1/2 probe output is identical to round 3 (`receipts/probes-r2-head.txt`). The earlier mutants are still KILLED (§3 item 2). |

## 5. Item (3): the declared parent edits, judged one by one

**How I checked them.**
- **Scratch parents.** Two scratch parents from dev `eaa88a32`, each with `protocol-processor` at this head and `gptp-processor` and `verilog-axis` at their gitlinks. `scripts/mk_scratch_parent.sh` builds them; they are never committed.
- **The edits apply unchanged.** No consumer-set file changed between `b5c0f69d` and `eaa88a32`. The author's `parent_edits.py` applies cleanly to the second tree, and the result is identical in body to the author's `parent-edits.diff`: 11 files (`receipts/parent/parent-edits-applied-at-eaa88a32.diff`).

| Declared edit | Legitimate consequence? | Why, and what I executed |
|---|---|---|
| `KL_pp_shadow.sv`: the five round-1 ports; `d3_unflushed_o` into `pend` | **yes** | §5.1 Exports and §5.2 (the final `pend_i` composition is staged per §10; the scratch keeps the old terms, which is lane 2's to finish) |
| `nvm_cosim` `cosim_top.sv`: `rs_agg_i` 0, `wr_chg_o`, `RETRY_BACKOFF_CYC_P` and `RS_TMO_CYC_P` derived from its clock | **yes** | §5.1: "Lane 1 derives both producers' backoff from the top's `CLK_HZ_P`"; the S3 banner. Lint rc 0, 0 PINMISSING, 85 warnings (S2c) |
| `nvm_cosim` B1–B4 give-up window 1,500 → 2,000 ms | **yes** | The ruling (5880658258): no write is lost, and a SET lost to a cut in the backoff is admitted when reported (§7.1, K18). The case's premise needs the window past the debounce and both backoffs. **Measured:** 308/315 with the gitlink only (the same seven B checks as round 3); **315/315** with the edits (`receipts/parent/nvm_cosim-quick-eaa88a32.txt`) |
| evidence-classifier disposition for `d3_mutants.py` | **yes** | A harness classification, not a behaviour |
| `sim_gmstep.cpp`, `sim_gptp.cpp` start the walk | **yes** | §5.1 Ownership; §8.1 steps 3 and 9 (not executed by me) |
| `milan_dp_render` T8 waits one commit-to-pin bound | **yes** | The harness waits out its own documented bound. The processor only shifts the boot, by the D3 walk; this is the author's measurement, not executed by me |
| `pp_shadow` K/K10/K12 walk before the enable, M2 walk after the handover, P3 blank 0 | **yes** | §8.1 order; §5.2 H8, "restore blank reads 1 only for a restore that did not fail" (not executed by me) |
| **Image-less legs (main, nolpf, ax1x1, aclk) accept the CLOSED terminal** | **yes** | §6.2: an image that cannot be proven ends CLOSED, cause 7. §8.1 step 6, and "A CLOSED terminal holds AECP and the enable until a reset, and does not take the listener's faces back". These legs start the walk only to release the listener for ACMP binding; they report ADP cadence and do not assert it (`sim_main.cpp:378`). **Executed** `ax1x1` (`receipts/parent/milan_dp-legs-eaa88a32.txt`): PP_STAT `0x5b000808` (CLOSED) in both trees; gitlink only 1/231 failing, the walk check alone; with the edit 231/231. The other 230 checks pass identically, so nothing else rests on the terminal |
| **`sim_nxn.cpp` legs start the walk once the descriptor memory answers; the no-image case graded as held; the wedged-response arm after the restore** | **yes** | §8.1 steps 2–3 (the image before `PP_CTRL[1]`), §5.1 Ownership, and the hold-admission ruling (5873580386). The retired arm, "READ_DESCRIPTOR with no descriptor memory answers BAD_ARGUMENTS", grades a boot the contract now ends CLOSED with AECP held (§5.3 item 1). **Executed:** `notify` 210/310 failing with the gitlink only, 372/372 with the edits (hold and release-answer checks pass); `nxn` 1,841/1,841 with the edits, WTMO graded with a SUCCESS heal. S2b notes the timed leg's lost WTMO arm |

**Conclusion.**
- **No behaviour change outside the contract.** No declared edit hides a processor behaviour change that §6.2 or §8.1 disallows. Each one moves a harness to the contract's boot order, or regrades a behaviour the contract retires.
- **Sufficient for the consumer set.** The list is sufficient for the manager's consumer set, as measured by the author (15/15). I reproduced 4 of its legs in part.
- **Not complete.** The list is missing one harness outside that set (F1).
- **Firmware.** The persistence-disabled boot path is declared, and not exercised by any gate (§5.3 item 2 of the contract).
- **The parent's offline AECP model features** pass at this pin (87 scenarios).

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The ruling 5880658258; contract §§5.1–5.3, 6.2, 6.4, 7, 8.1; the arbiter's issue-cycle arm against §5 rule 5 and §6.4; both managers' strobe and abort sources; the pre-proof terminals against the clarification; each declared parent edit against §§5.2, 6.2, 8.1 | R390-4 | `84572585ea76214c9f15f199590b8fc91f8c7edc` |
| RTL | CLEAN | Every RTL hunk: arbiter `arm0_w`/`arm1_w` and drain; shadow and writer comments; the drivers of the new arm in the shadow and writer; `lint_hdl.sh` 41/41 | R390-4 | `84572585ea76214c9f15f199590b8fc91f8c7edc` |
| Robustness | CLEAN | E1 aligned with ±1 controls; E2; D1; the round-1/2 probes; the 9-case arbiter unit probe (head and round-3 arbiter); the arbiter monitor over full `pp_top` and `acmp_nvm`; `nvm_cosim` with and without the edits | R390-4 | `84572585ea76214c9f15f199590b8fc91f8c7edc` |
| Tests | CLEAN (S1 only) | Full `tb/pp_top` 7,888 (D3 133); 8 focused suites; in-tree driver 76/76 with README equality; 18 earlier and 4 new reviewer mutants; D3R18–D3R21 and N10 read and run | R390-4 | `84572585ea76214c9f15f199590b8fc91f8c7edc` |
| Docs | UNCLEAN (F1) | 02, 07, 08, 09 and both guide diffs; shadow, writer and arbiter banners; suite READMEs; PR body round-4 section and the consolidated list against every processor-building parent harness at `eaa88a32`; `links`/`matrix`/`modmatrix`/`params`/`stale` gates | R390-4 | `84572585ea76214c9f15f199590b8fc91f8c7edc` |

## 7. Real limits of this review

- **Tooling.**
  - The requested simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used the same pinned Verilator 5.050 image as in rounds 2 and 3 (hashes in `receipts/tool-identity.txt`).
  - The host's newer system simulator was not used. Parent runs had the pinned binary first on `PATH`.
- **Hosted checks.** At 03:23Z all six check runs at this head had completed with success: `docs-gates`, `portability` and `suites`, in both the push run 36512813594 and the pull-request run 36512816353. All six executed, and none was skipped. The combined commit status has no contexts. Hosted acceptance is the manager's (`receipts/hosted-checks-snapshot.txt`).
- **Parent runs.** Only focused runs in scratch parents:
  - `nvm_cosim` quick and lint, with and without the edits;
  - `milan_dp` `ax1x1`, with and without; `notify`, with and without; `nxn`, with the edits;
  - the two offline AECP feature files.
  - **Not run by me:** `pp_shadow`, the full `milan_dp` sweep and its mutation campaigns, `milan_dp_render`, `gmstep`/`gptp`, xvlog, the classifier, and the parent's port-contract and naming gates. Those gates refuse a tree without real submodules; I re-counted the port-contract and naming ratchets with the parent's own parsers instead: 111 ≤ 111 undocumented, and 0 new naming identities (`receipts/port-doc-count.txt`, `receipts/naming-check.txt`).
  - `milan_dp_gptp` (F1) is derived, not executed.
- **Processor runs not made:** the full 33-suite bank, Yosys/OOC for DR4, and `make check`'s `lint`/`wavedrom-check`.
- **Probe models.**
  - E1, E2 and D1 add knobs and taps to disposable bench copies. The arbiter unit probe models the port as idle in the clock after its done pulse, as the arbiter's banner states.
  - The monitor only counts; the arbiter's logic is unchanged.
  - The `ax1x1` print of PP_STAT is a scratch-only harness line.
- **No hardware.** No hardware or physical calibration was used (NOT RUN). Field skips are not hardware proof.

## 8. Pending manager duties

- **Merge-turn builds.** The donor full bank and the parent consumer bank at dev `eaa88a32`, and the final current-dev candidate (source base `c951a9ff`, live dev `eaa88a32`), are built at the merge turn. When I checked, no manager bank comment at this head was public.
- **Evidence.** Publishing exact-head evidence.
- **Rulings:**
  - On R390-3-S2 (a bound inside a healthy re-LOCATE ends CLOSED with the pass-1 cause).
  - Recording in the parent contract that the §6.4 `drain'` equation now has the issue-cycle term the round-4 ruling directed. The printed equation lacks it.
- **Lane 2 (pin adoption):**
  - F1's harness;
  - S2's refinements;
  - the firmware persistence-disabled path with a host test;
  - the combined restore status and the §5.2 `REGISTER_MAP.md` rows;
  - DR4 post-place, and the 8x8 obligation (open, not waived);
  - a `milan_dp_gptp` run after the pin moves.

## 9. Prior public findings of the other reviewer, resolved or retained at this head

I read R391-3 (5880412380) only after §§2–6 were written. It changed no finding and no ledger entry.

My F1 is a different omission from R391-3 F1: a harness outside the consumer set, not the `nvm_cosim` bindings. For R391-1 and R391-2 I rely on my round-3 disposition. This round's reruns keep every mutant tied to them KILLED (§3 item 2).

| Finding | Status at this head | Evidence (mine) |
|---|---|---|
| R391-3 F1 (MINOR, the list omits the `nvm_cosim` backoff binding and misattributes the 7/315) | **RESOLVED** | The body names `.rs_agg_i (1'b0)`, `.wr_chg_o ()`, `RETRY_BACKOFF_CYC_P` and `RS_TMO_CYC_P` derived as the top derives them, and the B1–B4 window (2,000 ms). The attribution is as measured. At dev `eaa88a32`: 308/315 with the gitlink only, 315/315 with the edits (§5). |
| R391-3 F2 (MINOR, three pre-proof variants unguarded) | **RESOLVED** | D3R19 (the image proven by the writer's LOCATE after the bound, and the bound inside that LOCATE), D3R20 (the proof on the bound's clock in `W_IMG` and in `W_IMGLOC` with the answer in hand) and D3R21 (a binding byte in hand at the expiry) pass. The in-tree `proof_default_only_from_img`, `proof_past_bound_needs_fired` and `agg_o_pulse` carry that reviewer's described edits, and are KILLED in my run. |
| R391-3 S1 (the firmware wait, plus a few clocks) | **TAKEN** | §3 item (4) |
| R391-3 S2 (two terminal-table wording points) | **TAKEN** | The integrator row now reads "inside a roll-back another fault had started, or if the roll-back the bound started cannot prove the image again". 07 §5.3 has the image-proof per-wait row (CLOSED, cause 3, no roll-back), consistent with contract §6.2. |
| R391-3 S3 (the binding manager's backoff default) | **TAKEN** (comment only, as ruled) | `KL_acmp_nvm_shadow.sv:38-46`, `:145-146` |
| R391-2 F1, F2, S1; R391-1 F1–F4, S1 | **still RESOLVED/TAKEN** | `agg_not_stopped_at_terminal`, `agg_fires_with_event_in_hand`, `resident_never_returned`, `no_aggregate_deadline` and the admission and drain controls are KILLED in my 76/76 run. D1 is unchanged. Port-doc 111 ≤ 111 and naming 0 new (§7). |

## 10. Receipts and reproduction

- **Publication.** Every publishable file is listed in `MANIFEST.sha256`, with paths relative to the packet. Host paths are replaced by `<packet>`, `<scratch>`, `<clone>` and `<V>`.
- **Clone integrity** (`receipts/clone-integrity.txt`), after all probes:
  - HEAD and tree verified;
  - porcelain status (ignored and untracked included), `diff-index`, the worktree diff and the cached diff all empty;
  - no blob or mode differs across the 312 tracked files;
  - 0 gitlinks and no `.gitmodules`, because the repository has no submodules;
  - `ls-files -s` sha256 `ae1a96b1…29fd`.
- **Reproduce**, with `<clone>` the review clone, `<V>` the simulator, and `<copy>` a fresh `git archive` copy per run:
  - **Full suite:** `make VERILATOR=<V>` in `<copy>/tb/pp_top`, then `./obj_dir/Vpp_top_sim --dr3a`.
  - **Focused suites:** `scripts/run_focused_suites.sh <clone> <out> <V>`.
  - **In-tree driver:** from a copy, `python3 tb/pp_top/d3_mutants.py --output <dir> --verilator <V> --jobs 8 --only …`.
  - **Reviewer mutants:** `python3 scripts/r390_4_mutants.py <clone> <scratch> <V> [name …]`. The `issue_arm_*` edits also run `acmp_nvm` and the unit probe.
  - **Arbiter unit probe:** `scripts/arb_unit/run_arb_unit.sh <tree> <build> <V>`.
  - **Monitor:** `python3 scripts/instrument_arb.py <copy>`, then run the suite.
  - **E1/E2:** `scripts/run_probe_r3.sh <packet> <copy> <V>`.
  - **D1:** `scripts/run_probe_r2d.sh <packet> <copy> <V>`.
  - **Round-1/2 probes:** `scripts/run_probes.sh <packet> <copy> <V>`.
  - **Scratch parents:**
    - `scripts/mk_scratch_parent.sh <dest> <parent-clone> eaa88a32 <clone> 84572585 <gptp-clone>`, with `third_party/verilog-axis` at its gitlink;
    - `git init && git add -A` in each tree, for the suites that list files;
    - then the author's `parent_edits.py <dest>`;
    - then `make quick`/`make lint` in `tb/verilator/nvm_cosim`, and `make ax1x1`/`make notify` in `tb/verilator/milan_dp`.
  - **Ratchets:** `python3 scripts/port_doc_count.py <parent>/scripts <clone> <revs…>` and `python3 scripts/naming_check.py <parent>/scripts <clone> <revs…>`.

R390-4 FINISHED
