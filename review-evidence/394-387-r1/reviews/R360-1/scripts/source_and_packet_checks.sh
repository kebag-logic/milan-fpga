#!/bin/sh
# 1) Trace who writes the software-published link-status CSR at the head.
# 2) Verify the published packet against its author manifest and the publisher index.
# usage: source_and_packet_checks.sh <repo checkout at head> <evidence dir review-evidence/394-387-r1>
set -u
R=$1; EV=$2
echo "== link_status definition (milan_soc.py) =="
git -C "$R" grep -n -E 'self\.link_status = CSRStorage|CSRField\("link_up"|reset=1,' -- sw/litex/milan_soc.py | sed -n 1,4p
echo "== any writer of link_status / MAC_STATUS outside milan_soc.py (C, headers, Python, asm) =="
git -C "$R" grep -n -i -E 'link_status|mac_status' -- '*.c' '*.h' '*.S' '*.py' ':!sw/litex/milan_soc.py' ':!tb' | grep -v -i test || echo "  none besides a generator region marker above, if listed"
echo "== firmware MDIO use (C/headers under sw) =="
git -C "$R" grep -l -i 'mdio' -- 'sw/**/*.c' 'sw/**/*.h' || echo "  none"
echo "== MAC_STATUS reset composition: link_up=1 | speed=2<<1 | full_duplex=1<<3 =="
python3 -c "print(hex(1 | (2 << 1) | (1 << 3)))"
echo "== author MANIFEST.sha256 against the published files =="
( cd "$EV/author" && sha256sum -c MANIFEST.sha256 2>/dev/null | grep -v ': OK$' ; echo "  entries: $(wc -l < MANIFEST.sha256)" )
echo "== publisher MANIFEST.json =="
( cd "$EV" && python3 -c "
import json,hashlib
m=json.load(open('MANIFEST.json'))
bad=[e['file'] for e in m if hashlib.sha256(open(e['file'],'rb').read()).hexdigest()!=e['published_sha256']]
alt=[e['file'] for e in m if e['original_sha256']!=e['published_sha256']]
print('  entries',len(m),'; published-hash mismatches',len(bad),'; files altered at publication',len(alt))
print('  altered:',' '.join(f.split('/')[-1] for f in alt))" )
