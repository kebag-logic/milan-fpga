#!/usr/bin/env bash
# vdump2.sh <out-dir> <label-a> <dcp-a> <label-b> <dcp-b>: vdump.sh over two routed checkpoints, one after the other.
set -u
O=$1; mkdir -p "$O"
bash <scratch>/bin/vdump.sh "$3" "$O/$2"; ra=$?
bash <scratch>/bin/vdump.sh "$5" "$O/$4"; rb=$?
echo "vdump2 rc=$ra,$rb"; [ $ra = 0 ] && [ $rb = 0 ]
