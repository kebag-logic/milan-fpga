#!/bin/bash
# chainW: rtl-fast's wire-timing job (its step: run.py --ci, a fresh 1x1 build) on its own fresh clone of the gate head
G=<scratch>/gates4; export CPUS=64-67
$G/wf_jobs.sh rtl-fast $G/rtl-fast wire-timing:litex
echo done > $G/chainW.done
