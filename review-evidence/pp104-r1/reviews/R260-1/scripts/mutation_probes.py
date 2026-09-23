#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe: kill matrix of tb/pp_top/test_fixture_guards.py against
disposable mutants of fixture_guards.py, at BASE and at HEAD.

Usage: mutation_probes.py PP_BASE_CHECKOUT PP_HEAD_CHECKOUT WORKDIR

Each mutant is one exact text replacement that must match exactly once. The
two tb/pp_top Python files are copied into WORKDIR/<rev>/<mutant>/ and
`python3 -B -m unittest test_fixture_guards.py` runs there; the checkouts are
never written. "killed" = the unit test fails. Each mutant names the clause of
the new test docstring it exercises, or "control" when it must SURVIVE
(docstring text, annotation) or "out-of-scope" when the test docstring does not
claim that behaviour. Exit 0 when every expectation holds at both revisions and
BASE and HEAD give the same verdict for every shared mutant; 1 otherwise.
"""

import shutil
import subprocess
import sys
from pathlib import Path

# name -> (old, new, expectation, docstring clause). expectation: killed | survives
MUTANTS = {
    "M00-unmutated": (None, None, "survives", "baseline: test passes"),
    "M01-drop-LC_ALL-override": ('        compiler_env["LC_ALL"] = "C"\n', "", "killed",
                                 "each compiler call gets caller env plus LC_ALL=C"),
    "M02-LC_ALL-on-model-generation": ('"--Mdir", tmp], check=True', '"--Mdir", tmp], check=True, env={**os.environ, "LC_ALL": "C"}',
                                       "killed", "LC_ALL=C for the compiler only / exact model-generation call"),
    "M03-mutate-caller-environment": ("compiler_env = os.environ.copy()", "compiler_env = os.environ", "killed",
                                      "caller's environment unchanged"),
    "M04-drop-case-1002": (', ("1002", (class_d,))]', "]", "killed", "four compiler calls"),
    "M05-no-shlex-split-of-cxx": ("*shlex.split(args.cxx)", "args.cxx", "killed", "passes every argument through"),
    "M06-final-return-nonzero": ("    return 0\n", "    return 2\n", "killed", "requires exit 0"),
    "M07-drop-Wextra": ('"-Wall", "-Wextra", "-fsyntax-only"', '"-Wall", "-fsyntax-only"', "killed",
                        "exact compiler calls"),
    "M08-root-query-arguments": ('"--getenv", "VERILATOR_ROOT"]', '"--getenv", "VERILATOR_ROOT", "--quiet"]', "killed",
                                 "passes every argument through"),
    "M09-keep-leading-double-dash": ("vflags = vflags[1:]", "vflags = vflags", "killed",
                                     "exact model-generation call"),
    "M10-model-flags-after-Mdir": ('[args.verilator, *vflags, "--Mdir", tmp]', '[args.verilator, "--Mdir", tmp, *vflags]',
                                   "killed", "exact model-generation call"),
    "M11-stderr-not-merged": ("stderr=subprocess.STDOUT", "stderr=subprocess.PIPE", "killed", "exact compiler calls"),
    "M12-LC_ALL-C.UTF-8": ('compiler_env["LC_ALL"] = "C"', 'compiler_env["LC_ALL"] = "C.UTF-8"', "killed",
                           "LC_ALL=C"),
    "M13-never-report-mismatch": ("            if (bool(result.returncode)", "            if False and (bool(result.returncode)",
                                  "survives", "out-of-scope: the test docstring claims only the exit-0 path"),
    "M14-docstring-text-only": ("0 = all four PASS.", "0 = every case PASSES.", "survives", "control (HEAD only)"),
    "M15-drop-return-annotation": ("def main() -> int:", "def main():", "survives", "control (HEAD only)"),
}


def run(checkout: Path, work: Path, name: str) -> str:
    """Apply one mutant to a disposable copy and return killed / survives / NOT-APPLICABLE."""
    old, new, _, _ = MUTANTS[name]
    case = work / name
    shutil.rmtree(case, ignore_errors=True)
    case.mkdir(parents=True)
    for f in ("fixture_guards.py", "test_fixture_guards.py"):
        shutil.copy2(checkout / "tb/pp_top" / f, case / f)
    target = case / "fixture_guards.py"
    if old is not None:
        text = target.read_text()
        if text.count(old) != 1:
            return f"NOT-APPLICABLE({text.count(old)} matches)"
        target.write_text(text.replace(old, new))
    proc = subprocess.run([sys.executable, "-B", "-m", "unittest", "test_fixture_guards.py"],
                          cwd=case, capture_output=True, text=True)
    (case / "unittest.log").write_text(proc.stdout + proc.stderr)
    tail = (proc.stdout + proc.stderr).strip().splitlines()[-1]
    return ("survives" if proc.returncode == 0 else "killed") + f" [{tail}]"


def main() -> int:
    """Build the kill matrix; 0 = every expectation met and BASE agrees with HEAD."""
    base, head, work = (Path(p).resolve() for p in sys.argv[1:4])
    ok = True
    print(f"{'mutant':34s} {'expect':9s} {'base':38s} {'head':38s} clause")
    for name, (_, _, expect, clause) in MUTANTS.items():
        b = run(base, work / "base", name)
        h = run(head, work / "head", name)
        head_only = "HEAD only" in clause
        h_ok = h.startswith(expect)
        b_ok = b.startswith("NOT-APPLICABLE") if head_only else (b.startswith(expect) and b.split()[0] == h.split()[0])
        ok = ok and h_ok and b_ok
        print(f"{name:34s} {expect:9s} {b:38s} {h:38s} {clause}  {'OK' if h_ok and b_ok else 'MISMATCH'}")
    print(f"RESULT: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
