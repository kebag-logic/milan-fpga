"""Reproduce the remaining path-control failure, without changing source."""
import argparse
import codecs
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

p=argparse.ArgumentParser()
p.add_argument('checkout',type=Path)
p.add_argument('output',type=Path)
p.add_argument('--child',choices=['utf-8','iso8859-1'])
p.add_argument('--full',action='store_true')
a=p.parse_args()
a.checkout=a.checkout.resolve()
a.output=a.output.resolve()
a.output.mkdir(parents=True,exist_ok=True)

if not a.child:
    with tempfile.TemporaryDirectory(prefix='r251-parent-locale-') as td:
        work=Path(td)
        loc=work/'locales'
        loc.mkdir()
        r=subprocess.run(['rtk','proxy','localedef','--no-archive','-i','en_US','-f','ISO-8859-1',str(loc/'en_US.ISO-8859-1')],capture_output=True)
        assert r.returncode==0,('Latin-1 NOT RUN',r.stderr)
        old=work/'old'
        (old/'scripts').mkdir(parents=True)
        commit='df53dfa116b34816db0193230ad9833e67bf46dd'
        files=subprocess.run(['rtk','proxy','git','-C',str(a.checkout),'ls-tree','-r','--name-only',commit,'--','scripts'],capture_output=True,check=True).stdout.decode().splitlines()
        for name in files:
            if 'containment' in name and name.endswith('.py'):
                data=subprocess.run(['rtk','proxy','git','-C',str(a.checkout),'show',commit+':'+name],capture_output=True,check=True).stdout
                (old/name).write_bytes(data)
        records=[]
        for label,source in [('previous',old),('corrected',a.checkout)]:
            for encoding,locale in [('utf-8','C.UTF-8'),('iso8859-1','en_US.ISO-8859-1')]:
                dest=a.output/(label+'-'+encoding)
                dest.mkdir(exist_ok=True)
                cwd=work/(label+'-'+encoding)
                cwd.mkdir()
                env=dict(os.environ,LC_ALL=locale,LOCPATH=str(loc),PYTHONUTF8='0',PYTHONCOERCECLOCALE='0',
                         PYTHONIOENCODING='utf-8:backslashreplace',PYTHONDONTWRITEBYTECODE='1')
                cmd=['rtk','proxy','python3','-B',str(Path(__file__).resolve()),str(source),str(dest),'--child',encoding]
                r=subprocess.run(cmd,env=env,cwd=cwd,capture_output=True)
                (dest/'stdout').write_bytes(r.stdout)
                (dest/'stderr').write_bytes(r.stderr)
                expected=1 if label=='corrected' and encoding=='iso8859-1' else 0
                records.append({'source':label,'encoding':encoding,'argv':cmd,'exit':r.returncode,'expected':expected})
                assert r.returncode==expected,(label,encoding,r.stderr)
                print(label,encoding,'exit',r.returncode,flush=True)
        if a.full:
            env=dict(os.environ,LC_ALL='en_US.ISO-8859-1',LOCPATH=str(loc),PYTHONUTF8='0',PYTHONCOERCECLOCALE='0',
                     PYTHONIOENCODING='utf-8:backslashreplace',PYTHONDONTWRITEBYTECODE='1')
            cmd=['rtk','proxy','python3','-B',str(a.checkout/'scripts/check_merge_containment.py'),'--selftest']
            r=subprocess.run(cmd,cwd=a.checkout,env=env,capture_output=True)
            (a.output/'full.stdout').write_bytes(r.stdout)
            (a.output/'full.stderr').write_bytes(r.stderr)
            records.append({'kind':'full-default-selftest','argv':cmd,'exit':r.returncode})
            assert r.returncode==1,r.stderr
        (a.output/'processes.json').write_text(json.dumps(records,indent=2)+'\n')
    raise SystemExit(0)

actual=codecs.lookup(sys.getfilesystemencoding()).name
assert actual==a.child,(actual,a.child)
sys.path.insert(0,str(a.checkout/'scripts'))
import check_merge_containment as mc
import merge_containment_selftest_retention as retention
from merge_containment_selftest_replay import _History
from merge_containment_selftest_scratch import quiet_git
from merge_containment_selftest import _Fixture

rows=[]
runs=[]
def case(name,got,want,why):
    rows.append({'name':name,'got':got,'want':want,'pass':got==want})
def run(args):
    output=io.StringIO()
    with contextlib.redirect_stdout(output),contextlib.redirect_stderr(io.StringIO()):
        rc=mc.main(['checker',*args])
    runs.append({'argv':args,'exit':rc,'output':output.getvalue()})
    return rc,output.getvalue()
with quiet_git():
    history=_History()
    history._git('init','-q','-b','main')
    retention._path_and_format_cases(_Fixture(mc,case,run),history)
bad=[row for row in rows if not row['pass']]
assert len(rows)==22,len(rows)
path_bytes=b'raw-\xff'
expected_literal=repr('raw-\udcff')
actual_literal=repr(os.fsdecode(path_bytes))
record={'encoding':actual,'assertions':len(rows),'failures':bad,'rows':rows,'runs':runs,
        'raw_path_hex':path_bytes.hex(),'fixture_expected_repr':expected_literal,
        'filesystem_decoded_repr':actual_literal,
        'roundtrip_hex':os.fsencode(os.fsdecode(path_bytes)).hex()}
(a.output/'result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=True))
raise SystemExit(1 if bad else 0)
