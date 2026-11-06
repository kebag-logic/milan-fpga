#!/bin/bash
# identity_probe.sh CHECKOUT BOOTDIR OUT: is the json-only image the no-map image? Links both to one output path, compares
# loadable sections; then a complete map given by relative path, and the plain refusal with real archives.
C=$1; B=$2; O=$3; rm -rf "$O"; mkdir -p "$O/json-only"; cp "$B/split-soc/flash-map/flash_port.json" "$O/json-only/"; cd "$C"
args=(--config configs/endstation_ax7101_1x1_tdm8.yaml --csr-csv "$B/split-soc/mapped/soc/csr.csv" --output "$O/link" --libc "$B/runtime/libc.a" --compiler-runtime "$B/runtime/libcompiler_rt.a")
sum() { riscv32-linux-objcopy -O binary "$O/link/ctrl_app.elf" "$O/$1.bin"; sha256sum "$O/$1.bin" | cut -c1-64; }
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py "${args[@]}" --flash-map "$O/json-only" > "$O/json-only.log" 2>&1; echo "json-only rc=$?"; J=$(sum json-only); rm -rf "$O/link"
# the refusal taken out of a throwaway copy of the script, in the same directory so its imports hold
sed 's/^        refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))$/        pass/' sw/firmware/ctrl/test/ctrl_plat_image.py > sw/firmware/ctrl/test/ctrl_plat_image_noguard.py
python3 -B sw/firmware/ctrl/test/ctrl_plat_image_noguard.py "${args[@]}" > "$O/nomap.log" 2>&1; echo "no-map (refusal removed in a copy) rc=$?"; N=$(sum nomap); rm -rf "$O/link" sw/firmware/ctrl/test/ctrl_plat_image_noguard.py
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py "${args[@]}" --flash-map "$B/split-soc/flash-map" > "$O/true.log" 2>&1; echo "true map rc=$?"; T=$(sum true); rm -rf "$O/link"
echo "json-only image $J"; echo "no-map image    $N"; echo "true-map image  $T"
[ "$J" = "$N" ] && echo "json-only == no-map: BYTE-IDENTICAL" || echo "json-only != no-map"; [ "$J" = "$T" ] && echo "json-only == true map" || echo "json-only != true map"
rel=$(realpath --relative-to="$PWD" "$B/split-soc/flash-map"); python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py "${args[@]}" --flash-map "$rel" > "$O/rel.log" 2>&1; echo "relative complete map rc=$?"; R=$(sum rel); rm -rf "$O/link"; [ "$R" = "$T" ] && echo "relative map == true map" || echo "relative map != true map (FALLS THROUGH)"
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py "${args[@]}" > "$O/refused.log" 2>&1; echo "no map, real archives rc=$? elf=$([ -e "$O/link/ctrl_app.elf" ] && echo yes || echo no)"; tail -1 "$O/refused.log" | cut -c1-170
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml --csr-csv sw/firmware/ctrl/test/ctrl_plat_csr.csv --output "$O/none" --libc "$O/absent/libc.a" --compiler-runtime "$O/absent/libcompiler_rt.a" > "$O/none.log" 2>&1; echo "no map, no archives rc=$? elf=$([ -e "$O/none/ctrl_app.elf" ] && echo yes || echo no)"; grep -m1 -c 'No such file' "$O/none.log"
