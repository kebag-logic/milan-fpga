#!/bin/bash
# run_probes2.sh SRC: the two in-tree arms that share one campaign receipt name across two suites, run on the
# tb/srp_top applicant group alone so that their AP8 FAIL lines are kept (receipts/probe-arm-<name>-app.*)
set -u
PK=${PK:-$REVIEWS/pp216-r801-2-packet}
sed -n '/^run() {/,/^}/p' "$PK/scripts/run_probes.sh" > "$PK/scratch/run_fn.sh"
export PATH="$PK/scratch/bin:$PATH"; SRC=$1
. "$PK/scratch/run_fn.sh"
run arm-vlan-link-keeps-registrar app
run arm-vlan-link-no-begin app
echo done > $PK/receipts/probes2.done
