#!/usr/bin/env bash
# Run the default containment self-test in a fresh parent whose filesystem
# codec is set by the named locale.  Usage: parent_selftest.sh <label> <checker> <locale-dir> <out-dir>
set -u
label=$1 checker=$2 locales=$3 out=$4
base=(env -i "PATH=$PATH" "HOME=$HOME" "TMPDIR=${TMPDIR:-/tmp}" PYTHONDONTWRITEBYTECODE=1 PYTHONCOERCECLOCALE=0)
case $label in
  utf8-locale) e=(LC_ALL=en_US.UTF-8 PYTHONUTF8=0);;
  utf8-mode)   e=(LC_ALL=C PYTHONUTF8=1);;
  ascii)       e=(LC_ALL=C PYTHONUTF8=0);;
  latin1)      e=(LOCPATH=$locales LC_ALL=en_US.ISO-8859-1 PYTHONUTF8=0);;
  big5)        e=(LOCPATH=$locales LC_ALL=zh_TW.BIG5 PYTHONUTF8=0);;
  johab)       e=(LOCPATH=$locales LC_ALL=ko_KR.JOHAB PYTHONUTF8=0);;
  cp932)       e=(LOCPATH=$locales LC_ALL=ja_JP.WINDOWS-31J PYTHONUTF8=0);;
esac
"${base[@]}" "${e[@]}" python3 -c 'import sys,codecs;print("parent fs", codecs.lookup(sys.getfilesystemencoding()).name, "stdout", sys.stdout.encoding, sys.stdout.errors)' > "$out/$label.log" 2>&1
start=$(date +%s)
"${base[@]}" "${e[@]}" python3 "$checker" --selftest >> "$out/$label.log" 2>&1
rc=$?
echo "rc=$rc seconds=$(( $(date +%s) - start ))" >> "$out/$label.log"
printf '%-12s rc=%s ok=%s FAIL=%s NOTRUN=%s\n' "$label" "$rc" "$(grep -cE '^\s+ok ' "$out/$label.log")" "$(grep -cE '^\s+FAIL' "$out/$label.log")" "$(grep -c 'NOT RUN' "$out/$label.log")"
