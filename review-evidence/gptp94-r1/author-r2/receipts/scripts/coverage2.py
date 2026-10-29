"""Run chosen engine-arm controls with every FAIL line kept: the arm's own
named-check verdict per control, and a map of each #94 check to the
controls that fail it.

usage: coverage2.py <engine tb dir> <checks.txt> <out dir> <workers>
       <name> [<name> ...]   ("PORT" selects every port_mutants entry)
Writes <out>/<k>.log per control (verdict, FAIL lines, tally), coverage.md
and coverage.json. A check no control fails is listed as UNCOVERED.
"""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

tb = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tb))
import mutants  # noqa: E402
import port_mutants  # noqa: E402
from mutation_verdict import verdict  # noqa: E402

checks = [l for l in Path(sys.argv[2]).read_text().splitlines() if l]
out = Path(sys.argv[3])
workers = int(sys.argv[4])
names = sys.argv[5:]
chosen = [m for m in mutants.MUTATIONS
          if m[0] in names or ("PORT" in names and m in port_mutants.PORT_MUTATIONS)]
work = out / "work"


def one(args):
    k, mutation = args
    name, fname, pattern, replacement, breaks = mutation
    w = work / f"m{k}"
    w.mkdir(parents=True, exist_ok=True)
    src = mutants.stage(w, "m", (fname, mutants.edits_of(pattern, replacement)))
    run = w / "run_m"
    if not mutants.generate_image(src, run):
        return k, name, None, "image refused", "image refused"
    exe = mutants.build(src, w, "m")
    if exe is None:
        return k, name, None, "did not build", "did not build"
    rc, output = mutants.run_harness(exe, run)
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        answer = mutants.named_verdict(verdict(rc, output), breaks, output)
    lines = [l for l in output.splitlines() if l.startswith("FAIL") or "checks:" in l]
    return k, name, rc, answer, "\n".join(lines)


if __name__ == "__main__":
    out.mkdir(parents=True, exist_ok=True)
    cover = {c: [] for c in checks}
    rows = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for k, name, rc, answer, text in ex.map(one, list(enumerate(chosen, 1))):
            (out / f"{k:02d}.log").write_text(
                f"control: {name}\nrc: {rc}\nnamed verdict: {answer}\n{text}\n")
            fails = [l for l in text.splitlines() if l.startswith("FAIL ")]
            hit = [c for c in checks
                   if any(l.startswith("FAIL " + c + " ") for l in fails)]
            for c in hit:
                cover[c].append(name)
            rows.append(dict(k=k, control=name, rc=rc, named_verdict=answer,
                             new_checks_failed=hit,
                             tally=[l for l in text.splitlines() if "checks:" in l]))
            print(k, name, rc, answer, len(hit), flush=True)
    (out / "coverage.json").write_text(json.dumps(dict(controls=rows, coverage=cover), indent=1) + "\n")
    md = ["# #94 checks and the planted controls that fail them", "",
          "| Check | Controls whose run prints it as FAIL |", "|---|---|"]
    for c in checks:
        md.append(f"| {c} | {'; '.join(cover[c]) if cover[c] else 'UNCOVERED'} |")
    md += ["", "| Control | Arm verdict on its named checks |", "|---|---|"]
    for r in rows:
        md.append(f"| {r['control']} | {r['named_verdict']} |")
    (out / "coverage.md").write_text("\n".join(md) + "\n")
    print("uncovered:", [c for c in checks if not cover[c]])
    print("not caught on named:", [r["control"] for r in rows if r["named_verdict"] != "caught"])
