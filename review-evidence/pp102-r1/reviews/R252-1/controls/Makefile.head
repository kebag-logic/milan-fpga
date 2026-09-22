# SPDX-License-Identifier: CERN-OHL-W-2.0
# protocol_processor_top end-to-end suite — exit 0 = PASS.
#
# Two builds of one bench. The first overrides nothing and runs every
# section; the second overrides P-SRP-DOM-DEF-VID with SRP_VID_FIXTURE and
# runs section DV alone (README). The SRP engine's own default is 2 as well,
# so only a value the child cannot produce shows a dropped or misbound
# top-level connection. Each binary prints its own build's count; the last
# line is the one canonical tally, summed over both builds.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = pp_top_wrap
# verification only: Milan 4.2.7.2.1 fixes the product value at 2. README
# section DV says why this pattern
SRP_VID_FIXTURE = 5A3C

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/common/pp_pkg.sv $(HDL)/srp/srp_pkg.sv \
       $(HDL)/acmp/pp_acmp_pkg.sv $(HDL)/adp/pp_adp_pkg.sv \
       $(HDL)/common/KL_pp_prng.sv $(HDL)/common/KL_pp_timer_service.sv \
       $(HDL)/packet_engine/KL_pp_rx_validator.sv \
       $(HDL)/packet_engine/KL_pp_rx_slots.sv \
       $(HDL)/packet_engine/KL_pp_normalizer.sv \
       $(HDL)/packet_engine/KL_pp_dispatch.sv \
       $(HDL)/packet_engine/KL_pp_tx_slots.sv \
       $(HDL)/packet_engine/KL_pp_release_merge.sv \
       $(HDL)/packet_engine/KL_pp_tx_arbiter.sv \
       $(HDL)/packet_engine/KL_pp_scoreboard.sv \
       $(HDL)/packet_engine/KL_pp_event_router.sv \
       $(HDL)/packet_engine/KL_pp_originator.sv \
       $(HDL)/packet_engine/KL_pp_trace_ring.sv \
       $(HDL)/packet_engine/KL_pp_side_port.sv \
       $(HDL)/packet_engine/KL_pp_nvm_port.sv \
       $(HDL)/aecp/ucpu_pkg.sv $(HDL)/aecp/KL_aecp_ucpu.sv \
       $(HDL)/aecp/KL_aecp_desc_store.sv $(HDL)/aecp/KL_aecp_dyn_state.sv $(HDL)/aecp/KL_aecp_engine.sv $(HDL)/aecp/KL_aecp_resp_buf.sv \
       $(HDL)/aecp/KL_aecp_notify.sv $(HDL)/aecp/KL_aecp_ca_originator.sv \
       $(HDL)/adp/KL_adp_engine.sv \
       $(HDL)/acmp/KL_pp_acmp_listener.sv $(HDL)/acmp/KL_acmp_talker.sv \
       $(HDL)/acmp/KL_acmp_nvm_shadow.sv \
       $(HDL)/maap/KL_pp_maap.sv \
       $(HDL)/srp/KL_srp_decoder.sv $(HDL)/srp/KL_srp_domain.sv \
       $(HDL)/srp/KL_srp_vlan.sv $(HDL)/srp/KL_srp_admission.sv \
       $(HDL)/srp/KL_srp_talker_fsm.sv $(HDL)/srp/KL_srp_listener_fsm.sv \
       $(HDL)/srp/KL_srp_encoder.sv $(HDL)/srp/KL_srp_top.sv \
       $(HDL)/top/KL_mrp_strip.sv $(HDL)/top/protocol_processor_top.sv \
       pp_top_wrap.sv
CPP  = sim_main.cpp

run: fixture-guards ltn_rom.hex ucode.hex
	@rm -f obj_dir/build_tally.txt
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim
	./obj_dir/Vpp_top_sim
	$(VERILATOR) $(VFLAGS) "+define+PP_TOP_SRP_DOM_DEF_VID=16'h$(SRP_VID_FIXTURE)" \
	    -CFLAGS "-DPP_TOP_SRP_DOM_DEF_VID=0x$(SRP_VID_FIXTURE) -Wall -Wextra" \
	    --Mdir obj_vid $(SRCS) $(CPP) -o Vpp_top_vid
	./obj_vid/Vpp_top_vid
	@awk '{c += $$1; f += $$2} END {if (NR != 2) {print "FAIL: " NR " build tallies, expected 2"; exit 1} printf "%d checks: %d PASS, %d FAIL\n", c, c - f, f}' \
	    obj_dir/build_tally.txt

# Compile the actual bench with four fixture settings in a temporary model dir.
# No simulation or source mutation; bad fixtures must fail for the named guards.
fixture-guards: fixture-guards-test
	@python3 fixture_guards.py --verilator "$(VERILATOR)" --cxx "$(CXX)" -- \
	    $(filter-out --exe --build,$(VFLAGS)) $(SRCS)

fixture-guards-test:
	@python3 -B -m unittest -v test_fixture_guards.py

ltn_rom.hex: $(HDL)/acmp/rom/gen_ltn_rom.py
	python3 $< -o $@

ucode.hex: $(HDL)/aecp/ucode/gen_ucode.py
	python3 $< -o $@

clean:
	rm -rf obj_dir obj_vid ltn_rom.hex ucode.hex

.PHONY: run fixture-guards fixture-guards-test clean
