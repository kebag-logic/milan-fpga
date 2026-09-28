#!/usr/bin/env bash
# F1 derivation controls on a disposable copy of the exact head (never the
# review clone). Usage: derivation_probes.sh <disposable-head-tree>
# Each arm edits the copy, runs the named command(s), records rc and the
# decisive output line, then restores the copy (git checkout / reset).
set -u
T=$(cd "${1:?disposable head tree}" && pwd)
TD=sw/builder/test_declarations.py
PKG=adp/pp_adp_pkg.sv
cd "$T" || exit 2
echo "tree $T HEAD $(git rev-parse HEAD 2>/dev/null)"
[ "$(git rev-parse HEAD 2>/dev/null)" = 11e4e1f2876c99e8f136d869c70674e077ddcf94 ] || { echo "not the exact head"; exit 2; }

# Exact test code under test: the lines from the derivation comment to the caps
# parse, executed verbatim so the probes measure the shipped expression.
derive() {
  python3 - "$T" <<'EOF'
import re, sys
from pathlib import Path
ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "scripts"))
from pp_srcs import pp_sources
text = (ROOT / "sw/builder/test_declarations.py").read_text().splitlines()
a = next(i for i, l in enumerate(text) if "Find the authority by its package declaration" in l)
b = next(i for i, l in enumerate(text) if "caps = int(matches[0], 16)" in l)
body = "\n".join(l[4:] for l in text[a:b + 1])
ns = {"ROOT": ROOT, "pp_sources": pp_sources, "re": re}
try:
    exec(body, ns)
    print(f"derivation OK caps=0x{ns['caps']:08X} from {len(ns['sources'])} derived sources")
except AssertionError as e:
    print(f"derivation ASSERT: {e!s}"); sys.exit(1)
EOF
}
run() { # label, command...
  local label=$1; shift
  out=$("$@" 2>&1); rc=$?
  echo "[$label] rc=$rc :: $(printf '%s\n' "$out" | grep -v '^  prose' | grep -E 'names submodule|ASSERT|Assertion|Error|derivation|pp source list|gate 40\] 26' | head -3 | cut -c1-260 | tr '\n' ' ')"
}
restore() {
  git checkout -q -- "$TD"
  git -C protocol-processor reset -q --hard HEAD && git -C protocol-processor clean -qfd
  test -z "$(git status --porcelain)" && test -z "$(git -C protocol-processor status --porcelain)" && echo "  restored clean"
}

echo "== C0 unmodified control"
run C0-pp_srcs python3 scripts/pp_srcs.py --check --selftest
run C0-suite python3 $TD
run C0-derive derive

echo "== C1 removed-derivation control: literal path restored (round-1 spelling)"
python3 - "$TD" <<'EOF'
import sys
p = sys.argv[1]; s = open(p).read()
new = ('    # The descriptor\'s authority supplies the only legal capabilities value.\n'
       '    source = (ROOT / "protocol-processor/hdl/adp/pp_adp_pkg.sv").read_text()\n'
       '    matches = re.findall(r"ADP_ENTITY_CAPS_C\\s*=\\s*32\'h([0-9A-Fa-f_]+)", source)\n')
a = s.index("    # Find the authority by its package declaration")
b = s.index("    assert len(matches) == 1\n    caps")
s = s[:a] + new + s[b:]
open(p, "w").write(s)
EOF
git diff --stat -- "$TD" | tail -1
run C1-pp_srcs python3 scripts/pp_srcs.py --check
run C1-suite python3 $TD
restore
run C1-restored-pp_srcs python3 scripts/pp_srcs.py --check --selftest
run C1-restored-suite python3 $TD

echo "== C2 package moved inside the submodule (tracked): derivation follows it"
git -C protocol-processor/hdl mv $PKG common/pp_adp_pkg_moved.sv
run C2-derive derive
run C2-pp_srcs python3 scripts/pp_srcs.py --check
restore

echo "== C3 second tracked file declaring package pp_adp_pkg: uniqueness assert"
printf 'package pp_adp_pkg;\n  localparam logic [31:0] ADP_ENTITY_CAPS_C = 32%s0000_0001;\nendpackage\n' "'h" > protocol-processor/hdl/common/zz_dup_pkg.sv
git -C protocol-processor add hdl/common/zz_dup_pkg.sv
run C3-derive derive
run C3-suite python3 $TD
restore

echo "== C4 package untracked (git rm --cached; file stays on disk): tracked-only derivation"
git -C protocol-processor rm -q --cached hdl/$PKG
run C4-derive derive
restore

echo "== C5 package declaration renamed: nothing declares pp_adp_pkg"
sed -i 's/^package pp_adp_pkg;/package pp_adp_pkg_x;/' protocol-processor/hdl/$PKG
run C5-derive derive
restore

echo "== C6 constant removed from the package: single-match assert"
sed -i 's/ADP_ENTITY_CAPS_C = /ADP_ENTITY_CAPZ_C = /' protocol-processor/hdl/$PKG
run C6-derive derive
restore

echo "== C7 independent read bites: test caps perturbed by one bit"
sed -i 's/^    caps = int(matches\[0\], 16)$/    caps = int(matches[0], 16) ^ 1/' "$TD"
git diff --stat -- "$TD" | tail -1
run C7-suite python3 $TD
restore

echo "== final"
git status --porcelain | wc -l
git -C protocol-processor status --porcelain | wc -l
git rev-parse HEAD
