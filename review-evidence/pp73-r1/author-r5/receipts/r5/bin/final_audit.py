"""Audit commit, source exports, completed job statuses and scratch-parent pin."""
from pathlib import Path
import hashlib
import json
import subprocess
r=Path('$VALIDATION_STORAGE/pp73-a595/r5');root=Path('$LANES/pp73-command-model')
parent=r.parent/'parent';sub=parent/'protocol-processor'
def git(cwd,*args):
    if cwd==sub:
        top=subprocess.check_output(['git','-C',str(sub),'rev-parse','--show-toplevel'],text=True).strip()
        assert top==str(sub),top
    return subprocess.check_output(['git','-C',str(cwd),*args])
head=git(root,'rev-parse','HEAD').decode().strip()
assert head=='4bee75b2e647507a71ece50359fceb135c334757'
assert git(root,'rev-parse','--abbrev-ref','HEAD').decode().strip()=='pp73-command-model'
assert git(root,'remote','get-url','origin').decode().strip()=='https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git'
assert git(root,'show','-s','--format=%P',head).decode().strip()=='4029dc5de2a0a540d6a015c747319fbee7abba2e 6d536868ee2a4762ab307d5ed51ff09c01130942'
message=git(root,'show','-s','--format=%B',head).decode().strip();assert len(message.splitlines())==1
status=git(root,'status','--short','--ignored').decode();assert not status,status
(r/'worktree-status.txt').write_text('Processor tracked, untracked and ignored status: clean\n')
paths=git(root,'ls-tree','-r','--name-only',head).decode().splitlines()
for path in paths:
    assert (r/'head'/path).read_bytes()==git(root,'show',head+':'+path),path
assert git(parent,'rev-parse','HEAD').decode().strip()=='e8454e2751d05b02ee8e5a571857589ab358ab86'
assert git(parent,'rev-parse',':protocol-processor').decode().strip()==head
assert git(sub,'rev-parse','HEAD').decode().strip()==head
ss=git(sub,'status','--short','--ignored').decode();assert not ss,ss
ps=git(parent,'status','--short').decode();assert ps=='M  protocol-processor\n',ps
(r/'submodule-final-status.txt').write_text('Parent e8454e27; index gitlink and clean detached submodule at '+head+'\n'+ps)
expected={'base-check-setup-attempt':'2'}
codes={p.stem:p.read_text().strip() for p in (r/'logs').glob('*.rc')}
assert codes['final-comparisons']=='0'
assert all(value==expected.get(name,'0') for name,value in codes.items()),codes
processes=[]
for p in (r/'logs').glob('*.pid'):
    pid=int(p.read_text());proc=Path('/proc')/str(pid)/'stat'
    state=proc.read_text().split(') ',1)[1].split()[0] if proc.exists() else 'exited'
    assert state in ['Z','exited'],(p.stem,pid,state)
    processes.append({'job':p.stem,'pid':pid,'state':state})
(r/'process-exit.txt').write_text('Every supervised job has exited; no background job remains.\n')
c=Path('/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-pp73-a595f.service')
events=dict(line.split() for line in (c/'memory.events').read_text().splitlines())
assert events['oom']==events['oom_kill']=='0',events
(r/'memory-final.txt').write_text('peak bytes: '+(c/'memory.peak').read_text()+(c/'memory.events').read_text())
result={'head':head,'parents':git(root,'show','-s','--format=%P',head).decode().strip().split(),'one_line_subject':message,'clean_processor':True,'exported_files_match_commit':len(paths),'parent_pin_matches':True,'job_exit_codes':codes,'supervised_processes':processes,'memory_events':events}
(r/'final-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('Final audit passes: commit, source export, clean trees, parent pin, all required statuses, exited jobs and no OOM events')
