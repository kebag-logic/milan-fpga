#!/bin/sh
# Usage: chain_ab.sh <clone> <make-binary-dir> <scratchdir>
# The hosted chain, real run with VERILATOR=echo (prints the elaboration line, builds nothing): run_all_suites `make -C <suite>`
# (level 0, no -s, no inherited MAKEFLAGS) -> recipe runs plain `make -j8 -s -C <suite>
# integration-build` as mutants.py does (level 1) -> $(MAKE) -f integration.mk (level 2)
# -> $(shell ...) capture. Two untracked sibling copies of the suite directory are used:
# A = integration.mk from b9b38961 (pre-fix), B = integration.mk at the clone's HEAD.
# The copies are removed at the end; nothing tracked is touched.
set -u
C=$1; MB=$2; S=$3; export PATH="$MB:$PATH"; mkdir -p "$S"
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1)"
for v in A B; do
  D=$C/tb/verilator/zz_r559_probe_$v; rm -rf "$D"; mkdir -p "$D"
  cp "$C/tb/verilator/maap/Makefile" "$D/Makefile"
  if [ $v = A ]; then git -C "$C" show b9b389611:tb/verilator/maap/integration.mk > "$D/integration.mk"
  else cp "$C/tb/verilator/maap/integration.mk" "$D/integration.mk"; fi
  printf 'chain:\n\tmake -j8 -s -C %s integration-build DP_MDIR=%s/obj-%s VERILATOR=echo\n' "$D" "$S" "$v" > "$D/outer.mk"
  out=$(cd / && env -u MAKEFLAGS -u MAKELEVEL make -C "$D" -f outer.mk chain 2>&1); rc=$?
  echo "== $v rc=$rc"
  printf '%s\n' "$out" | grep -E 'non-files|empty|Error|--build -j' | sed 's/^\(.\{0,160\}\).*$/\1/' | sed 's/^\(verilator .\{0,40\}\).*/\1 .../'
  rm -rf "$D"
done
git -C "$C" status --porcelain --untracked-files=all | head
