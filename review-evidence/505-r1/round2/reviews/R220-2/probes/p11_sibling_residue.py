"""P11: which run steps of the RTL-file jobs OUTSIDE the seven RTL jobs
(`full-ci-gate`, `physical-gptp`, the fast selector `changes`, the fast
verdict `rtl-fast`) accept a content edit with the complete HEAD checker
green? Levers per step: body replaced by `true`, and ` || true` appended to
each normalized line in turn. In-memory worlds, HEAD checker, BASE checker
for comparison."""
from __future__ import annotations

import copy
import json
import sys

from common import BASE, HEAD, load_module, world_at

SIBLINGS = ((".github/workflows/rtl.yml", ("full-ci-gate", "physical-gptp")),
            (".github/workflows/rtl-fast.yml", ("changes", "rtl-fast")))


def main() -> int:
    out = {}
    for label, rev in (("head", HEAD), ("base", BASE)):
        m = load_module(rev, f"m11_{label}")
        w0 = world_at(m, rev)
        assert not m.check(w0).findings
        rows = []
        for path, jids in SIBLINGS:
            for jid in jids:
                for at, step in enumerate(w0[path]["jobs"][jid]["steps"]):
                    if not isinstance(step.get("run"), str):
                        continue
                    lines = m.normalize_script(step["run"])
                    accepted = []
                    edits = [("no-op", "true")]
                    for k in range(len(lines)):
                        e = list(lines)
                        e[k] = e[k] + " || true"
                        edits.append((f"or-true-line-{k + 1}", "\n".join(e)))
                    for lever, run in edits:
                        w = copy.deepcopy(w0)
                        w[path]["jobs"][jid]["steps"][at]["run"] = run
                        if not m.check(w).findings:
                            accepted.append(lever)
                    rows.append({"job": jid, "step": at + 1, "name": step.get("name"),
                                 "lines": len(lines), "accepted_with_check_green": accepted})
        out[label] = rows
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    for label in ("head", "base"):
        print(f"== {label}")
        for r in out[label]:
            print(f"  {r['job']:14s} step {r['step']} ({r['name']}): lines={r['lines']} "
                  f"accepted={r['accepted_with_check_green'] or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
