set -euo pipefail
: # package index prepared above
python3 -m pip install --quiet pyyaml -r sw/litex/litex_pins.txt
g++ --version | head -n 1
