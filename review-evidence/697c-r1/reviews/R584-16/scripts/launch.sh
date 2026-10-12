#!/bin/bash
# launch.sh NAME CMD... : run CMD in the head clone with the CI-layout HOME, log + rc under scratch/logs
set -u
S=$REVIEWS/697c-r584-16-packet/scratch
name=$1; shift
cd $REVIEWS/r584-16-697c
( start=$(date +%s); HOME=$S/home TMPDIR=$S/tmp LC_ALL=C "$@" > $S/logs/$name.log 2>&1; rc=$?; end=$(date +%s); echo "rc=$rc seconds=$((end-start))" > $S/logs/$name.rc ) &
