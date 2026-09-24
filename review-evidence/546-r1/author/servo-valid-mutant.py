import shlex
import subprocess
import tempfile
from pathlib import Path

root = Path('$LANES/546-crf-talker-step')
out = Path(__file__).resolve().parent
suite = root / 'tb/verilator/mmcm_servo'
rtl = root / 'hdl/ieee1722/crf/KL_mmcm_drp_servo.sv'
source = rtl.read_text()
anchor = '&& crf_rate_valid_i;'
assert source.count(anchor) == 1
with tempfile.TemporaryDirectory(prefix='546-servo-mutant-') as tmp:
 work = Path(tmp)
 mutant = work / 'KL_mmcm_drp_servo.sv'
 mutant.write_text(source.replace(anchor, "&& 1'b1;"))
 recipe = subprocess.check_output(['make', '-n', 'run',
  'VERILATOR=$VALIDATION_TOOLS/verilator-v5.050/bin/verilator'], cwd=suite, text=True)
 first = recipe.replace('\\\n', ' ').splitlines()[0]
 command = shlex.split(first)
 command = [str(mutant) if item.endswith('/KL_mmcm_drp_servo.sv') else item for item in command]
 command += ['-Mdir', str(work / 'obj')]
 with (out / 'servo-valid-mutant-build.log').open('w') as log:
  build = subprocess.run(command, cwd=suite, stdout=log, stderr=subprocess.STDOUT, timeout=600)
 assert build.returncode == 0, build.returncode
 with (out / 'servo-valid-mutant.log').open('w') as log:
  run = subprocess.run([str(work / 'obj/Vservo_sim')], cwd=suite,
   stdout=log, stderr=subprocess.STDOUT, timeout=600)
 text = (out / 'servo-valid-mutant.log').read_text()
 assert run.returncode == 1 and '[FAIL] [U13] invalid remote sample holds trim' in text
 print('Servo validity mutant caught by U13, rc=1')
