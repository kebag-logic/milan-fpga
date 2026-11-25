[R913] POSITIVE - exact head 2b98e219a5e2b0681f76be90083fc05e47a8f6c0

# R913-6: internal sync re-review of kebag-logic/milan-fpga PR #992 (issue #991)

Head `2b98e219a5e2b0681f76be90083fc05e47a8f6c0`, tree `4ccdecfab334bbef8e5686bedf87f0e4290a816b`. The remote head reports the same tree.
The delta is one merge commit. It merges `dev-soft-core` `e608f8d8` (PRs #1001 and #995, FPGA-gPTP `1213ac5b`) into `67838b37`, the head round R913-5 reviewed POSITIVE.
This is a narrow round. It checks only the sync merge. Code the merge does not touch keeps its R913-5 verdict, because nothing it depends on changed (see RTL and Tests below).

## Verdict summary

- **POSITIVE.** No BLOCKER, MAJOR, MINOR or new RESIDUE at this head. All five lenses are covered clean at `2b98e219`, within the narrow scope below.
- **The conflict resolution is the repository generator's own output.** Re-running `docs/diagrams/submodule_boundaries.gen.py` at the head rewrites the drawio, SVG, PNG and `PNG_MANIFEST.json` byte for byte (`receipts/sb_before.sha256` = `receipts/sb_after.sha256`). Its `--check` and `--selftest` pass.
- **The diagram shows both pins:** gptp-processor `1213ac5b9e09` and lwSRP `d1bb4f4e5954`. I checked the drawio text and looked at the decoded PNG.
- **The merge is pure upstream outside the five paths both sides changed.** `git diff 67838b37 2b98e219` and `git diff 2509db68 e608f8d8` list the same 37 paths. Outside the both-sides set, every path in the tree has `e608f8d8`'s blob where upstream changed it, and `67838b37`'s blob otherwise (0 violations, `receipts/tree_partition.txt`).
- **None of this PR's own changes is altered.** All 21 of its paths (`2509db68..67838b37`) keep `67838b37`'s blob, except the five both-sides paths. Every PR-owned line in `SUBMODULES.md` is present at the head (`receipts/submodules_pr_lines_present.txt`).
- **Hosted CI at the head had not finished at review time.** At 02:30:57Z, 17 check runs were queued or in progress and none had completed. The `docs`, `elaborate`, `rtl-full` and `rtl-fast` workflow runs were all queued. I claim no hosted result (see limits).

## How the task was reconstructed (public state only)

- **Contracts:** AGENTS.md, CONTRIBUTING.md, `docs/README.md`. Issue #991 title: "Pin lwSRP d1bb4f4e: send a withdrawal after the own LeaveAll as Lv". The issue is OPEN and has 0 comments.
- **PR #992 state:** open, not draft, base `dev-soft-core`, head `2b98e219`, mergeable. The live PR body has a sync section naming `2b98e219`, `e608f8d8`, PRs #1001 and #995, and both pins. It also says the routed 8x8/1if figures are `507bce7f`'s and exclude #995's fabric change.
- **Author packet:** `review-evidence/lwsrppin-r1/author-r6` at `53458a05`. I read `REVIEW-READY.md` and `receipts/INDEX.md`, and fetched four receipts to check them.
- **Generator authority:** `docs/diagrams/README.md:41` and `docs/DOC_GENERATION.md:169-171` name `docs/diagrams/submodule_boundaries.gen.py`. There is no `scripts/generate_diagrams.py` in the tree, so I re-ran the documented generator (note N1).

## Evidence produced by this round

| Check | Result | Receipt |
|---|---|---|
| Delta path set compared with upstream's own delta | Same 37 paths with the same status | `receipts/delta_names.txt`, `receipts/upstream_names.txt` |
| Per-path patch-id | Equal for all paths except `PNG_MANIFEST.json`, `submodule_boundaries.drawio`, `submodule_boundaries.png` and `SUBMODULES.md` | `receipts/pathwise_patchid.txt` |
| Per-path blob table (stronger than patch-id) | The five both-sides paths (adding `.svg`) differ from both parents. Every other path is pure upstream | `receipts/blob_table.txt`, `receipts/tree_partition.txt` |
| Whole-tree partition | 0 PR-owned paths altered, 0 upstream changes left out, 0 other changes | `receipts/tree_partition.txt` |
| `SUBMODULES.md` | `git merge-file` of (67838b37, 2509db68, e608f8d8): 0 conflicts, output identical to the head blob. Compared with `e608f8d8`, only the lwSRP pin row differs (`08ee86e8` → `d1bb4f4e`) | `receipts/submodules_mergefile.txt`, `receipts/submodules_vs_upstream.diff` |
| Generator re-run (write mode) | rc 0. drawio, SVG, PNG and manifest byte-identical. Porcelain 0 | `receipts/sb_gen_write.txt`, `receipts/sb_before.sha256`, `receipts/sb_after.sha256`, `receipts/status_after_gen.txt` |
| Pins in the diagram | `67838b37`: 1616fc8f + d1bb4f4e. `e608f8d8`: 1213ac5b + 08ee86e8. Head: 1213ac5b + d1bb4f4e. The decoded PNG shows the same pins | drawio text at the three commits. PNG inspected visually |
| Manifest binding | `source_sha256` of both changed entries equals the sha256 of its drawio. `check_diagram_pngs.py` passes: 6 decoded, source-bound rasters | `receipts/gates/check_diagram_pngs.log` |
| Docs gates at head (15, run concurrently) | 15 of 15 rc 0. Porcelain 0 before and after. `docs_check`: 0 findings across 223 md files and 1942 text files. `docs_inventory --check`: fresh. `check_doc_paths`: 1764 paths resolve. `check_submodule_docs`: 6 exact gitlinks. `check_gptp_docs`: 8 pages. DOC_MAP, submodule_boundaries and timesync_chain pass both `--check` and `--selftest`. `check_diagram_pngs --selftest`: 28 mutation controls | `receipts/gates/SUMMARY.txt`, `receipts/gates/*.log`, `*.rc` |
| `egress_ledger.py --selftest` at head | rc 0. 72 PASS controls, `RESULT: PASS: 18 mutants, 0 failure(s)`. Output identical to the author's head receipt after removing temporary paths (0 diff lines). The script imports only the standard library, and its directory's only delta path is `build.py` (a host compile flag) | `receipts/gates/egress_selftest.log`, `receipts/egress_selftest_vs_author.diff` |
| Author receipt integrity (spot-check) | 4 of 4 fetched receipts match the 16-hex sha256 prefixes in `INDEX.md` | `receipts/author_receipt_spotcheck.txt` |
| Comment-rule scan of the delta's added lines | No new instance written by the merge. The hits are upstream content, byte-equal to `e608f8d8`, where "lane" means the transmit data lane (note N4) | `receipts/comment_rule_scan.txt` |
| Merge commit form | One line with no trailers | `git log -1 --format=%B 2b98e219` |
| Hosted CI at head | 17 check runs: 3 in progress, 14 queued, 0 completed. 4 workflow runs queued | `receipts/hosted_check_runs.tsv`, `receipts/hosted_check_runs_2.tsv`, `receipts/hosted_workflow_runs.tsv` |
| Restore | HEAD, tree, index tree and worktree equal the exact head. 0 porcelain lines, untracked files included. All six gitlinks match the tree | `receipts/restore_check.txt` |
| Reproduction script | `scripts/merge_checks.sh` re-runs the path, blob, merge-file and generator checks. rc 0, porcelain 0 afterwards | `receipts/merge_checks.log` |

## Findings

No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is raised by this delta.

### Notes (no action on the PR)

- **N1. The review brief named the wrong generator.** It named `scripts/generate_diagrams.py`, which does not exist at this head. The repository's generator for this diagram is `docs/diagrams/submodule_boundaries.gen.py` (`docs/diagrams/README.md:41`, `docs/DOC_GENERATION.md:169-171`). The author's `REVIEW-READY.md` says the same. I re-ran the documented generator.
- **N2. The author's per-path receipt cannot see binary changes.** `merge/dev-delta-per-path.txt` compares diff bodies. For the PNG, the body is only "Binary files differ", and the SVG's hunk is equal even though its blob differs from both parents. So that receipt alone cannot show the PNG and SVG blob changes. The blob table and whole-tree partition here close that gap, and the generator re-run proves those blobs are the generator's output. The PR is not affected.
- **N3. The packet's push wording is stale.** `author-r6/REVIEW-READY.md:2` and `receipts/INDEX.md:3` say "local, not pushed", but `2b98e219` is now the published PR head. This is the same publication-time staleness as R913-5 N1. The evidence commit `53458a05` is unsigned (GitHub verification `unsigned`). Its integrity rests on the sha256 index, which the spot-check matched.
- **N4. The comment-rule hits are upstream content, not new instances.** The scan hits are in `tb/verilator/gptp_shadow/{mutants.py,sim_main.cpp,README.md}`, where "lane" names the transmit data lane, a technical term. The other hits are in `docs/reference/SUBMODULES.md` prose ("lane commit `973f2f20`", an issue-comment link). All of them are byte-equal to `e608f8d8`, already on `dev-soft-core` through PR #995, and outside this PR's own changes. The comment rule covers source comments. Documentation prose and findings pages may name lanes.
- **N5. One old lwSRP pin remains, outside this delta.** `ci/image/exec-audit-receipt.json:4184` still records lwSRP `08ee86e8`. The merge does not touch that file, which records an image audit run, and it is outside this round's scope. I raise no finding.

## Prior public findings at this head

| Finding | Status at `2b98e219` | Evidence |
|---|---|---|
| R913-5 S1 (SUGGESTION, Docs; `SPLIT_CONTROL_MEMORY.md:3044`, #1005 AC3) | Open, optional | File not in the delta (`receipts/delta_names.txt`) |
| R913-5 S2 (SUGGESTION, Tests; `egress_ledger.py:453-461`) | Open, optional | File not in the delta. Self-test output unchanged (`receipts/egress_selftest_vs_author.diff`) |
| R913-5 R1 = R913-4 R1 (RESIDUE, Docs; `sw/firmware/ctrl/test/test_ctrl_firmware.py:81-82`) | RETAINED for the residue checklist. Exact fix: "... after the board's own LeaveAll is sent as Lv within 240 ms ...", re-wrapped to the entry's column | File not in the delta |
| R913-4 F1, F2 (MINOR) | Remain RESOLVED (R913-5) | Their artifacts are not in the delta. Image identity at `2b98e219` matches `67838b37` (author `identity/identity.txt`: 20 of 28 files identical, every ctrl ELF and bin among them; the 8 differing files are `gptp_ucode.hex` from #995's pin) |
| R913-4 S1, S2; R913-2-S1, R913-2-S2; R913-3 N-S1 (SUGGESTION) | Open, optional | Files not in the delta |
| R913-1-F1, R914-1-F1 (MINOR) | Remain RESOLVED (R914-2 at `ed7df79c`) | Not touched by the delta |

## Lens results

```text
[R913] PASS Conformance - git diff 67838b37 2b98e219 vs git diff 2509db68 e608f8d8 (receipts/delta_names.txt, tree_partition.txt); docs/reference/SUBMODULES.md pin table; gitlinks at 2b98e219 (gptp-processor 1213ac5b, third_party/lwSRP d1bb4f4e) - the merge carries #995's and #1001's changes unaltered and keeps every one of this PR's own paths. The pin table matches the gitlinks (check_submodule_docs: 6 exact). Issue #991's lwSRP pin and its documented behaviour stand as R913-5 covered them
[R913] PASS RTL - receipts/tree_partition.txt (no hdl/, firmware, config or build input of this PR's altered); tb/verilator/ctrl_service_budget/build.py diff (OPT_FAST=-O3 only); ctrl_service_budget/ sources (no gptp-processor RTL or gptp_ucode compiled in); author identity/identity.txt (ctrl images identical, only gptp_ucode.hex differs from #995) - the gPTP RTL change is #995's, reviewed on its own PR. The delta changes no input this PR's RTL or image verdicts depend on
[R913] PASS Robustness - receipts/sb_gen_write.txt, merge_checks.log, restore_check.txt - the conflict resolution is reproducible by the generator alone (byte-identical, porcelain 0), the three-way merge of SUBMODULES.md is conflict-free, and the gitlinks are coherent with the docs and the diagram. The fail-closed parser behaviour of egress_ledger.py (R913-5) is unchanged and its self-test passes at the head
[R913] PASS Tests - receipts/gates/egress_selftest.log (72 controls, 18/18 mutants, identical to the author's head receipt); receipts/gates/sb_selftest.log, check_diagram_pngs_selftest.log (28 mutation controls), docmap/ts selftests - the selftests guarding the merged artifacts pass at the head. The gptp_shadow suite changes are #995's and out of scope. The author's ctrl_service_budget self-test at the head (295/295 mutants) is author evidence and was not re-run here
[R913] PASS Docs - docs/diagrams/submodule_boundaries.{drawio,svg,png}, docs/diagrams/PNG_MANIFEST.json, docs/reference/SUBMODULES.md at 2b98e219; receipts/gates/SUMMARY.txt (15/15 rc 0); live PR body sync section - the generated artifacts are the generator's output and show both pins. The manifest binds source and raster. The docs gates are clean. The PR body describes this head. No new comment-rule residue
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merge path and blob partition; `SUBMODULES.md` pin table; gitlinks; `check_submodule_docs` | R913-6 | `2b98e219a5e2b0681f76be90083fc05e47a8f6c0` |
| RTL | CLEAN | delta path list (no RTL, firmware or build input of this PR's); `ctrl_service_budget/build.py` diff; harness sources; author image identity | R913-6 | `2b98e219a5e2b0681f76be90083fc05e47a8f6c0` |
| Robustness | CLEAN | generator write-mode reproduction; `git merge-file` reproduction; restore and gitlink check | R913-6 | `2b98e219a5e2b0681f76be90083fc05e47a8f6c0` |
| Tests | CLEAN | `egress_ledger.py --selftest`; generator and PNG selftests; author receipt spot-check | R913-6 | `2b98e219a5e2b0681f76be90083fc05e47a8f6c0` |
| Docs | CLEAN | diagram drawio/SVG/PNG and manifest; `SUBMODULES.md`; 15 docs gates; live PR body; comment-rule scan | R913-6 | `2b98e219a5e2b0681f76be90083fc05e47a8f6c0` |

Code outside the delta keeps its R913-5 lens verdicts. Those were at `67838b37`, an ancestor of this head, and the merge changes nothing in their scope (`receipts/tree_partition.txt`).

## Real limits

- **Hosted CI:** at review time (02:30:57Z) no hosted check run at the head had completed. I make no hosted claim.
- **Not re-run here:** the ctrl_service_budget suite (`run.py --self-test`) and `plat_ledger.py --build-dir`. The image-identity and suite results at the head are the author's published receipts, which I spot-checked but did not execute.
- **Routed build:** no routed build at this head exists. The PR body's routed 8x8/1if figures are `507bce7f`'s, as the body says.
- **Scope:** #995's and #1001's own content (gptp_shadow harness, probe lists, ccache, `-O3`) was checked only for byte-equality with `e608f8d8`. It was not re-reviewed on its merits.
- **Not run:** no physical calibration, no hardware, no Docker or local CI replica, no manager source bank.

## Pending manager duties

- Hosted `rtl-fast`, `docs`, `elaborate` and `rtl-full` results at `2b98e219`, and the local CI replica for this head.
- The current-dev merge candidate against live `dev` `e275d7950ef3385753e6a15d2e191ba855b171ed`, with its builder and native banks.
- The second positive review required by CONTRIBUTING.md (the external delta review), and the #1005 AC3 ordering question (R913-5 S1).
- Carrying R1 to the residue checklist.

R913-6 FINISHED
