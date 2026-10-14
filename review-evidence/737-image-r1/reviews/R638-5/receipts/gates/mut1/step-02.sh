mkdir -p "$HOME/br-milan-rv32"; [ -e "$HOME/br-milan-rv32/host" ] || ln -s /opt/rv32-sdk "$HOME/br-milan-rv32/host"; "$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc" --version | head -1
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
