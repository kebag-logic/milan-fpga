#!/usr/bin/env python3
"""Reproduce the cumulative 1x1 attribution using the unchanged OOC recipe."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def counts(report, name):
    rows = [[cell.strip() for cell in line.split("|")][1:-1]
            for line in report.read_text().splitlines() if "|" in line]
    heading = next(row for row in rows if "Instance" in row and "Total LUTs" in row)
    hits = [row for row in rows if len(row) == len(heading)
            and (row[0] == name or row[0].endswith("." + name))]
    assert len(hits) == 1, (name, hits)
    return {"lut": int(hits[0][heading.index("Total LUTs")]),
            "ff": int(hits[0][heading.index("FFs")])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("base", "lane", "work", "vivado", "lock"):
        parser.add_argument("--" + option, required=True, type=Path)
    args = parser.parse_args()
    base = args.base.resolve()
    lane = args.lane.resolve()
    work = args.work.resolve()
    packet = Path(__file__).resolve().parent
    assert git(base, "rev-parse", "HEAD").decode().strip() == "6aa25dec977c6ad78bf4ff6275de47fb81d0c246"
    assert not git(base, "status", "--porcelain")
    for sub in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
        root = base / sub
        assert Path(git(root, "rev-parse", "--show-toplevel").decode().strip()) == root
        assert git(root, "rev-parse", "HEAD") == git(base, "rev-parse", "HEAD:" + sub)
        assert not git(root, "status", "--porcelain")
    work.mkdir(exist_ok=False)
    inputs = work / "inputs"
    inputs.mkdir()
    maap = "hdl/ieee1722/maap/KL_maap.sv"
    current = inputs / "KL_maap.sv"
    current.write_bytes(git(base, "show", "HEAD:" + maap))
    manifest = json.loads((packet / "area-inputs.json").read_text())
    datapaths = {}
    for item, rev in (("base", "6aa25dec"), ("M5", "19cc4eec")):
        path = inputs / (item + "-datapath.sv")
        path.write_bytes(git(lane, "show", rev + ":hdl/milan/milan_datapath.sv"))
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest[path.name]["sha256"]
        datapaths[item] = path
    env = dict(os.environ, TMPDIR=str(work), PYTHONDONTWRITEBYTECODE="1")
    results = []
    for item in ("base", "M4", "M2", "M7", "M8", "M1", "M5", "M6"):
        assert shutil.disk_usage(work).free > 30 * 1024**3, "30 GiB floor"
        if item != "base":
            subprocess.run(["patch", "--batch", "--forward", str(current),
                            str(packet / "input-deltas" / (item + ".patch"))], check=True)
        source = inputs / (item + ".sv")
        source.write_bytes(current.read_bytes())
        assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest[source.name]["sha256"]
        datapath = datapaths["M5" if item in ("M5", "M6") else "base"]
        out = work / item
        out.mkdir()
        tcl = "set_param general.maxThreads 1\nset_param synth.maxThreads 1\n"
        tcl += "rename read_verilog recipe_read_verilog\nproc read_verilog {args} {\n"
        tcl += "  set mapped {}\n  foreach arg $args {\n    set group {}\n    foreach token $arg {\n"
        for name, path in (("KL_maap.sv", source), ("milan_datapath.sv", datapath)):
            tcl += f'      if {{[file tail $token] eq "{name}"}} {{set token {{{path}}}}}\n'
        tcl += "      lappend group $token\n    }\n    lappend mapped $group\n  }\n"
        tcl += "  uplevel 1 [list recipe_read_verilog {*}$mapped]\n}\n"
        tcl += f"source {{{base}/syn/ooc/milan_datapath_ooc.tcl}}\nquit\n"
        (out / "run.tcl").write_text(tcl)
        with (out / "launcher.log").open("w") as log:
            result = subprocess.run(["flock", str(args.lock), str(args.vivado), "-mode", "batch",
                                     "-source", "run.tcl", "-nojournal", "-log", "baseline.log"],
                                    cwd=out, env=env, stdout=log, stderr=subprocess.STDOUT)
        (out / "run.rc").write_text(str(result.returncode) + "\n")
        if result.returncode:
            return result.returncode
        row = {"item": item, **counts(out / "util_hier_base.rpt", "maap_engine")}
        row["whole_datapath"] = counts(out / "util_hier_base.rpt", "milan_datapath")
        results.append(row)
        (work / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        print(json.dumps(row), flush=True)
    delta_lut = results[-1]["lut"] - results[0]["lut"]
    delta_ff = results[-1]["ff"] - results[0]["ff"]
    return 3 if delta_lut > 60 or delta_ff > 60 else 0


if __name__ == "__main__":
    raise SystemExit(main())
