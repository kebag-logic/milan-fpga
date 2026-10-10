#!/usr/bin/env python3
"""Reviewer M5 probes: plant link-level defects in a scratch copy of KL_maap.sv,
build the unit harness of the given tree against each, and record which M5
checks fail. No checkout file is edited.
Usage: VERILATOR=<path> python3 -I probe_m5.py <tree> <workdir> <receipts-dir>"""
import os, subprocess, sys, pathlib, concurrent.futures as cf
tree, work, out = (pathlib.Path(a).resolve() for a in sys.argv[1:4])
rtl = (tree / "hdl/ieee1722/maap/KL_maap.sv").read_text()
EDGE = "wire port_operational_p = port_operational_i && !port_operational_r;"
PROBES = {
    "clean": [],
    # restart at both edges: an outage restarts at the loss and again at the return
    "p1_both_edges": [(EDGE, "wire port_operational_p = port_operational_i != port_operational_r;")],
    # leaving the operational state releases the walk (INITIAL) while the link is down
    "p2_idle_while_down": [("          if (!enable_i) state_r <= IDLE_S;",
                            "          if (!enable_i || !port_operational_i) state_r <= IDLE_S;")],
    # the probe/announce timer freezes while the link is down
    "p3_timer_frozen_while_down": [("if (tick_ms_w && timer_ms_r != '0) timer_ms_r",
                                    "if (tick_ms_w && timer_ms_r != '0 && port_operational_i) timer_ms_r")],
    # the return is ignored (no PortOperational! at all)
    "p4_no_return_event": [(EDGE, "wire port_operational_p = 1'b0;")],
    # the return restarts but counts a conflict
    "p5_return_counts_conflict": [("            if (restart_w)\n              conflicts_o",
                                   "            if (restart_w || port_operational_p)\n              conflicts_o")],
}
M5 = ("M5 B.3.5.9 link return restarts PROBE", "M5 B.3.5.9 link return revokes and reprobes",
      "M5 stable operational level does not restart", "M5 B.3.5.9 link loss is no event; return reprobes")
V = os.environ.get("VERILATOR", "verilator")
def run(name):
    src = rtl
    for a, b in PROBES[name]:
        if src.count(a) != 1:
            return name, f"anchor count {src.count(a)} for {a!r}", None, None
        src = src.replace(a, b)
    d = work / name; d.mkdir(parents=True, exist_ok=True)
    f = d / "KL_maap.sv"; f.write_text(src)
    b = subprocess.run(["make", "-s", "-C", str(tree / "tb/verilator/maap"), "build", f"MAAP_RTL={f}",
                        f"MDIR={d/'obj'}", f"VERILATOR={V}", "VERILATOR_JOBS=2"], capture_output=True, text=True)
    (out / f"{name}.build.log").write_text(b.stdout + b.stderr)
    if b.returncode:
        return name, f"build rc {b.returncode}", None, None
    r = subprocess.run([str(d / "obj/VKL_maap_sim")], cwd=d, capture_output=True, text=True)
    (out / f"{name}.run.log").write_text(r.stdout + r.stderr)
    fails = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    return name, f"rc {r.returncode}", fails, [m for m in M5 if any(m in x for x in fails)]
out.mkdir(parents=True, exist_ok=True)
with cf.ThreadPoolExecutor(6) as ex:
    res = list(ex.map(run, PROBES))
ok = True
with open(out / "summary.txt", "w") as s:
    for name, status, fails, m5 in res:
        line = f"{name}: {status}; failures={len(fails) if fails is not None else 'n/a'}; M5 checks failed={m5}"
        print(line); s.write(line + "\n")
        for x in fails or []:
            s.write(f"    {x}\n")
        new = "M5 B.3.5.9 link loss is no event; return reprobes"
        if name == "clean":
            ok &= status == "rc 0" and fails == []
        else:
            ok &= status == "rc 1" and m5 is not None and new in m5
sys.exit(0 if ok else 1)
