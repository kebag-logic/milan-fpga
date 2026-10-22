#!/usr/bin/env bash
# probe_walk_revert.sh REPO SCRATCH: revert only the round-2 drive() branch of
# sw/firmware/ctrl/test/acmp_walk.cpp in REPO, run the acmp/acmpwalk arms,
# then restore the file from the index and prove the bytes are the head's.
set -u
repo=$1; s=$2; f=sw/firmware/ctrl/test/acmp_walk.cpp
here=$(cd "$(dirname "$0")" && pwd)
cd "$repo" || exit 2
before=$(git hash-object "$f")
python3 -I - "$f" <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
old=("        } else if (s.tk_kind == 2u && a.sinks[k].state == ACMP_SETTLED_RSV_OK) {\n"
     "            acmp_tk_kind_changed(&a, static_cast<unsigned>(k), s.tk_fail);   // the swap, as ctrl_app_srp.c delivers it\n")
assert t.count(old)==1, "fixture not unique"
open(p,'w').write(t.replace(old,""))
PY
echo "planted: $(git diff --stat -- "$f" | tail -n 1)"
python3 -I "$here/probe_walk.py" "$repo" "$s" 4 checkout-as-is
rc=$?
git checkout -- "$f"
after=$(git hash-object "$f")
echo "restore: before=$before after=$after index=$(git rev-parse :"$f") head=$(git rev-parse HEAD:"$f")"
exit $rc
