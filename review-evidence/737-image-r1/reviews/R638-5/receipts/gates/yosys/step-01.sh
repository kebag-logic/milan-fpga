YOSYS_VERSION=v0.66; test -x /opt/yosys/bin/yosys-abc; echo "bundled ABC: $(cat /opt/yosys/ABC_REV)"; yosys -V; yosys -V | grep -F "Yosys ${YOSYS_VERSION#v}"
