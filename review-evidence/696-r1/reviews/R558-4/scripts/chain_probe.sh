#!/bin/sh
# Usage: chain_probe.sh <clone> <make-binary-dir> <scratchdir>
# The hosted chain with the build stubbed out (VERILATOR=echo, so only parsing,
# the two ROM generators and an echo of the flag line run):
#   make -C <suite> -f top.mk  (auto -w; optionally MAKEFLAGS=w)
#     -> python3 subprocess: make -j8 -s -C <suite> -f <maap Makefile copy> integration-build
#       -> $(MAKE) -f <integration variant> build -> $(shell $(MAKE) ...)
# Variants: head (exact-head integration.mk) and pre (b9b38961's integration.mk).
# Temporary untracked files .r558probe-* are written into the suite directory and removed.
set -u
C=$1; MB=$2; S=$3; M=$C/tb/verilator/maap
export PATH="$MB:$PATH"; mkdir -p "$S"
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1)"
cp "$M/integration.mk" "$M/.r558probe-head.mk"
git -C "$C" show b9b389611:tb/verilator/maap/integration.mk > "$M/.r558probe-pre.mk"
sed 's/-f integration.mk build/-f $(IMK) build/' "$M/Makefile" > "$M/.r558probe-maap.mk"
for v in head pre; do
  printf 'all:\n\tpython3 -c "import subprocess,sys; sys.exit(subprocess.run([\\"make\\",\\"-j8\\",\\"-s\\",\\"-C\\",\\"%s\\",\\"-f\\",\\".r558probe-maap.mk\\",\\"integration-build\\",\\"IMK=.r558probe-%s.mk\\",\\"DP_MDIR=%s/obj-%s\\",\\"VERILATOR=echo\\",\\"VERILATOR_JOBS=5\\"]).returncode)"\n' "$M" "$v" "$S" "$v" > "$S/top-$v.mk"
  for ctx in auto-w MAKEFLAGS=w; do
    if [ $ctx = auto-w ]; then out=$(cd / && env -u MAKEFLAGS make -C "$M" -f "$S/top-$v.mk" 2>&1); rc=$?
    else out=$(cd / && env MAKEFLAGS=w make -C "$M" -f "$S/top-$v.mk" 2>&1); rc=$?; fi
    echo "== $v $ctx rc=$rc"
    printf '%s\n' "$out" | grep -E 'non-files|empty|failed|--build -j [0-9]+|maap_integration' | grep -o -E 'non-files[^.]*|source list is empty|derivation failed|--build -j [0-9]+|[0-9]+ words' | sort | uniq -c
    printf '%s\n' "$out" | grep -E 'maap_integration' | tr ' ' '\n' | grep -c '\.s\?v$' | sed 's/^/  sv-words-on-echoed-line: /'
  done
done
rm -f "$M/.r558probe-head.mk" "$M/.r558probe-pre.mk" "$M/.r558probe-maap.mk"
