#!/usr/bin/env bash
# comment_only.sh <base tree> <head tree> <work dir>: compare the two RTL files the delta touches, preprocessed and converted, and milan_soc.py's parsed program.
set -u
B=$1 H=$2 W=$3 V=${VERILATOR:-verilator}; mkdir -p "$W"
echo "base $(git -C "$B" rev-parse HEAD) head $(git -C "$H" rev-parse HEAD)"
echo "build inputs the delta touches:"; git -C "$H" diff --name-only "$(git -C "$B" rev-parse HEAD)" "$(git -C "$H" rev-parse HEAD)" -- hdl sw/litex sw/builder/endstation_builder.py configs syn constraints gptp-processor protocol-processor third_party
for f in hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv; do
  "$V" -E -P "$B/$f" > "$W/b.E" 2>/dev/null; rb=$?; "$V" -E -P "$H/$f" > "$W/h.E" 2>/dev/null; rh=$?
  printf '%s verilator -E -P rc %s/%s lines %s %s sha %s %s %s\n' "$f" $rb $rh "$(wc -l <"$W/b.E")" "$(wc -l <"$W/h.E")" "$(sha256sum <"$W/b.E"|cut -c1-16)" "$(sha256sum <"$W/h.E"|cut -c1-16)" "$(cmp -s "$W/b.E" "$W/h.E" && echo IDENTICAL || echo DIFFERENT)"
done
for t in "$B" "$H"; do
  n=$(basename "$t")
  ( cd "$t"; sv2v -I hdl gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv gptp-processor/hdl/wire/*.sv gptp-processor/hdl/common/KL_gptp_timer.sv gptp-processor/hdl/top/KL_gptp_engine.sv hdl/ieee8021as/gptp_plane/*.sv hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv hdl/ieee17221/adp/adp_tx_arbiter.sv hdl/common/KL_link_guard.sv hdl/common/cdc_pulse.sv hdl/common/cdc_handshake.sv > "$W/$n.v" 2>"$W/$n.err"; echo "$n sv2v rc=$? bytes=$(wc -c <"$W/$n.v") raw sha=$(sha256sum <"$W/$n.v"|cut -c1-16) with source line:col normalised sha=$(sed -E 's#\.sv:[0-9]+:[0-9]+#.sv:L:C#' "$W/$n.v"|sha256sum|cut -c1-16)" )
done
b=$(basename "$B"); h=$(basename "$H")
echo "raw sv2v lines that differ: $(diff "$W/$b.v" "$W/$h.v" | grep -c '^<'); of those, not an elaboration-refusal text naming a source line: $(diff "$W/$b.v" "$W/$h.v" | grep '^<' | grep -vc 'Error \[elaboration\]')"
python3 -I - "$B" "$H" <<'PY'
import ast,hashlib,sys
for t in sys.argv[1:]:
    print('milan_soc.py ast', hashlib.sha256(ast.dump(ast.parse(open(t+'/sw/litex/milan_soc.py').read())).encode()).hexdigest()[:16])
PY
