"""Decompose elaborate jobs-API listings into the components CI_WORKFLOWS.md names.

Usage: python3 -I hosted_components.py JOBS.json [JOBS.json ...]
Setup = job span - gate/leg step - "Build Verilator from source on cache miss" step.
Prints each worker's components and the figures they would replace under the
documented re-measurement rule (SETUP 485, COLD_VERILATOR 431, builder legs
1130/1119, aggregate 19 + 85, collector 149, tail 25)."""
import json, sys
from datetime import datetime

STATED = {"setup": 485, "cold_verilator": 431, "builder_leg_0": 1130, "builder_leg_1": 1119,
          "aggregate_checkout": 19, "aggregate_rest": 85, "collector": 149, "tail": 25}


def ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def span(item):
    start, end = ts(item.get("started_at")), ts(item.get("completed_at"))
    return int((end - start).total_seconds()) if start and end else None


for path in sys.argv[1:]:
    print("##", path)
    for job in sorted(json.load(open(path))["jobs"], key=lambda j: j["name"]):
        name, total = job["name"], span(job)
        steps = {s["name"]: span(s) or 0 for s in job["steps"]}
        gate = sum(v for k, v in steps.items() if k.startswith(("Elaboration gates", "Standalone LiteX")))
        verilator = steps.get("Build Verilator from source on cache miss", 0)
        line = f"{name:28} {job['conclusion']:10} span={total}"
        if name.startswith("elaborate-gates-"):
            setup = total - gate - verilator
            flag = " ABOVE-SETUP" if setup > STATED["setup"] else ""
            vflag = " ABOVE-COLD-VERILATOR" if verilator > STATED["cold_verilator"] else ""
            line += f" gate={gate} verilator={verilator} setup={setup}{flag}{vflag}"
            line += f" checkout={steps.get('Run actions/checkout@v4')} install_litex={steps.get('Install LiteX at the pinned revisions')}"
        elif name == "elaborate":
            checkout = steps.get("Run actions/checkout@v4", 0)
            line += f" checkout={checkout} rest={total - checkout}"
        elif name == "Collect CI manifest":
            line += " ABOVE-COLLECTOR" if total > STATED["collector"] else ""
        elif name == "Cancel late CI failures":
            line += " ABOVE-TAIL" if total > STATED["tail"] else ""
        print(line)
