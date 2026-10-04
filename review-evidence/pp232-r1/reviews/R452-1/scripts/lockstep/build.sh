#!/usr/bin/env bash
# Build one lockstep shape.
# Usage: build.sh REPO REF_COMMIT CANDIDATE_SV N_CTRL N_IN N_OUT IDENT OBJDIR
#   REPO        processor clone (pp_pkg.sv taken from CANDIDATE's tree is not
#               needed: pp_pkg.sv is read from REPO at REF_COMMIT, unchanged by the lane)
#   REF_COMMIT  main's commit; its hdl/aecp/KL_aecp_notify.sv becomes KL_aecp_notify_ref
#   CANDIDATE_SV  the candidate KL_aecp_notify.sv (head, or a planted control copy)
# Needs `verilator` on PATH (the pinned 5.050).
set -euo pipefail
repo=$1; refc=$2; cand=$3; n=$4; nin=$5; nout=$6; ident=$7; obj=$8
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$obj/src"
git -C "$repo" show "$refc:hdl/common/pp_pkg.sv" >"$obj/src/pp_pkg.sv"
git -C "$repo" show "$refc:hdl/aecp/KL_aecp_notify.sv" \
  | sed -e 's/^module KL_aecp_notify$/module KL_aecp_notify_ref/' \
        -e 's/^endmodule : KL_aecp_notify$/endmodule : KL_aecp_notify_ref/' >"$obj/src/ref.sv"
grep -q '^module KL_aecp_notify_ref$' "$obj/src/ref.sv"
cp "$cand" "$obj/src/cand.sv"
verilator --cc --exe --build -j 2 -O3 --top-module lockstep_top \
  -GN_CTRL_P="$n" -GN_STREAM_IN_P="$nin" -GN_STREAM_OUT_P="$nout" -GEN_IDENTIFY_NOTIF_P="$ident" \
  -Wno-fatal -Wno-lint -Wno-style -Wno-MULTIDRIVEN \
  -CFLAGS "-O2 -DN_CTRL=$n" --Mdir "$obj" -o Vlockstep \
  "$obj/src/pp_pkg.sv" "$obj/src/ref.sv" "$obj/src/cand.sv" \
  "$here/lockstep_top.sv" "$here/lockstep_main.cpp" >"$obj/build.log" 2>&1
echo "built $obj/Vlockstep"
