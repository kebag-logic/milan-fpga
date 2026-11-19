#!/usr/bin/env bash
# bench_build.sh <1x1|8x8>: the F-G4 DIAGNOSTIC bench bitstream (not the train's) at one point, by S9's recipe as the
# gating lane builds it (its HANDOFF 11.1): a clean clone of the diagnostic commit; the split boot simulation (its
# provisional image and runtime are the recipe's stand-in inputs); endstation_builder --placement split; a stand-in
# export for the CSR map; gen_flash_port; ctrl_plat_image --interfaces 1; then milan_soc.py with the recipe's argv and
# the bench override --eth-port e2, ExtraPostPlacementOpt, 16 threads, --build, through vivado-slot.sh.
set -euo pipefail
P=$1; T=<scratch>; F=$T/fg4; HEAD=fcdb9f6c2fb58ce064768fff4d52a0e142a2519b
LANE=<lane>; V=<management>/2026-09-23/vivado-slot.sh
if [ "$P" = 1x1 ]; then STEM=endstation_ax7101_1x1_tdm8; else STEM=endstation_ax7101_8x8; fi
CFG=configs/$STEM.yaml; R=$F/repo$P; W=$F/work$P; B=$W/boot
PY=<home>/litex-milan/venv/bin/python3
say() { echo "[bench $P $(date +%T)] $*"; }
# 1. the clean clone of the diagnostic commit, submodules from the lane's checkouts
if [ ! -d "$R" ]; then
  git clone -q --shared --no-checkout "$T/d12" "$R"
  git -C "$R" -c advice.detachedHead=false checkout -q --detach "$HEAD"
  for dep in $(git -C "$R" config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -v '^external$'); do
    git -C "$R" config "submodule.$dep.url" "$LANE/$dep"
  done
  git -C "$R" -c protocol.file.allow=always submodule update -q --init --force \
    $(git -C "$R" config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -v '^external$')
fi
say "head $(git -C "$R" rev-parse HEAD) porcelain $(git -C "$R" status --porcelain | wc -l)"
mkdir -p "$W" "$F/tmp"
# 2. the split boot simulation (S9's environment), the stand-in's inputs and the boot check
(
  export PATH=<home>/br-milan-rv32/host/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
  export VERILATOR=<tools>/pinned-verilator-5.050/verilator COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
  export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$F/tmp MAKEFLAGS="-j8 --no-print-directory"
  cd "$R" && "$PY" -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B" --shape "$STEM" > "$W/boot.log" 2>&1
)
say "boot simulation: $(tail -1 "$W/boot.log")"
# 3. the recipe
export PATH=<home>/br-milan-rv32/host/bin:/usr/local/bin:/usr/bin:/bin COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt --vivado-max-threads 16)
cd "$R"
/usr/bin/python3 sw/builder/endstation_builder.py "$CFG" --placement split > "$W/builder.log" 2>&1
mapfile -t ARGV < <(/usr/bin/python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" sw/builder/out/$STEM/soc_params.json)
FW=$(printf '%s\n' "${ARGV[@]}" | grep -A1 -x -- --ctrl-firmware | tail -1)
STANDIN=$B/image-provisional/ctrl_app.elf
STAND_ARGV=("${ARGV[@]}"); for i in "${!STAND_ARGV[@]}"; do [ "${STAND_ARGV[$i]}" = "$FW" ] && STAND_ARGV[$i]=$STANDIN; done
rm -rf "$W/standin" "$W/flash-map" "$W/image"
(cd sw/litex && "$PY" milan_soc.py "${STAND_ARGV[@]}" --eth-port e2 --entity-gen-dir "$R/configs/generated/$STEM" "${FLOW[@]}" --no-compile-software --output-dir "$W/standin" > "$W/standin.log" 2>&1)
"$PY" -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$W/standin/csr.csv" --csr-h "$W/standin/software/include/generated/csr.h" --out "$W/flash-map" > "$W/flash-map.log" 2>&1
"$PY" -B sw/firmware/ctrl/test/ctrl_plat_image.py --config "$CFG" --interfaces 1 --csr-csv "$W/standin/csr.csv" --flash-map "$W/flash-map" --output "$W/image" --libc "$B/runtime/libc.a" --compiler-runtime "$B/runtime/libcompiler_rt.a" > "$W/image.log" 2>&1
cp "$W/image/ctrl_app.elf" "$FW"
say "platform image $(sha256sum "$FW" | cut -c1-16)"
# 4. the bench build: the recipe's argv, the bench override --eth-port e2, through a Vivado slot
export HOME=<home> XILINXD_LICENSE_FILE=<home>/.Xilinx/Xilinx.lic
OUT=$W/build_ExtraPostPlacementOpt
date -Iseconds > "$W/build.start"
"$V" bash -c "source <home>/Xilinx/2026.1/Vivado/settings64.sh && export PATH=\$PATH:<home>/br-milan-rv32/host/bin && cd '$R/sw/litex' && '$PY' milan_soc.py $(printf '%q ' "${ARGV[@]}") --eth-port e2 --entity-gen-dir '$R/configs/generated/$STEM' $(printf '%q ' "${FLOW[@]}") --no-compile-software --build --output-dir '$OUT'" > "$W/build.log" 2>&1
echo $? > "$W/build.rc"; date -Iseconds > "$W/build.end"
say "build rc=$(cat "$W/build.rc")"
"$PY" sw/litex/check_image_identity.py "$OUT" > "$W/identity.log" 2>&1; say "identity: $(tail -1 "$W/identity.log")"
( cd "$OUT" && sha256sum gateware/alinx_ax7101.bit aem_desc.bin csr.csv flashboot_layout.json image_manifest.json 2>/dev/null ) > "$W/artifacts.sha256"
sha256sum "$FW" >> "$W/artifacts.sha256"
say "artifacts: $(head -1 "$W/artifacts.sha256")"
echo done > "$W/BENCH_DONE"
