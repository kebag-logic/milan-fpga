#!/bin/bash
# rxmon.sh CLONE: the receive monitor's suite (#947 adds its LCTX format contract, sim_ctxfmt and its mutants): make run.
. <scratch>/bin/env.sh
cd "$1/tb/verilator/avtp_rxmon" || exit 2
echo "HEAD $(git rev-parse --short=8 HEAD) start $(date +%T)"
make -j8 run; rc=$?
echo "END rc=$rc $(date +%T)"; exit $rc
