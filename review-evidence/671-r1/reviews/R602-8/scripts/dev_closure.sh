#!/bin/sh
# Usage: dev_closure.sh <repo-root>
# Lists which lane-relevant input paths dev changed between the two merges.
cd "$1" || exit 2
C=c6bd08c6f52632c6d33d834ce842ac3cf63f29cc; D=fa8209889411e8ca95757174c981f720dbcd95a2
for p in hdl/milan/KL_nvm_backend.sv hdl/milan/KL_pp_shadow.sv sw/firmware/milan_baremetal \
         sw/firmware/nvm_hosttest tb/verilator/nvm_cosim tb/verilator/nvm_capture_cpu sw/litex/patches \
         configs sw/builder protocol-processor gptp-processor sw/litex/boot_policy.py sw/litex/flash_map.py \
         scripts/nvm_contract.py scripts/nvm_klj2.py scripts/nvm_shape.py scripts/check_nvm_record_space.py \
         scripts/check_nvm_capture.py sw/litex/milan_soc.py; do
  if git diff --quiet $C $D -- "$p"; then echo "unchanged-by-dev $p"; else echo "CHANGED-by-dev $p"; fi
done
