#!/bin/bash
# run_probes.sh SRC: for each reviewer probe patch, a fresh copy of SRC's hdl/ and the SRP benches, the patch
# applied (git apply --check first), then the named suites; receipts/probe-<name>-<suite>.{log,rc}
set -u
PK=${PK:-$REVIEWS/pp216-r801-2-packet}; SRC=$1
export PATH="$PK/scratch/bin:$PATH"
run() { name=$1; shift
  T=$PK/scratch/probe-run/$name; rm -rf "$T"; mkdir -p "$T/tb"
  cp -r "$SRC/hdl" "$T/hdl"; for b in common srp_top srp_stream_fsms srp_encoder srp_admission; do cp -r "$SRC/tb/$b" "$T/tb/$b"; done
  ( cd "$T" && git init -q && git apply --check "$PK/scripts/probes/$name.patch" && git apply "$PK/scripts/probes/$name.patch" ) \
    > "$PK/receipts/probe-$name-apply.log" 2>&1 || { echo 99 > "$PK/receipts/probe-$name-apply.rc"; return; }
  for s in "$@"; do
    case $s in enc) cmd=(make -C tb/srp_encoder -j4);; app) cmd=(make -C tb/srp_top -j4 RUN_ARGS=applicant);; esac
    ( cd "$T" && "${cmd[@]}" ) > "$PK/receipts/probe-$name-$s.log" 2>&1; echo $? > "$PK/receipts/probe-$name-$s.rc"
  done
}
run p1-flush-dropped enc app
run p3-begin-keeps-registrar enc app
run p4-withdraw-keeps-valid enc
run p8-begin-by-alloc enc
echo done > $PK/receipts/probes.done
