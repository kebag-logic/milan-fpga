"""Copy current source bytes into a disposable test fixture for in-place defect controls."""
import hashlib,json,shutil,subprocess
from pathlib import Path
root=Path.cwd(); out=Path('$VALIDATION_STORAGE/artysplit-a829/r4/rtl-fixture')
assert not out.exists(),out
tracked=subprocess.check_output(['git','ls-files','-z','--recurse-submodules']).split(b'\0')
added=subprocess.check_output(['git','ls-files','-z','--others','--exclude-standard']).split(b'\0')
records=[]
for raw in sorted(set(tracked+added)-{b''}):
 name=raw.decode(); source=root/name; target=out/name
 if not source.is_file():continue
 target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(source,target)
 assert target.read_bytes()==source.read_bytes()
 records.append(dict(path=name,sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
# The legacy timestamp campaign requires tracked, clean inputs and restores
# through Git. This private fixture has no remote and no shared repository metadata.
for command in (['git','init','-q'],['git','add','-A'],
                ['git','-c','user.name=Test Fixture','-c','user.email=test@example.invalid',
                 'commit','-qm','Snapshot Arty RTL test inputs']):
 subprocess.run(command,cwd=out,check=True)
receipt=dict(kind='disposable test fixture, not an implementation lane',
             source_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
             files=records)
(out.parent/'rtl-fixture-inputs.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Prepared',len(records),'byte-checked source files')
