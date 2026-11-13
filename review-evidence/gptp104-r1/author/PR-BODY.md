[A777]

Closes #104

Follow-up to #102 / #103. The parallel engine mutation arm now passes the parent repository's Python idiom gate,
and the engine's Verilator builds compile through ccache when it is on PATH. No mutant, check, verdict rule or
tally is removed, merged or weakened: the arm's 159 mutants are the same tuples in the same order, and every run
below prints exactly what main's arm prints (77458 bytes, sha256 9fb353df86cecf91..., 160 checks: 160 PASS).

## Required items

1. **Parent idiom gate.** The four public functions are annotated (`named_verdict`, `run_mutant`, `in_list_order`,
   `planted`), the four undocumented ones documented (`control`, `planted`, `task`, `tb/mutation_jobs_test.py`'s
   `main`), and `tb/verilator/engine/mutants.py` is 863 lines (was 1080): the #85/#87/#88 table moved verbatim into
   `tb/verilator/engine/path_mutants.py` and is spliced back where it stood, like the three tables already split out.
   On a parent `dev` clone whose `gptp-processor` sits at this head, `scripts/check_py_idiom.py` and
   `scripts/check_cpp_idiom.py` both exit 0 with no ratchet or scope edit (`long module 10 <= 10`,
   `unannotated public function 0 <= 0`, `undocumented public function 0 <= 0`). At main the Python gate exits 1 on
   exactly those three ratchets.
2. **ccache.** `OBJCACHE` (verilated.mk's own variable) becomes `ccache` only when `ccache` is on PATH, in the
   engine Makefile and in `mutants.py` (`compiler_env`); plain builds otherwise. `OBJCACHE=` turns it off; the test
   guide documents it. Build paths stay out of the key. The arm hands Verilator the staged RTL by relative name, so
   no temporary directory is written into the model's C++. Before, the absolute staged path was, so a mutant's model
   could never hit, not even in the next run. `CCACHE_NOHASHDIR=1` keeps the build directory out, and the in-tree
   suite build sets `CCACHE_BASEDIR` to the checkout. A caller's own CCACHE_* settings win. The cache is ccache's own
   directory, never the tree. A ccache that cannot write its cache fails the build; the guide gives the remedy.
3. **Verdicts unchanged.** `make -C tb/verilator/engine mutants-jobs-test` runs the arm six times, `--jobs 1` and
   `--jobs 8`, each with ccache off, cold and warm. It compares exit status, verdict list, stdout and stderr with the
   uncached `--jobs 1` run byte for byte, and checks each run's verdict count and tally. It also checks that each
   cache is what its run is called: an off run leaves its cache empty, a cold run compiles into an empty cache, and a
   warm run takes every compilation from the cache although every build runs in new temporary directories. Result
   at this head: 38 checks: 38 PASS. All six runs printed the same 77458 bytes, and the warm runs took all 284
   compilations from the cache with 0 misses.
4. **Measured** on the same 16 CPUs, one run after another, each on a clean clone:

   | `make all` | wall | engine driver | ccache hits / misses |
   |---|---:|---:|---:|
   | before (main a64be73d) | 2894.8 s (0:48:15) | 2288.6 s | not used |
   | after, cold cache | 2810.6 s (0:46:51), -2.9 % | 2227.0 s | 212 / 76 |
   | after, warm cache, clone at another path | 2797.1 s (0:46:37), -3.4 % | 2205.8 s | 287 / 1 |

   The gain is small, and that is the finding: the arm is bound by simulation. A whole engine build is about 6 s of
   wall time. Only 71 of the 160 entries build (89 mutants change only the ROM generator and reuse the control's
   build), and each entry then simulates for about two minutes. Run-to-run noise is of the same order: the parser
   arm, untouched and uncached, moved by about 20 s between runs. The warm run's one miss is the harness compiled
   from the new checkout's path. The suite build hit through `CCACHE_BASEDIR`.
5. **#103 residue.** `docs/TEST_DEVELOPER.md:62` reads "By default, up to eight engine mutants run at once." The
   optional fast list-order check is in: `tb/mutation_order_test.py`, run by the engine's `all` (so by `make all`) as
   `mutants-order-test`. It runs the arm's own `main` at `--jobs 1` and `--jobs 8`, with stubbed builds and harness
   runs that finish out of list order, and takes about 4 s. The test guide states both tests' runtimes.

## Gates

On clean clones of this head, each command's own exit status, all rc 0: `make all` (the warm measurement run),
`make contract`, `make docs`, `make diagrams-check`, `make lint`, `scripts/check_docs.py --selftest` (127 arms),
`scripts/check_source_evidence.py --selftest` (7 arms), `scripts/generate_diagrams.py --selftest` (10 arms),
`syn/ooc/check_ooc_clock.py --selftest` (30 arms), `make -C tb/verilator/engine mutants-order-test` (10/10),
`make -C tb/verilator/engine mutants-jobs-test` (38/38). The diff touches no `hdl/`, `syn/` or ROM file.

The guide gives the jobs test as about seven hours on sixteen CPUs: that was its pace on a loaded host. The final
run took 5 h 48 min on a nearly idle one.
