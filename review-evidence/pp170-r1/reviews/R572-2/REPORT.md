[R572] POSITIVE - exact head 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54

# R572-2: independent internal delta review of processor PR #172 (issue #170, saved-state lane 3: every user name)

- **Exact head** `89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54`, tree `2949350d820ad16cda288abb624f4cea7a021e70`. Source base and merge-base `09e357fb4bf3d35c8a9deba9a787e13f74d08c83`.
- **Delta under review:** `c3864686..89464a9b`, five commits touching tests and docs only (`receipts/scope.txt`).
- **Review start:** https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/172#issuecomment-6092647026
- **Round-2 assignment:** https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/170#issuecomment-6091582915
- **Clone integrity.** The isolated detached clone was verified at exact-head bytes after every probe (`receipts/clone-integrity.txt`):
  - HEAD and tree as above, and the index tree equals the head tree;
  - 587 tracked blobs checked, 0 byte or mode mismatches;
  - 0 untracked or ignored files;
  - this repository has no gitlinks, so no submodule pins apply.
  
  Every probe ran on an extraction or local clone under the packet's `scratch/` directory.

## Verdict

**POSITIVE.** Both round-1 MINOR findings are resolved at this head, and I reproduced the evidence for each:

- **Shipping capacity** (R572-1-F2 = R573-1-F1). Every population now builds at its bound name capacity (39, 107) and then at 128. The boundary control is KILLED at `N3 saved ordinal 38` / `106`. The external reviewer's `capacity_probe.sh`, run unmodified, now fails the boundary defect in the PR's own suite.
- **Debt protection** (R572-1-F1). The new arm N9 grades descriptor-debt protection on names. `rollback_ignores_debt` is KILLED at `N9 debt names:`.

Both round-1 residues are applied. No MINOR, MAJOR or BLOCKER is open. One new RESIDUE (R572-2-R1, wording only) and three suggestions are recorded below.

No production change: RTL, the shared harness (`tb/pp_top`, `tb/common`), `syn`, `scripts`, `.github`, registers, ports, parameters and the 128-record name map are tree-identical at base, round 1 and this head.

## 1. Reconstruction

**Rules.**
- The repository has no `AGENTS.md` or `CONTRIBUTING.md` (`git ls-files` holds neither).
- The applicable conventions are in `docs/README.md`: single-source rules, plain-text citations, and the editing workflow gated by `make check`.
- Also applicable: the root `README.md` gates, and `docs/architecture/09_verification.md` §8, under which each suite README states what it proves and its mutation record.

**Frozen acceptance and scope decisions.**
- Issue #170 items 1–6, read against parent D3 `SAVED_STATE_MATERIALIZATION.md` §18 / §18.3 (milan-fpga `dev`).
- Assignment 6085041490. The tests-and-docs scope; no register, port or parameter change without a STOP.
- Ruling 6087242563. No adoption patches are needed; `parent-name-evidence.patch` is an input to the separate parent adoption lane.
- Round-2 assignment 6091582915. Bound-capacity geometry plus a boundary control, a name-valued debt arm graded on three named outcomes, both residues verbatim, and no DR4 re-measure (confirmed by design-input identity).
- Author's REVIEW READY 6092638097.

**Interfaces.**
- The parent binds `.DESC_NAME_ENTRIES_P (AEM_NAME_ENTRIES_C)` at milan-fpga `5603c353` `hdl/milan/milan_datapath.sv:8026`.
- `AEM_NAME_ENTRIES_C` is 39 and 107 in `configs/generated/endstation_ax7101_{1x1_tdm8,8x8}/gen/adp_shape_defaults.svh:31`, which I checked directly.
- The processor default stays 32 (`hdl/top/protocol_processor_top.sv:155`).

**Evidence.**
- The public tree milan-fpga `00db2c38` `review-evidence/pp170-r1` holds the author's receipts for **round 1 (`c3864686`) only**. No author receipts for `89464a9b` are published there.
- The round-2 figures in the REVIEW READY comment and the PR body are therefore checked below by my own re-execution, not against published receipts (see limits).

**Count note.** The brief and the round-2 assignment say "15 of 15". The code has 16 controls: the 14 from round 1, plus the boundary control and the debt control (`mutants.py:31-66`). The author disclosed this, and 16/16 is the arithmetically correct target. This is not a defect.

## 2. What I executed at the exact head

All runs used the pinned simulation compiler, 5.050 (`receipts/toolchain.txt`). The scripts are in `scripts/`.

| # | Run | Result | Receipts |
|---|---|---|---|
| 1 | Normal suite `run.py` (synthetic populations at 39, 107, then 128) | rc 0; 173 + 445 + 173 + 445 = **1,236/1,236 PASS** | `suite.{log,rc}` |
| 2 | Full campaign `mutants.py --jobs 8` | rc 0; golden PASS at 39 and 107; **16/16 KILLED**, each in a completed run with rc 1 and its named assertion. The boundary control fails `N3 saved ordinal 38` (39 entries) and `N3 saved ordinal 106` (107 entries). `rollback_ignores_debt` fails `N9 debt names:` | `campaign.{log,rc}`, `campaign-results.json`, `campaign-*_run.log` |
| 3 | Parent images regenerated from the head README's recipe: parent `5603c353` builder overlay, then `avdecc/gen_aemi_image.py --overlay` | 1x1: 7,512 B, `4fc8d615…b396d`; 8x8: 19,520 B, `d8296833…a7bc`. Byte-identical to the README's stated identities | `regen-images.log`, `scripts/06_regen_images.sh` |
| 4 | Generated images, functional (`--image`, bound capacity then 128) | 1x1 rc 0, **346/346**; 8x8 rc 0, **890/890** | `generated-{1x1,8x8}.*` |
| 5 | Generated images, `--measure` | At the bound capacity, worst terminal **28,714** of 1,000,001 clocks and worst D3 wait **1,908** of 20,001: exactly the author's round-2 figures. The 128 rows reproduce round 1 (29,008). Record operation 87; binding wait 12 | `generated-*-measure.*` |
| 6 | Synthetic `--measure` | At the bound capacity, worst terminal 28,694 and worst D3 wait 1,898. At 128, 28,988 | `suite-measure.*` |
| 7 | Independent boundary probes, written by me (exact edits, unmodified suite) | See §3 | `probe-*.{diff,log,rc}` |
| 8 | N9 failure-mode diagnostic: head and debt defect, 1x1 at 39, printf lines only in a scratch `sim_main.cpp` | Head: 0 entries off default, 0 GETs off default; restore done, rolled back, cause 6, debt owed 11,921 cycles. Defect: 0 entries off default, **39/39 GETs not served**; restore CLOSED (rolled back 0), owed 2 cycles | `debtdiag-{golden,mutant}.txt` |
| 9 | Round-1 external `capacity_probe.sh`, byte-identical (sha256 `a6f13785…`), unmodified | `cap39-1x1` rc 0 (346/346). `cap107-8x8` rc 0 (890/890). **`cap128-boundary-synth` rc 1**, failing N3/N5/N6/N9-SET at 38 and 106 (it was rc 0 in round 1). `cap39-boundary-1x1` rc 1 | `prior-capacity-probe.*`, `prior-probe-identity.txt` |
| 10 | Round-1 internal `debt_probe.py` (sha256 `2f4d1c60…`) | Unmodified: rc 1, `TypeError: build() missing … 'line'`. The head's `run.build()` gained a capacity argument, so this is an API change, not a test result. With the one-line adaptation (`harness.EXTRA`, the round-1 128 geometry): golden 4/4 at both shapes and both latencies; defect 0/4 at late 16,000 on both shapes, and passing at late 5,000, as in round 1 | `prior-debt-probe-*` |
| 11 | `make check` and `gen_matrix.py --check`, in a local clone | rc 0 / rc 0: 41 mermaid + 18 wavedrom blocks, 1,180 links, 562 files of IDs, matrix 94 rows with 0 untested, figures OK | `make-check.*`, `gen-matrix-check.*` |
| 12 | Existing campaign output directory | Refused before anything runs: argparse error, rc 2, nothing created | `refuse-existing-output.log` |
| 13 | Parent evidence gate (`scripts/measure_test_evidence.py --check`) in a disposable, never-committed parent `5603c353`, with the processor gitlink staged at this head and both submodules initialised at their pins | Without the adoption patch: rc 1, `protocol-processor/tb/name_state/mutants.py: UNEXPLAINED`. With `parent-name-evidence.patch` (sha256 `2ec42e1f…`): rc 0, ratchet PASS (71 ≤ 77, 0 ≤ 0 unexplained readers) | `parent-evidence-gate-*` |

**Process note.** My first launch of runs 1 and 2 started two copies of each into the same work directories. The colliding builds failed with a precompiled-header error. I discarded those attempts and killed only my own processes. Every receipt above comes from a single clean re-run.

## 3. Reviewer-owned probes (independent of the author's controls)

Each probe is one exact edit in a pristine extraction, run through the unmodified `run.py` (bound capacity, then 128):

| Probe | Edit | 39 / 107 entries | 128 entries |
|---|---|---|---|
| `writer_last_entry` (the boundary control's edit, run through the normal suite) | `KL_aecp_nvm_writer.sv:1006` `< N_NAME_P` → `< N_NAME_P - 1` | FAIL `N3 saved ordinal 38` / `106`, plus N5 at the same ordinal, N6 and N9 SET | PASS 173 / 445 (survives) |
| `replay_last_record` (replay side, not in the campaign) | `KL_aecp_nvm_writer.sv:854` `N_REC_C - 1` → `N_REC_C - 2` (the walk ends one record early) | FAIL only `N5 restored ordinal 38` / `106` | PASS (survives) |
| `store_name_count` (store side, not in the campaign) | `KL_aecp_desc_store.sv:582` `>` → `>=` (an exactly full name table is refused) | FAIL: image refused, 171 / 443 failures, starting at N0 | PASS (survives) |
| `debt_hold_dropped` (the debt control, run through the normal suite) | `KL_aecp_nvm_writer.sv:870` drops `!desc_debt_i` | FAIL N9 names, entity and SET in all four geometries | FAIL |

The bound-capacity geometry catches boundary defects on the trigger, replay and store sides that the 128-entry geometry alone cannot. This is the substance of the shipping-capacity finding, now resolved.

## 4. Prior public review findings at this head

I read these only after my own pass and notes (`scratch/`, unpublished).

| ID | Severity | Status at 89464a9b | Evidence |
|---|---|---|---|
| R572-1-F2 = R573-1-F1 (shipping capacity) | MINOR | **RESOLVED** | `run.py:31-37,63-65` builds `DESC_NAME_ENTRIES_P` = 39 / 107 first, then 128, for synthetic and generated runs alike. `mutants.py:59-66` adds `name_table_last_entry_dropped`, graded in both populations at their bound capacity. Campaign KILLED at `N3 saved ordinal 38` / `106` (runs 2, 9; §3). README:46-52 and the `09_verification.md:204` row state the geometry |
| R572-1-F1 (debt protection on names) | MINOR | **RESOLVED** | `sim_main.cpp:152-197` (N9): every name saved, a rate record seeded, AUDIO_UNIT 16,000 clocks late. Graded on every entry and GET_NAME at the image default, on READ_DESCRIPTOR serving both image ENTITY names, and on a later SET_NAME of the last ordinal saving. `mutants.py:43` grades `rollback_ignores_debt` on `N9 debt names:`; KILLED (run 2), and it also fails at 107 and 128 (§3). The round-1 probe reproduces (run 10). The diagnostic (run 8) shows the defect manifests as an unserved, CLOSED restore, not as altered store bytes (S1 below) |
| R572-1 RS1 (§8.2 registration) | RESIDUE | **RESOLVED** | Heading `:188` and intro `:191` are verbatim. The closing sentence `:233` carries this head's correct counts ("16 controls … twelve reused … four of its own"); the reviewer's text gave the round-1 counts, which are now stale, and the change is disclosed |
| R573-1-R1 (README distinctness sentence) | RESIDUE | **RESOLVED** (verbatim at README:74-77) | The prescribed sentence is still slightly inexact; see R572-2-R1 |
| R573-1-S1 / R572-1-S3 (how the images are produced) | SUGGESTION | **TAKEN** | README:38-44 recipe; I reproduced both images byte for byte (run 3) |
| R573-1-S2 / R572-1-S4 (existing output directory) | SUGGESTION | **TAKEN** | `mutants.py:126-127`; run 12 |
| R573-1-S3 (prefix grading) | SUGGESTION | **TAKEN** | `mutants.py:99-102` `(?!\d)`; e.g. `name_empty_refused` is graded on `N5 restored ordinal 2` exactly |
| R572-1-S1 (`d3_unflushed_o` name check), R572-1-S2 (an injective value pattern), R572-1-S5 = R573-1-S4 (`--measure` asserts nothing), R572-1-S6 (compliance-matrix citations) | SUGGESTION | **RETAINED** (optional, not taken) | No change at this head. S2 is now documented, not fixed |

## 5. Findings

No MINOR, MAJOR or BLOCKER finding is open.

### R572-2-R1 (RESIDUE): the prescribed distinctness sentence overstates the 8x8 repetition

- **Lens:** Docs.
- **Where:** `tb/name_state/README.md:74-77`, "…so in the 8x8 diagnostic ordinals 90–106 repeat the values of ordinals 0–16, and only each saved frame's record ID and CRC distinguish them."
- **Evidence:**
  - `sim_main.cpp:24-25` gives ordinals with `ordinal % 7 == 2` an empty name.
  - Of the 17 pairs (n, n + 90), five pair a full-length name with an empty one: 92, 93, 99, 100 and 106 (ordinals 2, 9 and 16 are empty, and so are 93 and 100).
  - Only twelve pairs actually repeat, the same count the round-1 external report itself recorded.
  - No test, figure, verdict or claim changes.
- **Impact:** a reader could take ordinal 92 to hold ordinal 2's (empty) value.
- **Exact fix:** replace "ordinals 90–106 repeat the values of ordinals 0–16" with "the full-length value at each ordinal n from 90 to 106 repeats that of ordinal n − 90 whenever both are full-length (twelve pairs; 92, 93, 99, 100 and 106 pair a full-length name with an empty one)".
- **Verification:** reading the text against `sim_main.cpp:24-25`.

### Suggestions (do not affect the verdict)

- **S1 (Tests, Robustness).** N9 names its observable but not its failure mode.
  - With debt protection removed, the store's entries stay at the image defaults, and the restore ends CLOSED with every GET_NAME unserved (`debtdiag-mutant.txt`). N9 still fails its named name assertion, which is what §18.3 requires.
  - `sim_main.cpp:153-159` describes the golden path as "the image proves again", but N9 never asserts the restore outcome. The round-1 probe did, with `b.done >= 0 && restore_rb_o`.
  - Adding that as a named N9 premise would state why the names fail.
- **S2 (Docs).** README:110-114 says N9 "grades that protection on name values". "On the names a controller reads (GET_NAME, READ_DESCRIPTOR) and on a later SET_NAME" would match the observed mechanism exactly.
- **S3 (Robustness).** The retained round-1 suggestions in §4 stand: `--measure` CHECKs against `RS_TMO` / `AGG`, and a value pattern injective over 128 ordinals.

## 6. Lens notes

**Conformance (CLEAN).**
- **Items 1–2.** Every generated ordinal (39 / 107) is exercised, at the parent's bound capacity, where the last ordinal is the table's last entry. This covers both ENTITY names, CONTROL with IDENTIFY volatile (N8), and empty and full 64-byte values.
- **Item 3.** Lane 1's debt protection is now graded on names (N9). Roll-back is graded by D3N5, and pending ownership by N6.
- **Item 4.** Real SET_NAME / GET_NAME on generated images, at bound capacity.
- **Item 5.** All §18.3 controls map to the 16 KILLED controls, including both halves of "omit descriptor rollback or debt protection" (`store_not_rolled_back` → D3N5; `rollback_ignores_debt` → N9).
- **Item 6.**
  - DR3a: re-measured at bound capacity, within 20,001 per wait and 1,000,001 aggregate.
  - DR4: not re-measured, by ruling. The `hdl`, `syn` and `scripts` trees are identical, so the processor's design inputs are unchanged.
  - The 8x8 post-place obligation stays open and blocked.
- **Outside items 1–6.** The §18.3 physical cold-cycle of all writable names; the PR states it keeps its separate acceptance.

**RTL (CLEAN).**
- No RTL change (`receipts/scope.txt`).
- I examined the bounds the new geometry exercises: writer trigger `:1006`, pass end `W_NEXT` `:853-866`, roll-back debt wait `W_RB` `:867-871` and `stall_w` `:599`, store name-count check `:582`, and the store and writer capacity parameter chain `protocol_processor_top.sv:3796` → `KL_aecp_engine.sv:2006`.
- The parent binding was checked at `5603c353`. No defect found.

**Robustness (CLEAN).**
- Boundary defects on three sides fail only at the bound capacity (§3).
- The debt defect fails in all geometries and on the generated 1x1 image (`generated-1x1-debt`).
- A crash, build failure or missing tally still never counts as a kill (`mutants.py:88-89,101-102`; `run.py:89-95`). An existing output directory is refused cleanly.
- S1 records N9's failure mode.

**Tests (CLEAN).**
- 1,236/1,236; golden plus 16/16 KILLED; generated 346/346 and 890/890.
- Prior probes reproduced. Four reviewer probes behave as predicted.

**Docs (CLEAN, RESIDUE R572-2-R1).**
- README check counts (173 / 445; 1,236; 346 / 890), geometry, recipe and image identities, N9 description, control table and campaign text all match the code and my runs.
- The 09 row `:204` and §8.2 `:188,191,233` are accurate. `make check` passes.
- The PR body's figures match my runs, except the full processor-bank and parent-gate totals, which I did not rerun.

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #170 items 1–6; D3 §18 / §18.3; assignment, ruling and round-2 assignment; parent binding `milan_datapath.sv:8026` and `adp_shape_defaults.svh:31` at `5603c353`; N1–N9 and D3N5–D3N7 at bound capacity; DR3a re-measured; DR4 design-input identity | R572-2 (delta; earlier rounds stand for unchanged files) | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |
| RTL | CLEAN | scope proof (hdl, syn, scripts, .github, tb/pp_top, tb/common identical at base, r1 and head); writer `:599,:853-871,:1006`; store `:582`; parameter chain top → engine → writer; parent binding | R572-2 | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |
| Robustness | CLEAN | three boundary probes and the debt probe in four geometries; N9 failure-mode diagnostic; generated-image debt run; harness refusal and kill grading | R572-2 | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |
| Tests | CLEAN | `tb/name_state/{run.py,mutants.py,sim_main.cpp,README.md}` delta; normal suite; 16-control campaign; generated functional and measure; prior capacity and debt probes; reviewer probes | R572-2 | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |
| Docs | CLEAN (RESIDUE R572-2-R1) | `tb/name_state/README.md`; `09_verification.md` §8.2 and row 204; PR body; REVIEW READY comment; `make check`; matrix check | R572-2 | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |

## 8. Real limits

- **Not rerun by me** (not permitted, or out of scope by ruling): the full processor bank, `lint_hdl.sh` and the portable synthesis flow; the full parent consumer banks (17 gates), except the single evidence-classification gate; vendor OOC synthesis (DR4).
  - These rest on the author's round-2 statements, which have **no published receipts at this head** (the public evidence tree is round 1).
  - Production RTL and the shared harness are tree-identical to the base, so lint, synthesis and DR4 inputs are unchanged by construction. The suite-bank total (1,028,293 + 1,236 = 1,029,529) is arithmetically consistent with my 1,236.
- **DR3a figures** are simulation-model clocks, not a hardware service guarantee.
- **Physical calibration and cold-cycle:** NOT RUN. Nothing here is hardware proof.
- **Hosted CI at the exact head** (snapshot 2026-10-10T02:44Z, `receipts/hosted-ci-snapshot.txt`): `docs-gates` and `portability` completed with success on both runs (38016526950, 38016528989); `suites` was **still in progress** on both, so it has no conclusion yet.
- **No manager source bank** runs at this exact head, and I claim or infer none. The merge-turn current-dev candidate (source base `09e357fb`, live dev `aef7ac66`) was not built.
- **Shared harness.** My probes use the suite's own harness and build path, so a defect common to the harness and the RTL would be invisible to both.
- **Clause wording.** The IEEE and Milan subclause wording was not checked against the (non-distributed) texts.

## 9. Pending manager duties

- Hosted acceptance at the exact head, including the two `suites` contexts still in progress.
- Publish, or link, the author's round-2 gate receipts for `89464a9b`: processor gates, parent consumer gates, the campaign and the design-input digest.
- Build the current-dev merge candidate at the merge turn (builder and native banks) and link its receipts.
- Carry RESIDUE R572-2-R1 to the residue checklist.
- Route `parent-name-evidence.patch` into the parent adoption lane, which also owns §18.3's parent obligations: the name-pending transfer and the targeted cold-cycle of all writable names. At this head the patch's disposition wording does not mention the boundary and debt controls; the parent lane may broaden it.
- The separate acceptance of physical cold-cycle and lane 5; the 8x8 post-place obligation (open, blocked).

R572-2 FINISHED
