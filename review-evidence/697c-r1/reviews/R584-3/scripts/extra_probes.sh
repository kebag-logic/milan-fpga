#!/usr/bin/env bash
# R584-3 extra probes, each in a disposable copy of the checkout at the exact head.
# Usage: extra_probes.sh <disposable-checkout-copy> <receipts-dir>
set -u; C=$1; R=$2
# 1. The gate without gptp-processor: must refuse (exit 2) naming the submodule.
cd "$C" && mv gptp-processor gptp-processor.aside && mkdir gptp-processor
python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 > "$R/no_gptp.log" 2>&1; echo "rc=$?" >> "$R/no_gptp.log"
rmdir gptp-processor && mv gptp-processor.aside gptp-processor
# 2. The pin recipe with its errors ignored ('-' prefix): the static check passes it (boundary_probes.py
#    makefile-pin-errors-ignored); the self-test's bench arms must not.
sed -i 's|^\tpython3 -B $(FW_DIR)/test/ctrl_build.py --stack-pin $(STACK_DIR)$|\t-python3 -B $(FW_DIR)/test/ctrl_build.py --stack-pin $(STACK_DIR)|' tb/verilator/mbx/Makefile
W=$(mktemp -d)
(cd sw/firmware/ctrl/test && python3 -B -c "
import sys; sys.path.insert(0,'../../gtest')
from pathlib import Path
import ctrl_pin, ctrl_configs
bad,n=ctrl_pin.pin_controls(Path('$W'), ctrl_configs.makefiles())
print('misbehaved', bad, 'of', n)") > "$R/pin_controls_pin_errors_ignored.log" 2>&1
echo "rc=$?" >> "$R/pin_controls_pin_errors_ignored.log"
git checkout -q -- tb/verilator/mbx/Makefile; rm -rf "$W"
# 3. The image builder at the head and at dev aef7ac66 (a second copy checked out there), five shapes each:
#    python3 -B sw/firmware/ctrl/test/ctrl_image.py --shape <each of configs/*.yaml> --out <dir>; sha256 of every ELF.
# 4. The mailbox bench at the head: make -C tb/verilator/mbx -j16 VERILATOR=<pinned 5.050> VBUILD_JOBS=8
# 5. ctrl_image_selftest.py; scripts/ci_events.py --check; the docs gates listed in docs_checks.log.
