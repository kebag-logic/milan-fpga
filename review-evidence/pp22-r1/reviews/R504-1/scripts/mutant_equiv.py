#!/usr/bin/env python3
"""Plant every arm/patch that edits an edited file at base AND head, then compare
the mutated module's elaborated netlist between the two revisions.

usage: mutant_equiv.py <base-tree> <head-tree> <workdir> <out.json>

Netlist: sv2v(pp_pkg.sv + module) -> yosys read_verilog; hierarchy -top;
proc; opt_clean; write_verilog -noattr, with `all.v:<line>` in generated names
normalised (a declaration move shifts source lines, nothing else). Equal
netlists at base and head mean the mutant is the same design at both revisions,
so its kill outcome cannot have changed. Also records whether each mutant
changes the netlist at all relative to the unmutated module.
"""
import hashlib
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys

base, head, work, out = (pathlib.Path(a).resolve() for a in sys.argv[1:5])
EDITED = {"hdl/packet_engine/KL_pp_originator.sv": "KL_pp_originator",
          "hdl/packet_engine/KL_pp_rx_validator.sv": "KL_pp_rx_validator"}
PKG = "hdl/common/pp_pkg.sv"


def netlist(tree: pathlib.Path, rel: str, d: pathlib.Path) -> str:
    d.mkdir(parents=True, exist_ok=True)
    v = subprocess.run(["sv2v", str(tree / PKG), str(tree / rel)], capture_output=True,
                       text=True, check=True).stdout
    (d / "all.v").write_text(v)
    top = EDITED[rel]
    subprocess.run(["yosys", "-q", "-p", f"read_verilog -defer all.v; hierarchy -check -top {top}; "
                    f"proc; opt_clean; write_verilog -noattr n.v"], cwd=d, check=True,
                   capture_output=True)
    n = re.sub(r"all\.v:\d+", "all.v:N", (d / "n.v").read_text())
    return hashlib.sha256(n.encode()).hexdigest()


def tables():
    for name in ("notify_mutants", "acmp_mutants", "d3_mutants"):
        py = head / "tb/pp_top" / f"{name}.py"
        spec = importlib.util.spec_from_file_location(name, py)
        mod = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(py.parent))
        spec.loader.exec_module(mod)
        sys.path.pop(0)
        seen = set()
        for m in mod.MUTANTS:
            files = {e[0] for e in m.edits}
            if not files & set(EDITED) or (m.name, m.edits) in seen:
                continue
            seen.add((m.name, m.edits))
            yield f"tb/pp_top/{name}.py:{m.name}", mod.plant, m.edits


rows = []
if work.exists():
    shutil.rmtree(work)
for label, plant, edits in tables():
    files = sorted({e[0] for e in edits})
    assert len(files) == 1 and files[0] in EDITED, (label, files)
    rel = files[0]
    h = {}
    for rev, tree in (("base", base), ("head", head)):
        t = work / re.sub(r"\W", "_", label) / rev
        (t / rel).parent.mkdir(parents=True, exist_ok=True)
        (t / PKG).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tree / rel, t / rel)
        shutil.copy2(tree / PKG, t / PKG)
        why = plant(t, tuple(edits))
        assert why == "", (label, rev, why)
        h[rev] = netlist(t, rel, t / "y")
        h[rev + "_clean"] = netlist(tree, rel, t / "y0")
    rows.append({"arm": label, "file": rel, **h, "mutant_same_base_head": h["base"] == h["head"],
                 "mutant_differs_from_clean": h["head"] != h["head_clean"]})

patch = "tb/maap/mutations/validator-maap-version-1-only.patch"
h = {}
for rev, tree in (("base", base), ("head", head)):
    t = work / "maap_patch" / rev
    shutil.copytree(tree / "hdl", t / "hdl")
    subprocess.run(["git", "init", "-q"], cwd=t, check=True)
    r = subprocess.run(["git", "apply", str(tree / patch)], cwd=t, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    rel = "hdl/packet_engine/KL_pp_rx_validator.sv"
    h[rev] = netlist(t, rel, t / "y")
    h[rev + "_clean"] = netlist(tree, rel, t / "y0")
rows.append({"arm": patch, "file": "hdl/packet_engine/KL_pp_rx_validator.sv", **h,
             "mutant_same_base_head": h["base"] == h["head"],
             "mutant_differs_from_clean": h["head"] != h["head_clean"]})
out.write_text(json.dumps(rows, indent=1) + "\n")
for r in rows:
    print(f"{r['arm']}: same_base_head={r['mutant_same_base_head']} "
          f"differs_from_clean={r['mutant_differs_from_clean']}")
