#!/bin/bash
# Export the switch-on SoC at the shipping 1x1 shape, then compare KL_mbx's instance with the module's port list.
tree=$1; elf=$2; out=$3; cd "$tree" || exit 9
cfg=endstation_ax7101_1x1_tdm8
OPTS=$(bash -c ". configs/generated/sweep_opts_ax7101.sh; printf '%s' \"\$OPTS\"")
# shellcheck disable=SC2086
python3 sw/litex/milan_soc.py $OPTS --entity-gen-dir "$PWD/configs/generated/$cfg" --output-dir "$out" --no-compile --ctrl-mailbox --ctrl-firmware "$elf" > "$out.log" 2>&1
echo "export rc=$?"
