# SPDX-License-Identifier: Apache-2.0
import hashlib,json,os,pathlib,re,stat,subprocess,sys
sys.dont_write_bytecode = True
from run_common import ROOT,PACKET,SCRATCH,RECEIPTS
HEAD='a29f8d13ff4869e54997d9adf05d83a4ace4b8bd'
TREE='dfff72e82034986739d9f8641a820a0d76ea6dd1'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('rev-parse','HEAD^{tree}').decode().strip()==TREE
assert git('write-tree').decode().strip()==TREE
records=[];gitlinks=[]
for entry in git('ls-tree','-rz',HEAD).split(b'\0'):
    if not entry:continue
    left,name=entry.split(b'\t');mode,kind,oid=left.decode().split();name=name.decode()
    if mode=='160000':gitlinks.append({'path':name,'oid':oid});continue
    path=ROOT/name;data=path.read_bytes();original=git('cat-file','blob',oid)
    actual='100755' if path.stat().st_mode&stat.S_IXUSR else '100644'
    assert data==original and mode==actual,name
    assert b'SPDX-License-Identifier: Apache-2.0' in data,name
    records.append({'path':name,'blob':oid,'mode':mode,'sha256':hashlib.sha256(data).hexdigest()})
assert not gitlinks
status=git('status','--porcelain=v1','--untracked-files=all').decode();assert not status,status
index=git('ls-files','--stage').decode()
for row in index.splitlines():assert row.split()[2]=='0'
result={'head':HEAD,'tree':TREE,'index_tree':TREE,'status':status,'tracked_blobs':len(records),'gitlinks':gitlinks,'required_gitlinks':[],'files':records}
(RECEIPTS/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')
(RECEIPTS/'history.txt').write_bytes(git('log','--format=%H %P%n%s%n%b','1401654530ce7d9275de9b901e67df47e5bbc536..HEAD'))
(RECEIPTS/'changed-files.txt').write_bytes(git('diff','--name-status','1401654530ce7d9275de9b901e67df47e5bbc536..HEAD'))
anchors=[]
for page in [ROOT/'README.md',*sorted((ROOT/'doc').rglob('*.md'))]:
    for match in re.finditer(r'\]\(([^)]+)#L(\d+)(?:-L(\d+))?\)',page.read_text()):
        target,line,last=match.groups();path=(page.parent/target).resolve()
        if not path.is_file():continue
        lines=path.read_text().splitlines();n=int(line)
        anchors.append(f'{page.relative_to(ROOT)} -> {path.relative_to(ROOT)}:{line}: {lines[n-1]}')
(RECEIPTS/'source-anchors.txt').write_text('\n'.join(anchors)+'\n')
print('Integrity PASS:',len(records),'tracked blobs, exact modes/index/tree, zero gitlinks; anchors',len(anchors))
