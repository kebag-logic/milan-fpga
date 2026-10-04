#!/bin/sh
# Re-measure the four slope controls at N = 3, 5, 8, one shape per run, each in
# a scratch copy. usage: <tree> <scratch> <receipt-dir>
set -u
tree=$1; scr=$2; out=$3; mkdir -p "$out"
for c in slope-stored-at-stage-2-index slope-stored-at-source-0 slope-store-source-0-only slope-read-source-0; do
  (
    d="$scr/slope-$c"; rm -rf "$d"; mkdir -p "$d/tb"
    cp -r "$tree/hdl" "$d/hdl"; cp -r "$tree/tb/srp_admission" "$tree/tb/common" "$d/tb/"
    cd "$d" && git apply "$tree/tb/srp_top/mutations/$c.patch" || exit 2
    for n in 3 5 8; do
      make -C tb/srp_admission run N=$n > "$out/$c-N$n.log" 2>&1
      echo "$c N=$n: $(grep -E "^[0-9]+ checks:" "$out/$c-N$n.log" | tail -1)"
    done
    rm -rf "$d"
  ) &
done
wait
