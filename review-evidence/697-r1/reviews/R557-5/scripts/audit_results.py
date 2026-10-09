#!/usr/bin/env python3
"""Independently summarize executed receipts and retained source identities."""
import collections
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
out = packet / "receipts"
table = json.loads((root / "tests/mutations.json").read_text())

def regrade(results, markers, xml_root=None):
    rows = json.loads(results.read_text())
    assert len(rows) == len(table) == 311
    indexed = {r["name"]: r for r in rows}
    assert len(indexed) == len(rows)
    assert set(indexed) == {r["name"] for r in table}
    begin, end = ["\n" + marker + "\n" for marker in json.loads(markers.read_text())]
    required = 0
    failures = []
    for plant in table:
        row = indexed[plant["name"]]
        assert row["status"] == "CAUGHT" and row["rc"] == 1
        for kill in plant["kills"]:
            required += 1
            matched = False
            messages = row["failures"]
            if xml_root:
                module = Path(plant["path"]).stem
                default = "maap_debug" if any(k["test"].startswith("MaapDebug.") for k in plant["kills"]) else module
                doc = ET.parse(xml_root / plant["name"] / (kill.get("arm", default) + ".xml")).getroot()
                messages = {c.get("classname") + "." + c.get("name"): "\n".join(f.get("message", "") for f in c.findall("failure")) for c in doc.iter("testcase")}
            for name, message in messages.items():
                if not (name.startswith(kill["test"]) if kill["test"].endswith("/") else name == kill["test"]):
                    continue
                for piece in message.split(begin)[1:]:
                    if end in piece and kill["needle"] in piece.split(end, 1)[0]:
                        matched = True
            if not matched:
                failures.append([plant["name"], kill])
    return {"plants": len(rows), "statuses": dict(collections.Counter(r["status"] for r in rows)),
            "required_killers": required, "unmatched_streamed_killers": failures}

summary = {"fresh_mutation": regrade(out / "mutation-results.json", out / "message-markers.json")}
repeat = packet / "scratch/linux/mutations"
if (out / "mutation-reused.rc").exists():
    summary["reused_mutation"] = regrade(repeat / "results.json", repeat / "message-markers.json", repeat)

old = json.loads(subprocess.check_output(["git", "-C", str(root), "show", "625b0011:tests/mutations.json"]))
def ignore_needles(rows):
    return [{**r, "kills": [{k: v for k, v in kill.items() if k != "needle"} for kill in r["kills"]]} for r in rows]
summary["round6_plants_and_killer_names_equal"] = ignore_needles(old) == ignore_needles(table)
summary["changed_needles"] = sum(a["needle"] != b["needle"] for x, y in zip(old, table) for a, b in zip(x["kills"], y["kills"]))

summary["native_instances"] = {}
for name in ("gcc", "clang-sanitizers"):
    log = (packet / "scratch/linux" / name / "Testing/Temporary/LastTest.log").read_text()
    rows = re.findall(r'\[=+\] (\d+) tests? from .* ran\.', log)
    summary["native_instances"][name] = {"binary_counts": [int(v) for v in rows], "total": sum(map(int, rows)), "skipped_lines": [line for line in log.splitlines() if "[  SKIPPED ]" in line]}
    (out / (name + "-instances.log")).write_text(log)

hosted = packet / "scratch/hosted"
if hosted.exists():
    quality = hosted / "quality-evidence"
    summary["hosted"] = {
        "run": "https://github.com/kebag-logic/tsn-c-stack/actions/runs/37909284956",
        "gates": json.loads((quality / "gates.json").read_text()),
        "mutation": regrade(quality / "mutations/results.json", quality / "mutations/message-markers.json"),
        "rv32": json.loads((hosted / "rv32-evidence/results.json").read_text()),
        "graphs": sorted(p.name for p in (quality / "graphs").glob("*.svg")),
    }
    jobs = json.loads((out / "pr-run-jobs.json").read_text())["jobs"]
    summary["hosted"]["job_steps"] = [{"name": j["name"], "head_sha": j["head_sha"], "conclusion": j["conclusion"], "steps": [{"name": s["name"], "conclusion": s["conclusion"]} for s in j["steps"]]} for j in jobs]

(out / "independent-result-audit.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k:v for k,v in summary.items() if k != "hosted"}, indent=2))
if "hosted" in summary:
    print("Hosted", len(summary["hosted"]["gates"]), "gates;", summary["hosted"]["mutation"])
