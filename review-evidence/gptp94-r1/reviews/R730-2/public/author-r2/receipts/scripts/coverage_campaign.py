"""Run chosen engine-arm controls with every FAIL line kept, and map each new
check to the controls that fail it.

usage: coverage_campaign.py <engine tb dir> <checks.txt> <out dir> <workers>
       <name> [<name> ...]   ("PORT" selects every port_mutants entry)
Writes <out>/<k>.log per control (its FAIL lines and tally), coverage.md and
coverage.json. A check no control fails is listed as UNCOVERED.
"""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

tb = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tb))
import mutants  # noqa: E402
import port_mutants  # noqa: E402

checks = [l for l in Path(sys.argv[2]).read_text().splitlines() if l]
out = Path(sys.argv[3])
workers = int(sys.argv[4])
names = sys.argv[5:]
chosen = [m for m in mutants.MUTATIONS
          if m[0] in names or ("PORT" in names and m in port_mutants.PORT_MUTATIONS)]
work = out / "work"


def one(args):
    k, mutation = args
    name, fname, pattern, replacement, _ = mutation
    w = work / f"m{k}"
    w.mkdir(parents=True, exist_ok=True)
    src = mutants.stage(w, "m", (fname, mutants.edits_of(pattern, replacement)))
    run = w / "run_m"
    if not mutants.generate_image(src, run):
        return k, name, None, "image refused"
    exe = mutants.build(src, w, "m")
    if exe is None:
        return k, name, None, "did not build"
    rc, output = mutants.run_harness(exe, run)
    lines = [l for l in output.splitlines() if l.startswith("FAIL") or "checks:" in l]
    return k, name, rc, "\n".join(lines)


if __name__ == "__main__":
    out.mkdir(parents=True, exist_ok=True)
    cover = {c: [] for c in checks}
    rows = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for k, name, rc, text in ex.map(one, list(enumerate(chosen, 1))):
            (out / f"{k:02d}.log").write_text(f"control: {name}\nrc: {rc}\n{text}\n")
            fails = [l for l in text.splitlines() if l.startswith("FAIL ")]
            hit = [c for c in checks if any(c in l and not l.startswith("FAIL p1 255 ") for l in fails)]
            for c in hit:
                cover[c].append(name)
            rows.append(dict(k=k, control=name, rc=rc, new_checks_failed=hit,
                             tally=[l for l in text.splitlines() if "checks:" in l]))
            print(k, name, rc, len(hit), flush=True)
    (out / "coverage.json").write_text(json.dumps(dict(controls=rows, coverage=cover), indent=1) + "\n")
    md = ["# New #94 checks and the planted controls that fail them", "",
          "| New check | Controls whose run prints it as FAIL |", "|---|---|"]
    for c in checks:
        md.append(f"| {c} | {'; '.join(cover[c]) if cover[c] else 'UNCOVERED'} |")
    (out / "coverage.md").write_text("\n".join(md) + "\n")
    print("uncovered:", [c for c in checks if not cover[c]])
