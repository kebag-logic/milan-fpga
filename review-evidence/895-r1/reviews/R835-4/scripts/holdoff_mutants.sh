#!/bin/bash
# holdoff_mutants.sh CLONE OUT SCRATCH: replace SRP_REDECLARE_CS in CLONE's srp_mbx.c with each probe expression
# (the TX term dropped; the JoinTime and TX terms dropped), run the Talker arms on each, and restore the file's
# committed bytes after each (git checkout), refusing to continue if the restore does not match HEAD's blob.
set -u
C=$1 O=$2 S=$3; F=sw/firmware/ctrl/srp/srp_mbx.c; H=$(dirname "$0")
OLD='#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)'
for spec in "m1-drop-tx-term|#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS)" "m2-drop-join-and-tx|#define SRP_REDECLARE_CS (2u * 1000u)"; do
  name=${spec%%|*} new=${spec#*|}
  python3 -I -c "import sys;p=sys.argv[1];t=open(p).read();assert t.count(sys.argv[2])==1;open(p,'w').write(t.replace(sys.argv[2],sys.argv[3]))" "$C/$F" "$OLD" "$new" || exit 3
  echo "$name: $(grep -c -F "$new" "$C/$F") planted" > "$O/$name.log"
  python3 -B "$H/talker_arms.py" "$C" "$S/arms-$name" talker-only >> "$O/$name.log" 2>&1; echo $? > "$O/$name.rc"
  git -C "$C" checkout -- "$F"
  [ "$(git -C "$C" hash-object "$F")" = "$(git -C "$C" rev-parse "HEAD:$F")" ] || { echo "restore mismatch" >&2; exit 4; }
done
