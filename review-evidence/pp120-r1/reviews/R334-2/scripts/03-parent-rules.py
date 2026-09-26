#!/usr/bin/env python3
"""Apply the parent's own per-file scanners (fetched read-only at parent 7eb3b0d4 by
00-fetch-parent.sh) to the processor files this PR touches, at base, round-2 head
and round-3 head. Port contracts via check_port_contracts.scan_ports (the parser the
parent gate uses); the effect bundle's attribution is read from sv_ports.declarations
directly, so the report shows WHICH //! run documents each effect/name port."""
import importlib.util, os, subprocess, sys
from pathlib import Path
PK = Path(__file__).resolve().parents[1]; S = PK / "scratch/parent-scripts"; sys.path.insert(0, str(S))
C = os.environ.get("CLONE", "$REVIEWS/r334-2-pp120")
REVS = (("base", "0922e43408f891fc0b84a84691df86b4fd0f1c0d"), ("r2", "a9b7874d415d935949becd7ccfd58799927efb08"),
        ("head", "83c84b19e09d397ed2eb6f5ace337686ce0ef86b"))
def show(rev, path):
    """File text at a revision ('' when absent)."""
    r = subprocess.run(["git", "-C", C, "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""
import check_port_contracts as ports, check_cpp_idiom as cpp, check_py_idiom as py, measure_test_evidence as evid  # noqa
from sv_ports import declarations  # noqa
print("== Port contracts: undocumented ports per file (parent scan_ports)")
for f in ("tb/pp_top/pp_top_wrap.sv", "hdl/aecp/KL_aecp_desc_store.sv", "hdl/aecp/KL_aecp_engine.sv",
          "hdl/top/protocol_processor_top.sv", "tb/desc_mem_guard/wrap.sv"):
    res = {n: ports.scan_ports(show(r, f)) for n, r in REVS}
    print(f"  {f}: " + ", ".join(f"{n} {t}/{len(u)}" for n, (t, u) in res.items())
          + f"; newly undocumented vs base at head: {sorted(set(res['head'][1]) - set(res['base'][1]))}"
          + f"; fixed vs base at head: {sorted(set(res['base'][1]) - set(res['head'][1]))}")
GROUP = ("aecp_name_wr_o", "dbg_name_live_we_o", "dbg_dyn_writes_o", "aecp_nvm_stb_o", "aecp_nvm_mark_o", "dbg_notify_enq_o")
print("== pp_top_wrap.sv: attribution of the six effect/name ports (first words of the //! that documents each)")
for n, r in REVS:
    docs = {name: doc for _m, name, doc, _mb, k in declarations(show(r, "tb/pp_top/pp_top_wrap.sv")) if k != "param"}
    print(f"  {n}:")
    for g in GROUP:
        if g in docs:
            d = " ".join(docs[g].split())
            print(f"    {g:20s} {'UNDOCUMENTED' if not d else repr(d[:60])}")
print("== Rule 11 (C++ idiom) tb/pp_top/sim_main.cpp")
for n, r in REVS:
    t = show(r, "tb/pp_top/sim_main.cpp")
    counts = dict(cpp.scan(t, "tb/pp_top/sim_main.cpp"))
    print(f"  {n}: {counts}; long functions (> {cpp.LONG_FUNCTION_LINES} lines): {cpp.long_functions(cpp.blank_non_code(t))}")
print("== Rule 12 (Python idiom) tb/pp_top/name_wr_mutant.py at head")
print("  ", dict(py.scan(show(REVS[2][1], "tb/pp_top/name_wr_mutant.py"), "tb/pp_top/name_wr_mutant.py")[0]))
print("== Wall-clock / DUT-source reading at head")
for f in ("tb/pp_top/name_wr_mutant.py", "tb/pp_top/sim_main.cpp"):
    t = show(REVS[2][1], f); suf = Path(f).suffix
    print(f"  {f}: uses_wall_clock={evid.uses_wall_clock(t, suf)} reads_dut_source={evid.reads_dut_source(t, suf) if suf == '.py' else 'n/a'}")
