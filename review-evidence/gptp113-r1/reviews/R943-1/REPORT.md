[R943] POSITIVE - exact head af11b3ef631eb44cdc1730cfb31bedda95c33dc5

Internal independent review of Mister-M-alt/FPGA-gPTP#113 / PR #114, round R943-1.
Head `af11b3ef631eb44cdc1730cfb31bedda95c33dc5`, tree `de4e33ba9c752220bdb0567cb6b9b5ec6c7c7e2a`, base `3009f9a2a2d69375211d8355490675879033d940` (the PR #112 merge). Two commits: `f3b24f3` (docstrings, one annotation, `make()` loses `stdout`) and `af11b3e` (the passes test moves to `tb/engine_passes_test.py`).

No open BLOCKER, MAJOR, MINOR or RESIDUE. Two SUGGESTIONs. One of them keeps the earlier SUGGESTION R944-S1.

## Basis

- **Repository rules.** This repository tracks no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md`, `docs/README.md` and `docs/TEST_DEVELOPER.md`. I also read the consumer's `AGENTS.md`, `CONTRIBUTING.md` and the Rule 12 text inside `scripts/check_py_idiom.py`.
- **Frozen acceptance (issue #113).**
  1. Both consumer ratchets pass, with their budgets unchanged, at a pin of the fix.
  2. `make passes-test` and the engine's four passes behave as in PR #112.
  - Scope allows either taking the test off host time or moving it out of the suite directory. The engine's behaviour, the microcode and `hdl/` are out of scope.
  - The issue has no comments, so there are no extra scope decisions.
- **Authorities.** The consumer `kebag-logic/milan-fpga` at `dev-soft-core` `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`, the same base the author used:
  - `scripts/check_py_idiom.py`, with `MAX_PARAMETERS = 6` and its budget `scripts/py_idiom.budget`;
  - `scripts/measure_test_evidence.py`, with its budget `scripts/test_evidence.budget`;
  - `scripts/code_quality_scope.py`, which refuses a scan when a project submodule is missing or off its pin.
- **Order of work.** I reviewed the diff (`receipts/diff_3009f9a_af11b3e.patch`) and both commits first. I then ran every campaign below and settled my findings. Only after that did I open the PR discussion.
- **Disclosure.** That discussion contains R944-1's published report. I read it after my independent runs and analysis, but before I had written this verdict and ledger to disk. The verdict rests only on the receipts in this packet. The one prior finding (R944-S1) is resolved below.
- **Public author packet.** For comparison only, I read the published author receipts under `review-evidence/gptp113-r1/author` at `dcfe275d`. No conclusion here depends on them.

## Conformance

- **Python idiom gate.** I reproduced it in a consumer checkout at `c34e7d8b`. `protocol-processor` sits at its pin `801ef228`. Only the `gptp-processor` gitlink moves, in a local commit. Budget files: `git diff --stat` against the consumer base is empty in every run.

  | `gptp-processor` at | `check_py_idiom.py` | `measure_test_evidence.py --check` |
  |---|---|---|
  | `1213ac5` (consumer's own pin) | rc 0 | rc 0, 3 <= 3 wall-clock files |
  | `3009f9a` (#112) | rc 1: unannotated 1 > 0, undocumented 7 > 0, too many parameters 8 > 7 | rc 1, 4 > 3; the fourth is `gptp-processor/tb/verilator/engine/passes_test.py` |
  | `af11b3e` (this head) | rc 0: 0 <= 0, 0 <= 0, 7 <= 7 | rc 0: 69 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |

  The other evidence counts at this head equal those at `1213ac5`, so the move hides nothing in any other metric. Receipts: `receipts/consumer/ratchets-*.log`.
- **Self-tests at the head pin.** `check_py_idiom.py --selftest` gives 54/54 PASS and `measure_test_evidence.py --selftest` gives 105/105 PASS. Receipts: `receipts/consumer/selftest-*.log`.
- **Live consumer `dev`.** As extra information, I also ran both gates on the consumer's live `dev` `e275d795`, with the pin moved from `1616fc8` to this head. Both gates return rc 0 with unchanged budgets: 0/0/7 idiom counts, and 67 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 evidence counts. Receipts: `receipts/consumer-livedev/`. This is not the manager's merge candidate.
- **Neither consumer branch names the old path.** `git grep passes_test` in the consumer at both commits finds nothing, outside `review-evidence/`.
- **The "eight parameters" wording.** The issue says "one function with eight parameters (limit 7)". In fact 8 is the gate's count of over-long signatures, against a budget of 7. The limit per function is 6, and `make()` had 7 parameters. The PR body states this correctly, and this head brings the count back to 7 <= 7. This is issue text, not delta text, so it is not a finding.
- **The move is in scope.** The issue allows moving the test out of the suite directory. `tb/` has no Makefile, so it is not a suite directory, and the consumer's scan confirms this.
- **No out-of-scope change.** The diff touches only `docs/TEST_DEVELOPER.md`, `tb/engine_passes_test.py` (a rename at 93% similarity), `tb/verilator/engine/Makefile` and `tb/verilator/engine/pass_run.py`.

## RTL

- **No RTL or microcode change.** The diff touches nothing under `hdl/`, and leaves `gptp_ucode.hex`, `sim_main.cpp`, the generator arguments, the stubs and `run`'s recipe lines alone.
- **`pass_run.py` is unchanged as a program.** With docstrings removed, base and head parse to the IDENTICAL program (`scripts/ast_equiv.py`, `receipts/ast_equiv.txt`).
- **The engine's four passes, run for real.** I ran `make -j4 -C tb/verilator/engine run` at base and at head. Each ran from a clean exported tree, with the pinned Verilator (it reports `Verilator 5.050 2026-07-01 rev v5.050`), `OBJCACHE=` and `ulimit -c 0`. Receipt: `receipts/engine_compare.txt`.
  - **Clean runs.** Both exit rc 0, and the transcripts are IDENTICAL over 175 normalised lines. The passes print in serial order with 2302, 2302, 2302 and 61 checks, all PASS. All four records are `exit 0`.
  - **Planted abort in a copy of the harness.** The abort fires at the start of pass 1 (`cwd` ends in `/seedrun`). Both trees exit rc 2, and the transcripts are IDENTICAL over 61 normalised lines, ending `make: *** [Makefile:74: run] Aborted (core dumped)`.
  - **Pass records under the planted abort.** Identical at both layouts: pass 1 `signal 6, core`; passes 2 and 3 `stopped, signal 15`; only `1.stop` marked.
  - **Normalisation.** It drops only the Verilator command and banner, compiler and sub-make directory lines and my own wall-time line, and masks the tree path (`scripts/compare_engine.py`).
- **Lint.** `make lint` exits 0 with the pinned Verilator 5.050 (`receipts/gates/make-lint.log`).

## Robustness

- **Docstrings checked against the code.**
  - `chunk` (`tb/verilator/engine/pass_run.py:105`): one byte for the stream, a 4-byte big-endian length, then the data. Correct.
  - `forward` (`:109`): installed for the INT, TERM, QUIT and HUP signals that are not ignored, and `signal_all` sends it to the child and all its descendants. Correct.
  - `stop` (`:115`): SIGUSR1 is sent only by `stop_later` of a failing earlier pass. It is guarded by `failed_before(n)`, and it ends the child with SIGTERM. Correct.
  - `main` (`:268`): correct.
  - `caller` (`tb/engine_passes_test.py:402-404`): the docstring and the `tuple[int, int]` annotation match the clamping to the hard limit and the INT and QUIT defaults.
  - Test `main` (`:434`): correct.
- **Dropping `stdout` from `make()` is behaviour-neutral.** All six call sites pass at most four positional arguments, and `directory`/`target` only by keyword, so none ever passed `stdout`. The AST diff of the test shows only the `HERE` to `ENGINE` path change, that parameter removal and the annotation (`receipts/ast_equiv.txt`).
- **Path resolution.** `ENGINE = Path(__file__).resolve().parent / "verilator" / "engine"` (`tb/engine_passes_test.py:66`) is absolute. The test therefore finds the same Makefile and `pass_run.py` from any working directory. `passes-test` runs `python3 ../../engine_passes_test.py` from the engine directory (`tb/verilator/engine/Makefile:99-100`).
- **Signal and exit replay.** The planted defects below show that the signal and exit-status replay paths stay load-bearing through the moved test.

## Tests

- **Planted defects, each in its own exported tree, at both layouts.** I planted seven defects of my own into the real engine `pass_run.py` or Makefile and ran `make -C tb/verilator/engine passes-test`. Every one is caught at base and at head, and the set of failing checks that do not depend on host load is identical at the two layouts (`scripts/campaign.sh`, `scripts/compare_plants.py`, `receipts/plants_compare_wave1.txt`, `receipts/runs/`):

  | Planted defect | Checks that fail at both layouts |
  |---|---|
  | No fail-fast stop after a failing simulator | 2: the fail-fast checks at `-j4` and `-j1`, with all four passes started and the run taking 30–67 s |
  | Signals not forwarded | 1: SIGTERM to make's own process leaves 4 simulators |
  | A simulator's signal death replayed as 128+n | 13 |
  | Standard error merged into standard output | 51 |
  | Replay re-raising in make's directory | 1: check 6 |
  | No-core replay left dumpable (no `prctl`) | 2 |
  | `-i` not passed to the runner | 8: the `-i` transcripts of every plan with a failure before its last step |

  These checks read the real engine files. A defect planted in `tb/verilator/engine/` is caught by the test at its new place, so the move kept the coverage.
- **Unplanted controls.** At low concurrency, base, head, and head under `ulimit -c 0` each pass 73/73 with rc 0 (`receipts/runs-wave2/`).
  - Check 8 ran at core limits 0 and 1. Under `ulimit -c 0` it reports `0 (clamped to the hard limit)`, as designed.
  - In the first wave (12 concurrent campaigns, host load about 95 on 32 CPUs), the head control passed 73/73. The base control and the head control under `ulimit -c 0` each failed one check, and only a check that a budget is actually reached (see R943-S1).
- **Coverage is kept.** All 8 check groups and the 73 checks are present. `all: run passes-test ...` still runs it. The top-level `make tb` runs the engine's `all`.

## Docs

- **`docs/TEST_DEVELOPER.md:25`.** The new Python-layers row names the right file and purpose, and the entry-point row at `:53` still names `make -C tb/verilator/engine passes-test`.
- **Module docstring and Makefile comment.** The test's module docstring (`tb/engine_passes_test.py:4-17`) and the Makefile comment (`tb/verilator/engine/Makefile:97-98`) say where the test lives and why, citing #111 and #113.
- **Gates.** `make docs` and `make contract` exit 0 (`receipts/gates/`). No doc carries a line anchor into the changed files. A probe that removed the new row still passed `check_docs.py`, so the gate does not enforce the row: it is a hand-kept entry, and it is correct (`receipts/gates/docs-row-probe.log`).
- **Comment rule.** None of the 34 added lines and neither commit message carries a lane label, lane name, review round, reviewer ID, issue-comment ID, tool or model name, or private path (`receipts/residue_scan.txt`). The PR body's opening lane tag is allowed in PR text.

## Findings

### R943-S1: SUGGESTION. Lenses: Tests, Robustness

- **Retains** R944-S1 at this head.
- **Artifact.**
  - `tb/engine_passes_test.py:259-275`: the budget must be reached, for `make -jN run` and for the parent `make -j3`.
  - `tb/engine_passes_test.py:282-291`: every pass must start before the fail-fast stop at `-j4`.
  - The same lines at base, `tb/verilator/engine/passes_test.py`.
- **Evidence.** In wave 1, under host load:
  - The base control failed `make -j4 run: at most 2 passes at once (budget 4)`.
  - The head control under `ulimit -c 0` failed `a parent make -j3 with two other jobs: ... at most 2 jobs at once in all`.
  - Several planted-defect runs at both layouts failed the same kind of check.
  - In wave 2, all three controls passed 73/73.
  - These checks are identical programs at base and head (AST), so the sensitivity is inherited from PR #112, not introduced here.
  - Wall times of 215–508 s also exceed the "about 90 seconds" in the docstring and Makefile, which is inherited text.
- **Impact.** On a loaded shared host, a correct tree can fail a check that only proves the budget is reached. No defect goes undetected.
- **Required outcome.** None for this PR. A follow-up could start the stubs through a barrier while keeping the upper bounds and the hang bounds.
- **Verification.** `receipts/runs/pt-*-control*.log` against `receipts/runs-wave2/*.log`.

### R943-S2: SUGGESTION. Lenses: Docs

- **Artifact.** `tb/engine_passes_test.py:212`, the docstring of `read`: "The stub jobs' recorded events, none before the first."
- **Evidence.** It is accurate, since it returns `[]` until the events file exists, but it is hard to parse.
- **Impact.** Readability only.
- **Outcome.** Optional: "The stub jobs' recorded events; an empty list until the first is written."
- **Verification.** Reading.

## Prior public findings at this head

- **R944-S1 (SUGGESTION, Tests/Robustness).** Retained as R943-S1, with my own receipts. It does not block.
- **Other findings.** The PR has no inline review comments or other findings.

## Ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #113 acceptance and scope; consumer `check_py_idiom.py` (MAX_PARAMETERS 6), `measure_test_evidence.py`, `code_quality_scope.py` and both budgets; my own consumer runs at pins 1213ac5/3009f9a/af11b3e on `c34e7d8b` and 1616fc8/af11b3e on `e275d795`; both self-tests; the four-file diff | R943-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| RTL | CLEAN | No `hdl/`, microcode, harness or recipe change; `pass_run.py` AST IDENTICAL; real engine `make -j4 run`, clean and planted abort, base against head: IDENTICAL transcripts, status and pass records; `make lint` with Verilator 5.050 | R943-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| Robustness | CLEAN | `pass_run.py:105,109,115,268` docstrings against the code; `engine_passes_test.py:66,191-201,357,370,398,402-404`; `make()` call sites; signal, exit and core replay through 7 plants at both layouts | R943-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| Tests | CLEAN | `make passes-test` controls 73/73 at base, head and head under `ulimit -c 0`; 7 planted defects caught with identical failing-check sets at both layouts; the move's coverage (real engine files read from `tb/`); `all` wiring | R943-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| Docs | CLEAN | `docs/TEST_DEVELOPER.md:25,53`; module docstring; Makefile `:97-100`; `make docs`, `make contract`; docs-row probe; comment-rule and privacy scan of the added lines and commit messages | R943-1 | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |

## Real limits

- **Hosted checks.** At this exact head there are 0 check runs and 0 commit statuses, and the combined state is `pending` with no contexts. The repository tracks no workflows. There is neither an executed nor a skipped hosted context to count (`receipts/hosted_status.txt`). The manager owns hosted and act acceptance.
- **No manager source bank** ran at this head, and none is claimed or inferred. I ran no full parent, PP, gPTP, Yosys or builder banks, and no Vivado.
- **Host load.** The host was shared and heavily loaded throughout, at about 80–95 on 32 CPUs. The timings recorded here are not comparisons.
- **Planted defects.** I planted seven defects of my own design. I did not re-run all thirteen of the author's.
- **Core limits.** The host's `core_pattern` is piped. The caller-limit-1 case of check 8 ran at limit 1, not clamped. I did not exercise a file `core_pattern`.
- **Consumer scope.** The consumer runs used scratch local commits that only move the gitlink, and nothing was pushed. Other consumer submodules (`external`, `third_party/*`) were not initialised, and the gates do not scan them.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof. This makes no hardware or certification claim.
- **Clone integrity.** The review clone was never edited. It is verified at exact head and tree: index tree = `de4e33ba`, 123/123 tracked blobs and modes match, the worktree is clean including ignored files, and the repository has no gitlinks or `.gitmodules` (`receipts/clone_integrity.txt`).

## Pending manager duties

- Build and validate the current-dev merge candidate with the builder and native banks at the merge turn, and link those receipts on the PR. The source base is `3009f9a2a2d69375211d8355490675879033d940` and live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`.
- Decide on hosted and act acceptance for the exact head.
- Carry R943-S1 and R943-S2 as optional follow-ups. Neither is a merge condition.
- Bump the consumer pin under milan-fpga #1013, with the ratchets re-run at the bumped pin.

## Reproduction

These scripts are in `scripts/`. Arguments are a review clone, this packet directory, the Verilator path and a consumer checkout:

- `ast_equiv.py OLD NEW`
- `campaign.sh CLONE PACKET VERILATOR` (`JOBS=12`)
- `controls.sh RUNS OUT`
- `compare_plants.py RUNS`
- `compare_engine.py RECEIPTS RUNS`
- `consumer_ratchets.sh CONSUMER BASE OUT PIN...`

Host paths in the receipts are masked as `<packet>`, `<clone>`, `<verilator-5.050>`, `<verilator-install>` and `<home>`. Only this file and the files listed in `MANIFEST.sha256` are publishable.

R943-1 FINISHED
