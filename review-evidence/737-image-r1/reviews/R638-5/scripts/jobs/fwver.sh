. /jobs/lib.sh
gtest
step "Verilator version proof" '/opt/verilator/bin/verilator --version | grep -F "5.050"'
rv32
step "TSN stack boundary (only verilator)" 'python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator'
