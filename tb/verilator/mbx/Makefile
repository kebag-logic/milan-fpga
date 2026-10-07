# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of the packet-mailbox fabric skeleton (KL_mbx and
# its leaves, #665 lane F0), through BOTH bus adapters.
#   make           - the RTL checks through KL_mbx_wb, then through KL_mbx_axil,
#                    then the firmware co-simulation over the real RTL, then the
#                    same checks on a two-interface variant of the contract
#                    through both adapters and on the host model (run-if2), then
#                    five planted RTL defects (one per leaf and one in the
#                    filter's tuple), each of which must redden the check it
#                    names (mutants.py --quick)
#   make mutants   - every planted RTL defect, after both positive controls
#   make clean     - remove build artifacts
#
# The RTL list is the mailbox's own, package first. RTL_DIR is overridable so
# mutants.py builds a planted COPY with this same recipe (print-vflags).

VERILATOR ?= verilator
VBUILD_JOBS ?= 0
ROOT      := ../../..
RTL_DIR   ?= $(ROOT)/hdl/milan/mailbox
TOP        = tb_mbx_top

RTL = $(RTL_DIR)/KL_mbx_pkg.sv $(RTL_DIR)/KL_mbx_ring.sv $(RTL_DIR)/KL_mbx_rx.sv \
      $(RTL_DIR)/KL_mbx_tx.sv $(RTL_DIR)/KL_mbx_evt.sv $(RTL_DIR)/KL_mbx.sv \
      $(RTL_DIR)/KL_mbx_wb.sv $(RTL_DIR)/KL_mbx_axil.sv tb_mbx_top.sv

# The directory of the contract header the C++ side includes: the tracked one.
CONTRACT_INC := $(abspath $(ROOT))/sw/firmware/ctrl/mbx

# -Werror-USERERROR: an elaboration $error is a failed build, never a warning.
# -Werror-PINMISSING / -Werror-UNDRIVEN: a dropped binding is refused by name.
VFLAGS = --cc --exe --build -j $(VBUILD_JOBS) --top-module $(TOP) \
         -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Werror-UNDRIVEN \
         -Wno-DECLFILENAME -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I$(CONTRACT_INC)"

# The firmware the co-simulation links: the mailbox driver, the event loop,
# the port layer, the ADP slice, the ACMP module and the app, compiled as C11 exactly as the
# target builds them, plus the host model the same scenario also runs on.
# mbx_hal.h is answered by cosim_main.cpp, never by the host platform file.
FW_DIR := $(abspath $(ROOT)/sw/firmware/ctrl)
FW_SRC  = $(addprefix $(FW_DIR)/,mbx/mbx.c loop/ctrl_loop.c port/ctrl_pool.c port/ctrl_debug.c \
            port/shlan_port.c adp/adp.c adp/adp_mbx.c maap/maap.c maap/maap_mbx.c maap/maap_csr.c \
            acmp/acmp.c acmp/acmp_mbx.c acmp/acmp_nvm.c app/ctrl_app.c host/mbx_model.c)
FW_INC  = $(addprefix -I$(FW_DIR)/,mbx wire host port loop adp maap acmp app) -I$(abspath $(ROOT))/sw/firmware/ctrl_nvm
# Every header those sources can include, so a header-only change rebuilds them.
FW_HDR  = $(wildcard $(FW_DIR)/*/*.h) $(wildcard $(abspath $(ROOT))/sw/firmware/ctrl_nvm/*.h)
CC     ?= cc
AR     ?= ar

.PHONY: all run-wb run-axil run-cosim run-if2 if2-gen mutants-quick mutants print-vflags clean
all: run-wb run-axil run-cosim run-if2 mutants-quick

run-wb:
	$(VERILATOR) $(VFLAGS) -GHOST_P=0 --Mdir obj_wb $(RTL) sim_main.cpp -o Vmbx_wb
	@echo "======================================================================"
	./obj_wb/Vmbx_wb 0

run-axil:
	$(VERILATOR) $(VFLAGS) -GHOST_P=1 --Mdir obj_axil $(RTL) sim_main.cpp -o Vmbx_axil
	@echo "======================================================================"
	./obj_axil/Vmbx_axil 1

obj_fw/libctrlfw.a: $(FW_SRC) $(FW_HDR)
	@mkdir -p obj_fw
	rm -f obj_fw/*.o obj_fw/libctrlfw.a
	cd obj_fw && $(CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic $(FW_INC) -c $(FW_SRC)
	cd obj_fw && $(AR) crs libctrlfw.a *.o

# Verilator's own build relinks Vmbx_cosim only when one of its objects
# changed, and the firmware library is not one of them: the binary goes
# whenever the library is newer, so a firmware-only change is never run stale.
run-cosim: obj_fw/libctrlfw.a
	if [ -e obj_cosim/Vmbx_cosim ] && [ obj_cosim/Vmbx_cosim -ot obj_fw/libctrlfw.a ]; then \
	  rm -f obj_cosim/Vmbx_cosim; fi
	$(VERILATOR) $(VFLAGS) -GHOST_P=0 --Mdir obj_cosim $(RTL) cosim_main.cpp \
	  -CFLAGS "-Wall -Wextra $(FW_INC)" -LDFLAGS "$(abspath obj_fw/libctrlfw.a)" -o Vmbx_cosim
	@echo "======================================================================"
	./obj_cosim/Vmbx_cosim

# The per-interface own MAC on two real interfaces (lane FC): the contract
# elaborated for two by its generator into the build directory (never the
# tree), then the same suite on that RTL through both adapters, and on the host
# model compiled against that header (model_main.cpp). The variant's header
# directory comes first, so every include of mbx_contract.h finds it.
IF2      := obj_if2
IF2_GEN  := $(abspath $(IF2))/gen
IF2_RTL   = $(IF2_GEN)/KL_mbx_pkg.sv $(RTL_DIR)/KL_mbx_ring.sv $(RTL_DIR)/KL_mbx_rx.sv \
            $(RTL_DIR)/KL_mbx_tx.sv $(RTL_DIR)/KL_mbx_evt.sv $(IF2_GEN)/KL_mbx.sv \
            $(RTL_DIR)/KL_mbx_wb.sv $(RTL_DIR)/KL_mbx_axil.sv tb_mbx_top.sv
IF2_VFLAGS = $(subst -I$(CONTRACT_INC),-I$(IF2_GEN),$(VFLAGS))
CXX ?= c++

if2-gen:
	python3 -B $(ROOT)/sw/mailbox/gen_mailbox.py --variant-interfaces 2 --out $(IF2_GEN)

run-if2: if2-gen
	$(VERILATOR) $(IF2_VFLAGS) -GHOST_P=0 --Mdir $(IF2)/obj_wb $(IF2_RTL) sim_main.cpp -o Vmbx_wb
	$(VERILATOR) $(IF2_VFLAGS) -GHOST_P=1 --Mdir $(IF2)/obj_axil $(IF2_RTL) sim_main.cpp -o Vmbx_axil
	$(CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic -I$(IF2_GEN) $(FW_INC) \
	  -c $(FW_DIR)/host/mbx_model.c -o $(IF2)/mbx_model.o
	$(CXX) -std=c++17 -O2 -Wall -Wextra -Werror -I$(IF2_GEN) -I. -I$(FW_DIR)/test $(FW_INC) \
	  model_main.cpp $(IF2)/mbx_model.o -o $(IF2)/Vmbx_model
	@echo "======================================================================"
	./$(IF2)/obj_wb/Vmbx_wb 0
	./$(IF2)/obj_axil/Vmbx_axil 1
	./$(IF2)/Vmbx_model

# run-wb and run-axil are this arm's positive controls, hence the prerequisites
mutants-quick: run-wb run-axil
	python3 -B mutants.py --quick

mutants:
	python3 -B mutants.py

# mutants.py builds its copies with this recipe, read through this target.
print-vflags:
	@printf '%s\n' $(VERILATOR) $(VFLAGS)

clean:
	rm -rf obj_wb obj_axil obj_cosim obj_fw obj_if2
