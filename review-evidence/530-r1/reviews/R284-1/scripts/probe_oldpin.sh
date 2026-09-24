#!/bin/sh
# Item 1 failing arm, independently: copy the clone, move ONLY the processor
# submodule back to the previous pin 424c688f, regenerate its ROM images and
# run the unchanged obj_crflic leg against the head datapath. Expected: the
# leg FAILS with the Run B burst-end signature (DUT LeaveAll flags only the
# Domain; Talker Advertise Leaves). Usage:
#   REPO=/path/to/clone VERILATOR=/path/to/verilator-5.050 WORK=/scratch/dir OUT=/receipts \
#     sh probe_oldpin.sh
set -eu
: "${REPO:?}" "${VERILATOR:?}" "${WORK:?}" "${OUT:?}"
export VERILATOR VERILATOR_JOBS=8
mkdir -p "$WORK" "$OUT"
rm -rf "$WORK/oldpin"
cp -a "$REPO" "$WORK/oldpin"
cd "$WORK/oldpin"
rm -rf tb/verilator/milan_dp/obj_crflic tb/verilator/milan_dp/ltn_rom.hex tb/verilator/milan_dp/ucode.hex
git -C protocol-processor checkout -q 424c688fa2205b934a7689a58f2aa766420f2326
{
  echo "superproject head $(git rev-parse HEAD)"
  echo "processor checked out at $(git -C protocol-processor rev-parse HEAD)"
  git diff --stat
} > "$OUT/oldpin_identity.txt"
set +e
make -C tb/verilator/milan_dp crflic CRFLIC_MDIR=obj_crflic_oldpin > "$OUT/crflic_oldpin.log" 2>&1
rc=$?
set -e
echo "rc=$rc" >> "$OUT/crflic_oldpin.log"
sha256sum tb/verilator/milan_dp/ucode.hex tb/verilator/milan_dp/ltn_rom.hex >> "$OUT/oldpin_identity.txt"
exit 0
