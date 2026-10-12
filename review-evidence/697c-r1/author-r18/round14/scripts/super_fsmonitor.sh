#!/usr/bin/env bash
# Scratch: a disposable clone's own .git/config names a recorder as core.fsmonitor; the clone's pin check
# (ctrl_build.py --stack-pin, which reads the superproject's index for the gitlink) runs once; how often did Git
# start the recorder? usage: super_fsmonitor.sh <disposable clone> <work>
set -u
clone=$1; work=$2
mkdir -p "$work"; rm -f "$work/ran"
printf '#!/bin/sh\necho "$0 $*" >> %s/ran\nexit 1\n' "$work" > "$work/recorder"; chmod +x "$work/recorder"
git -C "$clone" config core.fsmonitor "$work/recorder"
python3 -I "$clone/sw/firmware/ctrl/test/ctrl_build.py" --stack-pin; echo "exit $?"
echo "recorder runs during the pin check: $( [ -f "$work/ran" ] && wc -l < "$work/ran" || echo 0)"
git -C "$clone" config --unset core.fsmonitor
