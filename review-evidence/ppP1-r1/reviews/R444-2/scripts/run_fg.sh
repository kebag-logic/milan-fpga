#!/usr/bin/env bash
# Run the round-2 focused jobs concurrently INSIDE one foreground call and wait
# for all of them (each bounded by `timeout`). Each job writes receipts/<name>.log
# and receipts/<name>.rc (124 = timed out; builds are incremental, so a re-run
# resumes). Usage: run_fg.sh JOB...   jobs: pp_top nvm_port nvm_figures timer_map
#   lint docs probe. Needs REAL_VERILATOR, scratch/bin/verilator -> verilator-capj.sh,
#   HEADDIR (archive of the head), HEADGIT (git clone at the head) and
#   scratch/base (archive of the round-1 head). nvm_port and nvm_figures share
#   one tree's build dirs: run them in separate calls.
set -uo pipefail
P=$(cd "$(dirname "$0")/.." && pwd); S=$P/scratch; R=$P/receipts
H=${HEADDIR:-$S/head}; G=${HEADGIT:-$S/headgit}
export PATH=$S/bin:$PATH
mkdir -p "$R"
T=${T:-560}
job() { # name capj dir cmd...
  local name=$1 capj=$2 dir=$3; shift 3
  ( cd "$dir" && CAPJ=$capj timeout "$T" "$@" ) >> "$R/$name.log" 2>&1
  echo $? > "$R/$name.rc"
}
for j in "$@"; do
  case $j in
    pp_top)      job pp_top_head 7 "$H/tb/pp_top" make & ;;
    nvm_port)    job nvm_port_head 3 "$H/tb/nvm_port" make & ;;
    nvm_figures) job nvm_figures_head 12 "$H/tb/nvm_port" make figures & ;;
    timer_map)   job timer_map_head 2 "$H/tb/timer_map" make & ;;
    lint)        job lint_hdl_head 1 "$G" ./scripts/lint_hdl.sh & ;;
    docs)        job docs_gates_head 1 "$G" bash -c 'make check && python3 scripts/gen_matrix.py --check' & ;;
    probe)       job probe 1 "$P" "$P/scripts/probe_comment_only.sh" "$S/base" "$H" "$R/probe" & ;;
  esac
done
wait
for j in "$R"/*.rc; do echo "$(basename "$j" .rc) rc=$(cat "$j")"; done
