#!/usr/bin/env python3
"""R456-1 disposable probe driver for tb/verilator/milan_dp_render (#643).

Two stages, so builds can be serialised and runs parallelised:

  run_probe.py build TREE NAME [--dp-edit FROM TO]... [--tb-edit FROM TO]...
                               [--tb-file PATH] --verilator VL
  run_probe.py run   TREE NAME --mode=MODE --log LOG

build: plants each --dp-edit into a COPY of hdl/milan/milan_datapath.sv
(TREE/tb/verilator/milan_dp_render/probe_NAME/milan_datapath.sv, passed as
DP_SRC), and each --tb-edit (or the whole --tb-file) into the suite's
sim_tdm8_render.cpp IN PLACE, builds `make tdm8render-build` with
TDM8R_MDIR=obj_probe_NAME, then restores sim_tdm8_render.cpp byte for byte.
Every FROM must match exactly once or the probe refuses to build.

run: runs obj_probe_NAME/Vmilan_dp_tdm8r MODE ('full' = no argument) from the
suite directory and writes the log plus a LOG.rc line `rc=<n> wall=<s>`.
"""
import argparse
import hashlib
import shutil
import subprocess
import sys
import time
from pathlib import Path

SUITE = Path("tb/verilator/milan_dp_render")
TB = "sim_tdm8_render.cpp"


def plant(text: str, edits: list[list[str]], what: str) -> str:
    for frm, to in edits:
        frm = frm.encode().decode("unicode_escape")
        to = to.encode().decode("unicode_escape")
        n = text.count(frm)
        if n != 1:
            sys.exit(f"{what}: edit pattern matches {n} times, not once: {frm!r}")
        text = text.replace(frm, to)
    return text


def build(a: argparse.Namespace) -> None:
    tree = Path(a.tree).resolve()
    suite = tree / SUITE
    over = []
    if a.dp_edit:
        pdir = suite / f"probe_{a.name}"
        pdir.mkdir(exist_ok=True)
        src = (tree / "hdl/milan/milan_datapath.sv").read_text()
        mut = pdir / "milan_datapath.sv"
        mut.write_text(plant(src, a.dp_edit, "datapath"))
        over.append(f"DP_SRC={mut}")
    tbp = suite / TB
    orig = tbp.read_bytes()
    h0 = hashlib.sha256(orig).hexdigest()
    try:
        if a.tb_file:
            tbp.write_bytes(Path(a.tb_file).read_bytes())
        if a.tb_edit:
            tbp.write_text(plant(tbp.read_text(), a.tb_edit, "harness"))
        cmd = ["make", "-s", "-C", str(suite), "tdm8render-build",
               f"TDM8R_MDIR=obj_probe_{a.name}", f"VERILATOR={a.verilator}"] + over
        out = subprocess.run(cmd, capture_output=True, text=True)
        (suite / f"obj_probe_{a.name}.buildlog").write_text(out.stdout + out.stderr)
    finally:
        tbp.write_bytes(orig)
    assert hashlib.sha256(tbp.read_bytes()).hexdigest() == h0
    exe = suite / f"obj_probe_{a.name}" / "Vmilan_dp_tdm8r"
    if out.returncode != 0 or not exe.is_file():
        sys.exit(f"build failed rc={out.returncode}; see obj_probe_{a.name}.buildlog")
    print(f"built {exe}")


def run(a: argparse.Namespace) -> None:
    suite = Path(a.tree).resolve() / SUITE
    exe = suite / f"obj_probe_{a.name}" / "Vmilan_dp_tdm8r"
    argv = [str(exe)] + ([] if a.mode == "full" else [a.mode])
    t0 = time.monotonic()
    with open(a.log, "w") as f:
        rc = subprocess.run(argv, cwd=suite, stdout=f, stderr=subprocess.STDOUT).returncode
    Path(a.log + ".rc").write_text(f"rc={rc} wall={time.monotonic() - t0:.1f}\n")


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="stage", required=True)
    b = sub.add_parser("build")
    b.add_argument("tree")
    b.add_argument("name")
    b.add_argument("--dp-edit", nargs=2, action="append")
    b.add_argument("--tb-edit", nargs=2, action="append")
    b.add_argument("--tb-file")
    b.add_argument("--verilator", required=True)
    r = sub.add_parser("run")
    r.add_argument("tree")
    r.add_argument("name")
    r.add_argument("--mode", required=True)
    r.add_argument("--log", required=True)
    a = p.parse_args()
    build(a) if a.stage == "build" else run(a)


if __name__ == "__main__":
    main()
