#!/bin/bash
. "$(dirname "$0")/env.sh"
cd "$1" && python3 -B "$(dirname "$0")/nomap_boot.py" "$@"
