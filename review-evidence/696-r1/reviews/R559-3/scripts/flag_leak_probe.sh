#!/bin/sh
# Inherited-flag behaviour of the nested $(shell $(MAKE) ...) captures (no build).
# Usage: flag_leak_probe.sh <disposable repo copy>
cd "$1/tb/verilator" || exit 2
make --version | head -1
out=$(MAKEFLAGS= make -n -C maap integration-build 2>&1); echo "dry run 'make -n -C maap integration-build' rc=$?"
printf '%s\n' "$out" | grep '\*\*\*' | sed "s|$1|<copy>|g"
for f in maap/integration.mk capture_coherence/Makefile milan_dp_mclk/Makefile; do
  out=$(cd "$(dirname $f)" && env MAKEFLAGS= MFLAGS= make -pqrR -f "$(basename $f)" --eval '__p: ;' __p 2>&1)
  echo "database read 'make -pqrR' of $f rc=$?"; printf '%s\n' "$out" | grep '\*\*\*' | head -1
done
echo "integration.mk names adp_shape_defaults.svh (shape-inventory consumer): $(grep -c adp_shape_defaults.svh maap/integration.mk)"
