[R573] NEGATIVE - exact head c3864686c0b254bd2d7b7f733078ec302fb9be62

# R573-1 external independent review: processor PR #172 (issue #170, saved-state lane 3, every user name)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #172, branch `pp170-names`.
- Exact head `c3864686c0b254bd2d7b7f733078ec302fb9be62`, tree `305218ec054c05ed7e023594e71642049fc790e9`.
- Source base and merge-base `09e357fb4bf3d35c8a9deba9a787e13f74d08c83`. Processor main has since moved to `336e9f36` (PR #171), which this PR does not include. The manager's merge-turn candidate (live dev `8b61b709…`) is separate and was not built here.
- Review start: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/172#issuecomment-6091093399
- Reconstruction order: repository README and `docs/README.md` (the repository has no AGENTS.md or CONTRIBUTING.md); the issue #170 body (acceptance items 1–6); the assignment (6085041490), the STOP (6087210228) and the manager's ruling (6087242563); D3 `SAVED_STATE_MATERIALIZATION.md` §18 and §18.3 at milan-fpga `dev`; the diff `09e357fb..c3864686` and its two commits; the author's published evidence at milan-fpga `00db2c38/review-evidence/pp170-r1`.
- Evidence integrity: all 39 published evidence files match the `published_sha256` values in their MANIFEST.json.

## Verdict

**NEGATIVE.** One MINOR finding is open (R573-1-F1, Tests and Robustness).

The production name path itself behaves correctly. RTL, NVM framing, registers, ports, parameters and the 128-record name allocation are byte-identical to the base. The new suite's oracle is independent, and its inventory matches both generated parent images exactly. All 14 author controls and five of my six independently written controls are killed by name-value assertions; the sixth was caught by N4 rather than the D3N7 I predicted. DR3a and DR4 are supported.

The gap is in geometry. The suite runs every population at a name capacity of 128. The parent ships with `DESC_NAME_ENTRIES_P` set to the exact generated name count (39 or 107), so in the shipping build the last ordinal is the table's last entry, and the suite never puts it there. I planted an off-by-one that drops the last table entry: it passes this PR's full suite (610/610), and the same defect fails N3/N5/N6 at ordinal 38 when the suite runs at capacity 39.

## Scope confirmation (tests only plus one verification-table row)

- `git diff --name-only 09e357fb c3864686` lists `docs/architecture/09_verification.md` (+1 row) and six new files under `tb/name_state/`: Makefile, README.md, fixture.py, mutants.py, run.py and sim_main.cpp.
- These tree objects are identical at base and head: `hdl` `4d21ab65…`, `syn` `a5e560a6…`, `scripts` `316cdbc8…`, `tb/pp_top` `4c9d4c49…`, `tb/common` `118f4454…`, the root `Makefile`, and `docs/architecture/{01_overview,02_interfaces,07_memory_maps}.md`. RTL, NVM framing, registers, ports, parameters, the shared harness and the name record map (0x80 + ordinal, 128 records) are therefore byte-identical to the base.
- The suite adapts the shared wrapper only in its own external build directory. `run.py:25-29` adds `.DESC_NAME_ENTRIES_P (128)` and widens the test-only `dbg_name_lane_i` input to 10 bits. `tb/pp_top/pp_top_wrap.sv:879` indexes `u_store.name_r` directly with that lane, so the N4 tap is valid for all 1,024 lanes.

## Lens 1: Conformance (CLEAN)

Authorities: issue #170 items 1–6; D3 §18.3; Milan v1.2 §5.3.13 (user names persist) and §5.3.12 (IDENTIFY volatile, consistent with `docs/00_MILAN_COMPLIANCE_REVIEW.md` lines 249–250 and REQ-AEM-014); IEEE 1722.1-2021 §7.4.17/§7.4.18 (SET_NAME/GET_NAME, 64-byte values, name selectors).

- **Inventory (item 1).** I regenerated both parent images at milan-fpga `5603c353` from the parent's own builder overlay and image joiner, using the reviewed processor packer (`scripts/gen_parent_images.py`). Both match the author's recorded identities: 1x1 is 7,512 B, sha256 `4fc8d615…396d`; 8x8 is 19,520 B, sha256 `d8296833…a7bc`.
- **Ordinal map.** My own image parser (`scripts/inventory_check.py`) reads the header, the index map, name_base and each body's own (type, index) key. The derived (type, index, name_index) → ordinal map equals the bench oracle's enumeration exactly: 39 of 39 and 107 of 107, dense from 0.
- **No named type is missing.** The only index-map entries without names are LOCALE (72 B), STRINGS (452 B) and STREAM_PORT_INPUT/OUTPUT (20 B), and none of them carries an object_name.
- **The suite asserts each item 1 property.** Both ENTITY selectors and CONTROL are in the inventory. IDENTIFY is set to 255 before reset and must read 0 afterwards (N8). The captured frame must be one coherent eight-lane old or new value (N7, plus D3N6 taint).
- **Empty and full-length values (item 2).** Every seventh ordinal from 2 is empty and the rest are 64 non-NUL bytes. N2, N3 and N5 compare all 72 frame bytes or all 64 name bytes. Both of these are killed: `name_empty_refused` (author) and `R_empty_replay_skipped` (reviewer, N5 at ordinals 2, 9, 16…).
- **Debt and rollback (item 3).** `store_not_rolled_back` fails D3N5. The debt control (`rollback_ignores_debt`, D3R10) stays in the unchanged `tb/pp_top`, and the author reports it killed at base and head. Pending is `unflushed_o = |dirty_r` over every record, names included (`KL_aecp_nvm_writer.sv:1254`). The author's `pending_clears_other_name` and my `R_pending_clears_higher` both fail N6.
- **Negative controls (item 5).** Every §18.3 control maps to a killed author control (mapping table in the README and in the author's HANDOFF). I re-applied five of my own variants and each was killed (Tests lens).
- **Measurement (item 6).** See the RTL lens.
- **Limits.** Physical cold-cycle of all writable names (D3 §18.3, "Dependencies and physical result") is outside the frozen issue items 1–6, and the PR says it keeps its separate acceptance. It is NOT RUN, and nothing here is hardware proof.

## Lens 2: RTL (CLEAN)

- **No RTL change.** The `hdl` tree object is identical (above).
- **DR4, from the author's receipts.** `ooc-{base,head}-{ax7101,ax8x8}.json` are identical in all 332 fields, including `inputs_sha256`, all scope figures and the 57 hierarchy rows. `resumed-measurement-comparison.json` gives 1x1 TDM8 `KL_pp_shadow` LUT 23,171 → 23,171 (LUTRAM 2,728 → 2,728), FF 19,807 → 19,807, RAMB36/18 16/3 → 16/3 and DSP 8 → 8, a delta of +0/+0/0/0 against the names-stage ceiling of +750/+400/0/0. WNS stays +3.203 ns and WHS +0.159 ns at 20 ns. The 8x8 diagnostic is likewise unchanged, with WNS −3.243 ns already present at the base; its post-place obligation stays open and blocked.
- **No vendor rerun.** The figures are supported: the input digests are equal and the RTL is byte-identical, so a zero delta is the expected outcome. The parent glue is inside the measured top.
- **DR3a, re-executed.** I ran `--measure` on both regenerated images at the head. All twelve rows match the author's published logs byte for byte (`name-restore-{1,8}-timing.log`). The longest terminal is 29,008 clocks against the 1,000,001-clock aggregate, the longest D3 wait is 1,908 against 20,001 per wait, and the longest record operation is 87. No restore path changed.
- These are model numbers at the suite's 128-entry geometry (see F1), not shipping-geometry or physical latency.

## Lens 3: Robustness (UNCLEAN: F1)

- **Grading cannot be faked by a crash.** A compiler failure, crash or missing completion tally never counts as a kill (`mutants.py:82-86`), and `run.py:63-69` returns non-zero on a missing tally or a crash with zero FAILs.
- **Concurrency.** The author campaign ran with `--jobs 8` without interference, and its records are byte-identical to the published head records.
- **F1 (capacity boundary).** See the findings section.
- **Lower-severity items.** S2 (rerun of `make mutants` crashes rather than refusing cleanly), S3 (prefix grading) and S4 (`--measure` asserts nothing) are suggestions.

## Lens 4: Tests (UNCLEAN: F1)

All runs used the pinned simulation compiler 5.050; I checked its identity first (`--version` gives `5.050 2026-07-01 rev v5.050`).

| Run | Result | Receipt |
|---|---|---|
| Normal suite, both synthetic populations (`run.py`) | rc 0; 169 + 441 = 610 checks, 0 FAIL | `receipts/golden-synthetic.{log,rc}` |
| Generated 1x1 / 8x8 images, functional | rc 0 / rc 0; 169 / 441 checks; logs byte-identical to the author's (`5299b35d…`, `562d06f9…`) | `receipts/gen-{1x1,8x8}.*` |
| Generated images, `--measure` | rc 0; byte-identical to the author's timing logs | `receipts/gen-*-measure.*` |
| Author mutation campaign (`mutants.py --jobs 8`) | rc 0; golden PASS, 14/14 KILLED; `results.json` byte-identical to the published `mutants-head-results.json` | `receipts/author-campaign*` |
| Reviewer-written controls (`scripts/reviewer_controls.py`, each plant written independently from the RTL) | golden PASS; 5 KILLED against my predicted assertions, 1 caught by N4 rather than my predicted D3N7 (rc 1 by my own strict grading) | `receipts/reviewer-controls*` |
| `make check`, `gen_matrix.py --check` | rc 0 / rc 0 (562 files, 94 matrix rows, 0 untested) | `receipts/make-check.*`, `receipts/gen-matrix.*` |
| Shipping-capacity probe (`scripts/capacity_probe.sh`) | capacity 39/107: rc 0; boundary defect at 128: rc 0 (survives); at 39: rc 1 (N3/N5 ordinal 38, N6) | `receipts/capacity-probe.*`, `receipts/probe-*` |

My controls, all plants in `hdl/aecp/KL_aecp_nvm_writer.sv`:

- `R_trigger_odd_dropped`: the name trigger is kept for even ordinals only. Fails N3/N5 at the odd ordinals; 148 FAILs.
- `R_record_id_neighbour`: a name's record ID becomes `0x80 + (ordinal ^ 1)`. Fails N3 at every ordinal; 300 FAILs.
- `R_empty_replay_skipped`: replay skips an all-zero lane write. Fails N5 at ordinals 2, 9, 16…; 22 FAILs.
- `R_pending_clears_higher`: a completed record also clears every higher pending record. Fails N6 (and N3).
- `R_latch_lane_alias`: the service latch aliases odd lanes onto even lanes. Fails N3.
- `R_replay_skips_locate_wait`: the late-image LOCATE leaves without waiting for the store's answer. I predicted D3N7; it fails N4 instead ("every name reset to image default before replay") in both populations. N4 is a name-value assertion, and the README assigns it to this defect class.

The author's 14 controls together cover every §18.3 negative control. The suite's oracle is independent of the RTL and of the image directory: the C++ group table is checked against my parser above, and `name_record()` encodes the 07 §5.2 frame and its CRC itself.

The gap is F1: no run exercises the shipping capacity, where the last generated ordinal is the table's last entry.

## Lens 5: Docs (CLEAN; RESIDUE R573-1-R1 and suggestions only)

- **Verification-table row.** The new `09_verification.md:204` row is accurate against the suite (populations, checks and the 14 controls) and cites Milan §5.3.13. `make check` passes.
- **README.** The inventory table, check table, control mapping, timing conditions and scope limits match the code and the receipts.
- **Clause citations.** They agree with the compliance review's §5.3.12/§5.3.13 usage.
- **Wording residue.** R573-1-R1 (the "distinct values" sentence).
- **Suggestion S1.** The README never says how to produce the `--image` inputs it uses.

## Findings

### R573-1-F1 (MINOR): the name suite never runs at the shipping name capacity, so the full-table boundary is untested

- **Lenses:** Tests, Robustness.
- **Where:** `tb/name_state/run.py:25-27` (`.DESC_NAME_ENTRIES_P (128)` for every run) and `tb/name_state/README.md:37-38`; consumed by `mutants.py:70` (via `build`).
- **Authority:**
  - Issue #170 item 4 and D3 §18.3 Validation require real SET_NAME/GET_NAME across the generated inventory, with every ordinal verified.
  - The parent at `5603c353` binds `.DESC_NAME_ENTRIES_P (AEM_NAME_ENTRIES_C)` (`hdl/milan/milan_datapath.sv:8026`).
  - `AEM_NAME_ENTRIES_C` is the generated exact name count (`sw/builder/endstation_builder.py:2734/3188`; `hdl/common/gen/adp_shape_defaults.svh:31` has 39).
  - In the shipping build the last generated ordinal is therefore entry `N_NAME_P - 1` of a full table.
- **Evidence (`scripts/capacity_probe.sh`, `receipts/capacity-probe.log`).**
  - With the suite rebuilt at capacity 39 (1x1 image) and 107 (8x8 image), production passes: 169/169 and 441/441.
  - With a planted defect in which the name trigger drops the table's last entry (`32'(nchg_ord_i) < N_NAME_P - 1`), the PR's suite at 128 passes 610/610, so the defect survives. The same defect at capacity 39 fails `N3 saved ordinal 38`, `N5 restored ordinal 38` and `N6 pending`.
- **Impact.** A capacity or off-by-one regression in the trigger, store or restore bounds would break persistence of the last name on every shipping shape while the lane's acceptance suite and its mutation campaign stay green. The PR's claim to cover "every generated writable ordinal" holds only for a non-shipping 128-entry geometry. The DR3a figures also come from that geometry, as the author already discloses.
- **Required outcome.**
  - Run the generated-image acceptance runs and the default synthetic populations at the shipping capacity: `DESC_NAME_ENTRIES_P` equal to the population's name count (39 and 107), for example one build per population. The 128 geometry may stay as an additional run.
  - Add a planted capacity-boundary control, for example the trigger bound above, that fails a named N3/N5 last-ordinal assertion in a completed run.
  - Update the README and the 09 row to state the geometry.
- **Verification.** The normal suite passes at 39/107. The new boundary control is KILLED in the campaign, and it survives at 128 if the 128 run is kept. Rerunning `scripts/capacity_probe.sh` against the fixed head shows the boundary defect failing in the PR's own suite.

### R573-1-R1 (RESIDUE): the README overstates the distinctness of the patterned saved values

- **Lens:** Docs.
- **Where:** `tb/name_state/README.md:61`, "Distinct full-length values expose aliasing and lane swaps."
- **Evidence.** `sim_main.cpp:24` uses `33 + (ordinal*11 + byte*7) % 90`, whose period is 90 in the ordinal. In the 107-name 8x8 run, ordinals 90–106 repeat ordinals 0–16: twelve non-empty duplicate pairs (`receipts/inventory-check.log`). The author's HANDOFF already states this limitation correctly. No test, figure or claim changes, because record IDs and CRCs still separate ordinals in N3 and all power-of-two aliasings give distinct values.
- **Exact fix.** Replace the sentence with: "Full-length values are distinct for every ordinal of the 1x1 population; the pattern repeats with period 90, so in the 8x8 diagnostic ordinals 90–106 repeat the values of ordinals 0–16, and only each saved frame's record ID and CRC distinguish them."

### Suggestions (do not affect the verdict)

- **S1 (Docs).** `README.md:22-24` uses `/tmp/1x1.img.bin` and `/tmp/8x8.img.bin` without saying how to produce them. Add the parent pin and the two commands (builder overlay, then `avdecc/gen_aemi_image.py`) and the expected sha256 values `4fc8d615…` and `d8296833…`.
- **S2 (Robustness).** `mutants.py:105` accepts an existing output directory, and `:61` then raises FileExistsError with a traceback. `Makefile:3` fixes `OUTPUT ?= /tmp/name-state-mutants`, so a second `make mutants` crashes. Refuse an existing directory cleanly up front, or default to a fresh temporary directory.
- **S3 (Tests).** `mutants.py:83` grades with `startswith`, so "N5 restored ordinal 1" also matches ordinals 10–19 and "…2" matches 20–29. The published records show the intended ordinals, so nothing changes today. Anchor the match to the exact ordinal.
- **S4 (Robustness).** `--measure` executes zero checks and returns rc 0 whatever the timings. Asserting terminal ≤ AGG and every wait ≤ RS_TMO would make a DR3a regression fail rather than only print.

## Prior public review findings

At the review start, PR #172 had only the two manager start notices (R572-1, R573-1) and no review objects. The issue carries no review findings. There are no prior public findings to resolve or retain at this head. I read no other reviewer's report.

## Parent consumer input (`parent-name-evidence.patch`)

I judged this patch as an input to the parent adoption lane; it is not part of this PR.

- In a disposable copy of milan-fpga `5603c353`, with the processor gitlink staged at `c3864686` and never committed, the patch applies cleanly.
- Without it, `scripts/measure_test_evidence.py --check` returns rc 1: "1 unexplained DUT-source reader(s)", namely `protocol-processor/tb/name_state/mutants.py`.
- With it, the gate returns rc 0: 71 ≤ 77 suites without a mutation arm, 0 ≤ 0 unexplained readers.
- Its disposition text is accurate: the driver plants isolated defects and grades named value assertions, and expected names come from the independent inventory.
- The parent adoption lane must carry this entry, or an equivalent one, when it moves the gitlink. It may add the remaining control classes (identify, image defaults, live lanes, rollback, taint) to the wording.
- The other parent gates the author reports were not run (full parent banks are not allowed in this review).

## Hosted evidence at the exact head (as of 2026-10-09T23:54Z)

- `docs-gates` ×2: completed, success.
- `portability` ×2: completed, success.
- `suites` ×2: in progress, with no conclusion.
- Combined status: pending.

The manager owns hosted and act acceptance. There is no manager source bank at this exact head, and I neither claim nor infer one.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #170 items 1–6, D3 §18.3, ruling 6087242563; regenerated parent images and independent ordinal parser; N1–N8, D3N5–D3N7; compliance review clause use | R573-1 | c3864686c0b254bd2d7b7f733078ec302fb9be62 |
| RTL | CLEAN | base/head tree objects for hdl, syn, scripts, tb/pp_top, tb/common and docs 01/02/07; wrapper adaptation; OOC receipts (DR4); re-executed DR3a `--measure` | R573-1 | c3864686c0b254bd2d7b7f733078ec302fb9be62 |
| Robustness | UNCLEAN (F1) | run.py/mutants.py grading and failure paths; capacity probe; campaign concurrency | R573-1 | c3864686c0b254bd2d7b7f733078ec302fb9be62 |
| Tests | UNCLEAN (F1) | normal suite, generated-image runs, author 14-control campaign, 6 reviewer controls, capacity probe, `make check`, matrix | R573-1 | c3864686c0b254bd2d7b7f733078ec302fb9be62 |
| Docs | CLEAN (RESIDUE R1, S1) | tb/name_state/README.md, 09_verification.md:204, PR body, HANDOFF | R573-1 | c3864686c0b254bd2d7b7f733078ec302fb9be62 |

## Real limits

- Not run: the full processor suite bank, HDL lint, the synthesis flow, any vendor synthesis (DR4 was taken from the author's receipts, as instructed), and every parent gate except the single evidence-reader gate. Production RTL is byte-identical, so those gates' inputs are unchanged apart from the new suite.
- Physical calibration and cold-cycle were NOT RUN; nothing here is hardware proof.
- The manager's merge-turn current-dev candidate (builder and native banks) was not built.
- The DR3a numbers are simulation-model figures at the suite's 128-entry geometry.
- After every probe, the review clone was restored and verified: HEAD `c3864686`, tree `305218ec`, index equal to the tree, all 587 tracked blobs byte-identical with matching modes, no untracked or ignored files, and no gitlinks in this repository. Every probe tree lived under the packet's `scratch/` directory.

## Pending manager duties

- Hosted acceptance at the exact head, including the two `suites` contexts still in progress.
- The merge-turn current-dev candidate banks and their receipts.
- Carrying RESIDUE R573-1-R1 to the residue checklist.
- After the author resolves F1, a re-review at the new head.
- Making sure the parent adoption lane carries the evidence-reader classification.
- The separate acceptance of physical cold-cycle and lane 5.

R573-1 FINISHED
