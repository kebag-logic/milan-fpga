set -euo pipefail
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/docs_inventory.py --check
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/docs_inventory.py --selftest

