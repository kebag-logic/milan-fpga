#!/usr/bin/env bash
# fabric_route_image.sh: the shipping 1x1 all-fabric export at the lane head, firmware compiled, for the endpoint route.
set -euo pipefail
L=<lane>; S=<scratch>; W=$S/route/fabric
PY=<home>/litex-milan/venv/bin/python3
export PATH=<home>/br-milan-rv32/host/bin:/usr/local/bin:/usr/bin:/bin PYTHON=<home>/litex-milan/venv/bin/python3 PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux
cd "$L"; echo "head $(git rev-parse HEAD)"
mapfile -t ARGV < <(cd sw/builder && /usr/bin/python3 -c "
import contextlib, io, endstation_builder as eb
p='../../configs/endstation_ax7101_1x1_tdm8.yaml'
with contextlib.redirect_stdout(io.StringIO()): eb.build(p)
print('\n'.join(eb.emit_soc_argv(eb.load_config(p))))")
rm -rf "$W"
(cd sw/litex && "$PY" milan_soc.py "${ARGV[@]}" --entity-gen-dir "$L/configs/generated/endstation_ax7101_1x1_tdm8" \
  --synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt \
  --vivado-max-threads 32 --output-dir "$W" > "$W.log" 2>&1)
"$PY" sw/litex/check_image_identity.py "$W"
/usr/bin/python3 syn/ooc/pp_baseline.py "$W/gateware" --single-thread-synthesis
echo done
