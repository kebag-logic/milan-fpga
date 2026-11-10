#!/bin/bash
# Usage: variant_identity.sh <clone> <round3-tree> <out> : each config's --variant-shape outputs at both trees, compared.
C=$1; B=$2; O=$3; mkdir -p "$O"
for cfg in "$C"/configs/endstation_*.yaml; do n=$(basename "$cfg" .yaml)
  python3 -B "$C/sw/mailbox/gen_mailbox.py" --variant-interfaces 2 --variant-shape "$cfg" --out "$O/head/$n" >/dev/null 2>"$O/head-$n.err"; h=$?
  (cd "$B" && python3 -B sw/mailbox/gen_mailbox.py --variant-interfaces 2 --variant-shape "configs/$n.yaml" --out "$O/r3/$n" >/dev/null 2>"$O/r3-$n.err"); r=$?
  if diff -rq "$O/head/$n" "$O/r3/$n" >/dev/null 2>&1; then same=identical; else same=DIFFERENT; fi
  echo "$n head-rc=$h r3-rc=$r $same"
done
