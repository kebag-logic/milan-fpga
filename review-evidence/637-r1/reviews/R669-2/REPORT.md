[R669] NEGATIVE - exact head 8000520cc12ec5d107a2a67f8ba3d6134b87d2b5

# R669-2: internal cleared-context review of #637 / PR #768, round 2

- Head `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5`, tree `fc876150e72e530d5c4122f04c3ec89700523b2a`. Processor pin `2cbed0a9` is unchanged from base `e9cbb676`.
- Delta judged: `63a187e1..8000520c`. That is merge commit `8a7e6beb` of dev `e26f1816` plus 8 commits (13 files, +1553/-652). The merge is a clean auto-merge: `git merge-tree --write-tree 63a187e1 e26f1816` gives tree `d6b88a1d`, which equals `8a7e6beb^{tree}`.
- Reconstructed in this order:
  - AGENTS.md and CONTRIBUTING.md (sections 3 and 6);
  - docs/README.md;
  - issue #637: the body, scheduling 6257040284, assignment 6257168886, TAKEN, REVIEW READY round 1 and round 2;
  - the round-2 assignment and rulings, PR #768 comment 6269988820;
  - D3 (`docs/design/SAVED_STATE_MATERIALIZATION.md` sections 3 rule 7, 5.2, 8.7 and 18.4), REGISTER_MAP PP_STAT, and the processor's `KL_aecp_nvm_writer.sv` frame and blank rules at the pin;
  - the diff and history;
  - the published evidence `180fc3a8:review-evidence/637-r1/author-r2`.
- I read the prior public findings (R669-1 6268811441, R670-1 6269970193) only after my own pass over the diff and my probes. Each is resolved or retained explicitly below.
- No manager source bank runs at this head, and I claim none. Source-head execution evidence is the author's published receipts plus my own focused runs below.

## Verdict basis

The round-2 work answers every round-1 finding. Specifically:

- **PP_STAT composition:** the composition is correct in the RTL (`milan_datapath.sv:5769-5773`).
- **Three-stage restore:** it restores cross-port transfers in both port orders and around a cycle.
- **Restore arms:** all six have committed checks with killing controls.
- **Gates:** they pass at the head with no ratchet file touched.
- **D3 amendment:** it states the one-pass transaction, its map-only boundary and its validation obligation.

I reproduced the following myself at the exact head:

- the three legs: dynmap 589/0, maprec8 219/0, maprec4 137/0;
- 28 docs-workflow gate commands, all rc 0, including the ones that failed at round 1;
- three committed controls, all caught.

Two MINOR findings remain open, so the verdict is NEGATIVE:

- **F1 (Tests):** three of the three terms of the new validated-record test behind PP_STAT `[7]` survive mutation. A two-case probe shows that two of them change the public blank bit, and the committed leg does not see it.
- **F2 (Docs):** REGISTER_MAP and D3 8.7 say both cause fields read 0 after a map roll-back. That is false when the binding walk failed in the same boot.

Neither needs RTL change. Both are small and are listed with their exact fix.

## Findings

### R669-2-F1 MINOR - Tests - `hdl/milan/milan_datapath.sv:5487-5488` (`amr_rs_valid_r`), `:5771-5773`; `tb/verilator/milan_dp/sim_nxn.cpp:5055-5093`, `:5391-5409` - the validated-record test that PP_STAT `[7]` blank now reads is unproven term by term

**Authority.**
- D3 section 3 rule 7 as amended, and 8.7: blank needs "neither walk validated a record, nor did the parent's map restore".
- REGISTER_MAP `[7]`: "neither walk nor the parent's map restore read a framed, crc-clean record".
- The processor's own test, which the RTL comment says it mirrors (`KL_aecp_nvm_writer.sv:549-552`, `:793-798`), counts a record as validated only when magic, layout, id, length and crc16 all hold. A frame-refused record leaves blank possible.
- AGENTS section 6, Tests: every new test can fail for the defect it claims to detect; negative and boundary behaviour is covered.

**Evidence.**
- I planted one term out of `amr_rs_valid_r`'s condition at a time: crc16, layout and id, magic and length. Each mutant builds and passes the committed dynmap leg at 589/0 (`receipts/probes.log`, `receipts/probe-valid-no-*.headleg.log`). The only committed control is "the map restore takes every record it reads for a validated one" (condition forced to 1), which first boot catches.
- The reason: every committed case that grades `blank 0` has another, whole map record in its window. The only `blank 1` case reads erased records, and those fail every term at once.
- Falsification: `scripts/r669_blank_probe.py` adds two cases to a disposable copy of the leg, each a window holding only one framed map record:
  - a payload byte changed under its old crc16;
  - a wrong record id, re-sealed.

  The clean head passes them: `PP_STAT 5b000484`, done 1, fail 0, blank 1; 602 checks, 0 failures (`receipts/blank-probe-clean.log`). The crc-term mutant then fails "probe crc-bad lone record: PP_STAT blank 1", and the id-term mutant fails "probe wrong-id lone record: PP_STAT blank 1" (`receipts/blank-probe-mutants.log`). So these mutants are not equivalent: they change the public bit, and nothing committed sees it.

**Impact.** A regression that counts a torn or foreign map record as validated ships green. PP_STAT would then read "something came back" (blank 0, fail 0) after a boot that restored nothing. This is the truthfulness of the composed status that round 2 exists to establish.

**Required outcome.** The committed `[MAPREC]` section grades PP_STAT blank 1, fail 0 and done 1 for a window whose only record is a framed map record that fails the validated test: at least one crc case and one layout-or-id case. A planted control removing each of the crc term and the layout/id term is caught. A magic/length-term control is welcome but optional. This needs no RTL change.

**Verification.** At least two new `dynmap_mutants.py` rows, each caught by its named check. The clean dynmap leg still passes, and the vacuity guard is updated if pages are added.

### R669-2-F2 MINOR - Docs - `docs/reference/REGISTER_MAP.md:2378` and the PP_STAT row `:2401` (`[3]`), `docs/design/SAVED_STATE_MATERIALIZATION.md:1499-1500` - "both cause fields then read 0" is false when the binding walk also failed

**Evidence.**
- The map restore starts on the D3 walk's COMPLETE terminal. Its gate reads only the D3 cause and roll-back (`milan_datapath.sv:5347-5348`: `pp_restore_rb_w || (pp_rs_cause_w != 3'd0)`).
- The binding walk's cause `restore_cause_o` (`KL_pp_shadow.sv:729`, `:1369`) reaches PP_STAT `[22:21]` unmasked (`milan_csr.sv:670`, `milan_datapath.sv:2845`).
- D3 8.7 makes the two walks' failures independent: "either walk failed". The binding walk fails on a torn binding record with D3 still COMPLETE.
- So a boot whose binding walk failed (cause 1 to 3) and whose map restore then rolled back reads `[3]` 1 with `[22:21]` non-zero. REGISTER_MAP says "`[20:18]` and `[22:21]` then read 0" and "with both cause fields `0`", and D3 8.7 says "both cause fields then read 0".
- The RTL comment states the safe converse (`milan_datapath.sv:5763-5765`: a fail with both causes 0 on a walk that did not run blind is the map restore's). That converse holds, because every processor abort carries a non-zero cause (`KL_aecp_nvm_writer.sv:655-667`).

**Impact.** The register contract states a value the hardware does not give in a reachable two-fault case. Firmware that attributes a fail by these fields could misread it. This changes a contract claim, so it is MINOR, not wording residue. That matches the precedent of R670-1 F5.

**Required outcome.** All three places say what holds. For example: "the map restore adds no cause of its own: `[20:18]` reads 0, since the D3 walk ended COMPLETE, and `[22:21]` keeps the binding walk's", or "a fail with both cause fields 0 on a walk that did not run blind is the map restore's".

**Verification.** A docs read against `milan_datapath.sv:5347-5348` and `milan_csr.sv:670`, and the doc gates rc 0.

### Residue (wording only, no lens left unclean; the manager carries these to the residue checklist)

New instances in the reviewed delta under the 2026-10-15 comment rule, plus two prose slips:

| ID | Artifact | Defect | Exact fix |
|---|---|---|---|
| RES-1 | `hdl/milan/milan_datapath.sv:4921-4922`, `:4926` | A source comment cites "#637 ruling, PR #768 comment 6269988820" and "(the same ruling)": an issue-comment ID in source. | `(Milan v1.2 5.3.10.1; #637, D3 18.4)` and `(#637, D3 18.4)`. |
| RES-2 | `tb/verilator/milan_dp/sim_nxn.cpp:5528-5529` | Same: "the #637 ruling, PR #768 comment 6269988820". | `(D3 18.4; Milan v1.2 5.3.10.1; #637)`. |
| RES-3 | `tb/verilator/milan_dp/dynmap_mutants.py:29`, `:35`, `:148`, `:162`, `:310`, `:339`, `:380`, `:381` | Review IDs and round labels in source comments and a mutant name: "(reviews R669-1 and R670-1)", "#637 round 2", "round 1's order", "the round-1 ordering". | Drop the review IDs and say what the arm is, e.g. "#637: PP_STAT's composition ..." and "the per-port order: a port's reset set comes down just before its saved set". |
| RES-4 | `tb/verilator/milan_dp/dynmap_mutants.py:29-38` | The docstring counts "seven ... eleven ... and the round-1 ordering", which is 19 rows. MUTATIONS rows 38 to 60 are 23. The 8x8 fail composition, the cross-port refused put-back and the last-port put-back rows are not mentioned. | State eight composition rows (seven on dynmap, one on maprec8) and fourteen value and recovery rows, or name all 23. |
| RES-5 | `hdl/milan/milan_datapath.sv:5491` | "refused before the port is touched": in the three-stage walk, stage 0 has already emptied the port. | "refused before its saved set touches the port". |

### Suggestions (optional; no lens effect)

- **S1** - `milan_datapath.sv:5380`: the stage 0 and stage 2 wait for the post-terminal sweep (`if (!amap_sweep_busy_w)`) has no check. A probe that removes the wait passes dynmap at 589/0 (`receipts/probe-no-sweep-wait.log`). The leg already exposes `amap_boot_last_r` read-write to hold the sweep open. One case that holds it across the D3 terminal and grades the RAMs after the restore would prove the wait, or would show it is redundant with the server's own wait.
- **S2** - `milan_datapath.sv:5602`: the roll-back on a refused stage-0 take-down is unexercised. A probe that lets the take-down pass on refusal survives dynmap (589/0) and maprec8 (219/0) (`receipts/probe-takedown-no-rb*.log`). The arm is defensive: the stores equal the clip while every face is held. REGISTER_MAP `[3]` and D3 8.7 still name it as a fail cause. Either plant it through a store perturbation between the terminal and stage 0, or say in 18.4 that it is defensive and unreachable while the faces are held.
- **S3** - `tb/verilator/milan_dp/Makefile:575`: `dynmap-mutants` still does not build `milan_dp_render`'s `tdm8render-build`, so the TESTING.md command fails its listener row on a clean tree. The author records this and the dev precedent, and proposes a fix. Making the target build it would make the stated command self-sufficient.

## Round-2 focus items, judged

1. **PP_STAT composition (D3 3 rule 7, 5.2):** met.
   - `busy = pp_busy || (pp_done && hold)`, `done = pp_done && !hold`, `fail = pp_fail || amr_rs_fail_r`, and `blank = pp_blank && !hold && !amr_rs_fail_r && !amr_rs_valid_r` (`:5769-5773`).
   - The validated test matches the processor's frame test: magic and length, layout and id, crc16.
   - Public-register assertions read `A_PP_STAT` over AXI (`sim_nxn.cpp:4879-4889`, mid-hold `:4837-4841`): first boot `5b000484`, saved `5b000404`, refused put-back `5b00040c` (`receipts/leg-maprec8.log`).
   - Controls caught: rows 38 to 44 and 56 (`campaign-af5eefc6.verdicts.txt`), and I reran row 41 (`receipts/spot-mutants-41-54-55.log`).
   - The component gap is F1.
2. **Three-stage restore (Milan v1.2 5.3.10.1):** met.
   - Stage 0 REMOVEs every dynamic port's clip, stage 1 ADDs well-formed saved sets and marks refused or blank ports, and stage 2 ADDs the marked ports' clips back. A refused take-down or put-back goes to AS_RB (`:5363-5401`, `:5484-5504`, `:5589-5604`).
   - maprec8 grades the following on GET_AUDIO_MAP, every key's owner and cluster in the stores, and the capture RAM against its own pre-cycle reading:
     - port 1 to port 0 (taker first);
     - port 0 to port 7 (taker last);
     - a 2 to 3 to 4 cycle.
   - The per-port-order control (row 54) is caught, and I reran it. A probe that puts back every port, marked or not, is also caught (`receipts/probe-pb-all-8.log`).
   - maprec4 covers the first and last input ports, an emptied port, and a put-back under a narrower format.
   - Faces held for 13,618 to 13,773 clocks at 8x8, as documented.
3. **Six restore arms:** met. Put-back (rows 45, 46, 57, 60), hole (47), layout (48), id (49), ranges in both directions (50), conflicting keys for input, output and across ports (51, 52, 57), and pass-0 DEFAULTS (53). Each is graded on the real restore path through a codec-framed window and a planted power cycle.
4. **D3 amendment:** met. Section 3 rule 7 carries the one-pass amendment and cites the ruling. 18.4 states the transaction, its map-only boundary, its validation obligation with deadlines and their planted controls, the status composition, and the 8x8 hold.
5. **Gates:** met at the head (my run, `receipts/gates/rc.tsv`).
   - `check_port_contracts.py` and `--selftest`, `check_cpp_idiom.py`, `measure_test_evidence.py --check`, the three other idiom gates, `docs_check`, `check_em_dash --base e26f1816` and `--base e9cbb676` plus `--selftest`, `gen_toc --check` and `--verify-anchors`, `check_doc_style`, `check_doc_paths`, `check_hygiene`, `check_todo_ownership`, `measure_fail_fast`, `measure_naming`, `check_nvm_record_space`, `check_nvm_capture`, `check_feature_status`, `check_rtl_source_lists`, `pp_srcs --check` and `lint_rtl --check`: all rc 0.
   - The renderer-dependent gates were first refused for a missing pinned renderer, then run rc 0 under the hash-pinned lock in a private venv.
   - No `*.budget` or ratchet file changed over `e9cbb676..8000520c`.
   - The literal-bound `mrec_offset_i` carries `// whole-record commands: each starts at byte 0` (`:9152`), and the gate accepts it.
6. **PP_STAT `[4]`:** met. It names "the parent map writer of records `0x60`/`0x70` (#637)", three attempts 500 ms apart, reset-sticky (`REGISTER_MAP.md:2401`).
7. **No processor register-map, top-level port or parameter change:** met. `git diff 63a187e1 8000520c -- hdl` adds or removes no port or parameter line. The gitlink is unchanged.
   - route-1x1 at `887b6bf2` (hdl and syn equal to the head): LUT +260 and FF +258 against the DR4 maps ceiling of 1,250 / 600, WNS +0.065 ns, WHS +0.036 ns, 0 routing errors (`author-r2/receipts/round2/route-ooc/`). This is the author's receipt, read and not re-run.

## Prior public findings: disposition at this head

| Finding | Disposition | Evidence |
|---|---|---|
| R669-1 F1 / R670-1 F1 (status excludes the map restore) | RESOLVED | `pp_stat_*_w` `:5769-5773`; public-register checks; rows 38-44, 56 caught. Residual component gap filed as new F1. |
| R669-1 F2 / R670-1 F3 (six arms without evidence) | RESOLVED | rows 45-53, 57, 60 caught (`campaign-af5eefc6.verdicts.txt`); the round-1 hole and put-back oracles are now committed checks. |
| R669-1 F3 (port-contract gate) | RESOLVED | `check_port_contracts.py` and `--selftest` rc 0 (`receipts/gates`). |
| R669-1 F4 / R670-1 F4 (cpp idiom, test-evidence ratchet; validation account) | RESOLVED | both rc 0 with no ratchet moved. The PR body's validation account separates executed, skipped and cancelled work. |
| R669-1 F5 / R670-1 F2 (cross-port ownership) | RESOLVED (fixed, per ruling) | three-stage walk; maprec8 both orders and the cycle; row 54 caught (rerun). |
| R669-1 F6 / R670-1 F5 (PP_STAT `[4]`) | RESOLVED | `REGISTER_MAP.md:2401`. |
| R670-1 F6 (one-pass deviation) | RESOLVED | ruling 6269988820; D3 3 rule 7 amendment; 18.4 transaction, boundary and obligation. |
| R669-1 R1 / R670-1 R1 (`check 13`) | RESOLVED | `:4938` reads `check 15`. |
| R669-1 R2 / R670-1 R2 (`lane 3`, shadow) | RESOLVED | `KL_pp_shadow.sv:966`. |
| R669-1 R3 / R670-1 R3 (`lane 3`, sim) | RESOLVED | no `(lane N)` in `sim_nxn.cpp`. |
| R669-1 S1 (attempt counted from request) | APPLIED | 18.4, one sentence. |
| R669-1 S2 (busy covers the map restore) | APPLIED | `pp_stat_busy_w`. |
| R669-1 S3 (payload-length formula in check 15) | Not assigned (ruling); stays a suggestion. | |

## Clean results by lens (same format as findings)

- `[R669] PASS Conformance - hdl/milan/milan_datapath.sv:5346-5604, :5769-5773; leg-maprec8.log, leg-maprec4.log, leg-dynmap.log - three-stage restore vs Milan v1.2 5.3.10.1 and the ruling; composition vs D3 3 rule 7, 5.2, 8.7 and the processor's frame test; issue acceptance 1-4 and the #763 empty/non-default lists (dynmap "empty"/"saved" after the power cycle). The on-board cold cycle is not claimed and not counted.`
- `[R669] PASS RTL - hdl/milan/milan_datapath.sv:5222-5223 (amr_stage_r, amr_pb_r), :5363-5401, :5484-5504, :5589-5620, :5769-5773; hdl/common/csr/milan_csr.sv:650-651 - stage counter, port mask width AMR_NR_C, reset of the new state, stage exit release (own and hold fall together), refused stage 0 or 2 to AS_RB, composition is combinational on registered levels; no port or parameter change; lint_rtl --check rc 0; route-1x1 receipt within DR4.`
- `[R669] PASS Robustness - leg-dynmap.log (first-record and later device error, silent and slow memory, D3 roll-back, D3 pass-0 abort, torn record, holes, ranges, conflicts, legal maximum), leg-maprec8.log (refused put-back rolls every port back, PP_STAT 5b00040c), leg-maprec4.log (last-port put-back under a narrower format) - failure, boundary and malformed paths end at reset sets or the saved set as specified.`
- Tests: UNCLEAN (F1). Otherwise clean: 60 controls in the committed campaign, 23 new, verdicts read and manifest-verified; rows 41, 54 and 55 reproduced; legs 589/219/137 with 0 failures reproduced; `test_sim_pool.py` 17/17.
- Docs: UNCLEAN (F2). Otherwise clean: D3 3 rule 7 and 18.4, REGISTER_MAP `[1]`, `[2]`, `[4]` and `[7]`, TESTING.md fourteen legs and 60 controls (counted against MUTATIONS: 51/5/2/1/1), the 598 to 672 clock hold (my dynmap run: 598 to 672 healthy), the 13,7xx-clock 8x8 hold, and `sw/firmware/ctrl/README.md` 165.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv` amr_fsm and pp_stat_*_w; D3 3/5.2/8.7/18.4; ruling 6269988820; issue acceptance; maprec8/maprec4/dynmap runs | R669-2 | `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5` |
| RTL | CLEAN | `milan_datapath.sv` delta, `milan_csr.sv`, `KL_pp_shadow.sv` delta; lint; port/parameter diff; route-1x1 receipt | R669-2 | `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5` |
| Robustness | CLEAN | failure, deadline, malformed and boundary cases in the three legs; refused put-back; probes S1/S2 (suggestions) | R669-2 | `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5` |
| Tests | UNCLEAN (F1) | `sim_nxn.cpp` [MAPREC] and multi-port sections; `dynmap_mutants.py`; Makefile; campaign verdicts; seven own probes and the blank probe | R669-2 | `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5` |
| Docs | UNCLEAN (F2) | D3 page delta, REGISTER_MAP delta, TESTING.md, milan_dp README, ctrl README, PR body account | R669-2 | `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5` |

## Real limits

- I re-ran no full parent, PP, gPTP, Yosys or builder bank, no xvlog, no Vivado route, no full `dynmap-mutants` campaign, and no full sweep. For those I read the author's published receipts. `author-r2/` has 541 files, all hashes verified against `MANIFEST.json` (`receipts/author-r2-manifest-verify.txt`); the evidence commit is not signature-signed.
- The author's 60-of-60 is a composite: the af5eefc6 four-job run (63 of 65; the listener leg was unbuilt) plus a row-36 rerun after the render build. Both are published and disclosed.
- No hosted check run exists at this exact head: the check-runs API returns 0 and the combined status is pending (`receipts/hosted-check-runs-8000520c.tsv`). Exact-head `verilator-suites` and `yosys-portability` evidence is therefore absent.
- The on-board cold cycle and physical calibration are NOT RUN. Desk power cycles use a zero-latency window model, and DDR latency adds to the 598 to 672 clock hold.
- At 8x8 (non-shipping) the hold exceeds the processor's 4,096-clock gather watchdog. This is documented as open with the 18.4 8x8 obligations.
- My probes ran in a disposable copy (`scratch/`, unpublished). The review clone was verified byte-exact afterwards (`receipts/clone-integrity.txt`): index equal to the HEAD tree with modes, every blob re-hashed, no skip or assume flags, gitlinks as pinned.

## Pending manager duties

- Build and validate the current-dev merge candidate against live dev `78ca9bdf104819265588726bce4322696c38b8c2` (source base `e9cbb676`; dev `e26f1816` already merged). That covers the builder and native banks, the hosted and act acceptance, and the exact-head hosted contexts once the PR head is final.
- Carry RES-1 to RES-5 to the residue checklist.
- Route F1 and F2 to the author. Re-review needs the Tests and Docs lenses only, unless the fix touches RTL.
- Track the on-board cold cycle, which this PR does not claim ("Relates to #637").

## Receipts (listed in MANIFEST.sha256)

- `receipts/leg-dynmap.log`, `leg-maprec8.log`, `leg-maprec4.log`: the clean legs at the head.
- `receipts/probes.log`, `probe-*.log`: seven fault probes on the committed legs.
- `receipts/blank-probe-clean.log`, `blank-probe-mutants.log`, `blank-probe-valid-no-*.log`: the F1 falsification.
- `receipts/spot-mutants-41-54-55.log`: three committed controls reproduced.
- `receipts/gates/`: gate logs and `rc.tsv`.
- `receipts/test_sim_pool.log`, `verilator-identity.txt`, `author-r2-manifest-verify.txt`, `hosted-check-runs-8000520c.tsv`, `clone-integrity.txt`.
- `scripts/r669_probes.py`, `scripts/r669_blank_probe.py`, `scripts/verify_manifest.py`.

R669-2 FINISHED
