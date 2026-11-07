[R785] POSITIVE - exact head 43410ce1ec16e08fff22c35115d1fea9a6ed78de

Round R785-3, internal independent review of PR #847 (issue #845), tree `f1cb37b9893f744fef22b3190ee05b3a6aeccb64`. This is a delta review against `853ca25ae00fe26b09e019fbfe70893666617fc1`, the head R785-2 and R786-2 reviewed. The delta is a manager sync and nothing else: `f7e94a07` merges #849's head `697e17a4`, which carries #842's head, and `43410ce1` regenerates the documentation audit. As briefed, #842 and #849 are not re-reviewed here.

## Verdict

POSITIVE. All five lenses are clean at this head, and no BLOCKER, MAJOR or MINOR is open. One new RESIDUE (PR body wording) is recorded. The RESIDUE and SUGGESTION items from earlier rounds are carried unchanged. The act at this head has not run yet. It is listed below as open and is not a finding.

## The four focus checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Both `CHANGELOG.md` conflicts keep both entries whole, with #847's first, and the contents list matches the sections | Holds | `changelog_check.txt`. Every section on the #847 side (`853ca25a`) and on the #849 side (`697e17a4`) is in the head byte for byte. There is no extra section. `Unreleased - processor pin 92100657` comes directly before `Unreleased - station MAC from reset`. The contents list has 44 entries for 44 sections, in the same order, and every anchor matches its heading's slug. Every contents line from either side is in the head verbatim. Reconstructing the merge with `git merge-file` gives exactly two conflict regions, the contents list and the entry body. The head is that result with the markers removed and both sides kept. |
| 2 | `docs/DOCUMENTATION_AUDIT.md` is exactly what `docs_inventory.py --write` produces at this head | Holds | `docs_inventory_check_head.txt`: `--check` rc 0, "547 lines ... is fresh". `docs_inventory_write_scratch.txt`: `--write` in a disposable clone at `43410ce1` gives rc 0, an empty `git status` and a byte-identical page. `43410ce1` changes one row, the `INTEGRATION_GUIDE.md` authorities cell, which gains "Milan v1.2". The cause is that `f7e94a07` took #849's audit, which predates #847's `INTEGRATION_GUIDE.md` edit, and the regeneration restores that input. |
| 3 | `git diff 853ca25a..43410ce1` is empty outside the paths #849 and #842 changed | Holds | `delta_paths.txt` and `side849_paths.txt`: 56 paths each, and `comm -23` is empty. The merge base of the two sides is `87e9d03a`, the PR's source base. `path_blob_check.txt`: 53 of the 56 head blobs, modes included, are identical to `697e17a4`. The other three are `CHANGELOG.md`, the audit and `tb/verilator/milan_dp/README.md`. The `protocol-processor` (`92100657`), `gptp-processor` and `external` gitlinks are unchanged. |
| 4 | The merge altered no file #847 changed except `CHANGELOG.md` and the audit | **Literally false, but the content is correct**: see R785-3-R1 | Three of #847's 19 paths are in the delta. The third is `tb/verilator/milan_dp/README.md`. Both branches changed it, and Git merged it without a conflict: three-way `git merge-file` over `87e9d03a`, `853ca25a` and `697e17a4` exits 0 and equals the head blob (`reproduce_run.txt`, `README_CLEAN_3WAY_EQUAL`). The merge adds #842's `obj_bootsa` table row, contents line and section, and #847's own lines in that file are unchanged. No processor pin, RTL of #847, gate record or area figure moved. |

## Gates run at this head

I re-ran every gate the manager listed in this clone, at `43410ce1`.

| Gate | rc | Receipt |
|---|---|---|
| `docs_inventory.py --check` | 0 | `docs_inventory_check_head.txt` |
| `docs_check.py` | 0 (0 findings, 214 md files, scrub self-test 23/23) | `gate_docs_check.txt` |
| `check_doc_style.py` | 0 | `gate_check_doc_style.txt` |
| `gen_toc.py --check` | 0 (152 pages) | `gate_gen_toc_check.txt`. It ran with the pinned renderer from `tools/markdown/requirements.txt`, installed with `--require-hashes` into a disposable venv under `scratch/` |
| `git diff --check 853ca25a 43410ce1` | 0 | `gate_git_diff_check.txt` |
| `ci_differential.py --check` | 0 (224 fixtures, 185 census shapes) | `gate_ci_differential_check.txt` |

`reproduce.sh <clone> <outdir>` re-runs focus checks 1 to 4 and the inventory check (`reproduce_run.txt`, rc 0).

## Prior findings at this head

| Finding | State | Evidence |
|---|---|---|
| R785-1 F1 to F4, R786-1 F1 to F4 (MAJOR, MINOR) | Still resolved | Resolved at `853ca25a` by R785-2 and R786-2. The delta touches none of the artifacts they depend on: `AREA_BUDGET.md`, `SUBMODULES.md`, `INTEGRATION_GUIDE.md`, `pp_shadow/sim_main.cpp`, the baseline JSON, the gitlink and #847's CHANGELOG section are all byte-identical. |
| R785-2-R1 / R786-2-R1, RESIDUE, `docs/reference/SUBMODULES.md:615` | Carried, unfixed | The line still reads "Against that record, ...". Exact fix as published: "Against the thirteenth record, `check` exits 0 on every endpoint." |
| R786-2-R2, RESIDUE, CHANGELOG ExtraPostPlacementOpt line | Carried, unfixed | It is now `CHANGELOG.md:90`, because the merged contents line pushed it down by one. Exact fix as published: "- On ExtraPostPlacementOpt the route grows 503 LUTs and 478 FFs." |
| R785-2-R2 / R786-2-R3, RESIDUE, PR body Round 2 table, F1 row | Carried, unfixed | The row still runs "The gate ran in its own form Answered in [...". Exact fix as published. |
| R785-2-R3, RESIDUE, PR body Known limitations, `inputs_sha256` | Carried, unfixed | It still says "the fix belongs in a new Issue". Exact fix: "the fix is tracked by #850". |
| R786-R1, RESIDUE, "Recipe" wording | Carried | Sent to #495 by the round 3 ruling. |
| R785-1 S1 / R786-S2, R785-1 S2, R786-S1, R785-2-S1, R786-2-S1, R786-2-S2 | Retained as SUGGESTION | Unchanged. The `milan_dp/README.md` dated row (R785-1 S2) has moved to line 1644 because #842's content was merged in, and it still ends at 421. |

## Findings

No BLOCKER, MAJOR or MINOR.

### R785-3-R1 RESIDUE - lenses Docs

**Artifact:** PR #847 body, the contents entry for "Sync on #849" ("no change to this PR's own files"), and the bullets of that section.

**Authority and evidence:** the merge changed three of this PR's own files. Two of them, `CHANGELOG.md` and the audit, are named in the section. The third is not: `tb/verilator/milan_dp/README.md`, which this PR changed at `853ca25a` and which #842 also changed. Git merged it without a conflict, and the result equals the three-way merge (`reproduce_run.txt`). So "no change to this PR's own files" is true of this PR's content but not of its files, and the section omits the one file that merged cleanly.

**Why RESIDUE, not MINOR:** this is wording only. The merged README is correct, #847's lines in it are unchanged, and no figure, test, gate or generated artifact depends on the sentence.

**Impact:** a cold reader checking the sync against `git diff 853ca25a..43410ce1` finds a file of this PR's in the delta that the text does not mention.

**Exact fix:** change the contents hook to "The manager's merge of #849's head; this PR's own content is unchanged." Add this bullet after the `f7e94a07` bullet: "`tb/verilator/milan_dp/README.md`, which #842 also changed, merged without conflict: #842's `obj_bootsa` row, contents line and section join this PR's lines unchanged."

**Verification:** read the PR body. `git diff --name-only 853ca25a 43410ce1` intersected with `git diff --name-only 87e9d03a 853ca25a` gives exactly the three files the section names.

No new SUGGESTION.

## Lens results at this head

[R785] PASS Conformance - issue #845 acceptance and rulings as banked at 853ca25a; `changelog_check.txt`; `path_blob_check.txt`; gitlink protocol-processor 9210065779b0 at 853ca25a and 43410ce1 - no acceptance-bearing artifact of #847 moved: pin, decision text, area pages and #847's CHANGELOG entry are byte-identical. The merged-in content is the #849 and #842 sides' content byte for byte. The PR body's sync claims hold except the wording in R785-3-R1.

[R785] PASS RTL - `path_blob_check.txt` (`hdl/milan/milan_datapath.sv` EQ849); `git ls-tree` gitlinks at both heads - #847's RTL scope (the processor pin) is unchanged. The only RTL file in the delta, `milan_datapath.sv`, is byte-identical to #842's head as carried by `697e17a4`, and its review belongs to that lane. The merge resolved no RTL conflict, so it introduced no RTL of its own.

[R785] PASS Robustness - `delta_paths.txt` against `side849_paths.txt` (empty `comm -23`); README three-way equality - the merge has no stray path, no hand-edited hunk outside the two declared conflicts, and both conflict resolutions keep both sides whole. The prior link-change, pre-settle and gate-tamper verdicts stand, because nothing they depend on changed.

[R785] PASS Tests - `path_blob_check.txt`; `gate_ci_differential_check.txt` - no test file of #847 (`pp_shadow/sim_main.cpp`, `milan_dp/unb_mutants.py`) moved. The test files in the delta are #842's and #849's, identical to `697e17a4`. `ci_differential.py --check` rc 0 at this head. The prior pp_shadow and gate self-test receipts remain valid at this head, because their inputs are unchanged.

[R785] PASS Docs - `CHANGELOG.md` (`changelog_check.txt`); `docs/DOCUMENTATION_AUDIT.md` (`docs_inventory_write_scratch.txt`, byte-identical regeneration); `tb/verilator/milan_dp/README.md` (clean three-way merge); `gate_docs_check.txt`, `gate_check_doc_style.txt`, `gate_gen_toc_check.txt`, `gate_git_diff_check.txt` all rc 0; PR body Sync section - the contents lists match their sections and the audit is fresh. Comment rule: the manager-authored delta (the two conflict resolutions and the regeneration) adds no source comment, so no new instance is possible. R785-3-R1 and the carried RESIDUE items do not leave the lens unclean.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #845 acceptance and rulings as banked by R785-2; PR body Sync section; `changelog_check.txt`; `path_blob_check.txt`; gitlinks | R785-3 | `43410ce1ec16e08fff22c35115d1fea9a6ed78de` |
| RTL | CLEAN | gitlinks at `853ca25a` and `43410ce1`; `hdl/milan/milan_datapath.sv` blob equal to `697e17a4`; no RTL conflict in `f7e94a07` | R785-3 | `43410ce1ec16e08fff22c35115d1fea9a6ed78de` |
| Robustness | CLEAN | delta path sets; per-path blob and mode check; README three-way merge equality; CHANGELOG conflict reconstruction | R785-3 | `43410ce1ec16e08fff22c35115d1fea9a6ed78de` |
| Tests | CLEAN | #847's test files unchanged; delta test files equal to `697e17a4`; `ci_differential.py --check` | R785-3 | `43410ce1ec16e08fff22c35115d1fea9a6ed78de` |
| Docs | CLEAN | `CHANGELOG.md`, `docs/DOCUMENTATION_AUDIT.md`, `tb/verilator/milan_dp/README.md`, PR body; five documentation gates rc 0 | R785-3 | `43410ce1ec16e08fff22c35115d1fea9a6ed78de` |

## Real limits

- #842's and #849's own content, including the `milan_datapath.sv` station-MAC hold and the `obj_bootsa` leg, was checked only for byte identity with `697e17a4`. Its correctness is those lanes' review.
- I ran no simulation, synthesis or route at this head. Since the delta changes no #847 input, the prior measurement and suite receipts were carried by input identity, not re-executed.
- The published evidence tree `a3149b01/review-evidence/845-r1` predates this head. Its MANIFEST names neither `853ca25a` nor `43410ce1`, and this round relies on it only for the unchanged #847 artifacts. The new checks in this round are my own receipts.
- `gen_toc.py --check` needed the pinned renderer. I installed it from the repository's hash-pinned requirements into a disposable venv, not from a shared install.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- The act at `43410ce1` has not run: it is open, not a finding.
- Hosted contexts at this exact head were still in flight when I checked: the Verilator shards, `yosys-elaboration`, the firmware and docs gate jobs were queued or in progress. `Physical gPTP (nightly and manual)` was skipped by schedule. `full-ci-gate`, `wire-accountability`, `firmware-aecp-mutants` and `elaborate-gates-0/3/4` had completed with success. Hosted and act acceptance belong to the manager.
- The current-dev candidate merge validation (source base `87e9d03a`, live dev `35448611`), with its builder and native banks, is due at the merge turn.
- The second independent positive at this head (the external review) is needed.
- Carry R785-3-R1 and the carried RESIDUE items to the residue checklist.

R785-3 FINISHED
