#!/usr/bin/env bash
# Scratch: real-path probes of the stack pin and boundary over what F5 added, in a disposable clone of the
# lane at HEAD. The clone's own tsn-c-stack checkout and tree are edited (never the lane's); a plant the
# boundary must judge is committed locally inside the clone's submodule and its gitlink staged in the clone's
# index, so the pin check passes and the real path runs. usage: realpath2b.sh <lane> <work>
set -u
lane=$1; work=$2
export TMPDIR=$work/tmp MILAN_RV32_CC=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
export VERILATOR=false
runtime=$VALIDATION_STORAGE/697c-a583/runtime-freestanding
rm -rf "$work"; mkdir -p "$work/tmp"
git clone -q --no-hardlinks "$lane" "$work/repo"
R=$work/repo; S=$R/third_party/tsn-c-stack
git -C "$R" checkout -q "$(git -C "$lane" rev-parse HEAD)"
for sub in third_party/tsn-c-stack third_party/lwSRP protocol-processor gptp-processor; do
  git -C "$R" config "submodule.$sub.url" "$lane/$sub"
done
git -C "$R" -c protocol.file.allow=always submodule update -q --init third_party/tsn-c-stack third_party/lwSRP \
  protocol-processor gptp-processor
PIN=$(git -C "$R" rev-parse :third_party/tsn-c-stack)
echo "clone at $(git -C "$R" rev-parse HEAD), tsn-c-stack gitlink $PIN"
[ "$(git -C "$S" rev-parse --show-toplevel)" = "$S" ] || { echo "submodule top-level mismatch"; exit 2; }
restore() {
  git -C "$S" checkout -q -f --detach "$PIN"; git -C "$S" clean -qfdx
  git -C "$R" update-index --cacheinfo "160000,$PIN,third_party/tsn-c-stack"
  git -C "$R" checkout -q -- sw/firmware
}
gate() {  # label, command...
  local label=$1; shift
  (cd "$R" && "$@") > "$work/out.log" 2>&1; local rc=$?
  echo "  rc=$rc $label: $(grep -E 'REFUSED|\[FAIL\]|ctrl_boundary: (PASS|FAIL)|^tsn-c-stack at' "$work/out.log" | tr '\n' ' ' | cut -c1-360)"
}
echo "=== probe 1: src/acmp.c edited in the clone's submodule"
printf '\n/* local */\n' >> "$S/src/acmp.c"; git -C "$S" status --short
gate "aecp_arms.py --app" python3 -B sw/firmware/ctrl/test/aecp_arms.py --output "$work/o1" --app
gate "aecp_mutants.py --shard 0 1000" python3 -B sw/firmware/ctrl/test/aecp_mutants.py --output "$work/o2" --shard 0 1000
gate "aecp_wire.py" python3 -B sw/firmware/ctrl/test/aecp_wire.py --reference protocol-processor --output "$work/o3" \
  --verilator false
gate "ctrl_srp_image.py --with-aecp" python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py \
  --config configs/endstation_ax7101_1x1_tdm8.yaml --output "$work/o4" --with-aecp --libc "$runtime/libc.a" \
  --compiler-runtime "$runtime/libcompiler_rt.a"
gate "test_ctrl_firmware.py --require-rv32" python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
restore
plant() {  # name file anchor replacement: committed in the clone's submodule, gitlink staged
  python3 - "$S/$2" "$3" "$4" <<'PY'
import sys; p, a, r = sys.argv[1:4]; a = a.encode().decode("unicode_escape"); r = r.encode().decode("unicode_escape")
t = open(p).read(); assert t.count(a) == 1, (p, a); open(p, "w").write(t.replace(a, r))
PY
  git -C "$S" -c user.name=probe -c user.email=probe@invalid commit -q -am "probe $1"
  git -C "$R" update-index --cacheinfo "160000,$(git -C "$S" rev-parse HEAD),third_party/tsn-c-stack"
}
echo "=== probe 2: a stack source includes the AECP core's header"
plant "aecp header" src/adp.c '#include <assert.h>\n' '#include <assert.h>\n#include "aecp.h"\n'
gate "ctrl_boundary.py --require-rv32" python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
restore
echo "=== probe 3: an AECP arm's mode guards a stack include of the mailbox HAL"
plant "aecp mode" src/acmp.c '#include "acmp.h"\n' '#include "acmp.h"\n#ifdef AECP_TEST_APP\n#include "mbx_hal.h"\n#endif\n'
gate "ctrl_boundary.py --require-rv32" python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
restore
echo "=== probe 4: the AECP adapter reaches a stack source by its checkout path"
python3 - "$R/sw/firmware/ctrl/aecp/aecp_mbx.c" <<'PY'
import sys; p = sys.argv[1]; t = open(p).read(); a = '#include "aecp_mbx.h"\n'
assert t.count(a) == 1
open(p, "w").write(t.replace(a, a + '#include "../../../../third_party/tsn-c-stack/src/acmp.c"\n'))
PY
gate "ctrl_boundary.py --require-rv32" python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
restore
echo "=== restored"
git -C "$S" status --short; git -C "$R" status --short; git -C "$R" submodule status third_party/tsn-c-stack
