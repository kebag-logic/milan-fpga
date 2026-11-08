#!/bin/sh
# Probe: restore all fifteen removed entries in a disposable clone, regenerate, and ask --check.
set -u
cd "$1"
git show HEAD~1:scripts/docs_inventory.json > scripts/docs_inventory.json
python3 -I scripts/docs_inventory.py --check >/dev/null 2>&1; echo "restore-all, page not regenerated: check rc=$?"
python3 -I scripts/docs_inventory.py --write >/dev/null 2>&1; echo "write rc=$?"
python3 -I scripts/docs_inventory.py --check >/dev/null 2>&1; echo "restore-all, page regenerated: check rc=$?"
git diff --quiet HEAD~1 -- docs/DOCUMENTATION_AUDIT.md scripts/docs_inventory.json; echo "regenerated pair equals parent head bytes: rc=$?"
git checkout -q -- . ; git status --porcelain | wc -l
