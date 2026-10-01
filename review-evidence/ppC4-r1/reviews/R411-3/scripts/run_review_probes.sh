#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R411-3 reviewer probes for processor PR #137 at 4e558491, in the order run.
# Portable: set CLONE (a clone holding the five commits below), PACKET (output
# directory) and PINNED_VERILATOR (a Verilator 5.050 launcher). Every job runs
# in the foreground; Verilator builds are capped by verilator-capped.sh.
set -euo pipefail
: "${CLONE:?}" "${PACKET:?}" "${PINNED_VERILATOR:?}"
HEAD=4e558491c608dc88efc7963a77cb6b49bce2a46e
LANE=616cbdf1e54a56420e35b53cd161116702f7172d
MAIN=d5f73bac158276a9fcf549185bad5c65c0498dae
BASE=b2db3a970cedbbff2f8ba813acb96122c442bc58
S="$(cd "$(dirname "$0")" && pwd)"
R="$PACKET/receipts"; T="$PACKET/scratch/tree"
mkdir -p "$R" "$PACKET/scratch/bin" "$PACKET/scratch/tmp"
cp "$S/verilator-capped.sh" "$PACKET/scratch/bin/verilator"
export PATH="$PACKET/scratch/bin:$PATH" TMPDIR="$PACKET/scratch/tmp"
V="$PACKET/scratch/bin/verilator"

# 1. composition: the merged delta against the lane's own delta, after renames
git -C "$CLONE" merge-tree --write-tree --name-only "$LANE" "$MAIN" || true
python3 "$S/compose_check.py" "$CLONE" "$BASE" "$LANE" "$MAIN" "$HEAD" > "$R/01-compose_check.txt"

# 2. a disposable export of the exact head (its tree id must be 2cd26489)
rm -rf "$T"; mkdir -p "$T"; git -C "$CLONE" archive "$HEAD" | tar -x -C "$T"
(cd "$T" && git init -q && git add -A && git -c user.name=r -c user.email=r@x commit -qm head \
   && test "$(git rev-parse HEAD^{tree})" = 2cd2648917cdcf1ee850172ab08c6d92cbd23b6b)

# 3. the suites the lane and the merge touch, and the pp_top selectors
for s in rx_validator acmp_listener acmp_nvm; do (cd "$T/tb/$s" && make) > "$R/10-$s.log" 2>&1; done
(cd "$T/tb/pp_top" && make run) > "$R/11-pp_top-run.log" 2>&1
for f in --acmp-only --adp-only --maap-internal-only --name-writes-only; do
  (cd "$T/tb/pp_top" && ./obj_dir/Vpp_top_sim "$f") > "$R/12-pp_top$f.log" 2>&1
done

# 4. mutation campaigns at the merged head
(cd "$T" && python3 tb/pp_top/acmp_mutants.py --output "$R/20-acmp_mutants" --verilator "$V" --jobs 1) \
  > "$R/20-acmp_mutants.log" 2>&1
python3 "$S/mutant_counts.py" "$R/20-acmp_mutants" > "$R/20-acmp_mutants-counts.txt"
make -C "$T/tb/maap" mutants MUTANT_OUTPUT="$R/21-maap_mutants" > "$R/21-maap_mutants.log" 2>&1
make -C "$T/tb/adp_engine" mutants MUTANT_OUTPUT="$R/22-adp_mutants" > "$R/22-adp_mutants.log" 2>&1
# D3 in eight slices (4 copies at a time, each Verilator build at -j 2: 8 jobs)
python3 - "$T" > "$PACKET/scratch/d3_chunks.txt" <<'EOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("d3", sys.argv[1] + "/tb/pp_top/d3_mutants.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
names = sorted({x.name for x in m.MUTANTS})
for i in range(8): print(" ".join(names[i::8]))
EOF
for i in 1 2 3 4 5 6 7 8; do
  # shellcheck disable=SC2046
  (cd "$T" && VERILATOR_BUILD_JOBS=2 python3 tb/pp_top/d3_mutants.py --output "$R/23-d3_mutants/chunk$i" \
     --verilator "$V" --jobs 4 --only $(sed -n "${i}p" "$PACKET/scratch/d3_chunks.txt")) \
     > "$R/23-d3_mutants-chunk$i.log" 2>&1
done

# 5. re-anchor probe: the driver with the pre-rename F29 check names must not KILL
P2="$PACKET/scratch/probe-f29"; rm -rf "$P2"; cp -a "$T" "$P2"; (cd "$P2" && git clean -fdxq)
sed -i '97s/"F30 BIND_RX cdl 84", "F30 PROBE_TX cdl 84"/"F29 BIND_RX cdl 84", "F29 PROBE_TX cdl 84"/' \
  "$P2/tb/pp_top/acmp_mutants.py"
(cd "$P2" && git diff) > "$R/30-probe-f29-names.diff"
(cd "$P2" && python3 tb/pp_top/acmp_mutants.py --output "$R/30-probe-f29-names" --verilator "$V" \
   --jobs 1 --only cdl_not_44_rejected) > "$R/30-probe-f29-names.log" 2>&1 || true

# 6. static gates
(cd "$T" && ./scripts/lint_hdl.sh) > "$R/40-lint_hdl.log" 2>&1
(cd "$T" && python3 scripts/gen_matrix.py --check) > "$R/41-gen_matrix.log" 2>&1
(cd "$T" && make check) > "$R/42-make_check.log" 2>&1
for r in "$BASE..$HEAD" "$LANE..$HEAD" "$MAIN..$HEAD"; do git -C "$CLONE" diff --check "$r"; done

# 7. the name-write driver at the merged head (the gsi driver was not run: see REPORT limits)
(cd "$T" && python3 tb/pp_top/name_wr_mutant.py --output "$R/24-name_wr_mutant") > "$R/24-name_wr_mutant.log" 2>&1
