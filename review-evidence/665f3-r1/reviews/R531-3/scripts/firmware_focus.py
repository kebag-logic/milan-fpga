#!/usr/bin/env python3
"""Plant selected C-only faults and relink the unchanged baseline test objects.

First run test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir PACKET/scratch/firmware.
Only a changed C translation unit is rebuilt; headers and every test object remain baseline bytes.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("root", type=Path)
ap.add_argument("packet", type=Path)
ap.add_argument("--jobs", type=int, default=4)
a = ap.parse_args()
root, packet = a.root.resolve(), a.packet.resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build as b
import ctrl_mutants as mutations
import fw_gtest

names = {
    "acmp-probe-timer-before-its-send", "acmp-taken-probe-timer-from-the-entry-clock",
    "acmp-expiry-due-at-its-first-read", "acmp-owed-probe-timer-runs",
    "acmp-owed-probe-sequence-unchecked", "acmp-stop-keeps-the-hold", "acmp-lost-probe-held",
    "acmp-version-unchecked", "acmp-adp-version-unchecked", "acmp-slot-sum-wraps",
    "acmp-one-slot-for-all-interfaces", "acmp-record-flag-defines-swapped", "acmp-longer-record-applied",
    "acmp-nvm-d3-rollback-drops-bindings", "acmp-due-unsigned", "acmp-earliest-unsigned",
}
table = [m for m in mutations.MUTANTS if m.name in names]
assert {m.name for m in table} == names, names - {m.name for m in table}
baseline = packet / "scratch/firmware/checkout"
main = list((baseline / "harness").glob("*.o"))
assert len(main) == 1

def objects_for(arm):
    if arm == "acmpif2":
        base = baseline / "acmpif2/build"
        dirs = [base / d for d in ("fw", "host", "tests")]
        source = baseline / "acmpif2/ctrl"
    else:
        base = baseline / arm
        dirs = [base, base / "host", base / "tests"]
        if arm == "acmpnvm":
            dirs += [base / "store"]
        source = root / "sw/firmware/ctrl"
    objects = [o for d in dirs for o in sorted(d.glob("*.o"))]
    objects += main
    return objects, source

def probe(m):
    assert m.path.endswith(".c")
    work = packet / "scratch/fw-focus" / m.name
    work.mkdir(parents=True, exist_ok=True)
    original = (root / "sw/firmware/ctrl" / m.path).read_text()
    assert original.count(m.old) == 1, m.name
    changed = work / Path(m.path).name
    changed.write_text(original.replace(m.old, m.new))
    record = {"name": m.name, "path": m.path, "old": m.old, "new": m.new, "outcomes": []}
    for arm in dict.fromkeys(k[0] for k in m.kills()):
        objects, source = objects_for(arm)
        basename = Path(m.path).parent.name + "_" + Path(m.path).stem + ".o"
        matched = [o for o in objects if o.name == basename]
        assert len(matched) == 1, (m.name, arm, matched)
        obj = work / (arm + ".o")
        flags = ["-DCTRL_REENTRY_ASSERT"] if arm in ("acmp", "acmpif2") else []
        includes = [f"-I{source / d}" for d in b.INCLUDE_DIRS] + [f"-I{b.NVM_DIR}"]
        subprocess.run(["gcc", *b.C_FLAGS, *flags, *includes, "-c", str(changed), "-o", str(obj)], check=True)
        linked = [obj if o == matched[0] else o for o in objects]
        exe = work / arm
        subprocess.run(["g++", *map(str, linked), *fw_gtest.TEST_LIBS, "-o", str(exe)], check=True)
        result = b.execute(arm, exe)
        (packet / "receipts" / ("fw-" + m.name + "-" + arm + ".log")).write_text(result.log)
        kills = [k for k in m.kills() if k[0] == arm]
        caught = all(mutations.caught(test, needle, result) for _, test, needle in kills)
        record["outcomes"].append({"arm": arm, "rc": result.rc, "caught": caught,
                                    "required_assertions": kills,
                                    "unchanged_test_objects": {o.name: hashlib.sha256(o.read_bytes()).hexdigest() for o in objects if o.parent.name in ("tests", "harness")}})
    print(m.name, "CAUGHT" if all(o["caught"] for o in record["outcomes"]) else "ESCAPED", flush=True)
    return record

with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    results = list(pool.map(probe, table))
(packet / "receipts/fw-focus.json").write_text(json.dumps(results, indent=2) + "\n")
bad = sum(not all(o["caught"] for o in r["outcomes"]) for r in results)
print("focused firmware faults:", len(results), "caught:", len(results) - bad)
sys.exit(bool(bad))
