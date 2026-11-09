#!/bin/bash
# Reproduce every measured figure of the 32x32/2if census from a fresh clone of COMMIT, one limit at a time.
# Each stage lifts only the limit the previous stage reported, in the probe's own clone, never the lane.
# usage: census_probe.sh COMMIT OUT     (OUT: the receipts directory; logs are written with host paths scrubbed)
set -u
C=$1 OUT=$2
S=<scratch>
P=$S/probe-$C
. $S/scripts/env.sh
mkdir -p "$OUT"
rm -rf "$P" "$S/probe-out"
$S/scripts/clone.sh "$P" "$C" > "$OUT/clone.log" 2>&1 || { echo "clone failed"; exit 2; }
mkdir -p "$S/probe-out"
O=$S/probe-out
cd "$P"
log() { sed -e "s#$S#<scratch>#g" -e "s#<home>#<home>#g" -e "s#<data>#<data>#g" > "$OUT/$1"; }
step() { # name, command...: run, record rc
    local name=$1; shift
    ( "$@" ) > "$O/$name.raw" 2>&1; local rc=$?
    { cat "$O/$name.raw"; echo "rc=$rc"; } | log "$name.log"
    echo "$name rc=$rc"
}
DRAFT=$S/draft/endstation_ax7101_32x32.yaml
cp "$DRAFT" configs/endstation_ax7101_32x32.yaml
cp "$DRAFT" "$OUT/endstation_ax7101_32x32.draft.yaml"

# Stage 0: the head as it is.
step 00-builder-1x1 python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml -o "$O/b"
step 00-builder-8x8 python3 sw/builder/endstation_builder.py configs/endstation_ax7101_8x8.yaml -o "$O/b"
step 00-builder-32x32 python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o "$O/b"
for s in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    step 00-aemi-$s python3 avdecc/gen_aemi_image.py --overlay "$O/b/$s/aem_overlay.json" --line-bytes 576 -o "$O/$s.aemi.bin"
    step 00-records-$s python3 scripts/check_nvm_record_space.py --config configs/$s.yaml
done
step 00-flash-map python3 sw/litex/flash_map.py

# Stage 1: the builder's 16-stream cap lifted.
sed -i 's/    if len(lst) > 16:/    if len(lst) > 32:/' sw/builder/endstation_builder.py
step 01-builder-32x32 python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o "$O/b"
# Stage 2: the SRP row index widened.
sed -i 's/^SRP_CTX_IDX_BITS = 5 /SRP_CTX_IDX_BITS = 7 /' sw/builder/endstation_builder.py
step 02-builder-32x32 python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o "$O/b"
# Stage 3: the name capacity check skipped: the builder writes the model.
python3 - <<'EOF'
p = "sw/builder/endstation_builder.py"; s = open(p).read()
s = s.replace("    if aem_name_entries > capacity:\n", "    if False and aem_name_entries > capacity:\n", 1)
open(p, "w").write(s)
EOF
step 03-builder-32x32 python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o "$O/b"
step 03-aemi-32x32 python3 avdecc/gen_aemi_image.py --overlay "$O/b/endstation_ax7101_32x32/aem_overlay.json" --line-bytes 576 -o "$O/32.aemi.bin"
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o "$O/b" > /dev/null 2>&1
grep -h "utilization_pct\|ctx_rows" "$O/b/endstation_ax7101_32x32/lwsrp_table.json" "$O/b/endstation_ax7101_8x8/lwsrp_table.json" | log 03-srp-table.txt
grep -h "^- LUT\|^- FF\|^- BRAM\|Verdict" "$O/b/endstation_ax7101_32x32/build_plan.md" | log 03-resources-32x32.txt
grep -h "^- LUT\|^- FF\|^- BRAM\|Verdict" "$O/b/endstation_ax7101_8x8/build_plan.md" | log 03-resources-8x8.txt
step 03-records-32x32 python3 scripts/check_nvm_record_space.py --config configs/endstation_ax7101_32x32.yaml
# the datapath at 32 streams, lint-only, the obj_nxn8 recipe's own flags with the 32x32 shape include
mkdir -p configs/generated/endstation_ax7101_32x32/gen
cp "$O/b/endstation_ax7101_32x32/adp_shape_defaults.svh" configs/generated/endstation_ax7101_32x32/gen/
( cd tb/verilator/milan_dp && make -n build-nxn8 2>/dev/null | grep -- "--top-module milan_datapath" ) > "$O/nxn8.cmd"
CMD=$(sed -e 's#^[^ ]*verilator #$VERILATOR #' -e 's#endstation_ax7101_8x8#endstation_ax7101_32x32#' \
          -e 's#--cc --exe --build -j 0#--lint-only#' -e 's#-GN_STREAMS=8#-GN_STREAMS=32#' \
          -e 's# -CFLAGS "[^"]*"##g' -e 's# sim_nxn.cpp -o Vmilan_dp_nxn8##' "$O/nxn8.cmd")
step 03-datapath-lint-32x32 bash -c "cd tb/verilator/milan_dp && /usr/bin/time -f 'wall=%e maxrss_kb=%M' $CMD"

# The firmware link at 32x32/2if.
W=$O/fw
python3 -B - > "$O/runtime.raw" 2>&1 <<EOF
import subprocess, sys
from pathlib import Path
import pythondata_software_picolibc as picolibc, pythondata_software_compiler_rt as compiler_rt, litex
sys.exit(subprocess.run([sys.executable, '-B', 'tb/verilator/ctrl_service_budget/runtime_ssp.py',
    '--picolibc', picolibc.data_location, '--compiler-rt', compiler_rt.data_location,
    '--litex-software', str(Path(litex.__file__).parent / 'soc/software'), '--output', '$W/runtime']).returncode)
EOF
echo "runtime rc=$?"
link() { python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_32x32.yaml \
    --interfaces 2 --with-aecp --layout split --output "$W/image" --libc "$W/runtime/libc.a" \
    --compiler-runtime "$W/runtime/libcompiler_rt.a" "$@"; }
step 04-firmware-32x32 link
sed -i 's|^_Static_assert(NVM_N_REC <= NVM_ID_SPACE|//_Static_assert(NVM_N_REC <= NVM_ID_SPACE|; s|^_Static_assert(MILAN_NVM_N_NAME <= 128u|//_Static_assert(MILAN_NVM_N_NAME <= 128u|' sw/firmware/ctrl_nvm/nvm_shape.h
step 05-firmware-32x32 link
rm -rf "$O/stack33"; cp -a third_party/tsn-c-stack "$O/stack33"; rm -rf "$O/stack33/.git"
sed -i 's/^#define ACMP_MAX_SINKS 16u/#define ACMP_MAX_SINKS 33u/; s/^#define ACMP_MAX_SOURCES 16u/#define ACMP_MAX_SOURCES 33u/' "$O/stack33/include/acmp.h"
step 06-firmware-32x32 link --stack-source "$O/stack33"
# The contract's per-interface tables at 33 entries, through the variant generator the two-interface build uses.
sed -i 's/^bound_talkers: 16 /bound_talkers: 33 /' sw/mailbox/mailbox.yaml
step 07-contract-bound-33 python3 -B sw/mailbox/gen_mailbox.py --variant-interfaces 2 --out "$O/mbx"
sed -i 's/^bound_talkers: 33 /bound_talkers: 16 /; s/^  sources: 16 /  sources: 33 /; s/^  sinks: 16 /  sinks: 33 /' sw/mailbox/mailbox.yaml
step 08-contract-publication-33 python3 -B sw/mailbox/gen_mailbox.py --variant-interfaces 2 --out "$O/mbx"
sed -i 's/^  sources: 33 /  sources: 17 /; s/^  sinks: 33 /  sinks: 17 /' sw/mailbox/mailbox.yaml
step 09-contract-publication-17 python3 -B sw/mailbox/gen_mailbox.py --variant-interfaces 2 --out "$O/mbx"
git diff | log probe.patch
ls -l "$O"/*.aemi.bin | awk '{print $5, $NF}' | log aemi-sizes.txt
echo done
