#!/bin/bash
# probes.sh : reviewer fault probes of the fifth capture and the M8a classifications, in a disposable
# clone at the exact head (PROBE). Each probe edits the clone, runs the boundary gate on captures
# made in that clone, records rc and the gate's verdict lines, and restores the clone with git.
set -u
. "$(dirname "$0")/env.sh"
PROBE=${PROBE:-$PACKET/scratch/probe}; CAPS=$PACKET/scratch/caps; OUT=$PACKET/receipts/probes; mkdir -p "$OUT"
cd "$PROBE" || exit 3
[ "$(git rev-parse HEAD)" = 97e713168470bfae2685521fa557dc462b782b32 ] || exit 3
restore() { git checkout -q -- . && git clean -qfd -e third_party && [ -z "$(git status --porcelain)" ] || { echo "RESTORE FAILED"; exit 4; }; }
capture() { # capture NAME CMD... (in the clone)
  rm -rf "$CAPS/$1"; local n=$1; shift
  python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAPS/$n" -- "$@" > "$OUT/capture-$n.log" 2>&1; echo "capture $n rc $?"; }
gate() { # gate LABEL CAPTURE-NAMES...
  local label=$1; shift; local args=(); for c in "$@"; do args+=(--capture "$CAPS/$c"); done
  local t0=$(date +%s)
  python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator "${args[@]}" > "$OUT/gate-$label.log" 2>&1
  local rc=$?; echo "gate $label rc $rc ($(( $(date +%s)-t0 )) s)"; grep -E 'REFUS|refus|FAIL|finding|reads |names the firmware|holds no|BOUNDARY|PASS' "$OUT/gate-$label.log" | head -8 | sed 's/^/    /'; }
restore
echo "## captures at the exact head"
capture rv32 python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32 &
capture control python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only --jobs 4 &
capture store python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --build-only --jobs 4 &
capture coverage python3 sw/firmware/gtest/fw_coverage.py --build-only --jobs 4 &
capture memory python3 sw/litex/test_ctrl_memory.py --build-only &
wait
FIVE=(rv32 control store coverage memory)
echo "## P0 baseline: five captures, unmodified head (expect rc 0)"; gate P0-baseline "${FIVE[@]}"
echo "## P1 the fifth capture omitted (expect refusal naming sw/litex/test_ctrl_memory.py)"; gate P1-four-captures rv32 control store coverage
edit() { python3 - "$@" <<'PY'
import sys, pathlib
p, old, new = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
t = p.read_text(); assert t.count(old) == 1, (p, old); p.write_text(t.replace(old, new))
PY
}
CFG=sw/firmware/ctrl/test/ctrl_configs.py
echo "## P2 test_ctrl_memory.py removed from BUILDERS (expect refusal naming it)"
edit $CFG '    Builder("sw/litex/test_ctrl_memory.py", (("{python}", "sw/litex/test_ctrl_memory.py", "--build-only"),)),
' ''; gate P2-builder-removed "${FIVE[@]}"; restore
echo "## P3 ctrl_memory.py OUTSIDE entry removed (expect refusal naming it)"
edit $CFG '    "sw/litex/ctrl_memory.py": "reads linked ELF bytes and plans memory banks; it compiles nothing",
' ''; gate P3-ctrl_memory-unclassified "${FIVE[@]}"; restore
echo "## P4 milan_soc.py OUTSIDE entry removed (expect refusal naming it)"
edit $CFG '    "sw/litex/milan_soc.py": "loads a prelinked control image; its optional BIOS and milan_baremetal builds "
                            "compile no control-stack source",
' ''; gate P4-milan_soc-unclassified "${FIVE[@]}"; restore
echo "## P5 ctrl_memory_probe.py PART_OF entry removed (expect refusal naming it)"
edit $CFG '    "sw/litex/ctrl_memory_probe.py": "sw/litex/test_ctrl_memory.py",
' ''; gate P5-probe-unclassified "${FIVE[@]}"; restore
echo "## P6 a stack example header included by the reset entry, fifth capture re-made (expect a finding naming ctrl_split_start.S)"
edit sw/firmware/ctrl/plat/ctrl_split_start.S '	.section .text.start, "ax"
' '#define EXAMPLE_ADP_PORT_H
#include "../../../../third_party/tsn-c-stack/examples/adp_port.h"
	.section .text.start, "ax"
'
capture memory-planted python3 sw/litex/test_ctrl_memory.py --build-only
gate P6-reset-entry-include rv32 control store coverage memory-planted; restore
echo "## P7 control for P6: the same planted reset entry judged with the clean fifth capture (expect rc 0: the finding needs the fifth capture)"
edit sw/firmware/ctrl/plat/ctrl_split_start.S '	.section .text.start, "ax"
' '#define EXAMPLE_ADP_PORT_H
#include "../../../../third_party/tsn-c-stack/examples/adp_port.h"
	.section .text.start, "ax"
'
gate P7-planted-file-old-capture "${FIVE[@]}"; restore
git status --porcelain | wc -l
