#!/bin/bash
# R532-6 reviewer plants in the SRP adapter. Disposable exported copies under scratch only.
# usage: r532_plants.sh REPO PACKET  -> creates PACKET/scratch/root-head and root-<plant> copies
set -euo pipefail
R=$1; P=$2; S=$P/scratch
rm -rf $S/root-head; mkdir -p $S/root-head
git -C $R archive HEAD | tar -x -C $S/root-head
git -C $R/protocol-processor archive HEAD | tar -x -C $S/root-head/protocol-processor
git -C $R/gptp-processor archive HEAD | tar -x -C $S/root-head/gptp-processor
plant() { # name old new  (exactly one site required in srp_mbx.c)
  local n=$1; rm -rf $S/root-$n; cp -a $S/root-head $S/root-$n
  python3 - "$S/root-$n/sw/firmware/ctrl/srp/srp_mbx.c" "$2" "$3" <<'PY'
import sys; f,old,new=sys.argv[1:4]; t=open(f).read(); c=t.count(old)
assert c==1, f"{f}: {c} sites for {old!r}"; open(f,'w').write(t.replace(old,new))
PY
  echo "planted $n"
}
plant retry-removed 'if (m->pending_rx.len && m->pending_rx.interface == n && rx_order_ready(m)) {' 'if (false) {'
plant retain-dropped '        m->pending_rx = *frame;' '        (void)0;'
plant overtake 'return m->pending_rx.len == 0 && rx_order_ready(m);' 'return rx_order_ready(m);'
plant reset-keeps '    if (m->pending_rx.len && m->pending_rx.interface == i->index) {
        m->pending_rx.len = 0;' '    if (false) {
        m->pending_rx.len = 0;'
plant reset-any-interface 'if (m->pending_rx.len && m->pending_rx.interface == i->index) {' 'if (m->pending_rx.len) {'
plant refusal-malformed 'if (result == -SHLAN_ERROR_NO_MEMORY) {' 'if (false) {'
plant retry-ignores-order '&& m->pending_rx.interface == n && rx_order_ready(m)) {' '&& m->pending_rx.interface == n) {'
