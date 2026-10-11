#!/usr/bin/env python3
"""Independent scheduling, preservation, failure-path and aggregate probes."""
import argparse
import ast
from collections import Counter
from contextlib import ExitStack, redirect_stdout
import copy
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from types import ModuleType
from unittest.mock import patch

BASE = "ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5"
HEAD = "f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48"
PACKET = Path(__file__).resolve().parents[1]
ROOT = Path(sys.argv[1]).resolve()
DRIVER = "sw/firmware/ctrl/test/test_ctrl_firmware.py"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
import ci_events as ci
import test_ctrl_firmware as candidate
import test_ctrl_firmware_shards as shardtest
from ctrl_build import Tree, Outcome


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"})


def old_module():
    result = ModuleType("baseline_driver")
    result.__file__ = str(ROOT / DRIVER)
    sys.modules[result.__name__] = result
    exec(compile(git("show", f"{BASE}:{DRIVER}"), result.__file__, "exec"), result.__dict__)
    return result


def capture(module, flags):
    calls = []
    def normalise(value):
        if isinstance(value, Tree):
            return "tree"
        if isinstance(value, Path):
            return value.name
        return value
    def arm(name):
        def wrapped(*args, **kwargs):
            calls.append([name, [normalise(x) for x in args], {k: normalise(v) for k,v in kwargs.items()}])
            return Outcome(name, 0, "")
        return wrapped
    def control(root, reuse, jobs, part=(1,1), shard=None):
        assert part == (1,1) and shard is None
        calls.append(["control-unnamed-tests"])
        calls.extend(["control", m.name] for m in module.ctrl_mutants.MUTANTS)
        return False
    def aecp(root, jobs=4, shard=(0,1)):
        assert shard == (0,1)
        calls.append(["aecp-controls"])
        calls.extend(["aecp", d.name] for d in module.aecp_mutants.DEFECTS)
        return False
    def srp(root, lwsrp, jobs=4, interfaces=2):
        calls.extend(["srp", interfaces, d.name] for d in module.srp_mutants.DEFECTS)
        return False
    def pins(*args):
        calls.append(["pin-controls"])
        return 0
    with ExitStack() as stack, redirect_stdout(io.StringIO()):
        for owner in (module.ctrl_arms, module.srp_arms, module.aecp_arms):
            for name, value in vars(owner).copy().items():
                if callable(value) and (name.startswith("arm_") or name in ("core_arm", "image_arm")):
                    stack.enter_context(patch.object(owner, name, arm(owner.__name__ + "." + name)))
        for owner, name, replacement in (
            (module.ctrl_arms,"report",lambda outcomes: False),
            (module,"cut_reuse",lambda path: None),
            (module.fw_gtest,"toolchain",lambda: "intercepted"),
            (module.ctrl_mutants,"campaign",control),
            (module.aecp_mutants,"campaign",aecp),
            (module.srp_mutants,"campaign",srp),
            (module.ctrl_mutants,"lwsrp_pin_arms",pins)):
            stack.enter_context(patch.object(owner, name, replacement))
        assert module.main(flags) == 0
    return calls


def main():
    assert git("rev-parse","HEAD").decode().strip() == HEAD
    before = old_module()
    expected = capture(before, ["--require-rv32", "--self-test", "--jobs", "4"])
    default = capture(candidate, ["--require-rv32", "--self-test", "--jobs", "4"])
    shards = [capture(candidate, ["--require-rv32", "--self-test", "--jobs", "4", "--shard", f"{i}/4"]) for i in range(4)]
    assert expected == default == [c for group in shards for c in group]
    serialised = [json.dumps(x, sort_keys=True) for x in expected]
    assert len(serialised) == len(set(serialised)) == 844
    (PACKET / "receipts/independent-invocations.json").write_text(json.dumps({"baseline": expected, "shards": shards}, indent=2)+"\n")
    print(f"PASS: actual base main(), candidate default and four shard main() calls preserve all {len(expected)} ordered unique identities; sizes {[len(s) for s in shards]}.")
    assert capture(before, ["--jobs", "4"]) == capture(candidate, ["--jobs", "4"])
    print("PASS: ordinary no-self-test invocation unchanged.")
    # Compare coverage's complete syntax and every other coverage input byte.
    def coverage_ast(source):
        return ast.dump(next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name == "coverage"), include_attributes=False)
    assert coverage_ast(git("show", f"{BASE}:{DRIVER}")) == coverage_ast((ROOT/DRIVER).read_bytes())
    paths = ["sw/firmware/gtest", "sw/firmware/ctrl_nvm", "sw/firmware/ctrl/test/ctrl_arms.py", "sw/firmware/ctrl/test/srp_arms.py", "sw/firmware/ctrl/test/aecp_arms.py", "sw/firmware/ctrl/test/ctrl_mutants.py", "sw/firmware/ctrl/test/srp_mutants.py", "sw/firmware/ctrl/test/aecp_mutants.py", "hdl", "protocol-processor", "gptp-processor", "third_party/lwSRP"]
    assert not git("diff","--name-only",BASE,HEAD,"--",*paths)
    print("PASS: coverage function AST, complete coverage directory/ratchet, arm implementations, campaign tables, saved-state source, RTL and processor gitlinks are unchanged.")
    world = ci.parse_world(ci.read_tree(ROOT))
    base_wf = ci.parse_world({**ci.read_tree(ROOT), ci.RTL_FAST:git("show",f"{BASE}:{ci.RTL_FAST}").decode()})[ci.RTL_FAST]
    baseline_rows = ci.firmware_census(base_wf)
    current_rows = ci.firmware_census(world[ci.RTL_FAST])
    assert baseline_rows == ci.firmware_baseline_census()
    assert ci.firmware_commands(baseline_rows) == ci.firmware_commands(current_rows)
    (PACKET/"receipts/independent-command-census.json").write_text(json.dumps({"actual_base":baseline_rows,"candidate":current_rows},indent=2)+"\n")
    print(f"PASS: recorded base census equals the actual base workflow: {len(baseline_rows)} original and {len(current_rows)} current script lines; only terminal shard suffixes normalised, commands and if-guards equal.")
    # The production guard itself must fail, rather than merely displaying a count.
    original = candidate.selected_phases
    for label, replacement in (
        ("unassigned suites",lambda shard: original(shard) if shard is None else tuple(p for p in original(shard) if p != "suites")),
        ("suites assigned twice",lambda shard: original(shard) if shard is None else (*original(shard), *(("suites",) if shard[0] == 1 else ())))):
        with patch.object(candidate,"selected_phases",replacement), redirect_stdout(io.StringIO()):
            try:
                shardtest.run_cases(candidate)
            except AssertionError:
                pass
            else:
                raise AssertionError("guard escaped " + label)
        print("PASS: production ownership guard rejects " + label)
    # Failure from any dispatched phase must survive to the final status.
    for phase, owner, method in (("suites",candidate.ctrl_arms,"report"),("control",candidate.ctrl_mutants,"campaign"),("aecp",candidate.aecp_mutants,"campaign"),("srp",candidate,"run_srp_mutants")):
        args = argparse.Namespace(shard=(candidate.PHASES.index(phase),4),self_test=True,jobs=4,slice=(1,1),mutation_shard=None)
        with patch.object(candidate,"run_suites",return_value=[]), patch.object(owner,method,return_value=True):
            assert candidate.run_selected(args, argparse.Namespace(reuse=Path("reuse")),Path("out"))
        print("PASS: failure propagated by phase " + phase)
    old_table = candidate.srp_mutants.DEFECTS
    with patch.object(candidate.srp_mutants,"campaign",side_effect=[False,candidate.Refusal("injected refusal")]):
        try:
            candidate.run_srp_mutants(argparse.Namespace(lwsrp=Path("unused"),jobs=4),Path("unused"))
        except candidate.Refusal:
            pass
        else:
            raise AssertionError("missing SRP refusal")
    assert candidate.srp_mutants.DEFECTS is old_table
    print("PASS: SRP interface-one refusal restores the full mutable table.")
    wf = world[ci.RTL_FAST]
    verdict = wf["jobs"]["rtl-fast"]["steps"][0]
    default_env = {key:"success" for key in verdict["env"]}
    cases = 0
    for job in ci.FIRMWARE_JOBS:
        key = ci.fast_result_env_name(job)
        for status, expected_rc in (("success",0),("skipped",0),("failure",1),("cancelled",1),("",1),("unknown",1)):
            env = {**os.environ,**default_env,key:status}
            run = subprocess.run(["bash","-c",verdict["run"]],env=env,capture_output=True,text=True)
            assert run.returncode == expected_rc,(job,status,run.stdout,run.stderr)
            cases += 1
    print(f"PASS: actual aggregate shell rejects failures/cancellations/empty/unknown values for each firmware job; {cases} cases.")
    for job in ci.FIRMWARE_JOBS:
        for label, change in (
            ("missing need",lambda w,j=job:w[ci.RTL_FAST]["jobs"]["rtl-fast"]["needs"].remove(j)),
            ("disabled job",lambda w,j=job:w[ci.RTL_FAST]["jobs"][j].__setitem__("if",False)),
            ("raised timeout",lambda w,j=job:w[ci.RTL_FAST]["jobs"][j].__setitem__("timeout-minutes",46)),
            ("build-output cache",lambda w,j=job:next(s for s in w[ci.RTL_FAST]["jobs"][j]["steps"] if s.get("uses","").startswith("actions/cache"))["with"].__setitem__("path","build"))):
            mutated=copy.deepcopy(world)
            change(mutated)
            c=ci.check(mutated)
            assert c.findings,(job,label)
            print(f"PASS: contract rejects {job}: {label}")
    print("All independent focused probes PASS.")


if __name__ == "__main__":
    main()
