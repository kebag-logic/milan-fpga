#!/bin/bash
# Run the default containment self-test under several parent locales, in parallel.
# Usage: run_parents.sh <repo-root> <locpath> <outdir> [label...]
root=${1:?root}; locpath=${2:?locpath}; out=${3:?out}; shift 3
declare -A LC=( [default]="" [utf8-mode]=C [ascii]=C [utf8-strict]=en_US.UTF-8
  [latin1]=en_US.ISO-8859-1 [big5]=zh_TW.BIG5 [big5hkscs]=zh_HK.BIG5-HKSCS
  [johab]=ko_KR.JOHAB [cp932]=ja_JP.WINDOWS-31J )
labels=("$@"); [ ${#labels[@]} -eq 0 ] && labels=(default utf8-mode ascii utf8-strict latin1 big5 big5hkscs johab cp932)
mkdir -p "$out"
for l in "${labels[@]}"; do
  (
    cd "$root" || exit 9
    if [ "$l" = default ]; then envs=(env PYTHONDONTWRITEBYTECODE=1)
    else
      u=0; [ "$l" = utf8-mode ] && u=1
      envs=(env -u LANG -u LANGUAGE -u PYTHONIOENCODING LC_ALL="${LC[$l]}" LOCPATH="$locpath"
            PYTHONUTF8=$u PYTHONCOERCECLOCALE=0 PYTHONDONTWRITEBYTECODE=1)
    fi
    s=$(date +%s)
    "${envs[@]}" python3 -c 'import sys,codecs;print("parent fs",codecs.lookup(sys.getfilesystemencoding()).name,"stdout",sys.stdout.encoding,sys.stdout.errors)' > "$out/parent-$l.log" 2>&1
    "${envs[@]}" python3 scripts/check_merge_containment.py --selftest >> "$out/parent-$l.log" 2>&1
    rc=$?
    e=$(date +%s)
    ok=$(grep -c '^  ok  ' "$out/parent-$l.log"); fail=$(grep -c '^  FAIL ' "$out/parent-$l.log")
    notrun=$(grep -c 'NOT RUN' "$out/parent-$l.log")
    echo "$l rc=$rc ok=$ok fail=$fail notrun=$notrun seconds=$((e-s)) $(head -1 "$out/parent-$l.log")" > "$out/parent-$l.summary"
  ) &
  while [ "$(jobs -rp | wc -l)" -ge 8 ]; do wait -n; done
done
wait
cat "$out"/parent-*.summary
