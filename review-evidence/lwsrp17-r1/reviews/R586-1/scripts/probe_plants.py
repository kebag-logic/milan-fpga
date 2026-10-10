# SPDX-License-Identifier: Apache-2.0
"""Reviewer-owned planted defects for lwSRP PR #18, independent of the author's
tests/check_reversals.py cases. Each plant is applied to its own scratch copy
(never the checkout), built, and the unit runner's failing tests are listed.

Usage: probe_plants.py <checkout> <cgreen-prefix> <work-dir> <jobs> [<base-mrp_mad.c>]
"""
import concurrent.futures as cf
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

MAD = "src/core/mrp_mad.c"
PLANTS = [
    # (label, defect class, old, new)
    ("R1-base-encoder", "split Message (per-value Messages, the old encoder)", None, None),
    ("R2-no-list-endmark", "wrong EndMark count (no AttributeList EndMark)",
     "    end[0] = 0; end[1] = 0;\n    end += 2;\n", ""),
    ("R3-sort-ignores-last-octet", "wrong vector order (partial key)",
     "memcmp(at - size + 2, at + 2, len) > 0", "memcmp(at - size + 2, at + 2, len - 1u) > 0"),
    ("R3b-no-sort", "wrong vector order (list order)",
     "for (uint8_t *at = v; at > first &&", "for (uint8_t *at = v; false && at > first &&"),
    ("R4-drop-values-under-leaveall", "dropped vector (values after LeaveAll)",
     "    uint8_t *first = v;\n", "    uint8_t *first = v;\n    if (la) { return tx_close(ops, buf, v); }\n"),
    ("R4b-drop-list-head", "dropped vector (newest declaration)",
     "if (!a->tx_selected || a->attr_type != type || e->tx == TX_MSG_NONE)",
     "if (!a->tx_selected || a->attr_type != type || a == ps->attrs || e->tx == TX_MSG_NONE)"),
    ("R5-cost-misses-endmark", "sizing under-count (overrun)",
     "                    n += hdr + 2u;\n", "                    n += hdr;\n"),
    ("R6-cost-per-value", "sizing over-count (old per-value cost)",
     "                if (!tx_type_in(types.open, a->attr_type)) {\n                    n += hdr + 2u;\n                }\n",
     "                n += hdr + 2u;\n"),
    ("R7-descending-types", "Message order",
     "for (unsigned type = 0; type < 256u; ++type) {\n        if (!tx_type_in(types->open, type))",
     "for (unsigned type = 256u; type-- > 0;) {\n        if (!tx_type_in(types->open, type))"),
    ("R8-list-length-excludes-endmark", "AttributeListLength",
     "size_t list = (size_t)(end - message) - 4u;", "size_t list = (size_t)(end - message) - 6u;"),
    ("R9-writes-unselected-events", "event semantics (TX none written)",
     "if (!a->tx_selected || a->attr_type != type || e->tx == TX_MSG_NONE)",
     "if (!a->tx_selected || a->attr_type != type)"),
    ("R10-leaveall-cost-misses-vector", "sizing under-count under LeaveAll",
     "size_t n = hdr + tx_vector_len(ops, (uint8_t)type, true) + 2u;", "size_t n = hdr + 2u;"),
    ("R11-leaveall-vector-carries-values", "LeaveAll form (NumberOfValues 0 dropped)",
     "        v[0] = 0x20; v[1] = 0;\n", "        v[0] = 0x20; v[1] = 1;\n"),
]


def run(cmd, cwd, env, log):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=600)
    log.write_text(r.stdout + r.stderr)
    return r.returncode, r.stdout + r.stderr


def one(plant, root, prefix, work, base_mad):
    label, klass, old, new = plant
    tree = work / label
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    for name in ["CMakeLists.txt", "src", "tests"]:
        p = root / name
        (shutil.copytree if p.is_dir() else shutil.copy2)(p, tree / name)
    target = tree / MAD
    text = target.read_text()
    if old is None:
        shutil.copy2(base_mad, target)
    else:
        if text.count(old) != 1:
            return {"label": label, "class": klass, "error": f"target occurs {text.count(old)} times"}
        target.write_text(text.replace(old, new))
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = str(prefix / "lib")
    build = tree / "build"
    rc, _ = run(["cmake", "-S", str(tree), "-B", str(build), "-DCMAKE_BUILD_TYPE=Debug",
                 f"-DCMAKE_PREFIX_PATH={prefix}", "-DLWSRP_MILAN=OFF"], tree, env, work / f"{label}.configure.log")
    if rc:
        return {"label": label, "class": klass, "error": "configure"}
    rc, _ = run(["cmake", "--build", str(build), "--parallel", "2", "--target", "unit_tests"], tree, env,
                work / f"{label}.build.log")
    if rc:
        return {"label": label, "class": klass, "build_rc": rc, "killed": False}
    try:
        rc, out = run([str(build / "unit_tests")], build, env, work / f"{label}.unit.log")
    except subprocess.TimeoutExpired:
        return {"label": label, "class": klass, "unit_rc": "timeout", "killed": True, "failing": []}
    failing = sorted(set(re.findall(r"Failure: [a-z_]+ -> ([a-z_0-9]+)", out)) |
                     set(re.findall(r"Exception: [a-z_]+ -> ([a-z_0-9]+)", out)))
    return {"label": label, "class": klass, "unit_rc": rc, "killed": rc != 0,
            "failing_count": len(failing), "failing": failing}


def main():
    root, prefix, work = (Path(a).resolve() for a in sys.argv[1:4])
    jobs = int(sys.argv[4])
    base_mad = Path(sys.argv[5]).resolve() if len(sys.argv) > 5 else None
    work.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(jobs) as pool:
        results = list(pool.map(lambda p: one(p, root, prefix, work, base_mad), PLANTS))
    (work / "plants.json").write_text(json.dumps(results, indent=2) + "\n")
    survived = 0
    for r in results:
        state = "KILLED" if r.get("killed") else "SURVIVED"
        survived += not r.get("killed")
        print(f"{state} {r['label']} [{r['class']}] rc={r.get('unit_rc', r.get('error', r.get('build_rc')))} "
              f"failing={r.get('failing_count', 0)}: {' '.join(r.get('failing', []))}")
    print(f"plants: {len(results)}; survived: {survived}")
    return int(survived != 0)


if __name__ == "__main__":
    sys.exit(main())
