#!/usr/bin/env bash
# Probe the checker's default (CI/make) invocation on a disposable export of HEAD,
# and run it against the pre-change guide/diagram from the base and merged main.
# Usage: probe-default-path.sh <clone-dir> <scratch-dir>
set -u
clone="$1"; s="$2"; t="$s/tree"; rm -rf "$t"; mkdir -p "$t"
git -C "$clone" archive HEAD | tar -x -C "$t"
cd "$t"
echo "== export baseline"; python3 scripts/check-integrator-params.py; echo "rc=$?"
sed -i '/parameter int unsigned REG_TL_TIMEOUT_MS_P = 300_000,/d' hdl/top/protocol_processor_top.sv
echo "== default path, top parameter removed"; python3 scripts/check-integrator-params.py; echo "rc=$?"
echo "== make params, top parameter removed"; make -s params; echo "rc=$?"
echo "== make check (lint wavedrom-check links matrix modmatrix params stale; stale needs git so run the gate prefix only)"
make -s lint wavedrom-check links matrix modmatrix params; echo "rc=$?"
git -C "$clone" archive HEAD | tar -x -C "$t"   # restore
for rev in 008edbbf486598ae237414273d75e385cf0e1a56 60152f3ff068b81333326b5081b5303253ba7fe7; do
  git -C "$clone" show "$rev:docs/guides/integrator.md" > "$s/guide-$rev.md"
  git -C "$clone" show "$rev:docs/diagrams/21-integration-faces.svg" > "$s/diagram-$rev.svg"
  echo "== pre-change guide at $rev"; python3 scripts/check-integrator-params.py --guide "$s/guide-$rev.md"; echo "rc=$?"
  echo "== pre-change diagram at $rev"; python3 scripts/check-integrator-params.py --diagram "$s/diagram-$rev.svg"; echo "rc=$?"
done
