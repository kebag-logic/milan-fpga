#!/bin/bash
# Reviewer probe: export (no Vivado) the split SoC of the shipping config at the head, with the
# synthetic control image gate 23m uses (sw/litex/test_ctrl_memory.py's GOOD layout), so the
# generated top-level Verilog can be read for how KL_mbx, KL_mbx_cdc and the datapath are joined.
#   $1 a checkout at the head (with its submodules)   $2 the work directory (empty)
# The environment is the one the author's export_compare.sh uses.
set -eu
T=$1 W=$2
LITEX=$HOME/litex-milan
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$W/tmp
export PATH=$HOME/br-milan-rv32/host/bin:$LITEX/venv/bin:$PATH
export PYTHONPATH=$LITEX/litex:$LITEX/migen
mkdir -p "$W/tmp" "$W/elf"
c=endstation_ax7101_1x1_tdm8
(cd "$T" && /usr/bin/python3 sw/builder/endstation_builder.py "configs/$c.yaml") > "$W/builder.log" 2>&1
argv=$(/usr/bin/python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1]))['argv']))" \
       "$T/sw/builder/out/$c/soc_params.json")
elf=$(cd "$T/sw/litex" && "$LITEX/venv/bin/python3" -c \
      "import sys; from pathlib import Path; import test_ctrl_memory as t; print(t.elf(Path(sys.argv[1]), t.GOOD))" \
      "$W/elf" | tail -1)
echo "argv: $argv --ctrl-mailbox --ctrl-firmware $elf"
(cd "$T/sw/litex" && "$LITEX/venv/bin/python3" milan_soc.py $argv --ctrl-mailbox --ctrl-firmware "$elf" \
   --entity-gen-dir "$T/configs/generated/$c" --output-dir "$W/out") > "$W/export.log" 2>&1
echo "export rc=$?"
ls "$W/out/gateware"/*.v
