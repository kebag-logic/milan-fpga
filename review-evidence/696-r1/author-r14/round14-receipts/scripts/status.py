from pathlib import Path
import shutil,time
w=Path(__file__).resolve().parent
print(time.strftime('%H:%M:%S'))
for name in ('resource-bank','record-measurements','validation-bank','validation-resume'):
 p=w/(name+'.rc');print(name,p.read_text().strip() if p.exists() else 'running')
 if not p.exists():
  log=w/(name+'.log')
  if log.exists():print('\n'.join(log.read_text(errors='replace').splitlines()[-4:]))
if not (w/'resource-bank.rc').exists():
 p=w/'ax8x8-ooc.log'
 if p.exists():print('synthesis:','\n'.join(p.read_text(errors='replace').splitlines()[-3:]))
else:
 for p in sorted((w/'validation').glob('*.log')):
  if not p.with_suffix('.rc').exists():print(p.name, ' '.join(p.read_text(errors='replace').splitlines()[-2:])[:350])
c=Path('/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-696-a570l.service')
print('memory_GB',round(int((c/'memory.current').read_text())/1e9,2),'free_GiB',round(shutil.disk_usage(w).free/1024**3,2))
