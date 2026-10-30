import ast,hashlib,json,pathlib,re,stat,subprocess,sys
P=pathlib.Path(__file__).resolve().parent; S=pathlib.Path(sys.argv[1]).resolve()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip()
assert head=='013ee63fd42455987ddbbbeb3b66f5af106b5793'
tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=S,text=True).strip()
assert tree=='b0f66acb645e958b1c9212c9e4d842991154a9a8'
index=subprocess.check_output(['git','ls-files','--stage','-z'],cwd=S).split(b'\0')
tracked=subprocess.check_output(['git','ls-tree','-rz','HEAD'],cwd=S).split(b'\0')
expected={}; blobs=[];links=[]
for entry in tracked:
 if not entry: continue
 meta,name=entry.split(b'\t'); mode,kind,oid=meta.decode().split(); n=name.decode()
 expected[n]=(mode,oid)
 if kind=='commit': links.append((n,oid)); continue
 f=S/n; data=f.read_bytes()
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==oid,n
 actual='100755' if f.stat().st_mode & stat.S_IXUSR else '100644'
 assert actual==mode,n
 blobs.append(n)
for entry in index:
 if not entry:continue
 meta,name=entry.split(b'\t');mode,oid,stage=meta.decode().split()
 assert stage=='0' and expected.pop(name.decode())==(mode,oid)
assert not expected
status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=S,text=True)
assert not status,status
(P/'tracked-integrity.json').write_text(json.dumps(dict(head=head,tree=tree,tracked_blobs=len(blobs),gitlinks=links,index_and_modes='match',status='clean'),indent=2)+'\n')
module=ast.parse((S/'tb/pp_top/aecp_dispatch_mutants.py').read_text())
mutants=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MUTANTS' for t in n.targets))
readme=(S/'tb/pp_top/README.md').read_text(); results=[]
for arm,patch,target,label in mutants:
 if not arm.startswith('rbt-'):continue
 f=P/'public/author-r3/receipts/campaigns/aecp-dispatch-013ee63/aecp-dispatch-out'/f'{arm}.log'
 s=f.read_text(); failures=[x for x in s.splitlines() if x.startswith('FAIL:')]
 row=next(x for x in readme.splitlines() if x.startswith('| `'+arm+'` |'))
 expected_count=int(row.split('|')[-2].strip())
 named=any(x[len('FAIL:'):].strip().startswith(label) for x in failures)
 complete='[build default,' in s
 assert named and complete and len(failures)==expected_count,arm
 results.append(dict(arm=arm,failures=len(failures),named=named,complete=complete,readme_count=expected_count))
(P/'mutation-audit.json').write_text(json.dumps(results,indent=2)+'\n')
print('Tracked source:',len(blobs),'blobs, modes/index match; no submodule gitlinks' if not links else str(links))
print('Published REBOOT arms:',len(results),'complete, named failures and README counts match')
