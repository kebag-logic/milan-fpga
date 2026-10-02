#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R436-2: every device model of the figures gate (its own MODELS table, read
from tb/nvm_port/measure_figures.py at the head) built at the second bound,
MEM_TIMEOUT_CYC_P = TMO = 37 (`make primary TMO=37`), with the RW checks named.

usage: models_at_37.py <head export> <work dir> <out dir> [--jobs N]
"""
import argparse
import concurrent.futures as cf
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TALLY = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")


def load_gate(head, work):
    # the gate copies its suite into a temp dir at import; keep that in work
    os.environ["TMPDIR"] = str(work)
    tempfile.tempdir = str(work)
    sys.path.insert(0, str(head / "tb" / "nvm_port"))
    spec = importlib.util.spec_from_file_location("mf", head / "tb" / "nvm_port" / "measure_figures.py")
    mf = importlib.util.module_from_spec(spec)
    sys.argv = ["measure_figures.py"]
    spec.loader.exec_module(mf)
    return mf


def run(head, work, out, mf, name, edits, tmo):
    tag = re.sub(r"[^A-Za-z0-9]+", "_", name) + f"_{tmo}"
    d = work / tag
    shutil.rmtree(d, ignore_errors=True)
    (d / "hdl").mkdir(parents=True)
    shutil.copytree(head / "hdl" / "packet_engine", d / "hdl" / "packet_engine")
    (d / "tb").mkdir()
    shutil.copytree(head / "tb" / "nvm_port", d / "tb" / "nvm_port",
                    ignore=shutil.ignore_patterns("obj_dir", "obj_alt"))
    shutil.copytree(head / "tb" / "common", d / "tb" / "common")
    for path, old, new in edits:
        tgt = d / "tb" / "nvm_port" / "sim_main.cpp" if path == mf.SIM else None
        assert tgt is not None, path
        t = tgt.read_text()
        assert t.count(old) == 1, (name, old[:60])
        tgt.write_text(t.replace(old, new, 1))
    mk = d / "tb" / "nvm_port" / "Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", "--build -j 2"))
    p = subprocess.run(["make", "-s", "primary", f"TMO={tmo}", f"VERILATOR={os.environ['VERILATOR']}"],
                       cwd=d / "tb" / "nvm_port", capture_output=True, text=True)
    log = p.stdout + p.stderr
    (out / f"model_{tag}.log").write_text(log)
    fails = [l for l in log.splitlines() if l.startswith("FAIL")]
    rw = sorted({l[6:9] for l in fails if l.startswith("FAIL: RW")})
    shutil.rmtree(d, ignore_errors=True)
    t = TALLY.findall(log)
    return f"{name:<28} TMO={tmo:<4} {t[-1] if t else 'NO TALLY'}  RW failing: {rw or 'none'}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("head"); ap.add_argument("work"); ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=9)
    a = ap.parse_args()
    head, work, out = Path(a.head), Path(a.work), Path(a.out)
    work.mkdir(parents=True, exist_ok=True); out.mkdir(parents=True, exist_ok=True)
    mf = load_gate(head, work)
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(run, head, work, out, mf, n, list(e), 37) for n, _c, e in mf.MODELS]
        lines = [f.result() for f in futs]
    (out / "SUMMARY.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
