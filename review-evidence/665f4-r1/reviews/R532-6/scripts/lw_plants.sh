#!/bin/bash
# R532-6: dependency plants L5 (higher-version skip removed), L6 (per-value skip instead of
# whole-PDU rejection), L7 (atomic validation pre-pass removed) as commits in disposable clones.
set -euo pipefail
R=$1; S=$2
plant() { local n=$1 f=$2 old=$3 new=$4; rm -rf $S/lw-$n; git clone -q $R/third_party/lwSRP $S/lw-$n
  python3 - "$S/lw-$n/$f" "$old" "$new" <<'PY'
import sys; f,o,n=sys.argv[1:4]; t=open(f).read(); c=t.count(o); assert c==1,(f,c); open(f,'w').write(t.replace(o,n))
PY
  git -C $S/lw-$n -c user.name=probe -c user.email=probe@invalid commit -qam "plant $n"; echo "$n $(git -C $S/lw-$n rev-parse HEAD)"; }
plant L5 src/core/mrp_pdu.c 'bool later = pdu[0] > ops->proto_version;' 'bool later = false;'
plant L6 src/core/mrp_pdu.c 'return r; /* The validation pass rejects the complete PDU. */' 'continue;'
plant L7 src/core/mrp_pdu.c 'int r = parse_pass(pdu, len, ops, NULL, NULL, NULL);' 'int r = 0;'
