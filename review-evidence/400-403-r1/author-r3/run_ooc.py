from pathlib import Path
import subprocess, sys
out=Path(__file__).resolve().parent
for version in ('base','head'):
 cmd=['env',f'OOC_TMP=$VALIDATION_STORAGE/400-403-a316-ooc/{version}-results',
      'bash',str(out/f'ooc-{version}.sh'),'milan_csr','KL_pp_shadow','milan_datapath']
 rc=subprocess.run([sys.executable,str(out/'run_gate.py'),f'ooc-{version}-r2',*cmd],timeout=43200).returncode
 if rc:sys.exit(rc)
