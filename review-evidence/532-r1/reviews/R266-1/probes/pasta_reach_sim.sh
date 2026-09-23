#!/usr/bin/env bash
# R266-1 probe: does a slot namespace uplinked by pasta, with the runner's
# pinned "fib daddr type local counter reject" output rule, reach a routed
# NON-local address (a container IP behind a host bridge) while the rule
# rejects the host-local bridge gateway?
#
# Runs entirely inside an unprivileged user+network+mount namespace: a fake
# "host" netns H (dummy uplink 192.0.2.10/24, default via 192.0.2.1), a fake
# default-daemon container netns C behind a veth "bridge" (H side 172.31.0.1,
# C side 172.31.0.2), and a fake slot netns S uplinked by pasta with the
# runner's exact pasta options. No host interface, route or firewall is
# touched and nothing leaves the namespaces.
#
# Fidelity limit: the runner's rule selects sockets by the slot slice's
# cgroup; here pasta is the only client socket owner in H, so the same rule
# body is applied without the cgroup selector. The published-port case
# models Docker's nat OUTPUT DNAT (priority dstnat, before filter).
set -euo pipefail
work=${1:?usage: pasta_reach_sim.sh WORKDIR}
mkdir -p "$work"
exec timeout 120 unshare --user --map-root-user --net --mount --fork -- bash -s "$work" <<'INNER'
set -euo pipefail
work=$1
mount -t tmpfs tmpfs /run
mkdir -p /run/netns
ip link set lo up
ip link add up0 type dummy
ip addr add 192.0.2.10/24 dev up0
ip link set up0 up
ip route add default via 192.0.2.1 dev up0
ip netns add c
ip link add br0h type veth peer name eth0 netns c
ip addr add 172.31.0.1/24 dev br0h
ip link set br0h up
nsenter --net=/run/netns/c ip addr add 172.31.0.2/24 dev eth0
nsenter --net=/run/netns/c ip link set eth0 up
nsenter --net=/run/netns/c ip link set lo up
nsenter --net=/run/netns/c ip route add default via 172.31.0.1
cat >"$work/listen.py" <<'PY'
import socket, sys
host, port, reply = sys.argv[1], int(sys.argv[2]), sys.argv[3].encode()
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port)); s.listen(8)
while True:
    c, _ = s.accept(); c.sendall(reply + b"\n"); c.close()
PY
cat >"$work/connect.py" <<'PY'
import socket, sys
try:
    s = socket.create_connection((sys.argv[1], int(sys.argv[2])), timeout=5)
    print("REACHED", s.recv(64).decode().strip())
except OSError as exc:
    print("BLOCKED", type(exc).__name__, exc.errno)
PY
nsenter --net=/run/netns/c python3 "$work/listen.py" 172.31.0.2 8080 container-listener &
python3 "$work/listen.py" 172.31.0.1 8082 host-bridge-gateway-listener &
sleep 0.5
ip netns add s
nsenter --net=/run/netns/s ip link set lo up
pasta --runas 0:0 --netns-only --config-net --netns /run/netns/s \
  --tcp-ports none --udp-ports none --tcp-ns none --udp-ns none --no-map-gw \
  --pid "$work/pasta.pid" >"$work/pasta.log" 2>&1
sleep 1
echo "== fake host H: addresses and routes"
ip -brief addr; ip route
echo "== slot netns S as pasta configured it"
nsenter --net=/run/netns/s ip -brief addr; nsenter --net=/run/netns/s ip route
probe() {
  printf '%-44s ' "$1"
  nsenter --net=/run/netns/s python3 "$work/connect.py" "$2" "$3"
}
echo "== control: no slot firewall table"
probe "S -> host-local bridge gateway 172.31.0.1" 172.31.0.1 8082
probe "S -> routed container IP 172.31.0.2" 172.31.0.2 8080
nft -f - <<'NFT'
create table inet sim_slot
add chain inet sim_slot output { type filter hook output priority filter; policy accept; }
add rule inet sim_slot output fib daddr type local counter reject
NFT
echo "== with the runner's rule body (fib daddr type local counter reject)"
probe "S -> host-local bridge gateway 172.31.0.1" 172.31.0.1 8082
probe "S -> routed container IP 172.31.0.2" 172.31.0.2 8080
echo "== plus a Docker-style published port: nat output DNAT 172.31.0.1:9090 -> 172.31.0.2:8080"
nft -f - <<'NFT'
create table ip sim_publish
add chain ip sim_publish output { type nat hook output priority dstnat; policy accept; }
add rule ip sim_publish output ip daddr 172.31.0.1 tcp dport 9090 counter dnat to 172.31.0.2:8080
NFT
probe "S -> host-local 172.31.0.1:9090 (published)" 172.31.0.1 9090
probe "S -> host-local 172.31.0.1:8082 (unpublished)" 172.31.0.1 8082
nft list ruleset
kill "$(cat "$work/pasta.pid")" 2>/dev/null || true
kill %1 %2 2>/dev/null || true
INNER
