#!/usr/bin/env bash
# parent-rerun.sh <runs> <parent>: the two rtl-fast OOC self-tests again, after the ROM digests of the pin
R=$1; P=$2
T=<scratch>
export PATH=<toolchain>/sv2v-v0.0.12:$T/venv-ci/bin:<toolchain>/verilator-v5.050/bin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TMPDIR=$T<tmp>/parent
g() { n=$1; shift; echo "$*" > $R/$n.cmd; date +%s > $R/$n.start; (cd $P && "$@") > $R/$n.log 2>&1; echo $? > $R/$n.rc; date +%s > $R/$n.end; }
g ooc_selftest python3 syn/yosys/ooc_selftest.py
g guard_selftest python3 syn/yosys/guard_selftest.py
