#!/bin/bash
# What differs between a leg's head build and the build that ran its groups, beyond tree:firmware: each differing
# generated file's diff, the runtime archives' members by content, and the Vsim's strings with the build paths named
# alike. usage: explain_diffs.sh NAME > receipt
set -u
T=<scratch>
N=$1 A=$T/builds/$1 B=$T/builds-head/$1
echo "# $N: builds/$N (ran the groups) against builds-head/$N (the head), the differing build inputs explained"
for f in gateware/sim.v split-soc/flash-map/flash_port.json $(cd "$A" && find . -name csr.csv -o -name csr.h | sort); do
    echo "== $f"; diff "$A/$f" "$B/$f" | sed "s#$T#<scratch>#g"; done
for a in runtime/libc.a runtime/libcompiler_rt.a; do
    rm -rf /tmp/a683ze-ar1 /tmp/a683ze-ar2; mkdir -p /tmp/a683ze-ar1 /tmp/a683ze-ar2
    (cd /tmp/a683ze-ar1 && ar x "$A/$a"); (cd /tmp/a683ze-ar2 && ar x "$B/$a")
    echo "== $a: members by content: $(diff -r /tmp/a683ze-ar1 /tmp/a683ze-ar2 > /dev/null && echo identical || echo DIFFERENT); listing dates: $(ar tv "$A/$a" | head -1 | cut -c30-46) / $(ar tv "$B/$a" | head -1 | cut -c30-46)"
done
strings "$A/native/Vsim" | sed "s#$A#B#g; s#$T/hleg-wt-$N#C#g; s#$T#S#g" > /tmp/a683ze-s1
strings "$B/native/Vsim" | sed "s#$B#B#g; s#$T/hleg-wt-head#C#g; s#$T#S#g" > /tmp/a683ze-s2
echo "== native/Vsim strings, the build and clone paths named alike: $(diff /tmp/a683ze-s1 /tmp/a683ze-s2 | grep -c '^[<>]') differing lines"
diff /tmp/a683ze-s1 /tmp/a683ze-s2 | cut -c1-120
