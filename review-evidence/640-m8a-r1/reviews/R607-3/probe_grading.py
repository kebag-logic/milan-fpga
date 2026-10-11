#!/usr/bin/env python3
"""Plant an environmental failure in a disposable tree and prove it earns no mutation kills."""
import argparse,os,pathlib,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('repo',type=pathlib.Path);a=ap.parse_args()
p=pathlib.Path(__file__).resolve().parent;s=p/'scratch';assert a.repo.resolve().is_relative_to(s.resolve())
source=a.repo/'sw/litex/test_ctrl_memory.py';original=source.read_bytes();target=source.with_name('r607_grading_control.py');assert not target.exists()
old=b'original_includes(self, with_bios=False)';new=b'original_includes(self, with_bios=with_bios)';assert original.count(old)==1
try:
 target.write_bytes(original.replace(old,new))
 result=subprocess.run([sys.executable,str(target)],cwd=a.repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False,timeout=540)
 (s/'raw/grading-control-child.log').write_text(result.stdout)
 assert result.returncode==1,result.returncode
 lines=result.stdout.splitlines();notgraded=[line for line in lines if '[FAIL]' in line and 'is not graded: the soc arm fails unmutated' in line]
 assert len(notgraded)==6,notgraded
 assert any('the split build exports (rc 1, ImportError:' in line for line in lines)
 assert not any('caught by the soc arm' in line for line in lines)
 print('PASS: missing include hook causes baseline SoC ImportError, exit 1; all six SoC mutants NOT GRADED; no environmental failure credited as kill')
 for line in notgraded: print(line)
finally:
 target.unlink()
 assert source.read_bytes()==original
print('PASS: disposable fault copy removed; tracked source bytes unchanged')
