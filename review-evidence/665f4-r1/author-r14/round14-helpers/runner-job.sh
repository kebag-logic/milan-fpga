#!/bin/bash
set -eu
r="${SCRATCH:?set SCRATCH to the disk scratch root}"
sudo -n docker run --rm --init --network none --read-only --cap-drop ALL --security-opt no-new-privileges --memory 2g --pids-limit 512 --user 1000:1000 --mount "type=bind,src=$r/runner-tree,dst=/candidate,readonly" --mount "type=bind,src=$r/runner-work,dst=/scratch" --env TMPDIR=/scratch --env HOME=/scratch --env PYTHONDONTWRITEBYTECODE=1 --workdir /candidate --entrypoint /usr/bin/python3 catthehacker/ubuntu:full-latest -I scripts/act_ci.py --selftest
