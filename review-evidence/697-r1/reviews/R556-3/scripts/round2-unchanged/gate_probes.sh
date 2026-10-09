#!/bin/bash
# SPDX-License-Identifier: MIT
# Planted controls against the comment, boundary and RV32 gates, each in a fresh
# disposable copy of the exact head. Prints one line per probe: name, gate rc,
# and the expected outcome. usage: gate_probes.sh <git-repo> <rev> <scratch-dir>
set -u
REPO=$1; REV=$2; S=$3/probes
rm -rf "$S"; mkdir -p "$S"
fresh() { rm -rf "$S/$1"; mkdir -p "$S/$1"; git -C "$REPO" archive "$REV" | tar -x -C "$S/$1"; }
report() { printf '%-34s rc=%-3s expect=%s\n' "$1" "$2" "$3"; }

# ---- comment gate
fresh c-src-prose
sed -i '0,/^#include/s//\/\/ The core keeps the frame owed until the port takes it.\n#include/' "$S/c-src-prose/src/adp.c"
(cd "$S/c-src-prose" && python3 scripts/check_comments.py > ../c-src-prose.log 2>&1); report comment-src-line-prose $? refuse
fresh c-hdr-block
printf '/* Integrators must call adp_poll while it returns true. */\n' >> "$S/c-hdr-block/include/adp.h"
(cd "$S/c-hdr-block" && python3 scripts/check_comments.py > ../c-hdr-block.log 2>&1); report comment-header-block-prose $? refuse
fresh c-test-mixed
sed -i '0,/^\/\/ REQ: /s//\/\/ REQ: ADP-01 checks the encoder\n\/\/ REQ: /' "$S/c-test-mixed/tests/test_adp.cpp"
(cd "$S/c-test-mixed" && python3 scripts/check_comments.py > ../c-test-mixed.log 2>&1); report comment-test-req-plus-prose $? refuse
fresh c-clause-prose
sed -i 's|^// IEEE 1722-2016 Annex B$|// IEEE 1722-2016 Annex B describes the allocation protocol|' "$S/c-clause-prose/include/maap.h"
(cd "$S/c-clause-prose" && python3 scripts/check_comments.py > ../c-clause-prose.log 2>&1); report comment-clause-plus-prose $? refuse
fresh c-mutation-fragment
python3 -I - "$S/c-mutation-fragment/tests/mutations.json" <<'EOF'
import json, sys
p = sys.argv[1]; t = json.load(open(p)); t[0]['new'] += ' // planted narrative'; open(p, 'w').write(json.dumps(t, indent=1))
EOF
(cd "$S/c-mutation-fragment" && python3 scripts/check_comments.py > ../c-mutation-fragment.log 2>&1); report comment-mutation-fragment $? refuse
fresh c-asm-hash
sed -i 's|^_start:$|# Clear BSS, then call the smoke checks and report through the test device.\n_start:|' "$S/c-asm-hash/examples/rv32/start.S"
(cd "$S/c-asm-hash" && python3 scripts/check_comments.py > ../c-asm-hash.log 2>&1); report comment-asm-hash-prose $? refuse-or-gap
(cd "$S/c-asm-hash" && riscv64-elf-gcc -march=rv32i -mabi=ilp32 -c examples/rv32/start.S -o /dev/null > ../c-asm-hash.compile.log 2>&1); report '  (planted start.S still assembles)' $? info
fresh c-ifzero
sed -i '0,/^#include/s//#if 0\nThe core keeps the frame owed until the port takes it.\n#endif\n#include/' "$S/c-ifzero/src/adp.c"
(cd "$S/c-ifzero" && python3 scripts/check_comments.py > ../c-ifzero.log 2>&1); report comment-if0-prose-block $? info-not-a-comment

# ---- Linux boundary gate (library check only; no selftest)
bprobe() { # name expect header-and-code
  fresh "$1"
  python3 -I - "$S/$1/src/adp.c" "$3" <<'EOF'
import sys
p, plant = sys.argv[1], sys.argv[2].replace('\\n', '\n')
s = open(p).read()
i = s.index('#include')
open(p, 'w').write(s[:i] + plant + '\n' + s[i:])
EOF
  (cd "$S/$1" && python3 scripts/check_boundary.py --work "$S/$1/build-boundary" --jobs 4 > "../$1.log" 2>&1); report "$1" $? "$2"
}
bprobe b-unistd refuse '#include <unistd.h>'
bprobe b-pthread refuse '#include <pthread.h>'
bprobe b-sys-select refuse '#include <sys/select.h>'
bprobe b-sys-types refuse '#include <sys/types.h>'
bprobe b-alloca refuse '#include <alloca.h>\nint tsn_probe(unsigned n);\nint tsn_probe(unsigned n) { volatile char *p = alloca(n); p[0] = 1; return p[0]; }'
bprobe b-endian refuse '#include <endian.h>\nunsigned tsn_probe(unsigned v);\nunsigned tsn_probe(unsigned v) { return be32toh(v); }'
bprobe b-malloc refuse '#include <stdlib.h>\nvoid *tsn_probe(void);\nvoid *tsn_probe(void) { return malloc(4); }'
bprobe b-printf refuse '#include <stdio.h>\nvoid tsn_probe(void);\nvoid tsn_probe(void) { puts("x"); }'

# ---- RV32 gate
rprobe() {
  fresh "$1"
  python3 -I - "$S/$1/src/adp.c" "$3" <<'EOF'
import sys
p, plant = sys.argv[1], sys.argv[2].replace('\\n', '\n')
s = open(p).read()
i = s.index('#include')
open(p, 'w').write(s[:i] + plant + '\n' + s[i:])
EOF
  (cd "$S/$1" && python3 scripts/baremetal.py --work "$S/$1/build-rv32" --jobs 2 > "../$1.log" 2>&1); report "$1" $? "$2"
}
rprobe r-unistd refuse '#include <unistd.h>'
rprobe r-heap-symbol refuse 'extern void *malloc(unsigned long);\nvoid *tsn_probe(void);\nvoid *tsn_probe(void) { return malloc(4); }'
rprobe r-os-symbol refuse 'extern int getpid(void);\nint tsn_probe(void);\nint tsn_probe(void) { return getpid(); }'
fresh r-smoke-fail
sed -i 's/CHECK(p.length == MAAP_FRAME_BYTES \&\& p.frame\[15\] == MAAP_MSG_ANNOUNCE, 25);/CHECK(p.length == MAAP_FRAME_BYTES \&\& p.frame[15] == MAAP_MSG_PROBE, 25);/' "$S/r-smoke-fail/examples/rv32/smoke.c"
(cd "$S/r-smoke-fail" && python3 scripts/baremetal.py --work "$S/r-smoke-fail/build-rv32" --jobs 2 > ../r-smoke-fail.log 2>&1); report r-smoke-check-fails $? refuse
fresh r-core-defect
sed -i 's/#define ADP_ADVERTISE_MS 5000u/#define ADP_ADVERTISE_MS 4999u/' "$S/r-core-defect/include/adp.h"
(cd "$S/r-core-defect" && python3 scripts/baremetal.py --work "$S/r-core-defect/build-rv32" --jobs 2 > ../r-core-defect.log 2>&1); report r-core-defect-period $? refuse
