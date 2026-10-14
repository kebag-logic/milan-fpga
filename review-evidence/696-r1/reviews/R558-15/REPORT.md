[R558] POSITIVE - exact head 2c00861eb4c2a84e6a39a9b191d39b9d6aa38c81

# R558-15 - issue #696 / PR #706 - composition review of the merge-train candidate

Internal independent reviewer, cleared context, composition acceptance only.

- Candidate `2c00861eb4c2a84e6a39a9b191d39b9d6aa38c81`, tree `8f36c9035e32b78a26adbafa2ddb40719fc9380e`.
- Ordered parents: live dev `0136de16291a127e0a34627c77ac09cd41efc08b` and PR #706 head `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`.
- The PR head has two POSITIVE source reviews: R558-14 (comment 6153422555) and R559-11 (comment 6153298926).
- Live remote at review time: `dev` = `0136de16`, `696-maap-annexb` = `e2cd089c` (`receipts/ls_remote.txt`).

Order of reconstruction: AGENTS.md and CONTRIBUTING.md; the docs map; the issue #696 body and acceptance; the manager's round comments 6142198285 and 6148294623; the candidate diff and history; the public evidence tree `217cf130` (`review-evidence/696-r1/author-r14`, its receipt list only); the exact-head hosted check runs (read only). Prior public findings were read only after sections 1 to 5 were written (section 7).

## Summary

- The candidate tree equals `git merge-tree --write-tree 0136de16 e2cd089c` (`8f36c903`). The merge base is `d40e4e98`, PR #705's 697c head, so the shared stack enters both sides from the same commit and the composition neither duplicates nor reverts any of it.
- Since that base, dev changed four paths and the PR seventeen. Exactly one path is changed by both: `docs/findings/README.md`. Every other path in the candidate carries its changing side's blob and mode exactly.
- In `docs/findings/README.md`, the 629 row equals dev's (PR #725, B16) and the 234 row equals the PR's (#696 first-draw re-baseline of 2026-10-10). Every other line equals both sides, and the table still renders under the pinned GFM renderer as one table with 22 rows of 3 cells.
- Every gate that reads the composed files passes on the candidate. That includes docs_check, gen_toc `--check` and `--verify-anchors`, em-dash against both parents, ci_events `--check`/`--selftest`, the B16 figures check and 25 more static gates (section 3).
- The B16 figures check gives byte-identical rows, coverage and summary to its published round-11 receipt. A planted change to the 629 row's lane-B16 figure makes it fail (rc 1). The PR's 234 row is outside its scope.
- No BLOCKER, MAJOR or MINOR. One new RESIDUE in the PR body (R558-15-R1). The prior residues are retained, and the earlier findings are still resolved.

## 1. Composition identity

`scripts/composition_identity.sh` -> `receipts/composition_identity.log`, rc 0.

| Check | Result |
|---|---|
| `merge-base 0136de16 e2cd089c` | `d40e4e9827be2516f8f34b9d65f0a483fff2194c` (PR #705 head; dev's second parent; an ancestor of `e2cd089c`) |
| `merge-tree --write-tree 0136de16 e2cd089c` | `8f36c9035e32b78a26adbafa2ddb40719fc9380e`, clean, equal to the candidate tree |
| Dev-side paths since `d40e4e98` | `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, `docs/findings/README.md`, `docs/testing/CI_WORKFLOWS.md`, `scripts/act_ci.py` (PRs #725 and #731) |
| PR-side paths since `d40e4e98` | the 17 files of `git diff --stat 0136de16..2c00861e`, the same set exactly |
| Changed on both sides | `docs/findings/README.md` only |
| Candidate blob and mode per path | 16 PR paths equal `e2cd089c`; 3 dev paths equal `0136de16`; README is `both-changed` and is compared row by row (section 2) |
| Gitlinks | All six gitlinks are identical in dev and the candidate (tsn-c-stack `405dc683`, protocol-processor `2ad2f845`, gptp-processor `7dda9c3b`, lwSRP `08ee86e8`, verilog-axis `48ff7a7e`, external `efeb541a`) |

Shared-stack lineage. #705 (dev `a0f39ad4..0136de16`) and the PR both touch `sw/firmware/ctrl/maap/README.md` and `sw/firmware/ctrl/test/maap_differential.py`. Both sides take those files from `d40e4e98`. The PR's hunks since `d40e4e98` build on 697c's `STACK`/`stack_pin` code (`maap_differential.py:23,38,71-73,81-92`; README `:204-207`) and remove none of 697c's lines (`README:19-20,183-184` and the differential's stack-pin docstring stay). This merge was already resolved at `e2cd089c` and reviewed in R558-14. The composition adds nothing to it.

## 2. The shared file, docs/findings/README.md

`scripts/index_rows.py` -> `receipts/index_rows.json`, rc 0.

| Line | Row | Candidate equals | Dev equals PR? |
|---|---|---|---|
| 15 | `629_MEDIA_CLOCK_FOLLOWING_BENCH.md` | dev `0136de16` (lanes B15 and B16, B16b, B16c, rounds 2-10) | no |
| 25 | `234_PP_SHADOW_AREA_BASELINE.md` | PR `e2cd089c` ("#696's first-draw re-baseline of 2026-10-10") | no |
| all others | - | both | yes |

All three versions have the same line count. The pinned renderer (cmarkgfm 2025.10.22, html5lib 1.1, installed by hash from `tools/markdown/requirements.txt` into a scratch environment) yields one table of 22 rows of 3 cells for each.

The 234 row links to `../design/AREA_BUDGET.md#headroom-target`. In the candidate that heading is `docs/design/AREA_BUDGET.md:116`, and `:110-111` names #696's lane-head `bee1b0d7` re-record as the gate's record. `gen_toc.py --verify-anchors` reproduces all 495 cross-page fragments.

## 3. Gates on the candidate

Every gate below ran on the candidate checkout at `2c00861e`. Logs and rc files are in `receipts/` and `receipts/gates/` (`scripts/run_gates.sh` for the batch).

| Gate | Reads composed files | rc | Result line |
|---|---|---|---|
| `docs_check.py` | README, 629 page, CI_WORKFLOWS | 0 | 0 finding(s) across 206 md files + 1287 scrubbed text files |
| `docs_check.py --selftest` | - | 0 | PASS (23 scrub + 4 routing) |
| `gen_toc.py --check` | all pages | 0 | 146 pages carry a contents list |
| `gen_toc.py --verify-anchors` | cross-page links | 0 | 495 fragment links reproduced |
| `gen_toc.py --selftest` | - | 0 | 1501/1501 arms |
| `check_em_dash.py --base 0136de16` | PR's added lines | 0 | 0 findings over 347 added lines in 7 pages |
| `check_em_dash.py --base e2cd089c` | dev's added lines | 0 | 0 findings over 2508 added lines in 3 pages |
| `check_em_dash.py --selftest` | - | 0 | 339 arms |
| `ci_events.py --check` / `--selftest` | CI_WORKFLOWS.md (dev-changed) | 0 / 0 | 2169 contract items; 3064 arms |
| `check_doc_paths.py` | all cited paths | 0 | 982 resolve, 10 line anchors in range |
| `check_doc_style.py` (+ `--selftest`) | current docs | 0 / 0 | 22 current documents |
| `suite_shards.py --selftest` | `maap` duration 1375 | 0 | PASS |
| `syn/ooc/pp_resource_gate.py check-baseline` | `pp_resource_baseline.json`, AREA_BUDGET policy | 0 | baseline PASS: 3 endpoints |
| B16 figures check (published `author-r11/tools/check_b16_figures.py`, receipt root `author-r10`) | 629 page and README:15 | 0 | 1960/1960 rows, 0 uncovered, markup 0 |
| check_gptp_docs, DOC_MAP --check, timesync_chain --check, check_solution_docs, submodule_boundaries --check, check_submodule_docs, check_diagram_pngs, check_baremetal_only, check_nvm_record_space, check_soc_sources, check_rtl_source_lists, measure_naming, check_port_contracts, measure_fail_fast, check_todo_ownership, measure_test_evidence, check_hygiene, check_sv/cpp/py/sh_idiom, check_archive, check_feature_status | inventories | 0 each | see `receipts/gates/*.log` |

`check_diagram_pngs.py` needs its own directory on the module path, so it was run without isolated mode; the first isolated attempt failed only on that import, and the log in `receipts/gates/check_diagram_pngs.log` is the second run.

B16 figures check. The check was taken from the public branch `629-b16-review-evidence` at `6cc649ce`, under `review-evidence/629-b16-r1/`, and run with the pinned renderer.

| Run | Input | rc | Outcome |
|---|---|---|---|
| `cand` | candidate page and README | 0 | rows, coverage and stdout byte-equal to `author-r11/receipts/cand-*` |
| `fixture_exact` | copies of the candidate's two pages | 0 | same summary (fixture control) |
| `fixture_mut629` | README:15 `-14.1 dBFS` -> `-14.2 dBFS` | 1 | `BAD 1013 README.md:15 -14.1` and `UNCOVERED README.md:15 -14.2` |
| `fixture_dev234` | README with dev's 234 row, i.e. without the PR's edit | 0 | same summary: the PR's row is outside the check's scope |

Semantic interactions checked:
- The 629 page cites `hdl/milan/milan_datapath.sv:445` as the CRF port contract. The PR changes that file, but its `:264` comment edit is net zero lines and its other insertion is at `:7181`. So `:445` is still the `clk_audio_i` contract comment that names `KL_crf_tx`'s divide by 512.
- `CI_WORKFLOWS.md:191` and `:297` name `pp_resource_baseline.json` and `maap`'s duration. Neither line changed on dev since `d40e4e98`, and the gates that hold them (`ci_events`, `check-baseline`, `suite_shards --selftest`) pass.
- Dev's `act_ci.py` change (#731) pins containers to CPU ranges and keeps `nproc`. It touches no make flag, so it does not interact with the PR's `integration.mk:8-22`, which clears `MAKEFLAGS`. A search of its added lines finds no reference to MAAP, findings, area records or the PR's test paths.
- The composition adds no RTL, synthesis, testbench or firmware path relative to `e2cd089c`. So the resource record's relation to the merged RTL is the same one the source reviews accepted.

Hosted (read only). At PR head `e2cd089c`, 28 check runs succeeded and 1 was skipped (`Physical gPTP (nightly and manual)`), recorded in `receipts/hosted_checkruns_e2cd089c.tsv`. The candidate `2c00861e` is not on the remote, so it has no hosted runs. Hosted and act acceptance belong to the manager.

## 4. Findings of this round

### R558-15-R1 - RESIDUE - Docs - PR #706 body `:27-28`, `:175` - review status predates R558-14 and R559-11

- **Evidence:** the body (snapshot `receipts/pr706_body_snapshot.md`, sha256 `45730925...`, PR updated 2026-10-14T00:57:35Z) says at `:27-28`: "R558-13 and R559-10 are POSITIVE at `313616d1`. Those verdicts precede this merge; independent review of this head remains pending." R558-14 and R559-11 are POSITIVE at `e2cd089c` (comments 6153422555 and 6153298926). `:175` still lists "Independent review of this head" among the manager duties.
- **Why RESIDUE:** this is PR-body wording only. It changes no measurement, figure, verdict, test, code, generated artifact, conformance or clause claim, and touches no privacy rule.
- **Exact fix:**
  - `:27-28` becomes "R558-14 and R559-11 are POSITIVE at `e2cd089c`. Composition review R558-15 covers merge-train candidate `2c00861e` (dev `0136de16` merged with this head)."
  - `:175` becomes "Hosted acceptance, workflow replication and the current-dev candidate validation remain manager duties."
- **Verification:** reread the body against the PR's review comments.

## 5. Lens results

```text
[R558] PASS Conformance - issue #696 acceptance 1-4; receipts/composition_identity.log (KL_maap.sv, MAAP_FABRIC.md, sim_main.cpp, mutants.py, pp_resource_baseline.json equal e2cd089c); receipts/gates/pp_resource_check_baseline.log - the composition changes no artifact any acceptance item is judged by. AC3's record and policy are unchanged and check-baseline passes. AC4 (bench) is unchanged and not run. Source conformance is banked by R558-14 and R559-11 at e2cd089c.
[R558] PASS RTL - receipts/composition_identity.log (hdl/ieee1722/maap/KL_maap.sv 746be52d, hdl/milan/milan_datapath.sv e0ad4691 equal e2cd089c; dev adds no hdl/syn path since d40e4e98; gitlinks equal dev) - the composition is outside RTL scope. RTL is banked by R558-14 and R559-11 at e2cd089c, an ancestor whose RTL scope is untouched since.
[R558] PASS Robustness - receipts/composition_identity.log (KL_maap.sv, sim_main.cpp 9dfc863a, sim_integration.cpp e02f65f7, integration.mk 0d005fd0 equal e2cd089c); scripts/act_ci.py diff d40e4e98..0136de16 (CPU ranges only, nproc kept, no make flag) - no robustness-scoped path changes, and dev's runner change does not touch integration.mk's MAKEFLAGS handling. Banked by R558-14 and R559-11 at e2cd089c.
[R558] PASS Tests - receipts/b16/{cand,fixture_exact,fixture_mut629,fixture_dev234}.*; receipts/ci_events_*.log; receipts/gates/suite_shards_selftest.log; receipts/composition_identity.log (tb/verilator/maap/*, sw/firmware/ctrl/test/* equal e2cd089c) - the gates that read the composed files pass. The B16 check equals its published receipt and fails on a planted README:15 change. The MAAP suites, mutants and differential are byte-equal to the source head.
[R558] PASS Docs - docs/findings/README.md:15,25 (receipts/index_rows.json); docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:463 -> hdl/milan/milan_datapath.sv:445; docs/design/AREA_BUDGET.md:110-111,116; docs/testing/CI_WORKFLOWS.md:191,297; docs_check, gen_toc --check/--verify-anchors, em-dash x2, check_doc_paths, check_doc_style receipts - each row equals its side, the table parses, the anchors resolve and the cross-references hold. The PR-body status wording is R558-15-R1 (RESIDUE, no lens effect).
```

## 6. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition outside scope: AC artifacts byte-equal to source head; check-baseline PASS on candidate | R558-14 and R559-11 (source); R558-15 (composition) | `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`; `2c00861eb4c2a84e6a39a9b191d39b9d6aa38c81` |
| RTL | CLEAN | Composition outside scope: KL_maap.sv, milan_datapath.sv byte-equal; no dev RTL since `d40e4e98`; gitlinks equal | R558-14 and R559-11 (source); R558-15 confirms no touch | `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`; `2c00861eb4c2a84e6a39a9b191d39b9d6aa38c81` |
| Robustness | CLEAN | Composition outside scope: MAAP RTL, benches, integration.mk byte-equal; act_ci.py change has no make interaction | R558-14 and R559-11 (source); R558-15 confirms no touch | `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`; `2c00861eb4c2a84e6a39a9b191d39b9d6aa38c81` |
| Tests | CLEAN | Composition touches scope through README:15 (B16 check) and the CI contract: B16 check PASS + mutation probe, ci_events, suite_shards, 25 static gates | R558-15 | `2c00861eb4c2a84e6a39a9b191d39b9d6aa38c81` |
| Docs | CLEAN (RESIDUE R558-15-R1, plus the retained residues in section 7) | README rows 15 and 25, table parse, 629 page `:463`, AREA_BUDGET `:110-116`, CI_WORKFLOWS `:191,297`, docs gates | R558-15 | `2c00861eb4c2a84e6a39a9b191d39b9d6aa38c81` |

## 7. Prior public findings at this head (read after sections 1-5)

| Finding | State at `2c00861e` | Evidence |
|---|---|---|
| R558-14-R1 (RESIDUE, PR body publication wording) | **Resolved** | The body now reads "published as the PR #706 head" (`:17`) and "To check out this head:" (`:101`), and `:175` no longer lists publication |
| R559-11-R1 (RESIDUE, the same body sentences) | **Resolved** | Same lines as R558-14-R1 |
| R558-14-R2 (RESIDUE, `author-r14/HANDOFF.md:70-73` line pointers) | **Retained** | At evidence commit `217cf130` the lines still read ":75 copies", ":80 the RTL plant" and ":107 both command modes". This is a packet file, not a tree file |
| R558-2-R1 / R559-2-R1 (RESIDUE, `MARK_II_AREA_PLAN.md:66,67,317,1129`) | **Retained** | Blob `ee1c9b75` equals `e2cd089c`, and the four lines still carry the unqualified wording |
| R558-5-R1 (RESIDUE, `AREA_BUDGET.md:372,389`; `MARK_II_AREA_PLAN.md:669`) | **Retained** | Blobs equal `e2cd089c`; the lines still read "...remain unchanged" / "...are unchanged" |
| R558-11-F1, R558-9-F1, R558-5-F1 (MINOR), R558-1-F1, R558-3-F1 = R559-3-F1 (BLOCKER), R558-6-F1, R558-7-F1, R559-1-F1/F2/F3, R559-6-F1/F2 | **Still resolved** | Resolved at `e2cd089c` per R558-14 section 8 and R559-11. Every artifact they concern is byte-equal in the candidate (`receipts/composition_identity.log`) |
| Earlier SUGGESTIONs (R558-3/4/6/7/8, R558-14-S1, R559-1/3/4/5/6/7) | **Retained, optional** | No lens effect |

No finding is treated as resolved by moving it to another issue.

## 8. Limits

- Composition acceptance only. RTL behavior, the MAAP suites, the mutation campaign and the differential were not re-executed here. Their sources are byte-equal to `e2cd089c`, and their execution evidence is the author's round-14 receipts plus the hosted runs at `e2cd089c`. No manager source bank runs at this head, and none is claimed.
- Not run, by assignment: the full parent, PP, gPTP and Yosys banks, the builder, Docker/act, the host `act_ci.py` and its selftest, hardware and Vivado. `gen_hdl_reference.py`, the wavedrom checks, `make -C gptp-processor docs`, the RV32 SDK and builder steps of the docs workflow were also not run. None of their inputs is a composed file.
- Physical calibration NOT RUN. Acceptance 4 (bench interop with the reference peer) is not established by this review. Field skips are not hardware proof.
- The B16 figures check is the published packet's tool, not a tree tool. It was run unmodified from a scratch extraction.
- The candidate commit is local to this clone and is not on the remote, so it has no hosted runs.
- After the probes, the clone was restored: HEAD and tree are exact, index equals the HEAD tree, there are no untracked or ignored files, all submodules are clean and all six gitlinks are exact (`receipts/restore.txt`). The bytecode caches the gates created were removed. One temporary remote-tracking ref used for the B16 fetch was deleted. Fetched objects remain in the object store.

## 9. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn with the builder and native banks (source base `0136de16`, live dev `0136de16`), and link its receipts on the PR.
- Own hosted and act acceptance for the merge head.
- Carry R558-15-R1, R558-14-R2, R558-2-R1 / R559-2-R1 and R558-5-R1 to the residue checklist.
- Post-merge containment, closing #696 and moving it to Done. Acceptance 4 stays with the post-merge bench lane.

R558-15 FINISHED
