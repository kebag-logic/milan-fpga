#!/usr/bin/env bash
# extra_gate.sh <head> <name> <command...>: one gate outside the workflows, on its own fresh clean clone of <head>
# (submodules from the lane's clones), one log and one rc, never piped.
set -u
H=$1; N=$2; shift 2
L=<lane>; S=<scratch>/gates; W=$S/extra-$N/wt; G=$S/run/logs
mkdir -p "$G" "$S/extra-$N/tmp"
git clone -q --shared --no-checkout "$L" "$W" && git -C "$W" fetch -q "$L" "$H" && git -C "$W" -c advice.detachedHead=false checkout -q --detach "$H" || exit 3
for dep in $(git -C "$W" config --blob "$H:.gitmodules" --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  if [ -e "$L/$dep/.git" ]; then
    git -C "$W" config "submodule.$dep.url" "$L/$dep"
    git -C "$W" -c protocol.file.allow=always submodule update -q --init --force "$dep"
  fi
done
test -z "$(git -C "$W" status --porcelain)" || exit 4
cd "$W" || exit 5
export HOME=<scratch>/gates/home TMPDIR=$S/extra-$N/tmp VERILATOR=<tools>/pinned-verilator-5.050/verilator PYTHONHASHSEED=0
export PATH=$S/venv/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<shared-scratch>/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
{ echo "# head $H extra gate $N: $*"; "$@"; } > "$G/extra.$N.log" 2>&1
rc=$?; echo $rc > "$G/extra.$N.rc"
git status --porcelain > "$G/extra.$N.tree-after.txt"
echo "$N rc=$rc"
