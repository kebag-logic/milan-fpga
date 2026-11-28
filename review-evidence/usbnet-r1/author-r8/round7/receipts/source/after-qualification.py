import subprocess,sys,time
from pathlib import Path
p=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts');q=Path('$VALIDATION_STORAGE/usbnet-a855/round7/census/qualification.json')
while not q.exists():time.sleep(2)
for script in ('tables.py','archive-census.py'):
 print('START',script,flush=True)
 subprocess.run([sys.executable,str(p/'source'/script)],check=True)
 print('DONE',script,flush=True)
