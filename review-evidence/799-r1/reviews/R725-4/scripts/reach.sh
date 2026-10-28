#!/bin/sh
# Usage: reach.sh <clone> <base> <head>
# Prints the SV sources the PR changes (parent tree and the processor gitlink
# range) and, for named suites, whether their Makefile names one of them.
set -eu
c=$1; base=$2; head=$3
cd "$c"
old=$(git ls-tree "$base" protocol-processor | awk '{print $3}')
new=$(git ls-tree "$head" protocol-processor | awk '{print $3}')
changed=$( { git diff --name-only "$base" "$head" -- '*.sv' '*.svh';
  git -C protocol-processor diff --name-only "$old" "$new" -- 'hdl/*.sv' 'hdl/*.svh'; } | xargs -n1 basename | sort -u)
echo "changed SV sources: $(echo $changed)"
for s in maap nvm_cosim nvm_backend csr milan_dp_gm_steps aaf aaf_audio_loop chmap_capture tdm mbx follow_ring \
         mmcm_servo aaf_clock_meter crf_rx avtp_rxmon ptp_ts render_queue gptp_plane tkdiag; do
  hits=""
  for f in $changed; do
    grep -v '^[[:space:]]*#' "tb/verilator/$s/Makefile" | grep -q "${f%.*}" && hits="$hits $f"
  done
  dl=$(grep -oE '\$\(MAKE\) -C \.\./[a-z_]+' "tb/verilator/$s/Makefile" | sort -u | tr '\n' ' ')
  echo "$s: non-comment Makefile references:${hits:- none}${dl:+ ; delegates: $dl}"
done
