#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 5): is every rule of the name class held by the self-test, and which by the generator?

Each mutant edits one span of the gate in a copy of the three modules (as the shipped campaign copies them):
the four round-4 name mutants of probe_r4_generative.py whose spans round 5 rewrote, re-pointed at the code that
now holds their rule (prefix "r4:"), and new mutants of the names() walk, the SCOPES path and the two classes.
For each, two runs:
  fuzz     - only the generative test, fuzz(500, 234) on the self-test fixtures, then fuzz(5000, 234) if 500
             missed; rc != 0 = the generator alone detects it;
  selftest - the whole --selftest (arms plus the 500 cases); rc != 0 = KILLED.
Every mutant here changes documented behaviour, so the expected self-test result is KILLED; a SURVIVED line is a
test gap. A generator miss is recorded, not judged: the generator's oracle cannot tell an over-refusal (exit 2 on
a valid input) from a correct refusal, so a mutant that only over-refuses is the arms' to kill.

Usage: probe_r5_names.py <checkout> <scratch-dir> [--jobs N]
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
WALK = "                if not (SCOPE_NAME if scope else NAME).fullmatch(key):\n"
SCOPE_TEST = "            scope = len(path) == len(scopes) > 0 and all(want in (None, key) for want, key in zip(scopes, path))"
MUTANTS = {
    "control": (None, None),
    # Round-4 mutants of probe_r4_generative.py, re-pointed.
    "r4: strict(): plain json.loads": (
        "    tree = json.loads(text, object_pairs_hook=named, parse_constant=constant, parse_float=decimal,\n"
        "                      parse_int=integer)\n", "    tree = json.loads(text)\n"),
    "r4: names(): no name class": (WALK, "                if False:\n"),
    "r4: names(): NAME class for every key (no bracket exception)": (
        WALK, "                if not NAME.fullmatch(key):\n"),
    "r4: endpoint names not held to NAME (endpoints table keys as scope names)": (
        SCOPE_TEST, SCOPE_TEST.replace("scope = ", "scope = path == ('endpoints',) or ")),
    # New: the walk.
    "walk: every level below the scopes object also scope": (
        "scope = len(path) == len(scopes) > 0 and", "scope = len(path) >= len(scopes) > 0 and"),
    "walk: any path element matching suffices": ("and all(want in (None, key)", "and any(want in (None, key)"),
    "walk: only an object's first key checked": (
        "            for key in value:\n" + WALK, "            for key in list(value)[:1]:\n" + WALK),
    "walk: prefix match, not full": (WALK, WALK.replace(".fullmatch(key)", ".match(key)")),
    "walk: the image manifest unchecked (names only when scopes given)": (
        "    names(tree, scopes)\n", "    if scopes:\n        names(tree, scopes)\n"),
    "walk: only the baseline's top-level object descended": (
        "            stack += [((*path, key), item) for key, item in reversed(value.items())]\n",
        "            stack += [((*path, key), item) for key, item in reversed(value.items()) if not path]\n"),
    # New: the scopes path.
    "SCOPES: any top-level key": ('SCOPES = ("endpoints", None, "record", "scopes")',
                                  'SCOPES = (None, None, "record", "scopes")'),
    "SCOPES: any endpoint field": ('SCOPES = ("endpoints", None, "record", "scopes")',
                                   'SCOPES = ("endpoints", None, None, "scopes")'),
    "SCOPES: the record's figures instead": ('SCOPES = ("endpoints", None, "record", "scopes")',
                                             'SCOPES = ("endpoints", None, "record", "figures")'),
    # New: the two classes.
    "NAME: brackets allowed": ('NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")',
                               'NAME = re.compile(r"[A-Za-z0-9_.:/\\[\\]-]{1,128}")'),
    "NAME: empty key allowed": ('NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")',
                                'NAME = re.compile(r"[A-Za-z0-9_.:/-]{0,128}")'),
    "NAME: no length bound": ('NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")',
                              'NAME = re.compile(r"[A-Za-z0-9_.:/-]+")'),
    "NAME: space allowed": ('NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")',
                            'NAME = re.compile(r"[A-Za-z0-9_.:/ -]{1,128}")'),
    "SCOPE_NAME: space allowed": ('SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\\[\\]-]{1,128}")',
                                  'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\\[\\] -]{1,128}")'),
    "SCOPE_NAME: no length bound": ('SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\\[\\]-]{1,128}")',
                                    'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\\[\\]-]+")'),
    "SCOPE_NAME: any character": ('SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\\[\\]-]{1,128}")',
                                  'SCOPE_NAME = re.compile(r".{1,128}", re.S)'),
    "SCOPE_NAME: empty key allowed": ('SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\\[\\]-]{1,128}")',
                                      'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\\[\\]-]{0,128}")'),
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
        if source.count(old) != 1:
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
    print(f"probe_r5_names: {len(lines) - 1} mutants, {sum(line.startswith('KILLED') for line in lines)} killed, "
          f"{sum(line.startswith('SURVIVED') for line in lines)} survived, "
          f"{sum(line.startswith('NOT-APPLIED') for line in lines)} not applied, "
          f"{sum('generator detects' in line for line in lines)} detected by the generator alone; "
          f"control {'ok' if lines[0].startswith('ok') else 'BAD'}")


if __name__ == "__main__":
    main()
