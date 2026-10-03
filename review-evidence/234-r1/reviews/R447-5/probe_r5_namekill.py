#!/usr/bin/env python3
"""Which side of the round-5 name ruling does each check catch? Reviewer mutants of names(), strict() and NAME.

Usage: probe_r5_namekill.py <repo checkout> <scratch dir> [jobs]

Each mutant edits exactly one unique span of a copy of pp_resource_gate.py (with pp_baseline_rank.py, the
self-test and the committed baseline beside it). The mutants are this reviewer's own, distinct from the shipped
campaign's spans. "reject" mutants accept a key the ruling refuses; "accept" mutants refuse a key the ruling
accepts. For each mutant four runs, each a separate process in the copy:
  fuzz500   - gate.fuzz(500, 234) alone: the self-test's generated block
  fuzz5k    - gate.fuzz(5000, 447) alone: a second seed
  selftest  - the shipped --selftest (arms and the 500 cases)
  realaudit - check-baseline on the committed baseline and budget page (a gate the repository runs)
A run that exits 0 did not detect the mutant. The script never writes inside the checkout.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess
import sys

GATE, RANK, SELF, BASE = "pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py", \
    "pp_resource_baseline.json"
CLASS = "(SCOPE_NAME if scope else NAME)"
MUTANTS = {
    # reject side: a key the ruling refuses is accepted
    "reject: notes skipped by the walk": (
        "        if isinstance(value, dict):\n            scope =",
        "        if path[:1] in ((\"description\",), (\"schema\",)) or path[2:3] == (\"measured\",):\n"
        "            continue\n        if isinstance(value, dict):\n            scope ="),
    "reject: brackets allowed in notes": (
        CLASS, "(SCOPE_NAME if scope or path[:1] in ((\"description\",), (\"schema\",)) "
               "or path[2:3] == (\"measured\",) else NAME)"),
    "reject: manifest read strict but without the name walk": (
        '    images = strict((directory / "baseline_images.json").read_text())\n',
        '    images = json.loads((directory / "baseline_images.json").read_text(), object_pairs_hook=named, '
        'parse_constant=constant, parse_float=decimal, parse_int=integer)\n'),
    "reject: manifest's first entry takes scope names": (
        'strict((directory / "baseline_images.json").read_text())',
        'strict((directory / "baseline_images.json").read_text(), (0,))'),
    "reject: brackets allowed in every manifest key": (
        'strict((directory / "baseline_images.json").read_text())',
        'strict((directory / "baseline_images.json").read_text(), (None,))'),
    "reject: scope class below the scope names too": (
        "scope = len(path) == len(scopes) > 0 and", "scope = len(path) >= len(scopes) > 0 and"),
    "reject: scope class at every depth-4 object": (
        "all(want in (None, key) for want, key in zip(scopes, path))", "True"),
    "reject: scope class matched on the last two keys": (
        "all(want in (None, key) for want, key in zip(scopes, path))", "path[-2:] == scopes[-2:]"),
    "reject: scope names unbounded in length": (
        r'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\[\]-]{1,128}")', r'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\[\]-]+")'),
    "reject: NAME takes a space": (
        'NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")', 'NAME = re.compile(r"[A-Za-z0-9_.:/ -]{1,128}")'),
    "reject: NAME takes a brace": (
        'NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")', 'NAME = re.compile(r"[A-Za-z0-9_.:/{}-]{1,128}")'),
    "reject: walk visits only the first item of a list": (
        "            stack += [((*path, index), item) for index, item in reversed(list(enumerate(value)))]",
        "            stack += [((*path, index), item) for index, item in list(enumerate(value))[:1]]"),
    # accept side: a key the ruling accepts is refused
    "accept: scope names held to NAME": (CLASS, "(NAME if scope else NAME)"),
    "accept: scope names only on an endpoint named route": (
        'SCOPES = ("endpoints", None, "record", "scopes")', 'SCOPES = ("endpoints", "route", "record", "scopes")'),
    "accept: scope names only on an endpoint named route-1x1": (
        'SCOPES = ("endpoints", None, "record", "scopes")', 'SCOPES = ("endpoints", "route-1x1", "record", "scopes")'),
    "accept: NAME drops the colon": (
        'NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")', 'NAME = re.compile(r"[A-Za-z0-9_./-]{1,128}")'),
    "accept: NAME drops the dot": (
        'NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")', 'NAME = re.compile(r"[A-Za-z0-9_:/-]{1,128}")'),
    "accept: NAME drops the slash": (
        'NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")', 'NAME = re.compile(r"[A-Za-z0-9_.:-]{1,128}")'),
    "accept: NAME capped at 64": (
        'NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")', 'NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,64}")'),
    "accept: manifest keys held to path and sha256": (
        "    names(tree, scopes)\n    return tree",
        "    names(tree, scopes)\n    if isinstance(tree, list) and any(set(e) - {'path', 'sha256'} for e in tree "
        "if isinstance(e, dict)):\n        raise ValueError('extra manifest key')\n    return tree"),
}
RUNS = {
    "fuzz500": ["-c", "import sys, pp_resource_gate as g; sys.exit(g.fuzz(500, 234))"],
    "fuzz5k": ["-c", "import sys, pp_resource_gate as g; sys.exit(g.fuzz(5000, 447))"],
    "selftest": [GATE, "--selftest"],
    "realaudit": [GATE, "check-baseline", "--baseline", BASE, "--budget", "BUDGET"],
}


def run(name, spans, here, budget, tmp):
    folder = tmp / "".join(ch if ch.isalnum() else "_" for ch in name)
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for module in (GATE, RANK, SELF, BASE):
        shutil.copy(here / module, folder / module)
    text = (folder / GATE).read_text()
    if text.count(spans[0]) != 1:
        return name, {"apply": f"NOT-UNIQUE ({text.count(spans[0])})"}
    (folder / GATE).write_text(text.replace(*spans))
    out = {}
    for label, argv in RUNS.items():
        argv = [str(budget) if arg == "BUDGET" else arg for arg in argv]
        result = subprocess.run([sys.executable, "-B", *argv], capture_output=True, text=True, timeout=3600,
                                cwd=folder)
        lines = (result.stdout + result.stderr).strip().splitlines()
        tail = next((line for line in reversed(lines) if "Error" in line or "FAILURE" in line or "failures" in line
                     or "NOT COMPARABLE" in line), lines[-1] if lines else "")
        out[label] = ("DETECTED" if result.returncode else "passed", result.returncode, tail[:220])
    return name, out


def main():
    repo = Path(sys.argv[1]).resolve()
    here, budget = repo / "syn/ooc", repo / "docs/design/AREA_BUDGET.md"
    tmp = Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    control = run("control", ("BASELINE = ", "BASELINE = "), here, budget, tmp)
    print("control: " + ", ".join(f"{k} rc={v[1]}" for k, v in control[1].items()))
    if any(v[1] != 0 for v in control[1].values()):
        sys.exit("the unmutated control must pass every run")
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda item: run(item[0], item[1], here, budget, tmp), MUTANTS.items()))
    survived = []
    for name, out in results:
        if "apply" in out:
            print(f"{name}: {out['apply']}")
            survived.append(name)
            continue
        print(f"{name}: " + "; ".join(f"{k} {v[0]} rc={v[1]}" for k, v in out.items()))
        for k, v in out.items():
            print(f"    {k}: {v[2]}")
        if all(v[0] == "passed" for v in out.values()):
            survived.append(name)
    gen = sum(1 for _, o in results if "apply" not in o and "DETECTED" in (o["fuzz500"][0], o["fuzz5k"][0]))
    st = sum(1 for _, o in results if "apply" not in o and o["selftest"][0] == "DETECTED")
    print(f"round-5 name mutants: {len(results)}; self-test killed {st}; generative block alone detected {gen}; "
          f"undetected by every run: {len(survived)} {survived}")


if __name__ == "__main__":
    main()
