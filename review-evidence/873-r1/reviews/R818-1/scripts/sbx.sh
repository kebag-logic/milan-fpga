#!/bin/sh
# Run a command offline: Docker socket hidden (/run is an empty tmpfs), no network,
# every execve/connect traced. Usage: sbx.sh <out-prefix> <cwd> <cmd...>
set -u
out=$1; cwd=$2; shift 2
start=$(date +%s)
strace -f -qq --seccomp-bpf -e trace=execve,connect -s 200 -o "$out.strace" \
  bwrap --dev-bind / / --tmpfs /run --unshare-net --die-with-parent --chdir "$cwd" \
  env -u DOCKER_HOST -u DOCKER_CONTEXT "$@" > "$out.log" 2>&1
rc=$?
echo "$rc" > "$out.rc"
echo "elapsed $(( $(date +%s) - start ))s rc $rc" >> "$out.log.meta"
exit $rc
