. /jobs/lib.sh
gtest
step "tally selftest" 'python3 sw/firmware/gtest/tally_selftest.py'
rv32
step "control-plane suites shard 0/4" 'python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4'
step "saved-state store suites" 'python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs "$(nproc)"'
step "firmware coverage ratchet" 'python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs "$(nproc)"'
