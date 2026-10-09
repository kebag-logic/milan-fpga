#!/usr/bin/env python3
"""Check the assigned base's UNBIND equality prerequisite in external scratch.

The maintained walk permits LD1 explicitly. Its scratch variant removes only
that normalization. An echo mutation identifies the response fields causing
the mismatch; it is a negative conformance control, never a proposed fix.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    root, work = args.root.resolve(), args.work.resolve()
    assert root not in work.parents, "scratch must be outside the source tree"
    work.mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = str(work)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
    import ctrl_build as cb
    import ctrl_reuse
    import fw_gtest

    dep = root / "protocol-processor"
    top = subprocess.check_output(
        ["git", "-C", str(dep), "rev-parse", "--show-toplevel"], text=True).strip()
    assert Path(top).resolve() == dep.resolve()
    head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    pin = subprocess.check_output(["git", "-C", str(dep), "rev-parse", "HEAD"], text=True).strip()
    ctrl_reuse.cut_reuse(work / "reuse")
    tree = cb.Tree(cb.CTRL, work / "build", work / "reuse", fw_gtest.Build(jobs=4))
    objects = cb.firmware(tree, cb.PORTABLE, "firmware")
    main_object = fw_gtest.main_object(tree.build, tree.out / "harness")
    includes = [*cb.includes(tree), f"-I{tree.reuse}", "-Wno-unused-function"]
    normal_source = cb.HERE / "acmp_walk.cpp"
    normal_text = normal_source.read_text()
    normalization = "            std::memset(f.b + 20, 0, 8);\n            std::memset(f.b + 36, 0, 2);"
    assert normal_text.count(normalization) == 1
    strict_source = work / "strict_acmp_walk.cpp"
    strict_source.write_text(normal_text.replace(normalization, "            // LD1 normalization removed for exact-wire preflight."))
    normal_tests = fw_gtest.compile_tests(tree.build, includes, [normal_source], tree.out / "normal")
    strict_tests = fw_gtest.compile_tests(tree.build, includes, [strict_source], tree.out / "strict")

    firmware_source = cb.CTRL / "acmp/acmp.c"
    firmware_text = firmware_source.read_text()
    zero_fields = "\tr.talker = 0u;\n\tr.talker_uid = 0u;"
    assert firmware_text.count(zero_fields) == 1
    echo_source = work / "echo/acmp.c"
    echo_source.parent.mkdir(exist_ok=True)
    echo_source.write_text(firmware_text.replace(zero_fields, "\tr.talker = cmd->talker;\n\tr.talker_uid = cmd->talker_uid;"))
    echo_object = cb.compile_c(tree, [echo_source], "echo")
    echo_objects = [obj for obj in objects if obj.name != "acmp_acmp.o"]
    assert len(echo_objects) == len(objects) - 1
    echo_objects += echo_object

    cases = (
        ("maintained_walk", objects, normal_tests, 0, False),
        ("strict_unbind", objects, strict_tests, 1, True),
        ("echo_strict_control", echo_objects, strict_tests, 0, True),
        ("echo_conformance_rejection", echo_objects, normal_tests, 1, True),
    )
    results = []
    for name, firmware, tests, expected_rc, focused in cases:
        exe = fw_gtest.link(tree.build, [*firmware, *tests, main_object], tree.out / name)
        argv = [str(exe)]
        if focused:
            argv.append("--gtest_filter=Table530/ListenerWalk.Graded/UNBIND_*")
        result = fw_gtest.run(argv, cwd=work, timeout=180)
        log = result.stdout + result.stderr
        (work / f"{name}.log").write_text(log)
        assert result.returncode == expected_rc, (name, result.returncode, log)
        checks, failures, matched, unparsed, skipped = fw_gtest.suite_tally.scan(log)
        assert checks > 0 and matched and not unparsed and not skipped, (name, log)
        failed_names = fw_gtest.failed_tests(log)
        if expected_rc:
            assert checks == 8 and failures == 8 and len(failed_names) == 8, (name, log)
            assert all("UNBIND_" in test for test in failed_names)
            witnesses = [line for line in log.splitlines() if "[FAIL]" in line and "byte for byte" in line]
            assert len(witnesses) == 8, (name, log)
        else:
            assert fw_gtest.grade(result.returncode, log)[0], (name, log)
            if focused:
                assert checks == 8, (name, log)
        row = dict(case=name, rc=result.returncode, expected_rc=expected_rc,
                   checks=checks, failures=failures, failed_tests=sorted(failed_names),
                   log_bytes=len(log.encode()), log_sha256=hashlib.sha256(log.encode()).hexdigest())
        results.append(row)
        print(json.dumps(row), flush=True)
    receipt = dict(head=head, processor_pin=pin, results=results,
                   conclusion="LD1 prevents exact UNBIND wire equality at the assigned base")
    (work / "preflight.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print("PASS: prerequisite diagnostic and both controls behaved as required", flush=True)


if __name__ == "__main__":
    main()
