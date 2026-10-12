#!/usr/bin/env bash
# Scratch: R584-12's lazy probes against the head with one layer removed at a time from a disposable clone's
# ctrl_build.py (the allowlist's call, or GIT_NO_LAZY_FETCH), on this host's Git and the Ubuntu 24.04 replica's.
# usage: layer_probe.sh <round15 dir>
set -u
R=$1; cd "$R" || exit 2
B=clones/mut/sw/firmware/ctrl/test/ctrl_build.py
cp "$B" "$R/ctrl_build.orig"
for layer in allowlist-only lazy-env-only; do
  cp "$R/ctrl_build.orig" "$B"
  if [ "$layer" = allowlist-only ]; then
    python3 -I -c 'import sys;p=sys.argv[1];t=open(p).read();o=", \"GIT_NO_LAZY_FETCH\": \"1\"}";assert t.count(o)==1;open(p,"w").write(t.replace(o,"}"))' "$B"
  else
    python3 -I -c 'import sys;p=sys.argv[1];t=open(p).read();o="    configured(stack)\n";assert t.count(o)==1;open(p,"w").write(t.replace(o,""))' "$B"
  fi
  for git in host 2.43; do
    probes="lazy_uploadpack_fail lazy_uploadpack_serve lazy_ssh lazy_toctou"
    if [ $git = host ]; then
      out=$(git --version; python3 -I -B probes/R584-12/scripts/store_probe.py clones/mut/sw/firmware/ctrl/test clones/mut/third_party/tsn-c-stack "work-layer-$layer-$git" $probes 2>&1)
    else
      out=$(podman run --rm --network none -v "$R:$R" -w "$R" localhost/697c-r6-ci sh -c "git --version; python3 -I -B probes/R584-12/scripts/store_probe.py clones/mut/sw/firmware/ctrl/test clones/mut/third_party/tsn-c-stack work-layer-$layer-$git $probes" 2>&1)
    fi
    echo "== $layer, $(echo "$out" | head -1)"
    echo "$out" | grep '^PROBE\|planted' | sed -E 's/^(PROBE \S+ \S+ .{0,110}).*(RAN=[0-9]+)$/\1 ... \2/'
  done
done
cp "$R/ctrl_build.orig" "$B"; rm "$R/ctrl_build.orig"
git -C clones/mut diff --quiet && echo "clone restored"
