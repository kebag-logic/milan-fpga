#!/bin/bash
# Probe C2 (shadow path generation ignores entry 0) against milan_dp gptp and tsn_fuzz ptp.
# usage: <parent> <outdir> <tsn-gen-root>
set -u
src="$1"; out="$2"; export TSN_GEN_ROOT="$3"; work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
d="$work/c2"; cp -a "$src" "$d"
python3 -I - "$d/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv" <<'PY'
import sys; p = sys.argv[1]; t = open(p).read()
o = "      || (pub_path_next_w != pub_path_o);"
n = "      || (pub_path_next_w[8*64-1:64] != pub_path_o[8*64-1:64]);"
assert t.count(o) == 1; open(p, "w").write(t.replace(o, n))
PY
cp -a "$d" "$d-f"
( cd "$d" && make -C tb/verilator/milan_dp gptp ) > "$out/C2-milan_dp-gptp.log" 2>&1; echo "C2 milan_dp gptp rc=$? $(grep -E '^[0-9]+ checks:' "$out/C2-milan_dp-gptp.log" | tail -1)" >> "$out/summary.txt" &
( cd "$d-f" && make -C tb/verilator/tsn_fuzz ptp ) > "$out/C2-tsn_fuzz-ptp.log" 2>&1; echo "C2 tsn_fuzz ptp rc=$? $(grep -E '== gPTP.*pass' "$out/C2-tsn_fuzz-ptp.log" | tail -1)" >> "$out/summary.txt" &
wait
