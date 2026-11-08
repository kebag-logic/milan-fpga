#!/usr/bin/env bash
# probe_onevec.sh <clean-clone-at-head> <out-dir> [verilator]
#
# Reviewer probes of milan_dp's crflic leg [ONEVEC] check (PR #852, issue #851).
# Runs in a disposable COPY of the given clone; the clone itself is not modified.
#   clean : the leg at the head's processor pin (044cb25f)            expect rc 0, [ONEVEC] PASS
#   old   : the leg with KL_srp_encoder.sv from processor 92100657    expect rc 1, [ONEVEC] doubled-value FAIL
#   g1    : grader probe, value increment removed (kk = 0)            shows whether multi-value vectors occur
#   g2    : grader probe, Listener Ignore skip removed                shows whether Ignore values occur
# Between 92100657 and 044cb25f only hdl/srp/KL_srp_encoder.sv differs under the processor's hdl/.
set -euo pipefail
src=$(readlink -f "$1"); out=$(readlink -f "$2"); V=${3:-verilator}
mkdir -p "$out"; work="$out/work"; rm -rf "$work"; cp -a "$src" "$work"
cd "$work"
git rev-parse HEAD > "$out/head.txt"
cp -a protocol-processor/hdl "$out/pp_old_hdl"
git -C protocol-processor show 92100657:hdl/srp/KL_srp_encoder.sv > "$out/pp_old_hdl/srp/KL_srp_encoder.sv"
cd tb/verilator/milan_dp
cp sim_crf_licence.cpp "$out/sim_crf_licence.orig"
b() { make -s -j"${JOBS:-8}" crflic-build VERILATOR="$V" VERILATOR_JOBS="${JOBS:-8}" CRFLIC_MDIR="obj_probe_$1" "${@:2}" > "$out/build_$1.log" 2>&1; }
b clean
b old PP_DIR="$out/pp_old_hdl"
python3 -I - "$out" <<'EOF'
import sys
out = sys.argv[1]
s = open(f"{out}/sim_crf_licence.orig").read()
a = "const uint64_t kk = static_cast<uint64_t>(k);"
c = "if (n4 && ((f[fp + static_cast<size_t>(k / 4)] >> (6 - 2 * (k % 4))) & 3) == 0) continue;"
assert s.count(a) == 1 and s.count(c) == 1, "grader moved; update the probe patterns"
open(f"{out}/g1.cpp", "w").write(s.replace(a, "const uint64_t kk = 0;  // PROBE G1"))
open(f"{out}/g2.cpp", "w").write(s.replace(c, "/* PROBE G2 */"))
EOF
for g in g1 g2; do cp "$out/$g.cpp" sim_crf_licence.cpp; b "$g"; done
cp "$out/sim_crf_licence.orig" sim_crf_licence.cpp
for t in clean old g1 g2; do
  set +e; "./obj_probe_$t/Vmilan_dp_crflic" > "$out/run_$t.log" 2>&1; echo "$t rc=$?" >> "$out/rc.txt"; set -e
done
cat "$out/rc.txt"
