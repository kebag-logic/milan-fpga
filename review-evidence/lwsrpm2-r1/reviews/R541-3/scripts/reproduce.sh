#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
source_dir=$(cd "$1" && pwd)
packet_dir=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$packet_dir/scratch" "$packet_dir/receipts"
if [ ! -f "$packet_dir/scratch/cgreen/lib/libcgreen.so" ]; then
    git clone --depth 1 --branch 1.6.4 https://github.com/cgreen-devs/cgreen.git "$packet_dir/scratch/cgreen-src"
    cmake -S "$packet_dir/scratch/cgreen-src" -B "$packet_dir/scratch/cgreen-build" -DCMAKE_INSTALL_PREFIX="$packet_dir/scratch/cgreen" -DWITH_UNIT_TESTS=OFF
    make -C "$packet_dir/scratch/cgreen-build" -j16 install
fi
python3 "$packet_dir/scripts/run_checks.py" --source "$source_dir" --packet "$packet_dir" --jobs 4
python3 "$packet_dir/scripts/run_faults.py" --source "$source_dir" --packet "$packet_dir" --jobs 2
python3 "$packet_dir/scripts/run_reversals.py" --source "$source_dir" --packet "$packet_dir" --jobs 2
python3 "$packet_dir/scripts/run_docs.py" --source "$source_dir" --packet "$packet_dir" --jobs 2
python3 "$packet_dir/scripts/audit.py" --source "$source_dir" --packet "$packet_dir"
# The final probe currently returns one; each faulted Flush loses its withdrawal.
python3 "$packet_dir/scripts/run_flush.py" --source "$source_dir" --packet "$packet_dir" --jobs 2
