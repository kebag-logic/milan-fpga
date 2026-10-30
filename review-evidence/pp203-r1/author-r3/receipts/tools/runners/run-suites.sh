#!/usr/bin/env bash
export PATH=<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TMPDIR=<runs>/tmp
export MAKEFLAGS=-j16
rm -f <runs>/gates/req-tags.txt
mkdir -p <runs>/gates
REQ_TAG_LOG=<runs>/gates/req-tags.txt <tools>/gate.sh <runs>/gates run_suites <work> bash scripts/run_suites.sh
touch <runs>/gates/run_suites.done
