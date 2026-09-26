#!/usr/bin/env bash
# Reviewer reproduction for issue #509 / PR #568 at the reviewed head.
# Usage: reproduce.sh <parent-checkout-with-pinned-submodules> <work-dir>
# Clones the checkout into <work-dir>, never edits the source checkout, and
# writes receipts under <work-dir>/out. Mutations run only in disposable copies.
set -euo pipefail

src=$(cd "$1" && pwd)
work=$2
head=20423082f221a02f3de72952cec4e1ac0c839b1d
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$work/out"
out=$(cd "$work/out" && pwd)

# 1. Clean clone at the exact head, processor and gPTP submodules from the pins.
rm -rf "$work/clean"
git clone -q --no-checkout "$src" "$work/clean"
git -C "$work/clean" checkout -q "$head"
for sub in protocol-processor gptp-processor; do
  git -C "$work/clean" -c protocol.file.allow=always \
    -c "submodule.$sub.url=$src/$sub" submodule update -q --init "$sub"
done
cd "$work/clean"
python3 -B scripts/audit_pp_descriptors.py --output "$out/audit.json"
python3 -B "$here/check_page_vs_receipt.py" "$out/audit.json"

# 2. The page's generator CLI boundaries for all five tracked configurations.
for c in arty_current arty_4x4 arty_8ch ax7101_1x1_tdm8 ax7101_8x8; do
  python3 -B sw/builder/endstation_builder.py "configs/endstation_$c.yaml" -o "$out/build" >/dev/null
  overlay="$out/build/endstation_$c/aem_overlay.json"
  python3 -B avdecc/gen_aem_store.py --overlay "$overlay" --out-dir "$out/store-$c" >/dev/null
  python3 -B avdecc/gen_aemi_image.py --overlay "$overlay" -o "$out/$c.bin" \
    -m "$out/$c.map" --json "$out/$c.json" >/dev/null
  printf '%s %s\n' "$c" "$(sha256sum < "$out/$c.bin" | cut -c1-64)"
done | tee "$out/cli-hashes.txt"

# 3. Identity residue through the CLI path: reset_time 0 -> 3 in a copy.
rm -rf "$work/idprobe" && cp -a "$work/clean" "$work/idprobe"
sed -i 's/^    b += be32(0)                        # reset_time/    b += be32(3)                        # reset_time/' \
  "$work/idprobe/avdecc/aem_descriptors.py"
test "$(git -C "$work/idprobe" diff --numstat | awk '{print $1}')" = 1
(cd "$work/idprobe"
 python3 -B sw/builder/endstation_builder.py configs/endstation_arty_4x4.yaml -o "$out/id-build" >/dev/null
 python3 -B avdecc/gen_aemi_image.py --overlay "$out/id-build/endstation_arty_4x4/aem_overlay.json" \
   -o "$out/id-after.bin" -m "$out/id-after.map" --json "$out/id-after.json" >/dev/null)
sha256sum "$out/arty_4x4.bin" "$out/id-after.bin" | cut -c1-64
cmp -l "$out/arty_4x4.bin" "$out/id-after.bin" || true   # 1-based offsets
cmp "$out/build/endstation_arty_4x4/aem_overlay.json" "$out/id-build/endstation_arty_4x4/aem_overlay.json" \
  && echo "overlay (model id) unchanged"

# 4. Mutations: simulated processor L10/L6 refusal, raised loader bound,
#    and a packer that normalizes the model id (must fail closed; not under -O).
packer=protocol-processor/hdl/aecp/desc/gen_desc_image.py
anchor='        key = (cfg, typ)'
mutate_packer() {
  python3 - "$1" "$anchor" "$2" <<'EOF'
import sys
path, anchor, kind = sys.argv[1:]
text = open(path).read()
assert text.count(anchor + "\n        if idx in groups") == 1
checks = {
    "l10l6": (
        "        if typ == 0x0002:\n"
        "            off, cnt = int.from_bytes(body[140:142], 'big'), int.from_bytes(body[142:144], 'big')\n"
        "            if off != 144 or cnt > 8 or len(body) != 144 + 4 * cnt:\n"
        "                raise ImageError('MUTANT L10')\n"
        "        if typ == 0x0024:\n"
        "            cnt = int.from_bytes(body[74:76], 'big')\n"
        "            if [int.from_bytes(body[76 + 2 * i:78 + 2 * i], 'big') for i in range(cnt)] != list(range(cnt)):\n"
        "                raise ImageError('MUTANT L6')\n"),
    "normalize": (
        "        if typ == 0 and body[12:20] in (bytes(8), b'\\xff' * 8):\n"
        "            body = body[:12] + bytes.fromhex('001BC50AC1000005') + body[20:]\n"),
}
open(path, "w").write(text.replace(anchor + "\n", checks[kind] + anchor + "\n", 1))
EOF
}
rm -rf "$work/mut" && cp -a "$work/clean" "$work/mut" && cd "$work/mut"
mutate_packer "$packer" l10l6
python3 -B scripts/audit_pp_descriptors.py --output "$out/M1.json"
git -C protocol-processor checkout -q -- hdl/aecp/desc/gen_desc_image.py
sed -i 's/^MAX_AUDIO_UNIT_RATES = 8/MAX_AUDIO_UNIT_RATES = 9/' sw/builder/endstation_builder.py
python3 -B scripts/audit_pp_descriptors.py --output "$out/M2.json"
git checkout -q -- sw/builder/endstation_builder.py
mutate_packer "$packer" normalize
if python3 -B scripts/audit_pp_descriptors.py --output "$out/M3.json" 2>"$out/M3.err"; then
  echo "M3: UNEXPECTED pass"; exit 1
fi
echo "M3: refused (byte-survival assertion)"
python3 -O -B scripts/audit_pp_descriptors.py --output "$out/M3-O.json"
echo "M3 under -O: exit 0 (assertions stripped)"
git -C protocol-processor checkout -q -- hdl/aecp/desc/gen_desc_image.py
python3 - "$out" <<'EOF'
import json, sys
out = sys.argv[1]
for tag in ("M1", "M2", "M3-O"):
    r = json.load(open(f"{out}/{tag}.json"))
    rows = [(p["rule"], p["probe"], p["result"]) for p in r["packer_probes"] if p["rule"] in ("L6", "L9", "L10")]
    rows += [(p["rule"], p["probe"], p["loader"], p.get("image")) for p in r["config_probes"] if p["rule"] == "L10"]
    print(tag, *rows, sep="\n  ")
EOF
