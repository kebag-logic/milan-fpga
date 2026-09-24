#!/usr/bin/env python3
"""Rule 11 (parent C/C++ idiom gate) measurement of the processor's tb/ C++ at
two commits, using the parent's own checker module unchanged.

usage: idiom_scan.py CLONE CHECKER_PY COMMIT [COMMIT ...]

CHECKER_PY is the parent's scripts/check_cpp_idiom.py (fetched at the parent
dev commit). Its `code_quality_scope` import is satisfied by a stub that names
the processor submodule; nothing else of the parent is needed. Each commit's
blobs are read with `git show`, so the clone's worktree is never touched.
Prints per-key totals, every long-function site, and the length of every
function in tb/srp_stream_fsms/sim_main.cpp (limit 0 = list all).
"""
import importlib.util
import subprocess
import sys
import tempfile
import types
from pathlib import Path

SUFFIXES = (".c", ".cpp", ".cc", ".cxx", ".h", ".hpp")
FOCUS = "tb/srp_stream_fsms/sim_main.cpp"


def load_checker(path: str):
    stub = types.ModuleType("code_quality_scope")
    stub.PROJECT_SUBMODULES = ("protocol-processor",)
    stub.tracked = lambda *a, **k: []
    sys.modules["code_quality_scope"] = stub
    spec = importlib.util.spec_from_file_location("check_cpp_idiom", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(clone: str, *args: str) -> str:
    return subprocess.run(["git", "-C", clone, *args], check=True,
                          capture_output=True, text=True).stdout


def main() -> int:
    clone, checker_py, commits = sys.argv[1], sys.argv[2], sys.argv[3:]
    ck = load_checker(checker_py)
    print(f"checker LONG_FUNCTION_LINES = {ck.LONG_FUNCTION_LINES}")
    rc = 0
    for commit in commits:
        files = [p for p in git(clone, "ls-tree", "-r", "--name-only", commit,
                                "--", "tb").splitlines() if p.endswith(SUFFIXES)]
        totals: dict[str, int] = {}
        long_sites = []
        for rel in files:
            text = git(clone, "show", f"{commit}:{rel}")
            counts = ck.scan(text, "protocol-processor/" + rel)
            for key, value in counts.items():
                totals[key] = totals.get(key, 0) + value
            for n, desc in ck.sites(text, "long function", "protocol-processor/" + rel):
                long_sites.append(f"{rel}:{n} {desc}")
        print(f"== {commit} ({len(files)} C/C++ files under tb/)")
        for key in sorted(totals):
            print(f"  {key:30s} = {totals[key]}")
        for site in long_sites:
            print(f"  LONG {site}")
        if totals.get("long function", 0):
            rc = 1
        focus = ck.blank_non_code(git(clone, "show", f"{commit}:{FOCUS}"))
        lengths = ck.long_functions(focus, limit=0)
        raw = git(clone, "show", f"{commit}:{FOCUS}").splitlines()
        print(f"  {FOCUS}: {len(lengths)} functions, max {max(l for _, l in lengths)} lines")
        for n, length in lengths:
            if "listener_failure_change" in raw[n - 1] or length > 80:
                print(f"    {FOCUS}:{n} {length} lines: {raw[n - 1].strip()[:90]}")
    print(f"long-function sites present in some listed commit: {'yes' if rc else 'no'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
