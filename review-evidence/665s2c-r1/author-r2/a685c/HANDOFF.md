# [A685c] #665 lane S2c, round 2: answering R713-1 and R714-1 (HANDOFF)

Status: **REVIEW READY**, 2026-10-27.

- Branch `665-s2c-icache`, local, not pushed. Head **`de91db59d10d4e9e3de607f068ace7680f293fd7`**. That is six commits on the round-1 head `a611785f2afe5bbe587f74034d869e869a1c8d37` (PR #796, base `dev-soft-core`, on S2's final `f58d049b`, PR #792).
  - Commits: one-line subjects, no body, no trailers (`receipts/scope/commits_and_scope.txt`).
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified). Lane base `origin/dev-soft-core` `e76a755a` is an ancestor of the head (verified). `origin/dev-soft-core` is now `9220f9b3`, and the PR targets `dev-soft-core`.
  - S2's remote branch is still `f58d049b` (`git ls-remote` at the round's start and again before REVIEW READY, `receipts/scope/commits_and_scope.txt`), so there was no re-base this round.
- No git command ran inside a submodule of the checkout. The one `rev-parse --show-toplevel` on protocol-processor was the verification the brief requires, and its origin is the processor repository. No submodule pointer changed.
- Assignment: issuecomment-6433542516. TAKEN: issuecomment-6433696951 (`TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6434846736 (`REVIEW-READY-COMMENT.md`). The PR body for the manager is `PR-BODY.md`.
- Nothing pushed. No PR, issue or comment edit. No bench, no hardware, no flashing, no Vivado and no sweep: the round adds no measurement, as the assignment scopes it.

## Contents

1. Result
2. Acceptance (this round's items)
3. Changes, file:line and reason
4. Checks, planted mutants and failing words
5. Gate table
6. Run history and reproducibility
7. Findings, decisions and open questions

## 1. Result

**Every round-2 item is met at `de91db59`. No measured cycle count changed, and no figure other than the derived rate F2 names.**

| Finding | Result | Receipt |
|---|---|---|
| R713-1-F1 | The six unbounded rows carry "at least X, **never answered**" or "at least X, **never released**" in both ms columns, and their cycles cells are marked the same way. All 47 rows of the two miss tables match the archived regrades of P1-none, P1-64x1, P8-none and P8-64x1, with 0 mismatches. | `receipts/docs/miss_cells.txt` |
| R713-1-F2, R714-1-F2 | The stated rate is "one tile for each 4 KiB of data and half a tile of tags for each way". All 8 rows of the README's Vivado table satisfy it. | `receipts/docs/tile_rate.txt` |
| R713-1-F3 | Every S2 reproduction command on the page selects `--fetch-l1 none`, or the page states what the default gives. The documented cacheless `slow-adp-rx` control, rerun at the round's content, measures **24.614 ms** (`CONTROL slow-adp-rx caught`, rc 0), the figure printed beside it. The documented fixture regeneration reproduces the committed `fixture.log` and `oracle.json` **byte for byte**. | `receipts/reruns/` |
| R713-1-F4 | Two checks drive `run.main()`. Both reviewer source mutants are killed, as is a third (`main builds with the default cache`), and each new mutant is caught. | `receipts/probes/source_mutants.txt`, `r713_harness_probes.txt` |
| R714-1-F1 | The option test requires the literal `--xlen=32 --fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1` and kills three geometry controls. R714-1's probe at the head: control rc 0; sets128, ways2 and sets32 rc 1. | `receipts/probes/soc_geometry/` |
| Residue | RES1/RS1, RES2, RS2, RS3 and RS4 applied. No lane or review label remains on any source line added since S2. The same scan finds the four round-1 lines at `a611785f`. | `receipts/scope/comment_rule_scan.txt` |

## 2. Acceptance (issuecomment-6433542516)

| Item | Status | Evidence |
|---|---|---|
| 1. R713-1-F1: every unbounded row carries S2's lower-bound label, not a measured ceiling miss | met | Section 1; README `:664-666`, `:676`, `:681-682`, `:708`, `:718-719` |
| 2. R713-1-F2 / R714-1-F2: the block-RAM rate at the measured cost | met | README `:769` |
| 3. R713-1-F3: S2's control and fixture commands reproduce the figures beside them | met: commands fixed (not relabelled), and both reproduction claims rerun | README `:48-49`, `:75-76`, `:185-194`, `:796-797`, `:911-919`, `:921-930`; `receipts/reruns/` |
| 4. R713-1-F4: the reuse check exercises its refusal, and a mutant removing it is caught | met | `selftest.py:764-860`; `selftest_mutants.py:333-353`, `:462-466`; section 4 |
| 5. R714-1-F1: the split-cache option test pins 4 KiB, 64 sets, 1 way, no data cache, and a changing mutant is caught | met | `test_soc_options.py:22-26`, `:226-235`, `:247-249` |
| 6. Residue: RES1, RES2, R713-1's RS1 to RS4, as written | met. RES1 and RS1 differ at `build.py:149`; RES1's text is applied (section 7) | section 3 |
| Gates: self-test and mutants, `test_soc_options.py`, the bare-metal scope gate, the docs gates, `cd tests && behave` | met: 0 of 97 gates nonzero, behave 406 of 406 scenarios | section 5 |

The lane's acceptance from issuecomment-6421463860 stands as [A685] and [A685b] recorded it. The PR stays "Relates to #665": T_svc is not closed, and NFR-SCOUT-01 awaits the owner.

## 3. Changes, file:line and reason

Line numbers are at `de91db59`; `selftest.py` from `:779` on is one line later than at `619e84e6`.

| Commit | File:line | What | Reason |
|---|---|---|---|
| `706603ee` | `tb/verilator/ctrl_service_budget/README.md:664-666` | A note above the miss tables: a never-answered or never-released row gives the time waited by the run's end, at least, and does not measure what the cache saves | R713-1-F1 |
| `706603ee` | `README.md:676`, `:681-682`, `:708`, `:718-719` | The six unbounded rows read "at least X, **never answered**" / "never released" in both ms columns and the cycles column | R713-1-F1; S2's labels at `README.md:186`, `:395`, `:420-421` |
| `706603ee` | `README.md:769` | "one tile for each 4 KiB of data and half a tile of tags for each way" | R713-1-F2, R714-1-F2: the table beside it |
| `a75220ac` | `README.md:48-49` | The default commands give the split cache's arms; S2's Results add `--fetch-l1 none` | R713-1-F3 (the Results reproduction block) |
| `a75220ac` | `README.md:75-76` | Arms B and S build the split cache as written, and S2's arms with `--fetch-l1 none` | R713-1-F3 |
| `a75220ac` | `README.md:185-194` | Results gives its own cacheless commands at both points | R713-1-F3 |
| `a75220ac` | `README.md:796-797` | The cache section's controls name their command: the cacheless commands with `--fetch-l1 64x1` | R713-1-F3: each command beside its figure |
| `a75220ac` | `README.md:911-919` | The fixture regeneration gives the run that records it, on the cacheless core, then the generator | R713-1-F3: the fixture and oracle were recorded cacheless |
| `a75220ac` | `README.md:921-930` | The three controls select `--fetch-l1 none`, the core whose figures (24.614, 24.903 ms) the text gives | R713-1-F3 |
| `a75220ac` | `selftest.py:26-27` | The docstring's regeneration names the cacheless core | R713-1-F3 |
| `d50b799d` | `selftest.py:764-773` | `Reached` (a sentinel raised once `run.main` begins to set up its groups) and `write` | R713-1-F4 |
| `d50b799d`, `de91db59` | `selftest.py:775-792` | `main_verdict`: `run.main()` with its argv, its stdout and stderr captured, the environment restored, and `scenario.point` replaced by the sentinel | R713-1-F4: drive the refusal path itself |
| `d50b799d` | `selftest.py:795-822` | `built`: `run.main()` building on temporary files, with `build.firmware`, `xip_image`, `symbols`, `verilate` and the `split_soc` export replaced by placeholder writers and a recorder of the selection. The run's selection, the mailbox contract, the input digests and `build.json` are the real code's. | R713-1-F4: what `build()` records for `fetch_l1` and `xip` |
| `d50b799d` | `selftest.py:825-860` | `cache_build_checks`: two builds (`64x1` XIP, cacheless), then eight reuse cases through `run.main --reuse-build`, including a build whose `build.json` records neither key | R713-1-F4 |
| `d50b799d` | `selftest.py:751-756` at `a611785f` (removed) | The earlier check, which compared `built_as()` with `selected()` on dictionaries | Superseded. Its three cases are among the eight, through `run.main` |
| `d50b799d` | `selftest.py:18-21`, `:728-731`, `:757`, `:863` | Docstrings; the XIP check named "the flash driver"; `checks()` runs the new checks last | R713-1-F4; R713-1 RS1's optional rename |
| `d50b799d` | `selftest_mutants.py:333-353`, `:462-466`, `:469` | `_build_recorded`, `_build_with`; three mutants; the XIP driver mutant named "the flash driver" | R713-1-F4: "each part has a mutant"; RS1's optional rename |
| `d50b799d` | `README.md:829-831`, `:901-906`, `:957` | The check list, the mutant table (70 rows) and a limit: the self-test stands a recorder in for the SoC export | Docs for R713-1-F4 |
| `2d9671ac` | `sw/builder/test_soc_options.py:22-26` | `SPLIT_FETCH_L1`, the documented options restated in the test | R714-1-F1: not read back from the module under test |
| `2d9671ac` | `test_soc_options.py:234-235` | Both the constructor's `vexii_args` and `ctrl_cpu_args(CTRL_FETCH_L1)` must equal it exactly | R714-1-F1, R713-1-S1 |
| `2d9671ac` | `test_soc_options.py:247-249`, `:256-257` | Three killed controls (128 sets, two ways, 32 sets); the summary line names the geometry | R714-1-F1: a planted geometry change is caught |
| `2d9671ac` | `test_soc_options.py:6-8`, imports | Docstring; the `re` import round 1 added for the pattern, now unused, is removed | Tidiness of the touched test |
| `619e84e6` | `tb/verilator/ctrl_service_budget/build.py:149-155` | "(#665, decision D3)" and "the saved-state flash driver (nvm_flash_litespi.c)", rewrapped | R714-1 RES1, R713-1 RS1 |
| `619e84e6` | `README.md:741`, `:745` | "on a CPU of 13 tiles"; "a CPU of 13 tiles against 6" | R713-1 RS4 |
| `619e84e6` | `README.md:746` | "So the T_svc service paths stay in block RAM behind the split's cache, or behind one eight times its size, as D3 rules." | R714-1 RES2 |
| `619e84e6` | `docs/design/MARK_II_AREA_PLAN.md:897-898` | "All four leave ..." and "None of these numbers proves ..." | R713-1 RS2 |
| `de91db59` | `selftest.py:779` | A docstring on `main_verdict`'s sentinel `reached` | The Python idiom gate's rule 12 (no undocumented public function), which the first gate run at `619e84e6` failed (section 6) |
| (PR body) | `PR-BODY.md` | Status sentence (RS3), the XIP bullet (RES2), "a CPU of 13 tiles" (RS4), the round-2 table, the tallies and the expected outputs | R713-1 RS3, RS4; R714-1 RES2 |

Nothing under `sw/litex`, `sw/firmware`, `sw/mailbox`, `configs` or `hdl` changed, and no submodule pointer moved (`receipts/scope/commits_and_scope.txt`). So round 1's all-fabric export digest, Yosys and out-of-context pricing, PMA comparison and sweep still describe the head's build inputs. Only comments changed in `build.py`.

## 4. Checks, planted mutants and failing words

Self-test at the head: `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` prints 93 `PASS`, 70 `MUTANT caught` and `self-test: 0 failures`, rc 0. Round 1 had 92 and 67; this round removes 1 check, adds 2 and adds 3 mutants. `scripts/mutant_table_check.py` (S2's) matches all 70 README rows to the output (`receipts/docs/mutant_table.txt`).

New checks:

| Check (as printed) | Planted mutant (`selftest_mutants.py`) | Failing words |
|---|---|---|
| `the run builds and records the fetch L1 and the arm it selected` | `build: an XIP build records the block-RAM arm` (`build.build`'s record edited to `xip=False`, on disk and returned) | `MUTANT caught: build: an XIP build records the block-RAM arm: the run builds and records the fetch L1 and the arm it selected ({'xip': ('reached', ('64x1', False)), 'plain': ('reached', ('none', False))})` |
| (same) | `build: the CPU is built with the split's cache whatever the selection` (`build.build` handed `Core(fetch_l1='split')`) | `MUTANT caught: build: the CPU is built with the split's cache whatever the selection: the run builds and records the fetch L1 and the arm it selected ({'xip': ('reached', ('split', True)), 'plain': ('reached', ('split', False))})` |
| `the run refuses a reused build of another fetch L1 or arm and reuses the selected one; a build with no fetch L1 is cacheless` | `reuse: a reused build is not compared with the selection` (`built_as` and `selected` both `()`: R713-1's "condition replaced with False" as a patch) | `MUTANT caught: reuse: a reused build is not compared with the selection: the run refuses ... (xip --xip: reached; xip --fetch-l1 64x1: reached; plain (split): reached; plain --fetch-l1 none --xip: reached; no fetch L1 recorded (split): reached)` |
| (same) | `reuse: the fetch L1 and the arm are not compared` (round 1's mutant, now caught here) | the same check, with the same five cases reached |

The reuse check's eight cases:

| Build | Run's selection | Must |
|---|---|---|
| `64x1`, XIP | `--fetch-l1 64x1 --xip` | reach group setup |
| `64x1`, XIP | `--xip` (split) | be refused with `exit 2: run.py: error: the reused build is another point, CPU region set, mutation, variant, fetch L1 or arm` |
| `64x1`, XIP | `--fetch-l1 64x1` | be refused (another arm) |
| cacheless | `--fetch-l1 none` | reach group setup |
| cacheless | (split) | be refused |
| cacheless | `--fetch-l1 none --xip` | be refused |
| records neither key | `--fetch-l1 none` | reach group setup (an S2 build is cacheless) |
| records neither key | (split) | be refused |

Reviewer source mutants replayed on a copy of the head `de91db59` (`receipts/probes/copy_equals_head.txt`: 0 of 1,457 tracked files differ):

| Mutant | Result | Failing words |
|---|---|---|
| `run.py:317` condition replaced with `False` (R713-1-F4) | KILLED, rc 1 | `FAIL: the run refuses a reused build of another fetch L1 or arm and reuses the selected one; a build with no fetch L1 is cacheless: xip --xip: reached; xip --fetch-l1 64x1: reached; plain (split): reached; ...` |
| `build.py:520` `spec['xip'] = False` (R713-1-F4) | KILLED, rc 1 | `FAIL: the run builds and records the fetch L1 and the arm it selected: {'xip': ('reached', ('64x1', False)), ...}` |
| `run.py:321` builds `'split'` whatever `--fetch-l1` (R713-1's probe list) | KILLED, rc 1 | `FAIL: the run builds and records the fetch L1 and the arm it selected: {'xip': ('reached', ('split', True)), 'plain': ('reached', ('split', False))}` |
| R713-1's other five probes (flash image hand-off, `split_soc` geometry, non-power-of-two sets, the native model's refill end and code marks) | SURVIVED, as at round 1 | Outside this round's items (section 7) |

`sw/builder/test_soc_options.py` prints `Split placement CPU: the 4 KiB direct-mapped instruction cache on the split CPU only, 6 killed controls`:

| Planted control (source mutation of `milan_soc.py`) | Failing words |
|---|---|
| the split CPU without its cache (round 1) | `killed: the split CPU without its cache` |
| the all-fabric CPU with the cache (round 1) | `killed: the all-fabric CPU with the cache` |
| a data cache with it (round 1) | `killed: a data cache with it` |
| `CTRL_FETCH_L1 = (128, 1)` | `killed: a larger cache` |
| `CTRL_FETCH_L1 = (64, 2)` | `killed: a second way` |
| `CTRL_FETCH_L1 = (32, 1)` | `killed: a smaller cache` |

R714-1's own probe (`scripts/r714_probe_soc_geometry.sh`, run unchanged against a full copy of `619e84e6` with its git metadata; only `selftest.py` changed since, which the option test does not read): `control rc=0`, `sets128 rc=1`, `ways2 rc=1`, `sets32 rc=1`. Each failing probe ends `AssertionError: {'kind': 'setup', 'vexii_args': '--xlen=32 --fetch-l1 --fetch-l1-sets=128 --fetch-l1-ways=1', ...}` (`receipts/probes/soc_geometry/`).

## 5. Gate table

Every gate ran at the head `de91db59d10d4e9e3de607f068ace7680f293fd7` (`receipts/gates/HEAD.txt`).

- The runner is `scripts/gates_s2c.py`, round 1's runner unchanged: S2's round-5 runner with `test_soc_options.py` added.
- It ran the gates one at a time, each to its own log, unpiped. It refused a dirty tree before starting and checked `git status --porcelain --untracked-files=all --ignore-submodules=none` after every gate.
- Logs are in `receipts/gates/`, each with its rc and the tree's state on its last lines. `summary.md` is the runner's table with seconds, and `serial.out` its console.
- Two logs exceed 200 KB and are kept out of the packet by digest: `bdd_conformance.log` and `ci_events_selftest.log` (`<log>.digest.txt`).
- Inherited from S2's runner, as in round 1: `measure_fail_fast.py --selftest` and `ci_fail_fast_selftest.py` share the log name `fail_fast_selftest.log`, so only the second log is kept. Both rows of `summary.md` are rc 0.
- Environments are round 1's:
  - the pinned Markdown renderer's hash-locked environment (`tools/markdown/requirements.txt`, sha256 prefix `40cdefe08ebd`);
  - `tools/hdl_reference/requirements.txt`;
  - the product LiteX environment with the pinned RV32 SDK first on `PATH`, for the option test and the builder.

**0 of 97 gates nonzero or left the tree dirty** (`summary.md`). The first full run, at `619e84e6`, failed `py_idiom` (section 6); this is the run after the fix, from the start.

| Gate (`receipts/gates/<gate>.log`) | Command | Result |
|---|---|---|
| `harness_selftest` | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | rc 0: 93 `PASS`, 70 `MUTANT caught`, 0 escaped, `self-test: 0 failures` |
| `soc_options` | `python3 sw/builder/test_soc_options.py` | rc 0: 52 constructor and 18 CLI cases, 9 killed controls; `Split placement CPU: the 4 KiB direct-mapped instruction cache on the split CPU only, 6 killed controls`; `RESULT: PASS` |
| `baremetal_check`, `baremetal_selftest` | `python3 scripts/check_baremetal_only.py --check`, `--selftest` | rc 0: `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))` |
| The docs workflow's check-mode commands: 87 gates, `wire_accountability_selftest` to `ci_events_selftest` in `summary.md` | as listed in `scripts/gates_s2c.py` | rc 0 each. `check_em_dash: 0 finding(s) over 1004 added line(s) in 3 changed Markdown page(s) ... [e76a755a..HEAD]`; `docs_check: 0 finding(s) across 211 md files + 1433 scrubbed text files`; `TOC gate: OK`; `anchor check: 552 existing cross-page fragment links reproduced`; `doc path gate: OK (1062 cited paths all resolve ...)`; `documentation style: OK`; `HYGIENE RATCHET: PASS`; `py idiom`: `undocumented public function: 0 <= 0`, `over-long line: 0 <= 0` |
| `firmware_compiler_absent` | `python3 sw/builder/test_firmware_compiler.py --absent --audit <scratch>/rv32-absent.jsonl` | rc 0. Its compiled census is a registered NOT RUN in this mode by design, as in round 1 |
| `git_diff_check` | `git diff --check e76a755a HEAD` | rc 0 |
| `bdd_conformance` (rtl-fast) | `cd tests && behave` | rc 0: 14 features, 406 scenarios, 1977 steps passed |
| `hdl_reference_selftest`, `hdl_reference` | `python3 scripts/gen_hdl_reference.py --selftest`, `--output <scratch>` | rc 0 |
| `builder_require_rv32` | `python3 sw/builder/test_builder.py --require-rv32` | rc 0: `ALL GATES PASS EXCEPT 1 NOT RUN`, 1,376 s. Gate 11 needs a local Arty build report (`real report not on disk ... the calibration gate needs the mf48 build tree`), as in rounds 1 and S2 |

Outside the runner:

| Check | Command | Head | Result |
|---|---|---|---|
| R713-1-F1 cells | `scripts/check_miss_cells.py README <round-1 regrade arms>` | `de91db59` | rc 0: 47 rows, 0 mismatches (`receipts/docs/miss_cells.txt`) |
| R713-1-F2 / R714-1-F2 rate | `scripts/check_tile_rate.py README` | `de91db59` | rc 0: 8 rows, 0 mismatches (`receipts/docs/tile_rate.txt`) |
| README mutant table | `scripts/mutant_table_check.py` (S2's) on `harness_selftest.log` | `de91db59` | rc 0: 70 rows, 0 mismatches (`receipts/docs/mutant_table.txt`) |
| R713-1-F3 control | `run.py --point 1x1 --build-dir <scratch>/budget-slow-adp --fetch-l1 none --mutation slow-adp-rx` | final content, before the commits (section 6) | rc 0: `BUDGET control.discover.if0: 24.614 ms over T_svc 10 ms`, `CONTROL slow-adp-rx caught`, 164 s (`receipts/reruns/C1-slow-none.log`) |
| R713-1-F3 fixture | `run.py --point 1x1 --build-dir <scratch>/budget-fixture --fetch-l1 none --groups fixture --record-budget-findings`, then `selftest.py --write-fixture <its log> <its build.json>` | `619e84e6` | rc 0, rc 0; `git status` empty afterwards (`receipts/reruns/fixture_identity.txt`) |
| R713-1-F4 source mutants | `scripts/source_mutants.py <copy>`; R713-1's `harness_probes.py <copy>` | `de91db59` copy | 3 of 3 killed; R713-1's 8 probes: 3 killed, 5 survive as at round 1 (`receipts/probes/`) |
| R714-1-F1 probe | `scripts/r714_probe_soc_geometry.sh <full copy> <out>` (R714-1's, unchanged) | `619e84e6` copy (only `selftest.py` changed since) | `control rc=0`, `sets128 rc=1`, `ways2 rc=1`, `sets32 rc=1` (`receipts/probes/soc_geometry/`) |
| Comment rule | widened lane-name scan of every source line added since `f58d049b` | `de91db59` | none; the same scan finds round 1's four lines at `a611785f` (`receipts/scope/comment_rule_scan.txt`) |
| Scope | `git diff --stat a611785f..HEAD`; product, firmware, mailbox, config and HDL paths | `de91db59` | 6 files, none under `sw/litex`, `sw/firmware`, `sw/mailbox`, `configs` or `hdl`; no submodule pointer (`receipts/scope/commits_and_scope.txt`) |

Not re-run, as the assignment scopes it (no new measurement). Nothing they read changed since round 1: no Vivado or Yosys pricing, no all-fabric export digest, no PMA comparison, no four-shard sweep and no arm regrade.

## 6. Run history and reproducibility

- **No measurement.** The two reruns reproduce figures already on the page. They change no figure and are not new arms.
  - The cacheless `slow-adp-rx` control is the README's command with only `--build-dir` changed. It was run with the final content of every file a run reads, before the commits were made, and every file it reads is unchanged at the head.
  - The fixture run is the README's run, at `619e84e6`, followed by its generator command. Nothing a run or the generator reads changed after it. The generator rewrote `fixture.log` and `oracle.json` in place, and `git status` was then empty.
- **The commit split, and one slip.** The round's edits were committed in five logical steps by `scripts/stage_hunks.py`, which writes each file as the base plus chosen zero-context hunks.
  - Its first version read `HEAD`, which moves after the first commit. So the second, third and fifth steps were refused or left incomplete, and three local commits were wrong (`76251a69`, `26d38c13`, `7e31513c`).
  - The branch was moved back to the round-1 head with `git reset --mixed a611785f` on the local branch only. These were this session's unpushed commits. The final files, saved beforehand, were restored and checked with `cmp`.
  - The stager was fixed to read a fixed base, and the five commits were made again. Every changed file at `619e84e6` is byte-identical to the saved final files, and the tree was clean.
- **The first gate run failed one gate.** At `619e84e6`, `py_idiom` returned rc 1: `FAIL: undocumented public function 1 > ratchet 0`. The cause was the nested sentinel `reached` in the new `main_verdict`, which had no docstring.
  - That run's other 95 gates were rc 0 with the tree clean. Its log and console are kept in `receipts/gates-first-run-619e84e6/`.
  - It was stopped by PID during its last gate, the builder bank. The tree was clean after the stop.
  - `de91db59` adds the docstring. The full gate set then ran again from the start at `de91db59` (section 5), and the probes were replayed there.
- **Copies for probes.** The reviewer probes ran on scratch copies, never in the checkout, so they could run beside the gate runner. One copy omits `.git` and is verified blob for blob against the head. The other is a full copy with git metadata, needed because `milan_soc` lists protocol-processor's files with git, and `git status` shows it clean at `619e84e6`. The first copy was refreshed to `de91db59` from the head's objects and verified again.
- **Receipts.** Host paths in logs are replaced by `<checkout>`, `<scratch>`, `<tools>` and `$HOME` (`scripts/sanitize.py`, then `scripts/make_index.py`, round 1's). The raw copies of the 8 files scrubbed by the index are kept in scratch, and their raw sha256 is in `receipts/INDEX.md`, which lists every receipt present with its size and sha256.
- **Reviewer scripts, reused unchanged.** `scripts/r713_harness_probes.py` is R713-1's `harness_probes.py` and `scripts/r714_probe_soc_geometry.sh` is R714-1's `probe_soc_geometry.sh`, both copied from the reviewers' packets. `gates_s2c.py`, `mutant_table_check.py`, `make_index.py` and `env.sh` are round 1's.

## 7. Findings, decisions and open questions

1. **Two residue texts for one line.** R714-1 RES1 gives "(#665, decision D3)" for `build.py:149`, and R713-1 RS1 gives "(#665, the hybrid-XIP decision)". Both remove the lane name. RES1's is applied: it keeps the decision ID that line 153 also cites ("as D3 requires"). The difference is stated in TAKEN, here, in the PR body and in REVIEW READY. The reviewer may prefer RS1's.
2. **The earlier reuse check is replaced, not kept.** `cache_build_checks` covers its three cases through `run.main`, so it adds no coverage. Round 1's mutant `reuse: the fetch L1 and the arm are not compared` is still caught, now by the new check.
3. **One limit of the new build check.** The SoC export needs LiteX, so the self-test stands a recorder in for `split_soc.build`. `split_soc.py:353`'s own record of `fetch_l1` is attested by each run's `build.json` (`receipts/builds/` in round 1), not by the portable self-test. The README's Limits and the PR body say so.
4. **Suggestions not taken** (optional, outside the round's six items):
   - R713-1-S2: reuse compares the label `split`, not the resolved geometry.
   - R713-1-S3: `--xip --fetch-l1 none` is accepted.
   - R713-1-S4 and R714-1-S1: no synthetic refill trace for `sim_main.cpp`.
   - R714-1-S2: `xip_offset()` is not covered.
   - R713-1-S1 is answered by R714-1-F1's fix.
5. **Still open, as before:** NFR-SCOUT-01 awaits the owner's amendment, and the cache does not close T_svc. Also open: the integrated route (M8a-2), hardware evidence, and the self-test not run by a CI job.
