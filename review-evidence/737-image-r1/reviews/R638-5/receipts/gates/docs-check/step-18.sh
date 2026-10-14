python3 sw/builder/test_firmware_compiler.py --selftest
python3 sw/builder/test_firmware_compiler.py --absent --audit "$RUNNER_TEMP/rv32-absent.jsonl"
