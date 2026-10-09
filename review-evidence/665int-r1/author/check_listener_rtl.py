#!/usr/bin/env python3
"""Run the unchanged pinned listener suite entirely in external scratch."""

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
    parser.add_argument("--compiler", type=Path, required=True)
    args = parser.parse_args()
    root, work = args.root.resolve(), args.work.resolve()
    assert root not in work.parents
    work.mkdir(parents=True, exist_ok=True)
    dep = root / "protocol-processor"
    top = subprocess.check_output(["git", "-C", str(dep), "rev-parse", "--show-toplevel"], text=True).strip()
    assert Path(top).resolve() == dep.resolve()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
    import ctrl_reuse
    import ctrl_build
    pin, _ = ctrl_reuse.prove_pin("tb/acmp_listener/sim_main.cpp")
    paths = ("hdl/common/pp_pkg.sv", "hdl/acmp/pp_acmp_pkg.sv",
             "hdl/acmp/KL_pp_acmp_listener.sv", "hdl/acmp/rom/gen_ltn_rom.py",
             "tb/common/verilator_harness.hpp")
    for path in paths:
        ctrl_reuse.prove_pin(path)
    os.environ["TMPDIR"] = str(work)
    os.environ["VERILATOR_JOBS"] = "2"
    suite = dep / "tb/acmp_listener"
    commands = (
        ("rom", [sys.executable, str(dep / paths[3]), "-o", str(work / "ltn_rom.hex")]),
        ("build", [str(args.compiler.resolve()), "--cc", "--exe", "--build", "-j", "8",
                   "--top-module", "KL_pp_acmp_listener", "-GSTRM_TIMEOUT_CYC_P=32",
                   "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
                   "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
                   "-CFLAGS", f"-std=c++17 -O2 -I{suite} -Wall -Wextra",
                   "--Mdir", str(work / "obj"), *[str(dep / path) for path in paths[:3]],
                   str(suite / "sim_main.cpp"), "-o", "listener_sim"]),
        ("run", [str(work / "obj/listener_sim")]),
    )
    results = []
    for name, command in commands:
        result = subprocess.run(command, cwd=work, text=True, capture_output=True, timeout=500, check=False)
        log = result.stdout + result.stderr
        (work / f"{name}.log").write_text(log)
        assert result.returncode == 0, (name, result.returncode, log)
        row = dict(step=name, rc=result.returncode, bytes=len(log.encode()),
                   sha256=hashlib.sha256(log.encode()).hexdigest())
        results.append(row)
        print(json.dumps(row), flush=True)
        if name == "run":
            ok, reason = ctrl_build.fw_gtest.grade(result.returncode, log)
            assert ok, reason
            print(reason, flush=True)
    (work / "rtl.json").write_text(json.dumps(dict(processor_pin=pin, results=results), indent=2) + "\n")
    print("PASS: unchanged pinned listener suite", flush=True)


if __name__ == "__main__":
    main()
