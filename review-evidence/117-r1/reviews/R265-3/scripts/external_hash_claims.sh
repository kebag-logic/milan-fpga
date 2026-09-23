#!/usr/bin/env bash
# Check the page hashes that live outside the evidence archive.
# Usage: external_hash_claims.sh <clone> <evidence-root> <issue-117-comments.txt>
# The comments file is the concatenated public issue #117 comments, each headed "=== <id> <user> <date>".
set -u
clone=$1 root=$2 comments=$3
echo "== UART grader: sha256 of scripts/baremetal_uart_smoke.py"
for r in ede8d48e 8016f7ac; do printf '%s ' $r; git -C "$clone" show $r:scripts/baremetal_uart_smoke.py | sha256sum; done
echo "== presence in identity/expected-crc.txt (both packets)"
for h in f0725eef7a361bd7dc6d692c369868f25e5d4f49f6b7267562a0b5f949ada33d aaece32fc6c84f790273878350f674c142407a6b9ff2097862870784921da5fb \
         9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404 e84e579c 69322600 4db0e6da 71e798fc; do
  printf '%s a200:%s a202:%s\n' ${h:0:8} $(grep -c $h "$root/bench-a200/identity/expected-crc.txt") $(grep -c $h "$root/bench-a202/identity/expected-crc.txt")
done
cmp -s "$root/bench-a200/identity/expected-crc.txt" "$root/bench-a202/identity/expected-crc.txt" && echo "expected-crc.txt identical in both packets"
echo "== public issue #117 comments carrying the quoted prefixes (comment id, date, token length)"
python3 - "$comments" <<'PY'
import re, sys
t = open(sys.argv[1]).read()
for p in re.split(r"(?m)^=== ", t)[1:]:
    cid, _, date = p.split(" ", 3)[:3]
    for key in ("95d64fd5", "ad579e18", "0e9faf30", "8ef4b008", "33f0e7f9", "f0725eef", "9b077636", "71e798fc"):
        for m in re.finditer(key + r"[0-9a-f]*", p):
            print(f"{key} comment {cid} {date[:10]} token-len {len(m.group(0))}")
PY
