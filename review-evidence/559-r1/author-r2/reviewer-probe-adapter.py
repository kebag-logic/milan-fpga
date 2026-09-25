import argparse, json, sys, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent/'harness'))
import soc, run
parser=argparse.ArgumentParser()
parser.add_argument('--captures',type=int,default=2)
parser.add_argument('--mutation',default='none')
parser.add_argument('--cpu-hz',type=int,default=50000000)
parser.add_argument('--shape',default='endstation_ax7101_8x8')
parser.add_argument('--build-dir',type=Path,required=True)
args=parser.parse_args()
original=soc.eb._derive_artifacts
def derive(*a,**kw):
 art=original(*a,**kw)
 art.cfg['constraints']['milan_clk_hz']=args.cpu_hz
 return art
soc.eb._derive_artifacts=derive
soc.build(args)
spec=json.loads((args.build_dir/'sources.json').read_text())
run._compile(args.build_dir,spec)
with (args.build_dir/'capture.log').open('w') as log:
 result=subprocess.run([str(args.build_dir/'native/Vsim')],cwd=args.build_dir/'gateware',stdout=log,stderr=subprocess.STDOUT)
(args.build_dir/'vsim.rc').write_text(str(result.returncode)+'\n')
run._grade(args.build_dir,spec,result.returncode)
