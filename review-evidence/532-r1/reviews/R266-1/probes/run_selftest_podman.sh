#!/usr/bin/env bash
# R266-1: run the CANDIDATE runner's offline --selftest only inside a
# disposable, network-less rootless container (never on the host, never on a
# Docker daemon). sudo, gh and docker are absent from the image, so read-only
# recording stubs stand in for them on SAFE_PATH: any real invocation by the
# offline self-test is logged and fails with status 97.
# Usage: run_selftest_podman.sh <clone> <rev> <label> <user> <image> <outdir>
set -euo pipefail
clone=$1 rev=$2 label=$3 user=$4 image=$5
out=$(realpath -m "$6")
stage=$out/stage-$label
stubs=$out/stubs-$label
log=$out/stublog-$label
rm -rf "$stage" "$log"
mkdir -p "$stubs" "$log"
for tool in sudo gh docker; do
  cat >"$stubs/$tool" <<STUB
#!/bin/sh
printf '%s %s\n' "$tool" "\$*" >>/stublog/calls.log
exit 97
STUB
  chmod 0555 "$stubs/$tool"
done
chmod 0777 "$log"
git clone -q --no-hardlinks "$clone" "$stage"
git -C "$stage" checkout -q --detach "$rev"
chmod -R a+rX "$stage"
set +e
timeout 3000 podman run --rm --network none --cpus 8 --memory 8g --user "$user" \
  -v "$stage:/src:ro" -v "$stubs/sudo:/usr/local/bin/sudo:ro" \
  -v "$stubs/gh:/usr/local/bin/gh:ro" -v "$stubs/docker:/usr/local/bin/docker:ro" \
  -v "$log:/stublog" "$image" \
  sh -c 'cp -a /src /tmp/work && cd /tmp/work && id -u && python3 --version && python3 scripts/act_ci.py --selftest'
rc=$?
set -e
echo "container-selftest rc=$rc rev=$(git -C "$stage" rev-parse HEAD) tree=$(git -C "$stage" rev-parse 'HEAD^{tree}') act_ci.py sha256=$(sha256sum "$stage/scripts/act_ci.py" | cut -c1-64) user=$user image=$image"
echo "stub invocations: $(cat "$log/calls.log" 2>/dev/null | wc -l)"
rm -rf "$stage"
exit "$rc"
