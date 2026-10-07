#!/bin/bash
# Reviewer planted defects at the round-5 lwSRP seams. Creates disposable copies under scratch only.
set -euo pipefail
P=$REVIEWS/665f4-r532-5-packet; S=$P/scratch
plant() { # file old new  (exactly one site required)
  python3 - "$@" <<'PY'
import sys; f,old,new=sys.argv[1:4]; t=open(f).read(); n=t.count(old)
assert n==1, f"{f}: {n} sites for {old!r}"; open(f,'w').write(t.replace(old,new))
PY
}
# Parent-side plants: copies of the exported head tree
for a in A1 A2; do rm -rf $S/root-$a; cp -a $S/root-head $S/root-$a; done
plant $S/root-A1/sw/firmware/ctrl/srp/srp_mbx.c \
 'if (!app || mrp_rx(app,0,frame->bytes + 14,frame->len - 14u) != 0) {' \
 'int planted_r = app ? mrp_rx(app,0,frame->bytes + 14,frame->len - 14u) : -1;
    if (planted_r != 0 && planted_r != -SHLAN_ERROR_NO_MEMORY) {'
plant $S/root-A2/sw/firmware/ctrl/test/srp_fixture.hpp '        loop.n_polls=0;
' ''
# Dependency-side plants: committed in disposable clones so the pin guard sees a clean tree
lwplant() { # name file old new
  local n=$1; shift; rm -rf $S/lwgit-$n; git clone -q $S/lwgit-new $S/lwgit-$n; git -C $S/lwgit-$n checkout -q a4cbe41de1c80d43f26e0d348cbdb45075273a4f
  plant $S/lwgit-$n/$1 "$2" "$3"
  git -C $S/lwgit-$n -c user.name=probe -c user.email=probe@invalid commit -qam "plant $n"
  echo "$n $(git -C $S/lwgit-$n rev-parse HEAD)"
}
lwplant L1 src/core/mrp_mad.c 'if (changed && (ev == MRP_EVENT_RJOININ || ev == MRP_EVENT_RJOINMT)) {' 'if (false && changed && (ev == MRP_EVENT_RJOININ || ev == MRP_EVENT_RJOINMT)) {'
lwplant L2 src/core/mrp_mad.c 'bool changed_in = previous && previous->reg != MRP_REG_STATE_MT &&' 'bool changed_in = previous && previous->reg == MRP_REG_STATE_IN &&'
lwplant L3 src/modules/msrp.c '.milan_rapid_leave = LWSRP_MILAN != 0,' '.milan_rapid_leave = false,'
lwplant L5 src/core/mrp_pdu.c 'bool later = pdu[0] > ops->proto_version;' 'bool later = false;'
lwplant L6 src/core/mrp_pdu.c 'return r; /* The validation pass rejects the complete PDU. */' 'continue;'
