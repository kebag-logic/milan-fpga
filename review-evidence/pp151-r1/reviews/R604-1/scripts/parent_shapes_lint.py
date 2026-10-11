#!/usr/bin/env python3
"""Lint the parent's milan_datapath at each shipping config, reading Verilator's
raw output for any processor guard (USER* diagnostic) as well as its exit status.

Sources, include roots and flags are the parent's own lint_rtl.py sweep's, with the
config's generated shape directory first and -GN_STREAMS = the wider stream direction
(check_sweep_shape.config_shape), -GMILAN_CLK_FREQ_HZ=50000000.
Usage: parent_shapes_lint.py <parent-tree>   (verilator on PATH)
"""
import re, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "scripts"))
import lint_rtl  # noqa: E402

decls = lint_rtl.declarations()
inc = lint_rtl.included(decls)
pkgs = lint_rtl.packages(decls)
sources = ([p for p in pkgs if Path(p).name not in inc]
           + [r for r in sorted(decls) if r not in pkgs and Path(r).name not in inc]
           + lint_rtl.submodule_sources())
base_inc = lint_rtl.include_dirs()[1:]
worst = 0
for cfg in sorted((ROOT / "configs").glob("endstation_*.yaml")):
    name = cfg.stem
    s = (yaml.safe_load(cfg.read_text()).get("streams") or {})
    n = max(len(s.get("listeners") or []), len(s.get("talkers") or []))
    cmd = ["verilator", "--lint-only", "--sv", "--top-module", "milan_datapath",
           f"-GN_STREAMS={n}", "-GMILAN_CLK_FREQ_HZ=50000000"]
    cmd += ["-Wwarn-" + w for w in lint_rtl.EXTRA_WARNINGS]
    cmd += ["-I" + d for d in [f"configs/generated/{name}"] + base_inc]
    axis = lint_rtl.axis_lib()
    if axis:
        cmd += ["-y", axis]
    cmd += sources
    p = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    users = [l for l in p.stdout.splitlines() if re.match(r"^%(Warning|Error)-USER", l)]
    errors = [l for l in p.stdout.splitlines() if l.startswith("%Error")]
    pp = [l for l in users if "protocol-processor/" in l]
    print(f"{name} N_STREAMS={n}: verilator rc {p.returncode}, {len(users)} USER diagnostic(s), "
          f"{len(pp)} from protocol-processor/, {len(errors)} %Error line(s)")
    for l in users + errors[:5]:
        print("   ", l[:220])
    worst = max(worst, len(users) + len(errors))
sys.exit(1 if worst else 0)
