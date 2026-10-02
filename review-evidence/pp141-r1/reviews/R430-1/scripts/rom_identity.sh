#!/bin/sh
# Regenerate every generated ROM/image from git-archive exports of hdl/ at the
# base and at the head; print sha256 of each output and of every hdl/ file diff.
# Usage: rom_identity.sh <repo> <scratch-dir> <base> <head>
set -eu
REPO=$1; S=$2; BASE=$3; HEAD=$4
for rev in "$BASE" "$HEAD"; do
  d="$S/rom-$rev"; rm -rf "$d"; mkdir -p "$d/out"
  git -C "$REPO" archive "$rev" hdl | tar -x -C "$d"
  (cd "$d" && python3 hdl/aecp/ucode/gen_ucode.py -o out/ucode.hex >/dev/null \
     && python3 hdl/acmp/rom/gen_ltn_rom.py -o out/ltn_rom.hex >/dev/null \
     && python3 hdl/aecp/desc/gen_desc_image.py -i hdl/aecp/desc/example_milan_8.json -o out/image.bin >/dev/null)
  echo "== $rev"; (cd "$d/out" && wc -c ucode.hex ltn_rom.hex image.bin && sha256sum ucode.hex ltn_rom.hex image.bin)
done
echo "== cmp"; for f in ucode.hex ltn_rom.hex image.bin; do cmp "$S/rom-$BASE/out/$f" "$S/rom-$HEAD/out/$f" && echo "$f identical"; done
echo "== hdl files differing between base and head"; git -C "$REPO" diff --stat "$BASE" "$HEAD" -- hdl
echo "== gen_ucode.py token stream without comments/NL identical?"
python3 - "$S/rom-$BASE/hdl/aecp/ucode/gen_ucode.py" "$S/rom-$HEAD/hdl/aecp/ucode/gen_ucode.py" <<'PY'
import sys, tokenize
def toks(p):
    with open(p,'rb') as f:
        return [(t.type,t.string) for t in tokenize.tokenize(f.readline)
                if t.type not in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING)]
a,b=toks(sys.argv[1]),toks(sys.argv[2]); print(len(a),len(b),"identical" if a==b else "DIFFER")
PY
