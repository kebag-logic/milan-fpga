[R826] POSITIVE - exact head 6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c

# R826-5: external cleared-context delta review of PR #888 (issue #791)

- Head `6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c`, tree `e23dcaeaa23d7fd0f5b3e9ee67e92f101bfbb1e3`. Source base `1d6bf555`. Base branch `dev-soft-core`.
- The delta is `77e1efa0..6a5acf06`, two commits by the executor under the round-4 ruling on R826-4 (#791 issuecomment-6809199534):
  - `14a0c538` moves the mutant planting into a new module, `sw/litex/ctrl_memory_mutant.py`. It also restates the mutant count in `docs/testing/TESTING.md` and wraps docstring items 8 and 9.
  - `6a5acf06` re-keys the idiom gate's `exec` inventory entry to the new module.
- Four files change: `docs/testing/TESTING.md`, `scripts/check_py_idiom.py`, `sw/litex/ctrl_memory_mutant.py` (new) and `sw/litex/test_ctrl_memory.py` (`receipts/delta.diff`, `receipts/delta_facts.log`).
- Both commit messages are one line with no trailers.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR is open. Both R826-4 findings are fixed at their cause, and S1 was taken. This round records two new RESIDUE items (wording only) and carries forward the earlier RESIDUE and SUGGESTION items.

## Round-4 ruling items, checked at this head

| Ruling item | Result | Evidence |
|---|---|---|
| F1: `python3 scripts/check_py_idiom.py` exits 0 | **Met.** rc 0. `long module: 10 <= 10`, `dynamic eval/exec: 0`. `--selftest`: `54 checks: 54 PASS, 0 FAIL`, rc 0. | `receipts/py_idiom.log`, `receipts/py_idiom_selftest.log`, `receipts/*.rc` |
| F1: `scripts/py_idiom.budget` unchanged | **Met.** The blob is `008f7fd7` at both `77e1efa0` and the head. | `receipts/delta_facts.log` |
| F1: `test_ctrl_memory.py` is at most 1000 lines, and the moved code sits in a helper module under the limit | **Met.** `test_ctrl_memory.py` has 972 lines (it had 1003). `ctrl_memory_mutant.py` has 46 lines. | `git show HEAD:<file> \| wc -l` |
| F1: nothing dropped | **Met.** Old `test_ctrl_memory.py` L863-891 (`mutated`, `patched`) is byte-identical to `ctrl_memory_mutant.py` L18-46. Only the now-unused imports were removed: `__future__`, `ast`, `inspect`, `textwrap` and `Iterator`. The test imports both names back (L100), and every call site is unchanged (L349, L623, L900, L909, L960). The new module's only importer is the test. | `receipts/delta_facts.log` ("IDENTICAL", importer list) |
| F1: RESULT: PASS with 62 caught mutants, and both the CPU-decode and the mapper arms run | **Met.** rc 0, 192 `[ok]`, 0 FAIL, `RESULT: PASS`. 62 `MUTANT` oks: 33 checks + 11 decode + 7 sim + 7 soc + 1 banks = 59 from `MUTANTS`, plus 3 mapper. Arm headers `-- CPU decode` (log L113-125) and `-- out-of-context mapper` (log L198) both ran with no failure. The RV32 link arm ran (no SKIP). | `receipts/test_ctrl_memory.log`, `receipts/delta_facts.log` |
| F1: the docstring's item count equals what the file grades | **Met.** The header says "nine things", and items 1-9 map to the arms in `main()`: banks, rules (with planted ledgers), simulation, link, SoC build, register, mutants, mapper and CPU decode. | `sw/litex/test_ctrl_memory.py:7-63` against `:927-961` |
| F2: TESTING.md states the graded count and names the CPU-decode arm, and S9's mapper sentence is unchanged | **Met.** `TESTING.md:792` says "fifty-nine", which equals `len(MUTANTS)` (59, tallied above). `:795-798` names the CPU decode arm and links `ctrl_memory_decode.py`. The "Three more mutants" sentence (`:802-804`) is outside the diff hunk and byte-unchanged. 59 + 3 = 62, which matches the run. See RESIDUE R7 on how the arm is attributed. | `receipts/delta.diff`, `receipts/test_ctrl_memory.log` |
| S1: items 8 and 9 wrapped | **Met.** Items 8/9 now wrap at 58-71 columns, within the 79-column width of items 1-7. | `sw/litex/test_ctrl_memory.py:61-65` |
| No generated netlist or all-fabric export byte moved | **Met by dependency.** No delta file is an input to `milan_soc.py`, the builder or the LiteX generator. `ctrl_memory_mutant.py` is imported only by `test_ctrl_memory.py`, and `milan_soc.py`, `ctrl_memory.py`, `ctrl_memory_decode.py`, `hdl/` and `tb/` are untouched. I did not re-measure (see Limits). | `receipts/delta_facts.log` (name-status, importers) |
| The region-decode self-test passes | **Met.** `none: fails 0 check(s), wants 0`, `single-mask: 4/4`, `cover: 6/6`, `ctrl_region_decode self-test: PASS`, rc 0. | `receipts/region_selftest.log` |
| `git diff --check 1d6bf555..HEAD` | No output, rc 0. | `receipts/diff_check.log` |
| Docs gates | `docs_check.py`: 0 findings across 218 md files. `check_doc_paths.py`: OK, 1086 cited paths resolve. Both rc 0, run on a scratch clone of the head. | `receipts/docs_check.log`, `receipts/check_doc_paths.log` |

### Probes showing the F1 fix is at its cause

`scripts/gate_probes.sh` runs on a disposable clone, and `receipts/gate_probes.log` holds its output:

- **P0, unmodified head:** rc 0.
- **P1, inventory key changed back to `sw/litex/test_ctrl_memory.py`:** rc 1, `REFUSED DYNAMIC EVAL/EXEC: sw/litex/ctrl_memory_mutant.py:33`. The gate tracks the `exec` site by file, so the second commit is required, and it is enough.
- **P2, `test_ctrl_memory.py` set back to its `77e1efa0` bytes (1003 lines):** rc 1, `long module 11 > ratchet 10`. The original defect is still detected, and the move is what clears it.

Every probe edit was restored, and the clone was clean afterwards.

## Findings

No new BLOCKER, MAJOR or MINOR.

### R7 - RESIDUE - Docs, Tests - `docs/testing/TESTING.md:795` - "Twelve of them are its CPU decode arm's"

- **Evidence:** the count is right. `ctrl_memory_decode.MUTANTS` has 12 rows. Eleven are graded by the `decode` arm. The twelfth, "decode hookup removed" (`sw/litex/ctrl_memory_decode.py:69`), is graded by the `soc` arm, because the hookup it removes is in `add_ctrl_memory`. The run's tally shows "11 is caught by the decode arm" (`receipts/delta_facts.log`). Read as "the twelve the CPU decode arm grades", the sentence overstates by one.
- **Impact:** wording only. The figure (59), the run, the arms and the gates do not change.
- **Exact fix:** replace "Twelve of them are its CPU decode arm's (#791," with "Twelve of them come from its CPU decode arm (#791,". Then, after "...may read any other region list.", add: "Eleven turn that arm red; the twelfth, the hookup removed, turns the SoC arm red."
- **Verification:** reread against the arm column of `sw/litex/ctrl_memory_decode.py:57-82`.

### R8 - RESIDUE - Docs, Tests - `sw/litex/ctrl_memory_mutant.py:3` and `scripts/check_py_idiom.py:195-198` - `mutated` also rebuilds `ctrl_memory_ooc.py`'s `main`

- **Evidence:** the new module docstring says "one definition of ctrl_memory.py or milan_soc.py". The inventory entry says "rebuilds one function or class of ctrl_memory.py or milan_soc.py, both already imported". But the mapper arm passes `rebuild=partial(mutated, ledgers.mapper(), "main")` (`sw/litex/test_ctrl_memory.py:960`), and `ledgers.mapper()` returns `syn/ooc/ctrl_memory_ooc.py` (`sw/litex/ctrl_memory_ledger.py:139-144`, called at `:191`). So the same `exec` site also compiles that module's `main` for the three mapper mutants.
  - The inventory wording predates this delta (it was the same at `77e1efa0`). The docstring is a new instance, and the delta edited the entry.
  - The guard described ("matching exactly once", "exactly one definition", "that module's namespace") is accurate for all three owners.
- **Impact:** wording only. The gate's verdict is keyed by file path, not by this text, and the guards do not change.
- **Exact fix:**
  - In `ctrl_memory_mutant.py:3`, change "one definition of ctrl_memory.py or milan_soc.py rebuilt" to "one definition of ctrl_memory.py, milan_soc.py or syn/ooc/ctrl_memory_ooc.py rebuilt".
  - In `check_py_idiom.py:195-196`, change "ctrl_memory.py or milan_soc.py, both already imported" to "ctrl_memory.py or milan_soc.py, or ctrl_memory_ooc.py's main for the mapper mutants, each already imported". While there, reflow the short `"mutation check. Guarded "` line.
- **Verification:** `python3 scripts/check_py_idiom.py` stays at rc 0.

### Comment rule

The hand-written source text in the delta has no bench lane label, lane name, review round, reviewer ID or comment ID. That text is the helper docstring, the test docstring item 7 line, items 8/9 and the inventory string. A scan of the added lines for those patterns found nothing (`rc=1` on the grep). It cites issue `#791` and module identifiers only. The `(#665 S9)` tag on `TESTING.md:804` is old text the delta did not touch.

### Observation (no finding)

The first commit, `14a0c538`, is red on the idiom gate on its own: the moved `exec` was not yet in the inventory. The executor disclosed this in REVIEW READY, and `6a5acf06` fixes it. CONTRIBUTING.md has no rule that each lane commit must pass the gates, and the head is green.

## Prior findings, resolved or retained at this head

This round read the earlier public findings only after the independent pass above.

| Prior finding | State at `6a5acf06` | Disposition |
|---|---|---|
| R826-4 F1, MAJOR, Tests: idiom gate red (`test_ctrl_memory.py` 1003 lines, 11 > 10) | Gate rc 0 with the budget unchanged. P2 shows the old bytes are still refused, and P1 shows the re-keyed inventory is required. | **Resolved at its cause** |
| R826-4 F2, MINOR, Docs: TESTING.md mutant figure and CPU-decode arm | "fifty-nine" equals the graded `MUTANTS`. The arm and `ctrl_memory_decode.py` are named. The mapper sentence is unchanged. | **Resolved.** One attribution wording point is recorded as R7 (RESIDUE). |
| R826-4 S1, SUGGESTION: wrap items 8/9 | Wrapped, within the items' width | **Taken** |
| R826-3 S5, SUGGESTION: stale count | Superseded by F2 | **Resolved with F2** |
| R826-2/R826-3 R5, RESIDUE: "instead of building a decode other than the pieces" | `docs/design/SPLIT_CONTROL_MEMORY.md:55` and `sw/litex/milan_soc.py:3278-3279`; neither file is touched by the delta | **Retained as RESIDUE.** Exact fix as published in R826-3. |
| R826-3 R6, RESIDUE: check label "may read the whole rows after naming" | `sw/litex/ctrl_memory_decode.py:200`, unchanged | **Retained as RESIDUE.** Exact fix: `f"exact_cpu_decode refuses a CPU whose generator may read a region list other than the pieces after naming: {shape} "` |
| R826-2/R826-3 S3, SUGGESTION, Robustness: refuse before the generator writes the cache | `milan_soc.py`, unchanged | **Retained as SUGGESTION** |
| R826-2/R826-3 S4, SUGGESTION, Robustness: unreachable `else []` | `milan_soc.py`, unchanged | **Retained as SUGGESTION** |
| R825-S-2, SUGGESTION, Tests: no workflow runs the region-decode test at a re-pin | No workflow is changed by the delta | **Retained as SUGGESTION, mitigated** |
| R826-1 F1-F4, R826-2 F5, R825-RES-1 | Resolved in earlier rounds. Their artifacts (`milan_soc.py`, `ctrl_memory_decode.py`, `tb/verilator/ctrl_region_decode/*`) are not in the delta, and the CPU decode arm and region self-test pass at head. | **Resolved** |

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #791 acceptance (exact decode, edge fetch/load test plus single-mask mutant, all-fabric CPU). The delta touches none of its artifacts (`receipts/delta_facts.log` name-status). `receipts/region_selftest.log`: none 0/0, single-mask 4/4, cover 6/6. `receipts/test_ctrl_memory.log` CPU decode arm L113-125, all ok. Each round-4 ruling item is checked in the table above. | R826-5 | `6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c` |
| RTL | CLEAN | No `hdl/`, generator or `milan_soc.py` byte in the delta. `ctrl_memory_mutant.py` is imported only by the test (`receipts/delta_facts.log`). The CPU's generated fetch/load decode is graded at head by the `ctrl_region_decode` DECODE checks, and the shipping build has no failure (`receipts/region_selftest.log` L1-24). | R826-5 | `6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c` |
| Robustness | CLEAN | `mutated` guards (single match, single definition, the owner's namespace, `dont_inherit`) and `patched` restore-in-`finally` are verbatim-identical to `77e1efa0` (`receipts/delta_facts.log` "IDENTICAL"). The `exec` site is still refused when it is not inventoried (`receipts/gate_probes.log` P1). The CPU-decode arm's refusals all pass at head (`receipts/test_ctrl_memory.log` L113-125). | R826-5 | `6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c` |
| Tests | CLEAN (R7/R8 are RESIDUE) | `receipts/test_ctrl_memory.log`: 192 ok, 0 FAIL, 62 mutants, PASS. `receipts/py_idiom.log` rc 0 and `receipts/py_idiom_selftest.log` 54/54. Falsification probes P0/P1/P2 in `receipts/gate_probes.log`. `scripts/check_py_idiom.py:194-200`. | R826-5 | `6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c` |
| Docs | CLEAN (R7/R8 are RESIDUE) | `docs/testing/TESTING.md:786-808` checked against the run tally. `sw/litex/test_ctrl_memory.py:4-66` docstring checked against `main()`. `sw/litex/ctrl_memory_mutant.py:1-46`. `receipts/docs_check.log` and `receipts/check_doc_paths.log` rc 0. Comment-rule scan clean. | R826-5 | `6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c` |

Under the delta rule, the R826-4 Conformance, RTL and Robustness verdicts at `77e1efa0` carried forward for code the delta does not touch. This round re-covers all five lenses at the exact head.

## Real limits

- **All-fabric export and region netlists not re-measured.** I did not regenerate netlists or re-run the all-fabric compare. The claim "no byte moved" rests on dependency: no delta file is a generator input. The executor's published compare covers it; I did not verify that compare independently. The region self-test used the pinned build's cached netlist.
- **Hosted exact-head jobs mostly unfinished.** At review time, 6 checks had succeeded, including `full-ci-gate`, `changes`, `bdd-conformance` and `docs-check-no-git`. One was skipped: `Physical gPTP (nightly and manual)`, which is a skip, not an execution. About 39 were queued or in progress, including the Verilator and Yosys shards and the docs and elaborate gates (`receipts/hosted_checks.txt`). This round claims none of the unfinished ones.
- **No manager source bank at this head.** None was run or inferred here. The source-head execution evidence is the executor's published receipts plus this round's own runs, which are listed above.
- **Environment.** The gates ran in the LiteX venv that `sw/litex/sweep.sh` names (Python 3.14.9), with the pinned RV32 SDK compiler, so the link arm ran rather than skipped.
- **Not run.** The full parent, PP, gPTP, Yosys and builder banks; Docker or act; physical calibration (NOT RUN); and hardware. Field skips are not hardware proof.

## Restore

The reviewed clone is at the exact head with its tree, index and working tree all matching (`git diff-index` rc 0, `git diff` rc 0). There are no untracked or ignored leftovers: outputs this round created were removed. The six submodule gitlinks are unchanged (`receipts/restore_check.txt`). All probes ran in a disposable clone under `scratch/`.

## Pending manager duties

- Carry RESIDUE R7 and R8 (new), and R5 and R6 (retained), to the residue checklist.
- Hosted and act acceptance of the exact head (Verilator/Yosys shards, docs and elaborate gates) once they finish.
- Build and validate the current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b`) with builder and native banks at the merge turn, and link the receipts on the PR.
- Keep the merge-order dependency: #889 (S9) lands on `dev-soft-core` before this PR.
- An agent may merge only with explicit maintainer authorization.

R826-5 FINISHED
