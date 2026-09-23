#!/usr/bin/env python3
"""Replay the 23 published A172 mutants (correction packet 9f5e84ce,
mutations.json) against the lane working tree's scripts/gen_toc.py.

Each `before` must occur exactly once. Both selftests run in a scratch copy;
every required arm must fail in both consumers.

Usage: replay_a172_mutants.py OUT.json
"""
import json
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mutate import LANE, failing, run  # noqa: E402

PACKET = (Path(__file__).resolve().parent.parent / "public-inputs/review-evidence/437-r1"
          / "correction-a172/mutations.json")


def replay(m: dict) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"a184.a172.{m['name']}.") as d:
        tmp = Path(d)
        shutil.copytree(LANE / "scripts", tmp / "scripts")
        path = tmp / "scripts" / "gen_toc.py"
        src = path.read_text()
        if src.count(m["before"]) != 1:
            return {"name": m["name"], "error": f"before occurs {src.count(m['before'])} times"}
        path.write_text(src.replace(m["before"], m["after"]))
        res = run(tmp)
    missing = {tool: [a for a in m["required_arms"] if a not in res[tool]["failing"]]
               for tool in ("toc", "emdash")}
    return {"name": m["name"], "before": m["before"], "after": m["after"],
            "required_arms": m["required_arms"], **res, "missing": missing,
            "killed": res["toc"]["exit"] == 1 and res["emdash"]["exit"] == 2
            and not missing["toc"] and not missing["emdash"]}


def main() -> int:
    mutants = json.load(open(PACKET))["mutants"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(replay, mutants))
    for r in results:
        print(f"{r['name']:38s} " + (f"ERROR {r['error']}" if "error" in r else
              f"killed={r['killed']} toc={r['toc']['exit']} emdash={r['emdash']['exit']} missing={r['missing']}"))
    Path(sys.argv[1]).write_text(json.dumps(results, indent=1) + "\n")
    return 0 if all(r.get("killed") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
