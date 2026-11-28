[R957] POSITIVE - exact head 25132e3029557d2d992dc42f2a77c6840e5c05d3

R957-5 is the internal review of issue kebag-logic/milan-fpga#977 / PR #993. It ran in a cleared context at exact head `25132e3029557d2d992dc42f2a77c6840e5c05d3`, tree `222e3e20fa0f6313632775aabf4f74a26c4417fc`. All five lenses were applied, each against artifact-specific evidence.

The reviewed delta is `a5b19f70..25132e30`, one base-merge commit. I also covered the four #977 commits `3256d1d2..a5b19f70`, for the reason in section 2.

- **No BLOCKER, MAJOR or MINOR finding is open.**
- One new RESIDUE (R957-5-R1, the PR status line).
- Two RESIDUE items are retained from round 4 (R957-4-R2 and R957-4-R3).
- Two optional suggestions are retained (R957-4-S1 and R957-4-S2).

## 1. What the base merge is, and the four checks

The merge is commit `25132e30`, "Merge dev-soft-core into the Talker registration branch". It has one line and no trailers (CONTRIBUTING.md:404).

**(1) Parents: HOLDS.**
- The parents are exactly `a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35` and `0b5940237e8de8bd5912db87e5e036a78f59b5a6`.
- `0b594023` is the live `dev-soft-core`. I read it with `git ls-remote` during this round, and `refs/pull/993/head` is `25132e30`.
- Receipt: `receipts/verify-base-merge.txt`.

**(2) Tree: HOLDS, by recomputation.**
- The head's tree is `222e3e20`.
- `git merge-tree --write-tree a5b19f70 0b594023` recomputes exactly that tree, with rc 0 and no conflict.
- `0b594023` is GitHub's merge of PR #1015. Its parents are `71bad8c0` and `35d29eb7`, PR #1015's head. Its tree, `2dc4b2ce`, is exactly the clean merge of those two parents, so it adds no content of its own.
- Both of its parents are already ancestors of `a5b19f70`:
  - `71bad8c0` came in through `8d573763`;
  - `35d29eb7` came in through `aad9a682`, "Merge PR #1015's head 35d29eb7 … into #977's lane".
- So the only correct result of this merge is `a5b19f70`'s own tree, and that is what the commit carries.
- **Limit:** the merge-train candidate `75d1fcbf` is not publicly resolvable. The commits API answers "No commit found", and no PR or issue comment names it. I therefore cannot confirm that its tree is `222e3e20`, or its bank results. That stays the manager's published claim (section 6).

**(3) The tsn-c-stack gitlink: HOLDS.**
- The head pins `5a07d9b7d87298f04b15aa28f0304ec88b0aef81`, the same as `a5b19f70`. `0b594023` pins `c3bff8f3dea03870ea7ae62965db360b509ee3b3`.
- `c3bff8f3` is an ancestor of `5a07d9b7`, six commits behind it. The path runs through `5d03517f`, "Merge main c3bff8f3 (PR #40) into 977-settle", and then PR #41's merge.
- `5a07d9b7` is reachable from tsn-c-stack `main`.
- `docs/reference/SUBMODULES.md` states it: line 27 is the pin row, and lines 1206 to 1269 say "It holds PR 40's merge on `main`, `c3bff8f3`".
- So #1015's tsn-c-stack change (the ADP delay seeded on each transition out of DOWN) is kept.

**(4) The delta: the substance HOLDS. The brief's literal wording does not match the repository.**
- The brief says the diff `a5b19f70..25132e30` is exactly #1015's delta. In fact that diff is **empty** (0 bytes).
- The reason: #1015's content was already in the lane, through `aad9a682`, before `a5b19f70`. Adding the base therefore changes no byte. The base merge does not touch #977's files, or any other file.
- The property the check exists for, that #1015 is kept at the head, I verified directly over its 27 files (`receipts/verify-base-merge.txt`, `receipts/pr1015-files-at-head.txt`):
  - **14 files are byte-identical to `0b594023`.** They include every #1015 product and test file: `adp_mbx.c/.h`, `ctrl_plat.c`, `test_adp.cpp`, `adp_first_mutants.py`, `ctrl_configs.py`, `model_counts.py`, `hooks.py`, `cosim_main.cpp`, CHANGELOG and the audit page.
  - **13 files differ from `0b594023` only by #977's own later commits.** These are the pin documents and the regenerated submodule diagram (`9380ff82`), `test_plat_boot.cpp`'s inter-tick `pass_ms(0)` and the removal of bench labels from #1015's comments (`3b944823`, `8ffdea83`), the budget harness (`ddf5c568`, `d8e12c16`, `09599524`), `ctrl_mutants.py` (`6e2c9116`), and the gitlink.
  - Every one of those lane commits is an ancestor of `3256d1d2`, except the two document edits in `3256d1d2..a5b19f70` (section 2).
- Reverse-applying #1015's delta to the head's index fails only on those pin- and lane-edited files (`receipts/pr1015-contained.txt`). That is the expected signature of a later lane edit, not of a lost change.

**GitHub's state.** PR #993 now reads `mergeable: MERGEABLE`, `mergeStateStatus: BLOCKED` (required reviews and checks). The CONFLICTING state described in the brief is cleared.

## 2. Coverage gap in the brief, closed in this round

The brief says "your report at a5b19f70 stands". But this reviewer's last public verdict is R957-4, **POSITIVE at `3256d1d2`** (PR comment 7230545660). No R957 report at `a5b19f70` is public. The other reviewer covered `a5b19f70`.

Under AGENTS.md section 7, a ledger banked at `3256d1d2` does not reach the merge head if a later commit touched that lens's scope. So I covered `3256d1d2..a5b19f70` here: four commits, five files, +27/-24 lines.

- **Executable code.** `flip_grade.py`, `load_grade.py` and `load_deliveries.py` have equal executable ASTs (docstrings stripped) at `3256d1d2` and `25132e30` (`receipts/ast-delta-3256d1d2-25132e30.txt`, rc 0). `FLIP`, `RULED_FLIP` (both `{'8x8/2if': 0.70, '8x8/1if': 0.79}`) and `EDGE_1IF = (0.790, 0.791)` (`flip_grade.py:69-76`) are unchanged. Only comments and docstrings moved.
- **Ceiling authority.**
  - The owner's decision of 2026-11-28 ([#977 comment 7235670586](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7235670586)) raises the 8x8/1if ceiling to 0.79 and leaves every other bound unchanged.
  - `docs/reference/FR_NFR.md:427` and `docs/design/SPLIT_CONTROL_MEMORY.md:2548` link it in place of "owner decision pending".
  - `flip_grade.py:26,67` and `load_grade.py:135` cite it by date.
  - This satisfies item 4 of the manager's deferred-deliveries decision (7229657853): cite the owner's answer, never "pending", before merge.
- **The new sentence in section 13.** `SPLIT_CONTROL_MEMORY.md:2548` (and its twin at `load_grade.py:380-381`) adds "each record from its own tagged receive commit on SRP's channel, 44 records at each point …, a record with no such commit, more than one, or one on another channel would be refused". The published receipts back it:
  - `author-r13/receipts/meas/deliv13-{1x1,8x8-1if}-e59cf6ea.txt` show "RECORDS …: 44 measured, each at its own tagged commit; 6 transmit-only aliases excluded".
  - `deliv13-selftest.txt` shows the missing, doubled, wrong-channel and misplaced-commit refusals, 8 of 8 controls.

## 3. Findings

### New

**R957-5-R1 - RESIDUE - Docs - the live PR #993 body, "Status" (line 18): the PR text still describes `a5b19f70` as the head and does not mention the base merge.**
- **Authority/evidence:**
  - The live body reads "**Ready for review at `a5b19f70`.**" The PR head is `25132e30`.
  - No PR text or comment says that `25132e30` merges dev-soft-core `0b594023` (PR #1015). None says that its tree is `a5b19f70`'s, which is what lets the round-14 receipts keyed to `a5b19f70` stand at the head.
  - AGENTS.md section 6, Docs: "The PR and Issue contain enough evidence for another cold reviewer."
- **Impact:** wording only. A cold reader has to rediscover from git why receipts named for `a5b19f70` apply to `25132e30`. No measurement, figure, verdict, test, code, generated artifact or clause claim changes, and no privacy rule is touched.
- **Exact fix:** replace the opening sentence of Status with: "**Ready for review at `25132e30`**, the merge of dev-soft-core `0b594023` (PR #1015's merge) into `a5b19f70`. Its tree, `222e3e20`, is `a5b19f70`'s: PR #1015's head `35d29eb7` was already in this lane through `aad9a682`, and tsn-c-stack `5a07d9b7` contains #1015's `c3bff8f3`, so every round-14 receipt keyed to `a5b19f70` holds at the head."
- **Verification:** read the live PR body.

### Prior findings at their causes

I resolved these only after my own pass over the delta and the four checks above.

| Finding | Status at `25132e30` | Evidence |
|---|---|---|
| R957-4 Conformance qualifier: "judged at 0.79; the owner's answer is pending" | **Resolved** | Owner decision 7235670586 approves 0.79. It is cited at `FR_NFR.md:427`, `SPLIT_CONTROL_MEMORY.md:2548`, `flip_grade.py:26,67` and `load_grade.py:135`. Author receipt `author-r14/receipts/meas/load-flip-a5b19f70.txt` (same tree) gives 8x8/1if 0.782 within 0.79 and 1x1/1if 0.533 within 0.70, rc 0. With FLIP at 0.77 the named controls fire. |
| R957-4-R1 RESIDUE (Docs): four source-comment issue-comment IDs | **Resolved** | `grep -rn 7229657853` over tb, sw, hdl and scripts source finds nothing (`receipts/prior-findings-at-head.txt`). The four sites now name "the manager's decision of 2026-11-27 on deferred deliveries". |
| R957-4-R2 RESIDUE (Docs): live PR body, "The deliveries term (`71503e5a`) … internal review F1, option (a)" | **Retained** | The text is now at line 71 of the live body (it was line 61), unchanged. Exact fix as before: "the round-2 internal review's F1, option (a)". Line 64 carries the same unqualified "internal review F1"; name its round in the same way. |
| R957-4-R3 RESIDUE (Docs): `load_grade.py` attaches `DELIVERY_MEASURED` to the ruled figure | **Retained** | The text is now at `load_grade.py:381-382`, unchanged: "plus 5 %, rounded up to 5 us (DELIVERY_MEASURED, the gate's floor: a cost stated under it is refused)". Exact fix as before: "… plus 5 %, rounded up to 5 us; DELIVERY_MEASURED holds the cycles, and their figure by the rule is the gate's floor: a cost stated under it is refused". This is comment wording only; the code is AST-equal. |
| R957-3-R4 / external round-3 R2 RESIDUE (packet): publish the round-10 and round-11 index notes | **Resolved** | `author-r10/receipts/SUPERSESSION-NOTE.md` and `author-r11/receipts/SUPERSESSION-NOTE.md` are published at evidence commit `d963a0c0`. All 705 manifest entries match (`receipts/evidence-manifest.txt`). |
| R957-4-S1 SUGGESTION (Tests): a planted mutant for the load gate's own unnamed-escape branch | **Retained (optional)** | `selftest_mutants.py:539-540` still guards only the flip-side branch. |
| R957-4-S2 SUGGESTION (Tests): the 0.71 plant is killed through a check that also fails on the pre-fix code | **Retained (optional)** | `selftest_mutants.py:539` is unchanged. |

The other reviewer's public findings on this PR (rounds 4 to 6) are all recorded as closed at `a5b19f70`, in comment 7236305705. This delta changes none of their dependencies, and none is reopened here.

## 4. Lens results at this head

```text
[R957] PASS Conformance - receipts/verify-base-merge.txt; sw/firmware/ctrl/adp/adp_mbx.{c,h}, sw/firmware/ctrl/plat/ctrl_plat.c (byte-identical to 0b594023); FR_NFR.md:427; SPLIT_CONTROL_MEMORY.md:2548; flip_grade.py:69-76; decision 7235670586; author-r14 load-flip-a5b19f70.txt - #1015's ADP random-delay seeding (IEEE 1722.1-2021 6.2.4.2.2, Milan v1.2 5.6.3.5.3, as cited at test_plat_boot.cpp B27) is kept byte for byte; the 0.79 ceiling now carries the owner's answer; the measured loads fit every bound
[R957] PASS RTL - git diff a5b19f70..25132e30 (0 bytes); git diff --name-only 3256d1d2..25132e30 (no file under hdl/ or sw/, no gitlink); merge-tree recomputation; the tsn-c-stack ancestry c3bff8f3 -> 5a07d9b7; receipts/checkout-integrity.txt (5 initialised gitlinks match) - no HDL, firmware product or interface change; product images are as covered at 3256d1d2 (80/80 ELF identity with 25ff0632, author-r14/receipts/elf-identity-a5b19f70.txt, same tree)
[R957] PASS Robustness - receipts/ast-delta-3256d1d2-25132e30.txt; flip_grade.py:69-76 (FLIP, RULED_FLIP, EDGE_1IF); load_grade.py DELIVERY_US/DELIVERY_MEASURED; author-r13 deliv13-selftest.txt - no executable change since the round-4 edge, drift, escape and floor probes, so they stand; the extraction refuses missing, doubled, wrong-channel and misplaced commits, 8 of 8
[R957] PASS Tests - receipts/pr1015-files-at-head.txt (test_adp.cpp, adp_first_mutants.py, ctrl_configs.py, model_counts.py identical to base; the test_plat_boot.cpp and ctrl_mutants.py lane edits predate 3256d1d2); author-r14 gates harness-*-a5b19f70.txt (flip --check 8x8/1if PASS, load --check PASS, selftests) on tree 222e3e20 - no test changed in the delta; #1015's tests are kept; the receipts transfer by tree identity
[R957] PASS Docs - receipts/em-dash-base-0b594023.txt (0 findings over 172 added lines, rc 0) and em-dash-base-a5b19f70.txt (rc 0); receipts/comment-rule-scan.txt (no comment ID, lane label, round or reviewer ID in added source lines); SUBMODULES.md:27,1206-1269; FR_NFR.md:427; SPLIT_CONTROL_MEMORY.md:2548 - the pin documentation states 5a07d9b7 and its containment of c3bff8f3; the new section-13 sentence matches the published receipts; R957-5-R1, R957-4-R2 and R957-4-R3 are residue only
```

## 5. Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | base-merge recomputation; #1015 ADP sources byte-identical to base; owner decision 7235670586 cited in FR_NFR 3.4.1, section 13 and the flip/load sources; load-flip receipt on tree `222e3e20` | R957-5 | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |
| RTL | CLEAN | empty `a5b19f70..25132e30` diff; no hdl/sw/gitlink change in `3256d1d2..25132e30`; tsn-c-stack ancestry; checkout and gitlink integrity; ELF identity receipt (same tree) | R957-5 | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |
| Robustness | CLEAN | AST equality of the three grading scripts since `3256d1d2`; round-4 probes standing on unchanged code; extraction self-test receipt | R957-5 | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |
| Tests | CLEAN (S1, S2 optional) | #1015 test files at head versus base; lane test edits predating `3256d1d2`; author-r14 gate receipts on tree `222e3e20` | R957-5 | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |
| Docs | CLEAN (residue R957-5-R1, R957-4-R2 and R957-4-R3 carried to the checklist) | em-dash gate against `0b594023` and `a5b19f70`; comment-rule scan; SUBMODULES.md pin text; FR_NFR 3.4.1; section 13; live PR body | R957-5 | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |

Every lens is banked at the merge candidate itself. Nothing is banked against an ancestor.

## 6. Real limits and pending manager duties

- **The merge-train candidate `75d1fcbf` is not public.** I cannot verify its tree, or the "both banks + egress exit 0" claimed for it. I verified independently that the head's tree is the clean recomputed merge. Bank results for this tree remain the manager's to publish.
- **No manager source bank runs at this head, and none is claimed or inferred.** The source-head execution evidence is the author's round-14 receipts at `a5b19f70`. They transfer by tree identity: `222e3e20` at both commits.
  - The one gate I found that reads history rather than the tree is the em-dash diff gate. I re-ran it against the new base, rc 0, using the hash-pinned renderer in a private disposable environment.
  - Any other history-reading gate is covered only by the hosted runs.
- **Hosted checks at `25132e30` were still running** at my snapshot (`receipts/hosted-snapshot.txt`): 6 success, 1 skipped (Physical gPTP, nightly/manual), 20 in progress, 39 queued. Hosted and act acceptance, `rtl-fast`, `verilator-suites` and `yosys-portability` at this exact head remain manager-owned.
- **Signatures.** Evidence commit `d963a0c0` is unsigned (public API: `verified=false, reason=unsigned`). Hash integrity of all 705 manifest entries is established; a cryptographic packet signature is not. The merge commit `25132e30` also carries no signature.
- **No hardware proof.** Physical calibration was NOT RUN, and field skips are not hardware proof. I ran no full parent, PP, gPTP, Yosys or builder bank, no Docker/act and no hardware.
- **Manager duties at the merge turn:**
  - the current-dev candidate (source base dev-soft-core, live dev `e275d795`) with builder and native banks;
  - candidate-merge validation and post-merge containment;
  - carrying R957-5-R1, R957-4-R2 and R957-4-R3 to the residue checklist;
  - the second independent positive.
- **Checkout state.** The checkout is restored and verified: HEAD and index tree are `222e3e20`, the worktree was rehashed equal to the index, and there are no untracked files. The five initialised submodules sit at their gitlinks and are clean; `external` is uninitialised with its gitlink unchanged. Temporary probe refs in the tsn-c-stack submodule were deleted (`receipts/checkout-integrity.txt`).

Portable scripts: `scripts/verify_base_merge.sh`, `scripts/ast_delta.py`, `scripts/verify_evidence_manifest.py`. Receipts are under `receipts/`, and `MANIFEST.sha256` lists them.

R957-5 FINISHED
