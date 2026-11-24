set -euo pipefail
python3 scripts/check_nvm_record_space.py
python3 scripts/check_nvm_record_space.py --self-test
python3 scripts/check_nvm_format_32x32.py
python3 scripts/check_nvm_format_32x32.py --self-test
python3 scripts/check_nvm_klj3.py
python3 scripts/check_nvm_klj3.py --self-test

