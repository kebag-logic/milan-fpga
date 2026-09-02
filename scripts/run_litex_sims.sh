#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Run every standalone LiteX simulation under sw/litex/ and summarise (#297).
#
#   scripts/run_litex_sims.sh [outdir]
#   scripts/run_litex_sims.sh --list
#   scripts/run_litex_sims.sh --selftest
#
# THE POPULATION IS PINNED, NOT DISCOVERED. The INVENTORY array below names
# every supported standalone LiteX simulation; sw/litex/ is then reconciled
# against it in both directions. A name whose file is gone is a FAILURE
# (MISSING), so a deleted or renamed test cannot vanish from the evidence
# silently - the gap #297 was filed about. A test_*.py present in sw/litex/
# but absent from the inventory is a FAILURE too (UNLISTED), because "one
# command runs every supported simulation" stops being true the day a new
# test arrives that only its author knows to run.
#
# WHY THE INVENTORY IS TWO. The issue was filed against a tree where
# sw/litex/ carried twelve test_*.py scripts. Ten of them tested the
# bare-metal ring/DMA product that #259 retired; commit ecf18de2 ("Finish
# bare-metal product and fabric gPTP ownership", merged by PR #294) deleted
# them together with the RTL they proved. The two survivors are the
# protocol-processor memory-path checks the bare-metal SoC still owns. This
# aggregate covers the survivors and records that reconciliation instead of
# resurrecting deliberately retired tests.
#
# WHAT IS DELIBERATELY OUTSIDE. sw/builder/test_builder.py is the builder
# gate with its own hosted owners (docs.yml and elaborate.yml).
# sw/trace/test_trace_roundtrip.py is the "C with Python" trace layer
# (docs/guides/VERIFICATION_DEVELOPER.md draws that boundary) and imports no
# migen or litex. sw/litex/milan_sim.py is the Section-3 SoC-level boot
# simulation with its own documented command (docs/testing/TESTING.md).
#
# THE INTERPRETER. Every member imports migen + litex, which never come from
# PyPI in this tree (the pins are sw/litex/litex_pins.txt). The search
# mirrors sw/builder/test_builder.py: $MILAN_LITEX_PYTHON when set, else
# `python3` on PATH, else the venv sweep.sh puts on PATH for every real
# build - READ OUT OF sweep.sh, never restated here. A set
# $MILAN_LITEX_PYTHON that cannot import migen + litex is a REFUSAL (exit
# 91, the run_all_suites REFUSED code - [R1] on PR #330 produced the old
# exit-2 spelling colliding with "2 findings" live), never a silent
# substitution: an explicit pin names the environment the verdict is about. With no usable interpreter at all every member is a
# DECLARED SKIP and the exit says the sweep is incomplete.
#
# Exit status:
#   0        every inventory member ran and passed, nothing skipped
#   1..89    that many findings: failing scripts, MISSING inventory members,
#            UNLISTED extras, and masked verdicts (a script that exited 0
#            while its log lacks `RESULT: PASS` is a FAIL here - an
#            assertion that only logs is the false green Rule 6 exists for)
#   90       nothing failed, but some member was SKIPPED (no LiteX
#            interpreter), so a green here is NOT the full aggregate
#   91       REFUSED: a set $MILAN_LITEX_PYTHON that cannot import
#            migen + litex (an explicit pin is never silently substituted)
#   92       some member was KILLED BY THE WALL CLOCK - result UNKNOWN,
#            neither a pass nor a failure; re-run it uncontended
#   2        usage error (bad option, more than one output directory)
#
# Environment:
#   MILAN_LITEX_PYTHON   the interpreter, as an explicit pin (see above)
#   LITEX_SIM_TIMEOUT    per-script wall clock in seconds (default 900)
#
# No sweep lock, deliberately: unlike tb/verilator these simulations build
# into no shared obj_* directory - each is one migen process with no on-disk
# build state - so two concurrent runs cannot corrupt each other.
#
# --selftest proves the runner CAN go red: a sandbox tree (this script
# located relative to itself makes the copy's sandbox its root) exercises a
# green control, a planted failure, a masked verdict, a MISSING member, an
# UNLISTED extra, the declared-skip path, the explicit-pin refusal and the
# wall-clock UNKNOWN, and requires the observed exit and message each time.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SIM_DIR="$ROOT/sw/litex"

#: Every supported standalone LiteX simulation, by basename. Growing sw/litex
#: means growing this list - the UNLISTED reconciliation makes forgetting it
#: a red run, and docs/testing/TESTING.md section 2 names the rule.
INVENTORY=(
  test_pp_boot_bus_freeze
  test_pp_mem_bridge
)

TMO="${LITEX_SIM_TIMEOUT:-900}"
PROBE='import migen, litex'

probe() { "$1" -c "$PROBE" >/dev/null 2>&1; }

# The venv sweep.sh puts on PATH for every real build, derived from its own
# `export PATH="$HOME/<name>/venv/bin` line - never restated here, because a
# second spelling of the build interpreter is a second thing that has to
# stay true (the same derivation sw/builder/test_builder.py uses).
sweep_venv_python() {
  local name
  name="$(sed -n 's|^export PATH="\$HOME/\([^/"[:space:]:]*\)/venv/bin.*|\1|p' \
          "$SIM_DIR/sweep.sh" 2>/dev/null | head -n1)"
  [ -n "$name" ] && echo "$HOME/$name/venv/bin/python3"
}

# stdout: the interpreter. Return 0 found, 1 none (declared skip), 2 refused.
find_interpreter() {
  if [ -n "${MILAN_LITEX_PYTHON:-}" ]; then
    if [ -x "$MILAN_LITEX_PYTHON" ] && probe "$MILAN_LITEX_PYTHON"; then
      echo "$MILAN_LITEX_PYTHON"; return 0
    fi
    return 2
  fi
  local cand
  for cand in "$(command -v python3 || true)" "$(sweep_venv_python)"; do
    [ -n "$cand" ] && [ -x "$cand" ] && probe "$cand" && { echo "$cand"; return 0; }
  done
  return 1
}

list_inventory() {
  local t
  for t in "${INVENTORY[@]}"; do echo "sw/litex/$t.py"; done
}

run_aggregate() {
  local out="$1"
  mkdir -p "$out"
  rm -f "$out"/*.log     # a stale log from a previous run is not evidence

  local pass=0 fail=0 skip=0 tmo=0 failed="" timedout="" t f name
  declare -A pinned=()
  for t in "${INVENTORY[@]}"; do pinned[$t]=1; done

  # Reconciliation, both directions, before anything runs.
  for t in "${INVENTORY[@]}"; do
    if [ ! -f "$SIM_DIR/$t.py" ]; then
      fail=$((fail + 1)); failed="$failed $t"
      printf 'FAIL     %s   (MISSING: pinned in the inventory, no such file - a deleted\n' "$t"
      printf '         or renamed test may not vanish silently; reconcile the inventory)\n'
    fi
  done
  for f in "$SIM_DIR"/test_*.py; do
    [ -e "$f" ] || continue
    name="$(basename "$f" .py)"
    if [ -z "${pinned[$name]:-}" ]; then
      fail=$((fail + 1)); failed="$failed $name"
      printf 'FAIL     %s   (UNLISTED: present in sw/litex/ but not in the pinned\n' "$name"
      printf '         inventory - "one command runs every supported simulation" just\n'
      printf '         stopped being true; add it to INVENTORY in %s)\n' "scripts/run_litex_sims.sh"
    fi
  done

  local py="" find_rc=0
  py="$(find_interpreter)" || find_rc=$?
  if [ "$find_rc" -eq 2 ]; then
    echo "REFUSED: MILAN_LITEX_PYTHON is set to '${MILAN_LITEX_PYTHON:-}' but it" >&2
    echo "cannot import migen + litex. An explicit pin names the environment the" >&2
    echo "verdict is about, so it is never silently substituted. Point it at an" >&2
    echo "interpreter with the sw/litex/litex_pins.txt set, or unset it." >&2
    return 91
  fi

  for t in "${INVENTORY[@]}"; do
    [ -f "$SIM_DIR/$t.py" ] || continue
    if [ "$find_rc" -ne 0 ]; then
      skip=$((skip + 1))
      printf 'SKIP     %s   (declared: no interpreter here imports migen + litex;\n' "$t"
      printf '         point MILAN_LITEX_PYTHON at one, or install sw/litex/litex_pins.txt\n'
      printf '         and run scripts/ci_litex_env.py)\n'
      continue
    fi
    (cd "$SIM_DIR" && timeout -k 10 "$TMO" "$py" "$t.py") > "$out/$t.log" 2>&1
    local rc=$?
    # Rule 6: a script that PRINTS a failure (or nothing) and exits 0 is a
    # masked verdict. Both members end with an explicit `RESULT: PASS`.
    if [ "$rc" -eq 0 ] && ! grep -q '^RESULT: PASS$' "$out/$t.log"; then
      rc=93
    fi
    case $rc in
      0)   pass=$((pass + 1)); printf 'PASS     %s\n' "$t" ;;
      93)  fail=$((fail + 1)); failed="$failed $t"
           printf 'FAIL     %s   (exited 0 without `RESULT: PASS` - a masked verdict)\n' "$t" ;;
      124|137)
           tmo=$((tmo + 1)); timedout="$timedout $t"
           printf 'TIMEOUT  %s   (%ss wall clock - result UNKNOWN, not a failure)\n' \
                  "$t" "$TMO" ;;
      *)   fail=$((fail + 1)); failed="$failed $t"; printf 'FAIL     %s\n' "$t" ;;
    esac
  done

  echo "----------------------------------------------------------------"
  echo "simulations: ${#INVENTORY[@]}   passed: $pass   failed: $fail" \
       "  skipped: $skip   timed out: $tmo"
  [ -n "$failed" ] && echo "failing:$failed"
  if [ -n "$timedout" ]; then
    echo "TIMED OUT (result unknown, NOT a failure):$timedout"
  fi
  if [ "$skip" -gt 0 ] && [ "$fail" -eq 0 ]; then
    echo "INCOMPLETE: $skip declared skip(s) - this green is not the full aggregate."
  fi
  echo "logs: $out"

  [ "$fail" -gt 89 ] && return 89
  [ "$fail" -gt 0 ] && return "$fail"
  [ "$tmo" -gt 0 ] && return 92
  [ "$skip" -gt 0 ] && return 90
  return 0
}

# --- the negative controls ---------------------------------------------------

selftest() {
  local real_py
  real_py="$(command -v python3)" || { echo "selftest needs python3" >&2; return 2; }
  local checks=0 fails=0
  ck() {   # ck <name> <want_rc> <got_rc> <needle> <output>
    checks=$((checks + 1))
    if [ "$3" -eq "$2" ] && printf '%s' "$5" | grep -q "$4"; then
      printf '  [ok]   %s\n' "$1"
    else
      fails=$((fails + 1))
      printf '  [FAIL] %s: wanted exit %s + /%s/, got exit %s\n' "$1" "$2" "$4" "$3"
      printf '%s\n' "$5" | sed 's/^/         | /'
    fi
  }

  local sand
  sand="$(mktemp -d)" || return 2
  # shellcheck disable=SC2064
  trap "rm -rf '$sand'" RETURN

  # A python3 shim that passes the import probe and otherwise runs the real
  # interpreter, so the sandbox needs no LiteX; and one that fails the probe.
  mkdir -p "$sand/bin-ok" "$sand/bin-no"
  printf '#!/bin/sh\nif [ "$1" = "-c" ] && [ "$2" = "%s" ]; then exit 0; fi\nexec %s "$@"\n' \
         "$PROBE" "$real_py" > "$sand/bin-ok/python3"
  printf '#!/bin/sh\nif [ "$1" = "-c" ] && [ "$2" = "%s" ]; then exit 1; fi\nexec %s "$@"\n' \
         "$PROBE" "$real_py" > "$sand/bin-no/python3"
  chmod +x "$sand/bin-ok/python3" "$sand/bin-no/python3"

  make_tree() {   # $1 = tree root; members are trivial passers
    local t
    mkdir -p "$1/scripts" "$1/sw/litex"
    cp "$ROOT/scripts/run_litex_sims.sh" "$1/scripts/"
    printf 'export PATH="$HOME/no-such-venv-297/venv/bin:$PATH"\n' > "$1/sw/litex/sweep.sh"
    for t in "${INVENTORY[@]}"; do
      printf 'import sys\nprint("%s: 1 checks: 1 PASS, 0 FAIL")\n' "$t" > "$1/sw/litex/$t.py"
      printf 'print("RESULT: PASS")\nsys.exit(0)\n' >> "$1/sw/litex/$t.py"
    done
  }
  arm() {   # arm <tree> <shim> [env VAR=... ...] -> runs the sandbox copy
    local tree="$1" shim="$2"; shift 2
    env -u MILAN_LITEX_PYTHON "$@" PATH="$sand/$shim:$PATH" \
        "$tree/scripts/run_litex_sims.sh" "$tree/logs" 2>&1
  }

  local out rc
  make_tree "$sand/a"
  out="$(arm "$sand/a" bin-ok)"; rc=$?
  ck "green control: a sandbox where everything passes exits 0" 0 "$rc" \
     "passed: 2\b" "$out"

  make_tree "$sand/b"
  printf 'import sys\nprint("RESULT: FAIL")\nsys.exit(1)\n' \
         > "$sand/b/sw/litex/test_pp_mem_bridge.py"
  out="$(arm "$sand/b" bin-ok)"; rc=$?
  ck "a planted failing simulation turns the aggregate red, named" 1 "$rc" \
     "failing: test_pp_mem_bridge" "$out"

  make_tree "$sand/c"
  printf 'import sys\nprint("RESULT: FAIL")\nsys.exit(0)\n' \
         > "$sand/c/sw/litex/test_pp_boot_bus_freeze.py"
  out="$(arm "$sand/c" bin-ok)"; rc=$?
  ck "a script that fails but exits 0 is a FAIL (masked verdict)" 1 "$rc" \
     "masked verdict" "$out"

  make_tree "$sand/d"
  rm "$sand/d/sw/litex/test_pp_mem_bridge.py"
  out="$(arm "$sand/d" bin-ok)"; rc=$?
  ck "a deleted inventory member is a FAIL (MISSING), not a silence" 1 "$rc" \
     "MISSING" "$out"

  make_tree "$sand/e"
  printf 'import sys\nprint("RESULT: PASS")\nsys.exit(0)\n' \
         > "$sand/e/sw/litex/test_rogue.py"
  out="$(arm "$sand/e" bin-ok)"; rc=$?
  ck "a test_*.py outside the inventory is a FAIL (UNLISTED)" 1 "$rc" \
     "UNLISTED" "$out"

  make_tree "$sand/f"
  out="$(HOME="$sand" arm "$sand/f" bin-no)"; rc=$?
  ck "no usable interpreter: every member a declared skip, exit 90" 90 "$rc" \
     "SKIP" "$out"

  make_tree "$sand/g"
  out="$(arm "$sand/g" bin-ok MILAN_LITEX_PYTHON="$sand/no-such-python")"; rc=$?
  ck "an explicit MILAN_LITEX_PYTHON that cannot probe is REFUSED" 91 "$rc" \
     "REFUSED" "$out"

  make_tree "$sand/h"
  printf 'import time\ntime.sleep(30)\n' > "$sand/h/sw/litex/test_pp_mem_bridge.py"
  out="$(arm "$sand/h" bin-ok LITEX_SIM_TIMEOUT=1)"; rc=$?
  ck "a wall-clock kill is UNKNOWN (exit 92), never a pass or a failure" 92 "$rc" \
     "TIMEOUT" "$out"

  printf '\nrun_litex_sims selftest: %s checks: %s PASS, %s FAIL\n' \
         "$checks" "$((checks - fails))" "$fails"
  if [ "$fails" -gt 0 ]; then echo "RESULT: FAIL"; return 2; fi
  echo "RESULT: PASS"
  return 0
}

# --- entry -------------------------------------------------------------------

OUT=""
MODE=run
while [ "$#" -gt 0 ]; do
  case "$1" in
    --list)     MODE=list; shift ;;
    --selftest) MODE=selftest; shift ;;
    -*)         echo "unknown option: $1" >&2; exit 2 ;;
    *)
      [ -z "$OUT" ] || { echo "more than one output directory" >&2; exit 2; }
      OUT="$1"; shift ;;
  esac
done

case "$MODE" in
  list)     list_inventory ;;
  selftest) selftest ;;
  run)      run_aggregate "${OUT:-$ROOT/.litex-sim-logs}" ;;
esac
