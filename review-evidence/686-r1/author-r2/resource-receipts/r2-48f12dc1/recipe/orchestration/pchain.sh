#!/usr/bin/env bash
# Round 2 Part B: the recipe on the merge result, one heavy job at a time,
# each Vivado step under the shared lock: export, shipping route, standalone
# endpoints, then the recipe's symlink removal. "rc seconds" per step.
T=<scratch>/r2
S=$T/scripts
echo $$ > "$T/pchain.pid"
for sig in HUP INT TERM QUIT; do trap "echo \"\$(date +%T) chain got SIG$sig\" >> $T/pchain.out; exit 1" $sig; done
bash "$S/memlog.sh" $$ "$T/pchain-mem.log" &
cd <repo> || exit 2
export TMPDIR=<scratch>/tmp
step() {  # name, command...
  local name=$1; shift
  local start; start=$(date +%s)
  echo "$(date +%T) start $name" >> "$T/pchain.out"
  "$@"
  local rc=$?
  echo "$rc $(( $(date +%s) - start ))" > "$T/$name.rc"
  echo "$(date +%T) end $name rc=$rc" >> "$T/pchain.out"
  return $rc
}
step export bash -c "bash $S/export.sh ax7101 ax8x8 > $T/export.log 2>&1" || exit 1
step route bash -c "bash $S/route.sh > $T/route.log 2>&1" || exit 1
step ooc bash -c "bash $S/ooc.sh > $T/ooc.log 2>&1" || exit 1
step unlink bash -c "test -L sw/builder/out && unlink sw/builder/out && unlink configs/generated/ltn_rom.hex && unlink configs/generated/ucode.hex && git diff --check > $T/unlink.log 2>&1"
echo "$(date +%T) chain done" >> "$T/pchain.out"
