#!/usr/bin/env python3
"""Shard verdict propagation at head: with every arm/campaign stubbed, make exactly one
target fail and require run_selected() to be True for its owning shard only (and for the
unsharded default). Targets include F-INT's comparator arm (shard 0) and an interface-1
ROUND5 publication mutant entry (shard 3).
Usage: verdict_propagation.py HEAD_TEST_DIR OUT_JSON
"""
import importlib.util
import json
import sys
from contextlib import ExitStack, redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

head_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(head_dir))
spec = importlib.util.spec_from_file_location("head_driver", head_dir / "test_ctrl_firmware.py")
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
Outcome = d.ctrl_arms.Outcome
real_report = d.ctrl_arms.report


def run(target, shard):
    args = SimpleNamespace(shard=shard, self_test=True, jobs=4, slice=(1, 1), mutation_shard=None,
                           require_rv32=True, lwsrp=d.CTRL.parents[2] / "third_party/lwSRP")
    tree = d.Tree(d.CTRL, Path("out/checkout"), Path("reuse"), d.fw_gtest.Build(jobs=4))
    with ExitStack() as st, redirect_stdout(StringIO()):
        for mod in (d.ctrl_arms, d.srp_arms, d.aecp_arms):
            for name, fn in list(vars(mod).items()):
                if callable(fn) and getattr(fn, "__module__", None) == mod.__name__ and (
                        name.startswith("arm_") or name.endswith("_arm")):
                    st.enter_context(patch.object(mod, name, lambda *a, _n=name, **k: Outcome(
                        _n, 1 if _n == target else 0, "planted" if _n == target else "")))
        st.enter_context(patch.object(d.ctrl_mutants, "campaign", lambda *a, **k: target == "control"))
        st.enter_context(patch.object(d.aecp_mutants, "campaign", lambda *a, **k: target == "aecp"))
        st.enter_context(patch.object(d.srp_mutants, "campaign", lambda root, lwsrp, jobs=4, interfaces=2:
                                      target == f"srp-if{interfaces}" or (
                                          target == "round5-if1" and interfaces == 1 and any(
                                              x.name.startswith(tuple(d.srp_pub_mutants.ROUND5))
                                              for x in d.srp_mutants.DEFECTS))))
        st.enter_context(patch.object(d.ctrl_mutants, "lwsrp_pin_arms", lambda *a: 1 if target == "pins" else 0))
        return bool(d.run_selected(args, tree, Path("out")))


TARGETS = {"none": [], "arm_srpcmp": [0], "arm_maap": [0], "arm_srp": [0], "core_arm": [0],
           "control": [1], "aecp": [2], "srp-if2": [3], "srp-if1": [3], "round5-if1": [3], "pins": [3]}
res, ok = {}, True
for t, owners in TARGETS.items():
    red = [i for i in range(4) if run(t, (i, 4))]
    default = run(t, None)
    res[t] = {"red_shards": red, "default_red": default}
    ok &= red == owners and default == bool(owners)
out.write_text(json.dumps({"ok": bool(ok), "targets": res}, indent=1) + "\n")
print(json.dumps(res))
print("OK" if ok else "MISMATCH")
raise SystemExit(0 if ok else 1)
