#!/usr/bin/env python3
"""Does the parent's lint gate see a processor guard? Lint KL_pp_shadow through the
parent's own lint_one() with -GN_STREAM_IN_P=40 (a shape the top's owner-tag guard
refuses) and compare Verilator's raw verdict with lint_one's parsed one.
Usage: parent_lint_hole.py <parent-tree>   (verilator on PATH)"""
import re, sys
from pathlib import Path
ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "scripts"))
import lint_rtl  # noqa: E402
decls = lint_rtl.declarations(); inc = lint_rtl.included(decls); pkgs = lint_rtl.packages(decls)
sources = ([p for p in pkgs if Path(p).name not in inc]
           + [r for r in sorted(decls) if r not in pkgs and Path(r).name not in inc]
           + lint_rtl.submodule_sources())
for extra in ([], ["-GN_STREAM_IN_P=40"]):
    raw, vios, hard = lint_rtl.lint_one("KL_pp_shadow", lint_rtl.include_dirs(), extra + sources, "verilator")
    users = [l for l in raw.splitlines() if re.match(r"^%(Warning|Error)-USER", l)]
    print(f"KL_pp_shadow {' '.join(extra) or 'defaults'}: {len(users)} USER diagnostic(s) in Verilator's output; "
          f"lint_one: {len(vios)} violation(s), {len(hard)} hard error(s)")
    for l in users:
        print("   verilator said:", l[:200])
    pp_v = [v for v in vios if v.path.startswith("protocol-processor/")]
    print(f"   violations lint_one kept from protocol-processor/: {len(pp_v)}")
