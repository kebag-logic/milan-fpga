#!/usr/bin/env python3
"""Reviewer probe of scripts/check_m9_opcodes.py: runs the gate on disposable copies of the
tree in which one declaration form is added to hdl/aecp/KL_aecp_engine.sv, and reports
whether the gate passes (rc 0) or refuses (rc 1). usage: probe_m9_gate.py <repo> <scratch>"""
import shutil, subprocess, sys
from pathlib import Path
repo, scratch = Path(sys.argv[1]), Path(sys.argv[2]) / "m9probe"
GATE_OLD_RE = r"\blocalparam\b[^;]*?\b(OP_[A-Z0-9_]+_C)\s*="
# (label, text appended after the last OP_*_C localparam, expected rc, why)
FORMS = [
    ("control: unchanged tree", None, 0, "head passes"),
    ("canonical localparam, new opcode", "localparam logic [15:0] OP_PROBE_NEW_C = 16'h0077;", 1, "missing from kOpcodes"),
    ("parameter keyword (S1)", "parameter logic [15:0] OP_PROBE_NEW_C = 16'h0077;", 1, "unparsed"),
    ("parameter, existing opcode alias", "parameter logic [15:0] OP_PROBE_DUP_C = 16'h0004;", 1, "unparsed"),
    ("untyped localparam", "localparam OP_PROBE_NEW_C = 16'h0077;", 1, "unparsed"),
    ("int localparam", "localparam int OP_PROBE_NEW_C = 119;", 1, "unparsed"),
    ("uppercase radix", "localparam logic [15:0] OP_PROBE_NEW_C = 16'H0077;", 1, "unparsed"),
    ("bit type", "localparam bit [15:0] OP_PROBE_NEW_C = 16'h0077;", 1, "unparsed"),
    ("multi-line canonical", "localparam logic [15:0]\n    OP_PROBE_NEW_C = 16'h0077;", 1, "missing from kOpcodes"),
    ("comma list, second name", "localparam logic [15:0] OP_PROBE_A_C = 16'h0077, OP_PROBE_B_C = 16'h0078;", 1, "first name unparsed"),
    ("parameter in a comma list", "parameter logic [15:0] OP_PROBE_A_C = 16'h0004, OP_PROBE_B_C = 16'h0078;", 1, "unparsed"),
    ("line-commented declaration", "// localparam logic [15:0] OP_PROBE_NEW_C = 16'h0077;", 0, "a comment is not an arm"),
    ("comparison, not a declaration", "wire probe_w = (txn_w.opcode == OP_READ_DESCRIPTOR_C);", 0, "no new name"),
    ("enum member (outside the gate's stated scope)", "typedef enum logic [15:0] { OP_PROBE_NEW_C = 16'h0077 } probe_e;", None, "documented scope: localparam/parameter"),
    ("macro (outside the gate's stated scope)", "`define OP_PROBE_NEW_C 16'h0077", None, "documented scope: localparam/parameter"),
]
def run(form):
    t = scratch / "t"
    if t.exists(): shutil.rmtree(t)
    (t / "scripts").mkdir(parents=True); (t / "hdl/aecp").mkdir(parents=True); (t / "tb/pp_top").mkdir(parents=True)
    shutil.copy(repo / "scripts/check_m9_opcodes.py", t / "scripts")
    shutil.copy(repo / "tb/pp_top/sim_main.cpp", t / "tb/pp_top")
    eng = (repo / "hdl/aecp/KL_aecp_engine.sv").read_text()
    if form is not None:
        anchor = "localparam logic [15:0] OP_GET_CONTROL_C      = 16'h0019;"
        assert eng.count(anchor) == 1
        eng = eng.replace(anchor, anchor + "\n" + form)
    (t / "hdl/aecp/KL_aecp_engine.sv").write_text(eng)
    p = subprocess.run([sys.executable, str(t / "scripts/check_m9_opcodes.py")], capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()
unexpected = 0
for label, form, want, why in FORMS:
    rc, out = run(form)
    verdict = "info" if want is None else ("ok" if rc == want else "UNEXPECTED")
    unexpected += verdict == "UNEXPECTED"
    print(f"[{verdict}] {label}: rc {rc} (expected {want}; {why})")
    for l in out[-3:]: print(f"      {l}")
p = subprocess.run([sys.executable, str(repo / "scripts/check_m9_opcodes.py"), "--selftest"], capture_output=True, text=True)
print(f"selftest at head: rc {p.returncode}: {p.stdout.strip()}")
# load-bearing: the old declaration pattern must fail the new selftest
src = (repo / "scripts/check_m9_opcodes.py").read_text()
new_re = r'RE_DECLARED = re.compile(r"\b(?:localparam|parameter)\b[^;]*?\b(OP_[A-Z0-9_]+_C)\s*=")'
assert src.count(new_re) == 1
t = scratch / "old_re.py"; t.write_text(src.replace(new_re, f'RE_DECLARED = re.compile(r"{GATE_OLD_RE}")'))
p = subprocess.run([sys.executable, str(t), "--selftest"], capture_output=True, text=True)
print(f"selftest with the round-2 pattern: rc {p.returncode}: {p.stdout.strip()}")
unexpected += p.returncode == 0
print(f"forms: {len(FORMS)}, unexpected: {unexpected}")
sys.exit(1 if unexpected else 0)
