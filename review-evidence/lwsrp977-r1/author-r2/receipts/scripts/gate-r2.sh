#!/bin/bash
# gate.sh <name> <head>: one lwSRP gate in its own clean clone of <head>; prints the commands, their output and rc.
set -u
name=$1; head=$2; tag=${3:-}
S=$VALIDATION_STORAGE/lwsrp22-a861-scratch
REPO=$VALIDATION_STORAGE/lwsrp22-r2
G=$S/gates/$name${tag:+-$tag}
CG=$VALIDATION_STORAGE/977-a825/cgreen/prefix
export CMAKE_PREFIX_PATH=$CG LD_LIBRARY_PATH=$CG/lib CGREEN_PREFIX=$CG
ES="-DLWSRP_ONE_PORT_MAP=1 -DLWSRP_LEAN_VALIDATE=1 -DLWSRP_RAPID_REPLACE=1 -DLWSRP_LEAN_COPY=1 -DLWSRP_LEAN_TX=1"
SC="-DLWSRP_TIMER_SLOTS=64u -DLWSRP_ATTR_BUCKETS=16u -DLWSRP_TX_MERGE=1"
mkdir -p "$G"
git clone -q --no-hardlinks "$REPO" "$G/src" && git -C "$G/src" checkout -q "$head" || exit 90
# The link checker derives the repository from an HTTPS origin, as the checkout has.
git -C "$G/src" remote set-url origin https://github.com/kebag-logic/lwSRP.git
cd "$G/src" || exit 91
echo "# gate $name at $(git rev-parse HEAD), clean clone; $(date '+%F %H:%M:%S %Z')"
step() { echo "\$ $*"; "$@"; local rc=$?; echo "[rc=$rc] $*"; return $rc; }
rc=0
case $name in
  suites-OFF|suites-ON)
    m=${name#suites-}; B=$G/build
    step cmake -S . -B "$B" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$m > "$G/configure.log" 2>&1 || rc=1
    step cmake --build "$B" --parallel 2 > "$G/build.log" 2>&1 || rc=1
    step ctest --test-dir "$B" --output-on-failure || rc=1
    step "$B/unit_tests" > "$G/unit.log" 2>&1 || rc=1; tail -n 14 "$G/unit.log"
    step env SHLAN_LIBRARY="$B/libshlan.so" python3 -m behave || rc=1
    step python3 -m behave --dry-run || rc=1 ;;
  units)
    step "$S/bin/units.sh" "$G/src" "$G/work" || rc=1 ;;
  codec)
    mkdir -p "$G/b"
    step cc -std=c11 -Isrc/include -I"$CG/include" -L"$CG/lib" tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o "$G/b/mrp_pdu_tests" <<'C' || rc=1
#include <cgreen/cgreen.h>
TestSuite *mrp_pdu_suite(void);
int main(void)
{
    return run_test_suite(mrp_pdu_suite(), create_text_reporter());
}
C
    step "$G/b/mrp_pdu_tests" || rc=1 ;;
  eq-OFF|eq-ON)
    step python3 tests/check_equivalence.py --work-dir "$G/work" --prefix "$CG" --milan ${name#eq-} || rc=1 ;;
  eqc-OFF|eqc-ON)
    step python3 tests/check_equivalence_controls.py --work-dir "$G/work" --prefix "$CG" --milan ${name#eqc-} || rc=1 ;;
  diff-OFF|diff-ON)
    step python3 tests/check_differential.py --work-dir "$G/work" --milan ${name#diff-} --sanitize-memory clang || rc=1 ;;
  rev-OFF|rev-ON)
    step python3 tests/check_reversals.py --work-dir "$G/work" --prefix "$CG" --milan ${name#rev-} || rc=1 ;;
  rev-key-OFF|rev-key-ON)
    step python3 tests/check_reversals.py --work-dir "$G/work" --prefix "$CG" --milan ${name#rev-key-} --scale ON || rc=1 ;;
  rev-es-OFF|rev-es-ON)
    step python3 tests/check_reversals.py --work-dir "$G/work" --prefix "$CG" --milan ${name#rev-es-} --scale ON --end-station ON || rc=1 ;;
  rev-es-noscale-OFF|rev-es-noscale-ON)
    step python3 tests/check_reversals.py --work-dir "$G/work" --prefix "$CG" --milan ${name#rev-es-noscale-} --end-station ON || rc=1 ;;
  baremetal)
    step python3 tests/check_embedded.py --work-dir "$G/work" || rc=1
    step python3 tests/check_freestanding.py || rc=1
    step env CC="cc -DLWSRP_MILAN=1" python3 tests/check_freestanding.py || rc=1
    step env CC="cc $SC" python3 tests/check_freestanding.py || rc=1
    step env CC="cc $ES" python3 tests/check_freestanding.py || rc=1
    step env CC="cc -DLWSRP_MILAN=1 $SC $ES" python3 tests/check_freestanding.py || rc=1 ;;
  docs)
    step python3 doc/tools/check_sentences.py || rc=1
    step python3 doc/tools/check_references.py || rc=1
    step python3 doc/tools/check_references.py --self-test || rc=1
    step python3 doc/tools/check_links.py --github-auth || rc=1
    step python3 doc/tools/render_mermaid.py --output "$G/graphs" || rc=1 ;;
  objects)
    step "$S/bin/objects_identical.sh" "$G/src" d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b HEAD "$G/work" || rc=1 ;;
  inventory)
    step git ls-files '*.pyc' '*__pycache__*'
    n=$(git ls-files '*.pyc' '*__pycache__*' | wc -l); echo "python caches tracked: $n"; [ "$n" -eq 0 ] || rc=1
    echo "tracked files: $(git ls-files | wc -l)"
    git ls-files -z | xargs -0 file --mime-encoding | grep -v -E ':[[:space:]]+(us-ascii|utf-8)$' && rc=1
    echo "tracked files by encoding: $(git ls-files -z | xargs -0 file -b --mime-encoding | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
    echo "non-text tracked files: $(git ls-files -z | xargs -0 file --mime-encoding | grep -c -v -E ':[[:space:]]+(us-ascii|utf-8)$')"
    git ls-files | grep -E '\.(o|a|so|pyc|pyo|log|bin|elf|exe|gcda|gcno|tar|gz|zip)$|(^|/)(build|__pycache__|CMakeFiles)/' && rc=1
    echo "generated-output paths tracked: $(git ls-files | grep -c -E '\.(o|a|so|pyc|pyo|log|bin|elf|exe|gcda|gcno|tar|gz|zip)$|(^|/)(build|__pycache__|CMakeFiles)/')"
    step cat .gitignore ;;
  *) echo "unknown gate $name"; rc=2 ;;
esac
echo "# gate $name rc=$rc $(date '+%F %H:%M:%S %Z')"
exit $rc
