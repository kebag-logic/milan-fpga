#!/bin/bash
# ctrl_plat_image.py given a relative map, a missing map and a map at another clock. mapflag_probe.sh <clone> <run> <out>
. "$(dirname "$0")/env.sh"
clone=$1; run=$2; out=$3; mkdir -p "$out"
cd "$clone" || exit 9
rel=$(realpath --relative-to="$clone" "$run/split-soc/flash-map")
args=(--config configs/endstation_ax7101_1x1_tdm8.yaml --csr-csv "$run/soc-provisional/csr.csv" --libc "$run/runtime/libc.a" --compiler-runtime "$run/runtime/libcompiler_rt.a")
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py "${args[@]}" --flash-map "$rel" --output "$out/rel" > "$out/rel.log" 2>&1
echo "relative map rc=$?"; riscv32-linux-objdump -d "$out/rel/ctrl_app.elf" | grep -cE 'lui.*0x20000$'
riscv32-linux-objcopy -O binary "$out/rel/ctrl_app.elf" "$out/rel.bin"; riscv32-linux-objcopy -O binary "$run/image-provisional/ctrl_app.elf" "$out/abs.bin"
ls -l "$out/rel.bin" "$out/abs.bin" | awk '{print $5}'; cmp "$out/rel.bin" "$out/abs.bin" && echo 'relative map: loaded bytes equal the absolute map image, same csr.csv'
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py "${args[@]}" --flash-map /nonexistent/map --output "$out/none" > "$out/none.log" 2>&1
echo "missing map rc=$?"; tail -1 "$out/none.log" | cut -c1-160
cp -r "$run/split-soc/flash-map" "$out/badclock"
python3 -I -c "import json,sys;p=sys.argv[1];d=json.load(open(p));d['clock_hz']=50000000;json.dump(d,open(p,'w'))" "$out/badclock/flash_port.json"
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py "${args[@]}" --flash-map "$out/badclock" --output "$out/clock" > "$out/clock.log" 2>&1
echo "wrong-clock map rc=$?"; tail -1 "$out/clock.log" | cut -c1-160
