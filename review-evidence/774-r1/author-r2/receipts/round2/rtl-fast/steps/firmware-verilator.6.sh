set -euo pipefail
: # package index prepared above
python3 -m pip install --quiet pyyaml
g++ --version | head -n 1
