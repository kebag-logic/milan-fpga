#!/usr/bin/env bash
# Build every ctrl_srp_image.py fixture (each shipped shape x 1/2 interfaces x without-SRP/SRP/AECP) in one
# checkout against empty runtime archives, so each run compiles every firmware object in link order and stops
# at its link; then list the sha256 of each object in link order. The linked images are a function of these
# objects, their order, the linker script and the runtime, so equal object lists at two revisions with the
# same runtime give equal images.
# usage: srp_objects.sh <checkout> <out dir> <runtime dir holding libc.a and libcompiler_rt.a> <jobs>
set -u
repo=$1 out=$2 rt=$3 jobs=$4
mkdir -p "$out"
one() {
  local shape=$1 ifs=$2 comp=$3 flag=()
  case $comp in without-srp) flag=(--without-srp);; with-aecp) flag=(--with-aecp);; esac
  local d="$out/$shape-if$ifs-$comp"
  rm -rf "$d"
  (cd "$repo" && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$shape.yaml" \
     --interfaces "$ifs" --output "$d" --libc "$rt/libc.a" --compiler-runtime "$rt/libcompiler_rt.a" \
     "${flag[@]}") > "$d.log" 2>&1
  echo "rc=$?" >> "$d.log"
}
running=0
for cfg in "$repo"/configs/*.yaml; do
  shape=$(basename "$cfg" .yaml)
  for ifs in 1 2; do
    for comp in without-srp srp with-aecp; do
      one "$shape" "$ifs" "$comp" &
      running=$((running + 1))
      if [ "$running" -ge "$jobs" ]; then wait -n; running=$((running - 1)); fi
    done
  done
done
wait
for d in "$out"/*/; do
  d=${d%/}; n=$(basename "$d")
  (cd "$d" && ls *.o 2>/dev/null | sort -n | xargs -r sha256sum | sed "s#^#$n #")
done
