from pathlib import Path
import subprocess
base=Path('/data-2/milan/tmp/opt-a837/scale/cost-controls')
source=Path('/data-2/milan/lanes/opt-hart2/tb/verilator/ctrl_service_budget/harts_cost.hpp').read_text()
for name,header in [('plain',source),('return-removed',source.replace('if (s.active && pc == s.ret)', 'if (false)'))]:
 (base/'harts_cost.hpp').write_text(header)
 p=subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-Werror',str(base/'test.cpp'),'-o',str(base/name)],capture_output=True,text=True)
 print(name,'compile',p.returncode,p.stdout,p.stderr)
 if p.returncode:raise SystemExit(1)
 p=subprocess.run([str(base/name)],capture_output=True,text=True)
 print(name,'run',p.returncode,p.stdout.strip())
 if p.returncode != (0 if name=='plain' else 1):raise SystemExit(1)
(base/'harts_cost.hpp').write_text(source)
print('2 cases, 0 failures; missing return observation caught')
