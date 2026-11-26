#!/bin/sh
# usage: probe_shadow_unsent_pair.sh <repo> <out-dir> [VERILATOR=<path>]
# Reviewer probe for gptp_shadow phase 22: build the harness with the graded
# Sync/Follow_Up pair of each delay trial NOT sent, and run it. A check that
# claims "the next Follow_Up is used" must fail when no Follow_Up is sent.
# The copy sits at the suite's own depth (its Makefile uses relative paths)
# and is removed afterwards; no tracked file is touched.
repo=$1; out=$2; shift 2
d=$repo/tb/verilator/r937_probe_shadow
rm -rf "$d"; mkdir -p "$d"
cp "$repo/tb/verilator/gptp_shadow/Makefile" "$repo/tb/verilator/gptp_shadow/sim_main.cpp" \
   "$repo/tb/verilator/gptp_shadow/gptp_shadow_wrap.sv" "$d/"
anchor='    gm_pair_on_link(m, used_delay(d));'
[ "$(grep -cxF "$anchor" "$d/sim_main.cpp")" = 1 ] || { echo "anchor not unique"; rm -rf "$d"; exit 2; }
sed -i "s#^$anchor\$#    /* r937 probe: the graded pair is not sent */#" "$d/sim_main.cpp"
diff "$repo/tb/verilator/gptp_shadow/sim_main.cpp" "$d/sim_main.cpp" > "$out/probe_shadow_unsent_pair.diff"
(cd "$d" && make run "$@") > "$out/probe_shadow_unsent_pair_full.log" 2>&1
rc=$?
grep -E '^FAIL|^[0-9]+ checks' "$out/probe_shadow_unsent_pair_full.log" > "$out/probe_shadow_unsent_pair.txt"
echo "make run rc=$rc" >> "$out/probe_shadow_unsent_pair.txt"
rm -rf "$d"
