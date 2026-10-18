#!/usr/bin/env python3
"""Read-only source identity, interface and lightweight repository checks."""
import concurrent.futures, hashlib, json, os, pathlib, re, stat, subprocess, sys
src=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]).resolve()
def git(*args): return subprocess.check_output(['git',*args],cwd=src)
head='85373de08a5c35487f260087ac8ceaf7a3789cdc'
base='b9ade3a63d1b2292d75eb9b1809647e6439542a0'
assert git('rev-parse','HEAD').decode().strip()==head
def verify():
    tree=git('ls-tree','-rz',head); index=git('ls-files','--stage','-z')
    expected=[]; records=[]
    for e in tree.split(b'\0'):
        if not e: continue
        meta,name=e.split(b'\t'); mode,typ,oid=meta.split(); p=src/os.fsdecode(name)
        if mode==b'160000':
            records.append({'path':os.fsdecode(name),'gitlink':oid.decode()}); continue
        data=os.fsencode(os.readlink(p)) if mode==b'120000' else p.read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert got==oid.decode(),p
        actual=b'120000' if p.is_symlink() else (b'100755' if p.stat().st_mode & stat.S_IXUSR else b'100644')
        assert actual==mode,p
        expected.append(mode+b' '+oid+b' 0\t'+name+b'\0')
        records.append({'path':os.fsdecode(name),'mode':mode.decode(),'blob':oid.decode()})
    assert b''.join(expected)==index, 'index differs from HEAD'
    assert not git('diff','--name-only',head)
    return {'head':head,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'tracked_count':len(records),'gitlinks':[x for x in records if 'gitlink' in x],'verified':records}
before=verify()
def header(commit):
    s=git('show',commit+':hdl/top/KL_gptp_engine.sv').decode()
    s=re.sub(r'/\*.*?\*/','',s,flags=re.S);s=re.sub(r'//[^\n]*','',s)
    s=s[s.index('module KL_gptp_engine'):];s=s[:s.index(');')+2]
    return re.sub(r'\s+',' ',s).strip()
assert header(base)==header(head)
diff=git('diff',base,head,'--','hdl','tb').decode()
added=[l for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')]
residue=[l for l in added if re.match(r'^\+\s*(?://|#)',l) and re.search(r'\b(?:B\d+|R\d{3}|A\d{3}|lane|review round|issuecomment-)\b',l,re.I)]
(out/'interface-check.json').write_text(json.dumps({'base':base,'head':head,'declaration_equal':True,'normalized_declaration_sha256':hashlib.sha256(header(head).encode()).hexdigest(),'new_comment_label_matches':residue},indent=2)+'\n')
env=os.environ.copy();env['PATH']='$VALIDATION_TOOLS/pinned-verilator-5.050:'+env['PATH'];env['TMPDIR']=str(out/'scratch/tmp');pathlib.Path(env['TMPDIR']).mkdir(exist_ok=True)
def gate(target):
    with open(out/(target+'.log'),'w') as f: r=subprocess.run(['make','-j16',target],cwd=src,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=540)
    (out/(target+'.log.rc')).write_text(str(r.returncode)+'\n');return target,r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: results=dict(ex.map(gate,['contract','docs','lint']))
after=verify();assert before==after
(out/'source-integrity.json').write_text(json.dumps(after,indent=2)+'\n')
(out/'local-gates.json').write_text(json.dumps(results,indent=2)+'\n'); print(json.dumps(results));print('Exact tracked bytes, modes and index verified; no nested gitlinks.')
