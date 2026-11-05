#!/usr/bin/env python3
"""Run the bootsa leg's own planted controls plus reviewer probes in parallel.
usage: VERILATOR=<pinned> python3 -I par_mutants.py <tree> <logdir> <jobs>
Imports the tree's own bootsa_mutants.py (MUTATIONS, build, run_leg, verdict) and adds probes.
Each case: plant into a copy of the RTL, build with the suite recipe, run, save the leg log,
print the driver's own verdict. The clean leg must already be built in <tree>/.../obj_bootsa."""
import concurrent.futures as cf, re, sys, tempfile
from pathlib import Path
tree, logs, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(tree / "tb/verilator/milan_dp"))
import bootsa_mutants as bm  # noqa: E402
SAT = "      else if (ctl_sa_idx_r != TX_SA_IW_C'(TX_SA_BEATS_C)) ctl_sa_idx_r <= ctl_sa_idx_r + 1'b1;"
EXTRA = [
    ("PROBE together, all four early-enable source checks named",
     {"DP_SRC": bm.HOLD["MAAP"] + bm.HOLD["AAF"] + bm.HOLD["CRF"]},
     [bm.ON_MAAP, bm.ON_CRF, bm.OFF_AAF, bm.OFF_CRF]),
    ("PROBE stamp position saturates one beat early",
     {"DP_SRC": [(SAT, SAT.replace("TX_SA_IW_C'(TX_SA_BEATS_C)", "TX_SA_IW_C'(TX_SA_BEATS_C - 1)"))]},
     [bm.OCTETS]),
    ("PROBE stamp position never advances",
     {"DP_SRC": [(SAT, "      else                                                 ctl_sa_idx_r <= ctl_sa_idx_r;")]},
     [bm.OCTETS]),
]
CASES = list(bm.MUTATIONS) + EXTRA

def one(m):
    name, plants, breaks = m
    tag = re.sub(r"[^A-Za-z0-9]+", "_", name)[:48]
    work = Path(tempfile.mkdtemp(prefix="bsa-", dir=str(logs.parent / "scratch")))
    sources = {}
    for var, edits in plants.items():
        text = bm.RTL[var].read_text()
        for a, b in edits:
            if text.count(a) != 1:
                return name, f"pattern count {text.count(a)}"
            text = text.replace(a, b)
        p = work / f"{tag}_{bm.RTL[var].name}"; p.write_text(text); sources[var] = p
    exe = bm.build(sources, work / f"obj_{tag}")
    if exe is None:
        return name, "did not build"
    rc, out = bm.run_leg(exe)
    (logs / f"mut_{tag}.log").write_text(out)
    fails = [l.strip() for l in out.splitlines() if l.strip().startswith("[FAIL]")]
    return name, f"{bm.verdict(rc, out, breaks)} rc={rc} fails={len(fails)} :: " + " | ".join(fails)

clean = tree / "tb/verilator/milan_dp/obj_bootsa" / bm.EXE
rc, out = bm.run_leg(clean)
print(f"CLEAN: {bm.verdict(rc, out, [])} rc={rc}")
with cf.ThreadPoolExecutor(jobs) as ex:
    for name, res in ex.map(one, CASES):
        print(f"CASE {name}: {res}", flush=True)
