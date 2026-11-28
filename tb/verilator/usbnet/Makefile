# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The USB network path (#1011) and the status LEDs (#1018).
#
#   make          - build and run the fabric and command harnesses
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

JOBS ?= 4
VFLAGS = --cc --exe --build -j $(JOBS) -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-PROCASSINIT -Werror-UNDRIVEN -Werror-MULTIDRIVEN \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

TAP_SRCS = $(RTL)/KL_usbnet_pkg.sv $(RTL)/KL_usbnet_rx_copy.sv $(RTL)/KL_usbnet_tx_inject.sv \
           $(RTL)/KL_usbnet_tx_arb.sv $(RTL)/KL_usbnet_tap.sv
TAP_G    = -GCLK_HZ_P=1000000 -GRATE_BPS_P=800000 -GBURST_OCTETS_P=3200

.PHONY: all run tap leds truth local wait clock datapath datapath-plants attachment egress egress-plants mutants clean
all: run
run: tap leds truth local wait clock attachment egress

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

truth:
	mkdir -p $(OBJ)/truth
	$(VERILATOR) $(VFLAGS) --top-module KL_status_led_truth --Mdir $(OBJ)/truth \
	  $(RTL)/KL_status_led_truth.sv sim_truth.cpp -o Vtruth
	$(abspath $(OBJ))/truth/Vtruth

local:
	mkdir -p $(OBJ)/local
	$(VERILATOR) $(VFLAGS) --top-module KL_usbnet_local_rx --Mdir $(OBJ)/local \
	  $(RTL)/KL_usbnet_pkg.sv $(RTL)/KL_usbnet_rx_copy.sv $(RTL)/KL_usbnet_local_rx.sv sim_local.cpp -o Vlocal
	$(abspath $(OBJ))/local/Vlocal

wait:
	mkdir -p $(OBJ)/wait
	$(VERILATOR) $(VFLAGS) --top-module usbnet_mailbox_wrap --Mdir $(OBJ)/wait \
	  ../../../hdl/milan/mailbox/KL_mbx_pkg.sv ../../../hdl/milan/mailbox/KL_mbx_rx.sv \
	  $(RTL)/KL_usbnet_pkg.sv $(RTL)/KL_usbnet_rx_copy.sv $(RTL)/KL_usbnet_local_rx.sv \
	  usbnet_mailbox_wrap.sv sim_wait.cpp -o Vwait
	$(abspath $(OBJ))/wait/Vwait

mutants:
	python3 mutants.py
	python3 datapath_leds.py $(OBJ)/datapath-plants --plants

egress:
	python3 egress_measure.py $(OBJ)/egress
	python3 egress_controls.py

egress-plants:
	python3 egress_measure.py $(OBJ)/egress-plants --plants
	python3 egress_controls.py

datapath:
	python3 datapath_leds.py $(OBJ)/datapath

datapath-plants:
	python3 datapath_leds.py $(OBJ)/datapath-plants --plants

clock: truth datapath
	python3 clock_commands.py $(OBJ)/clock $(OBJ)/truth $(OBJ)/datapath/4

attachment:
	mkdir -p $(OBJ)/attachment
	python3 led_attachment.py $(OBJ)/attachment/led_attachment.v
	$(VERILATOR) $(VFLAGS) --top-module led_attachment --Mdir $(OBJ)/attachment \
	  $(OBJ)/attachment/led_attachment.v $(RTL)/KL_status_led_truth.sv $(RTL)/KL_status_leds.sv \
	  sim_attachment.cpp -o Vattachment
	$(abspath $(OBJ))/attachment/Vattachment

clean:
	rm -rf obj_dir
