#!/usr/bin/env bash
# S3 probe: pp_shadow's nested-derivation status assertion.
# Run from a disposable copy of the reviewed tree. Arg 1: GNU Make 4.3 bin dir.
# For each make version: the real Makefile accepts the clean derivation and
# refuses MAKE=false; with the three assertion lines deleted, MAKE=false must
# be silently accepted (rc 0), which proves the control can fail.
set -u
M43=$1
mk="tb/verilator/pp_shadow/Makefile"
probe() {  # $1 make binary, rest extra args
  local m=$1; shift
  "$m" -s --no-print-directory -C tb/verilator/pp_shadow \
    --eval '.PHONY: shape-nested-probe' --eval 'shape-nested-probe:;' shape-nested-probe "$@" 2>&1
  echo "rc=$?"
}
for m in /usr/bin/make "$M43/make"; do
  echo "== $("$m" --version | head -1)"
  echo "-- real Makefile, clean derivation";  probe "$m"
  echo "-- real Makefile, MAKE=false";        probe "$m" MAKE=false
done
cp "$mk" "$mk.orig"
python3 - "$mk" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
block = ("ifneq ($(.SHELLSTATUS),0)\n$(error ../milan_dp print-srcs failed; "
         "the datapath source list could not be derived)\nendif\n")
assert t.count(block) == 1, "assertion block not found exactly once"
p.write_text(t.replace(block, ""))
PY
for m in /usr/bin/make "$M43/make"; do
  echo "== MUTANT (assertion deleted) $("$m" --version | head -1)"
  echo "-- MAKE=false";  probe "$m" MAKE=false
done
mv "$mk.orig" "$mk"
git diff --exit-code -- "$mk" && echo "restored: $mk matches HEAD"
