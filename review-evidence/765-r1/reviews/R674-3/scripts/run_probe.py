#!/usr/bin/env python3
"""Run the published probe with bounded compilation, then assert its observations."""
import hashlib,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
repo=Path(sys.argv[1]).resolve()
compiler=Path(sys.argv[2]).resolve()
version=subprocess.check_output([str(compiler),'--version'],text=True).strip()
assert 'Verilator 5.050 ' in version,version
print(version,flush=True)
original=ROOT/'scripts/probe_flat_cpf256.sh'
published=ROOT/'published/reviews/R673-2/scripts/probe_flat_cpf256.sh'
assert original.read_bytes()==published.read_bytes()
print('Published probe SHA256:',hashlib.sha256(original.read_bytes()).hexdigest(),flush=True)
wrapper=ROOT/'scratch/compiler_limit.py'
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i] in ('-j','--build-jobs'): a[i+1]='16'\nos.execv("+repr(str(compiler))+",["+repr(str(compiler))+"]+a)\n")
wrapper.chmod(0o755)
log=ROOT/'receipts/probe-flat.log'
with log.open('w') as f:
    rc=subprocess.run(['sh',str(original),str(repo),str(ROOT/'scratch/flat-probe'),str(wrapper)],stdout=f,stderr=subprocess.STDOUT,timeout=480).returncode
(ROOT/'receipts/probe-flat.rc').write_text(str(rc)+'\n')
text=log.read_text();print(text)
assert rc==0,rc
assert 'PROBE cpf=256: frames_rx=3 unsupported=2' in text
assert 'PROBE cpf=257: frames_rx=4 unsupported=2' in text
full=subprocess.run([str(ROOT/'scratch/flat-probe/tb/verilator/avtp_rxmon/obj_dir/Vavtp_rxmon_wrap_sim')],capture_output=True,text=True,timeout=60)
(ROOT/'receipts/probe-full.log').write_text(full.stdout+full.stderr)
(ROOT/'receipts/probe-full.rc').write_text(str(full.returncode)+'\n')
assert full.returncode==0
assert '97 checks, 0 failures' in full.stdout
assert 'FAIL' not in text
print('PASS: 256 rejected and counted; 257 accepted; existing 97 checks pass.')
