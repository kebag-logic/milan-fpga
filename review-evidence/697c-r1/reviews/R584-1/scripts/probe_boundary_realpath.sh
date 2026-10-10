#!/usr/bin/env bash
# Real-path boundary probes in the disposable head worktree WT: commit a plant inside its tsn-c-stack checkout
# (a local commit, never pushed), stage that gitlink in WT's index so the pin check accepts it, run
# ctrl_boundary.py without --selftest, then restore the pin. usage: probe_boundary_realpath.sh WT
set -u
WT=$1; S=$WT/third_party/tsn-c-stack; PIN=$(git -C "$WT" rev-parse HEAD:third_party/tsn-c-stack)
probe() {  # name file anchor replacement
  local name=$1 file=$2 anchor=$3 repl=$4
  python3 - "$S/$file" "$anchor" "$repl" <<'PY'
import sys; p, a, r = sys.argv[1:4]; a = a.encode().decode("unicode_escape"); r = r.encode().decode("unicode_escape")
t = open(p).read(); assert t.count(a) == 1, (p, a); open(p, "w").write(t.replace(a, r))
PY
  git -C "$S" -c user.name=probe -c user.email=probe@invalid commit -q -am "probe $name"
  git -C "$WT" update-index --cacheinfo 160000,$(git -C "$S" rev-parse HEAD),third_party/tsn-c-stack
  echo "=== probe: $name"
  (cd "$WT" && python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 2>&1 | grep -v '^    ' | grep -E 'FAIL|PASS|REFUSED|finding|tsn-c-stack at')
  echo "rc=${PIPESTATUS[0]}"
  git -C "$S" checkout -q --detach "$PIN"; git -C "$WT" update-index --cacheinfo 160000,$PIN,third_party/tsn-c-stack
}
probe "stack source includes the platform pool header" src/acmp.c '#include "acmp.h"\n' '#include "acmp.h"\n#include "ctrl_pool.h"\n'
probe "stack source includes the mailbox driver by relative path" src/maap.c '#include "maap.h"\n' '#include "maap.h"\n#include "../../../sw/firmware/ctrl/mbx/mbx.h"\n'
probe "stack test includes the mailbox HAL" tests/test_maap_debug.cpp '#include "maap.h"\n' '#include "maap.h"\n#include "mbx_hal.h"\n'
git -C "$S" status --short; git -C "$WT" diff --cached --stat; git -C "$WT" submodule status third_party/tsn-c-stack
