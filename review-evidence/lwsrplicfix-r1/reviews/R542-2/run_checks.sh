#!/usr/bin/env bash
# Launch every documented lwSRP check at the reviewed head concurrently.
# Each job writes receipts/head/<name>.log and receipts/head/<name>.rc.
# Usage: run_checks.sh <checkout> <packet> <cgreen-prefix>
set -u
SRC=${1:?checkout}
PKT=${2:?packet}
CG=${3:?cgreen prefix}
OUT="$PKT/receipts/head"
SCR="$PKT/scratch/run"
mkdir -p "$OUT"
rm -rf "$SCR"
mkdir -p "$SCR"
export CMAKE_PREFIX_PATH="$CG" LD_LIBRARY_PATH="$CG/lib" CPATH="$CG/include" LIBRARY_PATH="$CG/lib"

job() {
    local name=$1
    shift
    rm -f "$OUT/$name.rc"
    setsid nohup bash -c "cd '$SRC' && ( $* ) >'$OUT/$name.log' 2>&1; echo \$? > '$OUT/$name.rc'" < /dev/null > /dev/null 2>&1 &
}

profile() {
    local p=$1 b="$SCR/build-$1"
    echo "set -o pipefail;" \
        "echo '## configure'; cmake -S . -B '$b' -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$p; c=\$?; echo \"configure rc=\$c\";" \
        "echo '## build'; cmake --build '$b' --parallel 2; d=\$?; echo \"build rc=\$d\";" \
        "echo '## ctest'; ctest --test-dir '$b' --output-on-failure -V; e=\$?; echo \"ctest rc=\$e\";" \
        "echo '## unit'; '$b/unit_tests'; f=\$?; echo \"unit rc=\$f\";" \
        "echo '## behave'; SHLAN_LIBRARY='$b/libshlan.so' behave; g=\$?; echo \"behave rc=\$g\";" \
        "echo '## behave-dry'; behave --dry-run; h=\$?; echo \"behave-dry rc=\$h\";" \
        "exit \$(( c | d | e | f | g | h ))"
}

job check-sentences python3 doc/tools/check_sentences.py
job check-references python3 doc/tools/check_references.py
job check-references-selftest python3 doc/tools/check_references.py --self-test
job check-links-anon python3 doc/tools/check_links.py
job render-mermaid python3 doc/tools/render_mermaid.py --output "$SCR/graphs"
job profile-off "$(profile OFF)"
job profile-on "$(profile ON)"
job check-freestanding python3 tests/check_freestanding.py
job check-freestanding-milan "CC='cc -DLWSRP_MILAN=1' python3 tests/check_freestanding.py"
job check-embedded python3 tests/check_embedded.py --work-dir "$SCR/embedded"
job check-reversals-off python3 tests/check_reversals.py --work-dir "$SCR/rev-off" --prefix "$CG"
job check-reversals-on python3 tests/check_reversals.py --work-dir "$SCR/rev-on" --prefix "$CG" --milan ON
echo launched
