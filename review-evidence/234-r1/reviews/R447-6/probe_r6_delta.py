#!/usr/bin/env python3
"""Round-6 delta probe of the #234 resource gate's self-test: reviewer mutants the round-6 arms claim to pin.

Usage: probe_r6_delta.py <repo checkout> <round-5 self-test file> <scratch dir> [jobs]

Each mutant edits exactly one unique span of a copy of pp_resource_gate.py (byte-identical at rounds 5 and 6),
with pp_baseline_rank.py and the committed baseline beside it. These mutants are this reviewer's own and are
distinct from the shipped campaign's spans and from probe_r5_namekill.py. Groups:
  list   - the walk skips some list items (middle, first, last, past the second)
  image  - the image manifest alone is walked over some of its entries
  dict   - the walk descends below only some keys of an object
  scope  - the scope path SCOPES loosened at one position
  name   - NAME's accepted side narrowed at its lower bound or its first character
  scope-name - SCOPE_NAME's accepted side narrowed by one group or the length (an extension of R447-5 S1)
  bound  - the upper length bound of either class loosened by one
For each mutant five runs, each a separate process in the copy:
  fuzz500     - gate.fuzz(500, 234) alone, with the head's generator
  fuzz5k      - gate.fuzz(5000, 447) alone, with the head's generator
  selftest    - the head's --selftest (arms and the 500 cases)
  selftest_r5 - the round-5 self-test in place of the head's (what round 6 added)
  realaudit   - check-baseline on the committed baseline and budget page
A run that exits 0 did not detect the mutant. The script never writes inside the checkout.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess
import sys

GATE, RANK, SELF, BASE = "pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py", \
    "pp_resource_baseline.json"
LIST = "reversed(list(enumerate(value)))]"
DICT = "for key, item in reversed(value.items())]"
SCOPES = 'SCOPES = ("endpoints", None, "record", "scopes")'
NAME = 'NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,128}")'
SNAME = r'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\[\]-]{1,128}")'
IMAGES = '    images = strict((directory / "baseline_images.json").read_text())\n'


def images(select: str) -> str:
    return ('    images = json.loads((directory / "baseline_images.json").read_text(), object_pairs_hook=named, '
            'parse_constant=constant, parse_float=decimal, parse_int=integer)\n'
            f'    names(images{select} if isinstance(images, list) else images, ())\n')


def sname(body: str) -> str:
    return f'SCOPE_NAME = re.compile(r"{body}")'


MUTANTS = {
    "list: walk skips the middle items of a list": (LIST, "reversed(list(enumerate(value))[::2])]"),
    "list: walk visits only a list's first two items": (LIST, "reversed(list(enumerate(value))[:2])]"),
    "list: walk skips a list's first item": (LIST, "reversed(list(enumerate(value))[1:])]"),
    "list: walk skips a list's last item": (LIST, "reversed(list(enumerate(value))[:-1])]"),
    "list: walk visits only a list's last item": (LIST, "reversed(list(enumerate(value))[-1:])]"),
    "image: manifest walked over its first entry only": (IMAGES, images("[:1]")),
    "image: manifest walked over all but its last entry": (IMAGES, images("[:-1]")),
    "image: manifest walked over its first and last entries only": (IMAGES, images("[::2]")),
    "dict: walk descends below an object's first key only": (DICT, "for key, item in reversed(list(value.items())[:1])]"),
    "dict: walk descends below every key but an object's last": (
        DICT, "for key, item in reversed(list(value.items())[:-1])]"),
    "scope: SCOPES any third key": (SCOPES, 'SCOPES = ("endpoints", None, None, "scopes")'),
    "scope: SCOPES any last key": (SCOPES, 'SCOPES = ("endpoints", None, "record", None)'),
    "name: NAME needs two characters": (NAME, 'NAME = re.compile(r"[A-Za-z0-9_.:/-]{2,128}")'),
    "name: NAME refuses a leading digit": (NAME, 'NAME = re.compile(r"[A-Za-z_.:/-][A-Za-z0-9_.:/-]{0,127}")'),
    "name: NAME refuses a leading hyphen": (NAME, 'NAME = re.compile(r"[A-Za-z0-9_.:/][A-Za-z0-9_.:/-]{0,127}")'),
    "scope-name: drops upper case": (SNAME, sname(r"[a-z0-9_.:/\[\]-]{1,128}")),
    "scope-name: drops lower case": (SNAME, sname(r"[A-Z0-9_.:/\[\]-]{1,128}")),
    "scope-name: drops digits": (SNAME, sname(r"[A-Za-z_.:/\[\]-]{1,128}")),
    "scope-name: drops the underscore": (SNAME, sname(r"[A-Za-z0-9.:/\[\]-]{1,128}")),
    "scope-name: drops the dot": (SNAME, sname(r"[A-Za-z0-9_:/\[\]-]{1,128}")),
    "scope-name: drops the colon": (SNAME, sname(r"[A-Za-z0-9_./\[\]-]{1,128}")),
    "scope-name: drops the slash": (SNAME, sname(r"[A-Za-z0-9_.:\[\]-]{1,128}")),
    "scope-name: drops the hyphen": (SNAME, sname(r"[A-Za-z0-9_.:/\[\]]{1,128}")),
    "scope-name: capped at 127": (SNAME, sname(r"[A-Za-z0-9_.:/\[\]-]{1,127}")),
    "scope-name: needs two characters": (SNAME, sname(r"[A-Za-z0-9_.:/\[\]-]{2,128}")),
    "bound: NAME takes 129": (NAME, 'NAME = re.compile(r"[A-Za-z0-9_.:/-]{1,129}")'),
    "bound: SCOPE_NAME takes 129": (SNAME, sname(r"[A-Za-z0-9_.:/\[\]-]{1,129}")),
}
RUNS = {
    "fuzz500": ["-c", "import sys, pp_resource_gate as g; sys.exit(g.fuzz(500, 234))"],
    "fuzz5k": ["-c", "import sys, pp_resource_gate as g; sys.exit(g.fuzz(5000, 447))"],
    "selftest": [GATE, "--selftest"],
    "selftest_r5": [GATE, "--selftest"],
    "realaudit": [GATE, "check-baseline", "--baseline", BASE, "--budget", "BUDGET"],
}


def run(name, spans, here, r5, budget, tmp):
    out = {}
    for label, argv in RUNS.items():
        folder = tmp / ("".join(ch if ch.isalnum() else "_" for ch in name) + ("_r5" if label == "selftest_r5" else ""))
        if not folder.exists():
            folder.mkdir(parents=True)
            for module in (GATE, RANK, SELF, BASE):
                shutil.copy(here / module, folder / module)
            if label == "selftest_r5":
                shutil.copy(r5, folder / SELF)
            text = (folder / GATE).read_text()
            if text.count(spans[0]) != 1:
                return name, {"apply": f"NOT-UNIQUE ({text.count(spans[0])})"}
            (folder / GATE).write_text(text.replace(*spans))
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
    r5 = Path(sys.argv[2]).resolve()
    here, budget = repo / "syn/ooc", repo / "docs/design/AREA_BUDGET.md"
    tmp = Path(sys.argv[3]).resolve()
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    control = run("control", ("BASELINE = ", "BASELINE = "), here, r5, budget, tmp)
    print("control: " + ", ".join(f"{k} rc={v[1]}" for k, v in control[1].items()))
    if any(v[1] != 0 for v in control[1].values()):
        sys.exit("the unmutated control must pass every run")
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda item: run(item[0], item[1], here, r5, budget, tmp), MUTANTS.items()))
    survived, missed_by_selftest = [], []
    for name, out in results:
        if "apply" in out:
            print(f"{name}: {out['apply']}")
            survived.append(name)
            continue
        print(f"{name}: " + "; ".join(f"{k} {v[0]} rc={v[1]}" for k, v in out.items()))
        for k, v in out.items():
            print(f"    {k}: {v[2]}")
        if out["selftest"][0] == "passed":
            missed_by_selftest.append(name)
        if all(v[0] == "passed" for v in out.values()):
            survived.append(name)
    ok = [o for _, o in results if "apply" not in o]
    st = sum(1 for o in ok if o["selftest"][0] == "DETECTED")
    st5 = sum(1 for o in ok if o["selftest_r5"][0] == "DETECTED")
    gen = sum(1 for o in ok if "DETECTED" in (o["fuzz500"][0], o["fuzz5k"][0]))
    print(f"round-6 delta mutants: {len(results)}; head self-test killed {st}; round-5 self-test killed {st5}; "
          f"head generative block alone detected {gen}")
    print(f"missed by the head self-test: {len(missed_by_selftest)} {missed_by_selftest}")
    print(f"undetected by every run: {len(survived)} {survived}")


if __name__ == "__main__":
    main()
