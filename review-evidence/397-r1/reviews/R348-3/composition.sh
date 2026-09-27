#!/bin/sh
# Composition facts for #397 on the merge-train candidate. Usage: composition.sh <clone>
set -u
cd "$1" || exit 2
SRCBASE=ac18b50968b12efe4d15c0a06301264b35656b31
SRC=ff75a70807c151517860c73a06d7ea36e2a46008
PARENT=10a5bf59a6a73e9b6487d9ea6f42669ce142ae25
echo "candidate $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree}) parents $(git log -1 --format=%P HEAD)"
echo "parent-first-line: $(git log -1 --format=%s $PARENT)"
echo "== PR source files ($SRCBASE..$SRC)"; git diff --name-only $SRCBASE $SRC
echo "== candidate files ($PARENT..HEAD)"; git diff --name-only $PARENT HEAD
echo "== predecessor files ($SRCBASE..$PARENT)"; git diff --name-only $SRCBASE $PARENT
echo "== overlap"; git diff --name-only $SRCBASE $PARENT | sort > /tmp/r348c.a; git diff --name-only $SRCBASE $SRC | sort > /tmp/r348c.b; comm -12 /tmp/r348c.a /tmp/r348c.b
echo "== patch body identity (source patch vs candidate patch, index/hunk headers dropped)"
git diff $SRCBASE $SRC | grep -v '^index' | grep -v '^@@' > /tmp/r348c.p1
git diff $PARENT HEAD | grep -v '^index' | grep -v '^@@' > /tmp/r348c.p2
cmp /tmp/r348c.p1 /tmp/r348c.p2 && echo IDENTICAL
echo "== blob identity of PR-owned files: source head vs candidate"
for f in $(git diff --name-only $SRCBASE $SRC); do a=$(git rev-parse $SRC:$f); b=$(git rev-parse HEAD:$f); [ "$a" = "$b" ] && echo "same $f" || echo "DIFF $f"; done
echo "== firmware/litex/capture-code drift since source base"
git diff --stat $SRCBASE HEAD -- sw/firmware sw/litex tb/verilator/nvm_capture_cpu/firmware.py tb/verilator/nvm_capture_cpu/probe.py tb/verilator/nvm_capture_cpu/run.py
echo "== path RTL and capture-code drift since source base"
git diff --stat $SRCBASE HEAD -- hdl protocol-processor configs tb/verilator/nvm_capture_cpu
