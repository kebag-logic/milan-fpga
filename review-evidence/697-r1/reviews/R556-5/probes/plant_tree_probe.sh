#!/bin/sh
# SPDX-License-Identifier: MIT
# Plant the hidden-text forms into a disposable copy of the reviewed tree, then run
# the head's own comment and conditional gates and both target builds.
# Usage: plant_tree_probe.sh SOURCE_CLONE WORK   (TSN_CLANG must name Clang 18)
set -u
SRC=$1; W=$2
rm -rf "$W"; mkdir -p "$W"
git clone -q "$SRC" "$W/tree" && cd "$W/tree" && git checkout -q --detach 60c911b92825a720044e78bed540752c7dd0368e || exit 2
run() { label=$1; shift; "$@" > "$W/$label.log" 2>&1; echo "$label rc=$?"; }
gates() {
  run "$1-comments" python3 -B scripts/check_comments.py
  run "$1-conditionals" python3 -B scripts/check_conditionals.py --work "$W/$1-cond" --jobs 8
  run "$1-gcc" sh -c "cmake -S . -B '$W/$1-gcc' -DCMAKE_BUILD_TYPE=Debug && cmake --build '$W/$1-gcc' -j16 && ctest --test-dir '$W/$1-gcc' -j16"
  run "$1-clang" sh -c "cmake -S . -B '$W/$1-clang' -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Debug && cmake --build '$W/$1-clang' -j16 && ctest --test-dir '$W/$1-clang' -j16"
  run "$1-rv32" python3 -B scripts/baremetal.py --work "$W/$1-rv32" --jobs 4
}
# Row A: form feed before '#' in assembly (F1) and a C++ digit separator in a C header (F2).
python3 - <<'EOF'
from pathlib import Path
s = Path('examples/rv32/start.S'); t = s.read_text()
s.write_text(t.replace('_start:\n', '_start:\n    nop \f#define hidden probe words\n', 1))
w = Path('include/wire.h'); t = w.read_text(); k = '#include <stdint.h>\n'; i = t.index(k) + len(k)
w.write_text(t[:i] + "#define TSN_PROBE_IGNORE(a) 0\nenum { tsn_probe_value = TSN_PROBE_IGNORE(1'2 // hidden probe words '\n) };\n" + t[i:])
EOF
git diff --stat; gates A
git checkout -q -- .
# Row B: a quote in the linker script hides a block comment from the C-mode lexer (F2).
python3 - <<'EOF'
from pathlib import Path
p = Path('examples/rv32/link.ld'); t = p.read_text()
p.write_text(t.replace('ENTRY(_start)\n', "ENTRY(_start)\nPROVIDE(tsn_probe' = 1); /* hidden probe words */ PROVIDE(tsn_probe_end' = 2);\n", 1))
EOF
run B-comments python3 -B scripts/check_comments.py
run B-rv32 python3 -B scripts/baremetal.py --work "$W/B-rv32" --jobs 4
git checkout -q -- .
# Row C: an included file with an unscanned suffix (F3).
printf '// hidden probe words\n' > tests/probe.inc
python3 - <<'EOF'
from pathlib import Path
p = Path('tests/test_port.cpp'); t = p.read_text()
p.write_text(t.replace('#include "adp_port.h"\n', '#include "adp_port.h"\n#include "probe.inc"\n', 1))
EOF
run C-comments python3 -B scripts/check_comments.py
run C-gcc sh -c "cmake -S . -B '$W/C-gcc' -DCMAKE_BUILD_TYPE=Debug && cmake --build '$W/C-gcc' -j16 && ctest --test-dir '$W/C-gcc' -j16"
git checkout -q -- . && rm -f tests/probe.inc
echo "A GAP when every A row is rc=0; B and C GAP when their rows are rc=0."
