#!/usr/bin/env python3
"""arm_counts.py <tree> <out.tsv> <jobs> <arm:suite:group>...: run each planted arm against one suite group through
the campaign's own trial (tb/srp_top/mutants.py: a scratch copy of hdl/ and the suites, the arm applied with git
apply), and write one row per run: arm, suite, group, rc, the suite's tally line, and the distinct failing row tags
(the text before the first colon, or the first three words where a row has none)."""
import importlib.util
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
jobs_n = int(sys.argv[3])
spec = importlib.util.spec_from_file_location("mutants", tree / "tb/srp_top/mutants.py")
mutants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutants)
from mutant_pool import in_order  # noqa: E402  (tb/common, on the path mutants.py set)

units = []
for item in sys.argv[4:]:
    arm, suite, group = item.split(":")
    units.append((arm, suite, group))


def tag(line: str) -> str:
    body = line[len("FAIL: "):]
    head = body.split(":", 1)[0] if ":" in body[:40] else " ".join(body.split()[:3])
    return head.strip()


rows = ["arm\tsuite\tgroup\trc\ttally\tfailing"]
with in_order(mutants.trial, units, jobs_n) as results:
    for (arm, suite, group), (rc, text) in zip(units, results):
        tallies = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL", text)
        fails = [ln for ln in text.splitlines() if ln.startswith("FAIL: ")]
        tags = sorted({tag(ln) for ln in fails})
        rows.append(f"{arm}\t{suite}\t{group or '-'}\t{rc}\t{tallies[-1] if tallies else 'no tally'}\t"
                    + "; ".join(tags))
        print(rows[-1], flush=True)
out.write_text("\n".join(rows) + "\n")
