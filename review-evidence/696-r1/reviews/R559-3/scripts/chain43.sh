#!/bin/sh
# Emulate the hosted chain for the datapath arm of tb/verilator/maap/mutants.py:
#   scripts/run_all_suites.sh:  make -C tb/verilator/maap  (stdout to a log)
#   Makefile recipe          -> python3 (mutants.py's subprocess call)
#   mutants.py run_case      -> make -j8 -s -C <maap> integration-build ...
#   Makefile:29              -> $(MAKE) -f integration.mk build ...
# using whichever `make` is first on PATH. Builds nothing past parse when the
# derived list is polluted; otherwise builds the datapath harness.
# Usage: chain43.sh <repo copy> <mdir>
set -u
d=$1/tb/verilator/maap; mdir=$2
cat > "$d/probe_chain.mk" <<'MK'
include Makefile
.PHONY: probe-chain
probe-chain:
	python3 -I -c 'import subprocess,sys; r=subprocess.run(["make","-j8","-s","-C",sys.argv[1],"integration-build","MAAP_RTL="+sys.argv[1]+"/../../../hdl/ieee1722/maap/KL_maap.sv","DP_MDIR="+sys.argv[2],"VERILATOR="+sys.argv[3],"VERILATOR_JOBS=0"],capture_output=True,text=True); print(r.stdout[-1500:]+r.stderr[-1500:]); print("integration-build rc=%d" % r.returncode)' $(CURDIR) $(PROBE_MDIR) $(VERILATOR)
MK
make --version | head -1
make -C "$d" -f probe_chain.mk probe-chain PROBE_MDIR="$mdir" VERILATOR="${VERILATOR:-verilator}" 2>&1
echo "top rc=$?"
rm -f "$d/probe_chain.mk"
