#!/bin/sh
# run_r732_nonadv.sh TREE PATCH SCRATCH VERILATOR : R732-2's non-advertising probe on a copy of
# TREE, as its generator builds it: the method (the patch's second hunk) and the call added
# after the first `    every_slot_taken_at_the_shutdown();` (its first-occurrence replace)
set -u
W=$(mktemp -d -p "$3"); cp -a "$1"/. "$W"/; rm -rf "$W/tb/pp_top/obj_dir"
(cd "$W" && patch -p1 -F0 --no-backup-if-mismatch -r - < "$2"); echo "apply rc=$? (hunk 1 is re-made below)"
python3 -I -c '
import sys; p=sys.argv[1]; t=open(p).read()
a="    every_slot_taken_at_the_shutdown();"
assert "void nonadvertising_pending_frame_probe()" in t and "    nonadvertising_pending_frame_probe();" not in t
t=t.replace(a, a+"\n    nonadvertising_pending_frame_probe();", 1); open(p,"w").write(t)' "$W/tb/pp_top/sim_main.cpp"
echo "call rc=$?"; grep -n "nonadvertising_pending_frame_probe" "$W/tb/pp_top/sim_main.cpp"
make -C "$W/tb/pp_top" reboot VERILATOR="$4"; echo "make rc=$?"
rm -rf "$W"
