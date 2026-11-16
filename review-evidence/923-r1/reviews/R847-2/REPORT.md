[R847] POSITIVE - exact head d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b

# R847-2: internal cleared-context delta review of PR #931 (issues #923 and #924), round 3

- Head under review: `d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b`, tree `c6c0397815848b804297d8fe001d88e722b35f49`. It matches the PR's recorded head.
- Delta: `70c100da..d06ded5a`, four commits.
  - `88676700`: the late-reply model and its tests.
  - `08901183`: the F2 figure.
  - `63c60ad9`: the F3/R1 comment.
  - `d06ded5a`: the pick test and its plant.
- Files changed: 5 (+102 / -14).
  - `sw/firmware/ctrl/aecp/README.md`
  - `sw/firmware/ctrl/plat/README.md`
  - `sw/firmware/ctrl/test/aecp_map_mutants.py`
  - `sw/firmware/ctrl/test/test_aecp.cpp`
  - `sw/litex/ctrl_memory.py`, comment lines only
- Overall: no open BLOCKER, MAJOR or MINOR. Every named prior finding is resolved at its cause. Three new SUGGESTIONs follow; they have no lens effect.

## Reconstruction (public state only)

1. **Rules.** I read AGENTS.md sections 3 and 5-8, and the CONTRIBUTING.md review and lens rules it defers to.
2. **Issue #923.**
   - The frozen scope: the edit and the boot restore commit through the EDIT window; the edit path's cost; unit and co-simulation tests, each with a plant caught by name.
   - Acceptance: every gate rc 0 on the final head, plus the bench items.
   - Two rulings: issuecomment-6906679024 (ROM debt, (A)) and issuecomment-6923091710 (the 1x1/1if hold miss is owed to #927).
   - REVIEW READY round 3: issuecomment-6931638262.
3. **Interface authorities.**
   - `protocol-processor/hdl/aecp/KL_aecp_engine.sv:461-471`, the transaction face at gitlink `a9e84b66`. An accepted phase 1 reserves the transaction, and phases 5 and 2 must then complete without back-pressure.
   - `hdl/milan/milan_datapath.sv`:
     - `:4801-4813`, the phase verdicts;
     - `:4816`, `pp_amap_edit_wait_w = amap_boot_busy_w`;
     - `:5027`, boot busy is the sweep or the restore hold;
     - `:10052-10061`, in the split the control face drives the phases and sees that same wait.
4. **Delta and history.** I read the diff, and ran `git diff 16ba667d..d06ded5a --stat` for context.
5. **Author packet.** `review-evidence/923-r1/author-r3` at archive `43bf7e3e`.
6. **Prior findings.** I read R847-1 (issuecomment-6929792570) and R848-1 (issuecomment-6928957357) only after my own pass over the delta.

## Focus items, checked

### (1) R848-1 F1: the late-reply model writes before it silences the reply

- **The model.** `Far::edit` (`test_aecp.cpp:3985-3987`):
  - Silence on phase 5 or 2 now records the beat and applies it (`verdict=0`), and only the reply is SILENT.
  - Silence on phases 0, 4 and 1 still returns before anything is taken.
  - This matches the engine's point of no return (`KL_aecp_engine.sv:465-468`). It also matches the datapath's only edit wait, the boot sweep (`milan_datapath.sv:4816`, `:5027`), which the face waits out before its begin.
- **Agreement asserted.** Store and GET_AUDIO_MAP agreement (`agree(14)`, `test_aecp.cpp:4119`) is checked after every late-reply case:
  - `AnUnansweredEditFailsUntilItsCommitIsReserved` (`:4346`), after its phase-5 and phase-2 cases;
  - `ALostReplyAfterTheReservedCommitLeavesTheStoreAndTheMapAgreeing` (`:4377`): ADD and REMOVE, the reply of record 1 and then of record 0 lost;
  - `ALostReplyInTheRestoresCommitLeavesTheStoreAndTheMapAgreeing` (`:4417`): the restore's removal of the reset set, and its addition of a restored set, each record's reply lost in turn.
  - Each case also asserts the answer or the restored count, and that the lost reply was counted.
- **No test was weakened.** The only change to an existing assertion line adds `agree(14)`.
- **The plant.** `window-lost-reply-stops-the-commit` (`aecp_map_mutants.py:333`) is caught by name by both new late-reply tests. My own re-plant shows the same (`receipts/probes.jsonl`).
- **The control: round 2's model.**
  - I replaced the three reserved-phase lines with `if(verdict==2u){*reply=MBX_MODEL_SILENT;return 0;}`.
  - All three late-reply tests then fail on "GET_AUDIO_MAP and the datapath's store hold the same mappings" (probe `old-model-drops-the-write`).
  - This agrees with the author's `tests/old-model-control.txt`.
- **The README** (`sw/firmware/ctrl/aecp/README.md:185-191`):
  - It states the guarantee: a commit or finish with no answer was taken, the face counts it and goes on, and the edit stands in both the store and the map.
  - It states "Delivery loss after the commit-begin is outside that contract and has no recovery here".
  - It invents no rollback, and `aecp_face.c` is unchanged.
- **Extra probe.** `lost-commit-reply-answers-misbehaving`: a face that answers ENTITY_MISBEHAVING after a lost commit reply, although the store took every write. It is caught by "the reserved edit answers SUCCESS", and the existing unanswered-edit test also fails. So the SUCCESS assertions guard the guarantee from the other side too.
- **Resolved.**

### (2) R847-1 F1: the face's `pick`

- **The test.** `Face.AnEditCommitsTheMappingsTheCorePicksAndNoOthers` (`test_aecp.cpp:4396`) runs through the real face and the EDIT window model.
  - An ADD of {held, fresh}: the validated and committed records are exactly {fresh}, and COUNT is 1.
  - A REMOVE of {held, held, fresh}: the validated and committed records are exactly {held, fresh}, and COUNT is 2.
  - `agree(14)` runs after each.
- **The plant.** `window-pick-ignored` (`aecp_map_mutants.py:339`) is the same replacement as R847-1's probe. It is caught by name: "the records the core picked are committed".
- **My own probes:**
  - `window-pick-ignored`: caught.
  - `validate-pick-ignored`: only the validation pass ignores `pick`. Caught by "the records the core picked are validated".
  - The unplanted control: green.
- **The original probe script.** The author's `plants/r847-probe-face-pick-ignored.txt` records R847-1's `--only face-pick-ignored`: rc 1 with only the new test failing, and the control at rc 0. I did not rerun that script. My re-plant uses the identical replacement.
- **Resolved.**

### (3) F2 and F3/R1

- **F2.** `sw/firmware/ctrl/plat/README.md:111` now reads "1,280 B of `rom` past what 56.0 held".
  - The arithmetic holds: 2,168 B were added and 888 B were spare at 56.0 (`docs/design/SPLIT_CONTROL_MEMORY.md:567`), and 2,168 − 888 = 1,280 B.
  - It matches section 5's `:286` ("1,280 B of `rom`") and the same README's `:135`.
  - **Resolved.**
- **F3/R1.** `sw/litex/ctrl_memory.py:243-244` now reads "debt owed to the cold-code-to-flash work ... until that work lands (#923's ruling of 2026-11-16)". The block above it already names "hybrid XIP work (#665 decision D3)".
  - All 12 changed lines in that file are `#:` comment lines: no non-comment line changed (`receipts/head-integrity.txt`).
  - **Resolved.**

### (4) No compiled source changed

- The delta does not touch `hdl/`, `tb/`, `protocol-processor`, any gitlink, or any `sw/firmware/ctrl/aecp/` source other than its README (`receipts/head-integrity.txt`).
- `test_aecp.cpp` and `aecp_map_mutants.py` are host-only.
- This structurally supports the author's identity receipt (`images/IDENTITY.txt`). In it:
  - `ctrl_app.elf` is identical at 70c100da, d06ded5a and the routed images: 1x1/1if `caec0abc…`, 8x8/1if `59b9b736…`.
  - The release `bios.bin` is identical at both configs.
- So round 2's routes, CPU budget and sweep carry. The 1x1/1if hold miss of +0.014 ns is owed to #927 under the floor of #818 (#665 issuecomment-6930885185). That is known, and a pass.

### (5) Gates

- **Hash check.** Every row of the packet's `receipts/INDEX.md` matches the re-hashed file: 14 of 14 (`receipts/packet-verify.txt`).
- **Not signed.** The archive commit carries no signature (`%G?` = N). The packet is checked by its index hashes only.
- **Workflow table.** `workflows/verify-d06ded5a.md` reports 118 steps ran, 130 not run with a stated reason, and 0 bad. Its NOT RUN reasons are hosted-only orchestration, apt and cache steps.
- **Campaign counts.** The author reports AECP 331 of 331, SRP 421 of 421, control 716 of 716, and coverage PASS on 39 files.
  - Spot check: the AECP table has 331 rows at this head, and its own drift control `controls()` passes. That control requires every TEST in `test_aecp.cpp` to be claimed by a plant, so the 3 new tests are owned (`receipts/plant-table.txt`).
  - SRP, control and coverage inputs are untouched by the delta.
- **The AECP app arm.** My own unplanted controls ran 164 tests PASS at both 1 and 2 interfaces (`receipts/probe-logs/control-if1.log`, `control-if2.log`). That matches the author's `tests/aecp-app-if{1,2}.txt`.

## Findings

None at MINOR or above. No RESIDUE in the delta: no new source comment shows a lane label, review round, reviewer ID or comment ID.

### S1 - SUGGESTION - Docs, Conformance - `sw/firmware/ctrl/aecp/README.md:185-186`, `sw/firmware/ctrl/test/test_aecp.cpp:3955-3958` - cite the store side of the no-back-pressure guarantee

- **Evidence:** both texts attribute "each record's commit and the finish complete without back-pressure" to the release's engine (`KL_aecp_engine.sv`).
  - In the split, the engine is not on the firmware's path: `milan_datapath.sv:10052` drives the phases from `i_ctl_edit_phase`.
  - What makes a lost reply a taken write there is the datapath store's own contract. Its only edit wait is the boot busy (`:4816`, `:5027`), which the face waits out before its begin (`:10061`).
- **Impact:** none on behaviour. The statement is true of the engine contract that the store implements. A cold reader just cannot check the guarantee in the split from the citation alone.
- **Optional outcome:** add the datapath citation, `milan_datapath.sv`, the edit face's wait, next to the engine's.

### S2 - SUGGESTION - Tests, Robustness - `sw/firmware/ctrl/test/test_aecp.cpp:4417` - the restore's lost FINISH reply is not exercised

- **Evidence:** the restore late-reply test mutes phase 5 only. The commands' phase-2 (finish) loss is covered in `AnUnansweredEditFailsUntilItsCommitIsReserved`.
- **Impact:** low. The face's finish path is shared code (`aecp_face.c:312`).
- **Optional outcome:** a restore case muting phase 2, with `agree(14)`.

### S3 - SUGGESTION - Docs - `sw/firmware/ctrl/plat/README.md:111`, `:135` - the same debt is still "owed to S14"

- **Evidence:** the line edited for F2 still names the lane. The comment rule covers source comments, not READMEs, so this is not residue.
- **Optional outcome:** for consistency with the fix at `ctrl_memory.py:243`, name the work: "owed to the cold-code-to-flash work (#665 decision D3)".

### Prior findings at this head

| Prior finding | Status at d06ded5a | Evidence |
|---|---|---|
| R848-1 F1 (MINOR, Tests and Robustness): late-reply model | RESOLVED | focus item (1); probes `old-model-drops-the-write`, `window-lost-reply-stops-the-commit`, `lost-commit-reply-answers-misbehaving` |
| R847-1 F1 (MINOR, Tests): `pick` untested | RESOLVED | focus item (2); probes `window-pick-ignored`, `validate-pick-ignored` |
| R847-1 F2 / R848-1 F2 (MINOR, Docs): 888 B | RESOLVED | `plat/README.md:111`; section 5 `:286`, `:567` |
| R847-1 R1 / R848-1 F3 (RESIDUE, Docs): lane in a comment | RESOLVED | `ctrl_memory.py:243-244` |
| R847-1 S1-S3 (SUGGESTION) | Not taken; still optional | twin-maps plant breadth, the kept() length-82 boundary, the output port on RTL |
| R847-1 S4 (SUGGESTION, Robustness): SUCCESS after a lost reply | Answered | `aecp/README.md:185-191` now states the guarantee and its limit; the model and tests hold it |

## Per-lens results

[R847] PASS Conformance - `sw/firmware/ctrl/aecp/README.md:180-195`, `test_aecp.cpp:3955-3987, 4346-4434`, against `KL_aecp_engine.sv:461-471` and `milan_datapath.sv:4801-4816, 5027, 10052-10061`
- What I checked: the stated late-reply guarantee and the model against the transaction-face contract. The answers still hold all or none, as Milan v1.2 5.4.2.27 and 5.4.2.28 require: SUCCESS once committed, nothing moved before commit-begin.
- No conformance-bearing source changed in the delta: `aecp_face.c`, `aecp_maps.c` and `aecp_commands.c` are byte-identical to 70c100da, where this lens was clean (R847-1).
- S1 only.

[R847] PASS RTL - `receipts/head-integrity.txt`, `milan_datapath.sv:4816, 5027, 10052-10061`, `KL_aecp_engine.sv:465`
- No HDL, testbench, gitlink or nested-gitlink change since 70c100da, and the images are identical by hash.
- I re-checked the RTL facts the new model depends on: phases 5 and 2 are never back-pressured after the begin, and the only wait is the boot sweep or the restore hold. The model is faithful to them.
- The routes and timing carry (#818's floor; the 1x1/1if hold owed to #927).

[R847] PASS Robustness - `test_aecp.cpp:4346-4434`, `aecp_face.c:285-314`, `receipts/probes.jsonl`
- I checked a lost commit reply and a lost finish reply on commands, and lost commit replies in the restore of both directions. In each case the store and GET_AUDIO_MAP agree.
- A silent begin, validation or commit-begin still aborts with nothing moved.
- Faces that stop committing, or that turn a taken write into an error, are both caught.
- S2 only.

[R847] PASS Tests - `test_aecp.cpp:3985-3987, 4119, 4346-4434`, `aecp_map_mutants.py:26-31, 329-343`, `receipts/probes.jsonl`, `receipts/probe-logs/*.log`, `receipts/plant-table.txt`
- Each of the 3 new tests fails for its claimed defect: 5 plants, each caught by its named words.
- The old-model control fails all three agreement checks.
- The unplanted controls pass 164 of 164 at 1 and 2 interfaces.
- The plant table has 331 rows and its drift control passes. No assertion was weakened.

[R847] PASS Docs - `sw/firmware/ctrl/aecp/README.md:180-195`, `sw/firmware/ctrl/plat/README.md:111, 135`, `sw/litex/ctrl_memory.py:236-248`, `docs/design/SPLIT_CONTROL_MEMORY.md:148, 286, 567`
- F2's figure agrees with section 5 and its arithmetic.
- The guarantee and its limit are stated.
- The ledger comment names the work and an issue, with no lane.
- S1 and S3 only.

## Probes (`scripts/r847_2_probes.py`; each runs on a fresh `git archive HEAD` copy, so the clone is never written)

| Probe | Plant | Expected | Result |
|---|---|---|---|
| control-if1 | none | 164 pass | rc 0, 164 tests, 0 failed |
| control-if2 | none | 164 pass | rc 0, 164 tests, 0 failed |
| window-lost-reply-stops-the-commit | the table's row | both late-reply tests, on the agreement words | caught, caught |
| window-pick-ignored | the table's row (R847-1's probe) | the pick test, "committed" | caught |
| validate-pick-ignored | the VALIDATE pass passes NULL `pick` | the pick test, "validated" | caught |
| lost-commit-reply-answers-misbehaving | ENTITY_MISBEHAVING after a lost commit reply | the command test, "answers SUCCESS" | caught; 3 Face tests fail |
| old-model-drops-the-write | round 2's `Far` silence | the three late-reply tests, on the agreement words | caught x3 |

All runs used the app arm with the filter `Core.*:Face.*:AppStore.*` (105 tests), except the two controls, which ran everything (`*`). Wall time: 49 s with 8 probes in parallel.

After the probes, the head is intact (`receipts/head-integrity.txt`):
- HEAD and tree are exact.
- The worktree and index are clean. The index hash is recorded.
- Every gitlink is equal to 70c100da's.
- All five checked-out submodules are at their gitlinks with 0 dirty paths.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp/README.md:180-195`, `test_aecp.cpp:3955-3987, 4346-4434`, `KL_aecp_engine.sv:461-471`, `milan_datapath.sv:4801-4816, 5027, 10052-10061`; the edit and restore source unchanged since 70c100da | R847-2 | `d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b` |
| RTL | CLEAN | `receipts/head-integrity.txt` (no HDL, testbench or gitlink delta), `milan_datapath.sv:4816, 5027, 10052-10061`, `KL_aecp_engine.sv:465`, the author's `images/IDENTITY.txt` | R847-2 | `d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b` |
| Robustness | CLEAN | `test_aecp.cpp:4346-4434`, `aecp_face.c:285-314`, probes `lost-commit-reply-answers-misbehaving` and `old-model-drops-the-write` | R847-2 | `d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b` |
| Tests | CLEAN | `test_aecp.cpp`, `aecp_map_mutants.py`, `receipts/probes.jsonl`, `receipts/probe-logs/`, `receipts/plant-table.txt`, the author's `plants/*.txt` and `tests/*.txt` | R847-2 | `d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b` |
| Docs | CLEAN | `aecp/README.md:180-195`, `plat/README.md:111, 135`, `ctrl_memory.py:236-248`, `SPLIT_CONTROL_MEMORY.md:148, 286, 567` | R847-2 | `d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b` |

## Real limits

- **No manager source bank** ran at this head. I do not claim or infer one.
- **Gate counts taken from the author.** The figures are 118 workflow steps; SRP 421 and control 716; coverage on 39 files; and the full AECP campaign of 331 rows. They come from the author's published table and README. The per-step logs are not in archive `43bf7e3e`, and I did not rerun those campaigns.
  - I did re-plant the 2 new rows plus 3 of my own.
  - I did verify the AECP table's count and its drift control.
  - The SRP and control inputs are untouched by the delta.
- **Image hashes taken from the author.** I did not rebuild the images: the hashes are the author's receipt. My support for them is structural: no compiled source or gitlink changed.
- **No signature.** The author packet is checked by its index hashes; the archive commit is not signed.
- **Hosted checks were still running.** In my snapshot (`receipts/hosted-checks-snapshot.txt`), every check run at this head was queued or in progress. No hosted conclusion is relied on.
- **No hardware.** Physical calibration and the bench acceptance items (narrowing SET_STREAM_FORMAT, the persistence scenario, the render check) were NOT RUN. Field skips are not hardware proof.
- **Model, not RTL.** The late-reply guarantee is checked against the firmware model and the RTL contract by reading. No RTL co-simulation of a lost reply exists. Delivery loss is, as stated, outside the contract.

## Pending manager duties

- Hosted and act acceptance at the exact head. When this snapshot was taken, every run was still queued or in progress.
- The current-dev merge candidate (source base `16ba667d`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`), its builder and native banks, and their receipts. Note that the PR's recorded base branch is `dev-soft-core`.
- The bench acceptance items of #923, and physical calibration.
- Maintainer merge authorization (AGENTS.md section 7).
- S1-S3 here, and R847-1 S1-S3, are optional. No residue item comes from this round.

R847-2 FINISHED
