#!/usr/bin/env bash
# #651 example at the reviewed head: ooc.sh KL_nvm_backend refuses N_NAME_P=235
# and 129, and accepts the 128 boundary, with the pinned converter.
# Args: <sv2v-0.0.12 bin dir> <work dir>
set -u
S12=$1; W=$2
home="$W/home"; rm -rf "$W"; mkdir -p "$home/.local/bin"; cp "$S12/sv2v" "$home/.local/bin/sv2v"
export PYTHONDONTWRITEBYTECODE=1
echo "converter: $(HOME=$home PATH="$home/.local/bin:$PATH" sv2v --version)"
for n in 235 129 128; do
  out=$(HOME="$home" OOC_TMP="$W/ooc.$n" OOC_CHPARAM="N_NAME_P=$n" syn/yosys/ooc.sh KL_nvm_backend 2>&1)
  rc=$?
  echo "-- ooc.sh KL_nvm_backend N_NAME_P=$n rc=$rc"
  printf '%s\n' "$out" | grep -E 'KL_nvm_backend|ERROR|FAIL' | cut -c1-200 | head -4
done
