[A203] author-side mechanism experiment (scratch daemon, not the candidate runner)

Date 2026-09-23, host: the replay host (128 CPUs, 53 GiB RAM, Docker 29.8.1 with the
containerd image store on the system containerd, iptables-nft with FORWARD policy DROP).

Nothing here executed scripts/act_ci.py; every command was typed by hand.

1. `ip netns add a203-exp` then pasta as the uplink:
   `pasta --runas 0:0 --netns-only --config-net --netns /run/netns/a203-exp
    -t none -u none -T none -U none --no-map-gw -P <pidfile>` in a transient unit.
   - Without `--runas 0:0 --netns-only` pasta drops to nobody in its own user
     namespace and cannot join a root-owned netns (EPERM, journal kept).
   - From inside the namespace: HTTPS to github.com = 200; a listener on host
     127.0.0.1 is unreachable both as 127.0.0.1 and as the gateway address
     (`--no-map-gw`).
2. dockerd in a transient unit with NetworkNamespacePath, TemporaryFileSystem=/run/containerd,
   RuntimeDirectory, its own data-root under scratch, exec-root, socket, pidfile,
   `--containerd-namespace`, `--bridge none`, `--default-address-pool base=10.203.0.0/24,size=24`,
   systemd cgroup driver, `--cgroup-parent`, `--feature containerd-snapshotter=true`, a slot label.
   - `docker info` through the slot socket: DockerRootDir = scratch data-root,
     driver-type io.containerd.snapshotter.v1, label present.
   - The unit's cgroup holds dockerd and a MANAGED containerd whose config is
     under the slot exec-root: masking /run/containerd stops dockerd attaching
     to the system containerd the default daemon uses.
   - Host nft ruleset: 0 lines mention the slot subnet or name; the daemon's
     own nat/filter tables exist only inside the namespace; the host routing
     table has no route to 10.203.0.0/24.
3. A container on the slot network: DNS ok, internet TCP ok, host LAN
   address unreachable, but a listener bound on the DEFAULT daemon's bridge
   gateway (a host-local address) WAS reachable through pasta.
4. One nft table of its own, output hook, one rule
   `socket cgroupv2 level 2 "<uplink unit cgroup>" fib daddr type local counter reject`:
   the same container keeps DNS and internet, the default-daemon bridge gateway
   and docker0 become unreachable (counter 2), the host itself still reaches
   the listener. Table deleted afterwards (0 tables named a203 remain).
5. act 0.2.89 under `sudo nsenter --net=/run/netns/a203-exp -- env -i ...
   DOCKER_HOST=unix:///run/a203-exp/docker.sock act ... --container-daemon-socket -
   --network a203-exp-net --artifact-server-addr 10.203.0.1`: the job saw
   ACTIONS_RUNTIME_URL=http://10.203.0.1:<port>/, connected to it, nproc = 4 and
   cpuset 4-7 from `--cpuset-cpus=4-7`; the host namespace cannot connect to
   10.203.0.1 (no route).
6. `systemctl set-property --runtime <slice> MemoryMax=.. MemorySwapMax=0` before the
   slice exists creates runtime drop-ins that apply to memory.max/memory.swap.max;
   stopping the last unit leaves the slice active, `systemctl stop <slice>` removes
   its cgroup, `systemctl revert <slice>` removes the drop-ins. A dash in a slice
   name nests it (a203-exp.slice lives under a203.slice); an underscore name is
   top-level.
7. `dockerd --validate --config-file /dev/null` = configuration OK.

Measured image cost (default daemon, read-only): containerd content store 19 GB,
overlayfs snapshots 56 GB; `docker image ls` reports catthehacker/ubuntu:full-latest
at 76.1 GB. Free space: /data 107 GB, / 133 GB.
