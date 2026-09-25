#!/bin/sh
# Run the R249-3 mutant campaign against the DEFAULT targets of the csr and
# pp_shadow suites. Usage: run-mutants.sh <disposable tree> <receipt dir>
# Needs a Verilator 5.050 first on PATH and python3 with PyYAML.
set -u
T=$1
R=$2
M="python3 $(dirname "$0")/mutate3.py $T $R"
PP="make -C tb/verilator/pp_shadow"
CSR="make -C tb/verilator/csr"

# Reviewer round-2 receipts 41, 43 and 35, now against the default targets.
$M m41-shadow-vid-hop hdl/milan/KL_pp_shadow.sv \
  '      .SRP_DOM_DEF_VID_P (SRP_DOM_DEF_VID_P),\n' '' -- $PP
$M m43-datapath-vid-hop hdl/milan/milan_datapath.sv \
  '      .SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C),\n' '' -- $PP
$M m35-csr-reset-bits-masked hdl/common/csr/milan_csr.sv \
  'lwsrp_ctrl <= LWSRP_CTRL_RST_C;' "lwsrp_ctrl <= LWSRP_CTRL_RST_C & ~32'h3;" -- $CSR

# Round-3 additions: the donor hop, the builder emitters behind the new
# fixtures, and the live admission output.
$M m60-donor-top-vid-hop protocol-processor/hdl/top/protocol_processor_top.sv \
  '      .DOM_DEF_VID_P    (SRP_DOM_DEF_VID_P),\n' '' -- $PP
$M m61-builder-dom-vid-const sw/builder/endstation_builder.py \
  "ADP_SRP_DOM_DEF_VID_C = 16'd{cfg['srp']['vid']};" "ADP_SRP_DOM_DEF_VID_C = 16'd2;" -- $PP
$M m62-builder-reset-talker-bit sw/builder/endstation_builder.py \
  '| (int(s["talker_declare_at_reset"]) << 1)' '| 0' -- $CSR
$M m63-builder-crf-not-counted sw/builder/endstation_builder.py \
  'n_src = len(cfg["talkers"]) + (1 if cfg["clocking"]["crf_output"] else 0)' \
  'n_src = len(cfg["talkers"])' -- $PP
$M m64-csr-talker-arm-stuck0 hdl/common/csr/milan_csr.sv \
  'assign o_lwsrp_talker_en     = lwsrp_ctrl[1];' "assign o_lwsrp_talker_en     = 1'b0;" -- $CSR
# The child hop inside the processor (the other reviewer's round-2 R7b).
$M m65-child-srp-top-vid-hop protocol-processor/hdl/srp/KL_srp_top.sv \
  '      .DEF_VID_P  (DOM_DEF_VID_P)' "      .DEF_VID_P  (16'd2)" -- $PP
