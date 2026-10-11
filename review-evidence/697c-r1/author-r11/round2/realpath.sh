#!/usr/bin/env bash
# Scratch: real-path probes of the stack pin and boundary in a disposable clone of the lane at HEAD.
# The clone's own tsn-c-stack checkout is edited (never the lane's); a plant the boundary must judge is
# committed locally inside the clone's submodule and its gitlink staged in the clone's index, so the pin
# check passes and the real path runs. usage: realpath.sh <lane> <work>
set -u
lane=$1; work=$2
export TMPDIR=$work/tmp MILAN_RV32_CC=<pinned SDK>/bin/riscv32-linux-gcc
export VERILATOR=false
rm -rf "$work"; mkdir -p "$work/tmp"
git clone -q --no-hardlinks "$lane" "$work/repo"
R=$work/repo; S=$R/third_party/tsn-c-stack
git -C "$R" checkout -q "$(git -C "$lane" rev-parse HEAD)"
git -C "$R" config submodule.third_party/tsn-c-stack.url "$lane/third_party/tsn-c-stack"
for sub in third_party/lwSRP protocol-processor gptp-processor; do
  git -C "$R" config "submodule.$sub.url" "$lane/$sub"
done
git -C "$R" -c protocol.file.allow=always submodule update -q --init third_party/tsn-c-stack third_party/lwSRP \
  protocol-processor gptp-processor
PIN=$(git -C "$R" rev-parse :third_party/tsn-c-stack)
echo "clone at $(git -C "$R" rev-parse HEAD), tsn-c-stack gitlink $PIN"
[ "$(git -C "$S" rev-parse --show-toplevel)" = "$S" ] || { echo "submodule top-level mismatch"; exit 2; }
restore() {
  git -C "$S" update-index --no-assume-unchanged src/adp.c 2>/dev/null
  git -C "$S" checkout -q -f --detach "$PIN"; git -C "$S" clean -qfdx
  git -C "$R" update-index --cacheinfo "160000,$PIN,third_party/tsn-c-stack"
  git -C "$R" checkout -q -- sw/firmware
}
gate() {  # label, command...
  local label=$1; shift
  (cd "$R" && "$@") > "$work/out.log" 2>&1; local rc=$?
  echo "  rc=$rc $label: $(grep -E 'REFUSED|\[FAIL\]|ctrl_boundary: (PASS|FAIL)|^tsn-c-stack at' "$work/out.log" | tr '\n' ' ' | cut -c1-330)"
}
echo "=== probe 1: src/maap.c edited in the clone's submodule"
printf '\n/* local */\n' >> "$S/src/maap.c"; git -C "$S" status --short
gate "make -C tb/verilator/mbx run-cosim" make --no-print-directory -C tb/verilator/mbx run-cosim
gate "maap_differential.py" python3 -B sw/firmware/ctrl/test/maap_differential.py
gate "maap_differential.py --self-test" python3 -B sw/firmware/ctrl/test/maap_differential.py --self-test
gate "test_ctrl_firmware.py (control)" python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
restore
echo "=== probe 2: src/adp.c edited and hidden with assume-unchanged"
printf '\n/* local */\n' >> "$S/src/adp.c"; git -C "$S" update-index --assume-unchanged src/adp.c
echo "  git status in the submodule: '$(git -C "$S" status --porcelain)'"
gate "ctrl_build.py --stack-pin" python3 -B sw/firmware/ctrl/test/ctrl_build.py --stack-pin
gate "make -C tb/verilator/mbx run-cosim" make --no-print-directory -C tb/verilator/mbx run-cosim
restore
echo "=== probe 3: scripts/check_boundary.py edited"
printf '\n# local\n' >> "$S/scripts/check_boundary.py"
gate "ctrl_boundary.py --require-rv32" python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
restore
plant() {  # name file anchor replacement: committed in the clone's submodule, gitlink staged
  python3 - "$S/$2" "$3" "$4" <<'PY'
import sys; p, a, r = sys.argv[1:4]; a = a.encode().decode("unicode_escape"); r = r.encode().decode("unicode_escape")
t = open(p).read(); assert t.count(a) == 1, (p, a); open(p, "w").write(t.replace(a, r))
PY
  git -C "$S" -c user.name=probe -c user.email=probe@invalid commit -q -am "probe $1"
  git -C "$R" update-index --cacheinfo "160000,$(git -C "$S" rev-parse HEAD),third_party/tsn-c-stack"
}
echo "=== probe 4 (R584-1-S2): a stack test includes the mailbox HAL"
plant "test HAL" tests/test_maap_debug.cpp '#include "maap.h"\n' '#include "maap.h"\n#include "mbx_hal.h"\n'
gate "ctrl_boundary.py --require-rv32" python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
restore
echo "=== probe 5 (R585-1-F1): the stack's CTRL_REENTRY_ASSERT region includes the mailbox HAL"
plant "reentry HAL" src/acmp.c '#ifdef CTRL_REENTRY_ASSERT\n' '#ifdef CTRL_REENTRY_ASSERT\n#include "mbx_hal.h"\n'
gate "ctrl_boundary.py --require-rv32" python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
restore
echo "=== probe 6 (R585-1-F1): the stack's #ifndef NDEBUG region includes the platform's header"
plant "debug header" src/maap.c '#ifndef NDEBUG\n#include <assert.h>\n' '#ifndef NDEBUG\n#include <assert.h>\n#include "ctrl_debug.h"\n'
gate "ctrl_boundary.py --require-rv32" python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
restore
echo "=== probe 7 (R585-1-F1): the adapter reaches the stack's tests/acmp_fake.hpp under CTRL_REENTRY_ASSERT"
python3 - "$R/sw/firmware/ctrl/acmp/acmp_mbx.c" <<'PY'
import sys; p = sys.argv[1]; t = open(p).read(); a = '#include "acmp_mbx.h"\n'
assert t.count(a) == 1
open(p, "w").write(t.replace(a, a + '#ifdef CTRL_REENTRY_ASSERT\n#include "../../../../third_party/tsn-c-stack/tests/acmp_fake.hpp"\n#endif\n'))
PY
gate "ctrl_boundary.py --require-rv32" python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
restore
echo "=== restored"
git -C "$S" status --short; git -C "$R" status --short; git -C "$R" submodule status third_party/tsn-c-stack
