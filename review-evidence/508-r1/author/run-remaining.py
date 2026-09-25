from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
for first,last in [(1,12),(13,23),(24,30),(31,36)]:
 rc=subprocess.run(['python3',str(p/'run-dp-chunks.py'),str(first),str(last)]).returncode
 if rc:sys.exit(rc)
for name,args in [
 ('milan-dp-render',['make','-C','tb/verilator/milan_dp_render']),
 ('nvm-cosim',['make','-C','tb/verilator/nvm_cosim']),
 ('gsi-mutants',['make','-C','tb/verilator/milan_dp','gsi-mutants']),
 ('behave',['--cwd','tests','behave','--no-capture','-f','plain']),
 *[(f'yosys-{i}',['syn/yosys/run.sh','--shard',f'{i}/4','--results',str(p/'yosys-results')]) for i in range(4)],
]:
 rc=subprocess.run(['python3',str(p/'run_gate.py'),name,*args]).returncode
 if rc:sys.exit(rc)
print('ALL REMAINING BANKS rc 0',flush=True)
