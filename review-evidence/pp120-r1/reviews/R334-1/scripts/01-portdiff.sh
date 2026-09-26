#!/usr/bin/env bash
# Elaborate protocol_processor_top at base and head, dump every port of the top,
# KL_aecp_engine and KL_aecp_desc_store (name, direction, packed width), and diff.
set -euo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); V=$PK/tools/verilator
for t in base head; do
  cd $PK/scratch/$t/tb/pp_top
  srcs=$(make -s --eval 'print-srcs: ; @echo $(SRCS)' print-srcs)
  mkdir -p $PK/scratch/json-$t
  $V --json-only --json-only-output $PK/scratch/json-$t/top.json -Wno-fatal -Wno-lint -Wno-style \
     --top-module protocol_processor_top $(echo $srcs | tr ' ' '\n' | grep -v pp_top_wrap | sed "s#^#$PWD/#") >/dev/null 2>$PK/scratch/json-$t/err.log
  python3 - "$PK/scratch/json-$t/top.json" > $PK/scratch/json-$t/ports.txt <<'P'
import json,sys
j=json.load(open(sys.argv[1]))
want={'protocol_processor_top','KL_aecp_engine','KL_aecp_desc_store'}
types={}
def walk(n,f):
    if isinstance(n,dict):
        f(n)
        for v in n.values(): walk(v,f)
    elif isinstance(n,list):
        for v in n: walk(v,f)
def collect(n):
    if n.get('type') in ('BASICDTYPE','PACKARRAYDTYPE','STRUCTDTYPE','ENUMDTYPE','REFDTYPE','UNPACKARRAYDTYPE') and 'addr' in n:
        types[n['addr']]=n
walk(j,collect)
out=[]
def mods(n):
    if n.get('type')=='MODULE':
        base=n.get('origName',n.get('name'))
        if base in want:
            for s in n.get('stmtsp',[]):
                if s.get('type')=='VAR' and s.get('direction','NONE') not in ('NONE',''):
                    d=types.get(s.get('dtypep'),{})
                    out.append(f"{base} {n.get('name')} {s['direction']} {s.get('origName',s['name'])} {d.get('range',d.get('type',''))} {d.get('name','')}")
walk(j,mods)
print('\n'.join(sorted(set(out))))
P
done
wc -l $PK/scratch/json-*/ports.txt
diff $PK/scratch/json-base/ports.txt $PK/scratch/json-head/ports.txt && echo NO-DIFF || true
