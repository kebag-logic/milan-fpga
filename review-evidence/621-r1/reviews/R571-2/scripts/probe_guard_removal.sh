#!/bin/sh
# Usage: probe_guard_removal.sh <repo-root> <receipt-dir>
# Plants two guard removals into temporary copies of scripts/check_nvm_capture.py
# inside the repo's scripts directory (so ROOT and imports resolve), runs each,
# records rc and the FAIL line, then deletes the copies. Each must exit 1 with
# "receipt arm escaped the production timing bound".
set -u
root=$1; out=$2
cd "$root" || exit 2
python3 -I - <<'EOF'
from pathlib import Path
src = Path('scripts/check_nvm_capture.py').read_text()
call = "capture.grade_rows(arm['rows'], production_spec(arm, census))"
spec = "**census, mutation='none')"
assert src.count(call) == 1 and src.count(spec) == 1
Path('scripts/_r571_probe_callsite.py').write_text(
    src.replace(call, "capture.grade_rows(arm['rows'], dict(arm, **census))"))
Path('scripts/_r571_probe_specbuilder.py').write_text(
    src.replace(spec, "**census, mutation=arm.get('mutation', 'none'))"))
EOF
for name in callsite specbuilder; do
  python3 "scripts/_r571_probe_$name.py" > "$out/guard_$name.log" 2>&1
  echo $? > "$out/guard_$name.rc"
  echo "$name rc=$(cat "$out/guard_$name.rc") $(grep '^FAIL' "$out/guard_$name.log")"
  rm -f "scripts/_r571_probe_$name.py"
done
