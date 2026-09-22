#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compile the real pp_top bench and require the issue #97 fixture diagnostics."""

import argparse
import os
from pathlib import Path
import shlex
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verilator", default="verilator")
    parser.add_argument("--cxx", default="c++")
    parser.add_argument("vflags", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    vflags = args.vflags
    if vflags and vflags[0] == "--":
        vflags = vflags[1:]
    root = subprocess.check_output(
        [args.verilator, "--getenv", "VERILATOR_ROOT"], text=True
    ).strip()
    wire = "SRP VID fixture must differ from product default 2 in the 16-bit wire value"
    class_d = "SRP VID fixture must differ from product default 2 in the 12-bit class-D value"
    cases = [(None, ()), ("5A3C", ()), ("0002", (wire, class_d)), ("1002", (class_d,))]

    with tempfile.TemporaryDirectory(prefix="pp-top-vid-guards-") as tmp:
        subprocess.run(
            [args.verilator, *vflags, "--Mdir", tmp], check=True
        )
        command = [
            *shlex.split(args.cxx), "-std=c++17", "-Wall", "-Wextra", "-fsyntax-only",
            "-I" + tmp, "-I" + str(Path(root) / "include"),
            "-I" + str(Path(root) / "include/vltstd"),
        ]
        # The diagnostic checks below require the compiler's English wording.
        compiler_env = os.environ.copy()
        compiler_env["LC_ALL"] = "C"
        for value, expected in cases:
            define = [] if value is None else ["-DPP_TOP_SRP_DOM_DEF_VID=0x" + value]
            result = subprocess.run(
                [*command, *define, "sim_main.cpp"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                env=compiler_env,
            )
            errors = [line for line in result.stdout.splitlines() if "error:" in line]
            assertions = [line for line in errors if "static assertion" in line]
            found = tuple(message for message in (wire, class_d)
                          if any(message in line for line in assertions))
            label = "default (no override)" if value is None else value
            if (bool(result.returncode) != bool(expected) or found != expected
                    or len(errors) != len(expected)):
                print(f"FAIL: fixture {label}: unexpected compiler result {result.returncode}")
                print(result.stdout)
                return 1
            outcome = "compiles" if not expected else "refused: " + "; ".join(expected)
            print(f"fixture guard {label}: {outcome}")
    print("fixture guards: 4 cases PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
