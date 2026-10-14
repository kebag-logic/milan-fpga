. /jobs/lib.sh
gtest
step "litex pins importable" 'python3 -c "import litex, migen; print(litex.__file__)"'
rv32
step "TSN stack boundary (without verilator)" 'python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator'
