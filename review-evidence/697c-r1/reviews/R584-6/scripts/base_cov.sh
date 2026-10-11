#!/bin/bash
# Coverage check at the base checkout with its own reader and ratchet. Usage: base_cov.sh <packet-root> <base-checkout>
set -u; P=$1; cd "$2"; source $P/scripts/env.sh
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 > $P/logs/base_cov.log 2>&1; echo $? > $P/logs/base_cov.rc
