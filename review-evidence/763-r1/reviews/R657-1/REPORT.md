[R657] NEGATIVE - exact head 07c6c72fce79e705bcf28a70071497d0ce7040e4

# R657-1: internal cleared-context review of PR #766 (Closes #763, Relates to #637)

- Head `07c6c72fce79e705bcf28a70071497d0ce7040e4`, tree `c70d7afe29d34724474bfc05053fe3cb43801026`, on dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` (source base and live dev are the same commit).
- Delta: two one-line commits, four files, +65/-3. The files are `sw/firmware/ctrl/test/test_aecp.cpp`, `sw/firmware/ctrl/test/aecp_mutants.py`, `sw/firmware/ctrl/test/aecp_arms.py` and `sw/firmware/ctrl/aecp/README.md`. No firmware source, store source, record format or HDL changed.
- Scope reviewed against: the issue body, the manager's assignment (issuecomment 6256482855), the author's STOP (6257029697), and the manager's ruling (6257040042), which narrows #763 to option B and moves the board cold-cycle acceptance to #637. #637 records that acceptance in its comment 6257040284, which I checked.
- Prior public review findings on this PR: **none**. The PR has only the two review-start notices, there are no PR reviews, and there are no inline comments. Nothing needs to be resolved or retained.
- The verdict is NEGATIVE because of one open MINOR (F1). F1 is a provenance-artifact item and can be fixed in a few minutes. Every other check of the task contract passes on my own execution.

## Findings

### F1: MINOR (Conformance, Tests): the lane changes two CI tool-inventory inputs without refreshing their recorded digests

- **Where:** `ci/image/tool-inventory.json:148-149` (unchanged by the PR), together with `sw/firmware/ctrl/test/aecp_arms.py` and `sw/firmware/ctrl/test/aecp_mutants.py` (changed by the PR).
- **Authority:** `docs/testing/CI_IMAGE.md:768-770`: "Review script changes before updating their content hashes. Then refresh workflow provenance whenever its inputs change." The manager's assignment item 5 asks for every gate the change touches to be rc 0, and this round's brief repeats it ("the firmware test gate and every touched gate pass").
- **Evidence:** `receipts/inventory_input_digests.txt`.
  - The committed inventory records the base digests: `33c3c60a…` for `aecp_arms.py` and `b3f94ef0…` for `aecp_mutants.py`.
  - At head these files hash to `277a41b9…` and `bb4fe6f2…`.
  - Two unrelated rows were already stale on dev before this lane: `scripts/check_doc_style.py` and `scripts/measure_test_evidence_readers.py`, which went stale through interleaved merges.
  - The author's published derivation (`author/receipts/round-b/inventory/*.diff`) agrees: the lane adds exactly these two digest rows to the drift.
  - The author disclosed this as an open question in REVIEW READY. No public decision on it is recorded.
- **Impact:**
  - No PR workflow runs `ci_tool_inventory.py --check`, so no hosted context changes state.
  - The CI image build's provenance gate was already red on dev. The lane makes it red for two more reasons, both its own. They are unreviewed against the inventory (no recorded check that the changed scripts add no installation request).
  - The next inventory refresh would fold this lane's script changes in without that review.
  - The rule is explicit and the lane created the drift, so this is more than wording.
- **Required outcome (either one):**
  - (a) Update only the two lane-owned rows to the head digests. Leave the two pre-existing unrelated rows alone, so no unrelated drift is folded in.
  - (b) Record a public maintainer or manager decision that assigns the refresh of these rows to the inventory's owner, with a tracking issue that names both lane-owned rows.
- **Verification:**
  - For (a): with the pinned parser, run `python3 scripts/ci_tool_inventory.py --write` in a disposable full checkout and diff it against the committed file. The diff must list only `scripts/check_doc_style.py` and `scripts/measure_test_evidence_readers.py`. `sha256sum` of the two lane files must equal the committed rows.
  - For (b): the decision and the issue link are on #763 or #766.

### R1: RESIDUE (Docs): the PR body status line is stale

- **Where:** the PR #766 body, Status section.
- **Problem:** It says "`763-map-persist` -> `dev`, two commits, not yet pushed." The branch is pushed and is the PR head.
- **Exact fix:** change it to "`763-map-persist` -> `dev`, two commits." This is wording only. It changes no measurement, verdict, test, code or claim.

### S1: SUGGESTION (Docs): scope the new README sentence to this owner

- **Where:** `sw/firmware/ctrl/aecp/README.md:105-109`.
- **Current state:**
  - The new sentence says that an empty list and a non-default list each come back across the store's power cycle, citing #763 and Milan v1.2 5.3.9.1/5.3.10.1.
  - The page bounds this already: README:4-6 says the AECP owner is opt-in and that the shipping image keeps its existing owners. `docs/design/SAVED_STATE_MATERIALIZATION.md:17` says channel maps (stage 3) are not implemented, and the PR body's "Known limitations" says the same.
- **Suggestion:** Optionally add a clause: "in this opt-in owner; the shipping image writes no channel-map record until #637". That would stop a reader of this page alone from taking #763's closure as a board fix.

### S2: SUGGESTION (Tests): add the writer-side defect as a third named mutant

- **Where:** `sw/firmware/ctrl/test/aecp_mutants.py:358-371`.
- **Evidence:** My probe `writer-skips-all-unused-payload` makes `nvm_latch` (`nvm_store.c:494-517`) skip an all-UNUSED payload, which leaves the record erased.
  - With the full 73-test AECP app arm minus the new test, the arm passes and the defect escapes.
  - The new test catches it on both "the empty set is a framed record, not an erased one" and "the empty list survives the power cycle".
- **Suggestion:** Adding it as a named defect would bank the writer half of the same "empty vs erased" rule. This is optional, because the ruling asked for the two plants and both are in place.

## What was checked (independent pass, then evidence)

### Acceptance (narrowed #763, ruling option B)

1. **Empty list in both directions plus a non-default list survive the store's power-cycle path.**
   - Where: `test_aecp.cpp:250-286` runs once per direction (`SCOPED_TRACE` 14/15).
   - Setup: REMOVE_AUDIO_MAPPINGS (cmd 45) empties port 0 in one direction and removes the last row of port 0 in the other.
   - Save: the test commits through the real store (`save()` at :182-189 asserts one commit and idle).
   - Framing check: it checks that the empty record's magic is `0x1722` and that its payload is all-erased (UNUSED). This is the framed empty set of SAVED_STATE_MATERIALIZATION 8.3 V3g (`docs/design/SAVED_STATE_MATERIALIZATION.md:1164`), never the whole-span-erased record of the FASTCONNECT 6.1 erased-record rule (`docs/design/SAVED_STATE_FASTCONNECT.md:661`).
   - Power cycle: it restores defaults, which resets every map (`aecp_state.c:82-86`, so the post-cycle checks are not vacuous). It then power-cycles the flash model, boots to `NVM_T_COMPLETE`, and requires `count == 0` and the exact latched non-default rows.
   - Result: **met** on the firmware host path.
2. **Both plants are named mutants, and each fails the new test by name.**
   - `aecp_mutants.py:358-371`: `nvm-empty-map-keeps-defaults` (`count == 0` returns APPLIED, keeping defaults) and `nvm-unused-payload-reads-erased` (the record walk at `nvm_store.c:298` also treats an all-0xFF payload as erased). The second is planted into the campaign's sibling store copy (`aecp_mutants.py:507-509`, `aecp_arms.py:20`).
   - In my four-shard self-test bank both print `[ok]`, with 939 controls caught and none escaped.
   - My probes grade them with the campaign's own reader (`caught()`):
     - m1 fails the new test on "the empty list survives the power cycle", and fails `WholeMapFramingAndEmptySetAreDistinct` on "all UNUSED is an intentional empty set".
     - m2 fails only the new test.
   - Result: **met**.
3. **The gap is closed.**
   - m2, with the new test excluded, passes all 73 other AECP app-arm tests (probe `m2-gap-full-arm-without-new-test`).
   - I planted m2 independently into a store copy (`scripts/store_gap.py`). All six store suite binaries still pass at the shipping shape.
   - So before this PR no in-tree test caught it, and now one does. Result: **met**.
4. **No record-format change.** `git diff --name-status` shows only the four files above. `aecp_nvm.c`, `nvm_store.c`, `nvm_klj2.*` and the generated record geometry are untouched. Result: **met**.
5. **The firmware test gate and every touched gate pass.**
   - The firmware gate and all the gates listed below pass.
   - The tool-inventory provenance check does not pass. It was already failing at base, and the lane adds its own two rows to the failure (F1).
   - Result: **not fully met**.
6. **Scope stated honestly.** The PR body, README:4-6 and MATERIALIZATION.md:17-20 state the board gap and #637's ownership. #637 carries the moved acceptance. S1 is optional. Result: **met**.
7. **The receipts index matches its files.**
   - I fetched the published evidence tree at `c262f8de` blob by blob and verified each git blob id: 56 blobs.
   - `author/receipts/INDEX.md`: 51 rows for 51 files, 0 mismatches in bytes or sha256.
   - `MANIFEST.json`: 55 entries for 55 files, 0 mismatches, nothing redacted. See `receipts/index_check.log`.
   - Result: **met**.
8. **Comment rule.** The delta's new comments (`test_aecp.cpp:250-251`, `aecp_mutants.py:358`, `:507`, `aecp_arms.py:20`) state behaviour and reason with issue and requirement IDs. A scan of the delta finds no bench lane label, lane name, review round, reviewer ID or comment ID. No RESIDUE.
9. **Commits.** Both commit messages are one line with no trailers.

### My execution at the exact head

All runs used the reviewer clone, CPython 3.12.3 unless stated otherwise, GCC 16.2.1, GoogleTest/GoogleMock 1.18.0, and the pinned RV32 SDK. Every command below exited 0.

| Gate or probe | Result | Receipt |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --self-test --shard i/4 --jobs 3`, i = 0..3 | all four rc 0, `test_ctrl_firmware: PASS`; `[ok]` 61+520+78+280 = 939, 0 ESCAPED; both #763 mutants `[ok]` | `receipts/gates/fw_selftest_shard*.{log,rc}` |
| `test_ctrl_firmware_shards.py` | 940 live invocations in exactly one shard | `receipts/gates/fw_shards.*` |
| `fw_coverage.py --check --jobs 3` / `--selftest` | PASS (30 files) / 29 of 29 | `receipts/gates/fw_coverage_*` |
| `tally_selftest.py` | 18 of 18 | `receipts/gates/tally_selftest.*` |
| `test_ctrl_nvm.py --require-rv32 --jobs 4` | OK across 5 shapes, 435 tests | `receipts/gates/ctrl_nvm.*` |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (pinned Verilator 5.050, identity recorded) | PASS | `receipts/gates/boundary_only_verilator.*`, `verilator_identity.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` | PASS, 0 findings. It ran under the bench LiteX venv (Python 3.14.8), whose seven checkouts match `sw/litex/litex_pins.txt`. A first attempt under the system interpreter stopped on a missing `migen` before judging anything (kept as a receipt). | `receipts/gates/boundary_without.*`, `litex_venv_revisions.txt` |
| `docs_check.py`, `check_doc_style.py` (+ `--selftest`), `check_feature_status.py` | 0 findings / OK / OK / 0 findings | `receipts/gates/docs_check.*`, `doc_style*`, `feature_status.*` |
| `gen_toc.py --check`, `--verify-anchors`, `--selftest`; `check_em_dash.py --base e9cbb676` (pinned renderer venv) | OK / 528 links / 1501 arms / 0 findings over 9 added lines | `receipts/gates/toc_*`, `em_dash.*`, `md_venv_freeze.txt` |
| Ten fault probes in scratch copies (`scripts/probes.py`) | all ten as expected (table below) | `receipts/probes/` |
| `Nvm.*` shuffled (seed 763) × 25, and the new test alone × 10 | 25/25 and 10/10 pass | `receipts/probes/nvm_shuffle_repeat25.*`, `new_test_alone_repeat10.*` |
| Store suites under the m2 plant (`scripts/store_gap.py`) | 6/6 binaries pass: the store suites do not catch the defect | `receipts/store_gap/` |

| Probe (AECP app arm, two interfaces, 1x1 shipping shape) | Filter | Outcome |
|---|---|---|
| clean | `Nvm.*` | 8/8 pass |
| m1 table defect | `Nvm.*` | the new test and WholeMapFraming fail on their named words |
| m2 table defect | `Nvm.*` | only the new test fails, on its named words |
| m2, new test excluded | full arm | 73/73 pass: the gap the new test closes |
| m1, new test excluded | full arm | WholeMapFraming still fails |
| writer skips an all-UNUSED payload (`nvm_latch`) | `Nvm.*` | the new test fails on "framed record" and "empty list survives" (trace 14 and 15) |
| writer plant, new test excluded | full arm | 73/73 pass (S2) |
| output-only empty keeps defaults | `Nvm.*` | only the new test fails, trace 15: the output direction is covered only by the new test |
| input-only empty keeps defaults | `Nvm.*` | the new test and WholeMapFraming fail |
| non-empty saved map ignored | new test | fails on "the non-default list survives the power cycle" |

Hosted, observational only (the manager owns hosted and act acceptance): a snapshot of the exact-head check runs showed 37 completed/success, 14 in progress, and 1 skipped (Physical gPTP, nightly/manual). Every firmware and docs context (`firmware-unit`, `firmware-aecp-mutants`, `firmware-boundary`, `firmware-verilator`, `firmware-control-mutants`, `firmware-srp-mutants`, `docs-*`) was executed and successful. See `receipts/hosted_check_runs_snapshot.tsv`. The skipped context is not evidence of anything.

Clone integrity after probes (`receipts/head_integrity.txt`):
- Worktree and index are identical to HEAD, and the index writes tree `c70d7afe…`.
- `ls-files` matches `ls-tree` on mode, blob and path.
- All five required submodule gitlinks match HEAD, with clean worktrees.
- The ignored build outputs my runs created were removed, so the ignored and untracked set equals the pre-review set.

## Lens results

- **Conformance: UNCLEAN (F1).**
  - Applied to: the issue body; ruling 6257040042; assignment 6256482855; #637 comment 6257040284; `REQUIREMENTS.md:395-401` (Milan 5.3.9.1/5.3.10.1); MATERIALIZATION 8.3 V3g (`:1130`, `:1164`, `:2484`); FASTCONNECT 6.1 (`:661`); `test_aecp.cpp:250-286` against them; the PR body.
  - Each criterion holds except the touched-gate item (F1).
- **RTL: CLEAN.**
  - [R657] PASS RTL — `git diff --name-status e9cbb676..07c6c72f`, `aecp_nvm.c:52-104`, `nvm_store.c:288-310`, `nvm_store.c:494-517`, `aecp_arms.py:13-23`, `aecp_arms.py:51-90` — no HDL in the delta, and every firmware and store source is unchanged. The record walk (header-only erasure) and the writer (frames every latched payload) match FASTCONNECT 6.1 and V3g.
  - The harness interface change (the store taken from `tree.src.parent/ctrl_nvm`) resolves to the same directory for every checkout caller: `Tree(CTRL…)` at `test_ctrl_firmware.py:226,304`, `aecp_arms.py:149`, and `ctrl_pin.py:946` through `aecp_arms` main.
  - No other planted-copy campaign reaches the Nvm arm: `ctrl_mutants.py:844-850` holds no AECP arm, and `srp_mutants.py:913` and `ctrl_arms.py:83` use only their own arms.
  - The AECP arm's include path takes the copy's store headers (`aecp_arms.py:59-81`).
- **Robustness: CLEAN.**
  - [R657] PASS Robustness — `test_aecp.cpp:260-285`, `aecp_state.c:71-86`, `receipts/probes/*` — the new test covers both directions, each direction's empty and non-default case, reboots from a blanked model per iteration, and is not vacuous after `aecp_restore_defaults` (every map is reset).
  - It is order-independent and repeatable: 25 shuffled repeats and 10 isolated repeats pass.
  - It catches four extra defect shapes (output-only, input-only, writer-side, non-empty-ignored) beyond the two planted ones.
- **Tests: UNCLEAN (F1).**
  - Applied to: `test_aecp.cpp:250-286`, `aecp_mutants.py:358-371` and `:500-536` (`controls()` requires the new test to be claimed), the four-shard self-test bank, coverage, the store suites, both boundary halves, the gap probes, and the author's receipts (`author/receipts/round-b/*`), with the index verified.
  - Each new test fails for the defect it names, and existing regressions remain green.
  - It is unclean only for the unrefreshed provenance gate (F1).
- **Docs: CLEAN.**
  - [R657] PASS Docs — `sw/firmware/ctrl/aecp/README.md:101-113,129-141`, the PR #766 body, `docs/design/SAVED_STATE_MATERIALIZATION.md:17-20`, and the docs gate receipts — the new prose matches the test and campaign behaviour and the cited clauses. The opt-in scope is bounded at README:4-6. The board gap is stated in the PR body and the design page. The docs gates and em-dash check over the 9 added lines pass.
  - R1 is RESIDUE (PR body wording) and S1 is optional.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #763 body and ruling, assignment, #637 comment, REQUIREMENTS.md:395-401, MATERIALIZATION 8.3 V3g, FASTCONNECT 6.1, test_aecp.cpp:250-286, PR body | R657-1 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| RTL | CLEAN | diff name-status, aecp_nvm.c:52-104, nvm_store.c:288-310 and 494-517, aecp_arms.py:13-90, callers of core_arm/saved_state | R657-1 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Robustness | CLEAN | test_aecp.cpp:260-285, aecp_state.c:71-86, ten probes, shuffle/repeat runs | R657-1 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Tests | UNCLEAN (F1) | test_aecp.cpp, aecp_mutants.py, four-shard self-test bank, coverage, store suites, boundary halves, gap probes, author receipts and index, tool-inventory digests | R657-1 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Docs | CLEAN (R1 residue, S1 optional) | aecp/README.md:101-141, PR body, MATERIALIZATION.md:17-20, docs gate receipts | R657-1 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |

## Real limits

- **Host only.** The power cycle is the host flash model (`nvm_fmodel_power_on`) with a defaults reset that stands in for RAM loss. It is not a board cold cycle. By the ruling, that acceptance moved to #637. Physical calibration NOT RUN, and no hardware was used.
- **Shape and ports.** The new test runs at the shipping 1x1 shape, port index 0 in each direction, in the AECP app arm at one and two interfaces (bank) and two interfaces (probes). Other shapes are exercised only by the existing suites.
- **Inventory derivation.** I could not reproduce the full `ci_tool_inventory.py` derivation: my copy was a `git archive`, which carries no submodule content, and the derivation refused on a script outside it. F1 rests on direct sha256 comparison of the four affected inputs against the committed rows, plus the author's published derivation, which agrees.
- **Interpreter.** The `--without verilator` boundary half ran under Python 3.14.8 (the bench LiteX venv, pins matched), not CPython 3.12.3.
- **Hosted snapshot.** The hosted check-run snapshot was partial (14 in progress). No manager source bank ran at this head, and I claim none.

## Pending manager duties

- Rule on or carry F1, by option (a) or (b), then re-review the corrected head.
- Carry R1 to the residue checklist.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and own hosted and act acceptance.
- Collect the external review.

R657-1 FINISHED
