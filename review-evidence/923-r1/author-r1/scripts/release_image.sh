#!/usr/bin/env bash
# release_image.sh <clone> <out> <cfg-stem>...: the all-fabric (release) recipe's SoC export with its software compiled,
# then the sha256 of the release firmware image (the BIOS with libmilan_baremetal) per config, in <out>/IMAGES.sha256
# (the #919 lane's recipe).
set -u
C=$1; O=$2; shift 2
. /data-2/milan/tmp/923-a789/env.sh
export LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=/data-2/milan/tmp/923-a789/tmp
PY=$WORKSPACE_HOME/litex-milan/venv/bin/python3
mkdir -p "$O"; cd "$C" || exit 3
echo "head $(git rev-parse HEAD) porcelain $(git status --porcelain --untracked-files=no | wc -l)" > "$O/RUN.txt"
for STEM in "$@"; do
  /usr/bin/python3 sw/builder/endstation_builder.py "configs/$STEM.yaml" > "$O/$STEM-builder.log" 2>&1
  mapfile -t ARGV < <(/usr/bin/python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" "sw/builder/out/$STEM/soc_params.json")
  (cd sw/litex && "$PY" milan_soc.py "${ARGV[@]}" --entity-gen-dir "$C/configs/generated/$STEM" --output-dir "$O/$STEM" > "$O/$STEM-soc.log" 2>&1)
  echo "$STEM rc=$?" >> "$O/RUN.txt"
done
git checkout -q -- configs sw/builder 2>/dev/null; git clean -q -fd configs/generated sw/builder/out 2>/dev/null
(cd "$O" && find . -path '*/software/bios/bios.bin' -o -path '*/software/bios/bios.elf' -o -name 'libmilan_baremetal.a' | LC_ALL=C sort | xargs -r sha256sum) > "$O/IMAGES.sha256"
echo "images $(wc -l < "$O/IMAGES.sha256") porcelain-after $(git status --porcelain --untracked-files=no | wc -l)" >> "$O/RUN.txt"
OD=$(ls $WORKSPACE_HOME/br-milan-rv32/host/bin/*-objdump | head -1)
for e in $(cd "$O" && find . -path '*/software/bios/bios.elf' | LC_ALL=C sort); do
  "$OD" -d --no-show-raw-insn "$O/$e" | tail -n +3 | sha256sum | sed "s#-#$e (disassembly)#"
done >> "$O/IMAGES.sha256"
