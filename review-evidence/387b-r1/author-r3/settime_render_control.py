import os, sys, tempfile
from pathlib import Path
root = Path('$LANES/387-media-rebase')
sys.path.insert(0, str(root/'tb/verilator/milan_dp'))
import render_mutants as r
os.environ['VERILATOR_JOBS'] = '8'
anchor = "       media_rebase_p_w\n       | src_recentre_p_r;"
source = (root/'hdl/milan/milan_datapath.sv').read_text()
assert source.count(anchor) == 1
with tempfile.TemporaryDirectory(prefix='a277-settime-') as tmp:
    work = Path(tmp)
    mutant = work/'milan_datapath.sv'
    mutant.write_text(source.replace(anchor,"       eff_ptp_adjust_w\n       | src_recentre_p_r;"))
    exe = r.build('DP_SRC',mutant,work/'obj')
    assert exe is not None, 'mutant must build'
    rc, log = r.run_leg(exe, '--render-only')
    print(log)
    verdict = r.verdict(rc,log,'RENDER-SETTIME: the settime executes one render re-base')
    assert verdict == 'caught', verdict
    print('PASS: dropping only software settime from the render trigger fails the named check')
