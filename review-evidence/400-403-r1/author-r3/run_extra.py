from pathlib import Path
import subprocess, sys
out=Path(__file__).resolve().parent
steps=[('declarations',['python3','sw/builder/test_declarations.py']),
 ('docs-git',['python3','-B','scripts/docs_check.py']),
 ('docs-no-git',['env','GIT_DIR=/dev/null','python3','-B','scripts/docs_check.py']),
 ('behave',['bash','-c','cd tests && behave --no-capture -f plain']),
 ('diff-worktree',['git','diff','--check'])]
for label,cmd in steps:
 rc=subprocess.run([sys.executable,str(out/'run_gate.py'),label,*cmd],timeout=43200).returncode
 if rc:sys.exit(rc)
