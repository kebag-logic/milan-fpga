#!/usr/bin/env python3
"""Exercise standalone runner regressions only inside the disposable boundary."""
import hashlib,io,json,pathlib,subprocess,sys,tarfile
mode=sys.argv[1];root=pathlib.Path('/tmp/candidate');root.mkdir()
archive=subprocess.run(['git','archive','HEAD'],stdout=subprocess.PIPE,check=True)
with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as t:t.extractall(root,filter='data')
runner=root/'scripts/act_ci.py'
if mode=='before':runner.write_bytes(subprocess.check_output(['git','show','97907c2e:scripts/act_ci.py']))
if mode=='R01':
    target=root/'scripts/ci_scope.py';old='failures += history_selftest(ROOT)';new='failures += 0'
else:
    target=runner
    old={'R02':'    """Independently pin the executed history population and kill disconnections."""','before':'    """Independently pin the executed history population and kill disconnections."""','R03':'    """Forked PRs and lanes that merge newer dev, restore RTL, then edit docs."""'}[mode]
    old += '\n'
    new=old+'    import ci_scope_history\n'
s=target.read_text();assert s.count(old)==1;target.write_text(s.replace(old,new));print('MUTATION',mode,'sha256',hashlib.sha256(target.read_bytes()).hexdigest(),flush=True)
for form in ('ordinary','flat'):
    if form=='flat':
        d=pathlib.Path('/tmp/install');d.mkdir();f=d/'act_ci.py';f.write_bytes(runner.read_bytes());f.chmod(0o555);assert list(d.iterdir())==[f]
        cmd=[sys.executable,'-I',str(f),'--selftest','--worktree',str(root)]
    else:cmd=[sys.executable,'scripts/act_ci.py','--selftest']
    result=subprocess.run(cmd,cwd=root,text=True,capture_output=True,timeout=400)
    print('COMMAND',json.dumps(cmd),'RC',result.returncode,flush=True);print(result.stdout+result.stderr,flush=True)
    expected=0 if mode=='before' and form=='ordinary' else 1
    assert result.returncode==expected,(mode,form,result.returncode)
    if expected and mode!='R01':assert "No module named 'ci_scope_history'" in result.stdout+result.stderr
    if expected and mode=='R01':assert 'FAIL classifier selftest accumulates the history result' in result.stdout
    print('CONTROL PASS',mode,form,flush=True)
