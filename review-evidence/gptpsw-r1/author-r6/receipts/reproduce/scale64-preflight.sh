#!/usr/bin/env bash
set -euo pipefail
source /data-2/milan/tmp/opt-a837/env.sh
export A837_SOURCE=/data-2/milan/lanes/opt-hart2
cd /data-2/milan/lanes/opt-hart2
exec python3 /data-2/milan/tmp/opt-a837/run.py /data-2/milan/tmp/opt-a837/scale64-preflight.log python3 /data-2/milan/tmp/opt-a837/onehart_image.py /data-2/milan/tmp/opt-a837/scale/64-preflight endstation_ax7101_64x64 2
