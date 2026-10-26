#!/bin/bash
# sandbox.sh CHECKOUT DEST: a probe root whose every path links to the checkout, but for a private
# copy of the harness at tb/verilator/ctrl_service_budget.orig (and a working copy beside it).
C=$1 D=$2
rm -rf "$D"; mkdir -p "$D/tb/verilator"
for e in "$C"/* "$C"/.[!.]*; do b=$(basename "$e"); [ "$b" = tb ] || [ "$b" = .git ] || ln -s "$e" "$D/$b"; done
for e in "$C"/tb/*; do b=$(basename "$e"); [ "$b" = verilator ] || ln -s "$e" "$D/tb/$b"; done
for e in "$C"/tb/verilator/*; do b=$(basename "$e"); [ "$b" = ctrl_service_budget ] || ln -s "$e" "$D/tb/verilator/$b"; done
cp -a "$C/tb/verilator/ctrl_service_budget" "$D/tb/verilator/ctrl_service_budget.orig"
cp -a "$C/tb/verilator/ctrl_service_budget" "$D/tb/verilator/ctrl_service_budget"
