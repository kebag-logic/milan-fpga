#!/usr/bin/env python3
"""Offline audit: audit_receipts.py REPO B18_ROOT B17_AUTHOR B17_R2. No input writes."""
import ast, copy, hashlib, json, re, sys
from pathlib import Path
from datetime import datetime, timezone
repo, root, old, old2 = map(Path, sys.argv[1:])
p = root / "author"
section = (repo / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md").read_text().split("## Dev 9ef71772, 2026-10-15: lane B18\n", 1)[1]
sha = lambda data: hashlib.sha256(data).hexdigest()
def jl(path): return [json.loads(x) for x in path.read_text().splitlines() if x.startswith("{")]
def check(ok, message):
    if not ok: raise AssertionError(message)
def bursts(rows):
    out = []
    for r in rows:
        if r["s"] <= 0 or r["late_us"] <= 20: continue
        if out and r["s"] - out[-1]["end"] < .001:
            out[-1]["end"] = r["s"]
            out[-1]["peak"] = max(out[-1]["peak"], r["late_us"])
        else: out.append(dict(start=r["s"], end=r["s"], peak=r["late_us"]))
    return out
def held(rows):
    vals = [int(r["words"]["0x8d4"], 16) for r in rows]
    return len(vals) == 80 and len(set(vals)) == 1 and (vals[0] & 65535) < 65535 and (vals[0] >> 16) < 65535
manifest = json.loads((root / "MANIFEST.json").read_text())
for m in manifest: check(sha((root / m["file"]).read_bytes()) == m["published_sha256"], m["file"])
print(f"Publication manifest: {len(manifest)} files match")
nh = 0
for line in section.splitlines():
    m = re.match(r"\| `([^`]+)`.*?\| ([\d,]+) \| `([0-9a-f]{64})` \|", line)
    if m:
        name, size, digest = m.groups(); data = (p / name).read_bytes()
        check(len(data) == int(size.replace(',', '')) and sha(data) == digest, name); nh += 1
print(f"Findings evidence table: {nh} sizes and SHA-256 values match")
for f, src in [("console_poll_b8.py",old),("ana_b17.py",old),("peer_gap_b17.py",old2)]:
    data = (p / "tools" / f).read_bytes()
    check(data == (src / "tools" / f).read_bytes(), f)
    print(f"Unchanged {f}: {sha(data)}")
a = (old / "tools/cyc_b17.py").read_text(); b = (p / "tools/cyc_b18.py").read_text()
b = b.replace('/tmp/645-b18/raw','/tmp/645-b17/raw').replace('/tmp/a622','/tmp/a619').replace('645-b18-{tag}.pcap','645-b17-{tag}.pcap')
check(ast.dump(ast.parse(a)) == ast.dump(ast.parse(b)), "cycle runner changed beyond paths/comments")
print("Cycle runner AST: equal after three path substitutions; two explanatory comment lines added")
print("cycle | polls | first s | last s | old last s | first burst s | peak us | burst count | margin after design firing ms")
all_words = {}; digest_lines=[]; margin=[]
for i in range(1,11):
    tag = f"c{i:02d}"
    es = jl(p / "cycles" / tag / "events.jsonl"); rows = jl(p / "cycles" / tag / "poll.jsonl")
    prev_rows = jl(old / "cycles" / tag / "poll.jsonl"); prev_es = jl(old / "cycles" / tag / "events.jsonl")
    bykind = lambda k: [r for r in es if r['kind'] == k]
    tb = bykind('bind-time')[0]['t_bind_local']; ob = next(r['t_bind_local'] for r in prev_es if r['kind']=='bind-time')
    start = bykind('start')[0]
    check(start['hold_s']==32 and start['unbind_to_bind_s']==6 and start['pre_unbind_s']==2, tag+' durations')
    for key,f in [('tool_sha256','cyc_b18.py'),('poller_sha256','console_poll_b8.py')]: check(start[key] == sha((p/'tools'/f).read_bytes()), tag+' as-run hash')
    check(held(rows),tag+' held'); check([r['n'] for r in rows]==list(range(80)),tag+' sequence')
    check(all(len(r['words'])==8 and all(v is not None for v in r['words'].values()) for r in rows),tag+' reads')
    check(all(int(r['words']['0x8d4'],16)==0 and int(r['words']['0x8d8'],16)==0 for r in rows),tag+' zeros')
    for r in rows:
        for k,v in r['words'].items(): all_words.setdefault(k,set()).add(v)
    for k in ('bind','unbind'): check(len(bykind(k))==1 and bykind(k)[0]['status']==0,tag+' '+k)
    check(not bykind('bind-retry'), tag+' retry')
    check(all(r['clk_dut']==0 and r['clk_peer']==1 for r in bykind('state')),tag+' clocks')
    check(all(r['talker_fmt']==r['listener_fmt']=='0205022001006000' and r['set'] is None for r in bykind('format-check')),tag+' formats')
    check(bykind('cycle-check')[0]['bound_as_found'],tag+' bind restore')
    g = json.loads((p/'summary'/f'{tag}.json').read_text())['tap']; og = json.loads((old/'summary'/f'{tag}.json').read_text())['tap']
    bs = bursts(g['late_pdus']); obs = bursts(og['late_pdus']); f0, f1 = rows[0]['t0']-tb, rows[-1]['t1']-tb
    upto = [x for x in bs if x['start']<=f1]; first = g['priming']['first_pdu_after_command_ms']
    margin.append(bs[0]['start']*1000-first-2048/48)
    check(not [x for x in g['late_pdus'] if 0<x['s']<bs[0]['start'] and x['late_us']>10],tag+' first late')
    check(all(v['seq_gaps']==0 for v in g['streams'].values()),tag+' sequence gaps')
    cells = [tag,datetime.fromtimestamp(tb,timezone.utc).strftime('%H:%M:%S.%f')[:12],f'80, {f0:.2f} to {f1:+.2f}', '0, 0 to 0, 0','None','Held',f'{first:.3f}',f"{bs[0]['start']:.2f}, {bs[0]['peak']:.1f} us",f"{len(upto)}, {max(x['peak'] for x in upto):.1f} us",'0 to 0, 1 to 1', f"{g['delta_ppm']:+.4f}" if g['delta_ppm'] else '0.0000']
    check('| ' + ' | '.join(cells) + ' |' in section,tag+' table')
    changes=[]
    for x,y in zip(prev_rows,prev_rows[1:]):
        vx,vy = int(x['words']['0x8d4'],16),int(y['words']['0x8d4'],16)
        if vx != vy: changes.append((x['t0']-ob,y['t1']-ob,(vy&65535)-(vx&65535), (vy>>16)-(vx>>16)))
    check(len(changes)==1 and changes[0][2:]==(2,0),tag+' old slip')
    lo,hi,_,_ = changes[0]; oldutc=datetime.fromtimestamp(ob,timezone.utc).strftime('%H:%M:%S.%f')[:12]
    line=f"| {tag} | {oldutc} | {og['priming']['first_pdu_after_command_ms']:.3f} | {lo:.2f} to {hi:.2f}, +2 dups | {obs[0]['start']:.2f}, {obs[0]['peak']:.1f} us | {first:.3f} | None | {bs[0]['start']:.2f}, {bs[0]['peak']:.1f} us |"
    check(line in section,tag+' comparison table')
    capture=bykind('capture-end')[0]; check(capture['remote_equal'] and capture['removed_from_tap'],tag+' capture copy')
    check(f"| {tag} | `{capture['file']}` | {capture['bytes']:,} | `{capture['sha256']}` |" in section,tag+' capture hash table')
    digest_lines.append(f"{sha((p/'cycles'/tag/'poll.jsonl').read_bytes())}  cycles/{tag}/poll.jsonl")
    def counters(payload):
        raw=bytes.fromhex(payload); mask=int.from_bytes(raw[4:8],'big')
        return {j:int.from_bytes(raw[8+j*4:12+j*4],'big') for j in range(32) if mask>>j&1}
    cs={x['when']:x['payloads'] for x in bykind('counters')}
    for k in cs['start']:
        ca,cz=counters(cs['start'][k]),counters(cs['end'][k]); changed={j for j in ca if ca[j]!=cz[j]}
        expected={'dut-0x0005-0':{6,11},'dut-0x0009-0':set(),'peer-0x0006-0':{0,1,4}}[k]
        check(changed==expected,tag+' counters '+k)
        if k=='peer-0x0006-0': check(cz[0]-ca[0]==cz[1]-ca[1]==1,tag+' start stop')
    print(f"{tag} | 80 | {f0:.6f} | {f1:.6f} | {prev_rows[-1]['t1']-ob:.6f} | {bs[0]['start']:.6f} | {bs[0]['peak']:.3f} | {len(upto)} | {margin[-1]:.6f}")
digest=('\n'.join(digest_lines)+'\n').encode()
check(digest==(p/'summary/counter-logs.sha256').read_bytes(),'digest contents')
check(sha(digest)=='2c5e8d6ff8220cb16a9a3d0535279dfd7f04b5642c9aee2d9f97cdefcd939bdb','digest sha')
print('Counter digest:',sha(digest))
check({k for k,v in all_words.items() if len(v)>1}=={'0x8dc'},'only render moved')
print('800 readable polls: SLIP_LB and SLIP_TDM zero; only RENDER_STAT varies')
print(f'First burst minus design firing: min {min(margin):.6f} ms; max {max(margin):.6f} ms')
volatile={'t','seq','rtt_ms','sequence_id','t_tx','t_rx'}
def strip(r):
    if isinstance(r,dict): return {k:strip(v) for k,v in r.items() if k not in volatile}
    if isinstance(r,list): return [strip(v) for v in r]
    return r
ca=[strip(r) for r in jl(p/'restore/census-start.jsonl')]; cz=[strip(r) for r in jl(p/'restore/census-end.jsonl')]
check(len(ca)==len(cz)==46,'census length'); diffs=[i for i,(a,b) in enumerate(zip(ca,cz)) if a!=b]
check(diffs==[8],'restore differences'); x,y=ca[8],cz[8]
check(x['cmd']==y['cmd']=='GET_AVB_INFO' and x['role']==y['role']=='dut','restore exception')
check(x['payload'].replace('0000017e','00000184')==y['payload'],'propagation delay only')
print('Restore: 45/46 census records equal; sole difference propagation delay 382 -> 388 ns')
for which,seq,commits in [('start',315,0),('end',335,20)]:
    s=(p/'restore'/f'dut-{which}.txt').read_text()
    check(f'image seq {seq}' in s and f'commits ok={commits} failed=0' in s and 'pend=0' in s,'NVM '+which)
    line=re.search(r'^0x900008d4\s+((?:[0-9a-f]{2} ){12})',s,re.M)
    check(line and bytes.fromhex(line.group(1))[:8]==bytes(8),'baseline '+which)
print('Baselines: slip words zero; NVM sequence 315 -> 335, commits 0 -> 20, no pending write')
def entity(d):
    r=next(x for x in jl(d/'identity-aecp.jsonl') if x.get('req')=='0000000000000000' and x.get('cmd')=='READ_DESCRIPTOR')
    check(r['status']=='SUCCESS','entity status'); b=bytes.fromhex(r['payload'])[4:]
    return [b[4:12],b[48:112],b[116:180],b[244:308]]
check(entity(p/'identity')==entity(old/'identity'),'B17 identity equality')
print('Four ATDECC identity fields: byte-identical to B17 raw ENTITY reply')
base=jl(p/'cycles/c01/poll.jsonl')
for label,value in [('one-pair dup','00000001'),('one-frame dup','00000002'),('skip','00010000')]:
    m=copy.deepcopy(base)
    for row in m[40:]: row['words']['0x8d4']=value
    check(not held(m),'missed planted '+label); print('Control detected:',label)
m=copy.deepcopy(base)
for row in m: row['words']['0x8d4']='0000ffff'
check(not held(m),'saturation false green'); print('Control detected: saturated constant counter')
print('RECEIPT AUDIT PASS; flash provenance and raw capture availability remain separate evidence questions')
