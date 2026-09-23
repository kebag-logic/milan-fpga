#!/usr/bin/env bash
# Review round R266-2: behaviour of the slot firewall's two output rules.
# Runs entirely inside one unprivileged user+network namespace ("host" H) with
# two child network namespaces: U (reached through the uplink "up0", the only
# default route) and C (a "container" behind the bridge "br-x", with a
# Docker-like nat-output DNAT of a port published on the bridge gateway).
# The probing process plays the slot uplink: a socket owned on the "host"
# side, inside the level-1 cgroup the rule names. No sudo, no Docker, no host
# network. Everything vanishes with the namespaces when the script exits.
# Usage: firewall_semantics_probe.sh ACT_CI_PY
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
if [ "${1:-}" != --inside ]; then
  exec unshare --user --map-root-user --net --fork bash "$0" --inside "$1"
fi
act_ci=$2
level1=$(sed -n 's|^0::/\([^/]*\)/.*|\1|p' /proc/self/cgroup)
other=system.slice
[ "$other" != "$level1" ] || other=init.scope
pids=()
cleanup() { for p in "${pids[@]}"; do kill "$p" 2>/dev/null || true; done; }
trap cleanup EXIT
listen() { python3 -c 'import socket,sys
s=socket.create_server((sys.argv[1],int(sys.argv[2])))
while True: s.accept()[0].close()' "$1" "$2" & pids+=("$!"); }
ip link set lo up
unshare --net sleep 600 & U=$!; pids+=("$U")
unshare --net sleep 600 & C=$!; pids+=("$C")
sleep 0.3
ip link add up0 type veth peer name upx
ip link set upx netns "$U"
ip addr add 192.0.2.10/24 dev up0; ip link set up0 up
ip route add default via 192.0.2.1
nsenter --net=/proc/$U/ns/net sh -c 'ip link set lo up; ip addr add 192.0.2.1/24 dev upx; ip link set upx up; ip addr add 198.51.100.7/32 dev lo'
ip link add br-x type bridge; ip addr add 172.30.0.1/24 dev br-x; ip link set br-x up
ip link add vb type veth peer name vc; ip link set vb master br-x; ip link set vb up
ip link set vc netns "$C"
nsenter --net=/proc/$C/ns/net sh -c 'ip link set lo up; ip addr add 172.30.0.2/24 dev vc; ip link set vc up; ip route add default via 172.30.0.1'
nsenter --net=/proc/$U/ns/net python3 -c 'import socket
s=socket.create_server(("0.0.0.0",8443))
while True: s.accept()[0].close()' & pids+=("$!")
nsenter --net=/proc/$C/ns/net python3 -c 'import socket
s=socket.create_server(("0.0.0.0",8080))
while True: s.accept()[0].close()' & pids+=("$!")
listen 127.0.0.1 9000
listen 172.30.0.1 9001
nft -f - <<'NFT'
table ip dockerlike {
  chain output { type nat hook output priority -100; ip daddr 172.30.0.1 tcp dport 32768 dnat to 172.30.0.2:8080; }
}
NFT
sleep 0.5
probe() {
  python3 - <<'PY'
import socket
for name, host, port in (("internet", "198.51.100.7", 8443), ("container", "172.30.0.2", 8080),
                         ("published", "172.30.0.1", 32768), ("loopback", "127.0.0.1", 9000),
                         ("gateway", "172.30.0.1", 9001)):
    try:
        socket.create_connection((host, port), timeout=3).close(); r = "reached"
    except socket.timeout: r = "timeout"
    except OSError as e: r = f"refused({e.errno})"
    print(f"{name}={r}", end=" ")
print()
PY
}
phase() {
  local label=$1 rules=$2
  nft delete table inet milan_act_slot_2 2>/dev/null || true
  if [ -n "$rules" ]; then printf '%s' "$rules" | nft -f -; fi
  printf '%-58s %s\n' "$label" "$(probe)"
}
echo "probe cgroup level 1: $level1 (control selector: $other)"
phase "A no slot table" ""
full=$(python3 "$here/pinned_firewall_text.py" "$act_ci" "$level1" up0 | sed 's/milan_act_slot_2 /milan_act_slot_2 /')
echo "--- pinned rule text as loaded in B:"; printf '%s' "$full"; echo "---"
phase "B head rules (host-local + non-uplink), selector matches" "$full"
phase "C previous head rule set (host-local only)" "$(python3 "$here/pinned_firewall_text.py" "$act_ci" "$level1" up0 --rule1-only)"
phase "D head rules, selector names another level-1 cgroup" "$(python3 "$here/pinned_firewall_text.py" "$act_ci" "$other" up0)"
nft list table inet milan_act_slot_2 | sed -n '/counter/p'
