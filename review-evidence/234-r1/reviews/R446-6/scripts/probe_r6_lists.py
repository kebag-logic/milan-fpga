#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 6): do the self-test's arms and generator hold the list walk, the name classes' accepted
side and the scope path, beyond the mutants the PR ships?

Each mutant edits one span of the gate in a copy of the three modules (as the shipped campaign copies them). For
each, two runs, as in probe_r5_names.py:
  fuzz     - only the generative test, fuzz(500, 234) on the self-test fixtures, then fuzz(5000, 234) if 500
             missed; rc != 0 = the generator alone detects it;
  selftest - the whole --selftest (arms plus the 500 cases); rc != 0 = KILLED.
Families: the list walk (which items of a list are visited, and the index a refusal names), the accepted side of
SCOPE_NAME (each character group and the length; the PR ships the NAME ones), and the scope path. Every mutant
changes documented behaviour unless its label says "equivalent?"; a SURVIVED line is a test gap to judge.

Usage: probe_r6_lists.py <checkout> <scratch-dir> [--jobs N]
"""

import concurrent.futures
from pathlib import Path
import shutil
import subprocess
import sys

REPO, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
HERE = REPO / "syn/ooc"
GATE, RANK = "pp_resource_gate.py", "pp_baseline_rank.py"
ITEMS = "for index, item in reversed(list(enumerate(value)))]"
LIST = "        elif isinstance(value, list):\n"
SCOPE_NAME = 'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\\[\\]-]{1,128}")'
SCOPE_TEST = "scope = len(path) == len(scopes) > 0 and all(want in (None, key) for want, key in zip(scopes, path))"


def narrowed(group: str) -> tuple[str, str]:
    """SCOPE_NAME without one character group, removed inside the character class only."""
    head, tail = SCOPE_NAME.split('r"[', 1)
    return SCOPE_NAME, f'{head}r"[{tail.replace(group, "", 1)}'


MUTANTS = {
    "control": (None, None),
    # The list walk.
    "list: first item only (the shipped mutant's span)": (ITEMS, "for index, item in list(enumerate(value))[:1]]"),
    "list: last item only": (ITEMS, "for index, item in list(enumerate(value))[-1:]]"),
    "list: every item but the first": (ITEMS, "for index, item in list(enumerate(value))[1:]]"),
    "list: every item but the last": (ITEMS, "for index, item in list(enumerate(value))[:-1]]"),
    "list: even indices only": (ITEMS, "for index, item in list(enumerate(value))[::2]]"),
    "list: odd indices only": (ITEMS, "for index, item in list(enumerate(value))[1::2]]"),
    "list: first three items only": (ITEMS, "for index, item in list(enumerate(value))[:3]]"),
    "list: the index a refusal names is always 0": (
        "stack += [((*path, index), item) for index, item in reversed(",
        "stack += [((*path, 0), item) for index, item in reversed("),
    "list: the top-level list (image manifest) not descended": (
        LIST, "        elif isinstance(value, list) and path:\n"),
    "list: a list inside a list not descended": (
        LIST, "        elif isinstance(value, list) and not (path and isinstance(path[-1], int)):\n"),
    "list: lists below the top level not descended": (
        LIST, "        elif isinstance(value, list) and len(path) < 1:\n"),
    "list: visit order reversed (equivalent?)": (ITEMS, "for index, item in list(enumerate(value))]"),
    # The accepted side of SCOPE_NAME.
    "SCOPE_NAME: no upper case": narrowed("A-Z"),
    "SCOPE_NAME: no lower case": narrowed("a-z"),
    "SCOPE_NAME: no digits": narrowed("0-9"),
    "SCOPE_NAME: no underscore": narrowed("_"),
    "SCOPE_NAME: no dot": narrowed("."),
    "SCOPE_NAME: no colon": narrowed(":"),
    "SCOPE_NAME: no slash": narrowed("/"),
    "SCOPE_NAME: no hyphen": (SCOPE_NAME, SCOPE_NAME.replace("\\]-]", "\\]]")),
    "SCOPE_NAME: no opening bracket": narrowed("\\["),
    "SCOPE_NAME: no closing bracket": narrowed("\\]"),
    "SCOPE_NAME: 127 characters": (SCOPE_NAME, SCOPE_NAME.replace("{1,128}", "{1,127}")),
    # The scope path.
    "scope path: last two keys only (shipped)": (
        "all(want in (None, key) for want, key in zip(scopes, path))", "path[-2:] == scopes[-2:]"),
    "scope path: first key free (shipped)": ('SCOPES = ("endpoints", None, "record", "scopes")',
                                             'SCOPES = (None, None, "record", "scopes")'),
    "scope path: third key free": ('SCOPES = ("endpoints", None, "record", "scopes")',
                                   'SCOPES = ("endpoints", None, None, "scopes")'),
    "scope path: last key free": ('SCOPES = ("endpoints", None, "record", "scopes")',
                                  'SCOPES = ("endpoints", None, "record", None)'),
    "scope path: suffix match at any depth": (
        SCOPE_TEST, "scope = len(path) >= len(scopes) > 0 and all(want in (None, key) for want, key in "
                    "zip(scopes, path[-len(scopes):]))"),
}


def run(name: str) -> str:
    old, new = MUTANTS[name]
    folder = SCRATCH / "".join(char if char.isalnum() else "_" for char in name)
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for sibling in (GATE, RANK, "pp_resource_gate_selftest.py"):
        shutil.copy2(HERE / sibling, folder / sibling)
    if old is not None:
        source = (folder / GATE).read_text()
        if source.count(old) != 1 or old == new:
            return f"NOT-APPLIED {name}: span found {source.count(old)} times"
        (folder / GATE).write_text(source.replace(old, new))
    results = []
    for cases in (500, 5000):
        fuzz = subprocess.run([sys.executable, "-B", "-c", f"import sys, pp_resource_gate as g; sys.exit(g.fuzz({cases}, 234))"],
                              cwd=folder, capture_output=True, text=True, timeout=1800)
        last = [line for line in fuzz.stdout.splitlines() if "cases at seed" in line] or \
            fuzz.stderr.strip().splitlines()[-1:] or ["?"]
        results.append((cases, fuzz.returncode, last[0][-48:]))
        if fuzz.returncode != 0 or old is None:
            break
    selftest = subprocess.run([sys.executable, "-B", GATE, "--selftest"], cwd=folder, capture_output=True, text=True,
                              timeout=1800)
    failed = [line for line in (selftest.stdout + selftest.stderr).splitlines() if "FAIL" in line or "Error" in line]
    fuzz_text = "; ".join(f"fuzz{cases} rc={rc} [{line}]" for cases, rc, line in results)
    if old is None:
        verdict = "ok " if selftest.returncode == 0 and results[-1][1] == 0 else "BAD"
        return f"{verdict} {name}: {fuzz_text}; selftest rc={selftest.returncode}"
    verdict = "KILLED  " if selftest.returncode else "SURVIVED"
    generator = "generator detects" if results[-1][1] else "generator misses"
    first = f" | first: {failed[0][:150]}" if failed else ""
    return f"{verdict} {name}: {generator}; {fuzz_text}; selftest rc={selftest.returncode}{first}"


def main() -> None:
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        lines = list(pool.map(run, MUTANTS))
    for line in lines:
        print(line)
    print(f"probe_r6_lists: {len(lines) - 1} mutants, {sum(line.startswith('KILLED') for line in lines)} killed, "
          f"{sum(line.startswith('SURVIVED') for line in lines)} survived, "
          f"{sum(line.startswith('NOT-APPLIED') for line in lines)} not applied, "
          f"{sum('generator detects' in line for line in lines)} detected by the generator alone; "
          f"control {'ok' if lines[0].startswith('ok') else 'BAD'}")


if __name__ == "__main__":
    main()
