#!/usr/bin/env bash
# Real-kernel control: OOM-kill a 400 MiB allocation in a 200 MiB scope below a
# fresh user slice, then read that slice with the head's and dev's slot readers
# (imported from read-only copies; no runner command is executed).
# Usage: real_oom_control.sh <clone> <scratch-dir>
set -u
clone="$1"; scratch="$2"
mkdir -p "$scratch/head" "$scratch/dev"
git -C "$clone" show f643377f15c0d939d875ae5698672f1b0a99a644:scripts/act_ci.py > "$scratch/head/act_ci.py"
git -C "$clone" show 84f9e3001b7d9b77835c4a9a599dbe6230a8031b:scripts/act_ci.py > "$scratch/dev/act_ci.py"
slice="r636probe$$.slice"
base="$(sed -n 's/^0:://p' /proc/self/cgroup)"
mgr="${base%%/app.slice/*}"
# A sleeper keeps the slice alive while it is read.
systemd-run --user --slice="$slice" --unit="r636probe-sleeper-$$" -q sleep 120
systemd-run --user --slice="$slice" --scope -q -p MemoryMax=200M -p MemorySwapMax=0 -p OOMPolicy=continue \
  python3 -I -c 'b = bytearray(400 * 2**20)'
echo "allocating job rc=$?"
rel="${mgr#/}/$slice"
dir="/sys/fs/cgroup/$rel"
echo "slice cgroup: $dir"
echo "memory.events: $(tr '\n' ' ' < "$dir/memory.events")"
echo "memory.events.local: $(tr '\n' ' ' < "$dir/memory.events.local")"
for which in dev head; do
  python3 -I - "$scratch/$which" "$rel" "$which" <<'EOF'
import sys, types
sys.path.insert(0, sys.argv[1])
import act_ci
slot = types.SimpleNamespace(number=1, slice_unit=sys.argv[2])
host = act_ci.SlotHost()
which = sys.argv[3]
try:
    if which == "dev":
        print("dev 84f9e300:", act_ci.require_slot_memory_cap_unexhausted(slot, host))
    else:
        memory = act_ci.read_slot_memory(slot, host)
        print("head f643377f:", memory.report(), "; exhausted =", memory.exhausted)
        print("head f643377f evidence:", memory.evidence())
        print("head f643377f refusal:", memory.refusal())
except act_ci.Refusal as exc:
    print(which, "Refusal:", exc)
EOF
done
systemctl --user stop "r636probe-sleeper-$$.service" "$slice" 2>/dev/null
echo "slice stopped: $(systemctl --user show -p ActiveState --value "$slice")"
