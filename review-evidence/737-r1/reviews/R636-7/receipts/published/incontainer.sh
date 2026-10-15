#!/bin/bash
# usage: incontainer.sh <name> <logfile> <shell command>
# Runs in the hosted-runner-like image with the pinned CPython 3.12.3 venv first on PATH:
# read-only $VALIDATION_STORAGE, no network or Docker socket, 2 GiB, this session's die.
set -u
name=$1; log=$2; shift 2
scratch=$VALIDATION_STORAGE/737-a614/r7/scratch-$name
rm -rf "$scratch"; mkdir -p "$scratch/tmp"
start=$(date +%s.%N)
docker run --rm --name "lane737-r7-$name" --user=1000:1000 --network=none --memory=2g --memory-swap=2g --cpuset-cpus=48-63 \
  -v $VALIDATION_STORAGE:$VALIDATION_STORAGE:ro -v "$scratch:/scratch" -e TMPDIR=/scratch/tmp -e PYTHONDONTWRITEBYTECODE=1 \
  -e GITHUB_WORKSPACE=${WS:-$LANES/737-ci30} -w ${WS:-$LANES/737-ci30} \
  sha256:2d09d1152abecc5ed7799ead632f263d21ebec1f685809fe99c4e3e8801dadcc \
  bash -euo pipefail -c "export PATH=$VALIDATION_STORAGE/737-a614/venv/bin:\$PATH
$*" > "$log" 2>&1
rc=$?
end=$(date +%s.%N)
echo "rc=$rc seconds=$(echo "$end - $start" | bc)"
exit $rc
