#!/usr/bin/env bash
# Print every hierarchy row whose FF count differs between two routed hierarchy reports.
# Usage: ff_directive_diff.sh <a.rpt> <b.rpt>
ff(){ awk -F'|' 'NF>8 && $2!~/Instance/ {gsub(/ +$/,"",$2); gsub(/ /,"",$8); print NR": "$2" FF="$8}' "$1"; }
diff <(ff "$1") <(ff "$2")
