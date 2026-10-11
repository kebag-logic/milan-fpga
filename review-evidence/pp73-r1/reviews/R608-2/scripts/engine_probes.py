#!/usr/bin/env python3
"""Reviewer engine probes for tb/aecp_cmds (R608-2).

Each probe copies a pristine source tree (--src, an export of the exact head),
plants one exact engine edit, builds and sweeps the engine with tb/aecp_cmds,
then records three verdicts:
  1. the suite's own step (gate --observed): a fresh sweep against the table
     and against the recorded decode.json;
  2. the documented step after an intended engine change
     (gate --observed --write-record), which rewrites decode.json;
  3. make check's gate on the re-recorded tree (gate, no self-test).
A probe whose verdict 3 is rc 0 is an engine change the table does not see once
decode.json is re-recorded, as the documented workflow does.

usage: python3 -I engine_probes.py --src DIR --out DIR --verilator V [--jobs N]
"""
import argparse
import json
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ENGINE = "hdl/aecp/KL_aecp_engine.sv"

PROBES = {
    "amap-record-4-bytes": (
        "                   != (19'd20 + ({3'd0, desc_ty_r} << 3)))",
        "                   != (19'd20 + ({3'd0, desc_ty_r} << 2)))"),
    "amap-record-16-bytes": (
        "                   != (19'd20 + ({3'd0, desc_ty_r} << 3)))",
        "                   != (19'd20 + ({3'd0, desc_ty_r} << 4)))"),
    "mvu-pid-first-byte-unchecked": (
        "&& (raw_ct_r   == MVU_PID_HI_C)",
        "&& (raw_ct_r[7:0] == MVU_PID_HI_C[7:0])"),
}


def sh(cmd, cwd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT).returncode


def fails(log):
    return [x for x in Path(log).read_text().splitlines() if x.startswith("FAIL:") or "checks:" in x
            or x.startswith("  ") or "aecp commands:" in x][:8]


def probe(name, src: Path, out: Path, verilator: str) -> dict:
    old, new = PROBES[name]
    with tempfile.TemporaryDirectory(prefix="r608-2-eprobe-") as tmp:
        root = Path(tmp)
        for d in ("hdl", "scripts", "tb/common", "tb/aecp_cmds", "docs"):
            shutil.copytree(src / d, root / d, ignore=shutil.ignore_patterns(
                "obj_dir", "*.hex", "image.bin", "__pycache__"))
        p = root / ENGINE
        s = p.read_text()
        if s.count(old) != 1:
            raise SystemExit(f"{name}: edit site count {s.count(old)}")
        p.write_text(s.replace(old, new))
        bench = root / "tb/aecp_cmds"
        gate = ["python3", "-B", "../../scripts/check_aecp_commands.py"]
        r = {"probe": name}
        r["build_rc"] = sh(["make", "build", "VERILATOR=" + verilator], bench, out / f"{name}-build.log")
        r["sweep_rc"] = sh(["./obj_dir/Vaecp_cmds", "obj_dir/observed.json"], bench, out / f"{name}-sweep.log")
        r["suite_rc"] = sh(gate + ["--observed", "obj_dir/observed.json"], bench, out / f"{name}-1-suite.log")
        r["rerecord_rc"] = sh(gate + ["--observed", "obj_dir/observed.json", "--write-record"], bench,
                              out / f"{name}-2-rerecord.log")
        r["gate_after_rerecord_rc"] = sh(gate, bench, out / f"{name}-3-gate.log")
        shutil.copyfile(bench / "decode.json", out / f"{name}-decode.json")
        r["suite_lines"] = fails(out / f"{name}-1-suite.log")
        r["rerecord_lines"] = fails(out / f"{name}-2-rerecord.log")
        r["gate_lines"] = fails(out / f"{name}-3-gate.log")
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", default="verilator")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda n: probe(n, a.src.resolve(), a.out.resolve(), a.verilator), PROBES))
    (a.out / "summary.json").write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
