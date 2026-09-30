#!/usr/bin/env bash
# R400-3 reproduction: every reviewer run, in the order made, each in the foreground.
# Usage: R400_VERILATOR_ROOT=<Verilator 5.050 root> reproduce.sh <processor clone at the exact head>
# Every build and run happens in a git-archive copy under the packet's scratch/;
# the clone is only read (git archive, git show, git diff, git merge-tree).
set -uo pipefail
CLONE=$1
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/env.sh"
R="$P/receipts"; mkdir -p "$R"
HEAD=921fff59d6e1243284e477f7a368173018420d35
fresh() { rm -rf "$1"; mkdir -p "$1"; git -C "$CLONE" archive "$HEAD" | tar -x -C "$1"; }

# 1. merge audit: the mechanical merge of the round-2 head and main, against the merge commit
git -C "$CLONE" merge-tree --write-tree --name-only 053f979b b2db3a97 > "$R/merge-tree.txt"
AUTO=$(head -1 "$R/merge-tree.txt")
git -C "$CLONE" diff "$AUTO" c842670 -- tb/pp_top tb/maap > "$R/merge-resolution-vs-automerge-pp_top-maap.diff"
git -C "$CLONE" diff "$AUTO" c842670 -- tb/rx_validator > "$R/merge-resolution-vs-automerge-rx_validator.diff"

# 2. suites and entry points at the head
T="$P/scratch/head/tree"; fresh "$T"
make -C "$T/tb/maap" run > "$R/head-maap-run.log" 2>&1; echo "rc=$?" > "$R/head-maap-run.rc"
make -C "$T/tb/rx_validator" > "$R/head-rx_validator-run.log" 2>&1; echo "rc=$?" > "$R/head-rx_validator-run.rc"
make -C "$T/tb/pp_top" run > "$R/head-pp_top-run.log" 2>&1; echo "rc=$?" > "$R/head-pp_top-run.rc"
make -C "$T/tb/pp_top" maap-internal > "$R/head-pp_top-maap-internal.log" 2>&1; echo "rc=$?" > "$R/head-pp_top-maap-internal.rc"
(cd "$T/tb/pp_top" && ./obj_dir/Vpp_top_sim --d3-only) > "$R/head-pp_top-d3-only.log" 2>&1; echo "d3rc=$?" > "$R/head-pp_top-d3-only.rc"
for m in --gsi-internal-only --name-writes-only --dr3a; do
  (cd "$T/tb/pp_top" && ./obj_dir/Vpp_top_sim $m) > "$R/head-pp_top$m.log" 2>&1; echo "$m rc=$?" >> "$R/head-pp_top-modes.rc"
done
make -C "$T/tb/srp_top" > "$R/head-srp_top-run.log" 2>&1; echo "rc=$?" > "$R/head-srp_top-run.rc"

# 3. the MAAP campaign, and a slice of the D3 campaign with its goldens
make -C "$T/tb/maap" mutants MUTANT_OUTPUT="$R/maap-mutants" > "$R/maap-mutants.txt" 2>&1; echo "rc=$?" > "$R/maap-mutants.rc"
(cd "$T" && python3 tb/pp_top/d3_mutants.py --output "$R/d3-mutants-slice" --verilator "$VERILATOR" --jobs 1 \
   --only validator_admits_held_aecp dispatch_not_held) > "$R/d3-mutants-slice.txt" 2>&1; echo "rc=$?" > "$R/d3-mutants-slice.rc"

# 4. static gates
(cd "$T" && ./scripts/lint_hdl.sh) > "$R/head-lint_hdl.log" 2>&1; echo "lint rc=$?" > "$R/head-static.rc"
(cd "$T" && python3 scripts/gen_matrix.py --check) > "$R/head-gen_matrix.log" 2>&1; echo "gen_matrix rc=$?" >> "$R/head-static.rc"
make -C "$T" check > "$R/head-make-check.log" 2>&1; echo "make check rc=$?" >> "$R/head-static.rc"
for b in c951a9ff 053f979b b2db3a97; do git -C "$CLONE" diff --check "$b" "$HEAD" >/dev/null; echo "diff --check $b rc=$?"; done >> "$R/head-static.rc"

# 5. the head bench against the round-1 MAAP RTL (b03d36f): U29 must absorb 20 of 20
D="$P/scratch/r1rtl"; fresh "$D"
git -C "$CLONE" show b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745:hdl/maap/KL_pp_maap.sv > "$D/hdl/maap/KL_pp_maap.sv"
make -C "$D/tb/maap" run > "$R/r1rtl-maap-run.log" 2>&1; echo "rc=$?" > "$R/r1rtl-maap-run.rc"

# 6. reviewer probes (three disposable mutants), each planted in a fresh archive copy
python3 "$HERE/make_probe_patches.py" "$CLONE" "$P/probes"
bash "$HERE/run_probes.sh" "$CLONE" "$P/probes" "$R/probes" > "$R/probes.txt" 2>&1

# 7. clone integrity
bash "$HERE/verify_clone.sh" "$CLONE" > "$R/clone-verify.txt" 2>&1
