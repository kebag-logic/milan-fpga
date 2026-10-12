#!/usr/bin/env python3
"""Independent dispatch comparison: dev 09c7231e's driver default vs head's four shards.

Loads dev's test_ctrl_firmware.py (from a git object written to DEV_DRIVER) and the
head driver side by side over the head's helper modules (byte-identical to dev's:
the merge diff touches only the driver and its shard self-test). Every arm entry point
(name starting `arm_` or ending `_arm`) and every campaign entry is replaced by a recorder,
so nothing is compiled. Dev's default is driven through its real main(); head's shards and
default through run_selected(). Prints JSON; rc 0 only when dev default == head default ==
concatenated shards 0..3, in order, with no identity appearing twice.
Usage: dev_vs_head_dispatch.py HEAD_TEST_DIR DEV_DRIVER OUT_JSON
"""
import importlib.util
import json
import sys
from contextlib import ExitStack, redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

head_dir, dev_driver, out_json = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(head_dir))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


head = load("head_driver", head_dir / "test_ctrl_firmware.py")
dev = load("dev_driver", dev_driver)
assert head.ctrl_arms is dev.ctrl_arms and head.srp_mutants is dev.srp_mutants


def norm(v):
    if isinstance(v, Path):
        return v.name
    if isinstance(v, (str, int, float, bool, type(None))):
        return v
    if isinstance(v, (tuple, list)):
        return [norm(x) for x in v]
    return type(v).__name__


def record_into(calls):
    stack = ExitStack()
    for mod in (head.ctrl_arms, head.srp_arms, head.aecp_arms):
        for name, fn in list(vars(mod).items()):
            if callable(fn) and getattr(fn, "__module__", None) == mod.__name__ and (
                    name.startswith("arm_") or name.endswith("_arm")):
                def rec(*a, _n=f"{mod.__name__}.{name}", **k):
                    calls.append(json.dumps([_n, [norm(x) for x in a], {x: norm(y) for x, y in sorted(k.items())}]))
                    return head.ctrl_arms.Outcome(_n, 0, "") if hasattr(head.ctrl_arms, "Outcome") else None
                stack.enter_context(patch.object(mod, name, rec))
    stack.enter_context(patch.object(head.ctrl_arms, "report", lambda outcomes: False))

    def control(root, reuse, jobs, part=(1, 1), shard=None):
        table = head.ctrl_mutants.sliced(part) if shard is None else head.ctrl_mutants.MUTANTS[shard[0]::shard[1]]
        calls.extend(f"control:{m.name}" for m in table)
        return False

    def aecp(root, jobs=4, shard=(0, 1)):
        calls.extend(f"aecp:{d.name}" for d in head.aecp_mutants.DEFECTS[shard[0]::shard[1]])
        return False

    def srp(root, lwsrp, jobs=4, interfaces=2):
        calls.extend(f"srp-if{interfaces}:{d.name}" for d in head.srp_mutants.DEFECTS)
        return False

    def pins(root, lwsrp):
        calls.append("lwsrp-pin-arms")
        return 0
    stack.enter_context(patch.object(head.ctrl_mutants, "campaign", control))
    stack.enter_context(patch.object(head.aecp_mutants, "campaign", aecp))
    stack.enter_context(patch.object(head.srp_mutants, "campaign", srp))
    stack.enter_context(patch.object(head.ctrl_mutants, "lwsrp_pin_arms", pins))
    return stack


fake_tree = head.Tree(head.CTRL, Path("out/checkout"), Path("reuse"), head.fw_gtest.Build(jobs=4))

dev_calls = []
with record_into(dev_calls), redirect_stdout(StringIO()), \
        patch.object(dev, "Tree", lambda *a, **k: fake_tree), \
        patch.object(dev, "cut_reuse", lambda p: None), \
        patch.object(dev.fw_gtest, "toolchain", lambda: "stub"):
    rc = dev.main(["--require-rv32", "--self-test", "--jobs", "4"])
assert rc == 0, rc


def head_run(shard):
    calls = []
    args = SimpleNamespace(shard=shard, self_test=True, jobs=4, slice=(1, 1), mutation_shard=None,
                           require_rv32=True, lwsrp=head.CTRL.parents[2] / "third_party/lwSRP")
    with record_into(calls), redirect_stdout(StringIO()):
        assert not head.run_selected(args, fake_tree, Path("out"))
    return calls


head_default = head_run(None)
shards = [head_run((i, 4)) for i in range(4)]
concat = [c for s in shards for c in s]
srpcmp = [i for i, s in enumerate(shards) for c in s if "arm_srpcmp" in c]
round5 = sorted(head.srp_pub_mutants.ROUND5)
round5_if1 = [c for c in shards[3] if c.startswith("srp-if1:") and c[8:].startswith(tuple(round5))]
round5_if2 = [c for c in shards[3] if c.startswith("srp-if2:") and c[8:].startswith(tuple(round5))]
res = {
    "dev_default": len(dev_calls), "head_default": len(head_default),
    "shard_sizes": [len(s) for s in shards],
    "dev_eq_head_default_ordered": dev_calls == head_default,
    "dev_eq_concat_ordered": dev_calls == concat,
    "unique_identities": len(set(dev_calls)) == len(dev_calls),
    "srpcmp_in_shards": srpcmp,
    "round5_prefixes": round5, "round5_if1": len(round5_if1), "round5_if2": len(round5_if2),
    "pin_arms_in_shards": [i for i, s in enumerate(shards) if "lwsrp-pin-arms" in s],
}
ok = (res["dev_eq_head_default_ordered"] and res["dev_eq_concat_ordered"] and res["unique_identities"]
      and srpcmp == [0] and res["pin_arms_in_shards"] == [3] and round5_if1 and round5_if2)
res["ok"] = bool(ok)
out_json.write_text(json.dumps({"result": res, "dev": dev_calls, "shards": shards}, indent=1) + "\n")
print(json.dumps(res, indent=1))
raise SystemExit(0 if ok else 1)
