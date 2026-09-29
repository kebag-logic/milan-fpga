#!/bin/sh
# R405-4: seed faults into disposable copies of the archived author packet and
# check that both census checkers (the reviewer's r405_4_census.py and the
# author's round-4 census_b2r4.py) fail on each, and pass on the control.
# Usage: r405_4_probes.sh <packet-dir>   (expects scratch/review-evidence/b2-r1/)
set -u
P=$1; EV=$P/scratch/review-evidence/b2-r1; W=$P/scratch/probes
MINE="python3 -B $P/scripts/r405_4_census.py"
THEIRS="python3 -B $EV/author-r4/scripts/census_b2r4.py"
rm -rf "$W"; mkdir -p "$W"
mutate() {  # name, python snippet operating on directory d
  rm -rf "$W/$1"; cp -a "$EV/author" "$W/$1"
  [ -n "$2" ] && python3 -c "import json,os,glob,re; d='$W/$1'
$2"
  # the reviewer's checker verifies published_sha256; refresh the edited entries in a probe manifest
  python3 - "$W/$1" "$EV/MANIFEST.json" "$W/$1.manifest.json" <<'EOF'
import hashlib, json, os, sys
d, src, dst = sys.argv[1:]
m = json.load(open(src))
for e in m:
    f = e["file"]
    if f.startswith("author/") and os.path.exists(os.path.join(d, f[len("author/"):])):
        e["published_sha256"] = hashlib.sha256(open(os.path.join(d, f[len("author/"):]), "rb").read()).hexdigest()
json.dump(m, open(dst, "w"))
EOF
  $MINE "$W/$1" "$W/$1.manifest.json" > "$W/$1.mine.txt" 2>&1; rm=$?
  $THEIRS "$W/$1" > "$W/$1.theirs.txt" 2>&1; rt=$?
  echo "$1: reviewer rc=$rm [$(grep '^RESULT' "$W/$1.mine.txt")]  author rc=$rt [$(grep -c '^FAIL' "$W/$1.theirs.txt") FAIL lines: $(grep '^FAIL' "$W/$1.theirs.txt" | cut -c1-90 | tr '\n' ';')]"
}
mutate control ""
# M1: a CONNECT_RX addressed to the DUT's Stream Input 1, appended to one cycle transcript
mutate m1_connect_rx_to_dut_input '
p=d+"/cycles/cycle-050/cycle.jsonl"; r={"status":0,"stream_id":"0"*16,"controller":"<controller-host-id>","talker":"3cc0c60102030000","listener":"020000fffe000001","talker_uid":2,"listener_uid":1,"dmac":"0"*12,"conn_count":1,"flags":"0x0000","vlan":0}
open(p,"a").write(json.dumps({"role":"dut","what":"acmp-6","response":r,"t":1.0})+"\n"+json.dumps({"kind":"transaction","mt":6,"seq":1,"start":1.0,"end":1.0,"response":r,"t":1.0})+"\n")'
# M2: one DUT AECP command turned into a SET_ command
mutate m2_aecp_set_to_dut '
p=d+"/restore/census-start.jsonl"; s=open(p).read(); s=s.replace("\"cmd\":\"GET_CLOCK_SOURCE\"","\"cmd\":\"SET_CLOCK_SOURCE\"",1); open(p,"w").write(s)'
# M3: one GET_COUNTERS on DUT Stream Input 1 removed (227 left)
mutate m3_drop_dut_input_counter '
p=d+"/cycles/cycle-010/snapshot-before.jsonl"; L=open(p).read().splitlines(True); i=[k for k,l in enumerate(L) if "\"role\":\"dut\",\"what\":\"counter-5-1\"" in l][0]; del L[i]; open(p,"w").write("".join(L))'
# M4: a DUT READ_DESCRIPTOR retargeted from CLOCK_SOURCE (0x000a) to STREAM_INPUT (0x0005): 5 input reads
mutate m4_extra_dut_input_read '
p=d+"/restore/census-end.jsonl"; L=open(p).read().splitlines(True)
for k,l in enumerate(L):
    x=json.loads(l)
    if x.get("role")=="dut" and x.get("what")=="desc-10-0":
        x["response"]["payload"]=x["response"]["payload"][:8]+"0005"+x["response"]["payload"][12:]; L[k]=json.dumps(x,separators=(",",":"))+"\n"; break
open(p,"w").write("".join(L))'
# M5: a DISCONNECT_RX retargeted to the DUT listener, Stream Input 1
mutate m5_disconnect_rx_to_dut '
p=d+"/bind/unbind-2/unbind.jsonl"; s=open(p).read()
s=re.sub(r"(\"what\":\"acmp-8\",\"response\":\{[^}]*\"listener\":\")3cc0c60102030000(\",\"talker_uid\":\d+,\"listener_uid\":)8", r"\g<1>020000fffe000001\g<2>1", s, count=1)
s=re.sub(r"(\"mt\":8,[^\n]*\"listener\":\")3cc0c60102030000(\",\"talker_uid\":\d+,\"listener_uid\":)8", r"\g<1>020000fffe000001\g<2>1", s, count=1)
open(p,"w").write(s)'
for m in m1_connect_rx_to_dut_input m2_aecp_set_to_dut m3_drop_dut_input_counter m4_extra_dut_input_read m5_disconnect_rx_to_dut; do
  n=$(diff -r "$EV/author" "$W/$m" | grep -c '^[<>]'); echo "   $m: changed lines vs archive: $n"
done
