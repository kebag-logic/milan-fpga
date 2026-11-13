[R833] POSITIVE - exact head 3bebf03a1d25bcbde9c0ec48dfd711af7280131e

Round R833-2, internal cleared-context independent review of issue #897 / PR #898 (Mark II split: GET_AS_PATH answered through the face's GSI window kind 2).
Tree `172d19ad99d3f27c876898e8c2697918d59ba5ff`. This is a delta review from round 1's head `5e6fef3e` (R833-1 and R834-1 POSITIVE) to `3bebf03a`. The range has three commits:
- `d3202fa2`: merge of `dev-soft-core` `cec88385` (#810 merged). Two docs files conflicted.
- `d395f682`: the images' sizes restated.
- `3bebf03a`: a comment in `build.py` rewrapped to hold the 1,000-line module limit.

No BLOCKER, MAJOR or MINOR finding is open at this head, and all five lenses are covered clean.
Two RESIDUE items are wording only (F1 in a design doc, F2 in the PR body). Two new SUGGESTIONs (F3, F4) and three round-1 SUGGESTIONs are retained. Two round-1 items are resolved at this head.

## 1. Merge resolution: both sides' behaviour is kept

Method: `scripts/merge_sides.sh` and `scripts/merge_base_side.sh`. Each compares the `-U0` hunk bodies (the `+`/`-` lines, with line numbers stripped) of two diffs per file.

- **Branch side** (`receipts/merge_sides.txt`): all 16 files the branch changed from `7f50ee6a` to `5e6fef3e` are SAME. For each, `cec88385..d3202fa2` carries exactly the branch's own `7f50ee6a..5e6fef3e` hunks. That includes the two conflicted files, `docs/design/MAILBOX_SPLIT.md` and `docs/design/SPLIT_CONTROL_MEMORY.md`. The merge changes no other file against `cec88385`.
- **Base side** (`receipts/merge_base_side.txt`): 149 of the 150 files #810 changed (`7f50ee6a..cec88385`) carry identical hunks in `5e6fef3e..d3202fa2`. The 150th is `SPLIT_CONTROL_MEMORY.md`. The only difference is the order of one removed line relative to the branch's added line inside the conflicted hunk; the set of lines is identical. No submodule gitlink differs between `cec88385` and `d3202fa2`, and `d3202fa2..3bebf03a` touches four text files and no gitlink.
- **The merge's composition with #810's firmware:** `git diff 5e6fef3e 3bebf03a` was run over the branch's GET_AS_PATH sources and tests: `sw/firmware/ctrl/aecp/`, `plat/ctrl_plat.c`, `test/{aecp_mutants,plat_mutants}.py`, `test_aecp.cpp`, `test_plat_boot.cpp` and `ctrl_aecp_image.c`. #810 changed only two of them, and none of the face's GET_AS_PATH code:
  - `aecp_mbx.h:18-29`, the 8x8/2if cold cost 165 to 185 us;
  - `test_aecp.cpp`, NVM header renames and the round-room test at line 2466.
- **#810's `KL_mbx.sv` change** (`3ba76ae7c7`, register read answered a cycle later): no hunk in `hdl/milan/mailbox`, `aecp_mbx.h` or `sw/firmware/include` names GSI, the face or AS_PATH (grep over the diff). The real-RTL GSI window tests, `tb/verilator/mbx/suite_face.hpp:410,547-584,666`, are in the sweep that passed at the head.

## 2. The three base reds at the head (reviewer's own runs)

| Gate | Command (at `3bebf03a`, this clone) | rc | Result | Receipt |
|---|---|---:|---|---|
| idiom ratchet | `python3 -B scripts/check_cpp_idiom.py` | 0 | `multi-declarator declaration: 0 <= 0`, every rule within its ratchet | `receipts/head/cpp_idiom.{log,rc}` |
| hooks self-test | `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test` | 0 | `28 of 28 checks pass; 96 of 96 mutants caught` | `receipts/head/hooks_selftest.{log,rc}` |
| firmware boundary | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` (rtl-fast.yml:1220, the job's step 9), pinned RV32 SDK on PATH | 0 | `ctrl_boundary: PASS`, 3359 compiled sources of 3616 recorded invocations, the same counts as the author's step 9 receipt | `receipts/head/ctrl_boundary.{log,rc}` |

The composition's own red, and the fix in `3bebf03a`:
- `python3 -B scripts/check_py_idiom.py` at the head: rc 0, `long module: 10 <= 10` (`receipts/head/py_idiom.*`).
- Probe: I put `d395f682`'s 1,001-line `build.py` into the tree and re-ran the gate. It refuses with `FAIL: long module 11 > ratchet 10` and rc 1 (`receipts/probes/py_idiom_at_d395f682_build.*`). The head's bytes were then restored.
- The rewrap keeps the comment's words: their sha256 is identical before and after (`receipts/rewrap_check.txt`).
- `build.py` line counts: 997 at `7f50ee6a`, 1,000 at `cec88385`, 1,001 at `d3202fa2`, 1,000 at `3bebf03a`.
- The file's longest line is 120 columns, within `MAX_COLUMNS = 120` (`scripts/check_py_idiom.py:155`).
- `docs_check.py`: 0 findings across 219 md files (`receipts/head/docs_check.*`).

## 3. ROM ledger at every point, and the load

Figures are from the author's published receipts at `3bebf03a`, hash-verified (section 5):
- `gates/lane/plat_ledger.log:23-35`: `plat_ledger: PASS`, 7 of 7 controls as required;
- `gates/lane/fixtures.log`;
- `harness/final-3bebf03a/images.txt`.

| Image, point | rom B | RAMB36 | Limit | Holds |
|---|---:|---:|---:|---|
| fixture 1x1/1if, 1x1/2if, 8x8/1if | 108,920 / 110,624 / 122,464 | 38.5 / 41.5 / 51.5 | 56 | yes |
| fixture 8x8/2if | 124,136 (in 124,928) | 58.5 | 58.5 | yes, 792 B before the next granule |
| harness arm A / `answering-ports` / `answering-every-port`, 8x8/2if | 124,136 / 124,320 / 124,452 | 58.5 each | 58.5 | yes, 792 / 608 / 476 B under |
| harness arms at 1x1/1if | 108,920 / 109,104 / 109,244 | 38.5 each | 56 | yes |
| platform 1x1/1if, 1x1/2if, 8x8/1if | 113,984 / 115,712 / 127,568 | 39.5 / 43.0 / 53.0 | 56 | yes |
| platform 8x8/2if | 129,272 (in 131,072) | 60.0 | 60.5 (entry 60.0, `sw/litex/ctrl_memory.py:260-266`) | yes, `POINT 8x8-if2 ... PASS` |

- Each harness ELF at `3bebf03a` is byte-identical to `d3202fa2`'s, so the comment rewrap changed no generated code.
- **Load:** I ran `load_grade.py --check` at the head: rc 0. It reports `HELD 1x1/1if at the pin: the load 0.501, its ceiling 0.70` and `... with tsn-c-stack#32 ... 0.499` (`receipts/head/load_check.*`). The author's head log equals the `cec88385` log except for its first (head) line.
- **Arithmetic:** I re-checked every delta and margin in `SPLIT_CONTROL_MEMORY.md:358,473-482,513` and in the plat and split-boot READMEs against these receipts. Each one agrees. For example:
  - fixture 1x1/2if: 110,624 - 110,592 = 32 B past its banks, one 2 KiB granule more, 41.5;
  - platform 8x8/2if: 129,272 - 129,024 = 248 B past its banks, 60.0.

## 4. Round 1's plants, still caught by name at the head

From the author's receipts at `3bebf03a`, both rc 0 and hash-verified:
- `gates/wf/rtl-fast__firmware-aecp-mutants__ci_step_9.log`: 236 `[ok]`, 0 non-ok. Each of the nine `face-as-path-*` plants is `[ok]`, caught by its named test (`Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow`, `Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt`, `Face.AnUnansweredAsPathWordFailsItsPortThere`, `AppFace.AnAsPathChangeNotifiesTheDatapathsSequence`).
- `gates/wf/rtl-fast__firmware-control-mutants__ci_step_9.log`: `mutants: 699 of 699 caught`, including `[ok] mutant plat-as-path-unavailable (platboot1, platboot2)`.
- Source check: `aecp_mutants.py` holds nine `face-as-path` names and `plat_mutants.py:195` holds `plat-as-path-unavailable`. Both files are unchanged since `5e6fef3e`.

## 5. The full pass's receipts

- **Packet integrity:** I extracted archive `cd983efb` (branch `897-review-evidence`, `review-evidence/897-r1/author-r2`) into scratch and checked every row of `receipts/INDEX.md` (`scripts/verify_index.py`, output in `receipts/packet_index_verify.txt`). 569 rows match by size and sha256, no file is unlisted, and 4 rows mismatch (F3).
  - The packet commit carries no cryptographic signature. Its integrity rests on that index and the published commit id.
- `gates/verify-table.md:369`: `139 steps ran, 226 not run with a reason, 0 bad`. Each of the 139 `gates/wf/*.rc` reads 0, at head `3bebf03a` per each log's first line.
- **Sweep:** 62 suites PASS, 0 FAIL, and 3 were killed by the wall clock (`sweep/shard-*/summary.log`). Each of the three was re-run alone at `3bebf03a` and passed with 0 in-suite failures (`sweep/rerun*/*.tally.txt`):
  - milan_dp: 13,878 checks;
  - milan_dp_render: 347 checks;
  - mmcm_servo: 320 checks.
- **Lane gates:** `test_builder.log` reads `ALL GATES PASS EXCEPT 2 NOT RUN`, rc 0, and its index row verifies. The split boots, behave, coverage, hooks and target self-tests are rc 0, as the hand-off states.

## Findings

**F1 - RESIDUE - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:473`**
- Evidence: the new paragraph opens "**At this branch's head, the merge of `dev-soft-core` `cec88385` ...**". It comes straight after line 460's paragraph, which the base brought in and which also opens "**At this branch's head, the merge of the pin move's round 4 head ...**". The two paragraphs give different figures for the same points.
- Impact: once the branch lands in `dev-soft-core`, a reader has two "this branch's head" blocks and must infer from order that the second is current. No figure is wrong.
- Exact fix: open line 473 with "**At the merge of `dev-soft-core` `cec88385` with GET_AS_PATH read through the face's GSI window**".
- Verification: `docs_check.py` 0 findings, and line 473 no longer reads "this branch's head".

**F2 - RESIDUE - Docs - PR #898 body, lines 27-28 and 147-148**
- Evidence: the reviewer lines and the checklist read "round 2 to be assigned". Round 2 was assigned to one internal reviewer, R833-2, at issuecomment-6863428399 on this PR.
- Impact: PR text only.
- Exact fix: name R833-2 at `3bebf03a` on the internal line. State the external line as the manager's assignment for this round records it.
- Verification: the manager's PR-body update.

**F3 - SUGGESTION - Docs - evidence archive `cd983efb`, `review-evidence/897-r1/author-r2/receipts/INDEX.md`**
- Evidence: four files are each 8 B shorter than their index row, and their sha256 differs:
  - `gates/wf/docs__docs-gates-1__gate_25_0.log`
  - `gates/wf/docs__docs-gates-2__gate_25_1.log`
  - `gates/wf/elaborate__elaborate-gates-0__gate_15_0.log`
  - `gates/wf/elaborate__elaborate-gates-1__gate_15_1.log`
- Each of the four carries a `<home-path>` token in its compiler line, and no other packet file does. So these four files were redacted for privacy after the index was generated.
- Why SUGGESTION: the four logs are builder-gate legs. The same gates are covered by `gates/lane/test_builder.log`, whose row verifies (`ALL GATES PASS EXCEPT 2 NOT RUN`, rc 0). The four `.rc` rows verify and read 0, and no claim at this head rests on these files alone.
- Optional outcome: regenerate the index after redaction, or list the redacted files beside it, as this packet's `receipts/REDACTIONS.txt` does.
- Verification: `python3 -I scripts/verify_index.py <INDEX.md> <author-r2 dir>` reports `bad=0`.

**F4 - SUGGESTION - Docs - `tb/verilator/ctrl_service_budget/build.py:124-126`**
- Evidence: the rewrapped lines run to 120, 116 and 119 columns. The rest of the comment block wraps at about 85-99 columns. This is within the 120-column rule, but the block now has two widths.
- Optional outcome: a later edit that shortens the comment by a line could rewrap the block at one width. Nothing needs to change now; the 1,000-line limit leaves no slack.

**Comment rule.** The delta's only source-comment change is `build.py:122-130`, and its words are unchanged. It cites `#897`, `aecp.c` and `MAILBOX_SPLIT.md:523`, and no lane label, round, reviewer ID or comment ID. No new RESIDUE.

## Prior public findings at this head

| Prior item | Status at `3bebf03a` | Evidence |
|---|---|---|
| R833-1 S1 (SUGGESTION, Tests/Robustness): the answering arms' path stand-ins answer an empty sequence (`build.py:142,193`) | Retained as SUGGESTION, unchanged | `build.py:144-152,195-200` at the head; PR body line 136 still states the limit |
| R833-1 O1 (observation): `plat/README.md:139` said "plans 58.5, within the 59.0" | Resolved | `plat/README.md:139` now reads "plans 60.0 RAMB36, the 60.0 ... refused at 60.5", which matches `plat_ledger.log:34` |
| R834-1 SUGGESTION (RTL/Tests): no executable check of the firmware's kind 2 read on the split RTL | Retained as SUGGESTION. The delta changes neither side | no `hdl/` hunk in the branch; `aecp_face.c` unchanged since `5e6fef3e` |
| R834-1 SUGGESTION (Robustness): a datapath reset between the count read and the entry reads | Retained as SUGGESTION, unchanged | as above |
| R834-1 SUGGESTION (Docs): the every-port arm's 123,756 B had no published build receipt | Resolved | the figure is replaced by 124,452 B (`SPLIT_CONTROL_MEMORY.md:358`), receipted in `harness/final-3bebf03a/images.txt:4` (index row verifies) |

## Per-lens results

- [R833] PASS Conformance — `receipts/merge_sides.txt`; `git diff 5e6fef3e 3bebf03a -- sw/firmware/ctrl/aecp sw/firmware/ctrl/plat/ctrl_plat.c` (only `aecp_mbx.h:18-29`, a cost constant outside GET_AS_PATH); the AECP and control campaign logs at `3bebf03a`. Round 1's verdict against IEEE 1722.1-2021 7.4.41, Table 7-141 (as the ruling amends it) and Milan v1.2 5.4.2.24 / Table 5.22 holds, because the GET_AS_PATH sources the merge carries are byte-identical in their hunks. Acceptance 1-4 are met; acceptance 5 belongs to the bench lane.
- [R833] PASS RTL — no `hdl/` hunk in the branch's 16 files; #810's `KL_mbx.sv` hunks have no GSI, face or AS_PATH line; `tb/verilator/mbx/suite_face.hpp:410,547-584,666` (the GSI window, AS_PATH event) are in the sweep at `3bebf03a` (`sweep/shard-*/summary.log`, 65 of 65 after re-runs); the split boot at three points is ready (`gates/lane/boot_*.log`). Round 1's RTL verdict depends on nothing the delta changed.
- [R833] PASS Robustness — the ledger at every point (section 3 table: `plat_ledger.log:23-35`, `fixtures.log`, `harness/final-3bebf03a/images.txt`). Every image is within its limit, the two 8x8/2if entries are exactly at their tiles, and half a tile more is refused (plat_ledger control `past-its-tiles`). The load, 0.501 against 0.70, is my own run (`receipts/head/load_check.log`).
- [R833] PASS Tests — my own runs at the head: cpp idiom, py idiom, hooks self-test and firmware boundary, each rc 0 (`receipts/head/`). Mutation probe: the py idiom refuses the pre-rewrap `build.py` (`receipts/probes/`). Round 1's ten plants are caught by name in the campaign logs at `3bebf03a`.
- [R833] PASS Docs — `SPLIT_CONTROL_MEMORY.md:358,473-482,513`, `plat/README.md:113,139` and `ctrl_split_boot/README.md:112`, checked against the receipts' figures (all agree). `docs_check.py` reports 0 findings (`receipts/head/docs_check.log`), and `git grep` finds no stale round-1 figure left in a current-tense sentence. F1 and F2 are RESIDUE and F3 and F4 are SUGGESTION, so none leaves the lens unclean.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merge hunk comparison over 16+150 files; `aecp_face.c`/`ctrl_plat.c` unchanged; AECP campaign 236/236 and control 699/699 logs | R833-2 | 3bebf03a1d25bcbde9c0ec48dfd711af7280131e |
| RTL | CLEAN | branch `hdl/` diff (empty); #810 mailbox hunks (no GSI/face line); mbx `suite_face.hpp` in the passing sweep; split boot at 1x1/1if, 8x8/1if, 8x8/2if | R833-2 | 3bebf03a1d25bcbde9c0ec48dfd711af7280131e |
| Robustness | CLEAN | `plat_ledger.log` 4 points and 7 controls; `fixtures.log`; harness `images.txt` 6 builds; `load_check.log` (own run) | R833-2 | 3bebf03a1d25bcbde9c0ec48dfd711af7280131e |
| Tests | CLEAN | own runs of cpp idiom, py idiom, hooks self-test, ctrl_boundary; py-idiom mutation probe; plants by name | R833-2 | 3bebf03a1d25bcbde9c0ec48dfd711af7280131e |
| Docs | CLEAN (F1, F2 RESIDUE; F3, F4 SUGGESTION) | `SPLIT_CONTROL_MEMORY.md` sections 5-6, `plat/README.md`, `ctrl_split_boot/README.md`, `build.py:122-130`, PR body, packet INDEX | R833-2 | 3bebf03a1d25bcbde9c0ec48dfd711af7280131e |

## Real limits

- I ran no manager source bank, and none is claimed or inferred. My own executions are the four gates, the load check, docs_check and the py-idiom probe in section 2. Every other figure comes from the author's published receipts, verified against their index (F3 lists the four exceptions).
- I did not re-run the AECP, control or SRP campaigns, the sweep, the harness legs, `plat_ledger.py` or the builder. They are accepted from hash-verified receipts at `3bebf03a`.
- The harness's full legs were not re-run at this head (PR body line 136). The fresh builds ran sampled groups.
- The mmcm_servo re-run's head line reads `DIRTY 2`. The two dirty files are the suite-written `TEST_RESULTS.md` pair that `sweep/clones-after.txt` records in shard 3's clone. They are not inputs to mmcm_servo.
- `flip_grade.py --check` exits 1 at `cec88385` and at the head, with identical output. It is no merge gate.
- Hosted CI does not run on split PRs.
- Physical calibration was NOT RUN. Field skips are not hardware proof, and acceptance 5 (the bring-up board) is not evidenced here.
- My restore check (`receipts/restore_check.txt`) found HEAD and the index tree equal to `3bebf03a`/`172d19ad`, no worktree or index difference, no untracked or ignored file, and the six submodule gitlinks unchanged.

## Pending manager duties

- Validate the current-dev merge candidate (source base `7f50ee6a`, live dev `b7d692952305e4e0e132abb8f99c339eeb17a873`) with the builder and native banks, and link the receipts on the PR.
- Own hosted and act acceptance.
- Carry F1 and F2 to the residue checklist, and update the PR body's reviewer lines (F2).
- Decide whether round 2 needs an external review; the PR body still lists one "to be assigned".
- Optionally republish the packet index after redaction (F3).
- Obtain maintainer authorization before any merge.

R833-2 FINISHED
