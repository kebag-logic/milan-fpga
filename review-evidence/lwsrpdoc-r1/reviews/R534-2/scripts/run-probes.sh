#!/usr/bin/env bash
# Disposable probes on exported snapshots of HEAD (never the checkout).
# Usage: run-probes.sh CHECKOUT SCRATCH OUTDIR DEPS_PREFIX
set -u
repo=$1; scratch=$2; out=$3; deps=$4; mkdir -p "$out"
fresh() { rm -rf "$1"; mkdir -p "$1"; git -C "$repo" archive HEAD | tar -x -C "$1"; }

# P1: planted bare standard names in prose must fail the reference check.
p1() {
  d=$scratch/probe-c11; fresh "$d"; cd "$d"
  {
    python3 doc/tools/check_references.py >/dev/null 2>&1; echo "baseline rc=$?"
    i=0
    for text in 'Use a C11 compiler.' 'Use a `C11` compiler.' '| C language | Requires C11. |' 'Build with C17 or C2x.' 'Follow ISO/IEC 9899:2011.' 'Follow POSIX timers.' 'Use C++17 bindings.' 'Requires IEEE 802.1Q.' 'See clause 10.7.5.20.' 'See Table 8-1.' 'See issue #7.' 'Track #6.' 'Edit Kconfig.zephyr.' 'Call mrp_rx.' 'Use the SPDX comment.'; do
      i=$((i+1)); cp README.md "$scratch/readme.bak"; printf '\n%s\n' "$text" >> README.md
      python3 doc/tools/check_references.py > "$out/p1-plant-$i.log" 2>&1; rc=$?
      cp "$scratch/readme.bak" README.md
      echo "plant $i rc=$rc text=[$text] hits=[$(grep '^FAIL' "$out/p1-plant-$i.log" | tr '\n' ';')]"
    done
    python3 doc/tools/check_references.py >/dev/null 2>&1; echo "restored rc=$?"
    rm -f "$scratch/readme.bak"
  } > "$out/p1-planted-references.txt" 2>&1
}

# P2: weaken the checker; its self-test must fail.
p2() {
  d=$scratch/probe-selftest; fresh "$d"; cd "$d"
  {
    python3 doc/tools/check_references.py --self-test | tail -1; echo "unmodified rc=${PIPESTATUS[0]}"
    sed -i 's/|11|17|18|23|2x|2y)/|17|18|23|2x|2y)/' doc/tools/check_references.py
    grep -c '|11|17' doc/tools/check_references.py | sed 's/^/remaining C11 alternatives: /'
    python3 doc/tools/check_references.py --self-test | grep -E 'C11|self-test:' ; echo "C11-removed self-test rc=${PIPESTATUS[0]}"
    python3 doc/tools/check_references.py | tail -1; echo "C11-removed checker rc=${PIPESTATUS[0]}"
  } > "$out/p2-selftest-mutation.txt" 2>&1
}

# P3: wrong disable binding (disable calls enable) — documented to still pass.
p3() {
  d=$scratch/probe-wrongdisable; fresh "$d"; cd "$d"
  export CPATH="$deps/include" LIBRARY_PATH="$deps/lib" LD_LIBRARY_PATH="$deps/lib" CMAKE_PREFIX_PATH="$deps"
  {
    python3 - <<'PY'
import re, pathlib
p = pathlib.Path("tests/features/switch_bindings.c")
s = p.read_text()
s2 = s.replace("return shlan_port_disable(sw, port_id);", "return shlan_port_enable(sw, port_id);")
assert s2 != s
p.write_text(s2)
PY
    grep -n 'shlan_port_' tests/features/switch_bindings.c
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug >"$out/p3-configure.log" 2>&1; echo "configure rc=$?"
    cmake --build build --parallel 4 >"$out/p3-build.log" 2>&1; echo "build rc=$?"
    behave >"$out/p3-behave.log" 2>&1; echo "behave rc=$?"
    tail -4 "$out/p3-behave.log"
  } > "$out/p3-wrong-disable.txt" 2>&1
}
p1 & p2 & p3 & wait
cat "$out"/p1-planted-references.txt "$out"/p2-selftest-mutation.txt "$out"/p3-wrong-disable.txt
