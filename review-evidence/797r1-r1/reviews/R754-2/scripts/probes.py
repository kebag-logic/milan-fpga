#!/usr/bin/env python3
"""Directed refusal probes on disposable copies. Usage: probes.py <clone> <scratch> <python-with-wavedrom>.
One row per probe: command rc, page byte-identical after, last line."""
import hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path
clone, scratch, py = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
RTL = "hdl/common/csr/milan_csr.sv"; DESC = "scripts/register_descriptions.json"; PAGE = "docs/reference/REGISTER_MAP.md"
PATHS = ["scripts", "hdl/common/csr", "hdl/common/ethernet_packet_pkg.sv", "hdl/milan/milan_datapath.sv", "hdl/common/KL_link_guard.sv",
         "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv", "configs/generated/endstation_ax7101_1x1_tdm8", PAGE, "docs/reference/milan_feature_status.json",
         "docs/diagrams", "docs/design/CSR_REGISTER_NOTES.md"]
base = scratch / "probe_base"
if base.exists(): shutil.rmtree(base)
base.mkdir(parents=True)
subprocess.run(f"git -C {clone} archive HEAD {' '.join(PATHS)} | tar -x -C {base}", shell=True, check=True)
def rep(rel, a, b):
    def f(d):
        p = d / rel; t = p.read_text(encoding="utf-8")
        if a not in t: raise SystemExit(f"plant missed {a}")
        p.write_text(t.replace(a, b, 1), encoding="utf-8")
    return f
def desc(fn):
    def f(d):
        p = d / DESC; j = json.loads(p.read_text(encoding="utf-8")); fn(j); p.write_text(json.dumps(j, indent=2), encoding="utf-8")
    return f
def find(j, reg):
    for k, v in j.items():
        if isinstance(v, dict):
            if reg in v and isinstance(v[reg], dict) and "purpose" in v[reg]: return v[reg]
            r = find(v, reg)
            if r: return r
    return None
def blank(j): r = find(j, "ETH_GUARD"); r["purpose"] = ""; r["name"] = ""
def note(j): r = find(j, "ETH_GUARD"); r["notes"] = list(r.get("notes", [])) + [" ".join(["word"] * 340)]
def cell(j): r = find(j, "ETH_GUARD"); r["fields"]["ETH_GUARD"] = " ".join(["word"] * 340)
def onecol(j): r = find(j, "ETH_GUARD"); r["notes"] = list(r.get("notes", [])) + ["| Note |\n|---|\n| " + " ".join(["word"] * 40) + " |"]
PROBES = [
 ("masked write arm --write", "--write", rep(RTL, "A_CHMAP_CTRL: chmap_ctrl <= s_axi_wdata;", "A_CHMAP_CTRL: chmap_ctrl <= s_axi_wdata & 32'h1FF;")),
 ("blank purpose and name --write", "--write", desc(blank)),
 ("340-word note --write", "--write", desc(note)),
 ("340-word field cell --write", "--write", desc(cell)),
 ("one-column note table --write", "--write", desc(onecol)),
 ("doorbell added to a write arm --check", "--check", rep(RTL, "A_SCRATCH:   scratch  <= s_axi_wdata;", "A_SCRATCH: begin scratch <= s_axi_wdata; pp_req_r <= 1'b1; end")),
 ("unknown description key --check", "--check", desc(lambda j: find(j, "ETH_GUARD")["fields"].__setitem__("NOT_A_FIELD", "x"))),
]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for i, (name, cmd, plant) in enumerate(PROBES):
    d = scratch / f"probe_{i}"
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(base, d)
    plant(d); before = sha(d / PAGE)
    r = subprocess.run([py, "-B", str(d / "scripts/gen_register_reference.py"), cmd], capture_output=True, text=True, cwd=d)
    tail = (r.stdout + r.stderr).strip().split("\n")[-1][:220]
    print(f"{name}\trc={r.returncode}\tpage_same={sha(d / PAGE) == before}\t{tail}")
    shutil.rmtree(d)
shutil.rmtree(base)
