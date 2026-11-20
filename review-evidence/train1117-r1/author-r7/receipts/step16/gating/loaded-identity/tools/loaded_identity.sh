#!/bin/bash
# loaded_identity.sh OUT: loaded_identity.py at 1x1/1if and 8x8/1if (R866-4-F1), each gating bench image's firmware
# (the ELF its manifest binds, in the gating clone) against the product image the ROM ledger links at that point
# (plat_ledger.py --self-test's 1x1-if1 and 8x8-if1), into OUT/<point>.txt; then each link's toolchain into
# OUT/toolchains.txt. Exit 0 when both points pass. Run it as
#   bash loaded_identity.sh OUT > OUT/loaded-identity.log 2>&1; echo $? > OUT/loaded-identity.log.rc
# SCRATCH is the lane's scratch (the gating chains' gate15/, the gates' r9gates/), PYTHON the product venv's python3.
set -u
S=${SCRATCH:-<scratch>}
PY=${PYTHON:-<home>/litex-milan/venv/bin/python3}
OUT=$1; mkdir -p "$OUT"
echo "loaded_identity.sh $(date -Iseconds)"
rc=0
for spec in 1x1/1if:g1x1:endstation_ax7101_1x1_tdm8:1x1-if1 8x8/1if:g8x8:endstation_ax7101_8x8:8x8-if1; do
  IFS=: read -r point g stem led <<< "$spec"
  C=$S/gate15/clones/$g W=$S/gate15/work/$g L=$S/r9gates/led/pl/$led
  echo "== $point: head $(git -C "$C" rev-parse HEAD), clone clean: $(git -C "$C" status --porcelain --untracked-files=no | wc -l) changes"
  "$PY" -I "$S/tools/loaded_identity.py" --repo "$C" --point "$point" \
    --gating-elf "$C/sw/builder/out/$stem/ctrl_app.elf" --product-elf "$L/ctrl_app.elf" \
    --build "$W/build_ExtraPostPlacementOpt" --artifacts "$W/artifacts.sha256" \
    --gating-objects "$W/image" --product-objects "$L" > "$OUT/${g#g}.txt" 2>&1
  r=$?
  echo "$point rc=$r: $(tail -1 "$OUT/${g#g}.txt")"
  [ $r = 0 ] || rc=1
done
# planted controls at 1x1/1if, each of which the check must refuse by name: the product ELF with one byte of .rodata
# flipped (loaded and rom-words must fail), and the artifact list with the bitstream's digest altered (manifest)
P=$S/tmp/loaded-identity-plants; rm -rf "$P"; mkdir -p "$P"
C=$S/gate15/clones/g1x1 W=$S/gate15/work/g1x1 L=$S/r9gates/led/pl/1x1-if1
"$PY" -I - "$L/ctrl_app.elf" "$P/flipped.elf" "$W/artifacts.sha256" "$P/artifacts.sha256" <<'PYEOF'
import struct, sys
b = bytearray(open(sys.argv[1], 'rb').read())
shoff, = struct.unpack_from('<I', b, 0x20); shentsize, shnum, shstrndx = struct.unpack_from('<HHH', b, 0x2e)
S = [struct.unpack_from('<IIIIIIIIII', b, shoff + k * shentsize) for k in range(shnum)]
names = b[S[shstrndx][4]:S[shstrndx][4] + S[shstrndx][5]]
ro = next(s for s in S if names[s[0]:names.index(0, s[0])] == b'.rodata')
b[ro[4] + ro[5] // 2] ^= 0x01
open(sys.argv[2], 'wb').write(b)
lines = open(sys.argv[3]).read().splitlines()
lines = [('0' * 64 + l[64:]) if l.endswith('alinx_ax7101.bit') else l for l in lines]
open(sys.argv[4], 'w').write('\n'.join(lines) + '\n')
print(f'planted: .rodata byte at file offset {ro[4] + ro[5] // 2} flipped; the bitstream digest zeroed in the list')
PYEOF
plant() {  # plant NAME EXPECT... -- ARGS: refused when the run exits 1 and prints every expected CHECK line
  local name=$1; shift; local want=(); while [ "$1" != -- ]; do want+=("$1"); shift; done; shift
  "$PY" -I "$S/tools/loaded_identity.py" --repo "$C" --point "1x1/1if (plant: $name)" "$@" > "$P/$name.txt" 2>&1
  local r=$? ok=1
  for w in "${want[@]}"; do grep -qx "CHECK $w: FAIL" "$P/$name.txt" || ok=0; done
  [ $r = 1 ] && [ $ok = 1 ] && echo "PLANT $name: refused (rc=$r; ${want[*]} FAIL)" || { echo "PLANT $name: ESCAPED (rc=$r)"; rc=1; }
}
base=(--gating-elf "$C/sw/builder/out/endstation_ax7101_1x1_tdm8/ctrl_app.elf" --build "$W/build_ExtraPostPlacementOpt")
plant loaded-byte-flipped loaded rom-words -- "${base[@]}" --product-elf "$P/flipped.elf" --artifacts "$W/artifacts.sha256"
plant bitstream-digest-altered manifest -- "${base[@]}" --product-elf "$L/ctrl_app.elf" --artifacts "$P/artifacts.sha256"
# the toolchain each link used: the gating chain's (gate15/tools/env.sh, the gating lane's pinned SDK) and the
# ledger's (bin/env.sh, the lane's SDK)
{
  for side in "gating:$(sed -n 's/.*SDK=\([^ ;]*\).*/\1/p' "$S/gate15/tools/env.sh" | head -1)" \
              "ledger:$(sed -n 's#.*:\(/[^:]*br-milan-rv32\)/host/bin.*#\1#p' "$S/bin/env.sh" | head -1)"; do
    name=${side%%:*} sdk=${side#*:}
    echo "$name SDK $sdk"
    for t in gcc as ld; do echo "  $t: $("$sdk/host/bin/riscv32-buildroot-linux-gnu-$t" --version | head -1)"; done
  done
} > "$OUT/toolchains.txt" 2>&1
cat "$OUT/toolchains.txt"
echo "END rc=$rc $(date -Iseconds)"
exit $rc
