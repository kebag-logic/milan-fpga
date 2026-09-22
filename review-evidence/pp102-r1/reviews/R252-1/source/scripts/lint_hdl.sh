#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Verilator --lint-only over every module under hdl/, each elaborated as a top
# WITH the whole tree visible (hierarchical modules need their children).
# ZERO tolerance — greenfield; a waiver is a justified lint_off pragma in RTL.

# Strict mode, with every status this script EXPECTS to be non-zero marked
# where it is read. One of them is subtle: the verdict `grep`s take $out from a
# HERE-STRING, not a pipe, because under `pipefail` a `grep -q` that matches
# early closes the pipe, the `echo` feeding it dies of SIGPIPE, and the
# pipeline reports non-zero - so `elif echo "$out" | grep -q ...` would report
# `LINT OK` for a module that DID warn. A here-string has no such inversion.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1   # every path below is relative to the repo root

# THE VERDICT IS THE TOOL'S EXIT STATUS, NOT THE ABSENCE OF A STRING IN ITS
# OUTPUT. This script used to decide PASS by grepping verilator's combined
# output for `%Warning`/`%Error` and nothing else - so a verilator that was
# absent, unrunnable or crashing produced no such line, and the script printed
# `LINT OK` for every one of the forty modules and exited 0. Reproduced by
# putting a program that always fails on PATH as `verilator`: forty OK lines,
# exit 0, lint never ran. A gate whose tool is missing must refuse, not pass.
command -v verilator >/dev/null 2>&1 || {
  echo "REFUSED: verilator is not on PATH, so nothing was linted. This is not a pass." >&2
  exit 2
}

pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
rc=0
# $all and $pkgs are find's newline-separated lists, and the split into one
# word per file is what verilator is being handed.
for f in $all; do  # shellcheck disable=SC2086 # deliberate word split of the file list
  # A .sv file that declares no module (a bare interface, a header) is skipped
  # on the next line; `grep` finding nothing there is expected, so `pipefail`
  # must not end the lint at it.
  top=$(grep -oEm1 '^\s*module\s+\w+' "$f" | awk '{print $2}') || top=""
  [ -n "$top" ] || continue
  if ! out=$(verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
             -Wno-UNUSEDPARAM --top-module "$top" $pkgs $all 2>&1); then  # shellcheck disable=SC2086 # deliberate: the whole tree is passed as one argument per file
    # verilator itself failed. Not the same thing as a lint finding, and not
    # a pass either: say which it is.
    echo "LINT ERROR $top ($f): verilator exited non-zero"
    echo "$out" | tail -5
    rc=1
  elif grep -qE '%(Warning|Error)' <<<"$out"; then
    echo "LINT FAIL $top ($f)"
    # The verdict is already taken; `head` closing this pipe early is expected.
    grep -E '%(Warning|Error)' <<<"$out" | head -5 || true
    rc=1
  else
    echo "LINT OK  $top"
  fi
done
exit "$rc"
