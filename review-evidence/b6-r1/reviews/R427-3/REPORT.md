[R427] POSITIVE - exact head df943ae83af96553362ccf58ff96089d1c31ee04

# R427-3: composition review of PR #630 (issue #629, bench lane B6), merge-train candidate

- **Head under review:** `df943ae83af96553362ccf58ff96089d1c31ee04`, tree `01d643b8bd5636b83f869004dd9482d51f4629d3`. It is a two-parent merge. The first parent is live dev `d4dd742679b902b2bc5eedf89d525066d59aafbb`, which already includes PR #628 (lane B5). The second parent is the PR #630 source head `26dfc82f80b6e69fbc6126ef7ba7fddbf1e43778`. The merge base is `ea3fb38877842f223afea97e3bd72a10500455c9`.
- **Scope:** composition acceptance only. This round did not re-review the content of `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`. That belongs to the source reviews of `26dfc82f`.
- **Reconstruction order:**
  1. AGENTS.md, and CONTRIBUTING.md sections 6 and 6.1 (the docs gates).
  2. The docs workflow `.github/workflows/docs.yml`, for the gate inventory.
  3. The #629 body and its lane comments: the assignments 5929778646, 5932539168 and 5933253532, and the executors' TAKEN and REVIEW READY heads.
  4. The candidate diff and history.
  5. The public evidence archive commits.
  6. The prior review rounds on PR #630, read only after this round's own pass.
- **Verdict:** no BLOCKER, MAJOR or MINOR finding, and one SUGGESTION. All five lenses are covered clean for the composition at this exact head.

## Contents

- [Composition facts](#composition-facts)
- [Gates run on the candidate](#gates-run-on-the-candidate)
- [Fault probes](#fault-probes)
- [Findings](#findings)
- [Prior public findings on PR #630](#prior-public-findings-on-pr-630)
- [Ledger](#ledger)
- [Limits and pending manager duties](#limits-and-pending-manager-duties)

## Composition facts

| Check | Result | Receipt |
|---|---|---|
| Paths changed by both the predecessor (B5, `ea3fb388..d4dd7426`) and this PR (`ea3fb388..26dfc82f`) | Exactly one: `docs/findings/README.md` | `receipts/compose_check.txt`, `receipts/composition_paths.txt` |
| Candidate tree vs the mechanical three-way merge of `d4dd7426` and `26dfc82f` | Identical: both are `01d643b8bd5636b83f869004dd9482d51f4629d3`. The merge commit has no hand resolution. | `receipts/compose_check.txt` |
| Candidate vs dev `d4dd7426` | `A docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `M docs/findings/README.md` (+1 row). Nothing else. | `receipts/composition_paths.txt` |
| Candidate vs source `26dfc82f` | `A docs/findings/117_AUDIO_CONTINUITY.md` and `M docs/findings/README.md` (+1 row). This is exactly B5's change. | `receipts/composition_paths.txt` |
| #629 page blob | `93f8eb68ea9bfdf2c69ff8e13091b9905a7e49d6` at both `26dfc82f` and the candidate, so it is byte-identical to the reviewed source | `receipts/blob_carryover.txt` |
| #117 B5 page blob | `9e2fae6ca7551f97bd945a907370f8ca76b7479d` at both `d4dd7426` and the candidate | `receipts/blob_carryover.txt` |
| Index rows (`docs/findings/README.md`) | 17 rows, each link target exactly once. `629_MEDIA_CLOCK_FOLLOWING_BENCH.md` is at line 15, after `617_DIN_FRAME_COHERENCE_BENCH.md`, as on the source head. `117_AUDIO_CONTINUITY.md` is at line 22, after `117_GPTP_SILICON_EVIDENCE.md`, as on dev. The row sequence is the base sequence with each head's insert at its own position. Each added row is byte-equal to the row in the head that introduced it. | `receipts/compose_check.txt` |
| Index links | All 21 relative links in the index resolve to blobs in the candidate tree | `receipts/compose_check.txt` |
| Submodule gitlinks | `external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor b2db3a97` and `third_party/verilog-axis 48ff7a7e`. They are identical at the base, both parents and the candidate. | `receipts/composition_paths.txt`, `receipts/clone_integrity.txt` |
| Semantic cross-reference | The #629 page (lines 397-399) cites lane B5, through PR #628, for "16.46 ppm of drops at the peer's output". The merged B5 page states 16.46 ppm at `docs/findings/117_AUDIO_CONTINUITY.md:302`, so the two agree. There is no other cross-page reference, and the B5 page does not cite #629. | `receipts/blob_carryover.txt` |
| Evidence pin | The #629 page pins archive `422dcf91008a09cb882dcc2b760779ce22e530cd`, twice. That commit and `c9ada338` both resolve publicly. `review-evidence/b6-r1/` lists `MANIFEST.json`, `author`, `author-r2` and `reviews`. | `receipts/blob_carryover.txt`, `receipts/archive_commits.txt` |

The composition script `compose_check.py` needs only Python 3 and git, so it runs anywhere. It works from git objects alone and asserts six things: the shared-path set, the tree identity, row uniqueness, row order, the byte provenance of each row and link resolution.

## Gates run on the candidate

Every gate ran on the candidate head. The hash-locked renderer from `tools/markdown/requirements.txt` was installed in a private environment: cmarkgfm 2025.10.22, html5lib 1.1, cffi 2.1.1, pycparser 3.0, six 1.17.0 and webencodings 0.6.1. pyyaml was added as well, because the docs workflow installs it unpinned.

| Gate (docs workflow step) | Result | Receipt |
|---|---|---|
| `scripts/docs_check.py` | 0 findings over 184 md and 955 scrubbed files; scrub self-test 23/23; routing 4/4 | `receipts/docs_check.txt` |
| `scripts/docs_check.py` on a git-stripped export | 0 findings; scrub 22/22. Inventory parity is skipped by design when git is absent. | `receipts/docs_check_nogit.txt` |
| `scripts/check_em_dash.py --base d4dd7426` | 0 findings over 687 added lines in 2 pages; arms 339/339 | `receipts/em_dash_base_d4dd.txt` |
| `scripts/check_em_dash.py --base ea3fb388` (merge base, both lanes) | 0 findings over 1240 added lines in 3 pages | `receipts/em_dash_base_mb.txt` |
| `scripts/check_em_dash.py --selftest` | PASS, 339 arms | `receipts/em_dash_selftest.txt` |
| `scripts/gen_toc.py --check` | OK: 126 pages carry contents, 17 are below the threshold | `receipts/gen_toc_check.txt` |
| `scripts/gen_toc.py --verify-anchors` | 289 cross-page fragment links reproduced | `receipts/gen_toc_anchors.txt` |
| `scripts/gen_toc.py --selftest` | PASS, 1501/1501 arms | `receipts/gen_toc_selftest.txt` |
| `scripts/check_doc_paths.py` | OK: 862 cited paths resolve | `receipts/doc_paths.txt` |
| `scripts/check_doc_style.py` and `--selftest` | OK (22 current documents); selftest OK | `receipts/doc_style.txt`, `receipts/doc_style_selftest.txt` |
| `scripts/check_gptp_docs.py` | OK, 8 current pages | `receipts/gptp_docs.txt` |
| `docs/DOC_MAP.gen.py --check` | OK | `receipts/doc_map_check.txt` |
| `scripts/check_solution_docs.py` | OK | `receipts/solution_docs.txt` |
| `scripts/check_feature_status.py` (with git, git-stripped) and `--self-test` | 0 findings | `receipts/feature_status.txt`, `receipts/feature_status_nogit.txt`, `receipts/feature_status_selftest.txt` |
| `docs/traceability/gen_module_matrix.py --check` | up to date | `receipts/module_matrix_check.txt` |
| `scripts/check_hygiene.py --check` | PASS, 829 files | `receipts/hygiene_check.txt` |
| `scripts/check_archive.py` | OK, 21 historical pages | `receipts/archive_check.txt` |
| `scripts/check_todo_ownership.py` | OK | `receipts/todo_ownership.txt` |
| `scripts/ci_events.py --check` and `--selftest` | OK with 1655 contract items; selftest PASS with 2206 arms | `receipts/ci_events_check.txt`, `receipts/ci_events_selftest.txt` |

None of these gates reads a registry, workflow pin or record that either lane changed. Neither lane touches `scripts/`, `.github/`, `docs/testing/`, configs, HDL or gitlinks.

## Fault probes

Each probe is one disposable commit on a scratch clone of the candidate. Each was judged by `compose_check.py`, `docs_check.py` and `check_em_dash.py --base d4dd7426` (`receipts/mutation_probes.txt`).

| Probe | compose_check | docs_check | check_em_dash |
|---|---|---|---|
| Duplicate the #629 row | FAIL (appears 2 times) | 0 findings | 0 findings |
| Drop the #117 B5 row (a bad conflict resolution) | FAIL (row order) | 0 findings | 0 findings |
| Break the #629 row's link target | FAIL | 1 finding: broken link, README.md:15 | 0 findings |
| Swap the #629 row below its neighbour | FAIL (row order) | 0 findings | 0 findings |
| Insert U+2014 into the #629 row | FAIL (row not byte-equal to source) | 0 findings | 1 finding: README.md:15 |

So the composition check fails on each defect it claims to detect. The repository gates catch the broken-link and em-dash classes. Row duplication, loss and reordering are caught only by the composition check, not by any repository gate. All three properties hold at this head.

The review clone was never edited. After the probes it was checked again:

- HEAD is `df943ae8`, and the index tree `01d643b8` equals the head tree.
- `git diff --quiet HEAD` is clean and there are no untracked files.
- Every tracked regular file re-hashes to its index blob (0 mismatches).
- The index mode and blob digest equals the `ls-tree` of HEAD.
- The four gitlinks are at the recorded commits (`receipts/clone_integrity.txt`). The `external` submodule is not checked out in this clone (`-` in `git submodule status`), and its gitlink is unchanged.

## Findings

### R427-3-S1 - SUGGESTION - Docs - the #629 page cites lane B5 by PR, and the B5 page is now in the tree

- **Artifact:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:397-399`.
- **Evidence:** the page was written while PR #628 was still open, so it cites "Lane B5 ([PR #628](...))". In the composed tree B5's page is at `docs/findings/117_AUDIO_CONTINUITY.md`, and the cited figure is at its line 302. The PR link resolves and the figure agrees, so nothing is wrong.
- **Impact:** a reader of the merged tree needs one extra hop to reach the B5 figure.
- **Optional outcome:** a later docs change may add an in-tree link beside the PR link. This is not required for this merge and does not affect coverage.

No BLOCKER, MAJOR or MINOR finding.

## Prior public findings on PR #630

These were read after this round's own pass. Every prior finding concerns the #629 page content, which this round does not re-review. The composed page blob is byte-identical to the source head `26dfc82f` (`93f8eb68`), so the composition neither resolves nor reintroduces any of them. Their disposition belongs to the source reviews at `26dfc82f`.

| Finding | State on the public record | Disposition at this head |
|---|---|---|
| R426-1 F1, F2, F3 (MINOR) | Marked resolved by R427-2 at `e3f28f2f` | Carried unchanged; the page bytes are from `26dfc82f` |
| R427-1 F1, F2, F3 (MINOR) | Marked resolved by R427-2 at `e3f28f2f` (F3 by the manager, in the PR body) | Carried unchanged |
| R426-2 F1 (MINOR, the archive spelled the capture layout) | Manager comment 5933253119: masked at archive `422dcf91`, with the page re-pinned in round 3 | Confirmed mechanically only: the composed page pins `422dcf91` and no other archive commit. Judging the content belongs to the `26dfc82f` source reviews. |
| R426-2 F2 (MINOR, clusters on the wrong absorption branches) | Commit `26dfc82f` says it places A1's cluster 9 and A2's clusters 17 and 56 | Not judged here, because it is page content; it belongs to the `26dfc82f` source reviews |
| R427-2 S1-S4 (SUGGESTION) | Optional | No effect on coverage |

## Ledger

This ledger is owned by the reviewer. The "Composition touches" column says whether merging with B5 changes anything within the lens's scope.

| Lens | State | Composition touches | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | The index only. Both acceptance-summary rows are byte-equal to their reviewed sources. No requirement, clause or acceptance text changed. | `docs/findings/README.md:15` and `:22`; `receipts/compose_check.txt`; page blobs `93f8eb68` and `9e2fae6c` | R427-3 for the composition; page content by the `26dfc82f` source reviews | `df943ae83af96553362ccf58ff96089d1c31ee04` |
| RTL | CLEAN | No. Apart from the two findings pages and the index, no HDL, constraint, config or gitlink path differs from either parent. | `receipts/composition_paths.txt` (name-status of all three edges; gitlinks identical at the base, both parents and the candidate) | R427-3 for the composition; RTL scope by the `26dfc82f` source reviews (R426-3 and the paired external source review the manager cites) | `df943ae83af96553362ccf58ff96089d1c31ee04` |
| Robustness | CLEAN | Yes, through the merge mechanics. The candidate tree equals the mechanical merge, and five fault probes (duplicate, drop, reorder, broken link, em dash) were each detected. | `receipts/compose_check.txt`, `receipts/mutation_probes.txt` | R427-3 | `df943ae83af96553362ccf58ff96089d1c31ee04` |
| Tests | CLEAN | No test file changed. For the shared file, the executable evidence is the docs gates run on the candidate, plus a composition check shown to fail on each planted defect. | The gate receipts listed under "Gates run on the candidate"; `compose_check.py`; `receipts/mutation_probes.txt` | R427-3; the page's test scope by the `26dfc82f` source reviews | `df943ae83af96553362ccf58ff96089d1c31ee04` |
| Docs | CLEAN | Yes: `docs/findings/README.md` is the one shared file. | `docs/findings/README.md` (17 rows; both added rows appear once, in each head's order; 21 links resolve); the cross-figure at `629_MEDIA_CLOCK_FOLLOWING_BENCH.md:399` against `117_AUDIO_CONTINUITY.md:302`; S1 is a SUGGESTION only | R427-3 | `df943ae83af96553362ccf58ff96089d1c31ee04` |

## Limits and pending manager duties

- **Source POSITIVE pair at `26dfc82f`:** when this round ran, the public PR thread showed R426-3 started at `26dfc82f`. The last public verdicts were at `e3f28f2f`: R427-2 POSITIVE, and R426-2 NEGATIVE with F1 and F2. The manager states that two independent POSITIVE source reviews exist at `26dfc82f`. This composition POSITIVE relies on them for the page content and for R426-2 F1 and F2. Before merge, the manager must have both published, each naming `26dfc82f`.
- **Hosted evidence:** the candidate `df943ae8` is not on the remote, so it has no hosted checks. At the source head `26dfc82f`:
  - succeeded: `rtl-fast`, `full-ci-gate`, `elaborate`, `wire-accountability`, `docs-check-no-git`, `bdd-conformance` and `changes`;
  - still in progress when read: `docs-check`;
  - skipped contexts, not executed: `verilator-suites`, `yosys-portability`, the Verilator and Yosys shards, `verilator-lint`, `yosys-elaboration` and physical gPTP.

  Hosted and act acceptance remain the manager's.
- **Final candidate:** this round judged the merge-train candidate built on live dev `d4dd7426`. If dev moves before the merge turn, the manager's final current-dev candidate must be validated again. This verdict does not transfer to a different tree.
- **Not run:**
  - The full parent, PP, gPTP, Yosys, builder and native banks. The assignment excluded them, and nothing in their scope changed.
  - Any simulator, because the composition contains no HDL.
  - The docs workflow's non-docs steps (SDK, sv2v, builder, NVM and the idiom gates). Neither lane touches their inputs.
- **Physical:** calibration NOT RUN, and field skips are not hardware proof. Nothing here is bench evidence.
- **Repository gate gap (not a defect at this head):** no repository gate detects a duplicated, dropped or reordered findings-index row; only this round's composition check does. Adding such a guard is new work for its own Issue.

R427-3 FINISHED
