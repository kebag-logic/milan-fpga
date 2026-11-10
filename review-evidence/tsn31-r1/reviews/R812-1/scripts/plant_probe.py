#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Disposable plant probe for the ACMP owed-release mask (tsn-c-stack issue 31).

usage: plant_probe.py <clean head tree> <scratch work dir> <receipt json>

Each plant is one exact-once text replacement in a private copy of src/ and include/.
For each, the 16-sink acmp_tests binary (as the mutation driver's acmp arm builds it) and the
33-sink acmp_wide binary (ACMP_MAX_SINKS=33u, -fsanitize=shift,undefined, no recovery) are
built and run in full; the receipt records each binary's exit status, failing tests and any
sanitizer report.  The clean tree itself is never written.
"""
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TREE, WORK, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
WIDE = ["-DACMP_MAX_SINKS=33u", "-fsanitize=shift,undefined", "-fno-sanitize-recover=shift,undefined"]
GT = subprocess.check_output(["pkg-config", "--cflags", "gmock", "gtest"], text=True).split()
GL = subprocess.check_output(["pkg-config", "--libs", "gmock", "gtest"], text=True).split()
L_SET = "\t\to->release[(release - 1u) / 32u] = 1u << ((release - 1u) % 32u);"
L_ADD = "\t\ta->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed + ((o->release[k / 32u] >> (k % 32u)) & 1u));"
L_SUB = "\t\t\t\ta->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed - ((o->release[k / 32u] >> (k % 32u)) & 1u));"
BIND = "\trespond(a, interface, &r, k + 1u);\n}\n\n// Milan v1.2 5.5.3.5.3"
PLANTS = {
    "baseline": None,
    # The PR's three new plants, verbatim from tests/mutations.json.
    "acmp-wide-release-word-ignored": ("src/acmp.c", L_SET, "\t\to->release[0] = 1u << ((release - 1u) % 32u);"),
    "acmp-wide-owed-count-word-ignored": ("src/acmp.c", L_ADD, L_ADD.replace("o->release[k / 32u]", "o->release[0]")),
    "acmp-wide-release-loop-word-ignored": ("src/acmp.c", L_SUB, L_SUB.replace("o->release[k / 32u]", "o->release[0]")),
    # Reviewer plants on the same new lines.
    "x-memset-removed": ("src/acmp.c", "\tmemset(o->release, 0, sizeof o->release);\n", ""),
    "x-memset-first-word-only": ("src/acmp.c", "\tmemset(o->release, 0, sizeof o->release);",
                                 "\tmemset(o->release, 0, sizeof o->release[0]);"),
    "x-set-index-off-by-one": ("src/acmp.c", "o->release[(release - 1u) / 32u] =", "o->release[release / 32u] ="),
    "x-set-shift-unmasked":("src/acmp.c", L_SET, "\t\to->release[(release - 1u) / 32u] = 1u << (release - 1u);"),
    "x-add-shift-unmasked": ("src/acmp.c", L_ADD, L_ADD.replace("(k % 32u)", "k")),
    "x-sub-shift-unmasked": ("src/acmp.c", L_SUB, L_SUB.replace("(k % 32u)", "k")),
    "x-add-word-of-next-sink": ("src/acmp.c", L_ADD, L_ADD.replace("o->release[k / 32u]", "o->release[(k + 1u) / 32u]")),
    "x-sub-word-of-next-sink": ("src/acmp.c", L_SUB, L_SUB.replace("o->release[k / 32u]", "o->release[(k + 1u) / 32u]")),
    "x-bind-releases-next-sink": ("src/acmp.c", BIND, BIND.replace("k + 1u", "k + 2u")),
    "x-unbind-releases-nothing": ("src/acmp.c", "\trespond(a, interface, &r, k + 1u);\n\ts->state = ACMP_UNBOUND;",
                                  "\trespond(a, interface, &r, 0u);\n\ts->state = ACMP_UNBOUND;"),
    "x-guard-always": ("src/acmp.c", "\tif (release != 0u) {\n\t\to->release[", "\tif (1) {\n\t\to->release["),
    "x-refusal-off-by-one": ("src/acmp.c", "release * 8u >= ACMP_MAX_SINKS", "release * 8u > ACMP_MAX_SINKS"),
    "x-refusal-removed": ("src/acmp.c", "_Static_assert(sizeof ((struct acmp_owed *)0)->release * 8u >= ACMP_MAX_SINKS,\n\t       \"the owed release mask holds a bit for every sink\");\n", ""),
}


def sh(cmd, log):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=600)
    log.append("$ " + " ".join(cmd) + "\n" + r.stdout)
    return r.returncode, r.stdout


def arm(d, name, sinks_flags, test, log):
    cflags = ["-std=c11", "-O0", "-g", "-Wall", "-Wextra", "-Werror", "-DNDEBUG", "-DCTRL_REENTRY_ASSERT", *sinks_flags]
    cxx = ["-std=c++20", "-O0", "-g", "-Wall", "-Wextra", "-Werror", *sinks_flags]
    rc, out = sh(["gcc", *cflags, "-I" + str(d / "include"), "-c", str(d / "src/acmp.c"), "-o", str(d / (name + ".c.o"))], log)
    if rc:
        return {"build": "C_COMPILE_FAILED", "rc": rc, "diag": [l for l in out.splitlines() if "error" in l][:3]}
    rc, out = sh(["g++", *cxx, *GT, "-I" + str(d / "include"), "-I" + str(TREE / "tests"), "-I" + str(TREE / "examples"),
                  "-c", str(TREE / "tests" / test), "-o", str(d / (name + ".cpp.o"))], log)
    if rc:
        return {"build": "TEST_COMPILE_FAILED", "rc": rc}
    rc, out = sh(["g++", str(d / (name + ".c.o")), str(d / (name + ".cpp.o")), str(WORK / "main.o"), *sinks_flags[1:2], *GL,
                  "-o", str(d / name)], log)
    if rc:
        return {"build": "LINK_FAILED", "rc": rc}
    xml = d / (name + ".xml")
    rc, out = sh([str(d / name), "--gtest_output=xml:" + str(xml)], log)
    failed, total = [], 0
    if xml.exists():
        root = ET.parse(xml).getroot()
        for case in root.iter("testcase"):
            total += 1
            if case.find("failure") is not None:
                failed.append(case.get("classname") + "." + case.get("name"))
    san = [l.strip() for l in out.splitlines() if "runtime error" in l][:2]
    return {"build": "OK", "rc": rc, "tests_in_xml": total, "failed": failed, "sanitizer": san,
            "xml_written": xml.exists()}


def one(item):
    name, plant = item
    d = WORK / name
    shutil.rmtree(d, ignore_errors=True)
    for sub in ("src", "include"):
        shutil.copytree(TREE / sub, d / sub)
    log, row = [], {"plant": name}
    if plant:
        path, old, new = plant
        text = (d / path).read_text()
        row["matches"] = text.count(old)
        if row["matches"] != 1:
            row["error"] = "plant must match exactly once"
            return row
        (d / path).write_text(text.replace(old, new))
    row["acmp_tests_16"] = arm(d, "acmp16", [], "test_acmp.cpp", log)
    row["acmp_wide_33"] = arm(d, "wide33", WIDE, "test_acmp_wide.cpp", log)
    (d / "probe.log").write_text("".join(log))
    return row


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    log = []
    rc, _ = sh(["g++", "-std=c++20", "-O0", "-g", *GT, "-c", str(TREE / "tests/main.cpp"), "-o", str(WORK / "main.o")], log)
    if rc:
        sys.exit("".join(log))
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(one, PLANTS.items()))
    OUT.write_text(json.dumps(rows, indent=1) + "\n")
    for r in rows:
        a, w = r.get("acmp_tests_16", {}), r.get("acmp_wide_33", {})
        print(f"{r['plant']:40s} 16:{a.get('build')} rc={a.get('rc')} failed={len(a.get('failed', []))} | "
              f"33:{w.get('build')} rc={w.get('rc')} failed={w.get('failed')} san={bool(w.get('sanitizer'))} {r.get('error', '')}")


if __name__ == "__main__":
    main()
