set -euo pipefail
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/gen_hdl_reference.py --selftest
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/gen_hdl_reference.py --output "$RUNNER_TEMP/hdl-reference"
