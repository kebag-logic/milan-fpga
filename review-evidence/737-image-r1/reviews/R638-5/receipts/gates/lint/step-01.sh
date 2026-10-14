VERILATOR_VERSION=v5.050; /opt/verilator/bin/verilator --version; /opt/verilator/bin/verilator --version | grep -F "${VERILATOR_VERSION#v}"
