#!/bin/bash
# Link every RV32 image fixture of one tree with that tree's own scripts.
# usage: images.sh <tree> <outdir> <libc.a> <libcompiler_rt.a>
# Needs MILAN_RV32_CC. Writes one log and rc per image under <outdir>.
set -u
tree=$1; out=$2; libc=$3; crt=$4
shapes="endstation_arty_4x4 endstation_arty_8ch endstation_arty_current endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8"
mkdir -p "$out"
jobs=()
for s in $shapes; do
  jobs+=("ctrl $s")
  for i in 1 2; do jobs+=("srp $s $i with" "srp $s $i without"); done
done
one() {
  set -- $1
  if [ "$1" = ctrl ]; then
    d="$out/ctrl_image/$2"; mkdir -p "$d"
    (cd "$tree" && python3 -B sw/firmware/ctrl/test/ctrl_image.py --shape "$2" --out "$d") > "$d.log" 2>&1
    echo $? > "$d.rc"
  else
    d="$out/srp_image/$2-if$3-$4"; mkdir -p "$d"
    extra=(); [ "$4" = without ] && extra=(--without-srp)
    (cd "$tree" && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$2.yaml" \
       --interfaces "$3" "${extra[@]}" --output "$d" --libc "$libc" --compiler-runtime "$crt") > "$d.log" 2>&1
    echo $? > "$d.rc"
  fi
}
export -f one; export out tree libc crt
printf '%s\n' "${jobs[@]}" | xargs -P 6 -I{} bash -c 'one "$@"' _ {}
