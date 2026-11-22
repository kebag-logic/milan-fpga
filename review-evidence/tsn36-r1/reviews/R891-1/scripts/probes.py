#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Disposable fault probes for tsn-c-stack PR #36.

probes.py HEAD_CLONE BASE_CLONE WORK OUT_JSON [--jobs N] [--set main|followup]

Each probe copies a clean clone into WORK/<name>, applies exact single-match
replacements, builds the full CMake test set, runs ctest and the adp_tests
binary, and records which assertion messages failed. Nothing is written to
the clones it copies from.
"""
import argparse
import json
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SITE_OLD = ("\tif (a->enabled && a->state == ADP_STATE_WAITING) {\n"
            "\t\tenter_delay(a, ADP_DRAW_DELAY);                         // Milan v1.2 5.6.3.5.7\n\t}\n")


def site(new_body):
    return ("src/adp.c", SITE_OLD,
            "\tif (a->enabled && a->state == ADP_STATE_WAITING) {\n" + new_body + "\t}\n")


NO_KIND_OLD = ("EXPECT_TRUE(a.state == ADP_STATE_DELAY && a.last_draw == ADP_DRAW_DELAY && fk.last_delay == a.last_draw_ms &&\n"
               "                fk.last_delay <= 4000u)")
NO_KIND_NEW = ("EXPECT_TRUE(a.state == ADP_STATE_DELAY && fk.last_delay == a.last_draw_ms &&\n"
               "                fk.last_delay <= 4000u)")
SYMBOLIC_NEW = ("EXPECT_TRUE(a.state == ADP_STATE_DELAY && a.last_draw == ADP_DRAW_DELAY && fk.last_delay == a.last_draw_ms &&\n"
                "                fk.last_delay <= ADP_DELAY_MAX_MS)")
PLANT = site("\t\tenter_delay(a, ADP_DRAW_STARTUP);                       // Milan v1.2 5.6.3.5.7\n")
NO_NEW_DRAW = site("\t\ttimer_start(a, ADP_TIMER_DELAY, a->last_draw_ms);\n\t\ta->state = ADP_STATE_DELAY;\n")
# A candidate strengthening of the new assertion: require that this GM_CHANGE made exactly one draw.
COUNT_OLD = "    adp_gm_change(&a);\n    EXPECT_TRUE(a.state == ADP_STATE_DELAY && a.last_draw == ADP_DRAW_DELAY"
COUNT_NEW = ("    const uint32_t draws = a.draws;\n    adp_gm_change(&a);\n"
             "    EXPECT_TRUE(a.draws == draws + 1u && a.state == ADP_STATE_DELAY && a.last_draw == ADP_DRAW_DELAY")
COUNTED = ("tests/test_adp.cpp", COUNT_OLD, COUNT_NEW)
FOLLOWUP = {
    "head-counted-clean": ("head", [COUNTED]),
    "head-counted-plant": ("head", [COUNTED, PLANT]),
    "head-counted-no-new-draw": ("head", [COUNTED, NO_NEW_DRAW]),
    "base-no-new-draw": ("base", [NO_NEW_DRAW]),
}

PROBES = {
    # control: the exact head and the exact base, unmodified
    "head-clean": ("head", []),
    "base-clean": ("base", []),
    # the PR's registered plant, on the base (expected to escape) and the head (expected to be caught)
    "base-plant": ("base", [PLANT]),
    "head-plant": ("head", [PLANT]),
    # reviewer's own variants at the same call site
    "head-draw-none": ("head", [site("\t\tenter_delay(a, ADP_DRAW_NONE);\n")]),
    "head-arm-advertise-period": ("head", [site(
        "\t\t(void)draw_ms(a, ADP_DRAW_DELAY);\n\t\ttimer_start(a, ADP_TIMER_DELAY, ADP_ADVERTISE_MS);\n"
        "\t\ta->state = ADP_STATE_DELAY;\n")]),
    "head-arm-twice-the-draw": ("head", [site(
        "\t\ttimer_start(a, ADP_TIMER_DELAY, 2u * draw_ms(a, ADP_DRAW_DELAY));\n\t\ta->state = ADP_STATE_DELAY;\n")]),
    "head-stays-waiting": ("head", [site(
        "\t\ttimer_start(a, ADP_TIMER_DELAY, draw_ms(a, ADP_DRAW_DELAY));\n")]),
    "head-no-new-draw": ("head", [site(
        "\t\ttimer_start(a, ADP_TIMER_DELAY, a->last_draw_ms);\n\t\ta->state = ADP_STATE_DELAY;\n")]),
    # constants (out of scope for the PR; recorded to show which assertions pin them)
    "head-delay-max-500": ("head", [("include/adp.h", "#define ADP_DELAY_MAX_MS 4000u ", "#define ADP_DELAY_MAX_MS 500u  ")]),
    "head-delay-max-8000": ("head", [("include/adp.h", "#define ADP_DELAY_MAX_MS 4000u ", "#define ADP_DELAY_MAX_MS 8000u ")]),
    # test-side: drop the kind conjunct from the new assertion; the registered plant should then escape
    "head-plant-without-kind-conjunct": ("head", [PLANT, ("tests/test_adp.cpp", NO_KIND_OLD, NO_KIND_NEW)]),
    # test-side: the new bound written symbolically, under a widened constant
    "head-symbolic-bound-delay-max-8000": ("head", [
        ("tests/test_adp.cpp", NO_KIND_OLD, SYMBOLIC_NEW),
        ("include/adp.h", "#define ADP_DELAY_MAX_MS 4000u ", "#define ADP_DELAY_MAX_MS 8000u ")]),
}


def run(cmd, cwd, log):
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log.write("$ " + " ".join(map(str, cmd)) + f"\n{r.stdout}\n[rc {r.returncode}]\n")
    return r


def probe(name, spec, clones, work, jobs):
    which, edits = spec
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(clones[which], tree, ignore=shutil.ignore_patterns('.git'))
    result = {"name": name, "tree": which, "edits": []}
    for path, old, new in edits:
        target = tree / path
        text = target.read_text()
        n = text.count(old)
        result["edits"].append({"path": path, "matches": n})
        if n != 1:
            result["status"] = "EDIT-MISMATCH"
            return result
        target.write_text(text.replace(old, new))
    build = tree / "build"
    with open(tree / "probe.log", "w") as log:
        cfg = run(["cmake", "-S", str(tree), "-B", str(build), "-DCMAKE_BUILD_TYPE=Debug",
                   "-DCMAKE_C_COMPILER=gcc", "-DCMAKE_CXX_COMPILER=g++"], tree, log)
        bld = run(["cmake", "--build", str(build), f"-j{jobs}"], tree, log) if cfg.returncode == 0 else cfg
        result["build_rc"] = bld.returncode
        if bld.returncode != 0:
            result["status"] = "BUILD-FAILED"
            return result
        ct = run(["ctest", "--test-dir", str(build), f"-j{jobs}"], tree, log)
        result["ctest_rc"] = ct.returncode
        result["ctest_failed"] = sorted(set(re.findall(r"\d+ - (\S+) \(Failed\)", ct.stdout)))
        m = re.search(r"(\d+)% tests passed, (\d+) tests failed out of (\d+)", ct.stdout)
        result["ctest_summary"] = m.group(0) if m else None
        adp = run([str(build / "adp_tests"), "--gtest_filter=AdpCore.*"], tree, log)
        result["adp_core_rc"] = adp.returncode
        result["adp_failed_tests"] = sorted(set(re.findall(r"^\[  FAILED  \] (AdpCore\.\S+)", adp.stdout, re.M)))
        # every A-numbered assertion message that printed in a failure block
        result["adp_failure_messages"] = sorted(set(
            line.strip() for line in adp.stdout.splitlines() if re.match(r"\s*A\d+ ", line)))
    result["status"] = "FAILS" if result["ctest_rc"] != 0 else "PASSES"
    shutil.rmtree(build)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("head")
    ap.add_argument("base")
    ap.add_argument("work", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--jobs", type=int, default=16)
    ap.add_argument("--set", choices=("main", "followup"), default="main")
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    clones = {"head": Path(a.head), "base": Path(a.base)}
    per = max(1, a.jobs // 4)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda kv: probe(kv[0], kv[1], clones, a.work, per), (PROBES if a.set == "main" else FOLLOWUP).items()))
    a.out.write_text(json.dumps(results, indent=2) + "\n")
    for r in results:
        print(r["name"], r["status"], r.get("ctest_failed"), r.get("adp_failed_tests"))
        for msg in r.get("adp_failure_messages", []):
            print("    ", msg)


if __name__ == "__main__":
    main()
