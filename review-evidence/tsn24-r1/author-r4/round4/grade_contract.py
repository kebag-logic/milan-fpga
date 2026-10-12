#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reconcile every contract row with complete-suite XML and a physical removal."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

BINARIES = {"adp_tests", "acmp_tests", "maap_tests", "entity_tests", "port_tests",
            "adp_release", "adp_debug", "maap_debug"}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def xml_cases(work, tag):
    paths = sorted(work.glob("w*/build/" + tag + "-*.xml"))
    require(len(paths) == 8, tag + ": missing or duplicated binary XML")
    cases, failed, receipts = set(), {}, []
    for path in paths:
        binary = path.name[len(tag) + 1:-4]
        require(binary in BINARIES, "unknown binary " + binary)
        root = ET.parse(path).getroot()
        require(root.tag == "testsuites", "invalid root")
        require(int(root.get("errors", "0")) == 0 and int(root.get("disabled", "0")) == 0,
                "errors or disabled tests")
        entries = root.findall(".//testcase")
        require(len(entries) == int(root.get("tests")), "test count mismatch")
        for case in entries:
            name = case.get("classname") + "." + case.get("name")
            key = (binary, name)
            require(key not in cases, "duplicate case")
            require(case.get("status") == "run" and case.get("result") == "completed"
                    and case.find("skipped") is None, "incomplete case " + name)
            cases.add(key)
            failures = case.findall("failure")
            if failures:
                failed[key] = "\n".join(f.get("message", "") + (f.text or "") for f in failures)
        data = path.read_bytes()
        receipts.append({"path": str(path.relative_to(work)), "size": len(data),
                         "sha256": hashlib.sha256(data).hexdigest()})
    return cases, failed, receipts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    args = ap.parse_args()
    work = args.work.resolve()
    registry = {p["name"]: p for p in json.loads((args.repo / "tests/mutations.json").read_text())}
    rows = []
    for line in (args.repo / "docs/VERIFICATION.md").read_text().splitlines():
        if re.match(r"\| [PR][0-9]{2} \|", line):
            cells = [s.strip() for s in line.split("|")[1:-1]]
            names = re.findall(r"`([^`]+)`", cells[3])
            tests = set(re.findall(r"`([^`]+)`", cells[2]))
            require(tests == {k["test"] for n in names for k in registry[n]["kills"]},
                    "table/registry mismatch in " + cells[0])
            if not names:
                require("No " in cells[1], "unexplained no-test row")
            rows.append({"row": cells[0], "sentence": cells[1], "plants": names,
                         "killers": sorted(tests)})
    require([r["row"] for r in rows] == ["P%02d" % n for n in range(1, 30)] + ["R01", "R02"],
            "sentence row inventory mismatch")
    names = {n for r in rows for n in r["plants"]}
    plants = json.loads((work / "plants_contract.json").read_text())
    require({p["name"] for p in plants} == names, "plant list misses a contract row")
    for p in plants:
        r = registry[p["name"]]
        require(all(p[k] == r[k] for k in ("path", "old", "new")), "changed substitution")
        require(p["killer"] == r["kills"][0]["test"] and p["needle"] == r["kills"][0]["needle"],
                "changed killer")
    results = json.loads((work / "contract-results.json").read_text())
    result_map = {(r["plant"], r["mode"]): r for r in results}
    require(len(result_map) == len(results) == 2 * len(plants) + 1, "result inventory mismatch")
    baseline, failures, baseline_xml = xml_cases(work / "contract", "control-control")
    control = result_map[None, "control"]
    require(not failures and control["build_rc"] == 0 and control["tests"] == len(baseline),
            "control failed")
    receipt_dir = work / "contract-receipts"
    receipt_dir.mkdir(exist_ok=True)
    summary = []
    for p in plants:
        name, killer = p["name"], p["killer"]
        full, removed = result_map[name, "full"], result_map[name, "removed"]
        for result in (full, removed):
            require(result["build_rc"] == 0 and result["skipped"] == result["disabled"] == 0,
                    name + ": bad build or incomplete suite")
            require(set(result["binaries"]) == BINARIES, name + ": binary list differs")
        full_cases, full_failed, full_xml = xml_cases(work / "contract", name + "-full")
        removed_cases, removed_failed, removed_xml = xml_cases(work / "contract", name + "-removed")
        require(full_cases == baseline and full["tests"] == len(baseline), name + ": full registration differs")
        require({key[1] for key in full_failed} == {killer} and full["only_killer"]
                and full["needle_seen"] and full["caught"], name + ": missing unique catch")
        require(all(p["needle"] in message for message in full_failed.values()), name + ": needle absent")
        missing = {key for key in baseline if key[1] == killer}
        require(len(missing) == 1, name + ": not a single instance")
        require(removed_cases == baseline - missing and not removed_failed and removed["escapes"]
                and removed["tests"] == len(baseline) - 1, name + ": no physical removal escape")
        for binary in BINARIES:
            expected = 1 if any(key[0] == binary for key in full_failed) else 0
            require(full["binaries"][binary]["rc"] == expected
                    and removed["binaries"][binary]["rc"] == 0, name + ": unexpected process exit")
        receipt = dict(plant=name, killer=killer, needle=p["needle"], full_instances=len(full_cases),
                       removed_instances=len(removed_cases), full_failures=[killer], escapes=True,
                       full_xml=full_xml, removed_xml=removed_xml)
        (receipt_dir / (name + ".json")).write_text(json.dumps(receipt, indent=2) + "\n")
        summary.append({k: v for k, v in receipt.items() if not k.endswith("_xml")})
    for row in rows:
        row["result"] = "CAUGHT and escapes after only its killer is removed" if row["plants"] else "Inspection / caller obligation"
    (work / "contract-row-results.json").write_text(json.dumps(rows, indent=2) + "\n")
    (work / "contract-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (work / "baseline-xml.json").write_text(json.dumps(baseline_xml, indent=2) + "\n")
    print(f"{len(rows)} sentence rows; {len(plants)} plants; {len(baseline)} full / {len(baseline) - 1} removed instances; all passed")


if __name__ == "__main__":
    main()
