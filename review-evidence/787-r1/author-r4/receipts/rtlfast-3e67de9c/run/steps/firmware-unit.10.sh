set -euo pipefail
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs "$CI_CAMPAIGN_JOBS" --shard 0/4
