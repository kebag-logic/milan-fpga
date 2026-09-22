"""P1: independent census of the four non-RTL carriers' run bodies at HEAD.

Reads docs.yml/elaborate.yml with PyYAML directly (not through ci_events'
job/step helpers), normalizes each body with an INDEPENDENT implementation
of the item-7 shell normalization, and compares every body with the static
record in HEAD's CARRIER_STEP_LISTS. Also prints each body's lines so the
line population the per-line arms must cover is visible.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata

import yaml

from common import HEAD, load_module, show

CARRIERS = ((".github/workflows/docs.yml", ("docs-check", "wire-accountability",
                                            "docs-check-no-git")),
            (".github/workflows/elaborate.yml", ("elaborate",)))


def independent_normalize(text: str) -> list[str] | None:
    """Shell-style: drop backslash-newline, split on LF, collapse runs of
    space/tab, drop empty lines. Return None when any character other than
    space, tab, LF or a printable one appears (the pin refuses those)."""
    for ch in text:
        if ch in " \t\n":
            continue
        if not ch.isprintable():
            return None
    text = text.replace("\\\n", "")
    out = []
    for raw in text.split("\n"):
        words = [w for w in re.split(r"[ \t]+", raw) if w]
        if words:
            out.append(" ".join(words))
    return out


def main() -> int:
    mod = load_module(HEAD)
    census = []
    problems = []
    for path, jids in CARRIERS:
        wf = yaml.safe_load(show(HEAD, path))
        for jid in jids:
            steps = wf["jobs"][jid]["steps"]
            spec = mod.CARRIER_STEP_LISTS[(path, jid)]
            if len(spec) != len(steps):
                problems.append(f"{jid}: spec {len(spec)} != live {len(steps)}")
            for n, step in enumerate(steps, 1):
                if "run" not in step:
                    continue
                lines = independent_normalize(step["run"])
                rec = spec[n - 1].get("run")
                ok = lines is not None and rec is not None and tuple(lines) == tuple(rec)
                mod_lines = mod.normalize_script(step["run"])
                same_norm = lines == mod_lines
                census.append({"path": path, "job": jid, "step": n,
                               "name": step.get("name"), "lines": lines,
                               "n_lines": len(lines or []),
                               "record_equal": ok,
                               "independent_equals_module_normalize": same_norm,
                               "has_check_flag_lines": [i + 1 for i, l in enumerate(lines or [])
                                                        if re.search(r" --check(?= |$)", l)]})
                if not ok:
                    problems.append(f"{jid} step {n}: record differs from live body")
                if not same_norm:
                    problems.append(f"{jid} step {n}: independent normalization differs")
    per_job = {}
    for row in census:
        per_job.setdefault(row["job"], 0)
        per_job[row["job"]] += 1
    total_lines = sum(r["n_lines"] for r in census)
    nonlast = sum(max(r["n_lines"] - 1, 0) for r in census)
    multi = sum(1 for r in census if r["n_lines"] > 1)
    summary = {"bodies": len(census), "per_job": per_job,
               "total_normalized_lines": total_lines,
               "non_last_lines": nonlast, "multi_command_bodies": multi,
               "all_records_equal": all(r["record_equal"] for r in census),
               "problems": problems}
    json.dump({"summary": summary, "census": census},
              open(sys.argv[1], "w"), indent=1)
    print(json.dumps(summary, indent=1))
    for r in census:
        print(f"{r['job']:20s} step {r['step']:2d} lines {r['n_lines']:2d} "
              f"check-lines {r['has_check_flag_lines']} {r['name']}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
