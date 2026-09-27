#!/usr/bin/env python3
"""Composition probe for #571: elaborate the parent RTL and read the
processor dynamic-state row counts out of the elaborated tree.

Usage: elab_probe.py <repo> <verilator> <workdir>

For each shape (the shipping arty_current header, plus a synthetic copy of it
with distinct AUDIO_UNIT=2, CLOCK_DOMAIN=3, CONTROL=4 counts) this runs
`verilator --json-only` on milan_datapath with the same source list and
include order the repository lint gate uses, then reports the
N_AUDIO_UNIT_P / N_CLK_DOMAIN_P / N_CONTROL_P constants of every elaborated
KL_aecp_dyn_state module. Distinct counts reaching distinct processor
parameters is the end-to-end binding proof; equal shipping counts cannot
expose a swap. Nothing in <repo> is written.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

repo, verilator, work = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(repo / "scripts"))
import lint_rtl  # noqa: E402  (repository lint gate: source list + incdirs)

SHIP = "configs/generated/endstation_arty_current"
WANT = ("N_AUDIO_UNIT_P", "N_CLK_DOMAIN_P", "N_CONTROL_P")


def sources():
    decls = lint_rtl.declarations()
    inc = lint_rtl.included(decls)
    pkgs = lint_rtl.packages(decls)
    return ([p for p in pkgs if Path(p).name not in inc]
            + [r for r in sorted(decls) if r not in pkgs and Path(r).name not in inc]
            + lint_rtl.submodule_sources())


def synth_dir():
    dst = work / "synthetic_gen_parent"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(repo / SHIP, dst)
    hdr = dst / "gen" / "adp_shape_defaults.svh"
    text = hdr.read_text()
    for sym, val in (("AEM_N_AUDIO_UNIT_C", 2), ("AEM_N_CLKDOM_C", 3),
                     ("AEM_N_CONTROL_C", 4)):
        text, n = re.subn(rf"({sym}\s*=\s*)\d+", rf"\g<1>{val}", text)
        assert n == 1, sym
    hdr.write_text(text)
    return str(dst)


def walk(node, out):
    if isinstance(node, dict):
        if node.get("type") == "MODULE" and "KL_aecp_dyn_state" in node.get("name", ""):
            got = {}
            for st in node.get("stmtsp", []):
                if st.get("type") == "VAR" and st.get("name") in WANT:
                    val = st.get("valuep") or []
                    got[st["name"]] = val[0].get("name") if val else None
            out.append((node.get("name"), node.get("origName"), got))
        for v in node.values():
            walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)


def run(label, first_inc):
    incs = [first_inc] + lint_rtl.include_dirs()[1:]
    out = work / f"{label}.tree.json"
    cmd = [verilator, "--json-only", "--json-only-output", str(out), "--sv",
           "--top-module", "milan_datapath", "-Wno-fatal", "-Wno-lint",
           "-Wno-style"]
    cmd += ["-I" + (d if d.startswith("/") else str(repo / d)) for d in incs]
    axis = lint_rtl.axis_lib()
    if axis:
        cmd += ["-y", str(repo / axis)]
    cmd += [str(repo / s) for s in sources()]
    p = subprocess.run(cmd, cwd=repo, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True)
    errs = [ln for ln in p.stdout.splitlines() if ln.startswith("%Error")]
    print(f"== {label}: verilator rc={p.returncode}, %Error lines={len(errs)}")
    for ln in errs[:20]:
        print("   ", ln.replace(str(repo) + "/", ""))
    if p.returncode != 0 or not out.exists():
        return None
    found = []
    walk(json.loads(out.read_text()), found)
    for name, orig, got in found:
        print(f"   elaborated {orig}: {got}")
    out.unlink()
    return found


ship = run("shipping_arty_current", SHIP)
syn = run("synthetic_2_3_4", synth_dir())


def only(found):
    return [g for _n, _o, g in (found or [])]


ok = (ship is not None and syn is not None
      and only(ship) == [{"N_AUDIO_UNIT_P": "32'h1", "N_CLK_DOMAIN_P": "32'h1", "N_CONTROL_P": "32'h1"}]
      and only(syn) == [{"N_AUDIO_UNIT_P": "32'h2", "N_CLK_DOMAIN_P": "32'h3", "N_CONTROL_P": "32'h4"}])
print("RESULT:", "PASS" if ok else "FAIL (inspect values above)")
sys.exit(0 if ok else 1)
