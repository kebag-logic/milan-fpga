#!/bin/sh
# Usage: loadsample.sh <out> <seconds-between> <until-file>: append /proc/loadavg until <until-file> exists.
while [ ! -e "$3" ]; do cat /proc/loadavg >> "$1"; sleep "$2"; done
