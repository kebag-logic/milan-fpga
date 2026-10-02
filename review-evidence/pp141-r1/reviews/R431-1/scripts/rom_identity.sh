#!/bin/sh
# Regenerate every ROM/image from hdl/ at the base and at the head of PR #142
# and compare them byte for byte. Usage: rom_identity.sh REPO OUTDIR
# Exit 0 only when every output is byte-identical.
set -eu
REPO="$1"; OUT="$2"
BASE=03c842a780064048b0a1a3de29214174a1c13934
HEAD=4a40b1798e463d09aafd74632408003229bcc673
rm -rf "$OUT/base" "$OUT/head"
for rev in base head; do
  sha=$BASE; [ "$rev" = head ] && sha=$HEAD
  mkdir -p "$OUT/$rev"
  git -C "$REPO" archive "$sha" hdl | tar -x -C "$OUT/$rev"
  ( cd "$OUT/$rev" &&
    python3 hdl/aecp/ucode/gen_ucode.py -o ucode.hex > gen_ucode.log 2>&1 &&
    python3 hdl/acmp/rom/gen_ltn_rom.py -o ltn_rom.hex > gen_ltn_rom.log 2>&1 &&
    python3 hdl/aecp/desc/gen_desc_image.py -i hdl/aecp/desc/example_milan_8.json \
        -o image.bin > gen_desc_image.log 2>&1 )
done
echo "== hdl/ tree diff (paths differing between base and head exports)"
diff -rq "$OUT/base/hdl" "$OUT/head/hdl" || true
rc=0
for f in ucode.hex ltn_rom.hex image.bin; do
  b=$(sha256sum < "$OUT/base/$f" | cut -d' ' -f1)
  h=$(sha256sum < "$OUT/head/$f" | cut -d' ' -f1)
  n=$(wc -c < "$OUT/head/$f")
  if cmp -s "$OUT/base/$f" "$OUT/head/$f"; then v=IDENTICAL; else v=DIFFERENT; rc=1; fi
  echo "$f bytes=$n base=$b head=$h $v"
done
# comment-only proof: Python token streams with comments and NL/NEWLINE-only
# lines dropped must be identical
python3 - "$OUT/base/hdl/aecp/ucode/gen_ucode.py" "$OUT/head/hdl/aecp/ucode/gen_ucode.py" <<'EOF'
import sys, tokenize
def toks(p):
    with open(p, 'rb') as f:
        return [(t.type, t.string) for t in tokenize.tokenize(f.readline)
                if t.type not in (tokenize.COMMENT, tokenize.NL)]
a, b = toks(sys.argv[1]), toks(sys.argv[2])
print(f"gen_ucode.py tokens base={len(a)} head={len(b)} identical={a == b}")
sys.exit(0 if a == b else 1)
EOF
exit $rc
