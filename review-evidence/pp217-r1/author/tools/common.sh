# common.sh: sourced by the gate scripts. Venvs and temporary files live in the lane's scratch, never here.
# g <runs> <dir> <path> <name> <command...>: run one gate in <dir> with PATH=<path>; keeps cmd/log/rc/start/end.
S=$VALIDATION_STORAGE/scratch/pp217-a755
VC=$S/venv-ci
VD=$S/venv-docs
VL=$VALIDATION_TOOLS/verilator-v5.050/bin
SV=$VALIDATION_TOOLS/sv2v-v0.0.12
BASE=$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
g() {
  local R=$1 dir=$2 path=$3 n=$4; shift 4
  # RESUME=1: keep a gate that already ended rc 0 in this runs directory (one directory per head)
  if [ "${RESUME:-0}" = 1 ] && [ "$(cat "$R/$n.rc" 2>/dev/null)" = 0 ]; then echo "$n kept rc 0" >> "$R/resume.txt"; return 0; fi
  mkdir -p "$R"; rm -f "$R/$n.rc" "$R/$n.end"
  echo "$*" > "$R/$n.cmd"; date +%s > "$R/$n.start"
  (cd "$dir" && PATH="$path" "$@") > "$R/$n.log" 2>&1
  echo $? > "$R/$n.rc"; date +%s > "$R/$n.end"
}
