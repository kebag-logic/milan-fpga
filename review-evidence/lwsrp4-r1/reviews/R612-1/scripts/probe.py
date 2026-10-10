#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Apply one textual plant to a fresh copy of a source tree, build libshlan, run behave.

Usage: probe.py SRC_TREE WORK_ROOT PREFIX [STEPS_TREE]
STEPS_TREE (optional) supplies tests/features/{environment.py,steps/} (e.g. the base tree).
"""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

B = "tests/features/switch_bindings.c"
ENV = "tests/features/environment.py"
PLANTS = [
    # name, file, old, new, expectation (KILL or SURVIVE), family
    ("disable-via-ops-enable", B, "    return shlan_port_disable(sw, port_id);",
     "    return sw->ops->port_enable(sw, port_id);", "KILL", "disable"),
    ("disable-noop", B, "    return shlan_port_disable(sw, port_id);",
     "    (void)port_id;\n    return sw ? 0 : 1;", "KILL", "disable"),
    ("disable-ignores-port", B, "    return shlan_port_disable(sw, port_id);",
     "    (void)port_id;\n    return shlan_port_disable(sw, 0u);", "SURVIVE", "disable"),
    ("disable-reconnects", B, "    return shlan_port_disable(sw, port_id);",
     "    (void)port_id;\n    return shlan_connect(sw);", "SURVIVE", "disable"),
    ("connect-returns-zero", B, "    return shlan_connect(sw);",
     "    return sw == 0;", "KILL", "connect"),
    ("connect-clears-port0-only", B, "    return shlan_connect(sw);",
     "    return shlan_port_disable(sw, 0u);", "KILL", "connect"),
    ("connect-reports-failure", B, "    return shlan_connect(sw);",
     "    (void)shlan_connect(sw);\n    return 1;", "KILL", "connect"),
    ("enable-modulo-range", B, "    return shlan_port_enable(sw, port_id);",
     "    return shlan_port_enable(sw, (uint8_t)(port_id % 48u));", "KILL", "enable"),
    ("enable-also-next", B, "    return shlan_port_enable(sw, port_id);",
     "    (void)shlan_port_enable(sw, (uint8_t)(port_id + 1u));\n    return shlan_port_enable(sw, port_id);", "KILL", "enable"),
    ("enable-accepts-out-of-range", B, "    return shlan_port_enable(sw, port_id);",
     "    if (port_id >= 48u) {\n        return 0;\n    }\n    return shlan_port_enable(sw, port_id);", "KILL", "enable"),
    ("enable-mapped-to-disable", ENV, 'getattr(lib, f"shlan_test_{name}")',
     'getattr(lib, "shlan_test_" + {"port_enable": "port_disable"}.get(name, name))', "KILL", "enable"),
    ("disconnect-enables-port5", B, "    shlan_disconnect(sw);",
     "    (void)shlan_port_enable(sw, 5u);", "KILL", "disconnect"),
    ("disconnect-noop", B, "    shlan_disconnect(sw);", "    (void)sw;", "SURVIVE", "disconnect"),
    # layout probes
    ("layout-extra-field", "src/modules/sim_adapter.c", "struct sim_priv {\n",
     "struct sim_priv {\n    int generation;\n", "KILL", "layout"),
    ("layout-64-ports", "src/modules/sim_adapter.c", "#define SIM_MAX_PORTS 48",
     "#define SIM_MAX_PORTS 64", "SURVIVE", "layout"),
    ("layout-switch-swapped", "src/include/shish_lan/switch.h",
     "    const struct shlan_switch_ops *ops;\n    void                          *priv; /* adapter-private data */",
     "    void                          *priv; /* adapter-private data */\n    const struct shlan_switch_ops *ops;",
     "KILL", "layout"),
]

def failed(out):
    names, listing = set(), False
    for line in out.splitlines():
        if line in ("Failing scenarios:", "Errored scenarios:"):
            listing = True
        elif listing and line.startswith("  "):
            names.add(line.split("  ")[-1])
        else:
            listing = False
    return sorted(names)

def main():
    src, root, prefix = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    steps = Path(sys.argv[4]) if len(sys.argv) > 4 else None
    only = os.environ.get("ONLY")
    root.mkdir(parents=True, exist_ok=False)
    results = []
    for name, rel, old, new, expect, fam in PLANTS:
        if only and name not in only.split(","):
            continue
        tree = root / name / "src"
        shutil.copytree(src, tree, ignore=shutil.ignore_patterns("__pycache__"))
        if steps:
            shutil.copy2(steps / ENV, tree / ENV)
            shutil.rmtree(tree / "tests/features/steps")
            shutil.copytree(steps / "tests/features/steps", tree / "tests/features/steps")
        path = tree / rel
        text = path.read_text()
        n = text.count(old)
        assert n == 1, f"{name}: target occurs {n} times"
        path.write_text(text.replace(old, new))
        build = root / name / "build"
        log = []
        r = subprocess.run(["cmake", "-S", str(tree), "-B", str(build), "-DCMAKE_BUILD_TYPE=Debug",
                            f"-DCMAKE_PREFIX_PATH={prefix}"], capture_output=True, text=True)
        log.append(r.stdout + r.stderr)
        r2 = subprocess.run(["cmake", "--build", str(build), "--target", "shlan", "--parallel", "2"],
                            capture_output=True, text=True)
        log.append(r2.stdout + r2.stderr)
        env = dict(os.environ, SHLAN_LIBRARY=str(build / "libshlan.so"))
        r3 = subprocess.run([sys.executable, "-m", "behave", "--no-color", "tests/features"],
                            cwd=tree, env=env, capture_output=True, text=True, timeout=300)
        out = r3.stdout + r3.stderr
        (root / name / "behave.log").write_text(out)
        (root / name / "build.log").write_text("\n".join(log))
        asserts = sorted(set(l.strip() for l in out.splitlines()
                             if l.strip().startswith(("Assertion Failed:", "ASSERT FAILED:", "AssertionError"))
                             or "after " in l or "returned" in l or "no longer matches" in l))
        outcome = "KILLED" if r3.returncode != 0 else "SURVIVED"
        rec = dict(plant=name, family=fam, file=rel, configure_rc=r.returncode, build_rc=r2.returncode,
                   behave_rc=r3.returncode, outcome=outcome, expected=expect,
                   as_expected=(outcome == "KILLED") == (expect == "KILL") and r2.returncode == 0,
                   failing_or_errored=failed(out), messages=asserts[:8],
                   summary=[l for l in out.splitlines() if re.match(r"^\d+ (feature|scenario|step)", l)])
        results.append(rec)
        print(json.dumps(rec), flush=True)
    (root / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
