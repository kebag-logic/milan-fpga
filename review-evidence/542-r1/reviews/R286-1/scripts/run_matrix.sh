#!/usr/bin/env bash
# R286-1 reproduction driver for PR #550 / issue #542 at 68117c0bec0b767d38d9bb1150542e2346b615b7.
# Every build happens in a disposable clone under $PKT/scratch/head; the review
# clone is only read. Run each stage in the foreground; at most 8 compile jobs.
#   REPO : a clone at the exact head with protocol-processor, gptp-processor and
#          third_party/verilog-axis initialised at their gitlinks
#   PKT  : this packet directory
#   V    : Verilator 5.050 (`verilator --version` -> "Verilator 5.050 2026-07-01 rev v5.050")
# usage: run_matrix.sh prep | notify | nxn | legs | asan | nxnasan
set -eu
: "${REPO:?}" "${PKT:?}" "${V:?}"
HEAD_SHA=68117c0bec0b767d38d9bb1150542e2346b615b7
H=$PKT/scratch/head
export TB=$H/tb/verilator/milan_dp RCPT=$PKT/receipts VERILATOR=$V VJOBS=8
mkdir -p "$RCPT"
case "${1:-}" in
prep)
  rm -rf "$H"; git clone -q --no-checkout "$REPO" "$H"
  git -C "$H" checkout -q --detach "$HEAD_SHA"
  for m in protocol-processor gptp-processor third_party/verilog-axis; do
    git -C "$H" config "submodule.$m.url" "$REPO/$m"; done
  git -C "$H" -c protocol.file.allow=always submodule update --init \
      protocol-processor gptp-processor third_party/verilog-axis
  (cd "$TB" && make VERILATOR="$V" ltn_rom.hex ucode.hex gptp_ucode.hex \
      gen_divergent/gen/adp_shape_defaults.svh)
  # base source (615b5a5d), the head with the fix reverse-applied (old checks,
  # final lever), and the disposable mutants
  git -C "$H" show 615b5a5d7de01b23f15502e3732c6f2cb81ce74b:tb/verilator/milan_dp/sim_nxn.cpp > "$TB/sim_nxn_base.cpp"
  git -C "$H" diff 766b6a149 6c5fa5566 -- tb/verilator/milan_dp/sim_nxn.cpp | git -C "$H" apply -R
  cp "$TB/sim_nxn.cpp" "$TB/sim_nxn_oldchk.cpp"
  git -C "$H" checkout -- tb/verilator/milan_dp/sim_nxn.cpp
  python3 "$PKT/scripts/make_mutants.py" "$TB" ;;
notify)
  . "$PKT/scripts/probe_lib.sh"
  variant notify plain sim_nxn.cpp ""
  variant notify base sim_nxn_base.cpp ""
  variant notify lever sim_nxn.cpp "$LEVER"
  variant notify oldlever sim_nxn_oldchk.cpp "$LEVER"
  variant notify oldplain sim_nxn_oldchk.cpp ""
  variant notify nolever sim_nxn_mut_nolever.cpp "$LEVER"
  variant notify drainhold sim_nxn_mut_drainhold.cpp "$LEVER"
  variant notify drainholdplain sim_nxn_mut_drainhold.cpp "" ;;
nxn)
  . "$PKT/scripts/probe_lib.sh"
  variant nxn plain sim_nxn.cpp ""
  variant nxn base sim_nxn_base.cpp ""
  variant nxn lever sim_nxn.cpp "$LEVER"
  variant nxn oldlever sim_nxn_oldchk.cpp "$LEVER" ;;
legs)
  . "$PKT/scripts/probe_lib.sh"
  for l in nxn8 nxn4c nxndv; do
    variant $l plain sim_nxn.cpp ""; variant $l base sim_nxn_base.cpp ""
    variant $l lever sim_nxn.cpp "$LEVER"; done
  variant sim plain sim_nxn.cpp "" ;;
asan)   # about 4 minutes per build
  . "$PKT/scripts/probe_lib.sh"
  variant notify asan sim_nxn.cpp "$LEVER $ASAN"
  variant notify oldasan sim_nxn_oldchk.cpp "$LEVER $ASAN"
  variant notify baseasan sim_nxn_base.cpp "$ASAN"
  variant notify drainasan sim_nxn_mut_drainhold.cpp "$LEVER $ASAN"
  variant notify absentasan sim_nxn_mut_absent.cpp "$ASAN" ;;
nxnasan)
  . "$PKT/scripts/probe_lib.sh"
  variant nxn leverasan sim_nxn.cpp "$LEVER $ASAN" ;;
*) echo "usage: $0 prep|notify|nxn|legs|asan|nxnasan" >&2; exit 2 ;;
esac
