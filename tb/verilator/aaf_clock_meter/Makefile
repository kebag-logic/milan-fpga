# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_aaf_clock_meter (#629, docs/design/MEDIA_CLOCK_FOLLOWING.md): the meter
# rows of the design's test plan, M1 to M14, each with its named mutant.
#   make         - build and run every case, then the mutation campaign
#   make run     - the meter cases and the servo-with-meter run
#   make cases   - the meter cases only (Vmeter_sim CASE... runs some)
#   make servo   - the servo with the meter driving its reference ports
#   make mutants - every named mutant must fail its named check (mutants.py)
#   make clean   - remove build artifacts
#
# CLK_HZ is the ONE value for both the RTL's CLK_FREQ_HZ_P (the 100 ms
# timeouts) and the harness's slot length (CLK_HZ / 8000 cycles per 125 us
# PDU): derive, never mirror. Every rate is timestamp arithmetic, so the
# compressed clock changes no rate.

VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR    = ../../../hdl
CLK_HZ    ?= 200000
METER_RTL ?= $(RTL_DIR)/ieee1722/crf/KL_aaf_clock_meter.sv
MDIR      ?= obj_dir

VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --top-module meter_wrap \
         -GCLK_HZ_P=$(CLK_HZ) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DCLK_HZ_TB=$(CLK_HZ)"

SRCS = $(RTL_DIR)/ieee1722/avtp/avtp_subtype_pkg.sv $(METER_RTL) \
       $(RTL_DIR)/ieee1722/crf/KL_crf_rx.sv meter_wrap.sv

# The servo with the meter in front of it (sim_servo.cpp): the servo at its
# silicon loop parameters, TICK_CYC the one value for the RTL's 1 ms tick at
# the harness's 24.576 MHz / 32 audio clock and for the harness itself.
# --public-flat-rw: the harness reads the servo's tick divider (to run clk_i
# fine around each tick) and its window error; it writes nothing through it.
TICK_CYC   ?= 768
SERVO_RTL  ?= $(RTL_DIR)/ieee1722/crf/KL_mmcm_drp_servo.sv
SERVO_MDIR ?= obj_servo
SERVO_FLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --top-module meter_servo_wrap \
         --public-flat-rw -GTICK_CYC_P=$(TICK_CYC) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DTICK_CYC_TB=$(TICK_CYC)"
SERVO_SRCS = $(RTL_DIR)/ieee1722/avtp/avtp_subtype_pkg.sv $(METER_RTL) \
       $(RTL_DIR)/common/cdc_pulse.sv $(RTL_DIR)/common/cdc_handshake.sv \
       $(SERVO_RTL) meter_servo_wrap.sv

.PHONY: all run build cases servo servo-build mutants clean
all: run mutants

build:
	$(VERILATOR) $(VFLAGS) -Mdir $(MDIR) $(SRCS) sim_main.cpp -o Vmeter_sim

cases: build
	@echo "======================================================================"
	./$(MDIR)/Vmeter_sim

servo-build:
	$(VERILATOR) $(SERVO_FLAGS) -Mdir $(SERVO_MDIR) $(SERVO_SRCS) sim_servo.cpp -o Vservo_sim

servo: servo-build
	@echo "======================================================================"
	./$(SERVO_MDIR)/Vservo_sim

run: cases servo

mutants:
	python3 mutants.py

clean:
	rm -rf obj_dir obj_servo obj_mut_*
