# common.sh: sourced by the gate scripts. Every venv and tool of this lane is in the lane's own scratch. g() runs one
# gate and asserts python3 is the expected interpreter before and after it: a missing venv would otherwise fall
# through PATH to the system python with no error. Rc 97 marks such a gate; <gate>.python records what it saw.
S=$VALIDATION_STORAGE/scratch/pp216-a754b
T=$HOME/milan-fpga-management/2026-09-23/pp216-a754b/tools
V=$VALIDATION_STORAGE/scratch/pp216-a754/venv-ci
D=$VALIDATION_STORAGE/scratch/pp216-a754/venv-docs
VL=$VALIDATION_TOOLS/verilator-v5.050/bin
BASE=$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
pysee() { env PATH="$1" python3 -c 'import sys; print(sys.prefix, sys.version.split()[0])' 2>&1; }
# g <runs> <dir> <venv> <path> <name> <command...>
g() {
  local R=$1 dir=$2 venv=$3 path=$4 n=$5; shift 5
  rm -f "$R/$n.rc" "$R/$n.end"
  echo "$*" > "$R/$n.cmd"; date +%s > "$R/$n.start"
  echo "before $(pysee "$path")" > "$R/$n.python"
  if [ "$(pysee "$path")" != "$venv 3.12.3" ]; then echo 97 > "$R/$n.rc"; date +%s > "$R/$n.end"; return; fi
  (cd "$dir" && PATH="$path" "$@") > "$R/$n.log" 2>&1
  local rc=$?
  echo "after $(pysee "$path")" >> "$R/$n.python"
  [ "$(pysee "$path")" = "$venv 3.12.3" ] || rc=97
  echo "$rc" > "$R/$n.rc"; date +%s > "$R/$n.end"
}
