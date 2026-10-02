#!/bin/bash
# elaborate.yml's elaborate job in its own CPython 3.12 venv and HOME (isolated from the shared LiteX install)
set -u
R=$VALIDATION_STORAGE/629-a500
echo "elaborate start $(date -Is)"
VENV=$R/elab-venv HOMEDIR=$R/elab-home "$R/replay/run_job.sh" .github/workflows/elaborate.yml elaborate elaborate
echo "elaborate rc=$? end $(date -Is)"
