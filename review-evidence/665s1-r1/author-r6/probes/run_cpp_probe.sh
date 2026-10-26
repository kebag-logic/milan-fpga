#!/bin/bash
# Run a reviewer's C++ probe unchanged: append it to a disposable copy of the checkout's
# sw/firmware/ctrl/test/test_aecp.cpp and build and run the named tests with the reviewer's
# own run_arm.py, which reads the checkout's firmware.
#   $1 checkout   $2 probe .cpp   $3 scratch directory (must not exist)   $4 arm (core|mailbox|app)
#   $5 interfaces   $6 gtest filter   $7 the reviewer's run_arm.py
set -u
[ -e "$3" ] && { echo "$3 exists"; exit 2; }
mkdir -p "$3"
cp -r "$1/sw/firmware/ctrl/test" "$3/test"
rm -rf "$3/test/__pycache__"
cat "$2" >> "$3/test/test_aecp.cpp"
echo "probe $(sha256sum "$2" | cut -d' ' -f1) $(basename "$2") at $(git -C "$1" rev-parse HEAD), arm $4, interfaces $5"
python3 -B "$7" "$1" "$3/out" "$4" "$5" "$3/test" "$6"
