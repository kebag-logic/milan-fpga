#!/usr/bin/env bash
# vivado_mutants.sh: the suite's campaign through the two Vivado legs at the lane head,
# one Vivado at a time; its control is the full head bench through both legs
set -u
export PYTHONDONTWRITEBYTECODE=1
export PATH=<vivado>/2026.1/Vivado/bin:<scratch>/tools/bin:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
out=<scratch>/rec/head_vivado_mutants
L=<lane>
start=$(date +%s)
flock -x $VIVADO_LOCK python3 -B $L/tb/elab_guards/mutants.py --verilator "$VERILATOR" \
  --frontend xsim --frontend synth --jobs 1 --output "$out" \
  --only KL_pp_nvm_port.g_tmo_check:error,KL_pp_nvm_port.g_tmo_check:warning,KL_pp_nvm_port.g_tmo_check:initial,KL_pp_acmp_listener.g_strm_tmo_check:error,KL_pp_acmp_listener.g_strm_tmo_check:warning,KL_pp_acmp_listener.g_strm_tmo_check:initial,protocol_processor_top.gen_g_owner_overlap:error,protocol_processor_top.gen_g_owner_overlap:warning,protocol_processor_top.gen_g_owner_overlap:initial,protocol_processor_top.gen_g_tmr_overlap:error,KL_aecp_engine.gen_g_line_ceiling:warning,bench:deleted,bench:tightened,bench:loosened \
  > "$out.log" 2>&1
echo $? > "$out.rc"; echo $(( $(date +%s) - start )) > "$out.secs"
