#!/usr/bin/env bash
# Extract the route and gate figures this review cross-checked from the public
# evidence commits, so a second reader can repeat the comparison.
# usage: crosscheck_figures.sh <milan-fpga clone with both evidence commits fetched>
set -u
G=$1
E851=2dd97058243e5afc2dc91d8989970cc9049c6b5b
E843=425a829e46033442e9093825b4dbb8d69f4fab9c
A=review-evidence/851-r1/author/receipts
D=review-evidence/843-r1/author-r2/receipts/route-dev
show() { git -C "$G" show "$1:$2"; }
echo "== evidence $E851: route at the head (ExtraPostPlacementOpt)"
show $E851 $A/route-2d939d2d/RAW-RECORDS.txt | head -0
show $E851 $A/route-2d939d2d/01-clone.log | grep -E '^(head|tree) '
show $E851 $A/route-2d939d2d/utilization_place.rpt | grep -E '^\| (Slice LUTs|Slice Registers|Slice ) '
show $E851 $A/route-2d939d2d/head-2d939d2d.json | tr -d ' \n' | grep -o '"corners".*"whs_worst":[0-9.]*'; echo
show $E851 $A/route-2d939d2d/route_status.rpt | grep 'routing errors'
show $E851 $A/route-2d939d2d/worst-setup-path.txt | grep -E 'Slack|Path Group|Logic Levels'
echo "== evidence $E851: resource gate against the thirteenth record"
show $E851 $A/gate/gate-route-1x1.log
echo "rc=$(show $E851 $A/gate/gate-route-1x1.rc)"
for d in eto eppo aslh; do
  echo "-- $d post-route utilisation"
  show $E851 $A/gate/$d/$d-baseline_utilization.rpt | grep -E '^\| (Slice LUTs|Slice ) '
done
show $E851 $A/gate/after-route-1x1.log | tail -1
show $E851 $A/gate/check-baseline-after.log
echo "== evidence $E843: dev 1eb5289d route on the same recipe"
show $E843 $D/chain.log | head -1
show $E843 $D/eto-baseline_utilization.rpt | grep -E '^\| (Slice LUTs|Slice Registers|Slice ) '
show $E843 $D/gate-check.log | sed -n 1,8p
