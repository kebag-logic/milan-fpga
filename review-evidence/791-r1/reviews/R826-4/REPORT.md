[R826] NEGATIVE - exact head 77e1efa0f328f560656c049a923930509f196998

Round R826-4, external independent review of issue #791 / PR #888 (base `dev-soft-core`).
Exact head `77e1efa0f328f560656c049a923930509f196998`, tree `8ea69a1789c694cdec62197b100ceefb882e7303`.
This is a delta round over `c7e4badb..77e1efa0`. The delta is one sync merge: parent 1 is `c7e4badb` (my R826-3 POSITIVE head) and parent 2 is `a69fc0f5` (the split image, PR #889). The merge base is `1d6bf555`.

## Verdict in one paragraph

The merge is clean as a merge. Its only hand change is the conflict resolution in the `sw/litex/test_ctrl_memory.py` docstring. The ctrl-memory suite passes at the head, with all 62 mutants caught and both the mapper arm and the CPU-decode arm run. The region-decode self-test passes, with the shipping decode clean and both planted decodes killed exactly. The docstring list matches what the file grades.

The merge does break one hosted gate. Each parent leaves `test_ctrl_memory.py` at or under the Python idiom gate's 1000-line long-module limit (1000 and 996 lines). The merge puts it at 1003 lines. That makes 11 long modules against a ratchet of 10, so `scripts/check_py_idiom.py` exits 1 at this head and exits 0 at both parents. This is F1 (MAJOR, Tests), and it alone makes the verdict NEGATIVE.

There is a second, smaller finding. The merge also brings in S9's correction of `docs/testing/TESTING.md`. That changes the premise on which the earlier suggestion S5 (mutant count) was kept out of this PR. At this head the page's figure is wrong only because of #791's own twelve decode mutants, and the page does not mention #791's CPU-decode arm at all. This is F2 (MINOR, Docs). It was found when resolving S5 at this head, after my independent pass.

## Checks requested for this round

| # | Check | Result | Receipt |
|---|---|---|---|
| 1 | No hand change in the merge other than the docstring | **Yes.** `git show --remerge-diff 77e1efa0` shows exactly one file, `sw/litex/test_ctrl_memory.py`, with one conflict hunk (items 8/9) and the header line `eight` -> `nine`. Separately, `git merge-tree --write-tree c7e4badb a69fc0f5` yields auto-merge tree `3d6afc32`. Diffing that tree against published tree `8ea69a17` touches only that file (+2/-5): the conflict markers are dropped, item 8 is kept as the mapper (S9's), item 9 is added as the CPU decode (#791's), and the header is updated. The four other files both sides touched auto-merged cleanly: `docs/design/SPLIT_CONTROL_MEMORY.md`, `sw/litex/milan_soc.py`, `tb/verilator/ctrl_service_budget/README.md` and the `main()` hunk of the test file. In `milan_soc.py`, #791's hunk is in `add_ctrl_memory` (around L3235-3306 of the base) and S9's hunks are in `MilanSoC` and `main()`, with no overlap. | `remerge-diff.txt`, `merge-tree.txt`, `tree-compare.txt` |
| 2 | `test_ctrl_memory.py` passes with every mutant caught, and both the mapper arm and the CPU-decode arm run | **Yes.** Exit 0, `RESULT: PASS`, `0 failure(s)`, no `[skip]` line, and the link arm ran (RV32 compiler present). Arms run: banks, rules, simulation, link, SoC build, CPU decode (12 checks ok), register, mutants, planted ledgers, out-of-context mapper (7 ok lines, including its 3 mutants). There are 62 `MUTANT ... is caught` lines and 0 MUTANT lines that are not ok; 11 of them are graded by the decode arm. | `receipts/test_ctrl_memory.{log,rc}`, `receipts/summary.txt` |
| 3 | `tb/verilator/ctrl_region_decode/run.py --self-test` still passes | **Yes.** Exit 0. `SELF-TEST PASS none: fails 0 check(s), wants 0`; `single-mask: fails 4, wants 4`; `cover: fails 6, wants 6`; `ctrl_region_decode self-test: PASS`. Run with scoped Verilator 5.050 on PATH (identity in `receipts/env.txt`). | `receipts/region_decode_selftest.{log,rc}`, `receipts/env.txt` |
| 4 | The docstring list matches what the file grades | **Yes.** The header says nine and there are nine items (1-9). Item 8 corresponds to `run_arm(..., "out-of-context mapper", partial(ledgers.mapper_arms, ...))` in `main()` (L990-991). Item 9 corresponds to the `("decode", "CPU decode", decode.arms)` arm (L982) together with `decode.export_check` inside the SoC arm (L707). The decode mutants (`decode.MUTANTS`, L859) are owned by `ctrl_memory`/`milan_soc` through `MODULES` (L117), so item 7's wording still covers them. "Planted ledgers" is described inside item 2. | `sw/litex/test_ctrl_memory.py:4-63, 117, 707, 859, 982, 990-991` |

## Findings

### F1 - MAJOR - Tests - `sw/litex/test_ctrl_memory.py` (1003 lines) / `scripts/py_idiom.budget:7` - the sync merge makes the Python idiom gate red

- **Authority/evidence:**
  - CONTRIBUTING.md L576-583 makes the per-language idiom rules binding, and docs/development/CODE_QUALITY.md Rule 12 says "New Python complies immediately". The ratchet file `scripts/py_idiom.budget` says "EVERY NUMBER MAY ONLY GO DOWN" and sets `long module = 10`. `scripts/check_py_idiom.py:148` sets `LONG_MODULE_LINES = 1000` and L355 tests `len(lines) > LONG_MODULE_LINES`.
  - The gate is hosted: `.github/workflows/docs.yml:394-397`, step `gate_39`, "Python idiom gate". It is also in the local list at `scripts/ci_events.py:1125`.
  - Measured with each commit checked out in this clone. The submodule gitlinks are identical at all three commits.

    | commit | `test_ctrl_memory.py` lines | `check_py_idiom.py` |
    |---|---|---|
    | `c7e4badb` | 1000 | rc 0 |
    | `a69fc0f5` | 996 | rc 0 |
    | `77e1efa0` | 1003 | rc 1, `FAIL: long module 11 > ratchet 10` |

  - Neither parent alone crosses the limit. Their sum does: +1 from the docstring resolution and +2 from S9's `run_arm(... "out-of-context mapper" ...)` call, on top of #791's 1000.
- **Impact:** the hosted `docs` gates will fail at this head (`docs-gates-*` was still in progress when read), and the local code-quality gate fails. Raising the ratchet is not a remedy: the budget may only go down, and `--write-budget` refuses to raise it. The same red follows the candidate onto `dev-soft-core` once #889 lands, so the failure is the stack's and not only this head's.
- **Required outcome:** `python3 scripts/check_py_idiom.py` exits 0 at the PR head with `scripts/py_idiom.budget` unchanged or lowered. In practice that means `test_ctrl_memory.py` is at most 1000 lines, or the excess moves to a module that stays under the limit. It must happen without dropping any arm, mutant or docstring item graded today.
- **Verification:** at the fixed head, run `python3 scripts/check_py_idiom.py` (rc 0) and `python3 scripts/check_py_idiom.py --selftest` (rc 0). Also run `test_ctrl_memory.py` (`RESULT: PASS`, still 62 caught mutants, CPU-decode and mapper arms both run, docstring count equal to its item count) and `tb/verilator/ctrl_region_decode/run.py --self-test` (PASS).
- **Lens attribution:** Tests, because it is a red regression gate and the file is the test harness. I considered Conformance and Docs and did not attribute them. No issue #791 acceptance criterion names the gate, and the docstring itself is accurate (check 4). This is not RESIDUE: it changes a gate verdict.

### F2 - MINOR - Docs - `docs/testing/TESTING.md:792` - the test page's `test_ctrl_memory` mutant figure and arm list leave out #791's CPU-decode arm and its twelve mutants

- **Authority/evidence:**
  - AGENTS.md section 6, Docs lens: "Changed contracts are reflected in authoritative docs."
  - The figure at each commit, from `git show <c>:docs/testing/TESTING.md`:

    | commit | figure |
    |---|---|
    | `1d6bf555` | forty-four |
    | `c7e4badb` | forty-four |
    | `a69fc0f5` | forty-seven, plus "Three more mutants" for the mapper (S9's correction) |
    | `77e1efa0` | forty-seven, plus the three mapper mutants |

  - At this head, importing the module with the LiteX interpreter gives `len(test_ctrl_memory.MUTANTS) == 59`, of which `len(ctrl_memory_decode.MUTANTS) == 12`.
  - The run grades 62 `MUTANT` lines: 59 plus the 3 mapper mutants.
  - `grep -n "ctrl_memory_decode\|CPU decode\|decode arm\|ctrl_region_decode\|#791" docs/testing/TESTING.md` finds nothing.
- **Why it is in scope now:** in R826-3, S5 stayed a SUGGESTION and an issue candidate for two reasons: the figure was already wrong at the source base, and this PR did not touch the page. The merge removes the first reason. At the candidate head the figure is correct for everything except this PR's own additions, so the documentation drift is now this lane's. This is the delta changing what a prior verdict depended on.
- **Why MINOR and not RESIDUE:** it is a wrong figure in an authoritative page, and the owner rule excludes figures from RESIDUE.
- **Impact:** the test page understates the suite by twelve mutants and does not tell a reader that `test_ctrl_memory.py` grades the CPU's region decode (#791). A cold reviewer reading the page cannot learn from it that the decode guard is graded there.
- **Required outcome:** `TESTING.md`'s description of `test_ctrl_memory.py` states a mutant count that equals what the file grades (or derives it so it cannot drift) and names the CPU-decode arm. One sentence pointing at `ctrl_memory_decode.py` is enough. Make no change to S9's mapper sentence other than what the count requires.
- **Verification:** read the figure on the page and compare it with `len(test_ctrl_memory.MUTANTS)` and the run's `MUTANT` line count at the fixed head. Confirm the docs gates (`docs-gates-*`) are green at that head.

### S1 - SUGGESTION - Docs - `sw/litex/test_ctrl_memory.py:60-61` - items 8 and 9 are single unwrapped lines (90 and 110 characters)

Items 1-7 wrap at about 79 columns. Items 8 and 9 do not. This is within the gate (`over-long line: 0`), so it is not a finding. Do not wrap them as part of F1's fix: wrapping adds lines, which is the opposite of what F1 needs.

### Comment-rule residue check

The only hand-written text in the delta is the two docstring lines and the header count. They name issue #791 and module and function identifiers only, with no lane label, round, reviewer ID or comment ID. No RESIDUE.

## Other gates spot-checked at this head (all green)

These ratchet gates sum counts across both lines of work, so they were checked for the same hazard as F1.

| gate | rc | last line |
|---|---|---|
| `check_sv_idiom.py` | 0 | `SystemVerilog idiom gate: OK (144 first-party HDL file(s) ...)` |
| `check_cpp_idiom.py` | 0 | `build without warnings: 0 <= 0` |
| `check_sh_idiom.py` | 0 | `top-heavy long script: 0 <= 0` |
| `check_hygiene.py --check` | 0 | `HYGIENE RATCHET: PASS (3 population(s), 1381 file(s))` |
| `check_py_idiom.py --selftest` | 0 | `54 checks: 54 PASS, 0 FAIL` |

Receipts: `receipts/gate-*.{log,rc}`.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #791 acceptance (exact decode; edge fetch/load test plus single-mask mutant; all-fabric CPU byte-identical). Remerge-diff and the auto-merge-tree comparison show no hand change to any #791 artifact. `sw/litex/ctrl_memory_decode.py` and `tb/verilator/ctrl_region_decode/*` are byte-identical to `c7e4badb`. Region-decode self-test at head: shipping clean, single-mask and cover killed. | R826-4 | `77e1efa0` |
| RTL | CLEAN | `hdl/` at head is byte-identical to `a69fc0f5` (S9's mailbox HDL, not in this lane's scope), and the #791 lane changes no HDL. The CPU's generated decode is graded at head by the `ctrl_region_decode` DECODE checks (netlist fetch/load decode over 131072 representatives) and passes for the shipping build. Generator identity: bench `vexiiriscv/core.py` equals the pinned LiteX `a1e1c365` plus repository patch `sw/litex/patches/0004` (`receipts/litex-core-identity.txt`). | R826-4 | `77e1efa0` |
| Robustness | CLEAN | `test_ctrl_memory.py` CPU-decode arm at head: refusals of a CPU that never names its netlist, of rows re-collected, kept, renamed, mutated in place or appended after naming, and of non-aligned lists; non-VexiiRiscv pass-through. Region-decode past-the-end fetch/load faults and no-bus-command checks (shipping PASS). The merge changes none of these artifacts. | R826-4 | `77e1efa0` |
| Tests | **UNCLEAN** (F1 open) | `receipts/test_ctrl_memory.log` (PASS, 62 mutants caught; counts in `receipts/testing-md-count.txt`, all arms including mapper and CPU decode run); `receipts/region_decode_selftest.log` (PASS); `receipts/py_idiom-per-commit.txt` (head red, parents green) | R826-4 | `77e1efa0` |
| Docs | **UNCLEAN** (F2 open) | `sw/litex/test_ctrl_memory.py:4-63` docstring against `main()` L975-991, `mutant_arms` L923 and `MODULES` L117 (clean); `docs/design/SPLIT_CONTROL_MEMORY.md` auto-merged (the register arm, which reads section 3 against `ctrl_memory.RULES`, passes at head; clean); `docs/testing/TESTING.md:786-802` (F2); S1 is a suggestion only | R826-4 | `77e1efa0` |

The R826-3 lens verdicts at `c7e4badb` carry forward for code the delta does not touch, per the delta rule. This round re-covers all five at `77e1efa0` on the artifacts above.

## Prior public review findings, resolved or retained at this head

(Read only after the verdict and ledger above were written.)

All BLOCKER, MAJOR and MINOR findings from earlier rounds were resolved by R826-3 at `c7e4badb`: R826-1 F1 and R826-2 F5, the latter fixed at its cause. Their artifacts are byte-unchanged by this merge. `sw/litex/ctrl_memory_decode.py` and `tb/verilator/ctrl_region_decode/*` are identical to `c7e4badb`. The `exact_cpu_decode` hunk of `milan_soc.py` is unchanged and only shifted +28 lines by S9's insertions, and the CPU-decode arm passes at head. They stay **Resolved**.

These items were open at `c7e4badb`:

| prior item | state at `77e1efa0` | disposition |
|---|---|---|
| R826-2/R826-3 R5, RESIDUE Docs: "instead of building a decode other than the pieces" | Present verbatim at `docs/design/SPLIT_CONTROL_MEMORY.md:55` and `sw/litex/milan_soc.py:3278-3279`, shifted from `:3250-3251` | **Retained as RESIDUE.** Exact fix as published in R826-3, at the new line numbers. |
| R826-3 R6, RESIDUE Tests/Docs: check label "may read the whole rows after naming" | Present at `sw/litex/ctrl_memory_decode.py:200`, unchanged | **Retained as RESIDUE.** Exact fix: `f"exact_cpu_decode refuses a CPU whose generator may read a region list other than the pieces after naming: {shape} "`. |
| R826-2/R826-3 S3, SUGGESTION Robustness: refuse before the generator writes the cache | `milan_soc.py:3302-3315`, shifted from `:3274-3286`, unchanged | **Retained as SUGGESTION.** |
| R826-2/R826-3 S4, SUGGESTION Robustness: unreachable `else []` | `milan_soc.py:3308`, shifted from `:3280`, unchanged | **Retained as SUGGESTION.** |
| R826-3 S5, SUGGESTION (issue candidate) Docs: stale mutant count in `TESTING.md` | The merge brought S9's correction to "forty-seven" plus three mapper mutants. The remaining gap is exactly #791's 12 decode mutants, and the arm is unnamed on the page. | **Superseded by F2 (MINOR, Docs).** The delta removed the "already wrong at base" premise. |
| R825-S-2, SUGGESTION Tests: no workflow runs the region-decode test at a re-pin | Unchanged, and no workflow is added by the delta. The re-pin procedure still names it. | **Retained as SUGGESTION, mitigated.** |
| R825-RES-1, R826-1 F2/F3/F4 | Resolved in earlier rounds; the artifacts are unchanged by the delta | **Resolved** |

## Real limits

- **Interpreter.** The suites ran on the bench LiteX venv (`~/litex-milan/venv`, Python 3.14.9), not on a fresh hosted install. Its `litex` checkout is at the pinned `a1e1c365`, and its `vexiiriscv/core.py` is byte-identical to the pin plus repository patch 0004. I did not verify the other bench edits (`bios/main.c`, the untracked `bios/xz/`, `liteeth/phy/gmii.py`, and the pythondata-vexiiriscv `verilog/ext/` tree) against patches 0002/0005-0007 byte for byte. See `receipts/litex-env.txt`.
- **No author receipt at this head.** No author or manager source receipt exists at `77e1efa0`; the published `review-evidence/791-r1` receipts cover earlier heads. The source-head execution evidence for this round is this packet's own runs.
- **Byte-identical all-fabric CPU not re-measured.** I did not re-measure the all-fabric CPU's byte-identity at this head. The delta adds only S9's own content, and the #791 hunks are unchanged since R826-3.
- **Hosted checks not judged.** At read time, hosted check runs at this head were mostly in progress. Executed and completed successfully: `bdd-conformance`, `changes`, `docs-check-no-git`, `wire-accountability`. I made no judgment of hosted or act acceptance.
- **Not run.** No physical calibration, hardware, Vivado, builder bank or full parent/PP/gPTP/Yosys bank was run.

## Pending manager duties

- Carry F1 and F2 to the lane. They can share one commit, since both are in the test file and its page. After they are fixed, re-review re-covers Tests (F1) and Docs (F2) on the fixing commit. Carry RESIDUE R5 and R6 to the residue checklist.
- At the merge turn, build and validate the current-dev merge candidate (builder and native banks), with source base `1d6bf555` and live dev `fa6c094b`, and link the receipts. Hosted `docs-gates-*` (`gate_39`) at the fixed head must be green.
- Maintain the merge-order dependency: #889 (S9) lands on `dev-soft-core` before this PR.

## Packet

`probe.sh` reproduces checks 1-3 and the per-commit idiom-gate measurement. Its arguments are the clone, an output dir, a migen+litex interpreter and a Verilator 5.050 directory. Every receipt is listed in `MANIFEST.sha256`. After the probes, the clone was restored and verified: HEAD and `write-tree` match `8ea69a17`, the index equals the HEAD tree in modes and blobs, all tracked files rehash with 0 mismatches, and the submodule gitlinks are unchanged (`receipts/restore-check.txt`).

R826-4 FINISHED
