#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R291-3 reviewer probes for PR #110 at 2e1675d2. Portable: pass the reviewed
# clone, the packet directory and a Verilator 5.050 executable.
#   run_probes.sh <clone> <packet> <verilator>
# Every probe runs in a disposable clone under <packet>/scratch; the reviewed
# clone is only read. Receipts go to <packet>/receipts.
set -uo pipefail
CLONE=$(readlink -f "$1"); PKT=$(readlink -f "$2"); VL=$3
HEAD=2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f
PRIOR=cc077a6ffe20585d20b116f008e07189ba1bb7f8
BASE=008edbbf486598ae237414273d75e385cf0e1a56
R=$PKT/receipts; S=$PKT/scratch
mkdir -p "$R" "$S"
T=$S/tree
rm -rf "$T" "$S/tree-prior"
git clone -q --no-hardlinks "$CLONE" "$T" && git -C "$T" checkout -q --detach "$HEAD"
git clone -q --no-hardlinks "$CLONE" "$S/tree-prior" && git -C "$S/tree-prior" checkout -q --detach "$PRIOR"
export PATH="$(dirname "$VL"):$PATH"

step() { # name, command...
  local n=$1; shift
  ( cd "$T" && "$@" ) >"$R/$n.log" 2>&1; local rc=$?
  echo "$n rc=$rc" | tee -a "$R/rc.txt"
}
: >"$R/rc.txt"
{ echo "clone HEAD $(git -C "$T" rev-parse HEAD) tree $(git -C "$T" rev-parse 'HEAD^{tree}')"
  echo "verilator: $("$VL" --version)"; echo "wrapper sha256: $(sha256sum < "$VL")"
  echo "wrapper: $(cat "$VL")"; } >"$R/identity.txt"

# 1. scope of round 2: only these files may differ from the round-1b head
git -C "$T" diff --stat "$PRIOR..$HEAD" >"$R/round2-scope.txt"
git -C "$T" diff --name-status "$BASE..$HEAD" >"$R/pr-scope.txt"
step diff-check git diff --check "$BASE" "$HEAD"

# 2. figure freshness: re-render each hand-authored SVG at its committed width
: >"$R/png-render.txt"
for f in 20-rtl-dataflow 21-integration-faces 22-aecp-descriptor-fetch 23-bringup-decision 24-adp-acmp-states; do
  w=$(file "$T/docs/diagrams/$f.png" | sed -E 's/.* ([0-9]+) x ([0-9]+).*/\1/')
  rsvg-convert -w "$w" -o "$S/render-$f.png" "$T/docs/diagrams/$f.svg"
  a=$(sha256sum <"$S/render-$f.png" | cut -d' ' -f1); b=$(sha256sum <"$T/docs/diagrams/$f.png" | cut -d' ' -f1)
  echo "$f width=$w committed=$b rerender=$a $([ "$a" = "$b" ] && echo BYTE-IDENTICAL || echo DIFFERENT)" >>"$R/png-render.txt"
done
rsvg-convert --version | head -1 >>"$R/png-render.txt"

# 3. guard suite, full (expect 78/78)
step guard-suite make -C tb/desc_mem_guard VERILATOR="$VL"
# 4. unguarded reproduction (expected FAIL at the completed byte assertion)
step guard-baseline make -C tb/desc_mem_guard baseline VERILATOR="$VL"
# 5. hold-deleted mutation control (expect rc 0 = detected)
step guard-hold-mutant python3 tb/desc_mem_guard/mutate.py --output "$S/hold-mutant"
cp "$S/hold-mutant/mutant-no-hold.log" "$R/guard-hold-mutant-sim.log" 2>/dev/null

# 6. inverted priority mutant: terminal-beat clear wins over acceptance
M=$S/prio; mkdir -p "$M"
python3 - "$T/hdl/aecp/KL_aecp_desc_mem_guard.sv" "$M/guard_prio.sv" <<'PY'
import sys
src = open(sys.argv[1]).read()
old = """    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
    end else if (m_rsp_valid_i && m_rsp_ready_o
                 && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
    end"""
new = """    end else if (m_rsp_valid_i && m_rsp_ready_o
                 && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
    end"""
assert src.count(old) == 1, "REFUSED: priority block not found exactly once"
open(sys.argv[2], "w").write(src.replace(old, new))
PY
diff -u "$T/hdl/aecp/KL_aecp_desc_mem_guard.sv" "$M/guard_prio.sv" >"$R/prio-mutant.diff"
step prio-mutant-head make -C tb/desc_mem_guard GUARD_SRC="$M/guard_prio.sv" OBJ_DIR=obj_prio VERILATOR="$VL"
# same mutant against the round-1b bench: shows the new assertion is the sole discriminator
( cd "$S/tree-prior" && make -C tb/desc_mem_guard GUARD_SRC="$M/guard_prio.sv" OBJ_DIR=obj_prio VERILATOR="$VL" ) \
  >"$R/prio-mutant-prior-bench.log" 2>&1; echo "prio-mutant-prior-bench rc=$?" | tee -a "$R/rc.txt"

# 7. integration suites touching the seam
step desc-store-suite make -C tb/desc_store VERILATOR="$VL"
step pp-top-suite make -C tb/pp_top VERILATOR="$VL"
# 8. lint of the guard and the top with the whole tree visible (repo rule)
pk=$(cd "$T" && find hdl -name '*_pkg.sv' | sort); al=$(cd "$T" && find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
for top in KL_aecp_desc_mem_guard protocol_processor_top; do
  # shellcheck disable=SC2086
  step "lint-$top" "$VL" --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --top-module "$top" $pk $al
done
# 9. documentation gates and generated matrix
step make-check make check
step gen-matrix python3 scripts/gen_matrix.py --check
git -C "$T" status --porcelain --ignored >"$R/probe-tree-status.txt"
echo done >>"$R/rc.txt"
