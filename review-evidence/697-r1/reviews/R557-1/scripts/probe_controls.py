#!/usr/bin/env python3
"""Exercise reviewer-owned controls exclusively in disposable copies."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repository", type=Path)
p.add_argument("work", type=Path)
p.add_argument("baseline_campaign", type=Path)
a = p.parse_args()
root, work = a.repository.resolve(), a.work.resolve()
work.mkdir(parents=True, exist_ok=True)
def run(command, cwd):
    r = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    return {"rc": r.returncode, "output": r.stdout}
records = {}

boundary = work / "boundary"
for name in ("src", "include", "scripts"):
    shutil.copytree(root/name, boundary/name, dirs_exist_ok=True)
control = boundary/"src/review_control.c"
control.write_text('#include <unistd.h>\nint review_control(void) { return (int)getpid(); }\n')
records["boundary_normal_outside_include"] = run(["python3", "scripts/check_boundary.py", "--selftest"], boundary)
control.write_text('%:include <unistd.h>\nint review_control(void) { return (int)getpid(); }\n')
records["boundary_digraph_outside_include"] = run(["python3", "scripts/check_boundary.py", "--selftest"], boundary)
records["boundary_digraph_compiles"] = run(["gcc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-pedantic-errors", "-fsyntax-only", "src/review_control.c"], boundary)

trace = work / "trace"
for name in ("tests", "docs", "scripts", "include", "src"):
    shutil.copytree(root/name, trace/name, dirs_exist_ok=True)
test = trace/"tests/test_adp.cpp"
original = test.read_text()
test.write_text(original+'\n// REQ: UNKNOWN-REVIEW-ID\nTEST(ReviewControl, UnrecognizedRequirement) { SUCCEED(); }\n')
records["trace_unindented_unknown"] = run(["python3", "scripts/traceability.py", "--selftest"], trace)
test.write_text(original+'\n// REQ: UNKNOWN-REVIEW-ID\n TEST(ReviewControl, UnrecognizedRequirement) { SUCCEED(); }\n')
records["trace_indented_unknown"] = run(["python3", "scripts/traceability.py", "--selftest"], trace)
records["inventory_indented_unmapped"] = run(["python3", "scripts/test_inventory.py"], trace)
records["trace_indented_compiles"] = run(["g++", "-std=c++20", "-Wall", "-Wextra", "-Werror", "-Iinclude", "-fsyntax-only", "tests/test_adp.cpp"], trace)
binary = trace/"indented-test"
records["trace_indented_links"] = run(["g++", "-std=c++20", "-Wall", "-Wextra", "-Werror", "-Iinclude", "tests/test_adp.cpp", str(a.baseline_campaign.resolve()/"baseline/main.o"), str(a.baseline_campaign.resolve()/"baseline/adp.c.o"), "-lgmock", "-lgtest", "-pthread", "-o", str(binary)], trace)
records["trace_indented_runs"] = run([str(binary), "--gtest_filter=ReviewControl.*"], trace)

stale = work/"stale"
for name in ("tests", "examples", "include", "src", "scripts"):
    shutil.copytree(root/name, stale/name, dirs_exist_ok=True)
plants = json.loads((root/"tests/mutations.json").read_text())
plant = next(m for m in plants if m["name"] == "departing-keeps-index")
records["stale_original_plant"] = json.loads(json.dumps(plant))
plant["new"] = plant["old"] + "\texit(1);\n"
(stale/"tests/mutations.json").write_text(json.dumps([plant]))
source = stale/"src/adp.c"
source.write_text(source.read_text().replace('#include <string.h>', '#include <string.h>\n#include <stdlib.h>'))
campaign = stale/"campaign"
shutil.copytree(a.baseline_campaign/plant["name"], campaign/plant["name"], dirs_exist_ok=True)
fingerprint = lambda: {x.name: {"sha256": hashlib.sha256(x.read_bytes()).hexdigest(), "mtime_ns": x.stat().st_mtime_ns} for x in (campaign/plant["name"]).glob("*.xml")}
before = fingerprint()
records["stale_campaign"] = run(["python3", "scripts/mutation.py", "--work", "campaign", "--jobs", "4"], stale)
records["stale_campaign_results"] = json.loads((campaign/"results.json").read_text())
records["stale_xml_unchanged"] = before == fingerprint()
for x in (campaign/plant["name"]).glob("*.xml"):
    x.unlink()
records["fresh_campaign"] = run(["python3", "scripts/mutation.py", "--work", "campaign", "--jobs", "4"], stale)
records["fresh_campaign_results"] = json.loads((campaign/"results.json").read_text())
print(json.dumps(records, indent=2))
