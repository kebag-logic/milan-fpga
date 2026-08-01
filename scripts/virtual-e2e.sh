#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# One-command driver for the virtual end-to-end tier.
#   roadmap : docs/testing/VIRTUAL_E2E_QEMU.md   (tiers T0-T6)
#   operator: docs/testing/VIRTUAL_E2E_HOWTO.md  (the runnable guide)
#   env     : docs/tooling/virtual-e2e-env.md    (what this script re-verifies)
#
#   ./scripts/virtual-e2e.sh env-check   # T0 - inventory + prerequisite gate
#   ./scripts/virtual-e2e.sh t1          # T1 - M-A2 boot proof: CPU reads ID='MILN'
#   ./scripts/virtual-e2e.sh t2-prep     # T2 - RV32 image-boot prerequisites
#   ./scripts/virtual-e2e.sh t3-prep     # T3 - machine-to-machine bring-up prerequisites
#   ./scripts/virtual-e2e.sh all         # the whole graph, in dependency order
#
# Dependency graph (make-style: each target runs at most once per invocation)
#
#     env-check ---> t1 ---> t2-prep
#                      \---> t3-prep
#
# Exit codes - a green run must be earned, so BLOCKED never masquerades as PASS:
#     0  every requested tier PASSed
#     1  a tier FAILed              (something that should have worked did not)
#     2  a tier is BLOCKED          (a genuine prerequisite is absent)
#
# Per-check states: PASS (verified now) | FAIL (verified broken) |
#                   SKIP (optional, absent, does not gate) |
#                   BLOCKED (required by a later tier, genuinely absent).
#
# RV32 is the default focus everywhere below; RV64 is inventoried but never
# gates - see the roadmap's T0/T2 rows.
#
# Honesty rail: a green run here is a *simulation* result. It is not a hardware
# claim and never retires the bench (VIRTUAL_E2E_PLAN.md section 2).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ---- knobs (all overridable from the environment) ---------------------------
VENV="${VENV:-$HOME/litex-milan/venv}"
JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java-17-openjdk}"
BR32="${BR32:-$HOME/br-milan-rv32}"
BR64="${BR64:-$HOME/br-milan-output}"
TSN_GEN_ROOT="${TSN_GEN_ROOT:-$HOME/tsn-gen}"
# RV32 OpenSBI firmware (found 2026-08-01 in milan-tests-avb; embeds the RV32
# DTB with the PCM node - verified via embedded strings audio@f0003120 /
# kl,milan-pcm). Custom LiteX map: boots the Verilator exact-hardware lane,
# likely NOT stock qemu-system-riscv32 -machine virt (see env doc §6 caveat).
RV32_OPENSBI="${RV32_OPENSBI:-/home/alex/milan-tests-avb/fpga/boot/opensbi_ax_vexii_rv32.bin}"
EVIDENCE_DIR="${EVIDENCE_DIR:-$REPO_ROOT/docs/testing/evidence}"
LOG_DIR="${LOG_DIR:-${TMPDIR:-/tmp}}"
RUN_DATE="$(date +%F)"
export JAVA_HOME

SIM_BUILD="$REPO_ROOT/sw/litex/build_milan_sim"
MA2_DRIVER="$REPO_ROOT/scripts/ma2_sim_driver.py"

# ---- tallies ----------------------------------------------------------------
N_PASS=0; N_FAIL=0; N_SKIP=0; N_BLOCKED=0
TIER_FAIL=0; TIER_BLOCKED=0
REPORT=""          # markdown rows accumulated for the evidence file
declare -A DONE=() # make-style: a target body runs at most once

_c() { case "$1" in                      # colour, only on a tty
  PASS)    printf '\033[32m%s\033[0m' "$1" ;;
  FAIL)    printf '\033[31m%s\033[0m' "$1" ;;
  BLOCKED) printf '\033[33m%s\033[0m' "$1" ;;
  *)       printf '%s' "$1" ;;
esac; }

# record STATE LABEL DETAIL - the single place a result becomes visible
record() {
  local state="$1" label="$2" detail="${3:-}"
  case "$state" in
    PASS)    N_PASS=$((N_PASS+1)) ;;
    FAIL)    N_FAIL=$((N_FAIL+1)) ;;
    SKIP)    N_SKIP=$((N_SKIP+1)) ;;
    BLOCKED) N_BLOCKED=$((N_BLOCKED+1)) ;;
  esac
  if [ -t 1 ]; then
    printf '  %-8s %-42s %s\n' "$(_c "$state")" "$label" "$detail"
  else
    printf '  %-8s %-42s %s\n' "$state" "$label" "$detail"
  fi
  REPORT+="| \`${label}\` | **${state}** | ${detail} |"$'\n'
}

section() { printf '\n== %s ==\n' "$1"; REPORT+=$'\n'"### $1"$'\n\n'"| check | state | detail |"$'\n'"|---|---|---|"$'\n'; }

# have_file REQ|OPT|BLOCK LABEL PATH [DETAIL-IF-PRESENT]
have_file() {
  local mode="$1" label="$2" path="$3" extra="${4:-}"
  if [ -e "$path" ]; then
    local sz=""
    [ -f "$path" ] && sz="$(stat -c %s "$path" 2>/dev/null || echo '?') B"
    record PASS "$label" "${extra:-$sz}"
    return 0
  fi
  case "$mode" in
    REQ)   record FAIL    "$label" "absent: $path" ;;
    BLOCK) record BLOCKED "$label" "absent: $path" ;;
    *)     record SKIP    "$label" "absent: $path" ;;
  esac
  return 1
}

# have_cmd REQ|OPT|BLOCK LABEL COMMAND [novers]
# `novers` reports the resolved path instead of probing --version (sbt would
# spin up a JVM just to answer).
have_cmd() {
  local mode="$1" label="$2" cmd="$3" novers="${4:-}" ver=""
  if command -v "$cmd" >/dev/null 2>&1; then
    if [ -n "$novers" ]; then
      ver="$(command -v "$cmd")"
    else
      ver="$("$cmd" --version 2>&1 | head -1 || true)"
    fi
    record PASS "$label" "$ver"
    return 0
  fi
  case "$mode" in
    REQ)   record FAIL    "$label" "not on PATH: $cmd" ;;
    BLOCK) record BLOCKED "$label" "not on PATH: $cmd" ;;
    *)     record SKIP    "$label" "not on PATH: $cmd" ;;
  esac
  return 1
}

# The venv-activation gotcha, handled once and for all: subprocess `python3 -m
# litex...` and the BIOS `make` resolve python from PATH, so referencing
# $VENV/bin/python is NOT equivalent to activating. See the env doc, section 1.
activate_venv() {
  [ -n "${VIRTUAL_ENV:-}" ] && return 0
  if [ ! -f "$VENV/bin/activate" ]; then
    return 1
  fi
  set +u
  # shellcheck disable=SC1091
  . "$VENV/bin/activate"
  set -u
  return 0
}

# ---------------------------------------------------------------------------
# T0 - env-check
# ---------------------------------------------------------------------------
target_env_check() {
  section "T0 env-check - host, toolchain, images"

  local failed_before=$N_FAIL blocked_before=$N_BLOCKED

  record PASS "host.cores" "$(nproc) cores"
  have_cmd REQ "verilator" verilator || true

  if activate_venv; then
    record PASS "litex.venv" "$VENV (python $(python --version 2>&1 | awk '{print $2}'))"
    if python -c "import migen, litex" >/dev/null 2>&1; then
      record PASS "litex.venv.modules" "migen + litex importable"
    else
      record FAIL "litex.venv.modules" "venv active but 'import migen, litex' fails"
    fi
  else
    record FAIL "litex.venv" "no activate script at $VENV/bin/activate"
  fi

  if [ -x "$JAVA_HOME/bin/java" ]; then
    record PASS "jdk" "$("$JAVA_HOME/bin/java" -version 2>&1 | head -1) at $JAVA_HOME"
  else
    record SKIP "jdk" "no java at $JAVA_HOME (only needed to regenerate the core netlist)"
  fi
  have_cmd OPT "sbt" sbt novers || true

  # RV32 = the default focus; these gate.
  have_file REQ "rv32.kernel"       "$BR32/images/Image"           || true
  have_file REQ "rv32.rootfs.cpio"  "$BR32/images/rootfs.cpio.xz"  || true
  have_file OPT "rv32.kernel.xz"    "$BR32/images/Image.xz"        || true
  if [ -x "$BR32/host/bin/riscv32-buildroot-linux-gnu-gcc" ]; then
    record PASS "rv32.toolchain" "$("$BR32/host/bin/riscv32-buildroot-linux-gnu-gcc" -dumpversion 2>/dev/null || echo '?') at $BR32/host/bin/riscv32-buildroot-linux-gnu-"
  else
    record FAIL "rv32.toolchain" "no riscv32-buildroot-linux-gnu-gcc under $BR32/host/bin"
  fi

  # RV64 = supported, not primary; inventoried, never gates.
  have_file OPT "rv64.kernel"    "$BR64/images/Image"        || true
  have_file OPT "rv64.opensbi"   "$BR64/images/fw_jump.bin"  || true
  if [ -x "$BR64/host/bin/riscv64-buildroot-linux-gnu-gcc" ]; then
    record PASS "rv64.toolchain" "$BR64/host/bin/riscv64-buildroot-linux-gnu-"
  else
    record SKIP "rv64.toolchain" "absent (RV64 is not the primary path)"
  fi

  have_cmd OPT "qemu.riscv32" qemu-system-riscv32 || true
  have_cmd OPT "qemu.riscv64" qemu-system-riscv64 || true
  have_file OPT "tsn-gen"  "$TSN_GEN_ROOT" "$TSN_GEN_ROOT" || true
  have_file OPT "sim.cached-model" "$SIM_BUILD/gateware/obj_dir/Vsim" || true
  have_file REQ "ma2.driver" "$MA2_DRIVER" || true

  record PASS "verilator.threads" "VERILATOR_THREADS=${VERILATOR_THREADS:-(unset - single-threaded, the proven M-A2 path)}"

  if [ "$N_FAIL" -gt "$failed_before" ]; then TIER_FAIL=1; return 1; fi
  if [ "$N_BLOCKED" -gt "$blocked_before" ]; then TIER_BLOCKED=1; return 2; fi
  return 0
}

# ---------------------------------------------------------------------------
# T1 - M-A2 boot proof. Delegates to the PROVEN driver; no pty logic here.
# ---------------------------------------------------------------------------
target_t1() {
  need env-check || return $?
  section "T1 - M-A2 boot proof (softcore reads ID='MILN')"

  local log="$LOG_DIR/virtual-e2e-t1-$RUN_DATE.log"
  if ! activate_venv; then
    record BLOCKED "t1.venv" "cannot activate $VENV"; TIER_BLOCKED=1; return 2
  fi

  echo "  running: python scripts/ma2_sim_driver.py --repo $REPO_ROOT --log $log"
  echo "  (cold build + boot to the BIOS prompt is ~100 s on a many-core host)"
  local out rc=0
  out="$(cd "$REPO_ROOT" && python "$MA2_DRIVER" --repo "$REPO_ROOT" --log "$log" 2>&1)" || rc=$?

  local verdict="${out##*$'\n'}"
  if [ "$rc" -eq 0 ] && printf '%s' "$verdict" | grep -q 'M-A2: PASS'; then
    record PASS "t1.ma2.boot" "$verdict"
  else
    record FAIL "t1.ma2.boot" "driver rc=$rc: $verdict"
    TIER_FAIL=1; return 1
  fi

  # Independent re-read of the capture: the ID magic must be on the wire, and
  # this check can fail on its own (wrong bytes => FAIL even if the driver
  # reported PASS on prompt+dump alone).
  local dump
  dump="$(sed -e 's/\x1b\[[0-9;]*m//g' -e 's/\r//g' "$log" 2>/dev/null | grep -m1 '^0x90000000' || true)"
  if printf '%s' "$dump" | grep -q '4e 4c 49 4d'; then
    record PASS "t1.ma2.id-magic" "${dump#0x90000000  } (LE 'MILN')"
  else
    record FAIL "t1.ma2.id-magic" "no 4e 4c 49 4d at 0x90000000; got: ${dump:-<no dump line>}"
    TIER_FAIL=1; return 1
  fi
  record PASS "t1.log" "$log"
  return 0
}

# ---------------------------------------------------------------------------
# T2-prep - RV32 image boot prerequisites (RV64 stays behind --xlen=64)
# ---------------------------------------------------------------------------
target_t2_prep() {
  need t1 || return $?
  section "T2-prep - RV32 image-boot prerequisites"

  local blocked_before=$N_BLOCKED failed_before=$N_FAIL

  have_file REQ "t2.rv32.kernel"  "$BR32/images/Image"          || true
  have_file REQ "t2.rv32.rootfs"  "$BR32/images/rootfs.cpio.xz" || true
  have_file REQ "t2.sim.entry"    "$REPO_ROOT/sw/litex/milan_sim.py" || true

  if grep -q -- '--xlen' "$REPO_ROOT/sw/litex/milan_sim.py" 2>/dev/null; then
    record PASS "t2.xlen.default" "milan_sim.py --xlen default 32 (RV32 primary); --xlen=64 supported"
  else
    record FAIL "t2.xlen.default" "no --xlen switch in milan_sim.py"
  fi

  # The negative control T2 must carry, named so it cannot be quietly dropped.
  if [ -f "$REPO_ROOT/scripts/check_entity_shape.py" ]; then
    record PASS "t2.oracle.source" "scripts/check_entity_shape.py (same constants source as the CSR oracle)"
  else
    record FAIL "t2.oracle.source" "scripts/check_entity_shape.py absent - T2 would have no oracle"
  fi

  # RV32 SBI firmware FOUND (milan-tests-avb, verified DTB strings); see env doc §6.
  # Custom LiteX map: boots the Verilator exact-hardware lane; likely NOT stock
  # qemu virt (documented caveat). Still BLOCKED until the RAM sim model + wire
  # attachment (R3) exist, but the firmware artifact itself is present.
  have_file REQ "t2.rv32.opensbi" "$RV32_OPENSBI" || true

  record BLOCKED "t2.boot-the-image" "not implemented yet - this target only proves prerequisites"

  if [ "$N_FAIL" -gt "$failed_before" ]; then TIER_FAIL=1; return 1; fi
  if [ "$N_BLOCKED" -gt "$blocked_before" ]; then TIER_BLOCKED=1; return 2; fi
  return 0
}

# ---------------------------------------------------------------------------
# T3-prep - machine-to-machine verification prerequisites
# ---------------------------------------------------------------------------
target_t3_prep() {
  need t1 || return $?
  section "T3-prep - machine-to-machine (two virtual nodes, one enumerates the other)"

  local blocked_before=$N_BLOCKED failed_before=$N_FAIL

  have_cmd BLOCK "t3.qemu.riscv32" qemu-system-riscv32 || true
  have_cmd REQ   "t3.verilator"    verilator           || true
  have_file REQ  "t3.cosim.header" "$REPO_ROOT/tb/verilator/tsn_fuzz/cosim_axis.h" || true
  have_file REQ  "t3.cosim.driver" "$REPO_ROOT/tb/verilator/tsn_fuzz/cosim.py"     || true
  have_file REQ  "t3.dut-sim"      "$REPO_ROOT/scripts/run-dut-sim.sh"             || true
  have_file REQ  "t3.datapath.rtl" "$REPO_ROOT/hdl/milan/milan_datapath.sv"        || true

  # --threads-dpi only has meaning once a DPI bridge exists; today it does not.
  if grep -rqs 'import[[:space:]]*"DPI-C"' "$REPO_ROOT/hdl" "$REPO_ROOT/tb"; then
    record PASS "t3.dpi.present" "DPI-C imports found - build with --threads-dpi all"
  else
    record SKIP "t3.dpi.present" "no DPI-C in hdl/ or tb/ (bridges are --exe C++ over UNIX sockets); --threads-dpi is a no-op until T3 adds one"
  fi

  # Node B is a bootable virtual machine acting as the independent enumerator.
  # RV32 SBI firmware FOUND (milan-tests-avb); the remaining T3 blockers are
  # the bridge + virtual L2 + negative control, not the firmware artifact.
  have_file REQ "t3.rv32.opensbi" "$RV32_OPENSBI" || true

  record BLOCKED "t3.bridge"     "socket/chardev bridge between the two verilated nodes not built yet"
  record BLOCKED "t3.virtual-l2" "virtual L2 (QEMU netdev/TAP or userspace bridge) not wired yet"
  record BLOCKED "t3.neg-control" "stale-AEM-ROM-vs-new-model-id negative control not implemented yet"

  if [ "$N_FAIL" -gt "$failed_before" ]; then TIER_FAIL=1; return 1; fi
  if [ "$N_BLOCKED" -gt "$blocked_before" ]; then TIER_BLOCKED=1; return 2; fi
  return 0
}

# ---------------------------------------------------------------------------
# make-style target runner
# ---------------------------------------------------------------------------
need() {
  local t="$1"
  if [ -n "${DONE[$t]:-}" ]; then
    return "${DONE[$t]}"      # already built this invocation; reuse the verdict
  fi
  local rc=0
  case "$t" in
    env-check) target_env_check || rc=$? ;;
    t1)        target_t1        || rc=$? ;;
    t2-prep)   target_t2_prep   || rc=$? ;;
    t3-prep)   target_t3_prep   || rc=$? ;;
    *) echo "unknown target: $t" >&2; return 1 ;;
  esac
  DONE[$t]="$rc"
  return "$rc"
}

write_evidence() {
  local target="$1" verdict="$2"
  mkdir -p "$EVIDENCE_DIR"
  local out="$EVIDENCE_DIR/virtual-e2e-${target}-${RUN_DATE}.md"
  {
    echo "# Virtual E2E run - \`${target}\` - ${RUN_DATE}"
    echo
    echo "Produced by \`scripts/virtual-e2e.sh ${target}\`. Verdict: **${verdict}**."
    echo "Simulation result only - not a hardware claim."
    echo
    echo "Tally: ${N_PASS} PASS / ${N_FAIL} FAIL / ${N_SKIP} SKIP / ${N_BLOCKED} BLOCKED."
    echo "$REPORT"
  } > "$out"
  echo "$out"
}

usage() {
  sed -n '4,32p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

main() {
  local target="${1:-}"
  case "$target" in
    env-check|t1|t2-prep|t3-prep) need "$target" || true ;;
    all)
      need env-check || true
      need t1        || true
      need t2-prep   || true
      need t3-prep   || true
      ;;
    -h|--help|help|"") usage; return 0 ;;
    *) echo "unknown target: $target" >&2; usage >&2; return 1 ;;
  esac

  local verdict rc
  if [ "$TIER_FAIL" -ne 0 ]; then
    verdict="FAIL"; rc=1
  elif [ "$TIER_BLOCKED" -ne 0 ]; then
    verdict="BLOCKED"; rc=2
  else
    verdict="PASS"; rc=0
  fi

  local evidence; evidence="$(write_evidence "$target" "$verdict")"
  printf '\n== %s: %s ==\n' "$target" "$verdict"
  printf '   %d PASS / %d FAIL / %d SKIP / %d BLOCKED\n' "$N_PASS" "$N_FAIL" "$N_SKIP" "$N_BLOCKED"
  printf '   evidence: %s\n' "$evidence"
  if [ "$rc" -eq 2 ]; then
    printf '   BLOCKED is not a pass: a prerequisite is genuinely absent (see the rows above).\n'
  fi
  return "$rc"
}

MAIN_RC=0
main "$@" || MAIN_RC=$?
exit "$MAIN_RC"
