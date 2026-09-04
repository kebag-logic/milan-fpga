#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Prove `syn/yosys/run.sh --list` depends on NOTHING but itself and
# scripts/yosys_shards.py - not a submodule, not scripts/pp_srcs.py (#190/#192).
#
# The `yosys-portability` aggregate job checks out no submodule and calls
# `run.sh --list` to learn the top NAMES; #190 was that call reaching for the
# protocol-processor source list it did not need and reddening dev. #191 fixed
# it, and its DoD deferred a durable check because nothing here could build a
# submodule-free tree. This is that check: it builds a directory holding only
# the two files --list may read and confirms it works there, then its own
# NEGATIVE CONTROL removes yosys_shards.py and requires --list to fail - so a
# dependency added to the --list path later cannot pass this in silence.
#
# Needs bash + python3 only (no yosys, no sv2v, no submodule), so it runs on any
# box and in CI. Exit 0 = the contract holds, 1 = it was broken.
#
# The full trio is safe here because every failure this check REPORTS is read
# through an `if`: the two --list invocations are conditions, and the only
# commands whose non-zero status is expected are the two `grep -c` counts,
# which are taken explicitly below. Anything else that fails - a cp into the
# scratch tree, an mkdir - is a broken harness, and a broken harness must not
# print a verdict about run.sh.
set -euo pipefail

R="$(cd "$(dirname "$0")/../.." && pwd)"
fail=0

# The real tree's inventory is the reference count. --list needs no submodule,
# so this must already succeed here.
if ! real_out="$(bash "$R/syn/yosys/run.sh" --list 2>/dev/null)"; then
  echo "check_list_hermetic: run.sh --list failed in the real tree - the"
  echo "  inventory should print without tools or submodules (#191)."
  exit 1
fi
# `grep -c` exits 1 when the count is zero, and zero is an answer this check
# is entitled to compare rather than die on, so the status is taken here.
n_real="$(printf '%s\n' "$real_out" | grep -c .)" || true

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/syn/yosys" "$tmp/scripts"
cp "$R/syn/yosys/run.sh" "$tmp/syn/yosys/run.sh"
cp "$R/scripts/yosys_shards.py" "$tmp/scripts/yosys_shards.py"

# Positive: only those two files present, no submodule dir at all.
if bare_out="$(bash "$tmp/syn/yosys/run.sh" --list 2>/dev/null)"; then
  n_bare="$(printf '%s\n' "$bare_out" | grep -c .)" || true
  if [ "$n_bare" -eq "$n_real" ]; then
    echo "check_list_hermetic: PASS positive - --list printed $n_bare top(s)"
    echo "  from a tree holding only run.sh and scripts/yosys_shards.py"
  else
    echo "check_list_hermetic: FAIL - bare --list printed $n_bare top(s), the"
    echo "  real tree $n_real; the two should agree."
    fail=1
  fi
else
  echo "check_list_hermetic: FAIL - --list could not run from a tree holding"
  echo "  only run.sh and scripts/yosys_shards.py, so it depends on more than"
  echo "  it should (a submodule, or scripts/pp_srcs.py) - the #190 defect."
  fail=1
fi

# NEGATIVE CONTROL: remove the one file --list legitimately needs and require
# a failure. Without this the positive arm could pass over a --list that needs
# nothing at all - or everything - and this check would prove neither.
rm -f "$tmp/scripts/yosys_shards.py"
if bash "$tmp/syn/yosys/run.sh" --list >/dev/null 2>&1; then
  echo "check_list_hermetic: FAIL negative-control - --list still succeeded"
  echo "  with scripts/yosys_shards.py removed, so it is not the dependency"
  echo "  this check claims to pin."
  fail=1
else
  echo "check_list_hermetic: PASS negative-control - --list fails once"
  echo "  scripts/yosys_shards.py is removed, pinning the dependency set."
fi

[ "$fail" -eq 0 ] && echo "check_list_hermetic: OK" || echo "check_list_hermetic: FAIL"
exit "$fail"
