#!/usr/bin/env python3
"""Apply the parent's own per-file scanners (fetched read-only at parent
7eb3b0d4 into scratch/parent-scripts) to the base and head versions of the
processor files this PR touches. Focused: no parent tree, no bank; it checks the
four round-2 parent-gate findings on the processor side only."""
import importlib.util, subprocess, sys
from pathlib import Path

PK = Path(__file__).resolve().parents[1]
S = PK / "scratch/parent-scripts"
sys.path.insert(0, str(S))
CLONE = "$REVIEWS/r334-1-pp120"
BASE, HEAD = "0922e43408f891fc0b84a84691df86b4fd0f1c0d", "a9b7874d415d935949becd7ccfd58799927efb08"


def load(name: str):
    """Import one parent script as a module without running its main()."""
    spec = importlib.util.spec_from_file_location(name, S / f"{name}.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


def show(rev: str, path: str) -> str:
    """File text at a revision ('' when absent)."""
    r = subprocess.run(["git", "-C", CLONE, "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


cpp, py, ports, evid = (load(n) for n in ("check_cpp_idiom", "check_py_idiom",
                                         "check_port_contracts", "measure_test_evidence"))
print("== Rule 11 (C++ idiom) tb/pp_top/sim_main.cpp")
for rev in (BASE, HEAD):
    t = show(rev, "tb/pp_top/sim_main.cpp")
    print(f"  {rev[:8]} {dict(cpp.scan(t, 'tb/pp_top/sim_main.cpp'))}")
    print(f"  {rev[:8]} long functions (> {cpp.LONG_FUNCTION_LINES} lines): {cpp.long_functions(cpp.blank_non_code(t))}")
print("== Rule 12 (Python idiom) tb/pp_top/name_wr_mutant.py at head")
counts, sites = py.scan(show(HEAD, "tb/pp_top/name_wr_mutant.py"), "tb/pp_top/name_wr_mutant.py")
print(f"  {dict(counts)}")
print("== Port contracts (undocumented ports per file, base -> head)")
for f in ("hdl/aecp/KL_aecp_desc_store.sv", "hdl/aecp/KL_aecp_engine.sv",
          "hdl/top/protocol_processor_top.sv", "tb/pp_top/pp_top_wrap.sv", "tb/desc_mem_guard/wrap.sv"):
    b = ports.scan_ports(show(BASE, f)); h = ports.scan_ports(show(HEAD, f))
    new = sorted(set(h[1]) - set(b[1]))
    print(f"  {f}: ports {b[0]} -> {h[0]}, undocumented {len(b[1])} -> {len(h[1])}, newly undocumented {new}")
print("== Wall-clock dependence / DUT-source reading (head)")
for f in ("tb/pp_top/name_wr_mutant.py", "tb/pp_top/sim_main.cpp", "tb/pp_top/Makefile"):
    suf = Path(f).suffix or ".mk"
    t = show(HEAD, f)
    wc = evid.uses_wall_clock(t, suf) if suf in (".py", ".cpp", ".sh") else "n/a"
    rd = evid.reads_dut_source(t, suf) if suf == ".py" else "n/a"
    print(f"  {f}: uses_wall_clock={wc} reads_dut_source={rd}")
