# [A762] FPGA-gPTP #102 handoff

Head: 97d83a72f4939ff938917deef33fa1ec1a5ba810 (branch 102-parallel-mutants, not pushed). Every Required item met.

Lane: $LANES/gptp102-mut, branch 102-parallel-mutants from main 1616fc8f.
origin: https://github.com/Mister-M-alt/FPGA-gPTP.git (checked).
Scratch: /data-2/milan/tmp/gptp102-a762 (under 400 MB at peak; clones, logs, tools). Issue comments: [A762] TAKEN
(2026-11-10 07:34 CET, session 1); [A762] REVIEW READY 97d83a7... (session 2, at the end). Nothing pushed.
PR-BODY.md in this directory ("Closes #102": every Required item met).

Toolchain (as the parent's $VALIDATION_STORAGE/640-m10-candidate-0923/full-native.json, read only):
PATH=$VALIDATION_STORAGE/640-m10-candidate-0923/pinned-tool-bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin,
VERILATOR_ROOT=$WORKSPACE_HOME/.local/share/containers/storage/overlay/9517af57.../diff/usr/share/verilator, Verilator 5.050 rev v5.050.

Session 1 was cut by the 07:49 host power-off. It had written the engine change and the test, uncommitted,
but measured nothing (no 16-CPU block was free). Session 2 resumed at 09:44, kept those edits, started the
baseline before committing anything, reviewed the edits, and committed:

| commit | subject |
|---|---|
| ab89c60 | Run the engine mutation arm's mutants concurrently, --jobs N at once, printed in list order (#102) |
| 97d83a7 | Compare the engine mutation arm's --jobs 1 and --jobs 4 output byte for byte (#102) |

## Status

- [x] item 1: measured at main; the engine driver is 96.7 % of `make all` (5:09:36 of 5:20:12)
- [x] item 2: --jobs N in the dominant driver (ab89c60)
- [x] item 3: `mutants-jobs-test` rc 0 at 97d83a7: --jobs 1 and --jobs 4 identical byte for byte (and = main's serial output)
- [x] item 4: per-mutant directories (ab89c60)
- [x] item 5: no other driver over 10 min serially (parser 215 s, gaskets 32 s, tsngen 31 s)
- [x] item 6: `make all` on 80-95: before 19211.5 s (5:20:12), after 2992.8 s (0:49:53), 6.42x
- [x] gates on clean clones of the committed head 97d83a7: all rc 0 (table below)

## Units

| unit | what | CPUs | started |
|---|---|---|---|
| milan-gptp102-a762-before | `make all` at main 1616fc8f, clean clone | 80-95 | 09:45:09, done 15:05:20 |
| milan-gptp102-a762-eq | `make -C tb/verilator/engine mutants-jobs-test` at 97d83a7, clean clone | 8-15 | 11:05:21, done 16:34:22 |
| milan-gptp102-a762-probe | gaskets and tsngen mutant drivers alone at main (item 5 decision only) | 64-71 | 11:16:55, done 11:18 |
| milan-gptp102-a762-after | idles (polls `systemctl is-active` of before every 2 s) until before exits, then `make all` at 97d83a7, clean clone | 80-95 | 11:19:03; ran 15:05:22 to 15:55:14 |

No 16-block came free from 09:49 to 11:00 (0-95 all held in 8-wide halves), so the equivalence test
(a correctness run, 1 + 4 workers, not a timing measurement) and the item-5 probe book the host's
standard 8-wide author range (`cpu_ranges.py pick`). The before/after `make all` pair keeps 80-95.

## Measurements

### Item 1: `make all` at main 1616fc8f, before any change

Unit milan-gptp102-a762-before, `taskset -c 80-95` (16 CPUs; the driver saw affinity 80-95), clean clone,
parent toolchain, TMPDIR in scratch, PYTHONUNBUFFERED=1 so each line is stamped when printed (no effect on any
verdict). Start 09:45:09, end 15:05:20 CET, rc 0. systemd: 5 h 32 min 24 s CPU over 5 h 20 min 12 s wall, 1 G
memory peak (one core busy on average out of 16). The host was fully booked (128/128 CPUs) the whole time.

| step | start (s) | end (s) | wall | wall (s) | share |
|---|---:|---:|---:|---:|---:|
| target `contract` | 0 | 0 | 0:00:00 | 0.0 | 0.0 % |
| target `tb` | 0 | 19210 | 5:20:10 | 19209.9 | 100.0 % |
|   sub-make `tb/verilator/ucpu` | 0 | 7 | 0:00:07 | 6.9 | 0.0 % |
|   sub-make `tb/verilator/parser` | 7 | 229 | 0:03:42 | 221.8 | 1.2 % |
|     suite (build + run) | 7 | 13 | 0:00:06 | 6.5 | 0.0 % |
|     driver `tb/verilator/parser/mutants.py` | 13 | 229 | 0:03:35 | 215.3 | 1.1 % |
|   sub-make `tb/verilator/engine` | 229 | 19124 | 5:14:55 | 18895.2 | 98.4 % |
|     suite (build + run) | 229 | 548 | 0:05:20 | 319.5 | 1.7 % |
|     driver `tb/verilator/engine/mutants.py` | 548 | 19124 | 5:09:36 | 18575.7 | 96.7 % |
|   sub-make `tb/verilator/gaskets` | 19124 | 19164 | 0:00:40 | 39.5 | 0.2 % |
|     suite (build + run) | 19124 | 19130 | 0:00:06 | 6.4 | 0.0 % |
|     driver `tb/verilator/gaskets/mutants.py` | 19130 | 19164 | 0:00:33 | 33.1 | 0.2 % |
|   sub-make `tb/tsngen` | 19164 | 19205 | 0:00:41 | 41.5 | 0.2 % |
|     suite (build + run) | 19164 | 19172 | 0:00:09 | 8.7 | 0.0 % |
|     driver `tb/tsngen/mutants.py` | 19172 | 19205 | 0:00:33 | 32.7 | 0.2 % |
|   sub-make `bench/arty` | 19205 | 19210 | 0:00:05 | 5.0 | 0.0 % |
| target `lint` | 19210 | 19210 | 0:00:00 | 0.3 | 0.0 % |
|   sub-make `bench/arty` | 19210 | 19210 | 0:00:00 | 0.2 | 0.0 % |
| target `docs` | 19210 | 19212 | 0:00:01 | 1.3 | 0.0 % |
| whole `make all` (rc 0) | 0 | 19212 | 5:20:12 | 19211.5 | 100.0 % |

**The dominant step is `tb/verilator/engine/mutants.py`: 18575.7 s (5:09:36), 96.7 % of `make all`.** The next
driver is the parser arm at 215.3 s; gaskets 33.1 s, tsngen 32.7 s (tsn-gen present: 4 checks, not a SKIP).

Baseline engine arm output (the driver's lines between its recipe line and Leaving, timestamps stripped):
77458 bytes, sha256 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2, 160 verdict lines
(control + 159 mutants), 0 `[FAIL]`, tally `160 checks: 160 PASS, 0 FAIL`.
Receipts: receipts/before/make.log (134.5 KB, sha256 ed89180d5ee4614a255a2e41b2399f5de517f4386c2adfd5b87c432a894eab1a),
summary.json, walls.json, engine-arm.stdout.

### Item 6: `make all` after, same 16 CPUs

Unit milan-gptp102-a762-after, `taskset -c 80-95` (affinity 80-95, the same 16 CPUs), clean clone of 97d83a7,
same toolchain and environment. It was started at 11:19 pinned to 80-95 and idled until the before unit exited,
so nothing else could take the range in between: start 15:05:22, end 15:55:14 CET, rc 0. CPU over the run
about the same as before (systemd: 5 h 36 min 38 s for the unit, against 5 h 32 min 24 s before; same work, now
overlapped), memory peak 3.9 G (MemoryMax 8 G). The engine driver ran with its default `--jobs` = min(8, 16) = 8.

| step | start (s) | end (s) | wall | wall (s) | share |
|---|---:|---:|---:|---:|---:|
| target `contract` | 0 | 0 | 0:00:00 | 0.0 | 0.0 % |
| target `tb` | 0 | 2991 | 0:49:51 | 2991.3 | 99.9 % |
|   sub-make `tb/verilator/ucpu` | 0 | 6 | 0:00:06 | 6.0 | 0.2 % |
|   sub-make `tb/verilator/parser` | 6 | 221 | 0:03:35 | 215.1 | 7.2 % |
|     suite (build + run) | 6 | 12 | 0:00:06 | 6.1 | 0.2 % |
|     driver `tb/verilator/parser/mutants.py` | 12 | 221 | 0:03:29 | 209.0 | 7.0 % |
|   sub-make `tb/verilator/engine` | 221 | 2908 | 0:44:46 | 2686.5 | 89.8 % |
|     suite (build + run) | 221 | 540 | 0:05:19 | 318.6 | 10.6 % |
|     driver `tb/verilator/engine/mutants.py` | 540 | 2908 | 0:39:28 | 2367.9 | 79.1 % |
|   sub-make `tb/verilator/gaskets` | 2908 | 2947 | 0:00:39 | 38.9 | 1.3 % |
|     suite (build + run) | 2908 | 2914 | 0:00:06 | 6.1 | 0.2 % |
|     driver `tb/verilator/gaskets/mutants.py` | 2914 | 2947 | 0:00:33 | 32.8 | 1.1 % |
|   sub-make `tb/tsngen` | 2947 | 2986 | 0:00:40 | 39.5 | 1.3 % |
|     suite (build + run) | 2947 | 2955 | 0:00:09 | 8.6 | 0.3 % |
|     driver `tb/tsngen/mutants.py` | 2955 | 2986 | 0:00:31 | 31.0 | 1.0 % |
|   sub-make `bench/arty` | 2986 | 2991 | 0:00:05 | 5.2 | 0.2 % |
| target `lint` | 2991 | 2992 | 0:00:00 | 0.3 | 0.0 % |
|   sub-make `bench/arty` | 2991 | 2992 | 0:00:00 | 0.2 | 0.0 % |
| target `docs` | 2992 | 2993 | 0:00:01 | 1.2 | 0.0 % |
| whole `make all` (rc 0) | 0 | 2993 | 0:49:53 | 2992.8 | 100.0 % |

| step | before (main 1616fc8f) | after (97d83a7) | change |
|---|---:|---:|---:|
| `tb/verilator/engine/mutants.py` | 18575.7 s (5:09:36) | 2367.9 s (0:39:28) | 7.84x faster, -16207.8 s |
| sub-make `tb/verilator/engine` | 18895.2 s | 2686.5 s | -16208.7 s |
| `tb/verilator/parser/mutants.py` | 215.3 s | 209.0 s | unchanged code |
| `tb/verilator/gaskets/mutants.py` | 33.1 s | 32.8 s | unchanged code |
| `tb/tsngen/mutants.py` | 32.7 s | 31.0 s | unchanged code |
| **whole `make all`** | **19211.5 s (5:20:12)** | **2992.8 s (0:49:53)** | **6.42x faster, -16218.7 s (-4:30:19)** |

After the change the engine sub-make is still the largest step (89.8 %): its driver 2367.9 s, and its suite part,
four serial passes of one harness build, 318.6 s.

Output of every mutation arm under `make all`, before against after (timestamps stripped, bytes compared):

| arm | before bytes / sha256 | after bytes / sha256 | |
|---|---|---|---|
| parser | 5116 / 487f7e9b6171db09... | 5116 / 487f7e9b6171db09... | identical |
| engine | 77458 / 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2 | 77458 / same | identical, 160 checks: 160 PASS |
| gaskets | 613 / e3595306f54c2bd4... | 613 / e3595306f54c2bd4... | identical |
| tsngen | 540 / 05fdd6255bf3b7aa... | 540 / 05fdd6255bf3b7aa... | identical |

So the engine arm at `--jobs 8` printed exactly what main's serial arm printed: the same 160 verdicts in the same
order, every named failure line, the same tally. Receipts: receipts/after/make.log (134.4 KB, sha256
08297e6dfc842a8c080be7fde481c73e4ce46b29001d806e3ec989952354fa81), summary.json, walls.json, engine-arm.stdout.
The clone held no tracked change and no untracked file afterwards (only the ignored build outputs of `make all`).

## Changes (head 97d83a7; diff from main: 4 files, +260 -40)

ab89c60, `tb/verilator/engine/mutants.py`:
- :27-32 docstring: `--jobs N`, its default, and why concurrency changes no verdict or output.
- :116 `JOBS_CAP = 8`.
- :977 `default_jobs()`: `len(os.sched_getaffinity(0))`, at most 8, at least 1 (`os.cpu_count()` where there is no affinity call).
- :986 `in_list_order(jobs, tasks)`: `--jobs 1` calls the tasks one after another exactly as before; more submit
  them in list order to a `ThreadPoolExecutor(jobs)` and yield each result only after every earlier one, so the
  completion order never shows. Shutdown waits for running tasks and cancels unstarted ones.
- :1007 `jobs_arg`, :1024 `--jobs` (argparse; `--jobs 0` is refused with exit 2).
- :891, :927 `named_verdict` / `run_mutant` take `say=print`: every line a mutant prints goes to its own list,
  printed by main in list order. The text of every line is unchanged.
- :948-959 each mutant stages, runs and builds in its own `tempfile.mkdtemp(prefix="mutant-", dir=work)`
  (item 4); before, all mutants used `work/src_<tag>`, `work/run_<tag>`, `work/obj_<tag>` in one directory.
  The control keeps `work/src_clean`, `run_clean`, `obj_clean`. 159 mutants, no two tags equal; the harness
  writes no file (no fopen/ofstream/$fopen in sim_main.cpp or hdl/).
- :1041-1072 main: the control and the 159 mutants are one task list (control first); the tally counts the same
  entries the same way. Nothing else: no mutant, check, `breaks` name, pattern or verdict rule is touched.
- `tb/verilator/engine/Makefile`:51-56 the `mutants` comment says one defect per mutant, several at once, `--jobs 1`.

97d83a7:
- `tb/mutation_jobs_test.py` (new, 119 lines): runs `<driver> --jobs 1` and `--jobs 4` (both at once), compares
  exit status, the verdict lists (:93), stdout (:94) and stderr (:95) byte for byte, and requires each run to print
  exactly 1 + len(MUTATIONS) verdict lines and a tally of that many checks (:102, :104), so two runs that abort
  alike cannot pass. Prints a unified diff on mismatch.
- `tb/verilator/engine/Makefile`:20, :59-65 target `mutants-jobs-test`; `all` leaves it out (its serial half takes
  as long as the whole arm did before).
- `docs/TEST_DEVELOPER.md`:23, :49, :60-66 the new file, the new target, and four short lines on `--jobs`.

Item 5: no other driver takes 10 min serially (parser 215 s under `make all` at main; gaskets 32 s and tsngen 31 s
alone at main on 64-71, tsn-gen checkout present, no SKIP), so no other driver changed.

Scratch checks (not committed): tools/smoke_order.py stubs build/run with random delays: `--jobs` 1, 4, 8 print the
same 64240 bytes, 160 PASS lines, 160 distinct run dirs. tools/fake/{good,bad}: the jobs test passes a driver
whose output is order-independent (rc 0) and fails one whose --jobs 4 output is reordered (rc 1, diff shown).

## Equivalence test

`make -C tb/verilator/engine mutants-jobs-test` (= `python3 ../../mutation_jobs_test.py mutants.py`) on a clean clone
of 97d83a7, unit milan-gptp102-a762-eq, `taskset -c 8-15` (8 CPUs, the 1 + 4 workers of the two runs at once),
11:05:21 to 16:34:22 CET, **rc 0**:

```
INFO --jobs 1: exit 0, 77458 bytes, sha256 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2, 160 verdicts, 19741 s
INFO --jobs 4: exit 0, 77458 bytes, sha256 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2, 160 verdicts, 5653 s
PASS the exit statuses agree (0 and 0)
PASS the verdict lists agree byte for byte
PASS stdout agrees byte for byte
PASS stderr agrees byte for byte
PASS --jobs 1 prints 160 verdict lines (got 160)
PASS --jobs 1 tallies 160 checks (got 160)
PASS --jobs 4 prints 160 verdict lines (got 160)
PASS --jobs 4 tallies 160 checks (got 160)
8 checks: 8 PASS, 0 FAIL
```

The same sha256 as main's serial arm under `make all` (before) and as this head's `--jobs 8` arm under `make all`
(after): four runs, one output, 160 checks: 160 PASS, 0 FAIL. The clone held no change afterwards.
Receipts: receipts/eq/make.log, summary.json. systemd: 12 h 0 min CPU over 5 h 29 min, 1.6 G memory peak.

## Gates

Clean clone of 97d83a7 (scratch head/gates), parent toolchain, each command's own rc (output to a file, not piped):

| gate | rc | result |
|---|---|---|
| `make contract` | 0 | PHC interface contract: PASS |
| `make docs` | 0 | docs check PASS, docs selftest PASS (127 arms), source evidence PASS + selftest PASS (7 arms), diagrams |
| `make diagrams-check` | 0 | diagram check PASS, diagram selftest PASS (10 arms) |
| `make lint` | 0 | engine lint + bench/arty lint |
| `python3 scripts/check_docs.py --selftest` | 0 | PASS (127 arms) |
| `python3 scripts/check_source_evidence.py --selftest` | 0 | PASS (7 arms) |
| `python3 scripts/generate_diagrams.py --selftest` | 0 | PASS (10 arms) |
| `python3 syn/ooc/check_ooc_clock.py --selftest` | 0 | PASS (30 arms) |
| `make all` (the after run, clean clone head/after, 80-95) | 0 | 2992.8 s; every arm's tally all PASS, contract, lint, docs PASS |
| `make -C tb/verilator/engine mutants-jobs-test` (clean clone head/eq, 8-15) | 0 | 8 checks: 8 PASS, 0 FAIL; --jobs 1 and 4 both 77458 bytes, sha256 9fb353df... |

Not run: `make ooc`'s Vivado synthesis (`syn/ooc/run.sh`): not part of `all`, not named as a gate in the docs, and
the diff touches no hdl/ or syn/ file; its selftest is above.
