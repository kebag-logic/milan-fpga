#!/bin/sh
# Usage: chain_py.sh <clone> <make-binary-dir> <scratchdir>
# As chain_ab_echo.sh, but the level-1 make is started from python3 subprocess.run with
# captured output (mutants.py's exact call shape) and the outer make writes to a file
# (run_all_suites.sh's `make -C <suite> > log 2>&1`). Pre-fix copy only (A).
set -u
C=$1; MB=$2; S=$3; export PATH="$MB:$PATH"; mkdir -p "$S"
D=$C/tb/verilator/zz_r559_probe_A; rm -rf "$D"; mkdir -p "$D"
cp "$C/tb/verilator/maap/Makefile" "$D/Makefile"
git -C "$C" show b9b389611:tb/verilator/maap/integration.mk > "$D/integration.mk"
cat > "$S/call.py" <<'PY'
import subprocess, sys
r = subprocess.run(["make", "-j8", "-s", "-C", sys.argv[1], "integration-build",
                    f"DP_MDIR={sys.argv[2]}", "VERILATOR=echo", "VERILATOR_JOBS=0"],
                   capture_output=True, text=True, check=False)
print(r.stdout[-1500:] + r.stderr[-1500:]); print("inner rc", r.returncode)
PY
printf 'chain:\n\tpython3 -I %s %s %s\n' "$S/call.py" "$D" "$S/obj-py" > "$D/outer.mk"
(cd / && env -u MAKEFLAGS -u MAKELEVEL make -C "$D" -f outer.mk chain > "$S/outer.log" 2>&1); echo "make=$(make --version|head -1) outer rc=$?"
grep -E 'non-files|inner rc|--build -j' "$S/outer.log" | cut -c1-200
rm -rf "$D"; git -C "$C" status --porcelain --untracked-files=all | head
