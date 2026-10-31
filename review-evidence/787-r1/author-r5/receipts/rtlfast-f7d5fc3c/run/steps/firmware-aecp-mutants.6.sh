set -euo pipefail
: # package index prepared above
python3 -m pip install --quiet pyyaml
g++ --version | head -n 1
gcov --version | head -n 1
