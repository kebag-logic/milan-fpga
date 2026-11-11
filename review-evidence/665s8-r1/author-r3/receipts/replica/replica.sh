#!/bin/bash
# replica.sh: the wire-timing job's setup and step at fbe5acc9837dcd2a3ce4633b187982b2d684833d, as a fresh runner does it: a fresh clone, a fresh venv
# built by the job's own install steps (no bench venv), the Scala caches copied as a cache restore, the pinned
# Verilator and the RV32 SDK installed fresh, then the step itself on 4 CPUs.
set -uo pipefail
R=<scratch>/replica; S=<scratch>
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export HOME=$R/home PIP_DEFAULT_TIMEOUT=30 PIP_RETRIES=8 PYTHONHASHSEED=0 RUNNER_TEMP=$R/runner_temp TMPDIR=$R/tmp
mkdir -p $RUNNER_TEMP $TMPDIR
bash $S/clone_at.sh fbe5acc9837dcd2a3ce4633b187982b2d684833d $R/wt > $R/clone.log 2>&1 || { echo 3 > $R/rc; exit 3; }
cd $R/wt
export PATH=$RUNNER_TEMP/litex-venv/bin:<data>/tools/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin
step() { name=$1; shift; echo "== $name ($(date -u +%T))"; "$@"; rc=$?; echo "== $name rc=$rc"; [ $rc -eq 0 ] || { echo $rc > $R/rc; exit $rc; }; }
step venv /usr/bin/python3 -m venv $RUNNER_TEMP/litex-venv
step litex bash -c 'python3 -m pip install --quiet pyyaml && python3 -m pip install --quiet -r sw/litex/litex_pins.txt'
step vexii-source bash -c 'python3 scripts/ci_litex_env.py'
step patches sw/litex/patches/apply.sh
step runtime-sources bash -c "$(python3 -c 'import yaml; s=[s for s in yaml.safe_load(open(".github/workflows/rtl-fast.yml"))["jobs"]["wire-timing"]["steps"] if s.get("name","").startswith("Install the image")]; print(s[0]["run"])')"
step sdk python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
step verilator bash -c 'verilator --version'
start=$(date +%s)
echo "== wire-timing step ($(date -u +%T))"
WIRE_JOBS=4 taskset -c 56-59 python3 tb/verilator/ctrl_wire_timing/run.py --ci --build-dir "$RUNNER_TEMP/wire-timing"
rc=$?
echo "== wire-timing step rc=$rc wall $(( $(date +%s) - start )) s"
echo $rc > $R/rc
