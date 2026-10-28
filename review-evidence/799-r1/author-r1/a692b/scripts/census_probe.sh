#!/usr/bin/env bash
# #799: the publication census at <rev> in a scratch clone, with the two uncontroversial census edits applied
# (src_stream_id_o in CLASS_D_PORTS; the GSI selector-2 read as a processor row), to show what remains.
# Never committed; the lane is not touched.
# usage: census_probe.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/799-a692b; C=$X/clone-census-${rev:0:8}; O=$X/r/census-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"
python3 - sw/mailbox/publication_census.py > "$O/edit.txt" <<'PY' || exit 2
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text()
a = '    "acmp_bound_dmac_o", "acmp_bound_vlan_o", "adp_next_avail_index_o",\n})'
b = '    "acmp_bound_dmac_o", "acmp_bound_vlan_o", "adp_next_avail_index_o", "src_stream_id_o",\n})'
c = '    ("pp_cd_acmp_bound_sid_w", "gsi_sid_w"): Row("processor", "", "GET_STREAM_INFO"),\n'
d = c + '    ("pp_cd_src_stream_id_w", "gsi_osid_w"): Row("processor", "", "GET_STREAM_INFO"),\n'
assert s.count(a) == 1 and s.count(c) == 1
p.write_text(s.replace(a, b).replace(c, d))
print("applied: CLASS_D_PORTS += src_stream_id_o; (pp_cd_src_stream_id_w, gsi_osid_w) -> processor")
PY
git diff > "$O/edit.diff"
$VALIDATION_STORAGE/scratch/a662/ci312/bin/python3 sw/mailbox/publication_census.py --check --jobs 4 > "$O/census.log" 2>&1; echo "census rc=$?" > "$O/rc.txt"
git checkout -- sw/mailbox/publication_census.py
echo CENSUS-DONE >> "$O/rc.txt"
