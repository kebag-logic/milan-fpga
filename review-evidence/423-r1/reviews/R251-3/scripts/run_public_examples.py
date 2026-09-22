"""Re-execute the original public locale fixtures, then add positive controls."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

p=argparse.ArgumentParser()
p.add_argument('checkout',type=Path)
p.add_argument('output',type=Path)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
a.output.mkdir(parents=True,exist_ok=True)
original=(root/'public/original-locale-probe.sh').read_text()
adapted=original.replace('HEAD_SHA=df53dfa116b34816db0193230ad9833e67bf46dd',
                         'HEAD_SHA=4671e582cfa4bba4809b9e3a354ce5b6eb967f99').replace('head-df53dfa1','head-4671e582')
script=a.output/'locale_transport_probe-corrected.sh'
script.write_text(adapted)
env=dict(os.environ,PYTHONUTF8='0',PYTHONCOERCECLOCALE='0',PYTHONDONTWRITEBYTECODE='1',
         LC_ALL='C.UTF-8',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,
         GIT_AUTHOR_NAME='Fixture',GIT_AUTHOR_EMAIL='fixture@example.invalid',
         GIT_COMMITTER_NAME='Fixture',GIT_COMMITTER_EMAIL='fixture@example.invalid')
records=[]
with tempfile.TemporaryDirectory(prefix='r251-original-examples-') as td:
    work=Path(td)
    cmd=['rtk','proxy','bash','-x',str(script),str(a.checkout.resolve()),str(work),str(a.output.resolve())]
    r=subprocess.run(cmd,env=env,capture_output=True)
    (a.output/'original-fixtures.stdout').write_bytes(r.stdout)
    (a.output/'original-fixtures.stderr').write_bytes(r.stderr)
    assert r.returncode==0,r.stderr
    lines=[line for line in r.stdout.decode().splitlines() if ' fs=' in line]
    assert len(lines)==8,lines
    for line in lines:
        expected='UNKNOWN' if line.startswith('merge/') and '/head-' in line else 'STRANDED'
        encoding='iso8859-1' if '/latin1/' in line else 'utf-8'
        assert f'fs={encoding} rc=1 | {expected}' in line,line
    records.append({'kind':'original_negative_examples','argv':cmd,'runner_exit':r.returncode,'rows':lines})
    print('\n'.join(lines))
    for fixture in ['linear','merge']:
        repo=work/'lp'/fixture
        def git(*args):
            return subprocess.run(['rtk','proxy','git',*args],cwd=repo,env=env,capture_output=True,check=True).stdout
        source=git('rev-parse','pr').strip().decode()
        git('--literal-pathspecs','checkout',source,'--',os.fsdecode(b'\xc3\xa9.txt'))
        git('commit','-qm','positive control: restore exact source filename bytes')
        for mode in ['utf8','ascii','latin1']:
            child=dict(env)
            if mode=='ascii':child['LC_ALL']='C'
            if mode=='latin1':child.update(LC_ALL='en_US.ISO-8859-1',LOCPATH=str(work/'lp/locale'))
            encoding=subprocess.run(['rtk','proxy','python3','-B','-c','import sys; print(sys.getfilesystemencoding())'],env=child,capture_output=True,check=True).stdout.decode().strip()
            expected_encoding={'utf8':'utf-8','ascii':'ascii','latin1':'iso8859-1'}[mode]
            assert encoding==expected_encoding,(mode,encoding)
            cmd=['rtk','proxy','python3','-B',str(a.checkout.resolve()/'scripts/check_merge_containment.py'),'--no-fetch','--base','main','pr']
            r=subprocess.run(cmd,cwd=repo,env=child,capture_output=True)
            label=f'{fixture}-{mode}-positive'
            (a.output/(label+'.stdout')).write_bytes(r.stdout)
            (a.output/(label+'.stderr')).write_bytes(r.stderr)
            assert r.returncode==0 and r.stdout.split()[0]==b'contained',(label,r)
            if fixture=='merge':assert b'raw no-op retention' in r.stdout
            records.append({'kind':label,'encoding':encoding,'argv':cmd,'exit':r.returncode,
                            'source':source,'target':git('rev-parse','main').strip().decode()})
            print(label,encoding,'contained / 0')
(a.output/'results.json').write_text(json.dumps(records,indent=2)+'\n')
