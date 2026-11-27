#!/usr/bin/env python3
"""Audit public receipt hashes, executable counts, scope, and repository integrity."""
import argparse,ast,hashlib,json,os,stat,subprocess
from pathlib import Path
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True)
    a=ap.parse_args();repo=a.repo.resolve();packet=a.packet.resolve();out=packet/'receipts'
    def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
    entries=git('ls-tree','-rz','HEAD').split(b'\0');bad=[];tracked=[];links=[]
    for entry in filter(None,entries):
        head,path=entry.split(b'\t',1);mode,kind,oid=head.decode().split();name=os.fsdecode(path)
        if mode=='160000':links.append({'path':name,'oid':oid});continue
        p=repo/name
        data=os.fsencode(os.readlink(p)) if mode=='120000' else p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        executable=bool(p.stat().st_mode & stat.S_IXUSR)
        valid=actual==oid and (mode=='120000' or executable==(mode=='100755'))
        if not valid:bad.append(name)
        tracked.append({'path':name,'mode':mode,'blob':oid,'bytes':len(data),'verified':valid})
    index_diff=git('diff','--cached','--raw','HEAD').decode()
    result={'head':git('rev-parse','HEAD').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),
            'tracked':tracked,'bad':bad,'index_diff':index_diff,'gitlinks':links,'status':git('status','--porcelain').decode()}
    (out/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')
    rows=[]
    for row in json.loads((packet/'public-evidence/MANIFEST.json').read_text()):
        data=(packet/'public-evidence'/row['file']).read_bytes();digest=hashlib.sha256(data).hexdigest()
        rows.append({'file':row['file'],'expected':row['published_sha256'],'sha256':digest,'match':digest==row['published_sha256']})
    (out/'public-hashes.json').write_text(json.dumps(rows,indent=2)+'\n')
    tree=ast.parse((repo/'tests/check_reversals.py').read_text());cases=[];needs=set()
    # Evaluate only the static table in an isolated dictionary with its path constants.
    env={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            try:
                value=eval(compile(ast.Expression(node.value),'static-table','eval'),{'__builtins__':{}},env)
                for target in node.targets:
                    if isinstance(target,ast.Name):env[target.id]=value
            except (NameError,TypeError,AttributeError):pass
    cases=env['CASES'];needs=env['NEEDS_KEY']
    counts={'listed':len(cases),'scale_OFF_selected':sum(c[0] not in needs for c in cases),'scale_ON_selected':sum(c[0] in needs for c in cases)}
    (out/'reversal-counts.json').write_text(json.dumps(counts,indent=2)+'\n')
    additions=git('diff','--name-only','d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b..HEAD').decode().splitlines()
    scope={'changed_files':additions,'rtl_changes':[p for p in additions if p.endswith(('.sv','.v','.vhd','.vhdl'))],
           'changelog_files':[r['path'] for r in tracked if 'changelog' in r['path'].lower()],
           'generated_bytecode':[r for r in tracked if r['path'].endswith('.pyc')]}
    (out/'scope.json').write_text(json.dumps(scope,indent=2)+'\n')
    print(json.dumps({'integrity_ok':not bad and not index_diff and not result['status'],'public_hashes_match':sum(r['match'] for r in rows),'public_files':len(rows),'reversal_counts':counts,'gitlinks':links}))
if __name__=='__main__':main()
