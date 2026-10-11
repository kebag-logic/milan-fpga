#!/bin/bash
# fw_steps.sh CAPTURE : the hosted firmware-unit job's four firmware steps (rtl-fast.yml), each under
# ctrl_capture.py into CAPTURE, in order, stopping at the first failure; jobs 4 as hosted.
set -euo pipefail
C=$1
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$C" -- python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$C" -- python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$C" -- python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$C" -- python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$C" -- python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
