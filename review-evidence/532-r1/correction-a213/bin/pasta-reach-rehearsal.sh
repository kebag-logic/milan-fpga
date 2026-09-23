#!/usr/bin/env bash
# [A213] F1 rehearsal (after R266-1's probes/pasta_reach_sim.sh): does a slot
# namespace uplinked by pasta with the runner's EXACT pasta options reach a
# routed container address, a Docker-style published port and a host-local
# address, and do DNS and "internet" still answer, under (a) no slot table,
# (b) the head's old rule, (c) the corrected rules the candidate code emits?
#
# Everything runs inside ONE unprivileged user+network+mount namespace
# (unshare --user --map-root-user --net --mount): a fake host H, an "internet"
# netns I behind H's only default route (dev up0), a fake default-daemon
# container netns C behind a veth "bridge" br0h, and a slot netns S uplinked
# by pasta. No host interface, route, firewall or cgroup is touched and no
# packet leaves the namespaces.
#
# Fidelity limits: the runner's rules select sockets by the slot slice's
# cgroup; here pasta is the only client socket owner in H, so the rule bodies
# are loaded without the `socket cgroupv2 level 1 "<slice>"` selector (the
# only edit made to the emitted text). Docker's nat-output DNAT of a published
# port is modelled by hand at the same hook priority (dstnat).
#
# Usage: pasta-reach-rehearsal.sh WORKDIR NEW_RULES_FILE
set -euo pipefail
work=${1:?usage: pasta-reach-rehearsal.sh WORKDIR NEW_RULES_FILE}
rules=${2:?usage: pasta-reach-rehearsal.sh WORKDIR NEW_RULES_FILE}
mkdir -p "$work"
cp "$rules" "$work/new-rules.nft"
exec timeout 180 unshare --user --map-root-user --net --mount --fork -- bash -s "$work" <<'INNER'
set -euo pipefail
work=$1
mount -t tmpfs tmpfs /run
mkdir -p /run/netns
ip link set lo up
# I: the "internet" behind H's default route; 198.51.100.7 answers TCP 443,
# 198.51.100.53 answers DNS on UDP 53.
ip netns add i
ip link add up0 type veth peer name wan0 netns i
ip addr add 192.0.2.10/24 dev up0
ip link set up0 up
ip route add default via 192.0.2.1 dev up0
nsenter --net=/run/netns/i sh -c '
  ip link set lo up
  ip addr add 192.0.2.1/24 dev wan0
  ip link set wan0 up
  ip addr add 198.51.100.7/32 dev lo
  ip addr add 198.51.100.53/32 dev lo'
# C: a default-daemon container behind a host bridge; unpublished port 8080.
ip netns add c
ip link add br0h type veth peer name eth0 netns c
ip addr add 172.31.0.1/24 dev br0h
ip link set br0h up
nsenter --net=/run/netns/c sh -c '
  ip addr add 172.31.0.2/24 dev eth0
  ip link set eth0 up
  ip link set lo up
  ip route add default via 172.31.0.1'
cat >"$work/listen.py" <<'PY'
import socket, sys
host, port = sys.argv[1], int(sys.argv[2])
server = socket.create_server((host, port))
while True:
    connection, _ = server.accept()
    connection.sendall(b"hello\n")
    connection.close()
PY
cat >"$work/dns.py" <<'PY'
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("198.51.100.53", 53))
while True:
    query, peer = server.recvfrom(512)
    header = query[:2] + b"\x81\x80" + query[4:6] + b"\x00\x01\x00\x00\x00\x00"
    answer = b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04" + socket.inet_aton("198.51.100.7")
    server.sendto(header + query[12:] + answer, peer)
PY
cat >"$work/probe.py" <<'PY'
import os, socket, struct, sys
def tcp(host, port):
    try:
        with socket.create_connection((host, int(port)), timeout=4) as connection:
            return "REACHED " + connection.recv(16).decode().strip()
    except OSError as exc:
        return f"REFUSED {type(exc).__name__}"
def dns(server):
    ident = os.urandom(2)
    question = b"".join(bytes([len(p)]) + p.encode() for p in "registry.example".split(".")) + b"\x00\x00\x01\x00\x01"
    query = ident + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00" + question
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(4)
        try:
            client.sendto(query, (server, 53))
            reply, _ = client.recvfrom(512)
        except OSError as exc:
            return f"REFUSED {type(exc).__name__}"
    if reply[:2] != ident or struct.unpack("!H", reply[6:8])[0] != 1:
        return "REFUSED malformed"
    return "RESOLVED registry.example=" + socket.inet_ntoa(reply[-4:])
kind, *rest = sys.argv[1:]
print(tcp(*rest) if kind == "tcp" else dns(*rest))
PY
nsenter --net=/run/netns/c python3 "$work/listen.py" 172.31.0.2 8080 &
nsenter --net=/run/netns/i python3 "$work/listen.py" 198.51.100.7 443 &
nsenter --net=/run/netns/i python3 "$work/dns.py" &
python3 "$work/listen.py" 172.31.0.1 8082 &
nft -f - <<'NFT'
create table ip docker_publish_model
add chain ip docker_publish_model output { type nat hook output priority dstnat; policy accept; }
add rule ip docker_publish_model output ip daddr 172.31.0.1 tcp dport 9090 counter dnat to 172.31.0.2:8080
NFT
sleep 0.5
ip netns add s
nsenter --net=/run/netns/s ip link set lo up
pasta --runas 0:0 --netns-only --config-net --netns /run/netns/s \
  --tcp-ports none --udp-ports none --tcp-ns none --udp-ns none --no-map-gw \
  --pid "$work/pasta.pid" >"$work/pasta.log" 2>&1
sleep 1
echo "== H (fake host): addresses and routes; the only default route is via up0"
ip -brief addr
ip route
ip -json -4 route show default
echo "== S (slot namespace) as pasta configured it"
nsenter --net=/run/netns/s ip -brief addr
nsenter --net=/run/netns/s ip route
probes() {
  local label
  for label in \
    "container 172.31.0.2:8080 (routed via br0h, unpublished)|tcp 172.31.0.2 8080" \
    "published 172.31.0.1:9090 (host-local, DNAT to the container)|tcp 172.31.0.1 9090" \
    "host-local 172.31.0.1:8082 (bridge gateway listener)|tcp 172.31.0.1 8082" \
    "internet 198.51.100.7:443 (via the default route)|tcp 198.51.100.7 443" \
    "dns 198.51.100.53:53 (via the default route)|dns 198.51.100.53"; do
    printf '  S -> %-58s %s\n' "${label%%|*}" "$(nsenter --net=/run/netns/s python3 "$work/probe.py" ${label#*|})"
  done
}
echo "== (a) no slot table: every target is live and reachable through pasta"
probes
echo "== (b) the reviewed head's rule body only: fib daddr type local counter reject"
nft -f - <<'NFT'
create table inet slot_old
add chain inet slot_old output { type filter hook output priority filter; policy accept; }
add rule inet slot_old output fib daddr type local counter reject
NFT
probes
nft delete table inet slot_old
echo "== (c) the corrected rules as the candidate emits them (cgroup selector removed):"
sed -E 's/socket cgroupv2 level 1 "[^"]*" //' "$work/new-rules.nft" | tee "$work/new-rules-model.nft"
nft -f "$work/new-rules-model.nft"
probes
echo "== ruleset after (c)"
nft list ruleset
kill "$(cat "$work/pasta.pid")" 2>/dev/null || true
kill $(jobs -p) 2>/dev/null || true
INNER
