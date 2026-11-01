#!/usr/bin/env python3
"""Two probes of gate 1h at one clone, none of them writing there.

usage: gate1h_equiv_and_mutants.py <clone> <scratch dir>
1. the gate's read of the shipped text against the build's read (the record's own flags, no extra -I):
   whole output and the datapath's module, byte for byte; the flags syn/yosys/run.sh hands sv2v are compared by grep.
2. reader mutants on disposable copies: dropping the defines, dropping the include directories, leaving the shipped
   file in the list instead of the planted text. Each must turn the gate red by name.
"""
import concurrent.futures, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
root = Path(sys.argv[1]).resolve(); scratch = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "syn/ooc"))
import dp_srcs
rec, bad, rc = dp_srcs.ask_authority("milan_datapath")
inc = [a for i in rec["incdir"] for a in ("-I", i)]; defs = [f"-D{d}" for d in rec["define"]]
dp = str(root / "hdl/milan/milan_datapath.sv")
build = subprocess.run(["sv2v", "--pass-through", *defs, *inc, *rec["src"]], capture_output=True, text=True)
with tempfile.TemporaryDirectory(dir=scratch) as t:
    planted = Path(t) / "milan_datapath.sv"; planted.write_text(Path(dp).read_text())
    gate = subprocess.run(["sv2v", "--pass-through", *defs, "-I", str(root / "hdl/milan"), *inc,
                           *[str(planted) if s == dp else s for s in rec["src"]]], capture_output=True, text=True)
rx = r"^\s*module\s+milan_datapath\b.*?^\s*endmodule\b"
m_b = re.findall(rx, build.stdout, re.M | re.S); m_g = re.findall(rx, gate.stdout, re.M | re.S)
nt = lambda text: re.sub(r"^\s*// Trace: .*\n", "", text, flags=re.M)
print("build rc", build.returncode, "gate rc", gate.returncode, "whole output identical:", build.stdout == gate.stdout,
      "module count", len(m_b), len(m_g), "module identical:", m_b == m_g)
print("same with sv2v's own path-bearing Trace comment lines removed: whole", nt(build.stdout) == nt(gate.stdout),
      "module", nt(m_b[0]) == nt(m_g[0]), "non-Trace bytes", len(nt(gate.stdout)))
print("module text carries plane once:", len(re.findall(r"^\s*KL_gptp_shadow\b", m_g[0], re.M)), "whole output:", len(re.findall(r"^\s*KL_gptp_shadow\b", gate.stdout, re.M)))
MUT = [("no defines", '*(f"-D{define}" for define in record["define"]),\n', ""),
       ("no include directories", '*(arg for incdir in record["incdir"] for arg in ("-I", incdir)),\n', ""),
       ("the shipped file stays in the list", 'str(planted) if Path(src).resolve() == datapath else src', 'src')]
def one(i):
    name, old, new = MUT[i]
    c = scratch / f"mut{i}"
    shutil.rmtree(c, ignore_errors=True)
    shutil.copytree(root, c, symlinks=True)
    p = c / "sw/builder/test_builder.py"; s = p.read_text(); assert s.count(old) == 1, old; s = s.replace(old, new)
    if i == 2: s = s.replace('assert sources.count(str(planted)) == 1, \\\n            f"gate 1h: the build does not read {datapath.name} once: {record[\'src\']}"\n', "")
    p.write_text(s)
    o = subprocess.run([sys.executable, "sw/builder/test_builder.py", "--gates", "test_gptp_datapath_carries_the_launch_shape"], cwd=c, capture_output=True, text=True)
    why = next((l for l in (o.stdout + o.stderr).splitlines() if l.startswith("AssertionError") or "ALL GATES PASS" in l), "(no assertion line: " + (o.stdout + o.stderr)[-160:].replace("\n", " ") + ")")
    shutil.rmtree(c, ignore_errors=True)
    return f"{'ok ' if o.returncode else 'BAD'} rc={o.returncode} {name}: {why[:180]}"
with concurrent.futures.ThreadPoolExecutor(3) as ex:
    for line in ex.map(one, range(len(MUT))): print(line)
