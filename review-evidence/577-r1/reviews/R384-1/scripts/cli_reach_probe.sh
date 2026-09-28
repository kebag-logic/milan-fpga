#!/bin/sh
# Does the PR's "How to reproduce" builder CLI reach validate_shipping_image?
# Builds a farm, makes the checker raise unconditionally, runs the CLI.
# Usage: cli_reach_probe.sh <checkout> <scratch>
set -u
here=$(cd "$(dirname "$0")" && pwd)
sh "$here/make_farm.sh" "$1" "$2/farm_cli"
# The CLI writes these generated paths; make them real copies so nothing is
# written through a symlink into the source checkout.
for d in configs/generated hdl/common/csr/gen; do
  rm -rf "$2/farm_cli/$d"; cp -rL "$1/$d" "$2/farm_cli/$d"
done
python3 - "$2/farm_cli/sw/builder/aem_image_checks.py" <<'PY'
import sys; p = sys.argv[1]; t = open(p).read()
old = "    list_offset, walk_count = _sampling_rate_walk()\n"
assert t.count(old) == 1
open(p, "w").write(t.replace(old, "    raise ImageCheckError('PROBE_REACHED: checker was called')\n" + old))
PY
cd "$2/farm_cli" && python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml -o "$2/cli_out" > "$2/cli_stdout.txt" 2>&1
echo "builder CLI rc=$?"
grep -c PROBE_REACHED "$2/cli_stdout.txt" | sed 's/^/PROBE_REACHED lines in CLI output: /'
ls "$2/cli_out"/*/ 2>/dev/null | grep -c 'aem_desc' | sed 's/^/aem_desc* files emitted by CLI: /'
python3 - "$2/farm_cli" <<'PY'
import os, sys
root = sys.argv[1]; sys.path.insert(0, os.path.join(root, "sw", "builder")); os.chdir(root)
import endstation_builder as eb
cfg = eb.load_config("configs/endstation_arty_current.yaml")
try:
    eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg)); print("control _entity_model_image: checker NOT reached")
except eb.ConfigError as e:
    print("control _entity_model_image:", str(e)[:60])
PY
