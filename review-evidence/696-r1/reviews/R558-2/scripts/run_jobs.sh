#!/usr/bin/env bash
# R558-2 focused MAAP jobs on disposable copies of the exact head.
# Usage: run_jobs.sh <packet-dir> <pinned-bin-dir>
# Each job runs detached with its own log and rc file under <packet>/receipts.
# copyA: default MAAP target (harness then the full mutation campaign).
# copyB: R559-1's r_restart_on_link_loss.patch applied verbatim, harness only.
# copyC: line coverage, then reviewer probes (probe_mutants.sh).
set -u
P=$1
BIN=$2
S=$P/scratch
R=$P/receipts
export P S R
export PATH=$BIN:$PATH
export VERILATOR=$BIN/verilator
mkdir -p "$R"

job() {  # name dir command...
    local name=$1 dir=$2; shift 2
    ( cd "$dir" && "$@" ) > "$R/$name.log" 2>&1
    echo $? > "$R/$name.rc"
}

job_plant() {
    cd "$S/copyB" || return 2
    patch --no-backup-if-mismatch hdl/ieee1722/maap/KL_maap.sv < "$S/evidence/r_restart_on_link_loss.patch" || return 3
    git diff --stat
    make -s -C tb/verilator/maap run MDIR=obj_plant VERILATOR_JOBS=4
}

setsid nohup bash -c "$(declare -f job); job default_campaign $S/copyA make -C tb/verilator/maap VERILATOR=$VERILATOR VERILATOR_JOBS=4" >/dev/null 2>&1 &
setsid nohup bash -c "$(declare -f job job_plant); S=$S; job r559_plant $S/copyB job_plant" >/dev/null 2>&1 &
setsid nohup bash -c "$(declare -f job); job coverage $S/copyC make -C tb/verilator/maap coverage VERILATOR=$VERILATOR VERILATOR_JOBS=4; job probes $S/copyC bash $P/scripts/probe_mutants.sh $S/copyC" >/dev/null 2>&1 &
echo launched
