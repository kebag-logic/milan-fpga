#!/usr/bin/env python3
"""arm_logs.py <tree> <outdir> <jobs> <arm:suite:group>...: run each planted arm through the campaign's own trial
(tb/srp_top/mutants.py) and keep each run's whole log as <outdir>/<arm>.<suite>.<group>.log, then print each run's
failing row IDs (the first word after "FAIL: ", without a trailing colon) with their multiplicity."""
import collections
import importlib.util
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
jobs = int(sys.argv[3])
spec = importlib.util.spec_from_file_location("mutants", tree / "tb/srp_top/mutants.py")
mutants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutants)
from mutant_pool import in_order  # noqa: E402
units = [tuple(x.split(":")) for x in sys.argv[4:]]
with in_order(mutants.trial, units, jobs) as results:
    for (arm, suite, group), (rc, text) in zip(units, results):
        (out / f"{arm}.{suite}.{group or '-'}.log").write_text(text)
        ids = collections.Counter(l[6:].split()[0].rstrip(":") for l in text.splitlines() if l.startswith("FAIL: "))
        shown = ", ".join(f"{k} ({v})" if v > 1 else k for k, v in ids.items())
        print(f"{arm} {suite} {group or '-'} rc={rc} failures={sum(ids.values())}: {shown}", flush=True)
