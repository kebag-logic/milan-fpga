#!/usr/bin/env python3
"""mbx_port_width_lint.py PROBE_JSON CLONE OUTDIR VERILATOR [--plant]

Write an SV top that declares one net per KL_mbx / KL_mbx_wb port at exactly
the width milan_soc.py's Instance connects (from mbx_soc_probe.py's record),
binds each by name, and lint it with the mailbox sources under -Wall; any WIDTH or
PIN warning, or any error, fails. A width the SoC binds that the RTL port does not have fails.
Inputs the SoC ties to a constant are bound to a sized zero, as LiteX emits
them. --plant shrinks pub_sid_o by one bit, the negative control.
"""
import json
import os
import subprocess
import sys

probe, clone, outdir, verilator = sys.argv[1:5]
plant = "--plant" in sys.argv
rec = json.load(open(probe))
os.makedirs(outdir, exist_ok=True)
lines = ["`default_nettype none", "module mbx_width_probe;"]
for of in ("KL_mbx_wb", "KL_mbx"):
    ports = rec["mbx_instances"][of]
    binds = []
    for name, kind, width, const in ports:
        if const and kind == "Input":
            # an idle tie (F0): LiteX emits it as a sized zero, extended
            binds.append(f"    .{name}('0)")
            continue
        if plant and of == "KL_mbx" and name == "pub_sid_o":
            width -= 1
        net = f"{of}_{name}"
        lines.append(f"  logic [{width - 1}:0] {net};")
        binds.append(f"    .{name}({net})")
    lines.append(f"  {of} u_{of} (\n" + ",\n".join(binds) + "\n  );")
lines.append("endmodule")
top = os.path.join(outdir, "mbx_width_probe.sv")
open(top, "w").write("\n".join(lines) + "\n")
srcs = [os.path.join(clone, "hdl/milan/mailbox", f) for f in (
    "KL_mbx_pkg.sv", "KL_mbx_ring.sv", "KL_mbx_rx.sv", "KL_mbx_tx.sv",
    "KL_mbx_evt.sv", "KL_mbx.sv", "KL_mbx_wb.sv")]
cmd = [verilator, "--lint-only", "-Wall", "-Wno-UNDRIVEN", "-Wno-UNUSEDSIGNAL",
       "-Wno-PINCONNECTEMPTY", "-Wno-DECLFILENAME", "-Wno-MULTITOP",
       "-Wno-fatal", "--top-module", "mbx_width_probe", *srcs, top]
r = subprocess.run(cmd, capture_output=True, text=True)
out = r.stdout + r.stderr
print(out[-4000:])
width = [l for l in out.splitlines() if l.startswith("%Warning-WIDTH") or l.startswith("%Warning-PIN")
         or (l.startswith("%Error") and "Exiting due to" not in l)]
print(f"verilator rc={r.returncode} width/error lines={len(width)} plant={plant}")
ok = (r.returncode == 0 and not width) if not plant else (r.returncode != 0 or bool(width))
sys.exit(0 if ok else 1)
