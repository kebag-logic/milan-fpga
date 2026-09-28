#!/usr/bin/env bash
# Reproduce the hosted `elaborate` failure locally: the repository's pinned CI LiteX install
# (sw/litex/litex_pins.txt) carries no pythondata-software-picolibc. Shadow that module with one
# whose import raises ImportError (exactly what LiteX's get_data_mod sees when it is absent),
# then run the committed #607 bank entry (test_clock_constraints.py) on a copy of the head.
# Usage: no_picolibc_probe.sh <clean-clone> <scratch-dir> <litex-python>
set -uo pipefail
SRC=$1; WORK=$2; PY=$3
D=$WORK/no-picolibc; SHIM=$WORK/no-picolibc-shim
rm -rf "$D" "$SHIM"; mkdir -p "$D" "$SHIM/pythondata_software_picolibc" "$WORK/tmp"
printf 'raise ImportError("shadowed for probe: not installed by sw/litex/litex_pins.txt")\n' \
  > "$SHIM/pythondata_software_picolibc/__init__.py"
(cd "$SRC" && tar --exclude=sw/builder/out -cf - .) | (cd "$D" && tar -xf -)
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
export PATH="$(dirname "$PY"):/usr/bin:/bin" TMPDIR=$WORK/tmp
echo "shim active: $(PYTHONPATH=$SHIM "$PY" -c 'import pythondata_software_picolibc' 2>&1 | tail -1)"
echo "migen/litex/litex_boards still importable: $(cd "$D/sw/litex" && PYTHONPATH=$SHIM "$PY" -c 'import migen, litex, litex_boards; print("yes")' 2>&1 | tail -1)"
(cd "$D" && PYTHONPATH=$SHIM "$PY" -B sw/builder/test_clock_constraints.py > "$WORK/no-picolibc-test.log" 2>&1)
echo "test_clock_constraints.py without picolibc: rc=$?"
grep -E "^ImportError|^AssertionError|implementation-log diagnostics.*PASS|shipping .* PASS" "$WORK/no-picolibc-test.log" | cut -c1-140
(cd "$D" && "$PY" -B sw/builder/test_clock_constraints.py > "$WORK/with-picolibc-test.log" 2>&1)
echo "same copy with picolibc importable: rc=$?"
rm -rf "$D" "$SHIM"
