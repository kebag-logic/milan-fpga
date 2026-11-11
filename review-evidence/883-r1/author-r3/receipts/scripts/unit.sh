#!/usr/bin/env bash
# unit.sh <name> <workdir> <log> <command...>: run one command as its own transient user unit
# (milan-883-a768-<name>, MemoryMax 10G, on this session's CPU pool), detached; its exit status goes to <log>.rc.
set -u
name=$1; dir=$2; log=$3; shift 3
rm -f "$log.rc"
printf -v cmd '%q ' "$@"
systemd-run --user --quiet --collect --unit="milan-883-a768-$name" -p MemoryMax=10G -p CPUAffinity=96-127 \
  bash -c "source <scratch>/scripts/env.sh; cd $(printf %q "$dir") || exit 2; { $cmd; } > $(printf %q "$log") 2>&1; echo \$? > $(printf %q "$log.rc")"
