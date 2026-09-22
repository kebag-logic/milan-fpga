"""Independent commit-tree fixtures; no production predicate supplies expected outcomes."""
import contextlib, hashlib, io, json, os, subprocess, sys, tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent
SOURCE=Path('$VALIDATION_STORAGE/reviews/r243-423-r1')
sys.path.insert(0,str(SOURCE/'scripts'))
import check_merge_containment as mc
import merge_containment_replay as replay
os.environ.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,
 GIT_AUTHOR_NAME='R243 fixture',GIT_AUTHOR_EMAIL='r243@example.invalid',
 GIT_COMMITTER_NAME='R243 fixture',GIT_COMMITTER_EMAIL='r243@example.invalid',
 GIT_AUTHOR_DATE='@1790000000 +0000',GIT_COMMITTER_DATE='@1790000000 +0000',
 PYTHONDONTWRITEBYTECODE='1')
records=[]

def git(*args,data=None,allowed=(0,)):
 p=subprocess.run(['rtk','proxy','git','--no-replace-objects',*args],input=data,capture_output=True)
 assert p.returncode in allowed,(args,p.returncode,p.stderr)
 return p.stdout

def tree(entries):
 rows=[]
 for name,(mode,data) in entries.items():
  kind='commit' if mode=='160000' else 'blob'
  oid=data if kind=='commit' else git('hash-object','-w','--stdin',data=data).strip()
  rows.append(mode.encode()+b' '+kind.encode()+b' '+oid+b'\t'+os.fsencode(name)+b'\0')
 return git('mktree','-z',data=b''.join(rows)).strip().decode()

def commit(entries,parents,label):
 args=['commit-tree',tree(entries),'-m',label]
 for p in parents:args+=['-p',p]
 return git(*args).strip().decode()

def run_case(label,branch,tip,want,path=None):
 git('update-ref','refs/heads/pr',branch);git('update-ref','refs/heads/main',tip)
 buf=io.StringIO(); trace=[]
 def record(*args):
  rc,out=real_bytes(*args);trace.append(dict(args=args,rc=rc,sha256=hashlib.sha256(out).hexdigest(),length=len(out)));return rc,out
 real_bytes=replay._git_bytes
 with patch.object(replay,'_git_bytes',record),contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
  rc=mc.main(['checker','--no-fetch','--base','main','pr'])
 output=buf.getvalue(); actual=[rc,output.split()[0]]
 assert actual==list(want),(label,actual,output)
 if path is not None: assert repr(path) in output,(label,path,output)
 cli=subprocess.run(['rtk','proxy',sys.executable,'-B','-I',str(SOURCE/'scripts/check_merge_containment.py'),'--no-fetch','--base','main','pr'],capture_output=True)
 assert [cli.returncode,cli.stdout.split()[0].decode()]==actual
 item=dict(label=label,branch=branch,tip=tip,expected=want,actual=actual,stdout=output,stderr=cli.stderr.decode('utf8','surrogateescape'),raw_trace=trace)
 records.append(item);return item

base_bytes=b''.join(f'line {i:02d}\n'.encode() for i in range(60))
change_a=base_bytes.replace(b'line 05\n',b'SOURCE A\n')
change_c=change_a.replace(b'line 30\n',b'SOURCE C\n')
far=change_c.replace(b'line 55\n',b'LATER EXTENSION\n')

def history(path,original=base_bytes,source=change_c,current=far,mode='100644',tipmode=None):
 def entries(data,m=mode):return {path:(m,data)}
 o=commit(entries(original),[],'original')
 a=commit(entries(source),[o],'source first')
 m=commit(entries(source),[o,a],'redundant merge')
 # second independent touched path makes the nonmerge sequence observable.
 branch=commit({**entries(source),'control':('100644',b'source control\n')},[m],'source second')
 ap=commit(entries(source),[o],'replayed first')
 cp=commit({**entries(source),'control':('100644',b'source control\n')},[ap],'replayed second')
 tip=commit({**entries(current,tipmode or mode),'control':('100644',b'source control\n')},[cp],'later tip')
 return o,branch,tip,ap,cp

with tempfile.TemporaryDirectory(prefix='r243-independent-',dir=ROOT) as directory:
 os.chdir(directory);git('init','-q','-b','main')
 for suffix,data in [('lf',base_bytes),('crlf',base_bytes.replace(b'\n',b'\r\n')),('no-final-lf',base_bytes.rstrip(b'\n')),('non-utf8',base_bytes+b'\xff\n')]:
  a=data.replace(b'line 05',b'SOURCE A').replace(b'line 30',b'SOURCE C');t=a.replace(b'line 55',b'LATER')
  p='raw-\udcff\r\n'+suffix
  o,b,t0,ap,cp=history(p,data,a,t);row=run_case('retained-'+suffix,b,t0,(0,'contained'))
  assert 'raw no-op retention' in row['stdout']
  # Partial reversion makes a conflict-free merge that changes output.
  o,b,t0,ap,cp=history(p,data,a,t.replace(b'SOURCE A',b'line 05'))
  row=run_case('partial-reversal-'+suffix,b,t0,(1,'UNKNOWN'),p)
  merges=[r for r in row['raw_trace'] if 'merge-file' in r['args']]
  assert merges and merges[0]['rc']==0
  assert merges[0]['sha256']!=hashlib.sha256(t.replace(b'SOURCE A',b'line 05')).hexdigest()
 # Every possible later replacement position against two source edits.
 for i in (0,4,5,6,28,29,30,31,32,59):
  tipdata=change_c.replace(f'line {i:02d}\n'.encode(),b'LATER\n')
  if i==5:tipdata=change_c.replace(b'SOURCE A\n',b'line 05\n')
  if i==30:tipdata=change_c.replace(b'SOURCE C\n',b'line 30\n')
  o,b,t,_,_=history('positions',current=tipdata)
  want=(0,'contained') if i in (0,28,32,59) else (1,'UNKNOWN')
  run_case('current-position-'+str(i),b,t,want)
 # The previous linear policy remains historical even for CRLF/raw paths.
 p='old-arm-\udcff\r\n';d0={p:('100644',base_bytes.replace(b'\n',b'\r\n'))}
 d1={p:('100644',change_a.replace(b'\n',b'\r\n'))};d2={p:('100644',far.replace(b'\n',b'\r\n'))}
 o=commit(d0,[],'old original');a=commit(d1,[o],'linear source');ap=commit(d1,[o],'linear replay');t=commit(d0,[ap],'later reversal')
 row=run_case('old-linear-historical-crlf',a,t,(0,'contained'));assert 'every commit has a whitespace-exact' in row['stdout']
 # Touched-path identity must preserve the original literal raw path.
 t=commit({**d1,'unrelated':('100644',b'later')},[o],'squash')
 row=run_case('old-path-identity-crlf',a,t,(0,'contained'));assert 'every path this branch touched is identical' in row['stdout']
 # Differing postimage with NUL-delimited CRLF/nonUTF8 path stays refused.
 t=commit(d2,[o],'no matching replay')
 row=run_case('old-differing-path-crlf',a,t,(1,'STRANDED'));assert p in row['stdout']
 # Distinct H witnesses: A, reverse-A, A need two replays of A.
 d0={'data':('100644',base_bytes)};d1={'data':('100644',change_a)}
 o=commit(d0,[],'distinct original');a=commit(d1,[o],'first A');m=commit(d1,[o,a],'redundant distinct')
 r=commit(d0,[m],'source reverse A');c=commit(d1,[r],'second A')
 ap=commit(d1,[o],'single A replay');rp=commit(d0,[ap],'single reverse replay')
 t=commit({'data':('100644',change_a.replace(b'line 55',b'LATER'))},[rp],'combined reapply extension')
 row=run_case('distinct-history-required',c,t,(1,'STRANDED'))
 code=(SOURCE/'scripts/check_merge_containment.py').read_text();assert code.count('candidates.remove(match)')==1
 mutant=ROOT/'mutants/distinct-history';mutant.mkdir(parents=True,exist_ok=True)
 (mutant/'check_merge_containment.py').write_text(code.replace('candidates.remove(match)','pass # R243 removes distinct matching'))
 (mutant/'merge_containment_replay.py').write_bytes((SOURCE/'scripts/merge_containment_replay.py').read_bytes())
 p0=subprocess.run(['rtk','proxy',sys.executable,'-B','-I',str(mutant/'check_merge_containment.py'),'--no-fetch','--base','main','pr'],capture_output=True)
 assert p0.returncode==0 and b'raw no-op retention' in p0.stdout
 row['distinct_mutant']={'exit':p0.returncode,'stdout':p0.stdout.decode()}
 # Shared _git byte transport preserves CRLF, all byte values, path NULs.
 payload=bytes(range(256))+b'\r\n\xff\n'
 oid=git('hash-object','-w','--stdin',data=payload).strip().decode()
 rc,out=mc._git('cat-file','blob',oid);assert rc==0 and out.encode('utf8','surrogateescape')==payload.rstrip(b'\n')
 records.append({'label':'shared-transport-roundtrip','strip_contract':'terminal LF stripping remains existing behavior','raw_sha256':hashlib.sha256(payload).hexdigest()})
(ROOT/'independent-history-data.json').write_text(json.dumps(records,indent=2)+'\n')
print('PASS',len(records),'independent cases; real CLI and raw merge traces recorded')
