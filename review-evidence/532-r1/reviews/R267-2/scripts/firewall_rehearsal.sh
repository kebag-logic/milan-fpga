#!/usr/bin/env bash
# Reviewer rehearsal (round R267-2, PR #533): the replay-slot firewall's rule
# text, applied in an unprivileged user+net+mount namespace that stands in for
# the build host. No Docker, no act, no sudo, no host network change.
#
# Topology inside the stand-in host namespace H:
#   up0      the only default-route interface (the uplink), to netns I
#            ("internet": 203.0.113.10:443, and a LAN neighbour 198.51.100.1:80)
#   br0      a bridge like a Docker network, 172.30.0.1/24, with netns C
#            ("container": 172.30.0.2:8080) behind it, and a Docker-style
#            nat-output DNAT publishing 172.30.0.1:32768 -> 172.30.0.2:8080
#   vm0      a routed veth to netns V ("VM network": 192.0.2.2:22)
#   H itself listens on 172.30.0.1:9000 (a host service on a bridge gateway)
# netns S is the slot namespace, connected by pasta with the runner's exact
# options. pasta runs in a child cgroup of this session's own delegated cgroup,
# and the rules select that cgroup with `socket cgroupv2 level <depth>`, so the
# host-side probe is outside the selector exactly as on the real host.
#
# Phases: no slot table; the head's parent rule text (one rule, a37af3c6);
# the head's rule text (two rules, f5497170). Each phase probes every target
# from inside S and from H.
#
# usage: firewall_rehearsal.sh OUTDIR   (run as the invoking user)
set -euo pipefail
out=${1:?usage: firewall_rehearsal.sh OUTDIR}
mkdir -p "$out"
own=$(sed -n 's/^0:://p' /proc/self/cgroup)
selcg=/sys/fs/cgroup${own}/r267-slot-selector
mkdir "$selcg"
cleanup() { rmdir "$selcg" 2>/dev/null || true; }
trap cleanup EXIT
rel=${own#/}/r267-slot-selector
depth=$(printf '%s\n' "$rel" | awk -F/ '{print NF}')
export SELCG=$selcg SELREL=$rel SELDEPTH=$depth OUT=$out

unshare --user --map-root-user --net --mount --pid --fork --mount-proc -- bash -euo pipefail -c '
mount -t tmpfs tmpfs /run
mkdir -p /run/netns
ip link set lo up
LISTEN="import socket,sys
s=socket.create_server((sys.argv[1],int(sys.argv[2])))
while True: s.accept()[0].close()"
PROBE="import socket,sys
out=[]
for spec in sys.argv[1:]:
    n,h,p=spec.split(\",\")
    try:
        socket.create_connection((h,int(p)),timeout=3).close(); out.append(n+\"=reached\")
    except OSError as e:
        out.append(n+\"=refused\")
print(\" \".join(out))"
# internet / LAN neighbour
ip netns add I
ip link add up0 type veth peer name upx
ip link set upx netns I
ip addr add 198.51.100.2/24 dev up0; ip link set up0 up
ip -n I addr add 198.51.100.1/24 dev upx; ip -n I link set upx up; ip -n I link set lo up
ip -n I addr add 203.0.113.10/32 dev lo
ip route add default via 198.51.100.1 dev up0
# Docker-like bridge network with one container
ip netns add C
ip link add br0 type bridge; ip addr add 172.30.0.1/24 dev br0; ip link set br0 up
ip link add c0 type veth peer name c1; ip link set c1 netns C; ip link set c0 master br0; ip link set c0 up
ip -n C addr add 172.30.0.2/24 dev c1; ip -n C link set c1 up; ip -n C link set lo up
ip -n C route add default via 172.30.0.1
# a routed VM-style network
ip netns add V
ip link add vm0 type veth peer name vmx; ip link set vmx netns V
ip addr add 192.0.2.1/24 dev vm0; ip link set vm0 up
ip -n V addr add 192.0.2.2/24 dev vmx; ip -n V link set vmx up; ip -n V link set lo up
ip -n V route add default via 192.0.2.1
# listeners
nsenter --net=/run/netns/I python3 -c "$LISTEN" 203.0.113.10 443 &
nsenter --net=/run/netns/I python3 -c "$LISTEN" 198.51.100.1 80 &
nsenter --net=/run/netns/C python3 -c "$LISTEN" 0.0.0.0 8080 &
nsenter --net=/run/netns/V python3 -c "$LISTEN" 192.0.2.2 22 &
python3 -c "$LISTEN" 172.30.0.1 9000 &
# Docker-style published port: nat output DNAT of a host-local destination
nft -f - <<EOF
table ip dockerlike {
  chain output { type nat hook output priority -100; policy accept;
    fib daddr type local ip daddr 172.30.0.1 tcp dport 32768 dnat to 172.30.0.2:8080
  }
  chain postrouting { type nat hook postrouting priority 100; policy accept; }
}
EOF
sleep 1
# slot namespace and pasta uplink, pasta placed in the selector cgroup
ip netns add milan-act-slot-9
ip -n milan-act-slot-9 link set lo up
( echo $BASHPID > "$SELCG/cgroup.procs"; exec pasta --runas 0:0 --netns-only --config-net \
    --netns /run/netns/milan-act-slot-9 --tcp-ports none --udp-ports none --tcp-ns none \
    --udp-ns none --no-map-gw --pid /run/milan-act-slot-9-net.pid ) > "$OUT/pasta.log" 2>&1
sleep 1
pasta_pid=$(cat /run/milan-act-slot-9-net.pid)
echo "pasta pid $pasta_pid cgroup $(cat /proc/$pasta_pid/cgroup)" >> "$OUT/pasta.log"
# uplinks, read the way the runner reads them (unicast default routes)
uplinks=$(ip -json -4 route show default | python3 -c "
import json,sys
names=[]
for r in json.load(sys.stdin):
    if r.get(\"type\",\"unicast\")!=\"unicast\": continue
    for h in r.get(\"nexthops\",[r]):
        if h[\"dev\"] not in names: names.append(h[\"dev\"])
print(\", \".join(\"\\\"%s\\\"\" % n for n in names))")
sel="socket cgroupv2 level $SELDEPTH \"$SELREL\""
T="inet milan_act_slot_9"
targets="container,172.30.0.2,8080 published,172.30.0.1,32768 hostsvc,172.30.0.1,9000 vmnet,192.0.2.2,22 lan,198.51.100.1,80 internet,203.0.113.10,443"
phase() {
  echo "== $1"
  echo "slot: $(nsenter --net=/run/netns/milan-act-slot-9 python3 -c "$PROBE" $targets)"
  echo "host: $(python3 -c "$PROBE" $targets)"
}
{
echo "kernel $(uname -r); $(pasta --version | head -1); $(nft --version)"
echo "selector: $sel"
echo "uplinks: $uplinks"
echo "slot routes: $(nsenter --net=/run/netns/milan-act-slot-9 ip -4 route show | tr "\n" ";")"
phase "no slot table"
printf "%s\n" "create table $T" "add chain $T output { type filter hook output priority filter; policy accept; }" \
  "add rule $T output $sel fib daddr type local counter reject" > /run/old.nft
nft -f /run/old.nft
echo "--- rules loaded (parent head a37af3c6 text, selector adapted):"; cat /run/old.nft
phase "one rule (a37af3c6)"
nft list table $T | grep counter
nft delete table $T
printf "%s\n" "create table $T" "add chain $T output { type filter hook output priority filter; policy accept; }" \
  "add rule $T output $sel fib daddr type local counter reject" \
  "add rule $T output $sel oifname != { $uplinks } counter reject" > /run/new.nft
nft -f /run/new.nft
echo "--- rules loaded (head f5497170 text, selector adapted):"; cat /run/new.nft
phase "two rules (f5497170)"
echo "--- counters after the two-rule phase:"
nft list table $T | grep counter
echo "--- create over an existing table fails whole:"
nft -f /run/new.nft 2>&1 | head -2 || true
} > "$OUT/rehearsal.txt" 2>&1
kill $pasta_pid 2>/dev/null || true
kill $(jobs -p) 2>/dev/null || true
'
cat "$out/rehearsal.txt"
