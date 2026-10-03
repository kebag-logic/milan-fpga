#!/usr/bin/env bash
# R444-1: out-of-context cell counts of KL_aecp_nvm_writer and KL_aecp_desc_store
# at a revision, at the 1x1 stream shape, through sv2v then Yosys synth_xilinx
# (xc7, flattened). Usage: ooc_writer.sh REPO REV NAMES OUTDIR
set -u
REPO=$1; REV=$2; NAMES=$3; OUT=$4
d="$OUT/${REV:0:8}-n$NAMES"; rm -rf "$d"; mkdir -p "$d/src"
git -C "$REPO" archive "$REV" hdl | tar -x -C "$d/src"
W="$d/src/hdl/aecp/KL_aecp_nvm_writer.sv"
sv2v "$W" > "$d/writer.v" || exit 3
NP=""
grep -q "N_NAME_P" "$W" && NP="chparam -set N_NAME_P $NAMES KL_aecp_nvm_writer;"
yosys -q -l "$d/writer.log" -p "read_verilog $d/writer.v; \
  chparam -set N_STREAM_IN_P 1 -set N_STREAM_OUT_P 1 -set N_AUDIO_UNIT_P 1 \
          -set N_CLK_DOMAIN_P 1 KL_aecp_nvm_writer; $NP \
  synth_xilinx -flatten -family xc7 -top KL_aecp_nvm_writer; tee -o $d/writer.stat stat" >/dev/null 2>&1
echo "== ${REV:0:8} N_NAME_P=$NAMES writer"
grep -E "LUT[1-6]|RAM32M|RAM64M|RAM32X1|RAM64X1|FD[RSCE]+ |FDRE|FDSE|FDCE|FDPE|RAMB|DSP" "$d/writer.stat" | sed 's/^ */  /'
