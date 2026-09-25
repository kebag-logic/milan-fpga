from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
for mode in ['sdk','absent']:
 clean=["python3","-c","from pathlib import Path; import subprocess,shutil; p=Path('sw/builder/out'); assert not subprocess.check_output(['git','ls-files','--',str(p)]); shutil.rmtree(p,ignore_errors=True); print('Removed generated builder output; no tracked files affected')"]
 rc=subprocess.run(['python3',str(p/'run_gate.py'),'clean-builder-'+mode,*clean]).returncode
 if rc:sys.exit(rc)
 script='full-builder-sdk-candidate.py' if mode=='sdk' else 'full-builder-absent.py'
 rc=subprocess.run(['python3',str(p/'run_gate.py'),'builder-'+mode+'-candidate','python3',str(p/script)]).returncode
 if rc:sys.exit(rc)
print('BOTH FULL BUILDER MODES rc 0',flush=True)
