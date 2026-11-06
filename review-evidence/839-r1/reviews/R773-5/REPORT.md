[R773] POSITIVE - exact head cf4120f4cf6c711781b9e4aa24173691dcce0a95

Round R773-5, issue #839, PR #841. Tree `566fd3ae6acece2e2853310f9ef9e076ae3638a0`. Delta reviewed: `4f210018..cf4120f4`.

Verdict: no open BLOCKER, MAJOR, MINOR or RESIDUE. All three assigned checks hold, and the merge adds nothing beyond the two sides. One SUGGESTION (S1) needs a reader's attention: `tb/verilator/milan_dp/test_sim_pool.py` exits 1 at this head. It is red on dev too, the delta did not cause or change it, and no gate runs it, but the specific defect has no Issue. S1 sets out why it is a SUGGESTION and what would make it a MINOR.

## 1. Reconstruction

Read in order: AGENTS.md, CONTRIBUTING.md (merge, commit and docs rules), docs/README.md, the #839 body and its four acceptance items, then the diff, history and evidence. The prior public findings were read only after the independent pass over the delta. The concurrent R774-5 report was not read: at my last read of the PR only its start comment existed.

## 2. The three assigned checks

### Check 1: the merge keeps both sides. HOLDS

| Evidence | Result | Receipt |
|---|---|---|
| Parents of `19f4c0b4` | `4f210018` and `87e9d03a` | `receipts/01_topology.txt` |
| Independent replay of the merge | Differs from the recorded merge in `docs/DOCUMENTATION_AUDIT.md` only. It conflicts in that file alone, and `docs/testing/TESTING.md` auto-merges | `receipts/02_merge_tree.txt`, `receipts/03_both_sides.txt` |
| PR side kept | Patch-id of `cc204c6f..4f210018` equals patch-id of `87e9d03a..cf4120f4`, audit excluded: `ed69f100` | `receipts/01_topology.txt` |
| Dev side kept | Patch-id of `cc204c6f..87e9d03a` equals patch-id of `4f210018..cf4120f4`, audit excluded: `a5e12980` | `receipts/03_both_sides.txt` |
| Blob identity | The four dev-only paths equal dev's blobs. The 16 PR-only paths equal `4f210018`'s blobs | `receipts/03_both_sides.txt` |
| Merged `TESTING.md` | The #839 row (`:360`) and the #833 row (`:365`) both stand in one table, with uniform column counts around the #839 row. `:490` "eighteen ordinary commands", `:495` `obj_bootsa` and `:505` "other eight legs" are kept. Dev's hunks touch none of those lines | `receipts/10_residual_checks.txt` |

The merge commit took dev's audit verbatim (blob `9fdb8bf4`), so `--check` is rc 1 at `19f4c0b4`, and `cf4120f4` repairs that. This is the expected order and only the head matters to the gate, so it is not a finding.

### Check 2: audit and data file are what the generator produces. HOLDS

`--write` writes the audit page only. `scripts/docs_inventory.json` is a hand-kept input, so for that file the claim is "unchanged and used". Its blob `242c0553` and generator blob `fe9cbbc5` are the same at `cc204c6f`, `4f210018`, `87e9d03a`, `19f4c0b4` and `cf4120f4`.

All of the following are in `receipts/04_regen_proof.txt` unless noted:

- `--check` rc 0 in the review clone, in a fresh no-submodule clone, and on a no-Git archive (`receipts/14_final_probes.txt`).
- `--write` at the head leaves zero worktree delta. Audit sha256 `1d66bb1c...f3f99f` and data sha256 `6b53c9b3...84aaca` equal the head blobs byte for byte.
- Replay: `--write` run from `19f4c0b4` reproduces the head's audit byte for byte and changes no other path.
- `--selftest` rc 0, 50 controls.
- The gate can fail. A one-digit total edit, one added line in `TESTING.md`, and restoring the merge's stale audit are each rc 1. Restoring gives rc 0.
- Hand arithmetic agrees: current +153 = `CHANGELOG.md` +24 and milan_dp README +129. Stale +5 = `BAREMETAL_FIRMWARE.md` +3 and `TESTING.md` +2. Total 92,211 + 158 = 92,369.

### Check 3: one merge base, no other file changed. HOLDS

- `git merge-base --all cf4120f4 87e9d03a` gives only `87e9d03a`. The live dev tip was `87e9d03a` and the live PR head `cf4120f4` at my last read (`receipts/14_final_probes.txt`).
- `4f210018..cf4120f4` changes six files: the audit, `TESTING.md`, and four dev-only paths. `19f4c0b4..cf4120f4` changes the audit only, 13 lines each way.
- The file set of `87e9d03a..cf4120f4` equals that of `cc204c6f..4f210018`. No mode changed. The six gitlinks are identical at `4f210018`, `87e9d03a` and `cf4120f4`.
- Both commits are one line with no trailers. Added lines in `scripts` and `tb` carry no lane label, review round, reviewer ID or comment ID, and the regenerated audit lines carry none. There is no comment-rule RESIDUE (`receipts/10_residual_checks.txt`).

## 3. Does the delta change what the unchanged code depends on?

No. `hdl`, `sw`, `syn`, `third_party`, `tests`, `.github`, the submodule pins, the PR's milan_dp, render and capture harnesses, `docs/reference`, `docs/integration` and `CHANGELOG.md` have no change in `4f210018..cf4120f4` (`receipts/14_final_probes.txt`).

The dev side changes `scripts/owned_process.py`, `scripts/process_test_support.py`, `scripts/test_suite_cancellation.py` and one timeout in `tb/verilator/gptp_shadow/test_mutant_lifecycle.py`. The PR's `bootsa_mutants.py`, `gen_boot_fw.py` and `test_sim_pool.py` import none of them. The dev-side scripts name no PR-edited path except a comment pointing at the `TESTING.md` cleanup table, which the PR does not edit.

## 4. Gates run at this head

25 gates in one parallel pass, per-gate logs in `receipts/gates/`, summary in `receipts/05_gates_summary.txt`.

| Group | Result |
|---|---|
| 20 gates: docs_check, feature_status, doc_style, solution_docs, submodule_docs, gptp_docs `--with-submodule`, inventory `--check` and `--selftest`, baremetal_only `--check` and `--selftest`, test_evidence, fail_fast, hygiene, py_idiom, sh_idiom, todo_ownership, archive, naming, `test_mutant_lifecycle.py`, `test_suite_cancellation.py` | rc 0 |
| em_dash `--base` and `--selftest`, toc `--verify-anchors` and `--check` | rc 2 on the first pass, not a verdict: the pinned renderer was absent. Rerun with the hash-pinned renderer in a disposable environment: all rc 0, plus toc `--selftest` rc 0. Em dash: 0 findings over 179 added lines, 339 of 339 arms. Anchors: 582 links. TOC selftest: 1501 of 1501 (`receipts/09_gates_md_summary.txt`) |
| `tb/verilator/milan_dp/test_sim_pool.py` | **rc 1, 16 PASS and 1 FAIL.** See S1 |

## 5. Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### S1 - SUGGESTION - Tests, Docs - `tb/verilator/milan_dp/test_sim_pool.py:76`, `:874` - the runner's Makefile-inventory arm is red, on dev as well as here, and the exact defect has no Issue

**Authority and evidence.**
- AGENTS.md section 6 `Tests`: existing regressions remain green. `tb/verilator/milan_dp/README.md:59` documents the command, and its prose says the runner tests check the Makefile inventory.
- At this head `arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs` fails: 48 runner words against 42 expected. `LEGACY_LEGS` lacks `obj_sidmove` and `obj_sidmove8`, which the Makefile runs (`receipts/06_sim_pool_review_clone.log`, `receipts/06_sim_pool_triage.txt`).
- Origin, by execution with initialised submodules (`receipts/07_sim_pool_origin.txt`): green 17/17 at `18444ac64e^`, red at `18444ac64e`, red at `cc204c6f`, `87e9d03a`, `4f210018` and `cf4120f4`. That dev commit added the legs without touching the test, and it is an ancestor of the PR's first head.
- The PR's own row is correct. With the two legs removed the lists match in banners and order, and `obj_bootsa` is last and identical (`receipts/08_pr_row_check.txt`). Planting only the two missing rows in a disposable copy gives 17 PASS and 0 FAIL, so they are the sole cause (`receipts/14_final_probes.txt`).
- The arm's docstring says "the recipe's fifteen legs" (`:874`). The recipe has 18 and the table 16. It was already wrong at `cc204c6f`, where the recipe had 17.
- Related stale prose in `tb/verilator/milan_dp/README.md`: `:4` "fifteen elaborations", `:15` "The eleven ordinary simulations" and `:461` "retains its fifteen legs". Each is present at the base as well (`:459` there). `TESTING.md:490` and the runner give eighteen ordinary legs.

**Impact.** The only check that compares the runner's inventory with the Makefile stops at the first difference, so it gives no green proof that `obj_bootsa` is registered. A later inventory drift is hidden behind the existing red. Product behaviour is unaffected: `obj_bootsa` does run, as the dry run shows.

**Why SUGGESTION and not MINOR.** This is a judgement, so the basis is stated for anyone who wishes to overrule it:
- The cause is a dev commit unrelated to #839, and neither this PR nor this delta changes it.
- No #839 acceptance item covers it. Item 4 covers parent gates, and open #720 records that no gate runs this file.
- AGENTS.md section 4 says newly discovered work becomes another Issue and is not silently folded in.
- The assignment holds unchanged code at its prior lens verdict unless the delta changes what it depends on, and it does not.

The argument the other way is real and is not dismissed. AGENTS.md section 7 says a finding moved to another Issue is not resolved, and this PR did edit this table while leaving it red. I read that rule as covering defects of the change under review, not defects it inherited. If the reviewers or the maintainer read it more widely, S1 becomes MINOR under `Tests`, and this round's `Tests` lens and verdict must then be revisited.

**Tracking gap.** #720 covers the class: no gate runs the file, a prior drift of this same arm, and an acceptance item that a planted inventory break fails in CI. It does not name `obj_sidmove`. The specific gap appears only in the author's published handoffs, headed "not filed", and no public issue search for `obj_sidmove` returns anything. None of the eight earlier review reports recorded it.

**Required outcome (optional for this PR).** Add the two rows to `LEGACY_LEGS` in Makefile order, after `obj_tspec8` and before `obj_dynmap`. Correct or drop the docstring's count. Correct the README counts: `:15` and `:461` to eighteen, and `:4` to the count of elaborations `make -n` shows, which I did not establish. Land this under #720 or a new Issue, or here if the maintainer prefers.

**Verification.** `python3 tb/verilator/milan_dp/test_sim_pool.py` with initialised submodules gives 17 PASS and 0 FAIL. Removing one Makefile leg then turns the arm red.

## 6. Prior public findings at this head

| Finding | State at `cf4120f4` |
|---|---|
| R773-1 F1 = R774-1 F1 (MINOR, Tests): no test of the MAAP, AAF and CRF hold | Resolved in round 2. Resolving files unchanged since, blob-identical to `4f210018` |
| R773-1 F2 (MINOR, Docs, Tests): README credited an unchecked stamp property | Resolved in round 2. Unchanged |
| R774-2 F1 = R773-2 RES-1 (MINOR, Docs): README "grades every frame" list | Resolved in round 3. Unchanged |
| R773-1 S1, S2, R774-1 S1, RES-1, R1, R2 | Taken or applied in round 2. Unchanged |
| R773-2 S1, S2, R774-2 S4 | Taken in round 3. Unchanged |
| R773-2 S3 = R774-2 S3 (`gen_boot_fw.py:112` spacing) | Retained, optional. File unchanged |
| R773-2 S4 (PM2 equivalent mutant) | Informational. No `hdl` delta |
| R774-2 S1, S2 (check names, exported offsets) | Retained, optional. Files unchanged |
| R773-3 S1-S3, R774-3 S1, S2, S4 (README wording and placement) | Retained, optional. README unchanged |
| R774-3 S3 (EtherType check has no planted control) | Retained, optional. `bootsa_mutants.py` unchanged |
| R773-4 S1 = R774-4 S2 (D0-062 cites line 2291) | Retained, optional, dev-side data. The cited text is at `BAREMETAL_FIRMWARE.md:2294` and the audit row at `:492`. Blob of the data file unchanged |
| R774-4 S1 (no-Git walk counts ignored cache directories) | Retained, optional, dev side. Generator unchanged. A clean archive passes `--check` |

## 7. Lens results

```text
[R773] PASS Conformance - issue #839 acceptance 1-4; git diff 87e9d03a..cf4120f4 patch-id ed69f100 - PR net patch identical to the round 4 head outside the audit; no protocol, wire or register-map byte changed
[R773] PASS RTL - git diff 4f210018 cf4120f4 -- hdl sw syn third_party and the six gitlinks - both empty or identical, so nothing in RTL scope moved from the head R773-4 covered
[R773] PASS Robustness - scripts/docs_inventory.py in review clone, no-submodule clone and no-Git archive; three fault controls; test_suite_cancellation.py and test_mutant_lifecycle.py rc 0 - generator stable across tree shapes, gate fails when planted, dev-side cleanup works on the merged tree
[R773] PASS Tests - receipts/gates, gates_md, 04_regen_proof.txt, 07_sim_pool_origin.txt - 25 gates plus toc selftest run; every planted inventory control fired; the one red test is inherited and traced to its cause (S1, SUGGESTION)
[R773] PASS Docs - docs/DOCUMENTATION_AUDIT.md, docs/testing/TESTING.md:360,:490-505, scripts/docs_inventory.json - audit byte-identical to the generator, counts checked by hand, both sides' TESTING text intact; S1's stale counts predate the PR
```

## 8. Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #839 acceptance; PR net patch-id `ed69f100` at both heads; dev patch-id `a5e12980`; merge replay | R773-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |
| RTL | CLEAN | Empty `4f210018..cf4120f4` diff over `hdl`, `sw`, `syn`, `third_party`; identical gitlinks. RTL depth rests on R773-4 at `4f210018`, an ancestor nothing in this scope has touched since | R773-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |
| Robustness | CLEAN | Generator across three tree shapes; fault controls; cancellation and lifecycle tests on the merged tree | R773-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |
| Tests | CLEAN (S1 SUGGESTION, inherited red test; see the judgement in section 5) | `receipts/gates`, `receipts/gates_md`, regeneration proof, sim-pool origin and sole-cause probes | R773-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |
| Docs | CLEAN (S1 SUGGESTION; prior SUGGESTIONs optional) | `docs/DOCUMENTATION_AUDIT.md`, `scripts/docs_inventory.json`, `docs/testing/TESTING.md`, em-dash, TOC, anchor and docs gates | R773-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |

## 9. Real limits

- **No execution of the `bootsa` leg or its mutants this round.** Their inputs are byte-identical to `4f210018`, so the round 4 results (67/0, 13/13) carry by input identity, not by a rerun at this head. No full parent, processor, gPTP, Yosys or builder bank was run, and no manager source bank exists at this head.
- **Evidence packet.** Commit `b06fad40` carries no git signature (GitHub reports `unsigned`), and `MANIFEST.json` is an unsigned hash list, so I could not verify a signature. What I did verify: the manifest covers all 2099 published files in the tree, with only `MANIFEST.json` itself unlisted, and a seeded sample of 24 files plus 3 named files match their published hashes, 0 mismatches. 322 entries are path-redacted, so their originals cannot be compared. The packet describes round 4; there is no author packet for `cf4120f4`, and its two commits are manager commits.
- **`test_sim_pool_backpressure.py`.** It printed no summary line within my 200 s bound, so I draw no result from it. That fits #720 defect 2 but I did not establish the cause. `LEGACY_LEGS` is imported by it, and it is unchanged by the delta.
- **Superseded receipts.** `receipts/06_sim_pool_H.log`, `_P.log` and `_D.log` come from no-submodule clones, where `make -n` stops at rc 2. They do not show the S1 failure's cause. `receipts/07_sim_pool_origin.txt` is the valid origin evidence. The four rc 2 entries in `receipts/05_gates_summary.txt` are superseded by `receipts/09_gates_md_summary.txt`.
- **Hosted state.** Snapshot at 2026-11-06T11:43:48Z, while still running: 8 success (`Prepare pinned Yosys`, `verilator-lint`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, `changes`, `elaborate-gates-4`, `bdd-conformance`), 5 in progress, 37 queued, 1 skipped (`Physical gPTP`, nightly and manual, so no hardware proof). Merge state BLOCKED. I claim no hosted acceptance.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## 10. Pending manager duties

- Decide S1's placement: record the `obj_sidmove` gap on #720 or a new Issue, since it is currently unfiled. Tell the other reviewer and the maintainer about the classification judgement in section 5.
- Own hosted and local-replica acceptance at the exact head, once the queued contexts finish.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR. Recheck that live dev is still `87e9d03a`; any movement means a new merge and a new regeneration.
- Carry the retained optional SUGGESTIONs in section 6 to the author or the #797 lanes.
- Maintainer authorization is still required for the merge.

R773-5 FINISHED
