#!/usr/bin/env python3
"""R506-2 probe: build the clone's adp.c with gcov, run adp_reentry_probe.c, and
apply the README's adp.c exclusion rows to that measurement alone: a row whose
named arc or line is reported covered was reached by a re-entrant port.
Usage: python3 adp_reentry_probe.py <review clone> <scratch dir>"""
import subprocess, sys
from pathlib import Path
clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/gtest"))
import fw_coverage as cov  # noqa: E402
here = Path(__file__).resolve().parent
out.mkdir(parents=True, exist_ok=True)
inc = [f"-I{clone}/sw/firmware/ctrl/{d}" for d in ("adp", "wire")]
for argv in (["gcc", "-std=c11", "-O0", "--coverage", *inc, "-c", str(clone / "sw/firmware/ctrl/adp/adp.c"), "-o", str(out / "adp.o")],
             ["gcc", "-std=c11", "-O0", "-Wall", "-Wextra", *inc, "-c", str(here / "adp_reentry_probe.c"), "-o", str(out / "probe.o")],
             ["gcc", "--coverage", str(out / "adp.o"), str(out / "probe.o"), "-o", str(out / "probe")]):
    subprocess.run(argv, check=True)
for g in out.glob("*.gcda"):
    g.unlink()
print(subprocess.run([str(out / "probe")], check=True, capture_output=True, text=True).stdout, end="")
merged = cov.collect([out])
rows = [r for r in cov.exclusions((clone / "sw/firmware/gtest/README.md").read_text()) if r.file.endswith("adp/adp.c")]
src = merged["sw/firmware/ctrl/adp/adp.c"]
text = (clone / rows[0].file).read_text().splitlines()
for r in rows:
    span = src.functions[r.function]
    permit = cov.parse_uncovered(r.uncovered)
    first = next(n for n in range(span[0], span[1] + 1) if r.statement in text[n - 1])
    last = cov.statement_end(text, first, span[1])
    order = [(n, k, a) for n in range(first, last + 1) if n in src.lines for k, a in enumerate(src.lines[n].arcs)]
    reached = [p for p in permit.arcs if order[p - 1][2] > 0]
    print(f"row {r.function} `{r.statement}` names arcs {list(permit.arcs)} of {permit.of}: "
          f"reached by the probe {reached or 'none'}")
