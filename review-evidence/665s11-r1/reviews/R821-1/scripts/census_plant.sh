#!/bin/sh
# census_plant.sh CHECKOUT OUT NAME 'NEW LINE': the census's --check on a copy of milan_datapath.sv whose split
# REBOOT line reads NEW LINE; the log in OUT/NAME.log. Needs SV2V and YOSYS set to the pinned tools.
checkout=$1; out=$2; name=$3; new=$4
mkdir -p "$out"
old='    assign pp_reboot_req_w      = i_reboot_req;'
python3 - "$checkout/hdl/milan/milan_datapath.sv" "$out/$name.sv" "$old" "$new" <<'EOF'
import sys
src, dst, old, new = sys.argv[1:]
text = open(src).read()
assert text.count(old) == 1, text.count(old)
open(dst, 'w').write(text.replace(old, new))
EOF
cd "$checkout" && "$LITEX_PY" sw/mailbox/publication_census.py --check --jobs 6 --datapath "$out/$name.sv" > "$out/$name.log" 2>&1
echo "$name rc=$?"
grep -n 'reboot_req' "$out/$name.log" | cut -c1-300 | head -6
