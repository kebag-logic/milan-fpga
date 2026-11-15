#!/bin/bash
# Round 10's gate queue for a head (lane 895): every workflow job that reads a path round 10 changed (the docs, and
# sw/firmware/ctrl/test's srp_talker.cpp and srp_talker_mutants.py), each by run_wf.py on its own fresh clean clone,
# and the lane's gates part a; one unit each, for disp_once.py. The other jobs read none of those paths and carry
# from round 9's full pass by the images' identity (round10 receipts/identity).
# usage: gate_queue.sh HEAD OUTDIR > QUEUE
set -u
H=$1 O=$2
G=$MANAGEMENT/2026-09-23/895-a775/round10/scripts/gates
W="/usr/bin/python3 $G/run_wf.py"
echo "W-fw-srp 10G mkdir -p $O; $W rtl-fast.yml $H firmware-srp-mutants $O > $O/firmware-srp-mutants.driver.log 2>&1"
echo "W-fw-unit 10G mkdir -p $O; $W rtl-fast.yml $H firmware-unit $O > $O/firmware-unit.driver.log 2>&1"
echo "W-fw-control 10G mkdir -p $O; $W rtl-fast.yml $H firmware-control-mutants $O > $O/firmware-control-mutants.driver.log 2>&1"
echo "W-fw-aecp 10G mkdir -p $O; $W rtl-fast.yml $H firmware-aecp-mutants $O > $O/firmware-aecp-mutants.driver.log 2>&1"
echo "lane-a 10G /bin/bash $G/lane_gates.sh $H a"
echo "W-docs-gates-0 10G mkdir -p $O; $W docs.yml $H docs-gates-0 $O > $O/docs-docs-gates-0.driver.log 2>&1"
echo "W-docs-gates-1 10G mkdir -p $O; $W docs.yml $H docs-gates-1 $O > $O/docs-docs-gates-1.driver.log 2>&1"
echo "W-docs-gates-2 10G mkdir -p $O; $W docs.yml $H docs-gates-2 $O > $O/docs-docs-gates-2.driver.log 2>&1"
echo "W-docs-a 10G mkdir -p $O; for j in wire-accountability docs-check-no-git docs-check; do $W docs.yml $H \$j $O > $O/docs-\$j.driver.log 2>&1; done"
echo "W-ci 10G mkdir -p $O; for j in changes bdd-conformance; do $W rtl-fast.yml $H \$j $O > $O/rtl-fast-\$j.driver.log 2>&1; done; $W rtl.yml $H full-ci-gate $O > $O/rtl-full-ci-gate.driver.log 2>&1"
