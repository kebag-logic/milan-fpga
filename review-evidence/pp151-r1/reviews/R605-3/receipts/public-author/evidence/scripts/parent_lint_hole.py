"""The parent's own lint_one on KL_pp_shadow, with one -G override that trips a
processor guard: what Verilator says, and what the parent gate makes of it."""
import subprocess, sys
from pathlib import Path
parent = Path(sys.argv[1]); verilator = sys.argv[2]; override = sys.argv[3]
sys.path.insert(0, str(parent / "scripts"))
import lint_rtl
real = subprocess.run
seen = {}
def run(cmd, **kw):
    if cmd and cmd[0] == verilator:
        cmd = cmd[:1] + [override] + cmd[1:]
        r = real(cmd, **kw)
        seen["rc"] = r.returncode
        return r
    return real(cmd, **kw)
lint_rtl.subprocess.run = run
decls = lint_rtl.declarations(); inc = lint_rtl.included(decls); pkgs = lint_rtl.packages(decls)
sources = ([p for p in pkgs if Path(p).name not in inc]
           + [r for r in sorted(decls) if r not in pkgs and Path(r).name not in inc]
           + lint_rtl.submodule_sources())
out, vios, hard = lint_rtl.lint_one("KL_pp_shadow", lint_rtl.include_dirs(), sources, verilator)
user = [l for l in out.splitlines() if "USERFATAL" in l or "USERERROR" in l]
print(f"override {override}: verilator rc {seen.get('rc')}")
for l in user: print("  verilator said:", l)
print(f"  lint_one: {len(vios)} violation(s), {len(hard)} hard error(s): "
      f"{[str(v) for v in vios if 'protocol-processor' in v.path]} {hard}")
