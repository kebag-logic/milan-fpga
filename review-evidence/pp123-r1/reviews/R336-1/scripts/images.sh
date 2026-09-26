#!/usr/bin/env bash
# Rebuild every image the repository's build rules produce, in an exported tree,
# and print "sha256  <label>" for each. Usage: images.sh <tree> <outdir>
# The build commands are the repository's own Makefile targets and the two
# generator lines of syn/yosys/run.sh (no Verilator, no Yosys needed).
set -euo pipefail
tree=$(cd "$1" && pwd); out=$2; mkdir -p "$out"; out=$(cd "$out" && pwd)
cd "$tree"
make -s -C tb/desc_store image.bin >/dev/null
make -s -C tb/acmp_listener ltn_rom.hex >/dev/null
make -s -C tb/acmp_nvm ltn_rom.hex >/dev/null
make -s -C tb/pp_top ltn_rom.hex ucode.hex >/dev/null
make -s -C tb/ucpu ucode.hex >/dev/null
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$out/yosys_ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$out/yosys_ltn_rom.hex" >/dev/null )
for f in tb/desc_store/image.bin tb/desc_store/image.map \
         tb/acmp_listener/ltn_rom.hex tb/acmp_nvm/ltn_rom.hex \
         tb/pp_top/ltn_rom.hex tb/pp_top/ucode.hex tb/ucpu/ucode.hex; do
  cp "$f" "$out/$(echo "$f" | tr / _)"
done
# The worked example packed straight through build() with the default line size.
python3 -B - "$tree" "$out" <<'EOF'
import importlib.util, json, sys
tree, out = sys.argv[1:]
spec = importlib.util.spec_from_file_location("g", f"{tree}/hdl/aecp/desc/gen_desc_image.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
img, rep = g.build(json.load(open(f"{tree}/hdl/aecp/desc/example_milan_8.json")))
open(f"{out}/build_example_milan_8.bin", "wb").write(img)
open(f"{out}/build_example_milan_8.map", "w").write(rep)
EOF
cd "$out" && sha256sum -- * | sort -k2
