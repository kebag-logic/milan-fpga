#!/bin/bash
# images.sh ROOT OUTDIR RUNTIME_DIR : link the 65 control images of one checkout
#   5 standalone (ctrl_image.py, one per shipped shape) and 60 runtime-linked
#   (ctrl_srp_image.py: 5 shapes x 1/2 interfaces x without-srp/srp/aecp x flat/split),
#   copy each ELF to OUTDIR/elf/<canonical name>.elf and write OUTDIR/manifest.sha256.
set -u
root=$1; out=$2; rt=$3
mkdir -p "$out/err" "$out/elf"
cd "$root"
jobs=()
for cfg in configs/*.yaml; do
  s=$(basename "$cfg" .yaml)
  jobs+=("python3 -B sw/firmware/ctrl/test/ctrl_image.py --shape $s --out $out/standalone/$s")
  for i in 1 2; do for c in without-srp srp with-aecp; do for l in flat split; do
    flag=""; [ "$c" = srp ] || flag="--$c"
    jobs+=("python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config $cfg --interfaces $i $flag --layout $l --output $out/runtime/$s-if$i-$c-$l --libc $rt/libc.a --compiler-runtime $rt/libcompiler_rt.a")
  done; done; done
done
printf '%s\n' "${jobs[@]}" > "$out/commands.txt"
fail=0
printf '%s\n' "${jobs[@]}" | xargs -P 8 -I{} bash -c 'e=$(mktemp "$0/err/XXXXXX"); {} > "$e" 2>&1 || { echo "FAILED: {}"; tail -3 "$e"; exit 1; }' "$out" || fail=1
for d in "$out"/standalone/*/; do s=$(basename "$d"); n=$(find "$d" -name ctrl_app.elf | wc -l)
  [ "$n" = 1 ] || { echo "standalone $s: $n ELFs"; fail=1; }; find "$d" -name ctrl_app.elf -exec cp {} "$out/elf/standalone-$s.elf" \; ; done
for d in "$out"/runtime/*/; do cp "$d/ctrl_app.elf" "$out/elf/runtime-$(basename "$d").elf" || fail=1; done
(cd "$out/elf" && sha256sum *.elf > ../manifest.sha256)
echo "images: $(wc -l < "$out/manifest.sha256") ELFs, build failures: $fail"
exit $fail
