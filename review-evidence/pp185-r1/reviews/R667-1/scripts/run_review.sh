#!/usr/bin/env bash
# The reviewer's executions, in the order run. Portable: set PKT (this packet),
# CLONE (a clone of the processor at the exact head) and VERILATOR (a Verilator
# 5.050). Every build and probe runs in a disposable export under
# $PKT/scratch; the clone is only read.
set -euo pipefail
HEAD=b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
CLONE=${CLONE:?set CLONE to the processor clone}
VERILATOR=${VERILATOR:?set VERILATOR to a Verilator 5.050}
S=$PKT/scratch; L=$PKT/scripts/launch.sh; W=$PKT/scripts/wait_rc.sh
mkdir -p "$S/bin" "$S/tmp" "$S/src" "$S/out" "$PKT/receipts"
ln -sf "$VERILATOR" "$S/bin/verilator"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$S/src"
(cd "$S/src" && git init -q && git add -A && git -c user.name=r -c user.email=r@r commit -qm head)
test "$(git -C "$S/src" rev-parse 'HEAD^{tree}')" = 6ecc64cb8c3434106e71bbb191aebe9a0249db1e

# wave A: the four affected suites and the light gates, concurrently
$L suite-ucpu "$S/src/tb/ucpu" make
$L suite-aecp_notify "$S/src/tb/aecp_notify" make
$L suite-aecp_cmds "$S/src/tb/aecp_cmds" make
$L suite-pp_top "$S/src/tb/pp_top" make
$L gate-upcmap "$S/src" python3 scripts/check_upc_map.py
$L gate-m9 "$S/src" bash -c 'python3 scripts/check_m9_opcodes.py --selftest && python3 scripts/check_m9_opcodes.py'
$L gate-matrix "$S/src" python3 scripts/gen_matrix.py --check
MAXS=3000 $W suite-ucpu suite-aecp_notify suite-aecp_cmds suite-pp_top gate-upcmap gate-m9 gate-matrix

# the issue's mutation controls: the 16 lock-flag controls and #181's 11 occupancy controls
NOTIFY_ARMS="lock_unlock_notifies_flags_zero lock_auto_unlock_flags_zero lock_notification_flags_zero
lock_flags_unlock_bit_only lock_timeout_keeps_flags lock_timeout_flags_zero lock_flags_from_exclusion
lock_job_arguments_dropped lock_job_r14_unpacked lock_notification_not_sent lock_response_flags_zero
lock_coalesced_timeout_keeps_flags lock_coalesced_timeout_flags_zero lock_take_keeps_old_flags
lock_release_keeps_old_flags register_refused occupancy_pop_keeps_set occupancy_push_unseen
occupancy_pop_one_late occupancy_cleared_beside_push occupancy_not_busy occupancy_reset_set
occupancy_reset_set_identify occupancy_reset_set_interfaces occupancy_reset_set_collision
occupancy_reset_set_failure occupancy_pop_clears"
# shellcheck disable=SC2086
$L camp-notify "$S/src" python3 tb/pp_top/notify_mutants.py --output "$S/out/notify" \
  --verilator "$S/bin/verilator" --jobs 4 --only $NOTIFY_ARMS
MAXS=3000 $W camp-notify
$L camp-dispatch "$S/src" python3 tb/pp_top/aecp_dispatch_mutants.py --output "$S/out/dispatch" \
  --verilator "$S/bin/verilator" --jobs 3 --only rdc-base-no-overlay,rdc-unset-image,rdc-voffset-guard-nop,rdc-vtype-int16,rdc-vtype-uint8-only,rdc-short-floor-111,rdc-unit-shift-8,rdc-ident-reset-255,rdc-sctrl-no-write,lk-sctrl-lock-nop,rd-tail-uncut,rd-str-short-guard-nop
MAXS=3000 $W camp-dispatch
cp "$S/out/notify/results.json" "$PKT/receipts/camp-notify-results.json"
cp "$S/out/dispatch/results.json" "$PKT/receipts/camp-dispatch-results.json"

# reviewer probes, each on its own export
for v in tail missnop vendor; do
  rm -rf "$S/probe-$v"; mkdir -p "$S/probe-$v"
  git -C "$S/src" archive HEAD | tar -x -C "$S/probe-$v"
  python3 -I "$PKT/scripts/probe_rdc.py" "$S/probe-$v" "$v"
  $L "probe-$v" "$S/probe-$v/tb/pp_top" make aecp-dispatch
done
rm -rf "$S/probe-mr"; mkdir -p "$S/probe-mr"
git -C "$S/src" archive HEAD | tar -x -C "$S/probe-mr"
python3 -I "$PKT/scripts/probe_midround.py" "$S/probe-mr"
$L probe-midround "$S/probe-mr/tb/aecp_notify" make
MAXS=3000 $W probe-tail probe-missnop probe-vendor probe-midround

# lint and documentation gates at the head
$L gate-lint "$S/src" ./scripts/lint_hdl.sh
$L gate-makecheck "$S/src" make check
MAXS=600 $W gate-lint gate-makecheck
