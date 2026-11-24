set -euo pipefail
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/gen_toc.py --selftest
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/gen_toc.py --verify-anchors
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/gen_toc.py --check

