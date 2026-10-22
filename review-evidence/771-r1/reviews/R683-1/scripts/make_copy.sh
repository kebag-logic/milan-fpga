#!/usr/bin/env bash
# Usage: make_copy.sh SRC_CLONE DEST [GPTP_SHA]  - disposable shared clone at SRC HEAD with
# submodules cloned from SRC's module stores at the recorded gitlinks (or GPTP_SHA for gptp-processor).
set -eu
S=$1; D=$2; GP=${3:-}
rm -rf "$D"; git clone -q --shared --no-checkout "$S" "$D"
git -C "$D" checkout -q --detach "$(git -C "$S" rev-parse HEAD)"
for m in protocol-processor gptp-processor third_party/verilog-axis third_party/tsn-c-stack third_party/lwSRP; do
  sha=$(git -C "$D" rev-parse "HEAD:$m")
  [ "$m" = gptp-processor ] && [ -n "$GP" ] && sha=$GP
  rm -rf "$D/$m"; git clone -q --shared --no-checkout "$S/.git/modules/$m" "$D/$m"
  git -C "$D/$m" checkout -q --detach "$sha"
  echo "$m $(git -C "$D/$m" rev-parse HEAD)"
done
git -C "$D" rev-parse HEAD
