#!/usr/bin/env bash
# sync.sh: mirror the lane's working tree (no .git, no build output) into the dev scratch copy
set -euo pipefail
rsync -a --delete --exclude .git --exclude 'obj_*/' --exclude obj_dir/ --exclude ucode.hex --exclude ltn_rom.hex --exclude image.bin --exclude image.map --exclude __pycache__/ --exclude .venv-wavedrom/ <lane>/ <scratch>/dev/
