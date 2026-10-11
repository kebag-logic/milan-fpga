#!/usr/bin/env python3
"""Reviewer's focused parent check: does any shipping shape trip a processor guard?

Run from a scratch parent whose protocol-processor/ holds the processor head. For each
shipping config, milan_datapath is linted the way the parent's lint_rtl.lint_one builds
its Verilator command (same flags, include dirs with the config's generated shape
header first, -y axis library, the same source list), plus -GN_STREAMS and the 50 MHz
clock. Every raw USER* diagnostic is printed, whatever its path, because lint_rtl's own
verdict drops processor-path findings. A positive control lints KL_pp_shadow at
-GN_STREAM_IN_P=40, which must show a processor USERFATAL (the detector sees one).
usage: parent_shapes.py <parent> <verilator>
"""
import subprocess
import sys
from pathlib import Path

parent = Path(sys.argv[1]).resolve()
verilator = sys.argv[2]
sys.path.insert(0, str(parent / "scripts"))
import lint_rtl  # noqa: E402  (the parent's own module, read for its lists only)

decls = lint_rtl.declarations()
inc = lint_rtl.included(decls)
pkgs = lint_rtl.packages(decls)
sources = ([p for p in pkgs if Path(p).name not in inc]
           + [r for r in sorted(decls) if r not in pkgs and Path(r).name not in inc]
           + lint_rtl.submodule_sources())
base_dirs = lint_rtl.include_dirs()


def lint(top, dirs, extra):
    cmd = [verilator, "--lint-only", "--sv", "--top-module", top, *extra]
    cmd += ["-Wwarn-" + w for w in lint_rtl.EXTRA_WARNINGS]
    cmd += ["-I" + d for d in dirs]
    axis = lint_rtl.axis_lib()
    if axis:
        cmd += ["-y", axis]
    cmd += sources
    p = subprocess.run(cmd, cwd=parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, check=False)
    user = [l for l in p.stdout.splitlines() if l.startswith("%") and "-USER" in l]
    errors = [l for l in p.stdout.splitlines()
              if l.startswith("%Error") and not l.startswith("%Error: Exiting due to")]
    return p.returncode, user, errors


CONFIGS = (("endstation_arty_current", 1), ("endstation_arty_4x4", 4),
           ("endstation_arty_8ch", 4), ("endstation_ax7101_1x1_tdm8", 1),
           ("endstation_ax7101_8x8", 8))
bad = 0
for cfg, ns in CONFIGS:
    dirs = [f"configs/generated/{cfg}"] + base_dirs[1:]
    rc, user, errors = lint("milan_datapath", dirs,
                            [f"-GN_STREAMS={ns}", "-GMILAN_CLK_FREQ_HZ=50000000"])
    pp = [l for l in user if "protocol-processor/" in l]
    bad += bool(pp) or bool(errors)
    print(f"{cfg} N_STREAMS={ns}: verilator rc {rc}, {len(user)} USER, "
          f"{len(pp)} from protocol-processor/, {len(errors)} %Error")
    for l in user + errors:
        print("   ", l)
rc, user, errors = lint("KL_pp_shadow", base_dirs, ["-GN_STREAM_IN_P=40"])
pp = [l for l in user if "protocol-processor/" in l and "USERFATAL" in l]
print(f"control KL_pp_shadow -GN_STREAM_IN_P=40: verilator rc {rc}, "
      f"{len(pp)} processor USERFATAL ({'seen' if pp and rc != 0 else 'NOT SEEN'})")
for l in user:
    print("   ", l)
bad += not (pp and rc != 0)
print(f"parent shapes: {'PASS' if bad == 0 else 'FAIL'}")
sys.exit(int(bad != 0))
