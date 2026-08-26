#!/usr/bin/env bash
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Apply the Milan patches to the LiteX-ecosystem source trees in use.
#
#   0002-liteeth-gmii-tx-clk-invert.patch -> liteeth (GMII gtx_clk 180° option; fixes the
#                                            marginal RTL8211E TX setup/hold — used by
#                                            milan_soc.py --gtx-tx-invert)
#   0004-vexiiriscv-baremetal-variant.patch -> litex (RV32I, M-mode-only CPU variant)
#   0005-vexiiriscv-cacheless-litex.patch -> pythondata-cpu-vexiiriscv (connect the
#                                            cacheless iBus/dBus and direct DMA path)
#
# Each tree is discovered from the active Python environment (no hardcoded paths), so this
# works against a venv, a system install, or a git checkout. Idempotent: re-running is a
# no-op once applied. Run it after every `pip install -U litex/liteeth` / update.
#
# sw/builder/test_builder.py gate 23h runs this series against a fresh install
# and compares the result file by file.
#
#   ./apply.sh            # apply all (default)
#   ./apply.sh --reverse  # undo all
set -euo pipefail

HERE="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
PY="${PYTHON:-python3}"
REV=""
[ "${1:-}" = "--reverse" ] && REV="--reverse"

# THE SERIES, in apply order.
#   <tree-key> <patch file>
SERIES=(
    "liteeth 0002-liteeth-gmii-tx-clk-invert.patch"
    "litex   0004-vexiiriscv-baremetal-variant.patch"
    "pythondata_cpu_vexiiriscv 0005-vexiiriscv-cacheless-litex.patch"
)

tree_root() {  # $1 = tree key -> the directory the patch paths are relative to
    "$PY" -c "import $1, os; print(os.path.dirname(os.path.dirname($1.__file__)))"
}

# Idempotence is done by NORMALISING, not by testing each patch on its own.
# Asking "does 0001 reverse-apply?" against a tree that also carries 0003 is a
# question with no useful answer, because 0003 rewrote the hunks 0001 added;
# the old script asked exactly that and refused to run twice. So: reverse the
# whole series best-effort, which returns the trees to pristine from ANY
# partially-applied state, then apply it forward and fail hard on the first
# patch that does not go in.
revert_all() {
    local i entry key file root
    for (( i=${#SERIES[@]}-1 ; i>=0 ; i-- )); do
        entry="${SERIES[$i]}"; key="${entry%% *}"; file="${entry##* }"
        root="$(tree_root "$key")"
        if git -C "$root" apply --reverse --check "$HERE/$file" 2>/dev/null; then
            git -C "$root" apply --reverse "$HERE/$file"
            echo "[patches] reversed $file"
        fi
    done
}

apply_all() {
    local entry key file root
    for entry in "${SERIES[@]}"; do
        key="${entry%% *}"; file="${entry##* }"
        root="$(tree_root "$key")"
        if [ ! -d "$root" ]; then
            echo "[patches] ERROR: $root is missing, so $file cannot be applied." >&2
            [ "$key" = vexiiriscv ] && echo "[patches]   Run scripts/ci_litex_env.py first: it clones VexiiRiscv at the revision LiteX pins." >&2
            return 1
        fi
        echo "[patches] $file -> $root"
        if ! git -C "$root" apply --check "$HERE/$file" 2>/dev/null; then
            echo "[patches]   ERROR: does not apply to a pristine $key." >&2
            echo "[patches]   Re-diff against the new tree and refresh $file" >&2
            echo "[patches]   (sw/litex/patches/README.md has the procedure)." >&2
            return 1
        fi
        git -C "$root" apply "$HERE/$file"
        echo "[patches]   applied."
    done
}

# --reverse MUST PROVE THE TREE IS PRISTINE, not merely that it tried.
# revert_all() is best-effort ON PURPOSE - as the normalisation step of a
# forward apply, a patch it cannot reverse is fine, because apply_all() then
# refuses it by name. As the WHOLE of `--reverse` that same tolerance is a
# false success: one locally edited hunk leaves that patch applied while the
# others come out, and the caller is told the toolchain is pristine ([R0] on
# PR #189).
#
# THE TEST IS THE COMPLETE SERIES, NOT EACH PATCH. Two weaker invariants were
# written first and both were wrong, for the same reason the series is stacked:
#   * "the patch no longer reverse-applies" calls an EDITED hunk absent, since
#     an edited file matches neither state. Measured: it passed a tree in which
#     0002-liteeth was still applied with one changed line.
#   * "every patch forward-applies" fails on a genuinely pristine tree, because
#     0003 is diffed on top of 0001 and composes only after it.
# So apply the whole series in order - which succeeds only from pristine - and
# then unwind exactly what went on, leaving the caller as it found them.
verify_pristine() {
    local entry key file root i applied=0 ok=1
    for (( i=0; i<${#SERIES[@]}; i++ )); do
        entry="${SERIES[$i]}"; key="${entry%% *}"; file="${entry##* }"
        root="$(tree_root "$key")"
        if [ ! -d "$root" ] || ! git -C "$root" apply "$HERE/$file" 2>/dev/null
        then
            echo "[patches] ERROR: $key is not pristine for $file - it is" >&2
            echo "[patches]   neither cleanly reversed nor cleanly applied." >&2
            ok=0
            break
        fi
        applied=$((applied + 1))
    done
    for (( i=applied-1; i>=0; i-- )); do
        entry="${SERIES[$i]}"; key="${entry%% *}"; file="${entry##* }"
        root="$(tree_root "$key")"
        git -C "$root" apply --reverse "$HERE/$file" 2>/dev/null || true
    done
    [ "$ok" -eq 1 ]
}

revert_all
if [ -n "$REV" ]; then
    if ! verify_pristine; then
        echo "[patches] --reverse did NOT fully reverse the series, so this" >&2
        echo "[patches]   tree is in a MIXED state and is not pristine. Fix" >&2
        echo "[patches]   the reported file(s) by hand - a local edit to a" >&2
        echo "[patches]   patched hunk is the usual cause - and re-run." >&2
        exit 1
    fi
    echo "[patches] series reversed (verified absent)."
    exit 0
fi
apply_all
echo "[patches] series applied (${#SERIES[@]} patches)."
