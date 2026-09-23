#!/bin/sh
# Power-strip host side of one switch cycle (issue 117, A202): outlet off,
# hold, outlet on. Started under nohup by the caller, which holds the bench
# lock, so the "on" half still runs if the caller's session drops.
# usage: powerstrip_cycle.sh <outlet> <hold_s>
O=$1; H=$2
trap '' HUP
echo "T_STATUS_BEFORE $(date +%s.%N)"; powerstrip status
echo "T_OFF_CMD $(date +%s.%N)"; powerstrip off "$O"; echo "OFF_RC=$? T_OFF_DONE $(date +%s.%N)"
powerstrip status; echo "T_STATUS_OFF $(date +%s.%N)"
sleep "$H"
echo "T_ON_CMD $(date +%s.%N)"; powerstrip on "$O"; echo "ON_RC=$? T_ON_DONE $(date +%s.%N)"
powerstrip status; echo "T_STATUS_AFTER $(date +%s.%N)"
