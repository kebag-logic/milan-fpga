#!/usr/bin/env bash
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Apply the Milan BIOS patches to the LiteX source tree in use.
#
# The QSPI flash-boot feature (milan_soc.py --with-spiflash) needs one small addition to
# the LiteX BIOS: a `linux_flashboot` boot method that copies the Linux images out of the
# memory-mapped QSPI flash into DRAM (skipping the ~4-min serial upload). That lives in the
# vendored/pip-installed LiteX tree, so it is shipped here as a patch and applied in place.
#
# The LiteX tree is discovered from the active Python environment (no hardcoded paths), so
# this works against a venv, a system install, or a git checkout. Idempotent: re-running is
# a no-op once applied. Run it after every `pip install -U litex` / LiteX update.
#
#   ./apply.sh            # apply (default)
#   ./apply.sh --reverse  # undo
set -euo pipefail

HERE="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
PATCH="$HERE/0001-milan-linux-flashboot.patch"
PY="${PYTHON:-python3}"

# LiteX package dir -> repo root is two levels up (…/litex/litex -> …/litex).
LITEX_PKG="$("$PY" -c 'import litex, os; print(os.path.dirname(litex.__file__))')"
LITEX_ROOT="$(dirname "$LITEX_PKG")"
echo "[patches] LiteX tree: $LITEX_ROOT"

REV=""
[ "${1:-}" = "--reverse" ] && REV="--reverse"

# Already applied? (forward patch no longer applies, but reverse does.)
if [ -z "$REV" ] && ! git -C "$LITEX_ROOT" apply --check "$PATCH" 2>/dev/null; then
    if git -C "$LITEX_ROOT" apply --reverse --check "$PATCH" 2>/dev/null; then
        echo "[patches] already applied — nothing to do."
        exit 0
    fi
    echo "[patches] ERROR: patch does not apply and is not already applied (LiteX moved?)." >&2
    echo "[patches] Re-diff against the new tree and refresh 0001-milan-linux-flashboot.patch." >&2
    exit 1
fi

git -C "$LITEX_ROOT" apply $REV "$PATCH"
echo "[patches] ${REV:+reversed }applied 0001-milan-linux-flashboot.patch"
