#!/bin/sh
# [R383] Run a command in a pins-only environment modelled on
# .github/workflows/elaborate.yml: a fresh Python 3.12 venv holding only
# pyyaml + sw/litex/litex_pins.txt (no pythondata_software_* package),
# scripts/ci_litex_env.py + sw/litex/patches/apply.sh applied to it, the
# pinned sv2v v0.0.12, a fresh HOME carrying only the pinned RV32 SDK from
# scripts/ci_rv32_sdk.py, no MILAN_LITEX_PYTHON, and no Vivado on PATH.
# Usage: pins_env.sh <scratch dir> <command...>
S=$(cd "$1" && pwd); shift
exec env -i HOME="$S/home" LANG=C.UTF-8 \
  PATH="$S/bin:$S/pinsenv/bin:/usr/local/bin:/usr/bin:/bin" "$@"
