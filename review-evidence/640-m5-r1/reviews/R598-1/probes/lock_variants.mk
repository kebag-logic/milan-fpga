# Reviewer probe: the lane's lockstep bench at non-shipping parameter sets
# (feature-disabled / configuration-dependent paths). Uses the CSR suite's own
# variables; invoke with: make -f Makefile -f lock_variants.mk r598-var VAR=<a|b|c>
VAR ?= a
VAR_a = NUM_QUEUES=5 ADDR_WIDTH=16 GPTP_PLANE_EN_P=0 MILAN_CLK_FREQ_HZ_P=125000000 CHMAP_RDBK_P=0 PPS_P=1 PPS_WIDTH_CYC_P=125000 N_LISTENERS_P=1 N_TALKERS_P=1 SRP_LSN0_ROW_P=0
VAR_b = NUM_QUEUES=5 ADDR_WIDTH=16 GPTP_PLANE_EN_P=1 MILAN_CLK_FREQ_HZ_P=125000000 CHMAP_RDBK_P=3 PPS_P=1 PPS_WIDTH_CYC_P=125000 N_LISTENERS_P=4 N_TALKERS_P=4 SRP_LSN0_ROW_P=8
VAR_c = NUM_QUEUES=5 ADDR_WIDTH=16 GPTP_PLANE_EN_P=0 MILAN_CLK_FREQ_HZ_P=50000000 CHMAP_RDBK_P=0 PPS_P=0 PPS_WIDTH_CYC_P=50000 N_LISTENERS_P=4 N_TALKERS_P=2 SRP_LSN0_ROW_P=0
SHAPE_a = $(SHAPE_1x1)
SHAPE_b = $(SHAPE_4x4)
SHAPE_c = $(SHAPE_4x4)
N_a = 1
N_b = 4
N_c = 2
G_a = 0
G_b = 1
G_c = 0
VMDIR = obj_r598_$(VAR)
r598-var: $(LOCK_DEPS)
	python3 gen_lockstep.py $(LOCK_SRC) $(LOCK_REF) $(VMDIR)/gen $(VAR_$(VAR))
	$(VERILATOR) $(SHAPE_$(VAR)) $(VFLAGS) --Mdir $(VMDIR) --top-module csr_lockstep_top \
	  -CFLAGS "-DLOCK_N=$(N_$(VAR)) -DLOCK_GPTP=$(G_$(VAR)) -I$(abspath $(VMDIR)/gen) -Wall -Wextra" \
	  $(LOCK_SRC) $(LOCK_REF) $(VMDIR)/gen/csr_lockstep_top.sv sim_lock.cpp -o Vcsr_lock
	./$(VMDIR)/Vcsr_lock
