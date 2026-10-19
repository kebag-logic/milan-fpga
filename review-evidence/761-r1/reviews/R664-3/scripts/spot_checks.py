#!/usr/bin/env python3
"""Read-only checks of round-3 logic identity, recipe coverage and receipts."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args]).decode()
def tokens(s):
    return re.sub(r"\s+", "", re.sub(r"//[^\n]*|/\*.*?\*/", "", s, flags=re.S))
for name in ("hdl/milan/milan_datapath.sv", "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"):
    assert tokens(git("show", "eef90b42:" + name)) == tokens((root/name).read_text())
    print("PASS executable RTL unchanged:", name)
assert git("diff", "--name-only", "336a6f6a..HEAD").splitlines() == ["tb/verilator/milan_dp/README.md"]
print("PASS mutant receipt head 336a6f6a differs from reviewed head only in README")
make = (root/"tb/verilator/milan_dp/Makefile").read_text()
assert re.search(r"^CPP\s*[:?]?=\s*sim_main.cpp", make, re.M)
for name in ("nxn", "nxndv", "nxn8", "nxn4c"):
    recipe = make.split(f"build-{name}:",1)[1].split(f"exec-{name}:",1)[0]
    print(f"RECIPE build-{name}: " + " ".join(recipe.splitlines()[1:]))
    assert "sim_nxn.cpp" in recipe
ax = make.split("define AX1X1_BUILD",1)[1].split("endef",1)[0]
assert "$(CPP)" in ax and "sim_nxn.cpp" not in ax
assert "[762-DP]" not in (root/"tb/verilator/milan_dp/sim_main.cpp").read_text()
print("CONFIRMED shipping AX1X1_BUILD uses sim_main.cpp; new [762-DP] case absent there")
nx8 = make.split("build-nxn8:",1)[1].split("exec-nxn8:",1)[0]
for key in ("TALKER_WIRE_CHANS_P", "AUDIO_IF_SLOTS_P", "AUDIO_IF_MASTER_P", "LPF_P"):
    assert "-G"+key not in nx8
    line = next(l.strip() for l in (root/"hdl/milan/milan_datapath.sv").read_text().splitlines() if re.search(r"parameter.*\b"+key+r"\s*=",l))
    print("NxN8 inherits",line)
print("Shipping geometry:", " ".join(ax.split()))
pub = packet/"scratch/public/author-r3/receipts"
for mutant, n in (("clean",0),("tie0",2),("sink1",2),("bound",1)):
    text = (pub/f"r3-mutants/{mutant}.run.log").read_text()
    failures = [l for l in text.splitlines() if "[FAIL]" in l]
    assert len(failures) == n and all("[762-DP]" in l for l in failures)
    assert f"checks: 1981   failures: {n}" in text
    print(f"PASS published {mutant}: 1981 checks, {n} named failures")
    print("\n".join(failures))
    build = (pub/f"r3-mutants/{mutant}.build.log").read_text()
    assert "sim_nxn.cpp" in build and "-GN_STREAMS=4" in build and "-GTALKER_WIRE_CHANS_P=4" in build
    print("PASS build receipt is N=4, four wire channels (Arty geometry)")
lines = (pub/"r3-focused/c3-milan_dp.762-DP-lines.txt").read_text()
assert lines.count("[ok]") == 52 and lines.count("-- [762-DP]") == 4
print("PASS broad-leg excerpt: 4 cases x 13 successful checks")
gates = (pub/"r3-static/gates.tsv").read_text().splitlines()
bad = [l.split("\t")[:2] for l in gates if l.split("\t")[1] != "0"]
assert len(gates) == 82 and bad == [["todo_ownership_selftest","1"],["act_ci_selftest","1"]]
print("PASS static receipt census: 80/82 rc 0; two explicitly reported host exceptions")
gate50 = (pub/"r3-gate50/ci_controls.d30a208d.tsv").read_text().splitlines()
assert len(gate50) == 14 and all(l.split("\t")[1] == "0" for l in gate50)
print("PASS gate_50 receipt census: 14/14 rc 0")
commit=json.loads((packet/"receipts/evidence-authentication.json").read_text())
v=commit["verification"]
print("Publication authentication:",json.dumps({k:v[k] for k in ("verified","reason","verified_at")}))
print("Digest identity is verified separately; no signed execution attestation is established.")
