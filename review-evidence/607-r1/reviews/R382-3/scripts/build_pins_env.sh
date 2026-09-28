#!/usr/bin/env bash
# Build a pins-only elaborate environment the way .github/workflows/elaborate.yml does:
# Python 3.12, `pip install pyyaml`, `pip install -r sw/litex/litex_pins.txt`,
# scripts/ci_litex_env.py, sw/litex/patches/apply.sh, the pinned sv2v and the pinned
# RV32 SDK. A private HOME keeps every cache (pip, sbt/coursier, SDK) out of the host
# account, and a private venv keeps the interpreter free of any bench package.
# Usage: build_pins_env.sh <step> where step is venv|pins|litex_env|patches|sdk|census
#   env: PKT (packet dir), TREE (probe copy of the head), PY312 (a Python 3.12)
set -euo pipefail
PKT=${PKT:?}; TREE=${TREE:?}; PY312=${PY312:?}
export HOME="$PKT/scratch/home"
VENV="$PKT/scratch/pins-venv"
mkdir -p "$HOME"
cd "$TREE"
case "$1" in
  venv) "$PY312" -m venv "$VENV" ;;
  pins) "$VENV/bin/python3" -m pip install --quiet pyyaml
        "$VENV/bin/python3" -m pip install --quiet -r sw/litex/litex_pins.txt ;;
  litex_env) PATH="$VENV/bin:$PATH" python3 scripts/ci_litex_env.py ;;
  patches) PATH="$VENV/bin:$PATH" sw/litex/patches/apply.sh ;;
  sdk) PATH="$VENV/bin:$PATH" python3 scripts/ci_rv32_sdk_selftest.py
       PATH="$VENV/bin:$PATH" python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host" ;;
  census)
    "$VENV/bin/python3" --version
    "$VENV/bin/python3" -m pip freeze --all
    for m in pythondata_software_picolibc pythondata_software_compiler_rt; do
      "$VENV/bin/python3" -c "import importlib.util,sys; s=importlib.util.find_spec('$m'); print('$m', 'PRESENT' if s else 'ABSENT'); sys.exit(0)"
    done
    "$VENV/bin/python3" -c "import sys; print('sys.path', sys.path)" ;;
  *) echo "unknown step $1" >&2; exit 2 ;;
esac
