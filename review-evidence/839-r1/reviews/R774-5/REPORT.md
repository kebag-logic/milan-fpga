[R774] POSITIVE - exact head cf4120f4cf6c711781b9e4aa24173691dcce0a95

Round R774-5, external independent review of PR #841 (issue #839). Head `cf4120f4cf6c711781b9e4aa24173691dcce0a95`, tree `566fd3ae6acece2e2853310f9ef9e076ae3638a0`. The delta since the head round 4 reviewed is `4f210018..cf4120f4`: the merge of dev `87e9d03a` (`19f4c0b4`) and one regeneration commit (`cf4120f4`).

Verdict: no open BLOCKER, MAJOR or MINOR. One RESIDUE and three SUGGESTIONS.

- **The merge keeps both sides.** Replaying it gives the merge commit's tree, apart from the one conflicted generated page.
- **The audit is exactly the generator's output.** `--check` exits 0, and my regeneration is byte-identical in three separate trees.
- **There is one merge base, `87e9d03a`, and no other file changed.** Live dev is still `87e9d03a`.

**Read this before relying on the Tests row.** Two documented manual tests do not pass at this head, and no earlier round's report mentions either one:

- `tb/verilator/milan_dp/test_sim_pool.py` exits 1, with 16 of 17 arms passing (S1).
- `tb/verilator/milan_dp/test_sim_pool_backpressure.py` never finishes: it blocks forever at its first `make` case (S2).

Neither comes from this delta or from this PR's changes. Both trace to dev commits that predate the PR, and no workflow runs either test. I classed them as SUGGESTION because of this round's rule that code the delta does not touch keeps its prior lens verdict. That is a judgement call, and section 4 says what changes if the manager reads it differently.

## 1. The three assigned checks

Commit roles: `4f210018` is the prior head, `87e9d03a` is dev, `cc204c6f` is the base of the merge, `19f4c0b4` is the merge, and `cf4120f4` is this head.

| # | Claim | Method | Result | Receipt |
|---|---|---|---|---|
| 1a | Merge replay | `git merge-tree --write-tree 4f210018 87e9d03a`, compared with `19f4c0b4` and the head | One conflict, in `docs/DOCUMENTATION_AUDIT.md`. `docs/testing/TESTING.md` auto-merged. The replay tree differs from the merge in the audit only | `receipts/02-merge-replay.txt` |
| 1b | Files only dev changed | Blob comparison | `scripts/owned_process.py`, `scripts/process_test_support.py`, `scripts/test_suite_cancellation.py` and `tb/verilator/gptp_shadow/test_mutant_lifecycle.py` equal dev at the head | `receipts/02-merge-replay.txt` |
| 1c | `TESTING.md` keeps both sides | Line-level check against `cc204c6f` | PR side +5/-3 and dev side +90/-6: 0 lines lost, 0 removed lines returned, 0 merged lines found on neither parent | `receipts/06-merge-sides.txt` |
| 1d | The PR's content is unchanged | Name-status of `cc204c6f..4f210018` against `87e9d03a..cf4120f4` | The same 18 files | `receipts/02-merge-replay.txt` |
| 2a | Fresh at the head | `--check` in the clone | rc 0, `540 lines ... is fresh` | `receipts/04-check-inplace.txt` |
| 2b | Byte-identical regeneration, Git population | `--write` in a clean clone of the head | Audit sha256 `1d66bb1c...` and data sha256 `6b53c9b3...` both identical; 0 porcelain lines | `receipts/05-regen-probe.txt` A |
| 2c | Byte-identical regeneration, no Git metadata | `--write` on an archive of the head | Both identical | `receipts/05-regen-probe.txt` B |
| 2d | The commit was needed and is generator output | At `19f4c0b4`: `--check`, then `--write` | rc 1 (`73,487` against `73,640`), then byte-identical to the head; only the audit changes | `receipts/05-regen-probe.txt` C |
| 2e | The gate can fail | On a head copy: one extra `TESTING.md` line, an edited total, an edited line count | Each rc 1; restored rc 0. `--selftest` rc 0, 50 controls | `receipts/05-regen-probe.txt` D, E |
| 2f | Independent recount | Counted every page row from the head's blobs | 213 rows, 0 mismatches, total 92,369, equal to the summary row | `receipts/06-merge-sides.txt` |
| 3a | One merge base | `git merge-base --all HEAD 87e9d03a` | One base, `87e9d03a`; 20 commits ahead, 0 behind | `receipts/01-topology.txt` |
| 3b | No other file changed | Name-status of `19f4c0b4..cf4120f4` and `4f210018..cf4120f4` | The regeneration commit touches the audit only. The delta is 6 files, all also in `cc204c6f..87e9d03a`. 0 mode changes | `receipts/01-topology.txt`, `receipts/13-final-integrity.txt` |
| 3c | Submodule pins | Gitlink digest at `4f210018`, `87e9d03a` and the head | Identical | `receipts/13-final-integrity.txt` |

`scripts/docs_inventory.json` is generator input: `--write` does not write it. Its bytes are unchanged, so "what `--write` generates" holds for the audit, and for the data file only in the sense that it stays the same.

The merge commit took dev's audit blob verbatim (`9fdb8bf4`), so `git diff-tree --cc` does not list it. The regeneration commit then restores this PR's 13 lines. The audit's only difference from `4f210018` is 4 lines, from dev's `TESTING.md` edit: `TESTING.md` is 2021 lines (1937 + 84), the line totals move, and D0-057 moves to line 1904, which I checked holds its quote.

## 2. Does the delta change what this PR depends on

- **No PR file imports a dev-changed module.** `bootsa_mutants.py` and `test_sim_pool.py` import `suite_tally`, which the delta does not touch. `scripts/measure_test_evidence_readers.py:160` names `test_mutant_lifecycle.py`, but only as a table key, and dev's change there is one timeout value (5 to 15).
- **The artifacts under every retained finding are unchanged.** `milan_datapath.sv`, `sim_boot_sa.cpp`, `bootsa_mutants.py`, `gen_boot_fw.py`, `bootsa_probes.vlt`, `milan_dp/README.md`, `REGISTER_MAP.md`, `BAREMETAL_FIRMWARE.md`, `CHANGELOG.md` and both inventory files all have the same blob at `4f210018` and the head (`receipts/14-retained-artifacts.txt`). So I did not rerun `bootsa` or `bootsa-mutants`.
- **`measure_test_evidence.py --check`** exits 0 at the head. Its reader table still matches after dev's changes.

## 3. Documentation gates at this head

All rc 0 at the head: `check_doc_style.py` and `--selftest`, `check_doc_paths.py` (1631 paths), `check_archive.py`, `docs_check.py` (0 findings, 213 pages), `check_feature_status.py`, `gen_toc.py --selftest`, `--verify-anchors` and `--check`, `check_em_dash.py` against the prior head and against dev (0 findings), and `git diff --check` against dev.

`receipts/07-doc-gates.txt` shows rc 2 for two TOC runs and rc 1 for `sim_pool`. Those are first attempts. The TOC runs lacked the pinned renderer, which I then installed in scratch from the hash-pinned requirements (`receipts/09-toc-gates.txt`). That `sim_pool` run was in a copy with no submodules; the run that counts is in section 4.

Comment rule: the delta's added lines under `scripts/` and `tb/` carry no bench lane label, lane name, reviewer ID, round name or issue-comment ID. No new instance.

## 4. Findings

### S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/test_sim_pool.py:76-106` - the expected leg list has been missing two legs since 2026-10-27

- **Evidence.** `python3 tb/verilator/milan_dp/test_sim_pool.py` exits 1: `17 checks: 16 PASS, 1 FAIL` (`receipts/08-sim-pool-readme-command.log`). The failing arm is `arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs`. `make -n run` yields 18 legs and `LEGACY_LEGS` has 16. The only difference is `obj_sidmove` and `obj_sidmove8` (`receipts/08-sim-pool-arm-diff.txt`).
- **Origin.** Dev commit `18444ac64e` (2026-10-27) added both legs to `ORDINARY_CASES`. It is an ancestor of `cc204c6f`. The test contains no `sidmove` at `cc204c6f`, `87e9d03a`, `4f210018` or the head. The test and Makefile blobs are identical at `4f210018` and the head (`receipts/10-sim-pool-origin.txt`).
- **This PR's own row is correct.** The diff shows `bootsa` matching in name, banner and order. With the two rows added in memory, leaving the tree untouched, the arm passes (`receipts/08-sim-pool-arm-patched.txt`).
- **Impact.** The arm cannot currently detect a wrong leg list, including one affecting `bootsa`, because it fails either way. No workflow runs it, so the failure is silent. The docstrings at `:37` and `:874` still say "fifteen legs".
- **Required outcome.** A public Issue, outside this PR's scope, adds the two rows and corrects the docstrings.
- **Verification.** `python3 tb/verilator/milan_dp/test_sim_pool.py` reports 17 of 17.

### S2 - SUGGESTION - Tests, Robustness - `tb/verilator/milan_dp/test_sim_pool.py:287`, `tb/verilator/milan_dp/Makefile:588` - the backpressure test blocks forever at its first `make` case

- **Evidence.** `python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py` prints 14 PASS, then stops. After more than 800 s, `make` was defunct and the test was blocked in a pipe read (`receipts/08-sim-pool-backpressure-hang.txt`). The traceback from my interrupt ends at `next_start` (`test_sim_pool.py:287`), which reads with no timeout.
- **Cause.** Run directly in the retained fixture, `make` exits 2 at `Makefile:588`: `../nvm_capture_cpu/recipe.py did not yield CPU_HZ`. The fixture has no such sibling directory, so no leg ever starts and the test waits for one (`receipts/15-backpressure-origin.txt`).
- **S1 is not the cause.** I expected it to be, and tested that: with the two rows added in memory, the run stops at the same point (rc 124 at a 200 s bound, `receipts/08-sim-pool-backpressure-patched.txt`). That receipt is a one-line note I wrote; the raw log was not kept.
- **Origin.** The Makefile line comes from dev commit `9e53b1164d` (2026-09-29), an ancestor of `cc204c6f`. The test blob is identical at dev, `4f210018` and the head. I did not execute the test at dev, so "also hangs on dev" is inferred from those blobs.
- **Impact.** Anyone following `tb/verilator/milan_dp/README.md:59-60` gets a run that never ends rather than a failure. The stdout-backpressure behaviour has no working `make` coverage.
- **Required outcome.** A public Issue makes the fixture provide the clock recipe, and makes a `make` that exits early fail the case instead of blocking.
- **Verification.** The test finishes with every case passing, and a planted early `make` exit fails by name within a bound.

**Why SUGGESTION rather than MINOR, and what would change it.** The cause of both predates this PR, the delta changes nothing they depend on, and the round's rule keeps the prior lens verdict for such code. AGENTS.md section 4 sends newly found unrelated work to a new Issue. The argument the other way is that this PR edits `LEGACY_LEGS`, and section 7 says a finding moved to another Issue is not resolved. If the manager applies section 7 here, S1 and S2 become MINOR, the `Tests` and `Robustness` rows below become UNCLEAN, and this verdict becomes NEGATIVE. Either way, no prior report mentions these two tests, so the prior `Tests` coverage should not be read as including them.

### R1 - RESIDUE - Docs - PR #841 body, final round paragraph - the body stops at round 4

The body names `4f210018` as the head and `cc204c6f` as the base, and does not mention `cf4120f4` or `87e9d03a`. Those statements were true for round 4.

Exact fix, appended after that paragraph: "Round 5: head `cf4120f4cf6c711781b9e4aa24173691dcce0a95`, two commits on `4f210018` (no rebase, no force), base `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. `19f4c0b4` merges dev `87e9d03a` (PR #834), with one conflict, in the generated `docs/DOCUMENTATION_AUDIT.md`; `cf4120f4` is the output of `python3 scripts/docs_inventory.py --write` and nothing else."

### S3 - SUGGESTION - Tests - `.github/workflows` - neither pool test runs in any workflow

Both S1 and S2 stayed hidden because nothing runs these tests: `.github` has no match for `sim_pool`. The Issues above should decide whether they join a gate.

## 5. Prior findings at this head

| Finding | State at this head |
|---|---|
| R773-1 F1 = R774-1 F1 (MINOR, Tests), R773-1 F2 (MINOR, Docs, Tests) | Resolved in round 2. Resolving artifacts unchanged |
| R774-2 F1 (MINOR, Docs) = R773-2 RES-1 | Resolved in round 3. `milan_dp/README.md` unchanged |
| R773-1 RES-1 = R774-1 R2 (RESIDUE) | Applied in round 2 |
| R773-1 S1, S2; R774-1 S1; R773-2 S1, S2; R774-2 S4 | Taken. Unchanged |
| R774-2 S1, S2, S3 = R773-2 S3 | Retained, optional. Files unchanged |
| R773-2 S4 (PM2 is an equivalent mutant) | Informational. No `hdl/` change |
| R773-3 S1-S3, R774-3 S1-S4 | Retained, optional. Files unchanged |
| R773-4 S1, R774-4 S2 (D0-062 line reference) | Retained, optional. `docs_inventory.json` unchanged |
| R774-4 S1 (no-Git walk counts ignored cache directories) | Retained, optional. `docs_inventory.py` unchanged |

These states come from the prior reports' own resolution tables plus the blob identity above; I did not re-derive the round 2 and 3 resolutions.

## 6. Evidence and hosted state

- **Published packet.** `review-evidence/839-r1` at `b06fad40`. I fetched `MANIFEST.json` (2099 entries) and spot-checked `author-r4/HANDOFF.md` and two merge receipts: all three match their `published_sha256` (`receipts/11-evidence-spot-check.txt`). This was a spot-check, not a full verification.
- **Signature.** The manifest lists no signature file, and the API reports the evidence commit as `unsigned`. I therefore could not verify a signature and verified digests only.
- **Author receipts** stop at `4f210018`. None exist at this head, which matches the assignment.
- **Hosted, exact head, snapshot at 2026-11-06T11:57:16Z:** 11 completed success, 1 skipped (`Physical gPTP`, not executed), 6 in progress, 33 queued (`receipts/12-hosted-checks-snapshot.tsv`). It is unfinished, so it is no evidence of a final result. The manager owns hosted and act acceptance.

## 7. Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #839 acceptance and decision record 6655611611; delta file list; `hdl/milan/milan_datapath.sv` and `REGISTER_MAP.md` blobs unchanged (`receipts/14-retained-artifacts.txt`) | R774-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |
| RTL | CLEAN | No `hdl/` file in the delta (`receipts/01-topology.txt`); 6 gitlinks unchanged (`receipts/13-final-integrity.txt`) | R774-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |
| Robustness | CLEAN, with S2 recorded out of delta | Three dev scripts equal dev byte for byte; PR import graph; negative controls on the gate (`receipts/05-regen-probe.txt` D); S2 | R774-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |
| Tests | CLEAN for the delta, with S1, S2 and S3 recorded out of delta | `--selftest`; `measure_test_evidence.py --check`; both pool tests (`receipts/08-*`, `receipts/10-*`, `receipts/15-*`). `bootsa` and `bootsa-mutants` not rerun: inputs unchanged, last run at `4f210018` by R773-4 and R774-4 | R774-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |
| Docs | CLEAN | `docs/DOCUMENTATION_AUDIT.md`, `docs/testing/TESTING.md`, gates in section 3 (`receipts/05-*`, `06-*`, `07-*`, `09-*`, `16-*`); R1 is RESIDUE | R774-5 | `cf4120f4cf6c711781b9e4aa24173691dcce0a95` |

## 8. Limits

- `bootsa` and `bootsa-mutants` were not rerun here, and no parent bank was run.
- Neither pool test was executed at dev or at `4f210018`. One scratch-copy run at the parents was not permitted in this session, so origin rests on blob identity and commit ancestry.
- The S2 fix was not tested. Its cause comes from running the fixture's `make` directly.
- I interrupted the S2 runs. The two temporary directories they left under `/tmp` are removed.
- The in-memory `LEGACY_LEGS` edit never touched a tracked file.
- Physical calibration NOT RUN. Field skips are not hardware proof. Issue #839 stays open for the hardware capture under decision 6655611611.
- After all probes: tracked bytes, modes and index match the head, 0 porcelain lines, and the head and tree are as stated (`receipts/13-final-integrity.txt` plus a final status check).

## 9. Pending manager duties

- Decide the S1/S2 classification question in section 4.
- If it stands, open the public Issues for S1, S2 and S3; this round makes no GitHub writes.
- Carry R1 to the residue checklist.
- Build and validate the current-dev merge candidate, and link its receipts on the PR.
- Own hosted and act acceptance at the exact head.
- Confirm live dev at the merge turn; it was `87e9d03a` at the end of this round.
- R773-5 is still in flight, and no review round may remain in flight at merge.

R774-5 FINISHED
