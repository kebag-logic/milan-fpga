# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The USB network path (#1011) and the status LEDs (#1018).
#
#   make          - build and run both harnesses
#   make tap      - KL_usbnet_tap: the filter classes, the transmit drops, the
#                   best-effort-only injection and its rate limit
#   make leds     - KL_status_leds: each LED rule, the blink and the PWM
#   make mutants  - one planted defect per rule; each must fail
#   make clean
#
# The tap runs at a 1 MHz system clock so a millisecond is 1000 clocks:
# 800 kb/s rate limit, 3200-octet burst, station-record heartbeat timeout.

VERILATOR ?= verilator
RTL       ?= ../../../hdl/usbnet
OBJ       ?= obj_dir

VFLAGS = --cc --exe --build -j 0 -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-PROCASSINIT -Werror-UNDRIVEN -Werror-MULTIDRIVEN \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

TAP_SRCS = $(RTL)/KL_usbnet_pkg.sv $(RTL)/KL_usbnet_rx_copy.sv $(RTL)/KL_usbnet_tx_inject.sv \
           $(RTL)/KL_usbnet_tx_arb.sv $(RTL)/KL_usbnet_tap.sv
TAP_G    = -GCLK_HZ_P=1000000 -GRATE_BPS_P=800000 -GBURST_OCTETS_P=3200

.PHONY: all run tap leds mutants clean
all: run
run: tap leds

tap:
	mkdir -p $(OBJ)/tap
	$(VERILATOR) $(VFLAGS) --top-module KL_usbnet_tap $(TAP_G) --Mdir $(OBJ)/tap \
	  $(TAP_SRCS) sim_main.cpp -o Vtap
	$(abspath $(OBJ))/tap/Vtap

leds:
	mkdir -p $(OBJ)/leds
	$(VERILATOR) $(VFLAGS) --top-module KL_status_leds -GCLK_HZ_P=100000 --Mdir $(OBJ)/leds \
	  $(RTL)/KL_status_leds.sv sim_leds.cpp -o Vleds
	$(abspath $(OBJ))/leds/Vleds

mutants:
	python3 mutants.py

clean:
	rm -rf obj_dir
