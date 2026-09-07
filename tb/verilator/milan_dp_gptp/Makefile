# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

# Separate driver deadline for the real-cadence gPTP integration. The shared
# recipe owns the generated image, elaboration parameters and build directory.
# The milan_dp default no longer runs this leg, so a sweep executes it once.
.PHONY: all extended
all:
	$(MAKE) -C ../milan_dp ax1x1gptp
	python3 verify_abort.py

extended:
	$(MAKE) -C ../milan_dp ax1x1gptp-extended
