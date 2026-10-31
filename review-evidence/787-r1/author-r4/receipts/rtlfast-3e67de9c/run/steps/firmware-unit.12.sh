set -euo pipefail
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs "$CI_CAMPAIGN_JOBS"
