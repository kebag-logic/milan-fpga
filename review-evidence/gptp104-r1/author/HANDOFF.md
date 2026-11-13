# [A777] FPGA-gPTP #104 handoff

Head: 860e47493ad5a92c4662fef601fd196b0143c4bb (branch 104-ccache-idiom from main a64be73d, not pushed). Every
Required item met.

Lane: $LANES/gptp104-ccache. origin: https://github.com/Mister-M-alt/FPGA-gPTP.git (checked).
Scratch: /data-2/milan/tmp/gptp104-a777 (clones, parent clone, caches, logs, tools; every CCACHE_DIR and TMPDIR
there; 1.1 GB at peak, 702 MB at the end). PR-BODY.md in this directory ("Closes #104").
Issue comments: [A777] TAKEN (2026-11-12 16:07 CET, comment 6827331077, session 1); [A777] REVIEW READY 860e47493ad5a92c4662fef601fd196b0143c4bb
(2026-11-13 02:33 CET, comment 6841141540, session 2). Nothing pushed; no PR; nothing in the parent repository changed.

Toolchain (as $VALIDATION_STORAGE/883-candidate-0923/full-native.json, read only):
PATH=$VALIDATION_STORAGE/883-candidate-0923/pinned-tool-bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin,
VERILATOR_ROOT=$WORKSPACE_HOME/.local/share/containers/storage/overlay/9517af57.../diff/usr/share/verilator, Verilator 5.050 rev v5.050
(verilated.mk: `OBJCACHE ?=`, `CCACHE_SLOPPINESS ?= pch_defines,time_macros`, exported); ccache 4.14.1 at /usr/bin/ccache;
TMPDIR=/data-2/milan/tmp/gptp104-a777/tmp.

Session 1 (16:06) made all five commits, ran the three `make all` measurements (done 18:49) and the quick gates,
and started the equivalence test at ad06db3; the 19:20 host power-off killed that test about 70 of 160 entries into
its serial runs, with no result (partial log: receipts/eq-killed-1920). Session 2 (20:42) found the tree clean at
860e474, removed that run's temporary directories, and reran the test on a fresh clean clone of the head 860e474:
rc 0 at 02:31.

## Commits (a64be73d..860e474: 6 files, +687 -316)

| commit | subject |
|---|---|
| 60a2e3d | Annotate and document the engine mutation arm's public functions and move its path controls to path_mutants.py, under 1,000 lines (#104) |
| 80d1df4 | Compile the engine suite's and mutants' Verilator builds through ccache when it is on PATH, OBJCACHE= to turn it off, with no build path in the cache key (#104) |
| a73258c | Compare the engine arm's output at --jobs 1 and 8 with ccache off, cold and warm byte for byte, and check its verdict order inside make all (#104) |
| ad06db3 | Document the engine builds' ccache, its OBJCACHE= switch and the two order tests in the test guide (#104) |
| 860e474 | Give the engine jobs test's runtime as about seven hours on sixteen CPUs (#104) |

860e474 came after the measurements had started, once the first test run's serial pace (about 148 s per entry on
the loaded host) showed ad06db3's "about six hours" was short. `git diff ad06db3 860e474` is one docs sentence
(docs/TEST_DEVELOPER.md:86) and one Makefile comment (tb/verilator/engine/Makefile:78-81), no code. The before and
after-cold `make all` ran at a64be73d and ad06db3; the after-warm `make all`, every gate, both parent idiom gates and
the equivalence test ran at 860e474. The rerun then took 5:48:30 on a nearly idle host, so the guide's "about seven
hours" is the loaded-host figure; I left it rather than move the head again for one sentence (a reviewer may prefer
"six to seven").

## Status

- [x] item 1: parent `check_py_idiom.py` and `check_cpp_idiom.py` rc 0 at 860e474 (and at ad06db3); no ratchet or scope edit
- [x] item 2: ccache when on PATH, `OBJCACHE=` off, no build path in the key, cache outside the tree (80d1df4)
- [x] item 3: `mutants-jobs-test` rc 0 at 860e474: six runs (--jobs 1/8 x ccache off/cold/warm) byte-identical, 38/38
- [x] item 4: `make all` on 48-63: before 2894.8 s, after cold 2810.6 s (-2.9 %), after warm 2797.1 s (-3.4 %)
- [x] item 5: the residue's wording (docs/TEST_DEVELOPER.md:62); fast order check inside `make all` (a73258c)
- [x] gates on clean clones of the committed head 860e474: all rc 0 (table at the end)

## Units

| unit | what | CPUs | ran |
|---|---|---|---|
| milan-gptp104-a777-measure | `make all` at a64be73d (clone head/before), then at ad06db3 with an empty cache (head/after-cold), then at 860e474 with that cache warm (head/w/after-warm, another path), one after another | 48-63 | 16:27:21 - 18:49:04 |
| milan-gptp104-a777-eq | `make -C tb/verilator/engine mutants-jobs-test` at ad06db3 (head/eq) | 32-47 | 16:27:26, killed by the 19:20 power-off |
| milan-gptp104-a777-eq2 | the same test at 860e474 (head/eq, a fresh clean clone) | 80-95 | 20:42:42 - 02:31:12, rc 0 |

Each 16-CPU block was free when booked (`cpu_ranges.py pick --width 16`), and each unit was checked pinned (`taskset
-cp` of its main process). The quick gates and negative checks ran pinned to 44-47, inside the first eq block (that
test uses at most 3 + 8 workers), never on the measurement's 48-63.

## Item 1: the parent idiom gate

Scratch clone of kebag-logic/milan-fpga `dev` at fa6c094b8e (parent/), `git submodule update --init
protocol-processor gptp-processor`; then `gptp-processor` checked out at the head and its gitlink staged in the
scratch index only (`git update-index --cacheinfo 160000,<head>,gptp-processor`), which is what makes
`code_quality_scope.py` accept it as pinned (" " in `git submodule status`). Nothing committed or pushed; `git diff
HEAD -- scripts/` empty, so no ratchet (`scripts/py_idiom.budget`, `scripts/cpp_idiom.budget`) and no scope edit.

| gptp-processor at | `check_py_idiom.py` | `check_cpp_idiom.py` |
|---|---|---|
| 1616fc8f (the parent's pin) | rc 0, 541 modules | - |
| a64be73d (main) | **rc 1**: long module 11 > 10, unannotated public function 4 > 0, undocumented public function 4 > 0 | rc 0 |
| ad06db3 | rc 0, 544 modules, every ratchet at its budget | rc 0, every count 0 |
| 860e474 (head) | rc 0, 544 modules: long module 10 <= 10, unannotated 0 <= 0, undocumented 0 <= 0, every other ratchet at its budget | rc 0 |

Head output (receipts/parent-idiom/parent-py-idiom.log):

```
py idiom: 544 first-party modules, 284904 lines
  bare except: 0
  mutable default argument: 0
  shell invocation: 0
  shadowed builtin: 0
  wildcard import: 0
  dynamic eval/exec: 0
  unparseable source: 0
  long function: 9 <= 9
  long module: 10 <= 10
  unannotated public function: 0 <= 0
  undocumented public function: 0 <= 0
  os.path use: 1 <= 1
  unmanaged open: 0 <= 0
  too many parameters: 7 <= 7
  global statement: 0 <= 0
  over-long line: 0 <= 0
```

`check_cpp_idiom.py` at the head: rc 0, 352 translation units, every count 0 <= 0 (receipts/parent-idiom/parent-cpp-idiom.log).
The two new modules (path_mutants.py, mutation_order_test.py; 542 -> 544) and the rewritten mutation_jobs_test.py
and mutants.py scan clean on their own with the parent's `scan()`; mutants.py is 863 lines.

## Item 3: the equivalence test

`make -C tb/verilator/engine mutants-jobs-test` (= `python3 ../../mutation_jobs_test.py mutants.py`) on a clean
clone of 860e474, unit milan-gptp104-a777-eq2, `taskset -c 80-95` (16 CPUs), 20:42:42 to 02:31:12 CET
(20909.9 s), **rc 0**; the clone held no change afterwards (only `__pycache__`, ignored). Output
(receipts/eq/make.log):

```
INFO jobs1-cold: ccache cache_miss 74, direct_cache_hit 210, files_in_cache 78, ...
INFO jobs8-cold: ccache cache_miss 74, direct_cache_hit 210, files_in_cache 78, ...
INFO jobs1-warm: ccache direct_cache_hit 273, preprocessed_cache_hit 11, (no cache_miss), ...
INFO jobs8-warm: ccache direct_cache_hit 273, preprocessed_cache_hit 11, (no cache_miss), ...
INFO jobs1-off: exit 0, 77458 bytes, sha256 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2, 160 verdicts, 19412 s
INFO jobs8-off: exit 0, 77458 bytes, sha256 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2, 160 verdicts, 3020 s
INFO jobs1-cold: exit 0, 77458 bytes, sha256 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2, 160 verdicts, 18955 s
INFO jobs8-cold: exit 0, 77458 bytes, sha256 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2, 160 verdicts, 2721 s
INFO jobs1-warm: exit 0, 77458 bytes, sha256 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2, 160 verdicts, 18188 s
INFO jobs8-warm: exit 0, 77458 bytes, sha256 9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2, 160 verdicts, 2975 s
PASS jobs1-off: ccache wrote nothing (0 files)
PASS jobs8-off: ccache wrote nothing (0 files)
PASS jobs1-cold: 284 compilations, 74 into the empty cache (got 284, 74)
PASS jobs8-cold: 284 compilations, 74 into the empty cache (got 284, 74)
PASS jobs1-warm: all 284 compilations from the warm cache (got 284 hits, 0 misses)
PASS jobs8-warm: all 284 compilations from the warm cache (got 284 hits, 0 misses)
PASS jobs1-off: prints 160 verdict lines (got 160)
PASS jobs1-off: tallies 160 checks (got 160)
PASS <each of jobs8-off, jobs1-cold, jobs8-cold, jobs1-warm, jobs8-warm>: the exit status is jobs1-off's (0 and 0)
PASS <each>: the verdict list is jobs1-off's, byte for byte
PASS <each>: stdout is jobs1-off's, byte for byte
PASS <each>: stderr is jobs1-off's, byte for byte
PASS <each>: prints 160 verdict lines (got 160)
PASS <each>: tallies 160 checks (got 160)
38 checks: 38 PASS, 0 FAIL
```

(The `<each>` lines are 30 PASS lines printed one by one in the log; condensed here.) Six runs, one output: 77458
bytes, sha256 9fb353df..., 160 checks: 160 PASS, the same bytes main's serial arm printed under `make all` in #102
and here (before, after cold, after warm). 284 = 4 units x 71 builds (control + 70 RTL mutants; no suite build in
this test). The warm runs ran every build in new temporary directories and still missed nothing: 273 direct hits,
and 11 units answered in preprocessed mode where ccache had not stored a direct-mode entry in the cold run (ccache
skips that for sources written moments before the compile, as Verilator's are); none compiled. Serial runs 5:24
(off), 5:16 (cold), 5:03 (warm); `--jobs 8` 45-50 min each, alongside them.

## Item 4: `make all` before and after, same 16 CPUs, cold and warm cache

Unit milan-gptp104-a777-measure ran three `make all`s one after another, each `taskset -c 48-63` (the driver saw
affinity 48-63, 16 CPUs, in every run), each on its own clean clone, parent toolchain, TMPDIR in scratch,
PYTHONUNBUFFERED=1 so each line is stamped when printed (#102's timed_make.py and walls.py, no effect on any verdict).
Nothing else ran on 48-63 between them (the unit held the range throughout). The host stayed busy around it
(load average 72-82 of 128 CPUs).

| run | head | clone | CCACHE_DIR | start - end (CET) | rc |
|---|---|---|---|---|---|
| before | a64be73d | head/before | cache/before (empty; nothing uses it at a64be73d) | 16:27:21 - 17:15:36 | 0 |
| after, cold | ad06db3 | head/after-cold | cache/after, created empty | 17:15:36 - 18:02:27 | 0 |
| after, warm | 860e474 | head/w/after-warm (another path, one level deeper) | cache/after, as the cold run left it; stats zeroed | 18:02:27 - 18:49:04 | 0 |

| step | before (a64be73d) | after, cold cache | after, warm cache | cold - before | warm - before |
|---|---:|---:|---:|---:|---:|
| sub-make `tb/verilator/ucpu` | 5.2 s | 6.3 s | 5.2 s | +1.1 s | +0.0 s |
| driver `tb/verilator/parser/mutants.py` (no ccache; unchanged code) | 209.8 s | 187.7 s | 192.8 s | -22.1 s | -17.1 s |
| engine suite (build + 4 runs; after: + the order check, 2.4 s) | 306.4 s | 310.7 s | 307.6 s | +4.3 s | +1.2 s |
| driver `tb/verilator/engine/mutants.py` | 2288.6 s (0:38:09) | 2227.0 s (0:37:07) | 2205.8 s (0:36:46) | -61.7 s (-2.7 %) | -82.8 s (-3.6 %) |
| sub-make `tb/verilator/engine` | 2595.1 s | 2537.6 s | 2513.4 s | -57.4 s | -81.6 s |
| driver `tb/verilator/gaskets/mutants.py` | 28.2 s | 27.9 s | 29.7 s | -0.3 s | +1.6 s |
| driver `tb/tsngen/mutants.py` | 31.0 s | 27.8 s | 30.4 s | -3.2 s | -0.6 s |
| **whole `make all`** | **2894.8 s (0:48:15)** | **2810.6 s (0:46:51)** | **2797.1 s (0:46:37)** | **-84.2 s (-2.9 %)** | **-97.7 s (-3.4 %)** |

Full step tables: receipts/{before,after-cold,after-warm}/walls.json; logs receipts/*/make.log
(before 137633 B sha256 b7118d7e2b47b942..., after-cold 138690 B dfe5f9e89f630987..., after-warm 138793 B c1b827b3679ad710...).

ccache's own counters for the engine sub-make (the only one that uses it), receipts/*/ccache-stats.txt:

| run | compilations | direct hit | preprocessed hit | miss | cache after |
|---|---:|---:|---:|---:|---:|
| before | 0 | 0 | 0 | 0 | empty |
| after, cold | 288 | 210 | 2 | 76 | 84 files, 3088 KiB |
| after, warm (another clone path) | 288 | 214 | 73 | **1** | 89 files, 3264 KiB |

288 = 4 translation units (sim_main, verilated, verilated_threads, the model's __ALL) x 72 builds: the suite's and,
in the arm, the control's and the 70 RTL mutants' (the other 89 mutants change only the generator and reuse the
control's build). Cold: 76 misses = the suite's 4, the control's sim_main and model, and the 70 mutant models; every
other unit came from the cache within the same run. Warm, from a clone at another path: one miss, sim_main.o of the
arm's control, whose source path names the checkout; the suite build hit in direct mode (CCACHE_BASEDIR), and the
arm's other units in direct or preprocessed mode.

**What this shows.** ccache saves about 1.5 min of a 48 min `make all` (2.9 % cold, 3.4 % warm). The engine arm
is bound by simulation, not compilation: a whole engine build is about 6 s wall at `-j 4` (11.6 s CPU: sim_main 3.4,
verilated 4.8, verilated_threads 1.3, model 1.9; measured alone on 32-39), and only 71 of the arm's 160 entries
build; each entry then simulates two passes, about 2 min of one CPU. So the cache removes about 70 x 10 s of CPU
spread over 8 workers, which is what the driver's -62 s / -83 s show. The parser driver, which no change touches and
which uses no cache, moved by -22 s / -17 s between runs: differences of that size are run-to-run noise here.

## Changes

60a2e3d, item 1 (no behaviour change; `MUTATIONS` loaded from a64be73d and from 60a2e3d compare equal, 159 = 159
tuples in the same order, and `run_harness`, `stage`, `generate_image`, `build`, `_named_failure`, `edits_of`,
`default_jobs`, `jobs_arg` have identical source):
- `tb/verilator/engine/path_mutants.py` (new, 279 lines): the #85/#87/#88 table moved verbatim, byte for byte by
  script, from mutants.py's old lines 565-793, with `PARSER_EDITS`, `PATH_COPY`, `PATH_KEEP`, `PATH_APPEND` and
  `tails` (old :118-133), as `PATH_MUTATIONS` (:49); data only, like receipt_/port_/p100_mutants.py.
- `tb/verilator/engine/mutants.py`: :95 imports it, :554 splices `*PATH_MUTATIONS` exactly where the moved entries
  stood (the list's tail), so the order is unchanged; 1080 -> 839 lines (863 at the head).
- annotated: `named_verdict` :670-671 and `run_mutant` :706-707 (`say: Callable[[str], None] = print`),
  `in_list_order` :766 (`tasks: list[Callable[[], object]]) -> Iterator[object]`), `planted` :825
  (`-> Callable[[], tuple[bool, list[str]]]`); :81 `from collections.abc import Callable, Iterator`.
- documented: `control` :821, `planted` :825, `task` :827 (one-line docstrings), and `tb/mutation_jobs_test.py`
  `main` (:176, rewritten in a73258c); module docstring :62-65 points at path_mutants.py.

80d1df4, item 2:
- `tb/verilator/engine/mutants.py` :597 `compiler_env()`: OBJCACHE unset becomes `ccache` when `shutil.which("ccache")`
  finds it, else empty (a plain build); set, even empty, it is used as given (`OBJCACHE=` turns it off);
  `CCACHE_NOHASHDIR=1` unless the caller set it. :612-625 `build()` runs Verilator with `cwd=srcdir` and the RTL by
  relative name (`*RTL_SOURCES`), env `compiler_env()`. Before, the absolute staged path
  (`<tmp>/engine-mutants-XXXX/mutant-YYYY/src_<tag>/top/KL_gptp_engine.sv`) was written into the model's C++ (7
  `VL_STOP_MT`/`VL_FATAL_MT` sites), so the model never hit the cache, not even for the same mutant in the next run;
  now those strings read `top/KL_gptp_engine.sv` in every run. No harness output carries them (they print only on a
  `$stop`/fatal, and the arm prints only verdict and named FAIL lines). :25-29 docstring.
- `tb/verilator/engine/Makefile` :20-33: `OBJCACHE ?= $(if $(shell command -v ccache),ccache)`,
  `CCACHE_NOHASHDIR ?= 1`, both exported to every recipe (the suite's Verilator build and mutants.py);
  `run: export CCACHE_BASEDIR ?= $(abspath ../../..)` for the in-tree suite build only (it turns the absolute
  `-I$(CURDIR)` into a relative one, so a new checkout hits in direct mode; for the arm, whose builds run in TMPDIR,
  a base dir would only add the TMPDIR depth to the key). The cache is ccache's own (CCACHE_DIR, default
  ~/.cache/ccache), never in the tree; every measurement and test used a CCACHE_DIR in scratch.
- Checked by probe recipes (`make --eval`), receipts below: ccache on PATH -> recipes see `OBJCACHE=ccache
  CCACHE_NOHASHDIR=1`, and `run` also `CCACHE_BASEDIR=<checkout>`; ccache not on PATH -> `OBJCACHE=` (empty);
  `make OBJCACHE=` -> empty; a caller's `CCACHE_BASEDIR=/x` kept. `compiler_env()` the same four ways.
- Observed and documented, not worked around: a ccache that cannot write its cache directory compiles and then
  exits 1 (`Failed to create directory .../lock`), which fails the build; the remedy, `OBJCACHE=` or a writable
  CCACHE_DIR, is in the test guide.

a73258c, items 3 and 5b:
- `tb/mutation_jobs_test.py` (rewritten, 238 lines): `RUNS` :53 = jobs1-off, jobs8-off, jobs1-cold, jobs8-cold,
  jobs1-warm, jobs8-warm. `run_env` :80 drops every CCACHE_* and OBJCACHE of the caller, sets `OBJCACHE=` (off) or
  `ccache`, and a CCACHE_DIR of the run's own. `run_all` :129: jobs1-off and jobs1-cold start with jobs8-cold; the
  two warm caches are copies of jobs8-cold's (stats zeroed); jobs1-warm then starts, and jobs8-warm, jobs8-off
  follow (at most 3 + 8 mutants at once). Checks: every run's exit status, verdict list, stdout and stderr equal the
  reference's (jobs1-off) byte for byte (:212-216); each run prints 1 + len(MUTATIONS) verdict lines and that tally;
  `cache_checks` :153: an off run's CCACHE_DIR stays empty, a cold run misses at least once and makes as many
  compilations as jobs8-cold, a warm run makes all of them from the cache (0 misses, hits = jobs8-cold's
  compilations, > 0). Unified diff printed on any stdout mismatch.
- `tb/mutation_order_test.py` (new, 147 lines): the arm's own `main` in-process at --jobs 1 and 8 with `build`,
  `generate_image`, `run_harness` stubbed (seeded random sleep, then output failing each named check); checks exit 0,
  exactly the 160 expected `[PASS]` lines in list order, the tally, one run directory per entry, that at --jobs 8
  the entries really finished out of list order, and that both runs print the same bytes. About 4 s.
- `tb/verilator/engine/Makefile` :37 `all: run mutants-order-test mutants`; :75-83 `mutants-jobs-test` and its
  comment; :85-89 `mutants-order-test`.

ad06db3 and 860e474, item 5a and the guide:
- `docs/TEST_DEVELOPER.md` :62 "By default, up to eight engine mutants run at once." (the residue's wording, verbatim);
  :23-24, :50-51 the two tests and targets; :70-78 ccache, `OBJCACHE=`, the cache outside the tree, the unwritable
  cache failure and its remedy; :80-86 the order check in bare `make`, "takes seconds", the jobs test's six runs and
  "about seven hours on sixteen CPUs" (860e474; ad06db3 said six).

Scratch checks (not committed; tools/ in scratch):
- tools/fake/{good,badorder,nocache}: the jobs test on a 3-mutant fake driver that compiles one unit per entry
  through $OBJCACHE: good rc 0 (38/38); output differing at --jobs 8 rc 1 (3 stdout FAILs); a driver ignoring
  OBJCACHE rc 1 (cold and warm cache checks FAIL).
- neg/: `in_list_order` changed to yield in completion order: `mutants-order-test` rc 1 (list order and same-bytes
  checks FAIL).
- exp/: the plain engine build with absolute staged paths: a second build in another directory misses the model;
  with relative names it hits all 4 units; two clones: 3 of 4 hit (sim_main misses).

## Gates

Clean clones of the committed head 860e474 (scratch head/gates, head/w/after-warm, head/eq), parent toolchain, each
command's own rc (output to a file, never piped; receipts/gates/):

| gate | rc | result |
|---|---|---|
| `make all` (the after-warm run, clean clone head/w/after-warm, 48-63) | 0 | 2797.1 s; every arm's tally all PASS (parser 35, engine 160, gaskets 5, tsngen 4), order check 10/10, contract, lint, docs PASS; clone clean afterwards |
| `make contract` | 0 | PHC interface contract: PASS |
| `make docs` | 0 | docs check PASS (14 current, 18 historical pages), docs selftest PASS (127 arms), source evidence PASS (20 exact) + selftest PASS (7 arms), diagrams |
| `make diagrams-check` | 0 | diagram check PASS (9 pinned assets, 3 source-bound PNGs), diagram selftest PASS (10 arms) |
| `make lint` | 0 | engine lint + bench/arty lint |
| `python3 scripts/check_docs.py --selftest` | 0 | PASS (127 arms) |
| `python3 scripts/check_source_evidence.py --selftest` | 0 | PASS (7 arms) |
| `python3 scripts/generate_diagrams.py --selftest` | 0 | PASS (10 arms) |
| `python3 syn/ooc/check_ooc_clock.py --selftest` | 0 | PASS (30 arms) |
| `make -C tb/verilator/engine mutants-order-test` | 0 | 10 checks: 10 PASS (also inside `make all`) |
| `make -C tb/verilator/engine mutants-jobs-test` (head/eq, 80-95) | 0 | 38 checks: 38 PASS; six runs identical, 77458 bytes, sha256 9fb353df... |
| parent `scripts/check_py_idiom.py` (parent dev clone, gptp-processor at 860e474) | 0 | every ratchet at or under budget (above) |
| parent `scripts/check_cpp_idiom.py` (same clone) | 0 | every count 0 |

Not run: `make ooc`'s Vivado synthesis (`syn/ooc/run.sh`): not part of `all`, not named as a gate in the docs, and the
diff touches no hdl/, syn/ or ROM file; its selftest is above. The lane holds no untracked or ignored file.
