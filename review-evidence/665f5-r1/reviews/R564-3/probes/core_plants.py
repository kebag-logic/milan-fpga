# Reviewer plants for PR #700 round 3 (SET_STREAM_INFO without a sub-command).
# Usage: python3 -B core_plants.py <repo-root> <output-dir> [--jobs N]
# Each plant edits an isolated copy of sw/firmware/ctrl under <output-dir>, runs the
# complete composed AECP suite (no test filter) at one and two interfaces, and records
# every failing test plus whether each expected diagnostic appears inside it.
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

PLANTS = [
    # name, file, old, new, [(test, diagnostic words)]
    ("R564-2.nosub-applies-request-latency", "aecp/aecp_commands.c",
     "\t\tif ((requested & 0x20000000u) == 0u) {\n",
     "\t\tif ((requested & 0x20000000u) == 0u) {\n"
     "\t\t\ta->cfg.latency[index] = (uint32_t)wire_be32(in + 24); aecp_override(a, d, 2u);\n",
     [("Core.SetStreamInfoWithoutSubcommandPreservesState", "no subcommand preserves stored latency")]),
    ("R564-2.nosub-reports-request-latency", "aecp/aecp_commands.c",
     "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n",
     "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4); memcpy(out + 24, in + 24, 4u);\n",
     [("Core.SetStreamInfoWithoutSubcommandPreservesState",
       "no subcommand reports current latency, not requested latency")]),
    ("X1.nosub-sets-latency-valid", "aecp/aecp_commands.c",
     "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n",
     "\t\t\twire_put_be(out + 4, flags | 0x20000000u, 4);\n",
     [("Core.SetStreamInfoWithoutSubcommandPreservesState", "latency valid follows the request")]),
    ("X2.nosub-writes-store-only", "aecp/aecp_commands.c",
     "\t\tif ((requested & 0x20000000u) == 0u) {\n",
     "\t\tif ((requested & 0x20000000u) == 0u) {\n"
     "\t\t\ta->cfg.latency[index] = (uint32_t)wire_be32(in + 24);\n",
     [("Core.SetStreamInfoWithoutSubcommandPreservesState", "no subcommand preserves stored latency")]),
    ("X3.nosub-marks-override-only", "aecp/aecp_commands.c",
     "\t\tif ((requested & 0x20000000u) == 0u) {\n",
     "\t\tif ((requested & 0x20000000u) == 0u) {\n\t\t\taecp_override(a, d, 2u);\n",
     [("Core.SetStreamInfoWithoutSubcommandPreservesState", "no subcommand preserves saved override")]),
    ("X4.current-latency-ignores-override", "aecp/aecp_commands.c",
     "type == 6u && aecp_overridden(a, d, 2u) ? a->cfg.latency[index] : info.latency",
     "info.latency",
     [("Core.SetStreamInfoWithoutSubcommandPreservesState",
       "no subcommand reports current latency, not requested latency")]),
    ("X5.nosub-refused", "aecp/aecp_commands.c",
     "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n\t\t\treturn AECP_SUCCESS;\n",
     "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n\t\t\treturn AECP_NOT_SUPPORTED;\n",
     [("Core.SetStreamInfoWithoutSubcommandPreservesState", "status for command 14")]),
    ("X6.subcommand-echo-dropped", "aecp/aecp_commands.c",
     "\t\twire_put_be(out + 24, latency, 4); // Milan preserves the requested latency.\n",
     "\n",
     [("Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal",
       "SET latency follows Milan success and current refusal rules")]),
    ("X7.nosub-bypasses-running-and-lock", "aecp/aecp_commands.c",
     "\t\tif (info.running) {\n",
     "\t\tif ((wire_be32(in + 4) & 0xfaf80000u) == 0u) {\n"
     "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n"
     "\t\t\treturn AECP_SUCCESS;\n"
     "\t\t}\n"
     "\t\tif (info.running) {\n",
     [("Core.ConfigurationAndLockedSetRefusals", "status for command 14")]),
    ("X8.nosub-bypasses-running-only", "aecp/aecp_commands.c",
     "\t\tif (info.running) {\n",
     "\t\tif ((wire_be32(in + 4) & 0xfaf80000u) == 0u && !aecp_foreign_lock(a)) {\n"
     "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n"
     "\t\t\treturn AECP_SUCCESS;\n"
     "\t\t}\n"
     "\t\tif (info.running) {\n",
     [("any", "STREAM_IS_RUNNING for a no-sub-command SET")]),
    ("X9.nosub-bypasses-input-refusal", "aecp/aecp_commands.c",
     "\t\tif (type == 5u) {\n\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n",
     "\t\tif (type == 5u && (wire_be32(in + 4) & 0xfaf80000u) != 0u) {\n\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n",
     [("any", "NOT_SUPPORTED for a no-sub-command SET to a STREAM_INPUT")]),
]


def run_plant(args):
    repo, out, plant, interfaces, jobs = args
    name, path, old, new, checks = plant
    sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
    sys.path.insert(0, str(repo / "sw/firmware/gtest"))
    import aecp_arms
    import fw_gtest
    from ctrl_build import CTRL, Tree, Refusal
    root = out / f"{name}-if{interfaces}"
    src = root / "work/ctrl"
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    target = src / path
    text = target.read_text()
    sites = text.count(old)
    if name != "baseline":
        if sites != 1:
            return {"plant": name, "interfaces": interfaces, "error": f"{sites} planting sites"}
        target.write_text(text.replace(old, new))
    tree = Tree(src, root / "work/build", root / "work/reuse", fw_gtest.Build(jobs=jobs))
    config = repo / "configs/endstation_ax7101_1x1_tdm8.yaml"
    try:
        result = aecp_arms.core_arm(tree, config, interfaces, "app", "*")
    except Refusal as error:
        (root / "run.log").write_text(str(error))
        return {"plant": name, "interfaces": interfaces, "error": "build refusal"}
    (root / "run.log").write_text(result.log)
    failed = sorted(set(re.findall(r"^\[  FAILED  \] (\S+) \(", result.log, re.M)))
    summary = re.findall(r"^\[==========\] (\d+) tests? from .* ran", result.log, re.M)
    diagnosed = {}
    for test, words in checks:
        m = re.search(r"\[ RUN      \] " + re.escape(test) + r"\n(.*?)\[  FAILED  \] " + re.escape(test) + r" \(",
                      result.log, re.S)
        diagnosed[f"{test}: {words}"] = bool(m and words in m[1])
    return {"plant": name, "interfaces": interfaces, "rc": result.rc, "tests_ran": summary,
            "failed_tests": failed, "expected_diagnostics": diagnosed,
            "killed": result.rc != 0 and all(diagnosed.values())}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--only", nargs="*", default=None)
    a = ap.parse_args()
    repo, out = a.repo.resolve(), a.out.resolve()
    plants = [("baseline", "aecp/aecp_commands.c", "", "", [])] + PLANTS
    if a.only:
        plants = [p for p in plants if p[0] in a.only]
    work = [(repo, out, p, n, a.jobs) for p in plants for n in (1, 2)]
    with ProcessPoolExecutor(a.workers) as pool:
        results = list(pool.map(run_plant, work))
    (out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    bad = 0
    for r in results:
        if r["plant"] == "baseline":
            ok = r.get("rc") == 0
        else:
            ok = r.get("killed", False)
        bad += not ok
        print(f"[{'ok' if ok else 'FAIL'}] {r['plant']} if{r['interfaces']}: rc={r.get('rc')} "
              f"err={r.get('error')} failed={r.get('failed_tests')} diag={r.get('expected_diagnostics')}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
