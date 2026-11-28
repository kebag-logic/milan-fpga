[R958] POSITIVE - exact head 25132e3029557d2d992dc42f2a77c6840e5c05d3

R958-7 is a narrow re-review of one commit, `a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35..25132e3029557d2d992dc42f2a77c6840e5c05d3`, the merge of `dev-soft-core` into the PR branch. Tree: `222e3e20fa0f6313632775aabf4f74a26c4417fc`. **The merge commit changes no byte: its tree is the tree R958-6 reviewed at `a5b19f70`.** All five lenses are CLEAN at this head. No new BLOCKER, MAJOR or MINOR. One new RESIDUE (PR body). Of the four requested checks, (1) and (3) hold; (2) holds for the tree but its candidate is unverified; (4) is wrong as worded, though what it protects holds. Neither point changes a lens.

Reconstruction followed AGENTS.md and CONTRIBUTING.md (step 7, candidate merge; the one-line commit rule), the commit object and both parents, the per-path state of PR #1015's delta, then public evidence. The independent pass and the interim verdict were written before the public thread and the prior reports were read. No private author material, lane scratchpad or other checkout was read. R957-5 runs in parallel and was not consulted.

**The four requested checks**

| Check | Result | Evidence |
|---|---|---|
| (1) Parents are exactly `a5b19f70` and `0b594023`, the live `dev-soft-core` | **HOLDS** | Parent 1 `a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35`, parent 2 `0b5940237e8de8bd5912db87e5e036a78f59b5a6`, no third. The live remote `dev-soft-core` and `refs/pull/993/head` read `0b594023` and `25132e30` at review time. `receipts/verify_base_merge.log`, section C1. |
| (2) Tree is `222e3e20`, the same as candidate `75d1fcbf`, validated by both banks and egress | **HOLDS for the tree; the candidate and its bank results are NOT VERIFIED** | Tree(head) = tree(`a5b19f70`) = `222e3e20`. The hosted test merge `37aec182` (parents `0b594023`, `25132e30`) has the same tree, and replaying the merge of `a5b19f70` with `0b594023` yields it without conflict. So a mechanical merge of these two commits has tree `222e3e20`. The object `75d1fcbf` is in neither the clone nor the hosted repository, and no PR comment, issue comment or file at the evidence branch tip `a357189b` names it. Its identity and the banks' exit status are the manager's statement, pending published receipts. `receipts/candidate_lookup.log`, `receipts/hosted_test_merge.json`. |
| (3) The gitlink resolves to `5a07d9b7`, which contains `c3bff8f3` | **HOLDS** | `third_party/tsn-c-stack` is `5a07d9b7d87298f04b15aa28f0304ec88b0aef81` at the head and at `a5b19f70`, and `c3bff8f3dea03870ea7ae62965db360b509ee3b3` at `0b594023`. In the submodule `c3bff8f3` is an ancestor of `5a07d9b7` (six commits later, the merge of tsn-c-stack PR #41), and `5a07d9b7` is reachable from the public `main` `bf02d817`. PR #1015's tsn-c-stack change is kept. Section C3. |
| (4) The diff `a5b19f70..25132e30` is exactly PR #1015's delta and does not touch #977's files | **First clause DOES NOT HOLD as worded; the property it protects holds, more strongly** | The diff is **empty** (0 raw entries, identical trees), not PR #1015's 27-path delta. `a5b19f70` already contained both parents of `0b594023`: `71bad8c0` through the branch merge `8d573763`, and PR #1015's head `35d29eb7` through `aad9a682`. The base tip added one commit to the branch's history, `0b594023` itself, and that merge is mechanical (replaying `71bad8c0` with `35d29eb7` gives its tree `2dc4b2ce`). Second clause holds trivially: no file is touched. Section C4. |

What check (4) is for is met. Nothing enters the head through this commit, and PR #1015's delta is present in the head's tree:

- 13 of PR #1015's 27 paths are byte-identical at the head to `dev-soft-core`'s tip. These include `adp_mbx.c`, `adp_mbx.h`, `ctrl_plat.c`, `test_adp.cpp`, `adp_first_mutants.py`, `model_counts.py` and `cosim_main.cpp`.
- 14 paths were changed again on the branch after it merged PR #1015's head: 12 text files, the regenerated PNG and the gitlink. Every line PR #1015 added to the text files is verbatim at the head except ten. Seven follow from the pin value, moved from `c3bff8f3` to `5a07d9b7`: three lines of `SUBMODULES.md`, the diagram's `.drawio` and `.svg` lines, and the PNG manifest's two hashes of that regenerated diagram. Three are comment lines in `test_plat_boot.cpp` that lost only their bench-label prefix, in `8ffdea83`. All were in the tree R958-6 reviewed. `receipts/pr1015_retention.log`.

The correction matters for one reason. A published description of this commit must say "tree-identical to `a5b19f70`; PR #1015 was already merged into the branch", not "the diff is PR #1015's delta". Per CONTRIBUTING step 7 the reviewed head now directly descends from the unchanged base, so its tree is the candidate merge tree for `dev-soft-core`.

**New item**

- **R958-7-R1; RESIDUE; Docs; PR #993 body, Status ("Ready for review at `a5b19f70`").** Authority: AGENTS section 6, Docs lens ("The PR and Issue contain enough evidence for another cold reviewer"). Evidence: the live body names `a5b19f70` as the head and nowhere names `25132e30` or the base merge; every round-14 receipt is named for `a5b19f70`. Impact: a cold reader cannot tell from the PR text that the receipts apply to the head. No measurement, figure, verdict, test, code or clause claim changes, because the trees are identical. Exact fix, appended to Status: "The head is `25132e30`, the merge of dev-soft-core `0b594023` into `a5b19f70`. Its tree `222e3e20` is `a5b19f70`'s, so every round-14 receipt stands at the head." Verification: compare the two trees' object IDs and read the line in the published body. The manager carries this to the residue checklist.

**Prior findings at this head**

Every blob is the one R958-6 judged, so each disposition carries over unchanged.

| Finding | Disposition at this head | Verification |
|---|---|---|
| R958-4-F1 (MAJOR, Conformance), R958-4-F2, R958-4-R1, R958-4-R2, R958-5-R1 | Remain CLOSED, as R958-6 recorded | Tree identity with `a5b19f70`; `flip_grade.py` and `load_grade.py` blobs `12205895` and `a364a2a1` unchanged. |
| R957-4-R1 (RESIDUE, Docs) | Remains CLOSED | The delta adds no source line. |
| R957-4-R2 (RESIDUE, Docs), PR #993 body, Round 11 table, deliveries-term row | **Retained** | The live row still reads "internal review F1, option (a)". Exact fix as before: "the round-2 internal review's F1, option (a)". |
| R957-4-R3 (RESIDUE, Docs), `tb/verilator/ctrl_service_budget/load_grade.py:382` | **Retained** | The comment still calls DELIVERY_MEASURED the gate's floor. Exact fix as R958-6 gave it: "plus 5 %, rounded up to 5 us; DELIVERY_MEASURED holds the cycles, and their figure by the rule is the gate's floor: a cost stated under it is refused". |
| R957-4-S1 (SUGGESTION, Tests), `load_grade.py:963-965`, `selftest_mutants.py:539-541` | **Retained**, optional | No sibling control for an unnamed load escape. |
| R957-4-S2 (SUGGESTION, Tests), `selftest_mutants.py:539`, `flip_grade.py:460-467` | **Retained**, optional | The 0.71 plant is still checked through the combined adapters. |

Comment rule: the delta adds no source comment, so there is no new instance of a bench label, lane name, review round, reviewer ID or comment ID. The commit subject is one line with no trailer.

**Reviewer-owned lens ledger**

[R958] PASS Conformance - `git diff --raw a5b19f70 25132e30` (0 entries); `docs/reference/FR_NFR.md` (PR #1015's four added lines verbatim at the head); gitlink `third_party/tsn-c-stack` `5a07d9b7` containing `c3bff8f3` - no acceptance artifact of #977 moves, and #970's ADP seeding on the base is kept, in the firmware adapters byte for byte and in the stack by ancestry.

[R958] PASS RTL - `receipts/verify_base_merge.log` C2 and C3; PR #1015's path list (no path under `hdl/`); gitlinks `gptp-processor` `3ce71b76`, `protocol-processor` `801ef228`, `third_party/verilog-axis` `48ff7a7e` - no RTL, interface, build recipe or processor pin differs from `a5b19f70`. Against the base tip only `third_party/lwSRP` and `third_party/tsn-c-stack` differ, both the PR's own reviewed pins (`receipts/pins_and_docs.log`).

[R958] PASS Robustness - replayed merges (`71bad8c0` with `35d29eb7` gives `2dc4b2ce`; `a5b19f70` with `0b594023` gives `222e3e20`); hosted test merge `37aec182`; `receipts/exact_head_gates.log` - the two merge bases are enumerated and both replays are conflict-free, no conflict marker is in the tree, and `git diff --check` is clean against `0b594023` and `71bad8c0`.

[R958] PASS Tests - `sw/firmware/ctrl/test/test_adp.cpp`, `adp_first_mutants.py`, `ctrl_mutants.py`, `test_plat_boot.cpp`; `tb/verilator/ctrl_service_budget/model_counts.py`, `scenario.py`, `run.py`; `receipts/pr1015_retention.log` - PR #1015's tests and plants are at the head, verbatim or with every added line present bar three de-prefixed comments. #977's tests are the blobs R958-6 exercised. No test is weakened or dropped by the merge.

[R958] PASS Docs - `docs/reference/SUBMODULES.md:27,1281,1326`; `docs/diagrams/submodule_boundaries.svg:84`; `CHANGELOG.md` (verbatim to the base tip); the commit object; the live PR body - the documented stack pin equals the gitlink, PR #1015's changelog and document lines are kept, and the commit message meets the one-line rule. R958-7-R1 is wording only.

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Empty raw diff; FR_NFR retention; stack gitlink ancestry | R958-7 for the merge commit; R958-6 for the unchanged tree | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |
| RTL | CLEAN | Tree and gitlink identity; PR #1015 path list; base-relative gitlinks | R958-7 for the merge commit; R958-6 (retaining R958-5) for the unchanged tree | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |
| Robustness | CLEAN | Merge bases; both replays; hosted test merge; marker and whitespace checks | R958-7 for the merge commit; R958-6 (retaining R958-5) for the unchanged tree | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |
| Tests | CLEAN | Per-path retention of PR #1015's tests; unchanged #977 test blobs | R958-7 for the merge commit; R958-6 (retaining R958-5) for the unchanged tree | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |
| Docs | CLEAN | Pin text against gitlink; changelog; commit message; live PR body | R958-7 for the merge commit; R958-6 for the unchanged tree | 25132e3029557d2d992dc42f2a77c6840e5c05d3 |

Under AGENTS section 7, R958-6's coverage at `a5b19f70` stays banked: that head is an ancestor of the merge candidate and nothing in any lens's scope has changed since.

**Limits and pending manager duties**

- **Nothing was executed against product code in this round.** No build, simulation, bank, synthesis or hardware ran. The round is git-level: object identity, ancestry, merge replay, per-path blob comparison, and three text checks. Execution evidence for tree `222e3e20` is the author's round-14 receipts and R958-6's focused gates, both taken at `a5b19f70`.
- **The base-relative em-dash gate was NOT RUN here.** `scripts/check_em_dash.py --base 0b594023` stopped with rc 2 because its pinned Markdown renderer is not installed in the review environment. Its answer depends only on the two trees, which are those of the author's round-14 run, and the hosted `docs` workflow is running at this head.
- **Candidate `75d1fcbf` is unverified by this review**, as in check (2). There is **no manager source bank at this exact head**, and none is claimed or inferred.
- **Hosted checks at the exact head were in flight** when sampled at 2026-11-28T11:16:39Z. Workflows `elaborate`, `docs`, `rtl-fast` and `rtl-full` started on the `pull_request` event. Six jobs had completed with success (`changes`, `full-ci-gate`, `bdd-conformance`, `docs-check-no-git`, `docs-gates-4`, `wire-accountability`), 20 were in progress and 39 queued. `Physical gPTP (nightly and manual)` is **skipped**, not executed. No hosted verdict is asserted; the manager owns hosted and local-replica acceptance. `receipts/hosted_check_runs_25132e30.tsv`.
- The PR reads `MERGEABLE` against base `0b594023`, merge state `BLOCKED`. Why the previous head read as conflicting was not investigated. This review establishes only that the base tip was not an ancestor of `a5b19f70` and is one of `25132e30`.
- The final then-current-`dev` candidate (supplied live `dev` `e275d7950ef3385753e6a15d2e191ba855b171ed`) is a different tree from this source head. Its builder and native banks, published receipts, the review-bar accounting, explicit merge authorization, containment and issue completion remain manager duties.
- Physical calibration is **NOT RUN**; field skips are not hardware proof.
- The evidence commit's signature status is unchanged from R958-6 (unsigned; hash integrity only) and was not re-examined.
- Checkout preservation: 1997 superproject blobs and 1377 blobs across five initialised submodules were re-hashed against the index, with modes, index tree and gitlinks matching the head. `external` stays uninitialised with its gitlink preserved. No file in the clone was edited. `receipts/verify_checkout.log`.

Reproduce from an exact clone with `bash scripts/verify_base_merge.sh <clone> --net`, `python3 -I scripts/pr1015_retention.py <clone>` and `python3 -I scripts/verify_checkout.py <clone>`. Only REPORT.md and the files in MANIFEST.sha256 are publication artifacts; scratch is excluded.

R958-7 FINISHED
