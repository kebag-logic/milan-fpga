Closes #113.

Bring the engine runner of PR #112 inside the two documentation ratchets of the consumer, kebag-logic/milan-fpga,
that scan the pinned processor. The four passes and `make passes-test` behave as they did in PR #112.

Branch `113-runner-ratchets`: two commits on main `3009f9a` (#112), head `af11b3ef631eb44cdc1730cfb31bedda95c33dc5`.

- `f3b24f3` documents and annotates the runner's public functions, and drops an unused parameter.
- `af11b3e` moves the passes test to `tb/`, beside the mutation arm's scheduling tests, outside the suite
  directory.

## What changes

- **Python idiom** (the consumer's `scripts/check_py_idiom.py`, its Rule 12):
  - **`pass_run.py`.** The run closures `chunk`, `forward` and `stop` and the entry point `main` each gain a
    docstring.
  - **`engine_passes_test.py`.** `read` and `main` gain docstrings. The core-limit closure `caller` gains a
    docstring and annotates its `limit` parameter.
  - **`make()`.** It drops its `stdout` parameter, which no caller passed. It took 7 parameters, over the gate's
    limit of 6. It now takes 6.
- **Test evidence** (the consumer's `scripts/measure_test_evidence.py`, its wall-clock ratchet):
  - `passes_test.py` moves from `tb/verilator/engine/` to `tb/engine_passes_test.py`.
  - It finds the engine's `Makefile` and `pass_run.py` at `tb/verilator/engine/`, as it found them beside it
    before.
  - `make -C tb/verilator/engine passes-test` runs it from there.
  - `docs/TEST_DEVELOPER.md` lists it among the Python layers. The Makefile comment above `passes-test` says why
    it lives there.

Nothing else changes: no recipe of `run`, no pass, no check, no stub, no image, no generator argument, no
`hdl/` or microcode file. `pass_run.py` parses to the same program as at `3009f9a` once its docstrings are
removed.

## Why move the test rather than give it a controlled clock

The consumer's ratchet counts suite files that read host time or pass a process deadline. A suite file is any
file under a directory with a testbench `Makefile`. `passes_test.py` matches it at 13 lines, of four kinds:

| Kind | Lines | What it is for |
|---|---:|---|
| Stub run lengths and their timestamps | 4 | The stub passes must really overlap under make's jobserver: the budget peaks, the out-of-order finish, a pass still running when an earlier one fails |
| Hang bounds (`timeout=`) | 3 | A regressed stop or signal path fails in seconds instead of hanging the suite |
| Fail-fast elapsed time | 2 | Records that the stopped passes did not run out their 30 s |
| Signal-check start wait and grace | 4 | Waits until four simulators run before signalling make, then lets them die before counting survivors |

None of these is a DUT oracle. The test checks how make and the runner schedule, stop and signal real host
processes, and that behaviour happens in host time. A controlled clock would mean:

- replacing the stubs' overlap with barriers that depend on the job budget;
- rewriting most checks around them;
- dropping the hang bounds.

The first two would leave a different test from PR #112's. The consumer's own process tests keep such bounds on
purpose: they bound a hang and are never a property under test.

Both repositories already keep such tests outside the suite directories:

- in this repository, `tb/mutation_order_test.py` and `tb/mutation_jobs_test.py`, the mutation arm's scheduling
  tests, which also read host time;
- in the consumer, its sweep-cancellation and process tests under `scripts/`.

`tb/engine_passes_test.py` joins the first two. It still reads host time. It is no longer counted as RTL test
evidence, because it is not RTL test evidence.

## Evidence (2026-11-26)

### Both consumer ratchets, budgets unchanged

The probe was a kebag-logic/milan-fpga checkout of `dev-soft-core` (`c34e7d8b`), with both project submodules
initialised. Only the `gptp-processor` gitlink was moved, in a local commit, and the budget files are those of
`dev-soft-core`.

| `gptp-processor` at | `check_py_idiom.py` | `measure_test_evidence.py --check` |
|---|---|---|
| `1213ac5` (the branch's own pin) | rc 0 | rc 0, 3 <= 3 wall-clock files |
| `3009f9a` (#112) | rc 1: unannotated 1 > 0, undocumented 7 > 0, too many parameters 8 > 7 | rc 1: 4 > 3 wall-clock files |
| this head | **rc 0**: unannotated 0 <= 0, undocumented 0 <= 0, too many parameters 7 <= 7 | **rc 0**: 3 <= 3 wall-clock files |

- At this head the other evidence counts are those of `1213ac5`: 69 <= 77 suites without a mutation arm,
  10 <= 10 unseeded draw sites and 0 <= 0 unexplained DUT readers.
- Both tools' self-tests pass: 54/54 and 105/105.
- The "8" in the issue is the consumer's count of over-long signatures, against a budget of 7. The function was
  `make()` in the test, with 7 parameters where the limit is 6.

### `make passes-test` behaves as in PR #112

- **At this head.** 73 of 73 checks pass on each of four runs, one of them under `ulimit -c 0`. A run takes
  about 2 minutes on a shared host.
- **Planted defects.** PR #112's thirteen planted defects were each applied to a scratch copy, once at
  `3009f9a`'s layout and once at this head's. Each is caught at both layouts, with the same number of failing
  checks:

  | Planted defect | Failing checks at `3009f9a` / here |
  |---|---:|
  | the four passes in one job | 5 / 5 |
  | the echo under `-s` | 10 / 10 |
  | `-i` not passed | 8 / 8 |
  | the `-k` suppression removed | 8 / 8 |
  | a simulator's signal death replayed as 128+n | 13 / 13 |
  | no fail-fast stop | 2 / 2 |
  | a print failure ignored | 1 / 1 |
  | signals not forwarded | 1 / 1 |
  | standard error merged into standard output | 51 / 51 |
  | the generator without the serial redirection, its signal death replayed as 256-n | 5 / 5 |
  | a generator's own signal death not re-raised | 2 / 2 |
  | the replay re-raising in make's directory | 1 / 1 |
  | a no-core replay left dumpable | 2 / 2 |

  The unplanted control passes 73/73 at both layouts.

### The engine's four passes behave as in PR #112

`make -j4 -C tb/verilator/engine run`, at `3009f9a` and at this head, from clean trees, run concurrently with
Verilator 5.050 and `ulimit -c 0`:

| Run | `3009f9a` | this head | Transcript |
|---|---|---|---|
| Clean | rc 0, 175.3 s | rc 0, 174.0 s | IDENTICAL, 179 normalised lines |
| Planted abort at the start of pass 1 | rc 2, 181.5 s | rc 2, 170.0 s | IDENTICAL, 64 normalised lines |

- The abort was planted in scratch copies of the harness only.
- The normalisation is PR #112's own: the Verilator banner and compiler lines, plus the tree's own path.
- **Clean runs.** Passes 0–3 print in the serial order, with 2302, 2302, 2302 and 61 checks, all PASS.
- **Planted abort.** Both arms print pass 0's checks, the request-counter echo line and
  `planted: pass 1 aborts`, then `make: *** [Makefile:74: run] Aborted (core dumped)`.
  - In both, the records of passes 2 and 3 say `stopped`: they ended by SIGTERM.
  - `run`'s recipe lines did not move, so the line number is the same.
- **Timings.** They are recorded, not compared: the two arms shared a loaded host.

### This repository's checks

`make docs`, `make contract` and `make lint` each exit 0 at this head. Lint used Verilator 5.050.

## How to validate

```sh
git checkout 113-runner-ratchets
make -C tb/verilator/engine passes-test      # engine passes test: PASS (73 checks)
make docs contract lint                      # each exits 0
make -j4 -C tb/verilator/engine run          # rc 0; the transcript of 3009f9a's run
```

In a consumer checkout, with `gptp-processor` at this head and both project submodules initialised:

```sh
python3 scripts/check_py_idiom.py            # rc 0, budgets unchanged
python3 scripts/measure_test_evidence.py --check   # rc 0, 3 <= 3 wall-clock-dependent suite files
```
