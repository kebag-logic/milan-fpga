set -euo pipefail
python3 scripts/gen_register_reference.py --check
python3 scripts/gen_register_reference.py --selftest
python3 docs/diagrams/memory_map.gen.py --check

