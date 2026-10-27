"""Run selected mutants of one suite's own mutants.py, in parallel, each with
its full output kept, through the suite's own stage/build/run/verdict code.

usage: some_mutants.py <suite dir> <out dir> <workers> [name ...]
       (no names: every mutant in MUTATIONS)
Writes <out>/<tag>.log (every FAIL line, tally, verdict) and <out>/summary.txt.
"""
import concurrent.futures as cf
import importlib.util
import re
import sys
import tempfile
from pathlib import Path

suite = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
workers = int(sys.argv[3])
want = sys.argv[4:]
spec = importlib.util.spec_from_file_location("suite_mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
entries = [e for e in m.MUTATIONS if not want or e[0] in want]
missing = set(want) - {e[0] for e in entries}
assert not missing, missing
TALLY = re.compile(r"^\s*(\d+)\s+checks:.*$", re.M)


def tag_of(name):
    return "".join(c if c.isalnum() else "_" for c in name)


def one(work, clean_exe, entry):
    tag = tag_of(entry[0])
    lines = [f"mutant: {entry[0]}"]
    if suite.name == "parser":
        name, edits, breaks = entry
        exe = m.build(m.stage(work, tag, edits), work, tag)
        if exe is None:
            return entry[0], "did not build", lines
        rc, output = m.run_harness(exe)
        named = list(breaks)
        answer = m.verdict(rc, output)
    else:
        name, fname, pattern, replacement, breaks = entry
        edits = m.edits_of(pattern, replacement)
        srcdir = m.stage(work, tag, (fname, edits))
        rundir = work / f"run_{tag}"
        if not m.generate_image(srcdir, rundir):
            return name, "image refused", lines
        exe = clean_exe if fname == m.GENERATOR else m.build(srcdir, work, tag)
        if exe is None:
            return name, "did not build", lines
        rc, output = m.run_harness(exe, rundir)
        named = breaks.split(" | ")
        answer = m.named_verdict(m.verdict(rc, output), breaks, output)
    fails = [l for l in output.splitlines() if l.startswith("FAIL ")]
    lines += fails
    t = TALLY.findall(output)
    lines.append("tally: " + (output[output.rfind("\n", 0, output.rfind("checks:")) + 1:].strip().splitlines()[0] if "checks:" in output else "none"))
    missed = [w for w in named if not any(w in l for l in fails)]
    lines.append(f"named checks failing: {len(named) - len(missed)} of {len(named)}")
    lines += [f"NOT FAILING: {w}" for w in missed]
    lines.append(f"verdict: {answer}")
    if answer != "caught":
        lines += ["--- raw tail ---"] + output.splitlines()[-30:]
    return name, answer, lines


with tempfile.TemporaryDirectory(prefix="some-mutants-") as td:
    work = Path(td)
    clean_exe = None
    if suite.name != "parser":
        clean_src = m.stage(work, "clean")
        clean_exe = m.build(clean_src, work, "clean")
        assert clean_exe is not None, "clean build failed"
    results = []
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(one, work, clean_exe, e): e for e in entries}
        for f in cf.as_completed(futs):
            name, answer, lines = f.result()
            (out / f"{tag_of(name)}.log").write_text("\n".join(lines) + "\n")
            results.append((name, answer))
            print(f"{answer:>12}  {name}", flush=True)
    order = {e[0]: i for i, e in enumerate(m.MUTATIONS)}
    results.sort(key=lambda r: order[r[0]])
    (out / "summary.txt").write_text(
        "".join(f"{a}\t{n}\n" for n, a in results) +
        f"{sum(a == 'caught' for _, a in results)} of {len(results)} caught\n")
    print(f"{sum(a == 'caught' for _, a in results)} of {len(results)} caught")
