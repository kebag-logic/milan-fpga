#!/usr/bin/env python3
"""Run the unmodified parent `cflags_missing` against PP tb Makefiles.

usage: probe_cflags.py PARENT_SCRIPTS_DIR PP_CLONE BASE_REV HEAD_REV

PARENT_SCRIPTS_DIR holds the parent's check_cpp_idiom.py and
code_quality_scope.py fetched byte-exact from the parent repository.
Everything under test is read from git objects of PP_CLONE, so the working
tree is never touched. Exit 0 only when every expectation holds.
"""
import hashlib
import subprocess
import sys

scripts, clone, base, head = sys.argv[1:5]
sys.path.insert(0, scripts)
import check_cpp_idiom as cci  # noqa: E402  (the real, unmodified checker)

TARGET = "tb/pp_top/Makefile"
FIX_OLD = '-CFLAGS "-DPP_TOP_SRP_DOM_DEF_VID=0x$(SRP_VID_FIXTURE) -Wall -Wextra"'


def show(rev, path):
    return subprocess.run(["git", "-C", clone, "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout


def ls(rev):
    out = subprocess.run(["git", "-C", clone, "ls-tree", "-r", "--name-only", rev],
                         capture_output=True, text=True, check=True).stdout
    return out.splitlines()


fails = 0


def expect(label, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'}: {label}: got {got!r} want {want!r}")


print("checker sha256", hashlib.sha256(open(f"{scripts}/check_cpp_idiom.py", "rb").read()).hexdigest())
print("WARNING_FLAGS", cci.WARNING_FLAGS)
print("CFLAGS_RE", cci.CFLAGS_RE.pattern)

base_text, head_text = show(base, TARGET), show(head, TARGET)
print("groups@base", cci.CFLAGS_RE.findall(base_text))
print("groups@head", cci.CFLAGS_RE.findall(head_text))
expect("base pp_top", cci.cflags_missing(base_text), ["-Wall", "-Wextra"])
expect("head pp_top", cci.cflags_missing(head_text), [])

assert head_text.count(FIX_OLD) == 1, "fixture group not found exactly once"
for drop, want in ((" -Wall", ["-Wall"]), (" -Wextra", ["-Wextra"]),
                   (" -Wall -Wextra", ["-Wall", "-Wextra"])):
    mutated = head_text.replace(FIX_OLD, FIX_OLD.replace(drop, "", 1), 1)
    assert mutated != head_text
    expect(f"head minus{drop} in fixture group", cci.cflags_missing(mutated), want)

# Also drop each flag from the COMMON group only: the fixture group must not
# mask a regression in the other group.
COMMON = '-CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"'
assert head_text.count(COMMON) == 1
for drop, want in ((" -Wall", ["-Wall"]), (" -Wextra", ["-Wextra"])):
    mutated = head_text.replace(COMMON, COMMON.replace(drop, "", 1), 1)
    expect(f"head minus{drop} in common group", cci.cflags_missing(mutated), want)

# Project-wide view as the parent sees PP: every tracked Makefile whose
# parent-rooted path contains /tb/ (checker's testbench_makefiles filter).
for rev, label in ((base, "base"), (head, "head")):
    pop = [p for p in ls(rev)
           if (p == "Makefile" or p.endswith("/Makefile"))
           and "/tb/" in f"/protocol-processor/{p}"]
    bad = [(p, cci.cflags_missing(show(rev, p))) for p in pop]
    bad = [(p, m) for p, m in bad if m]
    print(f"PP testbench Makefiles@{label}: {len(pop)}; missing flags: {bad}")
    expect(f"PP build-without-warnings count@{label}", len(bad),
           1 if label == "base" else 0)

print(f"RESULT: {'PASS' if fails == 0 else 'FAIL'} ({fails} failing expectations)")
sys.exit(1 if fails else 0)
