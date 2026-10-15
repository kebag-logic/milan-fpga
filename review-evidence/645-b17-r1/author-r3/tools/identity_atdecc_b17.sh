#!/usr/bin/env bash
# Lane B17 resume: the quick identity re-check over ATDECC only (the resume ruling: no SoC board,
# identity re-checked over ATDECC). Under the bench lock: READ_DESCRIPTOR ENTITY 0 and
# GET_CLOCK_SOURCE on the DUT through avdecc_ro.py on the controller host, then the four ATDECC
# facts are checked offline. Read-only on the DUT and the controller host; the controller staging
# /tmp/a619 is created here and removed by the lane's end.
# usage: identity_atdecc_b17.sh <packet_dir> <out_subdir>
set -u
. "${B17_ENV:?}"
P=$1; D=$2
mkdir -p "$P/$D"
timeout -k 5 120 flock -w 60 /tmp/milan-bench.lock bash -c '
set -u
P=$0; D=$1
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a619" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$CTL_HOST:/tmp/a619/"
echo "STAGE_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a619 && sha256sum avdecc_ro.py; sudo -n timeout 30 python3 -B avdecc_ro.py aem $CTL_IFACE \
  020000fffe000001 020000000001 0x0004 0000000000000000 0x0017 00240000" > "$P/$D/identity-atdecc.jsonl" 2>&1
echo "AECP_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$D"
echo "LOCK_RC=$?"
python3 -I - "$P/$D/identity-atdecc.jsonl" <<'EOF'
import json, sys
want = dict(entity_id="020000fffe000001", entity_name="Milan FPGA 1x1 TDM8", firmware_version="2.96.0",
            serial_number="AX7101-0001")
ent = clk = None
for line in open(sys.argv[1]):
    if line.startswith("{"):
        r = json.loads(line)
        if r.get("cmd") == "READ_DESCRIPTOR" and r.get("status") == "SUCCESS":
            ent = bytes.fromhex(r["payload"])[4:]
        if r.get("cmd") == "GET_CLOCK_SOURCE" and r.get("status") == "SUCCESS":
            clk = int(r["payload"][8:12], 16)
s = lambda b: b.split(b"\0", 1)[0].decode("utf-8", "replace")
got = dict(entity_id=ent[4:12].hex(), entity_name=s(ent[48:112]), firmware_version=s(ent[116:180]),
           serial_number=s(ent[244:308])) if ent else {}
ok = got == want
print(json.dumps(dict(read=got, expected=want, clock_source=clk, verdict="PASS" if ok else "FAIL")))
sys.exit(0 if ok else 4)
EOF
