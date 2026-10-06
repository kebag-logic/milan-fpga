#!/usr/bin/env python3
"""Focused follow-up probes for newly published review findings; copies only."""
import argparse
from pathlib import Path
import resource
import shlex
import subprocess
import sys
p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
a = p.parse_args()
repo = a.repo.resolve()
work = Path(__file__).resolve().parent / "scratch/public-findings"
work.mkdir(parents=True, exist_ok=True)
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
def run(cmd):
    return subprocess.run([str(x) for x in cmd], cwd=work, capture_output=True, text=True)
port = repo / "sw/firmware/ctrl/port"
probe = work / "pool.c"
probe.write_text(r'''#include "ctrl_pool.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
int main(void) {
    union { max_align_t alignment; unsigned char bytes[512]; } arena;
    struct ctrl_pool p;
    const struct ctrl_pool_class c = {32, 2};
    assert(ctrl_pool_init(&p, arena.bytes, sizeof arena.bytes, &c, 1));
    void *a = ctrl_pool_alloc(&p, 32), *b = ctrl_pool_alloc(&p, 32);
    assert(a && b);
    ctrl_pool_free(&p, a); ctrl_pool_free(&p, b);
    void *null = NULL;
    memcpy(b, &null, sizeof null); /* client corrupts a block after release */
    assert(ctrl_pool_alloc(&p, 32) == b);
    void *last = ctrl_pool_alloc(&p, 32);
    printf("Corrupted released block: refused=%u, free_count=%u, null=%d\n",
           p.refused, p.bins[0].free_count, last == NULL);
    assert(last == NULL && p.refused == 1 && p.bins[0].free_count == 1);
    return 0;
}
''')
original = (port / "ctrl_pool.c").read_text()
needle = " && bin->free_head != NULL"
assert original.count(needle) == 1
mutant = work / "pool-mutant.c"
mutant.write_text(original.replace(needle, ""))
for tag, source in (("guard", port / "ctrl_pool.c"), ("unguarded", mutant)):
    exe = work / tag
    built = run(["gcc", "-std=c11", "-O0", "-I" + str(port), probe, source, "-o", exe])
    assert built.returncode == 0, built.stderr
    result = run([exe])
    print(tag, "exit", result.returncode, result.stdout.strip())
    assert result.returncode == (0 if tag == "guard" else -11)

harness = repo / "sw/firmware/gtest"
main = (harness / "fw_gtest_main.cpp").read_text()
needle = "info.result()->Failed() || info.result()->Skipped()"
assert main.count(needle) == 1
planted = work / "skip-not-counted.cpp"
planted.write_text(main.replace(needle, "info.result()->Failed()"))
flags = shlex.split(subprocess.check_output(["pkg-config", "--cflags", "--libs", "gtest", "gmock"], text=True))
exe = work / "tally-mutant"
built = run(["g++", "-std=c++20", "-O0", "-I" + str(harness), planted, harness / "tally_cases.cpp", *flags, "-o", exe])
assert built.returncode == 0, built.stderr
print("\nMutated skipped test raw output:")
result = run([exe, "--gtest_filter=Skip.*"])
print(result.stdout)
assert "checks: 1   failures: 0" in result.stdout and "RESULT: PASS" in result.stdout
sys.path.insert(0, str(harness))
import tally_selftest
found = []
for case in tally_selftest.CASES:
    found.extend(tally_selftest.grade_case(case, exe, work))
print("Unchanged tally self-test findings for skip-not-counted mutant:", found)
assert not found
print("REPRODUCED: released-block corruption reaches the pool guard; false skip tally survives all eleven self-test cases.")
