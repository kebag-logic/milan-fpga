set -euo pipefail
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
