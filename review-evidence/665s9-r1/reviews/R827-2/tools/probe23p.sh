#!/bin/bash
# probe23p.sh <source clone> <scratch dir> <arm> <log>
# Copies the clone, plants one arm in sw/litex/check_image_identity.py (or none),
# runs gate 23p alone with the LiteX interpreter, and records the rc.
# arms: head | if-true | have-eq-bound | no-manifest-ident
set -u
src=$1; dir=$2; arm=$3; log=$4
rm -rf "$dir"; cp -a "$src" "$dir"
f="$dir/sw/litex/check_image_identity.py"
case $arm in
  head) ;;
  if-true) sed -i 's/^    if have != bound:$/    if True:/' "$f";;
  have-eq-bound) sed -i 's/^    if have != bound:$/    if have == bound:/' "$f";;
  no-manifest-ident) python3 -I - "$f" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
a='    if claimed["ident"] != got["ident"]:\n        found.append(("manifest", f"the manifest\'s ident {claimed[\'ident\']!r} is not the image\'s {got[\'ident\']!r}"))\n'
assert s.count(a)==1; open(p,"w").write(s.replace(a,""))
PY
  ;;
esac
{
  echo "head $(git -C "$src" rev-parse HEAD) arm $arm"
  echo "planted diff:"; git -C "$dir" diff --stat; git -C "$dir" diff
  echo "---"
  cd "$dir" && MILAN_LITEX_PYTHON="${MILAN_LITEX_PYTHON:-$HOME/litex-milan/venv/bin/python3}" \
    python3 sw/builder/test_builder.py --gates test_image_identity_gate
  echo "rc=$?"
} > "$log" 2>&1
