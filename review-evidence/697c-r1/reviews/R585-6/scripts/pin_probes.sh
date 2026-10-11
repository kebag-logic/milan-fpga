#!/bin/bash
# pin_probes.sh : ctrl_build.py --stack-pin against disposable clones of the pinned stack, one defect each.
P=$REVIEWS/697c-r585-6-packet; S=$P/scratch/pinprobe; R=$REVIEWS/r585-6-697c
fresh(){ rm -rf $S; git clone -q --no-checkout $R/third_party/tsn-c-stack $S && git -C $S checkout -q 1a9f651cdf7846b8e10ac246a6ef6916960fbb92; }
probe(){ local label=$1; shift; fresh; ( cd $S && eval "$@" ); out=$(cd $R && python3 -B sw/firmware/ctrl/test/ctrl_build.py --stack-pin $S 2>&1); echo "rc=$? $label :: ${out:0:170}"; }
probe "clean clone" true
probe "docs edited (outside the proven parts)" "echo x >> docs/PORTING.md"
probe "untracked source added" "echo 'int x;' > src/extra.c"
probe "public header CRLF" "sed -i 's/\$/\r/' include/wire.h"
probe "include/ swapped for a symlink to an edited copy" "cp -r include ../inc2 && echo '//x' >> ../inc2/wire.h && rm -r include && ln -s ../inc2 include"
probe "test edited then hidden with skip-worktree" "echo '//x' >> tests/test_adp.cpp && git update-index --skip-worktree tests/test_adp.cpp"
probe "executable bit only" "chmod +x src/adp.c"
probe "empty directory added under src" "mkdir src/empty"
probe "file under an ignored path in tests" "mkdir -p tests/build && echo x > tests/build/junk.o"
rm -rf $S $P/scratch/inc2
