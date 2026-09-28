#!/bin/sh
# Round 2: does the PR body's "How to reproduce" command reach validate_shipping_image?
#  1. run the PR body's exact heredoc from a farm root (checker intact)      -> expect rc 0
#  2. same, with the checker forced to raise PROBE_REACHED on every call     -> expect rc != 0, PROBE_REACHED
#  3. control from round 1: the builder CLI with the forced checker          -> documented as not emitting the image
# Usage: cli_reach_probe.sh <checkout> <scratch>
set -u
here=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
repro() {  # the PR #612 body's reproduction block, verbatim
python3 - <<'PYTHON'
import sys
sys.path.insert(0, "sw/builder")
from test_builder import test_shipping_image_contract, test_soc_shipping_image_contract
test_shipping_image_contract()
test_soc_shipping_image_contract()
PYTHON
}
sh "$here/make_farm.sh" "$1" "$2/farm_repro"
(cd "$2/farm_repro" && repro > "$2/repro_intact.txt" 2>&1); echo "1. PR reproduction, checker intact: rc=$?"
grep -c 'gate 36b' "$2/repro_intact.txt" | sed 's/^/   gate 36b lines: /'
python3 - "$2/farm_repro/sw/builder/aem_image_checks.py" <<'PY'
import sys; p = sys.argv[1]; t = open(p).read()
old = "    list_offset, walk_count = _sampling_rate_walk()\n"
assert t.count(old) == 1
open(p, "w").write(t.replace(old, "    raise ImageCheckError('PROBE_REACHED: checker was called')\n" + old))
PY
(cd "$2/farm_repro" && repro > "$2/repro_forced.txt" 2>&1); echo "2. PR reproduction, checker forced to raise: rc=$?"
grep -c PROBE_REACHED "$2/repro_forced.txt" | sed 's/^/   PROBE_REACHED lines: /'
tail -1 "$2/repro_forced.txt" | cut -c1-160 | sed 's/^/   last line: /'
# 3. round-1 control: the builder CLI (generated paths copied so nothing is written into the checkout)
for d in configs/generated hdl/common/csr/gen; do
  rm -rf "$2/farm_repro/$d"; cp -rL "$1/$d" "$2/farm_repro/$d"
done
rm -rf "$2/cli_out"
(cd "$2/farm_repro" && python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml -o "$2/cli_out" > "$2/cli_stdout.txt" 2>&1); echo "3. builder CLI, checker forced: rc=$?"
grep -c PROBE_REACHED "$2/cli_stdout.txt" | sed 's/^/   PROBE_REACHED lines in CLI output: /'
ls "$2/cli_out"/*/ 2>/dev/null | grep -c 'aem_desc' | sed 's/^/   aem_desc* files emitted by CLI: /'
