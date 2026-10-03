#!/usr/bin/env python3
"""Show that the route endpoint's verdict ignores the routing-completion report.

Usage: probe_route_status.py <repo checkout> <scratch dir>
Builds the shipped self-test's route fixture, records it with the real
route-1x1 policy, then adds the build's route status report (the file the
LiteX flow writes beside the route checkpoint) once clean and once with
unrouted nets and routing errors, and runs the CLI on both.
"""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_resource_gate as gate  # noqa: E402
import pp_resource_gate_selftest as st  # noqa: E402

shutil.rmtree(scratch, ignore_errors=True)
scratch.mkdir(parents=True)
folder = st.fixture(scratch / "arm", "route")
real = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]["route-1x1"]
entry = copy.deepcopy({k: v for k, v in real.items() if k != "record"})
entry["record"] = gate.record(folder, "route")
baseline = scratch / "baseline.json"
baseline.write_text(json.dumps({"endpoints": {"ep": entry}}))
st.plant(folder, "{repo}/hdl/milan/KL_pp_shadow.sv".replace("{repo}", str(scratch / "arm/repo")),
         "endmodule", "wire w; endmodule")
STATUS = ("Design Route Status\n"
          "                                               :      # nets :\n"
          "   ------------------------------------------- : ----------- :\n"
          "   # of logical nets.......................... :      120000 :\n"
          "   # of nets with routing errors.............. : {err:>11} :\n"
          "   #   unrouted nets.......................... : {err:>11} :\n")
for label, errors in (("clean route status", 0), ("route status with 37 unrouted nets", 37)):
    (folder / "alinx_ax7101_route_status.rpt").write_text(STATUS.format(err=errors))
    run = subprocess.run([sys.executable, "-B", str(repo / "syn/ooc/pp_resource_gate.py"), "check", str(folder),
                          "--endpoint", "ep", "--baseline", str(baseline)], capture_output=True, text=True)
    print(f"{label}: exit {run.returncode} | {run.stdout.strip().splitlines()[-1]}")
source = (repo / "syn/ooc/pp_resource_gate.py").read_text()
print(f"references to route status in pp_resource_gate.py: {source.count('route_status')}")
