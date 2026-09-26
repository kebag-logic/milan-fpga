#!/usr/bin/env python3
"""Compare the processor's parameter inventory at the pin with the parent's
instantiation of protocol_processor_top, and probe the inventory checker.

Usage: param_agreement.py <clone> <processor-export-dir>
The export dir is a disposable copy of the processor tree; only it is mutated.
"""
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

clone, export = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location(
    "chk", clone / "protocol-processor/scripts/check-integrator-params.py")
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)

top = clone / "protocol-processor/hdl/top/protocol_processor_top.sv"
guide = clone / "protocol-processor/docs/guides/integrator.md"
diagram = clone / "protocol-processor/docs/diagrams/21-integration-faces.svg"
top_names = chk.top_parameters(top)
guide_names = chk.guide_parameters(guide)
diag_names = chk.diagram_parameters(diagram)
print(f"inventory: top {len(top_names)} guide {len(guide_names)} "
      f"diagram {len(diag_names)} equal={set(top_names) == set(guide_names) == set(diag_names)}")

# processor defaults
body = re.sub(r"//[^\n]*", "", top.read_text())
defaults = {n: re.search(rf"\b{n}\s*=\s*([^,\n]+)", body)[1].strip() for n in top_names}

# parent binding in KL_pp_shadow
shadow = (clone / "hdl/milan/KL_pp_shadow.sv").read_text()
inst = re.search(r"protocol_processor_top\s*#\((.*?)\)\s*u_pp", shadow, re.S)[1]
bound = dict(re.findall(r"\.(\w+)\s*\(([^()]*)\)", inst))
unknown = sorted(set(bound) - set(top_names))
print(f"parent binds {len(bound)} parameters; bindings naming no processor parameter: {unknown or 'none'}")
sh_defaults = dict(re.findall(r"parameter\s+[\w\s\[\]:']*?\b(\w+_P)\s*=\s*([^,\n]+)", shadow))
gen = (clone / "hdl/common/gen/adp_shape_defaults.svh").read_text()
genv = dict(re.findall(r"localparam\s+[\w\s\[\]:]*?\b(\w+_C)\s*=\s*([^;]+);", gen))

print(f"{'parameter':22} {'parent binding':24} {'processor default':34}")
for n in top_names:
    b = bound.get(n)
    print(f"{n:22} {('.'+n+'('+b+')') if b else 'unbound (default)':24} {defaults[n]:34}")

# The inventory's stated contracts for the unbound shape parameters:
# N_AUDIO_UNIT_P / N_CLK_DOMAIN_P / N_CONTROL_P "match the entity model".
print("generated model (hdl/common/gen/adp_shape_defaults.svh):",
      {k: genv.get(k) for k in ("AEM_N_AUDIO_UNIT_C", "AEM_N_CLKDOM_C", "ADP_SRP_DOM_DEF_VID_C", "AEM_NAME_ENTRIES_C")})
builder = (clone / "sw/builder/endstation_builder.py").read_text()
m = re.search(r'"AUDIO_UNIT":\s*(\d+).*?"CLOCK_DOMAIN":\s*(\d+),\s*"CONTROL":\s*(\d+)', builder, re.S)
print(f"builder descriptor_counts literal: AUDIO_UNIT={m[1]} CLOCK_DOMAIN={m[2]} CONTROL={m[3]}")
ok = (not unknown and m[1] == defaults["N_AUDIO_UNIT_P"] == "1"
      and m[2] == defaults["N_CLK_DOMAIN_P"] == "1" and m[3] == defaults["N_CONTROL_P"] == "1"
      and genv.get("ADP_SRP_DOM_DEF_VID_C", "").strip() == "16'd2")
print(f"AGREEMENT {'OK' if ok else 'MISMATCH'}")

# Fault probes of the new checker on the disposable export.
def run():
    return subprocess.run([sys.executable, "-B", "scripts/check-integrator-params.py"],
                          cwd=export, capture_output=True, text=True)
g, s = export / "docs/guides/integrator.md", export / "hdl/top/protocol_processor_top.sv"
keep_g, keep_s = g.read_text(), s.read_text()
r = run(); print(f"probe clean: rc={r.returncode} {r.stdout.strip().splitlines()[-1]}")
g.write_text(re.sub(r"^\| `LOCK_TIMEOUT_MS_P`.*\n", "", keep_g, flags=re.M))
r = run(); print(f"probe guide row dropped: rc={r.returncode} {' / '.join(r.stdout.strip().splitlines())}")
g.write_text(keep_g)
s.write_text(keep_s.replace("parameter int unsigned N_CONTROL_P         = 1,",
                            "parameter int unsigned N_CONTROL_P         = 1,\n    parameter int unsigned PROBE_EXTRA_P = 0,", 1))
r = run(); print(f"probe extra top parameter: rc={r.returncode} {' / '.join(r.stdout.strip().splitlines())}")
s.write_text(keep_s)
r = run(); print(f"probe restored: rc={r.returncode} {r.stdout.strip().splitlines()[-1]}")
sys.exit(0 if ok else 1)
