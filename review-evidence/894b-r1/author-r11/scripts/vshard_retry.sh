#!/bin/bash
# One of rtl.yml's verilator shards locally, its step "Run this exhaustive suite shard" on a clean clone of a head:
# scripts/run_all_suites.sh <logs> --wait --ci-pieces --shard K/19, with the sweep's pinned tools (round 6's private
# copy of the pinned tool directory, VERILATOR_ROOT, TSN_GEN_ROOT). Prints the suite runner's summary; its rc is the
# runner's. usage: vshard.sh HEAD K
set -u
H=$1 K=$2 T=/data-2/milan/tmp/894b-a781 F=/data-2/milan/tmp/894b-a781/fullR11
C=$F/vretry-$K L=$F/vretry-logs-$K
[ -d "$C" ] || bash $T/scripts/clone.sh "$C" "$H" > "$F/vretry-clone-$K.log" 2>&1 || exit 3
test "$(git -C "$C" rev-parse HEAD)" = "$H" || exit 4
# Preserve the declared remote after an offline local clone; provenance verifies it.
git -C "$C" config --file "$C/.git/modules/third_party/tsn-c-stack/config" remote.origin.url "$(git -C "$C" config -f .gitmodules submodule.third_party/tsn-c-stack.url)" || exit 5
test -z "$(git -C "$C" status --porcelain --untracked-files=all)" || exit 6
cd "$C" || exit 3
echo "# shard $K/19 at $H, owns: $(bash scripts/run_all_suites.sh --ci-pieces --shard $K/19 --list | tr '\n' ' ')"
env PATH=$T/fullR6/tool-bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
    VERILATOR_ROOT=$WORKSPACE_HOME/.local/share/containers/storage/overlay/9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator \
    TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c MAKEFLAGS=-j16 \
    bash scripts/run_all_suites.sh "$L" --wait --ci-pieces --shard "$K/19"
rc=$?
echo "# the clone after: $(git status --porcelain --untracked-files=all | wc -l) changed path(s); rc=$rc"
exit $rc
