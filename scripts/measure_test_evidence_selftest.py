#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Fixture arms for ``measure_test_evidence.py`` - one arm per idiom it reads.

This is the ``--selftest`` half of the Rule 8 measurement, kept beside it
rather than inside it: the arms are one long list of independent fixtures and
they share no reader with the rules they exercise. Run them through the
measurement, which is the only supported entry point:

    python3 scripts/measure_test_evidence.py --selftest

``run_arms()`` prints one line per arm in the order the groups below are
called, then the totals, and returns the exit code. Adding an arm to the END
of its group is what keeps the printed transcript stable.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from measure_test_evidence import (  # noqa: E402
    REPO,
    arms,
    audit,
    draws_without_seed,
    make_invocations,
    reads_dut_source,
    runner_contract,
    seed_population,
    suite_tally,
    uses_wall_clock,
)


class _Tally:
    """The self-test's running verdict: one line per arm, and the totals."""

    def __init__(self):
        self.total = 0
        self.failures = 0

    def ck(self, name: str, ok: bool, detail: str = "") -> None:
        """Record and print one arm's verdict, with its detail when it fails."""
        self.total += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            self.failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")


def _arms_mutation_classification(ck, driver, default):
    """Section 1: what makes a target's recipe an executed mutation arm."""
    # -- 1. an arm is what the entry executes --------------------------------
    ck("a reachable target running a mutation driver is armed",
       bool(arms("all: run mutants\nrun:\n\t./sim\nmutants:\n\tpython3 mutants.py\n",
                 default, {"mutants.py": driver})))
    ck("the driver may be reached through a make variable ($(PY) x.py)",
       bool(arms("PY ?= python3\nall: graderself\ngraderself:\n\t@$(PY) test_grade_tx.py\n",
                 default, {"test_grade_tx.py": "def mutation_checks(t):\n    pass\n"})))
    ck("a driver on a target the entry never runs is not an arm",
       not arms("run:\n\t./sim\nfigures:\n\tpython3 $(CURDIR)/measure_figures.py --check\n",
                default, {"measure_figures.py": driver}))
    ck("...until the processor's CI names that target",
       bool(arms("run:\n\t./sim\nfigures:\n\tpython3 $(CURDIR)/measure_figures.py --check\n",
                 {"", "figures"}, {"measure_figures.py": driver})))
    ck("a compile-time mutation define a recipe passes is armed",
       bool(arms("all: obj_mut/V\nobj_mut/V:\n\tverilator +define+NVM_MUT_MAP_ALIAS x.sv\n",
                 default, {})))
    ck("a mutation define reaches the recipe through variable expansion",
       bool(arms("MUTFLAGS = -DCORE_MUTANT_1\nall:\n\tg++ $(MUTFLAGS) x.cpp\n", default, {})))
    ck("a negative-case table the recipe consumes is armed",
       bool(arms("NEG_CASES = W=32 N=0\nall: negative\nnegative:\n\tfor c in $(NEG_CASES); do "
                 "$(V) -G$$c; done\n", default, {})))
    ck("a DUT-rewriting driver with no table is still a driver",
       bool(arms("all: run neg\nrun:\n\t./sim\nneg: run\n\tpython3 binding_mutant.py\n", default,
                 {"binding_mutant.py": 'FILTER = HERE / "../../../hdl/f.sv"\n'
                  'src = FILTER.read_text()\nout.write_text(src.replace(A, B))\n'})))
    ck("a DUT reader that rewrites nothing is not a driver",
       not arms("all:\n\tpython3 check.py\n", default,
                {"check.py": 'src = open("../hdl/x.sv").read()\nassert "port" in src\n'}))
    ck("(A) a suite whose entry runs nothing is not armed",
       not arms("all:\n\t@true\n# no mutant or negative arm here\n", default, {}))
    ck("(B) a comment naming mutants.py is not an arm",
       not arms("# TODO: write a mutants.py like tcam\nall:\n\t./sim\n", default,
                {"mutants.py": driver}))
    ck("(C) an unrelated -DUSE_MUTEX define is not an arm, even when passed",
       not arms("CFLAGS += -DUSE_MUTEX\nall:\n\tg++ $(CFLAGS) x.cpp\n", default, {}))
    ck("(D) an empty mutants: target is not an arm",
       not arms("all: mutants\nmutants:\n\t@true\n", default, {"mutants.py": driver}))
    ck("(E) README prose about a negative arm is not an arm",
       not arms("all:\n\t./sim\n", default,
                {"README.md": "Negative: none of the checks has a negative arm yet.\n"
                              "MUTATIONS = see above\n"}))
    ck("(F) a comment mentioning --selftest is not an arm",
       not arms("# run with --selftest to see the fixtures\nall:\n\t./sim\n", default, {}))
    ck("a driver named as an echo argument is not run, so not an arm",
       not arms("all:\n\t@echo mutants.py\n", default, {"mutants.py": driver}))
    ck("a table variable nobody's recipe consumes is not an arm",
       not arms("NEG_CASES = W=32\nall:\n\t./sim\n", default, {}))
    ck("mutation prose alone is not an executable arm",
       not arms("all:\n\t./sim\n# the mutation was run by hand and failed\n", default, {}))
    ck("a comment marker inside the driver does not make it one",
       not arms("all:\n\tpython3 x.py\n", default, {"x.py": "# MUTATIONS = none yet\nrun()\n"}))


def _arms_error_control(ck, driver, default):
    """Section 1, continued: a driver failure Make never sees is not evidence."""
    # -- error control: a failure Make never sees is not evidence -------------
    mut = {"mutants.py": driver}
    ck("(G) a `-` recipe line ignores errors: `-python3 mutants.py` is not an arm",
       not arms("all: mutants\nmutants:\n\t-python3 mutants.py\n", default, mut)
       and not arms("all:\n\t-verilator +define+NVM_MUT_MAP_ALIAS x.sv\n", default, {}))
    ck("(H) `python3 mutants.py || true` is not an arm: the fallback masks the driver",
       not arms("all: mutants\nmutants:\n\tpython3 mutants.py || true\n", default, mut))
    ck("`|| :` and `|| echo ...` mask the same way",
       not arms("all:\n\tpython3 mutants.py || :\n", default, mut)
       and not arms("all:\n\tpython3 mutants.py || echo 'mutants failed'\n", default, mut))
    ck("a `-` on another line of the same target leaves the driver's line evidence",
       arms("all: mutants\nmutants:\n\t-rm -rf obj_mut\n\tpython3 mutants.py\n", default, mut)
       == [("mutants", "driver", "mutants.py")])
    ck("an && chain carries the driver's failure, so it still counts",
       bool(arms("all:\n\t./sim && python3 mutants.py && echo ok\n", default, mut)))
    ck("`@-` and `-@` are both the ignore prefix, before and after expansion",
       not arms("all:\n\t@-python3 mutants.py\n", default, mut)
       and not arms("all:\n\t-@python3 mutants.py\n", default, mut)
       and not arms("Q = -\nall:\n\t$(Q)python3 mutants.py\n", default, mut))
    ck("a `; true` tail masks; `set -e` restores the driver's failure, `set +e` drops it",
       not arms("all:\n\tpython3 mutants.py; true\n", default, mut)
       and bool(arms("all:\n\tset -e; python3 mutants.py; rm -rf obj_mut\n", default, mut))
       and not arms("all:\n\tset -e; set +e; python3 mutants.py; rm -rf obj_mut\n", default, mut))
    ck("a driver feeding a pipe reports the consumer's status, not its own",
       not arms("all:\n\tpython3 mutants.py | tee mutants.log\n", default, mut))
    ck("a fallback that re-raises (`|| exit 1`, `|| { ...; exit 1; }`) still counts",
       bool(arms("all:\n\tpython3 mutants.py || exit 1\n", default, mut))
       and bool(arms("all:\n\tpython3 mutants.py || { echo FAIL; exit 1; }\n", default, mut))
       and not arms("all:\n\tpython3 mutants.py || { echo FAIL; exit 0; }\n", default, mut))
    ck("an if condition, a $$(...) and a backtick substitution are not arms",
       not arms("all:\n\tif python3 mutants.py; then echo ok; fi\n", default, mut)
       and not arms("all:\n\techo $$(python3 mutants.py)\n", default, mut)
       and not arms("all:\n\techo `python3 mutants.py`\n", default, mut))
    ck(".IGNORE makes a target's, or every, recipe non-evidence",
       not arms(".IGNORE: mutants\nall: mutants\nmutants:\n\tpython3 mutants.py\n", default, mut)
       and not arms(".IGNORE:\nall:\n\tpython3 mutants.py\n", default, mut)
       and bool(arms(".IGNORE: clean\nall:\n\tpython3 mutants.py\n", default, mut)))
    calls = make_invocations('for d in tb/*/; do\n  if (cd "$d" && make) >"$log" 2>&1; then\n'
                             'make -C tb/nvm_port figures\n$(MAKE) -C tb/verilator/ucpu\n')
    ck("the entry reader sees the loop, the named target and the sub-make",
       calls == [("$d", []), ("tb/nvm_port", ["figures"]), ("tb/verilator/ucpu", [])], str(calls))


def _arms_replayable_randomness(ck):
    """Section 2: one arm per draw idiom, in each language, seeded or not."""
    # -- 2. replayable randomness, one arm per idiom ----------------------
    ck("an unseeded draw is caught", draws_without_seed("x = random.choice([1,2])"))
    ck("a seeded draw is not", not draws_without_seed("random.seed(11)\nx = random.choice([1,2])"))
    ck("a Random(seed) instance counts as seeded",
       not draws_without_seed("rng = random.Random(13)\nx = rng.choice([1,2])"))
    ck("the guide's TEST_SEED pattern is clean",
       not draws_without_seed('seed = int(os.environ.get("TEST_SEED", "23"))\n'
                              'print(f"TEST_SEED={seed}")\nrng = random.Random(seed)\n'
                              'frame = bytes(rng.randrange(256) for _ in range(64))\n'))
    ck("an unseeded random.Random() instance draw is caught",
       draws_without_seed("_rng = random.Random()\n_probe = _rng.randint(0, 9)\n"))
    ck("a SystemRandom draw is caught (it cannot be seeded)",
       draws_without_seed("g = random.SystemRandom()\nx = g.random()\n"))
    ck("from random import randint is caught",
       draws_without_seed("from random import randint\nx = randint(0, 9)\n"))
    ck("...and seeded through seed() is not",
       not draws_without_seed("from random import randint, seed\nseed(7)\nx = randint(0, 9)\n"))
    ck("random.choices and random.gauss are draws",
       draws_without_seed("a = random.choices(p, k=2)\n") and draws_without_seed("b = random.gauss(0, 1)\n"))
    ck("np.random draws are caught",
       draws_without_seed("import numpy as np\n_probe = np.random.randint(0, 9)\n"))
    ck("...and np.random.seed / default_rng(seed) make them replayable",
       not draws_without_seed("np.random.seed(3)\nx = np.random.randint(0, 9)\n")
       and not draws_without_seed("g = np.random.default_rng(7)\n")
       and draws_without_seed("g = np.random.default_rng()\n"))
    ck("secrets.randbelow is a draw that can never be seeded",
       draws_without_seed("import secrets\nx = secrets.randbelow(10)\n"))
    ck("secrets.token_hex is a nonce, not a draw (known limit)",
       not draws_without_seed("name = f'ci-{secrets.token_hex(16)}'\n"))
    ck("a file that never draws is not counted", not draws_without_seed("x = 1"))
    ck("a C rand() with no srand is caught", draws_without_seed("int x = rand();", ".cpp"))
    ck("a C rand() with srand is not", not draws_without_seed("srand(7); int x = rand();", ".cpp"))
    ck("std::rand() is caught", draws_without_seed("static int p = std::rand();", ".cpp"))
    ck("srand(time(NULL)) is not a recorded seed",
       draws_without_seed("srand(time(NULL)); int x = rand();", ".cpp"))
    ck("mt19937(random_device) is caught",
       draws_without_seed("std::mt19937 _g(std::random_device{}()); int x = _g();", ".cpp"))
    ck("...unless the seed it produced is recorded",
       not draws_without_seed('unsigned seed = std::random_device{}(); printf("seed=%u\\n", seed);'
                              ' std::mt19937 g(seed);', ".cpp"))
    ck("a literally seeded engine is deterministic",
       not draws_without_seed("std::mt19937 rng(0xC0FFEE); int x = rng();", ".cpp"))
    ck("$urandom with no seed is caught", draws_without_seed("a = $urandom;", ".sv"))
    ck("$urandom_range and $random are caught",
       draws_without_seed("a = $urandom_range(0, 7);", ".sv") and draws_without_seed("b = $random;", ".sv"))
    ck("randomize() is a draw", draws_without_seed("if (!pkt.randomize()) $error;", ".svh"))
    ck("srandom(seed) makes SystemVerilog draws replayable",
       not draws_without_seed("initial begin $display(seed); process::self().srandom(seed);"
                              " a = $urandom; end", ".sv"))
    ck("$urandom(seed) is a seeded draw",
       not draws_without_seed("a = $urandom(seed); b = $urandom_range(0, 7);", ".sv"))
    ck("a +seed plusarg records the seed",
       not draws_without_seed('if (!$value$plusargs("seed=%d", seed)) seed = 1; a = $urandom;', ".sv"))
    ck("a draw in a comment is not a draw",
       not draws_without_seed("// calls rand() nowhere\nint x = 1;", ".cpp")
       and not draws_without_seed("# random.randint(0, 9) would be wrong here\nx = 1\n"))
    ck("a draw inside a string literal is not a draw",
       not draws_without_seed('msg = "x = random.randint(0, 9)"\n'))
    population = seed_population()
    ck("a depth-1 file of each tb/tests root is in the seed population",
       "gptp-processor/tb/check_phc_contract.py" in population
       and "tests/environment.py" in population, f"{len(population)} files")
    ck("SystemVerilog under tb/ is in the seed population",
       any(rel.endswith(".sv") for rel in population))


def _arms_dut_source_oracles(ck):
    """Section 3: one arm per idiom that reads the DUT's own source."""
    # -- 3. DUT-source oracles, one arm per idiom ------------------------
    ck("a test reading an HDL source is an oracle-review candidate",
       reads_dut_source('RTL = ROOT / "hdl/block.sv"\nsrc = RTL.read_text()'))
    ck("open(...hdl...).read() is a reader",
       reads_dut_source('_s = open("../../hdl/packet_engine/KL_pp_nvm_port.sv").read()\n'))
    ck("readlines() over an hdl path is a reader",
       reads_dut_source('lines = open(RTL_PATH).readlines()\nRTL_PATH = "../hdl/x.sv"\n'))
    ck("a C++ ifstream over an hdl path is a reader",
       reads_dut_source('std::ifstream f("../../hdl/x.sv");', ".cpp"))
    ck("an SV `include of production HDL is a reader",
       reads_dut_source('`include "../../hdl/pkg/x_pkg.svh"', ".sv"))
    ck("a Makefile grep over $(RTL_DIR) is a reader",
       reads_dut_source("check:\n\tgrep -c localparam $(RTL_DIR)/x.sv\n", ""))
    ck("a package import is a binding, not a reader (known limit)",
       not reads_dut_source("import x_pkg::*;\nmodule wrap;\nendmodule\n", ".sv"))
    ck("an ordinary behavioral harness is not a source-reader candidate",
       not reads_dut_source("expect(got, 7);", ".cpp"))
    ck("a reader mentioned only in a comment is not one",
       not reads_dut_source('# src = open("../hdl/x.sv").read()\nx = 1\n'))


def _arms_wall_clock(ck):
    """Section 4: one arm per host-clock, sleep and deadline idiom."""
    # -- 4. wall-clock dependence, one arm per idiom ---------------------
    ck("host sleep is wall-clock dependent", uses_wall_clock("time.sleep(0.02)"))
    ck("a cycle timeout is deterministic",
       not uses_wall_clock("for (int timeout_cycles = 0; timeout_cycles < 32; ++timeout_cycles) tick();", ".cpp"))
    ck("an int named timeout is not a deadline", not uses_wall_clock("int timeout = 100;", ".cpp"))
    ck("std::chrono is a host clock", uses_wall_clock("auto t = std::chrono::steady_clock::now();", ".cpp"))
    ck("clock() and usleep() are host time",
       uses_wall_clock("double t = clock();", ".cpp") and uses_wall_clock("usleep(1000);", ".cpp"))
    ck("check_output(..., timeout=) is a process deadline",
       uses_wall_clock('subprocess.check_output(["true"], timeout=5)'))
    ck("a timeout keyword after a nested call is still seen",
       uses_wall_clock("subprocess.run(build(x), timeout=30)"))
    ck("communicate(timeout=) and select.select are deadlines",
       uses_wall_clock("out, _ = p.communicate(timeout=10)") and uses_wall_clock("select.select([s], [], [], 1)"))
    ck("asyncio.wait_for(..., timeout=) is a deadline; a cycle-bounded wait_for is not",
       uses_wall_clock("await asyncio.wait_for(evt.wait(), timeout=2)")
       and not uses_wall_clock("wait_for(dut, done, 200);", ".cpp"))
    ck("SO_RCVTIMEO is a socket deadline", uses_wall_clock("s.setsockopt(SOL_SOCKET, SO_RCVTIMEO, tv)"))
    ck("a shell sleep and a Makefile timeout are host time",
       uses_wall_clock("sleep 2\n", ".sh") and uses_wall_clock("run:\n\ttimeout 60 ./obj_dir/Vsim\n", ""))
    ck("a comment about sleeping is not host time", not uses_wall_clock("# time.sleep(1) removed\n"))


def _arms_tally_evidence(ck):
    """The tally reader: a zero tally is NOCOUNT and a [FAIL] line contradicts it."""
    # -- tally evidence: the superproject reader refuses the processor shapes
    scan, nocount = suite_tally.scan, suite_tally.is_nocount
    c, f, matched, _u, skipped = scan("0 checks: 0 PASS, 0 FAIL\n")
    ck("a zero tally is NOCOUNT, not a pass", nocount(c, f, matched, skipped))
    ck("every tally line is summed, not only the last",
       scan("12 checks: 12 PASS, 0 FAIL\n3 checks: 3 PASS, 0 FAIL\n")[0] == 15)
    ck("both processor tally shapes are read",
       scan("checks: 19   failures: 0\n")[0] == 19 and scan("== co-sim: 42 pass, 0 fail ==\n")[0] == 42)
    ck("a [FAIL] line contradicts a green exit",
       suite_tally.log_reports_failure("  [FAIL] priority   got=1 exp=0\n")[1])


def _arms_runner_contract(ck):
    """The live runner still preserves its timeout and tally verdicts."""
    runner = (REPO / "scripts/run_all_suites.sh").read_text()
    ck("the live runner preserves timeout and tally verdicts",
       not runner_contract(runner), "; ".join(runner_contract(runner)))
    ck("a timeout reported as failure is rejected",
       bool(runner_contract(runner.replace("exit 92", "exit 1"))))


def _arms_live_scan(ck):
    """The live audit: the scan sees the suites and both sides of every split."""
    armed, unarmed, unseeded, readers, unexplained, stale, wallclock = audit()
    ck("the live scan sees the suites", len(armed) + len(unarmed) > 40,
       f"{len(armed) + len(unarmed)} suites")
    ck("both sides of the mutation split are non-empty",
       bool(armed) and bool(unarmed),
       "an inert classifier would put every suite on one side")
    ck("every live arm sits on a target the entry executes",
       all(found for found in armed.values()))
    ck("every DUT-source reader has a current disposition",
       not unexplained and not stale, f"unexplained={unexplained}, stale={stale}")


def run_arms() -> int:
    """Run every arm, print the transcript, and return the exit code."""
    tally = _Tally()
    ck = tally.ck
    driver = ("MUTATIONS = [\n  ('x', 'a', 'b'),\n]\n"
              "def main():\n    return 0\n")
    default = {""}
    _arms_mutation_classification(ck, driver, default)
    _arms_error_control(ck, driver, default)
    _arms_replayable_randomness(ck)
    _arms_dut_source_oracles(ck)
    _arms_wall_clock(ck)
    _arms_tally_evidence(ck)
    _arms_runner_contract(ck)
    _arms_live_scan(ck)
    print(f"\n{tally.total} checks: {tally.total - tally.failures} PASS, "
          f"{tally.failures} FAIL")
    return 1 if tally.failures else 0
