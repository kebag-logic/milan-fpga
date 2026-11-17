set -euo pipefail
python3 -m pip install --quiet --require-hashes \
  -r tools/hdl_reference/requirements.txt
python3 scripts/gen_hdl_reference.py --selftest
python3 scripts/gen_hdl_reference.py \
  --output "$RUNNER_TEMP/milan-hdl-reference"
