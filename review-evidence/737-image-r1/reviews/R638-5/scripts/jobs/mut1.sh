. /jobs/lib.sh
gtest
rv32
step "mutation campaign shard 1/4" 'python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4'
