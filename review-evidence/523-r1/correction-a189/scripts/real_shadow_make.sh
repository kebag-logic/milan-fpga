#!/usr/bin/env bash
# Real gptp_shadow campaign in a normal developer environment, with integrity
# snapshots of the checkout before and after.
# Usage: real_shadow_make.sh CHECKOUT PACKET [RECEIPT-PREFIX]
set -u
repo="$1"; packet="$2"; prefix="${3:-30-real-make}"
tools=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin
python3 "$packet/scripts/integrity.py" "$repo" "$packet/receipts/${prefix}-integrity-before.json" || exit 3
# Ordinary Git settings a developer shell exports, and a global Git config
# carrying a deprecated setting so every Git command warns on stderr.
python3 "$packet/scripts/rcpt.py" ${prefix} --cwd "$repo" \
  --env "PATH=$tools:$PATH" --env "VERILATOR=$tools/verilator" --env VERILATOR_JOBS=8 \
  --env GIT_EDITOR=vi --env GIT_SEQUENCE_EDITOR=vi --env GIT_PAGER=less \
  --env GIT_AUTHOR_NAME=Developer --env GIT_AUTHOR_EMAIL=developer@example.invalid \
  --env GIT_COMMITTER_NAME=Developer --env GIT_COMMITTER_EMAIL=developer@example.invalid \
  --env GIT_SSH_COMMAND="ssh -oBatchMode=yes" --env GIT_ASKPASS=/bin/false --env GIT_TRACE=0 \
  --env GIT_MERGE_AUTOEDIT=no --env GIT_TERMINAL_PROMPT=0 \
  --env "XDG_CONFIG_HOME=$packet/scratch/devenv" \
  -- make -C tb/verilator/gptp_shadow
status=$?
python3 "$packet/scripts/integrity.py" "$repo" "$packet/receipts/${prefix}-integrity-after.json"
exit $status
