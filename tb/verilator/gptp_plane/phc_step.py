#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the real-counter step regression and its isolated microcode defects."""

import argparse
import os
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GENERATOR = ROOT / "gptp-processor/hdl/ucode/gen_gptp_ucode.py"


def invoke(argv: list[str], cwd: Path, log: Path) -> int:
    """Keep the complete command output and return its actual exit status."""
    with log.open("w") as stream:
        result = subprocess.run(argv, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, check=False)
    return result.returncode


def run(work: Path, generator: Path, mutants: bool) -> None:
    """One compiled counter/engine model, independently generated ROM per arm."""
    work.mkdir(parents=True, exist_ok=True)
    donor = ROOT / "gptp-processor/hdl"
    sources = [HERE / "gptp_plane_wrap.sv", ROOT / "hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv"]
    sources.extend(donor / path for path in (
        "ucpu/gptp_ucpu_pkg.sv", "ucpu/KL_gptp_ucpu.sv",
        "wire/KL_gptp_rx_parser.sv", "wire/KL_gptp_tx_slot.sv",
        "common/KL_gptp_timer.sv", "top/KL_gptp_engine.sv"))
    binary = work / "obj/phc_step"
    command = [os.environ.get("VERILATOR", "verilator"), "--cc", "--exe", "--build", "-j",
               os.environ.get("VERILATOR_JOBS", "2"), "--top-module", "gptp_plane_wrap",
               "--Mdir", str(binary.parent), "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME",
               "-Wno-UNUSEDSIGNAL", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
               "-GCLK_HZ_P=8000000", "-GPHC_INCR_P=2097152000",
               "-CFLAGS", "-std=c++17 -O2 -Wall -Wextra",
               *map(str, sources), str(HERE / "sim_phc_step.cpp"), "-o", binary.name]
    if invoke(command, ROOT, work / "build.log"):
        raise RuntimeError("step regression compilation failed; see build.log")
    source = generator.read_text()
    arms = [("clean", source, None)]
    if mutants:
        defects = (
            ("stale-rate-window", '    p.emit("WRST", ra=0, imm=RG_SCR | S_NR3, fmt=FMT_Q)\n',
             "", "asCapable never falls after step"),
            ("crossing-exchange", '    p.emit("RDST", rd=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n',
             '    p.emit("MOVE", rd=RT, ra=0, imm=0)\n', "no invalid link-delay publication"),
            ("never-rearm-measurement", '    p.emit("WRST", ra=0, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n',
             "", "real excessive delay still clears asCapable"),
        )
        for name, old, new, assertion in defects:
            if source.count(old) != 1:
                raise RuntimeError(f"{name}: mutation anchor is not unique")
            arms.append((name, source.replace(old, new), assertion))
    for name, program, assertion in arms:
        directory = work / name
        directory.mkdir(exist_ok=True)
        script = directory / "generate.py"
        script.write_text(program)
        if invoke(["python3", str(script), "--clk-hz", "8000000", "-o", "gptp_ucode.hex"],
                  directory, directory / "generate.log"):
            raise RuntimeError(f"{name}: generation failed")
        rc = invoke([str(binary)], directory, directory / "run.log")
        log = (directory / "run.log").read_text()
        if assertion is None:
            print(log, end="", flush=True)
            if rc != 0 or "RESULT: PASS" not in log:
                raise RuntimeError("clean step regression failed")
        elif rc != 1 or f"[FAIL] {assertion}" not in log:
            raise RuntimeError(f"{name}: required runtime assertion did not reject the defect")
        else:
            print(f"PASS planted defect {name}: {assertion}", flush=True)
    print(f"phc_step campaign: {len(arms)} checks: {len(arms)} PASS, 0 FAIL", flush=True)


def main() -> None:
    """Use a retained external directory when requested, otherwise clean up."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path)
    parser.add_argument("--generator", type=Path, default=GENERATOR)
    parser.add_argument("--mutants", action="store_true")
    args = parser.parse_args()
    if args.work:
        run(args.work.resolve(), args.generator.resolve(), args.mutants)
    else:
        with tempfile.TemporaryDirectory(prefix="gptp-phc-step-") as directory:
            run(Path(directory), args.generator.resolve(), args.mutants)


if __name__ == "__main__":
    main()
