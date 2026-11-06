#!/usr/bin/env python3
"""List every run step of .github/workflows/docs.yml as job|index|name|env-keys|run (JSON lines)."""
import json, sys, yaml
wf = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
for job, spec in wf["jobs"].items():
    for i, st in enumerate(spec.get("steps", [])):
        if "run" in st:
            print(json.dumps({"job": job, "i": i, "name": st.get("name", ""), "if": st.get("if"),
                              "env": sorted((st.get("env") or {}).keys()), "run": st["run"]}))
