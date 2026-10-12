#!/usr/bin/env python3
"""Planted driver defects against the head's shard self-test and the independent
dev-vs-head dispatch comparison. Each probe extracts HEAD into a fresh scratch root,
edits sw/firmware/ctrl/test/test_ctrl_firmware.py, then runs (a) the head's
test_ctrl_firmware_shards.py from that root and (b) dev_vs_head_dispatch.py against it.
Usage: driver_probes.py CLONE HEAD_SHA DEV_DRIVER SCRATCH OUT_JSON
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

clone, sha, dev_driver, scratch, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4]), Path(sys.argv[5])
HERE = Path(__file__).resolve().parent
D = "sw/firmware/ctrl/test/test_ctrl_firmware.py"
PROBES = {
    "control-no-edit": ("", ""),
    "srpcmp-also-in-srp-phase": ("    lwsrp = args.lwsrp.resolve()\n",
                                 "    lwsrp = args.lwsrp.resolve()\n    ctrl_arms.arm_srpcmp()\n"),
    "srp-phase-dropped-from-shards": ('    return PHASES if shard is None else (PHASES[shard[0]],)',
                                      '    return PHASES if shard is None else (() if shard[0] == 3 else (PHASES[shard[0]],))'),
    "control-phase-also-in-aecp-shard": ('    return PHASES if shard is None else (PHASES[shard[0]],)',
                                         '    return PHASES if shard is None else ((PHASES[shard[0]],) if shard[0] != 2 else ("control", "aecp"))'),
    "future-suite-added": ("                ctrl_arms.arm_srpcmp()]",
                           "                ctrl_arms.arm_srpcmp(), srp_arms.arm_srp(tree, args.lwsrp.resolve(), 3)]"),
    "srpcmp-removed-everywhere": ("                ctrl_arms.arm_reentry_debug(tree), ctrl_arms.arm_reentry_release(tree),\n                ctrl_arms.arm_srpcmp()]",
                                  "                ctrl_arms.arm_reentry_debug(tree), ctrl_arms.arm_reentry_release(tree)]"),
    "round5-dropped-from-if1": ("                                                        *srp_pub_mutants.ROUND5)))",
                                "                                                        )))"),
}
EXPECT = {  # (shard self-test rc==0, dev comparison rc==0)
    "control-no-edit": (True, True),
    "srpcmp-also-in-srp-phase": (False, False),
    "srp-phase-dropped-from-shards": (False, False),
    "control-phase-also-in-aecp-shard": (False, False),
    "future-suite-added": (True, False),
    "srpcmp-removed-everywhere": (True, False),
    "round5-dropped-from-if1": (True, False),
}
results, ok = {}, True
for name, (old, new) in PROBES.items():
    root = scratch / ("drv-" + name)
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    tar = subprocess.run(["git", "-C", str(clone), "archive", sha], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(root)], input=tar, check=True)
    path = root / D
    text = path.read_text()
    if old:
        assert text.count(old) == 1, (name, text.count(old))
        path.write_text(text.replace(old, new))
    t = root / "sw/firmware/ctrl/test"
    a = subprocess.run([sys.executable, str(t / "test_ctrl_firmware_shards.py")], capture_output=True, text=True, cwd=root)
    b = subprocess.run([sys.executable, str(HERE / "dev_vs_head_dispatch.py"), str(t), dev_driver, str(root / "cmp.json")],
                       capture_output=True, text=True, cwd=root)
    got = (a.returncode == 0, b.returncode == 0)
    results[name] = {"shard_selftest_rc": a.returncode, "dev_compare_rc": b.returncode,
                     "shard_selftest_tail": (a.stdout + a.stderr).strip().splitlines()[-1:],
                     "as_expected": got == EXPECT[name]}
    ok &= got == EXPECT[name]
    shutil.rmtree(root)
out.write_text(json.dumps({"ok": bool(ok), "probes": results}, indent=1) + "\n")
for k, v in results.items():
    print(k, v["shard_selftest_rc"], v["dev_compare_rc"], v["as_expected"], (v["shard_selftest_tail"] or [""])[0][:150])
raise SystemExit(0 if ok else 1)
