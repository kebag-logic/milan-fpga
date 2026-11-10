[A762]

Run the engine mutation arm's mutants concurrently: `make all` goes from 5:20:12 to 0:49:53 on the same 16 CPUs,
and every mutation arm prints byte for byte what it printed before.

## 1. Measured first, at main 1616fc8

`make all` on a clean clone of main, pinned to 16 CPUs, every output line timestamped:

| step | wall | share |
|---|---:|---:|
| `contract` | 0.0 s | 0.0 % |
| `tb/verilator/ucpu` | 6.9 s | 0.0 % |
| `tb/verilator/parser` (suite 6.5 s, `mutants.py` 215.3 s) | 221.8 s | 1.2 % |
| `tb/verilator/engine` (suite 319.5 s, **`mutants.py` 18575.7 s**) | 18895.2 s | 98.4 % |
| `tb/verilator/gaskets` (suite 6.4 s, `mutants.py` 33.1 s) | 39.5 s | 0.2 % |
| `tb/tsngen` (suite 8.7 s, `mutants.py` 32.7 s) | 41.5 s | 0.2 % |
| `bench/arty test` | 5.0 s | 0.0 % |
| `lint` | 0.3 s | 0.0 % |
| `docs` | 1.3 s | 0.0 % |
| **`make all`** | **19211.5 s (5:20:12)** | |

The dominant step is `tb/verilator/engine/mutants.py`: 5:09:36, 96.7 % of `make all`. It builds and runs a
control and 159 mutants one after another, each harness run single-threaded (one core busy out of 16 on
average over the whole run).

## 2. `--jobs N` in the engine driver

- `tb/verilator/engine/mutants.py` takes `--jobs N` (at least 1). The default is the number of CPUs the
  process may use, `len(os.sched_getaffinity(0))`, capped at `JOBS_CAP = 8`.
- `--jobs 1` runs the control and then each mutant, in list order, one after another, as today.
- With more, the control and the mutants share a pool of N workers, submitted in list order.

## 3. Verdicts and output unchanged

- Every line a mutant prints goes to that mutant's own list, and main prints the lists in mutant list order,
  each once it and every earlier entry are done. Completion order never shows.
- The tally counts the same entries the same way. No mutant, pattern, named check, verdict rule or tally is
  removed, merged or weakened.
- New test `tb/mutation_jobs_test.py`, target `make -C tb/verilator/engine mutants-jobs-test`: runs the driver
  with `--jobs 1` and with `--jobs 4` and compares the exit statuses, the verdict lists, stdout and stderr byte
  for byte. It also requires each run to print exactly one verdict line per entry (control + every mutant) and
  a tally of that many checks, so two runs that abort alike cannot pass. `make all` leaves it out: its serial
  half takes as long as the whole arm did before.

Result at this head: rc 0, 8 checks: 8 PASS, 0 FAIL. `--jobs 1` and `--jobs 4` each printed 160 verdicts, 77458
bytes, sha256 `9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2`: the same bytes main's serial
arm prints under `make all` (section 6).

## 4. One temporary directory per mutant

Each mutant stages its sources, writes its images, builds and runs in its own `tempfile.mkdtemp()` under the
arm's temporary directory. No two mutants share a build or run directory (before, every mutant used
`src_<tag>`, `run_<tag>` and `obj_<tag>` side by side in one directory). The harness writes no file of its own.

## 5. Other drivers

None takes 10 min serially: parser 215.3 s, gaskets 33.1 s, tsngen 32.7 s under `make all` at main. They are
unchanged.

## 6. `make all` before and after, same 16 CPUs

| step | before (main) | after (this head) | |
|---|---:|---:|---:|
| `tb/verilator/engine/mutants.py` | 18575.7 s (5:09:36) | 2367.9 s (0:39:28) | 7.84x |
| `tb/verilator/engine` sub-make | 18895.2 s | 2686.5 s | |
| parser / gaskets / tsngen drivers | 215.3 / 33.1 / 32.7 s | 209.0 / 32.8 / 31.0 s | unchanged code |
| **`make all`** | **19211.5 s (5:20:12)** | **2992.8 s (0:49:53)** | **6.42x, -4:30:19** |

Both runs: clean clones, the same pinned toolchain, the same 16 CPUs, one directly after the other, on a host
that was fully booked throughout. The after run used `--jobs` 8 by default; memory peak 3.9 G.

Under `make all`, every mutation arm's output after is byte for byte its output before: parser 5116 bytes,
engine 77458 bytes (sha256 `9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2`,
160 checks: 160 PASS, 0 FAIL), gaskets 613 bytes, tsngen 540 bytes.

After the change the engine sub-make is still the largest step (89.8 %): its driver, and the four serial passes
of its suite (318.6 s).

## Files

- `tb/verilator/engine/mutants.py`: `--jobs`, `default_jobs()`, `in_list_order()`, one directory per mutant,
  lines collected per mutant and printed in list order.
- `tb/verilator/engine/Makefile`: the `mutants` comment, and the `mutants-jobs-test` target.
- `tb/mutation_jobs_test.py`: the `--jobs 1` / `--jobs 4` byte-for-byte test.
- `docs/TEST_DEVELOPER.md`: the new test file and target, and four lines on `--jobs`.

## Gates, on a clean clone of this head

| gate | rc |
|---|---|
| `make all` | 0 (2992.8 s) |
| `make -C tb/verilator/engine mutants-jobs-test` | 0 (8 checks: 8 PASS) |
| `make contract` | 0 |
| `make docs` | 0 |
| `make diagrams-check` | 0 |
| `make lint` | 0 |
| `python3 scripts/check_docs.py --selftest` | 0 (127 arms) |
| `python3 scripts/check_source_evidence.py --selftest` | 0 (7 arms) |
| `python3 scripts/generate_diagrams.py --selftest` | 0 (10 arms) |
| `python3 syn/ooc/check_ooc_clock.py --selftest` | 0 (30 arms) |

`make ooc`'s out-of-context synthesis is not part of `all`; this change touches no `hdl/` or `syn/` file.

Closes #102
