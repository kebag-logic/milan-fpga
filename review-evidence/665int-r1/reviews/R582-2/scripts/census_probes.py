#!/usr/bin/env python3
"""Reviewer probes of publication_census.py: each plant is applied to a
scratch copy of milan_datapath.sv and the census --check is run on it.
Usage: census_probes.py <checkout> <scratch-dir>. Writes nothing in the checkout."""
import subprocess, sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
src = (repo / "hdl/milan/milan_datapath.sv").read_text(encoding="utf-8")
SITE = "    crft_stat_c[4]     = 1'b0;"
CRF = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
PORT = ".srp_domain_change_o     (pp_cd_srp_domain_change_w),"
PROBES = [
    # (name, old, new, expect_refused)
    ("control: unmodified", None, None, False),
    ("alias wire read on the wire", CRF,
     "  wire probe_alias_w = pp_cd_srp_over_limit_w;\n" + CRF.replace("=", "= ~probe_alias_w &", 1), True),
    ("case selector read in always block", SITE,
     SITE + "\n    case (pp_cd_srp_over_limit_w) 1'b1: crft_stat_c[4] = 1'b1; default: crft_stat_c[4] = 1'b0; endcase", True),
    ("case item label read in always block", SITE,
     SITE + "\n    case (1'b1) pp_cd_srp_over_limit_w: crft_stat_c[4] = 1'b1; default: crft_stat_c[4] = 1'b0; endcase", True),
    ("function body read, called on the wire", CRF,
     "  function automatic logic probe_f();\n    probe_f = pp_cd_srp_over_limit_w;\n  endfunction\n"
     + CRF.replace("=", "= ~probe_f() &", 1), True),
    ("wrapper output renamed off the pp_cd_ prefix, read on the wire", None, None, True),
]
results = []
for name, old, new, expect in PROBES:
    text = src
    if name.startswith("wrapper output renamed"):
        assert src.count(PORT) == 1, PORT
        text = src.replace(PORT, ".srp_domain_change_o     (probe_dom_chg_w),").replace(
            CRF, "  wire probe_dom_chg_w;\n" + CRF.replace("=", "= ~probe_dom_chg_w &", 1), 1)
    elif old is not None:
        assert src.count(old) == 1, (name, src.count(old))
        text = src.replace(old, new, 1)
    path = scratch / (name.split(":")[0].replace(" ", "_").replace(",", "") + ".sv")
    path.write_text(text, encoding="utf-8")
    res = subprocess.run([sys.executable, "-I", "-B", str(repo / "sw/mailbox/publication_census.py"),
                          "--check", "--datapath", str(path)], capture_output=True, text=True)
    refused = res.returncode != 0
    first = next((l for l in res.stdout.splitlines() if l.startswith("[FAIL]")), res.stdout.strip().splitlines()[-1])
    verdict = "as expected" if refused == expect else "UNEXPECTED"
    results.append(verdict)
    print(f"[{verdict}] {name}: rc={res.returncode} {'REFUSED' if refused else 'ACCEPTED'} :: {first[:220]}")
print(f"probes: {len(results)}, unexpected: {results.count('UNEXPECTED')}")
