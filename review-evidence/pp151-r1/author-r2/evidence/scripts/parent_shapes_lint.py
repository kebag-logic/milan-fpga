"""The parent's own lint_one on milan_datapath at each shipping config: the config's
generated shape header first on the include path (lint_rtl.include_dirs names one),
N_STREAMS and the 50 MHz clock of its board options. Prints Verilator's status and
every raw USER* diagnostic, whatever its path: lint_rtl drops processor-path findings."""
import subprocess, sys
from pathlib import Path
parent = Path(sys.argv[1]); verilator = sys.argv[2]
sys.path.insert(0, str(parent / "scripts"))
import lint_rtl
CONFIGS = (("endstation_arty_current", 1), ("endstation_arty_4x4", 4), ("endstation_arty_8ch", 4),
           ("endstation_ax7101_1x1_tdm8", 1), ("endstation_ax7101_8x8", 8))
real = subprocess.run
state = {}
def run(cmd, **kw):
    if cmd and cmd[0] == verilator:
        cmd = cmd[:1] + state["extra"] + cmd[1:]
        r = real(cmd, **kw); state["rc"] = r.returncode; return r
    return real(cmd, **kw)
lint_rtl.subprocess.run = run
decls = lint_rtl.declarations(); inc = lint_rtl.included(decls); pkgs = lint_rtl.packages(decls)
sources = ([p for p in pkgs if Path(p).name not in inc]
           + [r for r in sorted(decls) if r not in pkgs and Path(r).name not in inc]
           + lint_rtl.submodule_sources())
base_dirs = lint_rtl.include_dirs()
bad = 0
for cfg, ns in CONFIGS:
    dirs = [f"configs/generated/{cfg}"] + base_dirs[1:]
    state["extra"] = [f"-GN_STREAMS={ns}", "-GMILAN_CLK_FREQ_HZ=50000000"]
    out, vios, hard = lint_rtl.lint_one("milan_datapath", dirs, sources, verilator)
    user = [l for l in out.splitlines() if l.startswith("%") and "-USER" in l]
    pp = [l for l in user if "protocol-processor/" in l]
    bad += bool(pp)
    print(f"{cfg} N_STREAMS={ns}: verilator rc {state['rc']}, {len(user)} USER diagnostic(s), "
          f"{len(pp)} from protocol-processor/, lint_one {len(vios)} violation(s) {len(hard)} hard")
    for l in user: print("   ", l)
sys.exit(int(bad != 0))
