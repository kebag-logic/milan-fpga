#!/usr/bin/env bash
# [A203] Hand-typed rehearsal of the exact host argv scripts/act_ci.py pins for
# an isolated slot, with scratch names (stem a203-rh) instead of
# milan-act-slot-N, a scratch data-root and pool 10.232.0.0/24. Nothing here
# runs the candidate runner. Order and flags follow slot_uplink_command,
# slot_firewall_rules, slot_daemon_command, acquire_replay_slot and
# release_replay_slot at the reviewed head.
set -euo pipefail
stem=a203-rh
table=a203_rh
slice=a203_rh.slice
netns=/run/netns/$stem
runtime=/run/$stem
pidfile=/run/$stem-net.pid
root=$REVIEWS/532-a203-packet/scratch/rh-root
token=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
scratch=$(mktemp -d)
sudo_run() { sudo -n -- "$@"; }
docker_slot() { sudo -n -- env -i PATH=/usr/bin:/bin HOME="$scratch" DOCKER_HOST="unix://$runtime/docker.sock" /usr/bin/docker "$@"; }

echo "== acquisition"
sudo_run install -d -m 0755 -o root -g root "$root"
sudo_run /usr/bin/ip netns add "$stem"
sudo_run /usr/bin/ip -n "$stem" link set lo up
sudo_run /usr/bin/systemctl set-property --runtime "$slice" MemoryMax=24G MemorySwapMax=0
sudo_run /usr/bin/systemd-run "--unit=$stem-net.service" --collect "--slice=$slice" \
  --property=Type=forking "--property=PIDFile=$pidfile" -- /usr/bin/pasta --runas 0:0 \
  --netns-only --config-net --netns "$netns" --tcp-ports none --udp-ports none \
  --tcp-ns none --udp-ns none --no-map-gw --pid "$pidfile"
cgroup=$(systemctl show --property=ControlGroup --value "$slice")
echo "slice cgroup: $cgroup"
[ "$cgroup" = "/$slice" ]
cat >"$scratch/$table.nft" <<EOF
create table inet $table
add chain inet $table output { type filter hook output priority filter; policy accept; }
add rule inet $table output socket cgroupv2 level 1 "$slice" fib daddr type local counter reject
EOF
sudo_run /usr/bin/nft -f "$scratch/$table.nft"
sudo_run /usr/bin/systemd-run "--unit=$stem-dockerd.service" --collect "--slice=$slice" \
  --property=Type=notify "--property=NetworkNamespacePath=$netns" \
  --property=TemporaryFileSystem=/run/containerd "--property=RuntimeDirectory=$stem" \
  --property=Delegate=yes --property=LimitNOFILE=infinity --property=LimitNPROC=infinity \
  --property=TasksMax=infinity --property=TimeoutStartSec=300 --property=TimeoutStopSec=300 \
  -- /usr/bin/dockerd --config-file /dev/null --data-root "$root/slot-rh" \
  --exec-root "$runtime/exec" --host "unix://$runtime/docker.sock" \
  --pidfile "$runtime/dockerd.pid" --containerd-namespace "$stem" \
  --containerd-plugins-namespace "$stem-plugins" --bridge none \
  --default-address-pool base=10.232.0.0/24,size=24 --exec-opt native.cgroupdriver=systemd \
  --cgroup-parent "$slice" --feature containerd-snapshotter=true \
  --label org.kebag-logic.milan-act-ci.slot=rh --label "org.kebag-logic.milan-act-ci.owner=$token"

echo "== identity (what verify_slot_daemon_identity reads)"
docker_slot info --format '{{json .Labels}} {{.DockerRootDir}} {{.CgroupDriver}} {{json .DriverStatus}}'
systemd-cgls -u "$stem-dockerd.service" --no-pager | head -4

echo "== one job-shaped container through the slot namespace"
listener_port_file=$(mktemp)
python3 -u -c 'import socket,time;s=socket.socket();s.bind(("0.0.0.0",0));s.listen();print(s.getsockname()[1],flush=True);time.sleep(90)' >"$listener_port_file" &
listener=$!
sleep 1
port=$(cat "$listener_port_file")
network=$(sudo -n -- nsenter "--net=$netns" -- env -i PATH=/usr/bin:/bin HOME="$scratch" \
  DOCKER_HOST="unix://$runtime/docker.sock" /usr/bin/docker network create --driver bridge \
  --label "org.kebag-logic.milan-act-ci.owner=$token" "milan-act-ci-$token")
echo "network $network"
docker_slot pull -q ubuntu:24.04
docker_slot run --rm --network "milan-act-ci-$token" \
  --label "org.kebag-logic.milan-act-ci.owner=$token" --cpuset-cpus=4-7 --memory=16g \
  --memory-swap=16g ubuntu:24.04 bash -c "
cat /sys/fs/cgroup/cpuset.cpus.effective; nproc
getent hosts github.com >/dev/null && echo dns-ok || echo dns-FAIL
(exec 3<>/dev/tcp/140.82.121.3/443) 2>/dev/null && echo internet-ok || echo internet-FAIL
(exec 3<>/dev/tcp/172.17.0.1/$port) 2>/dev/null && echo HOST-LOCAL-REACHED || echo host-local-rejected
(exec 3<>/dev/tcp/127.0.0.1/$port) 2>/dev/null && echo LOOPBACK-REACHED || echo loopback-isolated
" || true
cid_scope=$(systemctl list-units --no-legend --plain "docker-*.scope" | awk '{print $1}' | head -1 || true)
echo "container scopes now: ${cid_scope:-none left (run --rm)}"
sudo_run /usr/bin/nft list table inet "$table" | grep counter
docker_slot network rm "milan-act-ci-$token" >/dev/null
kill "$listener" 2>/dev/null || true

echo "== teardown in release_replay_slot order, with its absence proofs"
sudo_run /usr/bin/systemctl stop "$stem-dockerd.service" || true
echo "daemon LoadState=$(systemctl show --property=LoadState --value "$stem-dockerd.service")"
[ -e "$runtime" ] && echo "RUNTIME DIR SURVIVED" || echo "runtime dir absent"
sudo_run /usr/bin/systemctl stop "$stem-net.service" || true
echo "uplink LoadState=$(systemctl show --property=LoadState --value "$stem-net.service")"
sudo_run test -e "$pidfile" && echo "PIDFILE SURVIVED" || echo "pidfile absent"
sudo_run /usr/bin/systemctl stop "$slice" || true
sudo_run /usr/bin/systemctl revert "$slice" || true
echo "slice ActiveState=$(systemctl show --property=ActiveState --value "$slice") DropInPaths=[$(systemctl show --property=DropInPaths --value "$slice")]"
[ -e "/sys/fs/cgroup/$slice" ] && echo "SLICE CGROUP SURVIVED" || echo "slice cgroup absent"
sudo_run /usr/bin/nft delete table inet "$table" || true
if sudo -n nft list table inet "$table" 2>&1 | grep -q 'No such file or directory'; then echo "table absent"; else echo "TABLE SURVIVED"; fi
sudo_run /usr/bin/ip netns delete "$stem" || true
[ -e "$netns" ] && echo "NETNS SURVIVED" || echo "netns absent"
rm -rf "$scratch" "$listener_port_file"
