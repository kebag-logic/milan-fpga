#!/usr/bin/env bash
# Fresh checkout with no submodules: every suite inventory must fail before the
# generated preparation step, and succeed after it, through the production reader.
# Usage: fresh_inventory.sh <source-clone> <exact-head> <work-dir> <output-json>
# Submodule URLs point at the source clone's own module repositories, so the
# exact preparation command runs offline against the same pinned objects.
set -euo pipefail
src="$1"; head="$2"; work="$3"; out="$4"
rm -rf "$work"
git clone -q --no-checkout "$src" "$work"
git -C "$work" checkout -q --detach "$head"
test "$(git -C "$work" rev-parse HEAD)" = "$head"
for mod in protocol-processor gptp-processor third_party/tsn-c-stack third_party/verilog-axis; do
  test -z "$(ls -A "$work/$mod" 2>/dev/null)"
  git -C "$work" config "submodule.$mod.url" "$src/.git/modules/$mod"
done
suites="milan_dp milan_dp_mclk capture_coherence maap milan_dp_render pp_shadow"
reader='import json,sys; sys.path.insert(0,"scripts"); from ci_suite_pieces import inventory
out={}
for s in sys.argv[1:]:
    try: out[s]=len(inventory(s))
    except Exception as e: out[s]="refused: "+type(e).__name__
print(json.dumps(out))'
cd "$work"
before="$(python3 -c "$reader" $suites)"
preparation="$(python3 -c 'import sys; sys.path.insert(0,"scripts"); from ci_suite_workflows import inventory_dependencies; print(inventory_dependencies()["run"].strip())')"
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=protocol.file.allow GIT_CONFIG_VALUE_0=always bash -c "$preparation" > /dev/null 2>&1
gitlinks="$(git submodule status third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack | sed 's/ (.*//' | tr '\n' ';')"
after="$(python3 -c "$reader" $suites)"
python3 - "$out" "$head" "$preparation" "$before" "$after" "$gitlinks" <<'EOF'
import json, sys
out, head, prep, before, after, links = sys.argv[1:]
json.dump({"head": head, "preparation": prep, "before_preparation": json.loads(before),
           "after_preparation": json.loads(after), "submodule_status": links.strip(";").split(";")},
          open(out, "w"), indent=2)
EOF
cat "$out"
