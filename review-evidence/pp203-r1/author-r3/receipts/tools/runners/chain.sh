#!/usr/bin/env bash
# the remaining processor campaigns at the head, one at a time, after aecp-dispatch
until [ -f <runs>/camp/aecp-dispatch.done ]; do sleep 30; done
for c in acmp notify d3 aecp gsi elab-guards ctr aecp-cmds adp-engine name-wr; do
  case $c in
    ctr) j=4 ;;
    *) j=8 ;;
  esac
  if [ $c = elab-guards ]; then <tools>/camp.sh $c $j JOBS=8; else <tools>/camp.sh $c $j; fi
done
touch <runs>/camp/chain.done
