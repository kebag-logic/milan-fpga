#!/usr/bin/env bash
# Differential RV32 image identity: each tree's OWN image builders (ctrl_image.py; ctrl_srp_image.py at every
# shape x 1/2 interfaces x without SRP / SRP / AECP), the same pinned compiler, and the SAME reviewer-built
# stand-in runtime archives on both sides; then the sha256 of every linked ELF, dev against head.
# Usage: image_compare.sh <dev tree> <head tree> <runtime dir with libc.a, libcompiler_rt.a> <out dir> <rv32 cc> <jobs>
set -u
DEV=$(cd "$1" && pwd); HEAD=$(cd "$2" && pwd); RT=$(cd "$3" && pwd); OUT=$4; export MILAN_RV32_CC=$5; J=$6
mkdir -p "$OUT"; OUT=$(cd "$OUT" && pwd)
jobs=()
for side in dev head; do
  T=$DEV; [ $side = head ] && T=$HEAD
  for cfg in "$HEAD"/configs/endstation_*.yaml; do
    s=$(basename "$cfg" .yaml)
    jobs+=("$side|$T|image|$s|1")
    for i in 1 2; do for c in nosrp srp aecp; do jobs+=("$side|$T|$c|$s|$i"); done; done
  done
done
one() {
  IFS='|' read -r side T comp s i <<<"$1"; o=$OUT/$side/$comp-$s-if$i; rm -rf "$o"; mkdir -p "$o"
  cd "$T"
  if [ "$comp" = image ]; then
    python3 -B sw/firmware/ctrl/test/ctrl_image.py --shape "$s" --out "$o/keep" >"$o/run.log" 2>&1
  else
    extra=(); [ "$comp" = nosrp ] && extra=(--without-srp); [ "$comp" = aecp ] && extra=(--with-aecp)
    python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$s.yaml" --output "$o/keep" \
      --interfaces "$i" "${extra[@]}" --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" >"$o/run.log" 2>&1
  fi
  echo $? > "$o/rc"
}
export -f one; export OUT RT
printf '%s\n' "${jobs[@]}" | xargs -P "$J" -I{} bash -c 'one "$@"' _ {}
echo "runs: $(ls -d "$OUT"/*/* | wc -l)"
for d in "$OUT"/head/*; do
  n=$(basename "$d"); a=$OUT/dev/$n
  hh=$(find "$d/keep" -name '*.elf' -type f | sort | xargs -r sha256sum | awk '{print $1}' | tr '\n' ' ')
  dh=$(find "$a/keep" -name '*.elf' -type f | sort | xargs -r sha256sum | awk '{print $1}' | tr '\n' ' ')
  ne=$(find "$d/keep" -name '*.elf' -type f | wc -l)
  v=DIFFER; [ -n "$hh" ] && [ "$hh" = "$dh" ] && v=IDENTICAL
  printf '%s %s rc dev=%s head=%s elfs=%s head=%s dev=%s\n' "$v" "$n" "$(cat "$a/rc")" "$(cat "$d/rc")" "$ne" "$hh" "$dh"
done
