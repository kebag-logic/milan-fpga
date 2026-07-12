#!/usr/bin/env bash
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Apply the Milan patches to the LiteX-ecosystem source trees in use.
#
#   0001-milan-linux-flashboot.patch      -> litex   (BIOS `linux_flashboot` for QSPI boot)
#   0002-liteeth-gmii-tx-clk-invert.patch -> liteeth (GMII gtx_clk 180° option; fixes the
#                                            marginal RTL8211E TX setup/hold — used by
#                                            milan_soc.py --gtx-tx-invert)
#
# Each tree is discovered from the active Python environment (no hardcoded paths), so this
# works against a venv, a system install, or a git checkout. Idempotent: re-running is a
# no-op once applied. Run it after every `pip install -U litex/liteeth` / update.
#
#   ./apply.sh            # apply all (default)
#   ./apply.sh --reverse  # undo all
set -euo pipefail

HERE="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
PY="${PYTHON:-python3}"
REV=""
[ "${1:-}" = "--reverse" ] && REV="--reverse"

apply_one() {  # $1 = python package name, $2 = patch file
    local pkg="$1" patch="$HERE/$2" root
    root="$("$PY" -c "import $pkg, os; print(os.path.dirname(os.path.dirname($pkg.__file__)))")"
    echo "[patches] $2 -> $root"
    if [ -z "$REV" ] && ! git -C "$root" apply --check "$patch" 2>/dev/null; then
        if git -C "$root" apply --reverse --check "$patch" 2>/dev/null; then
            echo "[patches]   already applied — nothing to do."
            return 0
        fi
        echo "[patches]   ERROR: does not apply and is not already applied ($pkg moved?)." >&2
        echo "[patches]   Re-diff against the new tree and refresh $2." >&2
        return 1
    fi
    git -C "$root" apply $REV "$patch"
    echo "[patches]   ${REV:+reversed }applied."
}

apply_one litex   0001-milan-linux-flashboot.patch
apply_one liteeth 0002-liteeth-gmii-tx-clk-invert.patch

# 0003 needs the vendored xz_embedded decoder (0BSD, from linux lib/xz)
# copied into the BIOS tree first — the patch only touches boot.c/Makefile.
litex_root="$("$PY" -c "import litex, os; print(os.path.dirname(os.path.dirname(litex.__file__)))")"
if [ -z "$REV" ]; then
    mkdir -p "$litex_root/litex/soc/software/bios/xz"
    cp -f "$HERE"/files/xz/* "$litex_root/litex/soc/software/bios/xz/"
    echo "[patches] files/xz -> bios/xz (vendored xz_embedded)"
else
    rm -rf "$litex_root/litex/soc/software/bios/xz"
    echo "[patches] bios/xz removed"
fi
apply_one litex   0003-milan-flashboot-xz-kernel.patch
