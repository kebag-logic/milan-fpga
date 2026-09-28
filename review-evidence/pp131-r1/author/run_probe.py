#!/usr/bin/env python3
"""Reproduce the record-completion and slot-ACK distinction without source edits."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def execute(command: list[str], cwd: Path, log: Path) -> dict:
    """Run synchronously, keeping build output in scratch and reporting its identity."""
    with log.open("wb") as output:
        result = subprocess.run(command, cwd=cwd, stdout=output, stderr=subprocess.STDOUT,
                                timeout=7200, check=False)
    data = log.read_bytes()
    row = {"command": command, "cwd": str(cwd), "rc": result.returncode,
           "log": str(log), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    print(json.dumps(row), flush=True)
    return row


def main() -> int:
    """Compile unchanged production modules and run both interpretations plus a control."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processor", type=Path, required=True)
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent
    output = args.scratch / "obj"
    command = ["verilator", "--cc", "--exe", "--build", "-j", "4",
               "--top-module", "carrier_probe", "--Mdir", str(output), "-Wall", "-Wno-fatal",
               "-Wno-PINCONNECTEMPTY", "-Wno-UNUSEDSIGNAL", "-Wno-UNUSEDPARAM", "-CFLAGS",
               f"-std=c++17 -O2 -Wall -Wextra -I{args.processor / 'tb/common'}"]
    command += [str(args.processor / name) for name in (
        "hdl/common/pp_pkg.sv", "hdl/acmp/pp_acmp_pkg.sv", "hdl/acmp/KL_acmp_nvm_shadow.sv",
        "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv", "hdl/packet_engine/KL_pp_nvm_port.sv")]
    command += [str(args.parent / "hdl/milan/KL_nvm_backend.sv"),
                str(here / "carrier_probe.sv"), str(here / "carrier_probe.cpp")]
    rows = [execute(command, args.scratch, args.scratch / "build.log")]
    if rows[-1]["rc"]:
        return 1
    cases = (("golden", 0), ("require-carrier", 1), ("stall-window", 0), ("golden", 0))
    for number, (mode, expected) in enumerate(cases):
        log = args.scratch / f"{number}-{mode}.log"
        row = execute([str(output / "Vcarrier_probe"), mode], args.scratch, log)
        rows.append(row)
        data = log.read_text()
        if row["rc"] != expected or "checks:" not in data:
            return 1
        if mode == "require-carrier" and (
                "[FAIL] DR2C-CARRIER-3: failed slot leaves record producer un-ACKed" not in data
                or "failures: 1" not in data):
            return 1
    (args.scratch / "results.json").write_text(json.dumps(rows, indent=2) + "\n")
    print("Reproduction complete: the producer-retention interpretation fails its named assertion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
