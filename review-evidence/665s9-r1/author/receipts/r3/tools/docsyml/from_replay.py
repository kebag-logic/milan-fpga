#!/usr/bin/env python3
"""from_replay.py <replay head dir> <root>: the replay's docs.yml job results as verify_docs_yml.py reads them, root/logs/
<job>__<sid>.rc and .log for each run: step that ran, and not_run.json (beside this file) with each other step's reason."""
import json, shutil, sys
from pathlib import Path
src, root = Path(sys.argv[1]), Path(sys.argv[2])
logs = root / "logs"; logs.mkdir(parents=True, exist_ok=True)
not_run = {}
for res in sorted((src / "jobs").glob("docs__*/result.json")):
    job = res.parent.name.removeprefix("docs__")
    for s in json.loads(res.read_text())["steps"]:
        if s["kind"] != "run":
            continue
        sid, rc = s["step"], s["rc"]
        if isinstance(rc, int):
            (logs / f"{job}__{sid}.rc").write_text(f"{rc}\n")
            shutil.copy2(res.parent / "logs" / f"docs__{job}__{sid}.log", logs / f"{job}__{sid}.log")
        elif rc == "not run":
            not_run[f"{job}/{sid}"] = s["reason"]
        else:
            not_run[f"{job}/{sid}"] = f"{rc}: the step's if: is false for a ready pull_request to dev-soft-core at this head"
Path(__file__).with_name("not_run.json").write_text(json.dumps(not_run, indent=1) + "\n")
print(len(list(logs.glob("*.rc"))), "rc files,", len(not_run), "not run with a reason")
