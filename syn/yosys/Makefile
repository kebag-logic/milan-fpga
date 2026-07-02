# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Open-toolchain synthesis check (Yosys, device-independent). Proves the XPM-free
# RTL builds on non-Xilinx FPGAs. See README.md.
#   make          - generic synth of every top
#   make ecp5     - target a real device (Lattice ECP5)

.PHONY: all ecp5 clean
all:
	./run.sh

ecp5:
	YOSYS_SYNTH=synth_ecp5 ./run.sh

clean:
	@true
