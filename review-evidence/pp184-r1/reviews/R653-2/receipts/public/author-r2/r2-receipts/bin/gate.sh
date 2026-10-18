#!/usr/bin/env bash
# gate.sh <log-name> <workdir> <command...>
# Runs one gate with the pinned tools, never piped; writes <log>.log and <log>.rc.
set -u
name="$1"; dir="$2"; shift 2
logs=<scratch>/r2/logs
mkdir -p "$logs"
export PATH="<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH"
if [ -n "${GATE_VENV:-}" ]; then export PATH="$GATE_VENV/bin:$PATH"; fi
rm -f "$logs/$name.rc"
{
  echo "## gate $name"
  echo "## dir $dir"
  echo "## cmd $*"
  echo "## head $(git -C "$dir" rev-parse HEAD 2>/dev/null)"
  echo "## start $(date -Is)"
} > "$logs/$name.log"
cd "$dir" || { echo 99 > "$logs/$name.rc"; exit 99; }
"$@" >> "$logs/$name.log" 2>&1
rc=$?
echo "## end $(date -Is) rc $rc" >> "$logs/$name.log"
echo "$rc" > "$logs/$name.rc"
exit "$rc"
