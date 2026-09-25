"""Require the standalone CSR bench to reject a missing RENDER_STAT decode."""

from pathlib import Path
import subprocess
import tempfile

REPO = Path('$LANES/443-render-csr')
OUT = Path(__file__).resolve().parent
source = (REPO / 'hdl/common/csr/milan_csr.sv').read_text()
start = source.index('      A_RENDER_STAT: begin\n')
end = source.index('      //! LTAP_CTRL:', start)
with tempfile.TemporaryDirectory(prefix='443-a301-csr-probe-', dir='/tmp') as temp:
    work = Path(temp)
    rtl = work / 'milan_csr.sv'
    rtl.write_text(source[:start] + source[end:])
    command = [
        'rtk', 'proxy', 'verilator',
        '+incdir+' + str(REPO / 'configs/generated/endstation_arty_current'),
        '+incdir+' + str(REPO / 'hdl/common/csr'),
        '--cc', '--exe', '--build', '-j', '8',
        '-Wall', '-Wno-fatal', '-Wno-DECLFILENAME', '-Wno-UNUSEDSIGNAL',
        '-Wno-UNUSEDPARAM', '-CFLAGS', '-std=c++17 -O2 -Wall -Wextra',
        '--Mdir', str(work / 'obj'), '--top-module', 'milan_csr',
        str(rtl), str(REPO / 'tb/verilator/csr/sim_main.cpp'), '-o', 'Vcsr_probe',
    ]
    with (OUT / 'csr-nodecode-build.log').open('w') as log:
        subprocess.run(command, cwd=REPO / 'tb/verilator/csr', stdout=log,
                       stderr=subprocess.STDOUT, check=True, timeout=3600)
    with (OUT / 'csr-nodecode-run.log').open('w') as log:
        result = subprocess.run(['rtk', 'proxy', str(work / 'obj/Vcsr_probe')],
                                cwd=REPO / 'tb/verilator/csr', stdout=log,
                                stderr=subprocess.STDOUT, timeout=600)
    log = (OUT / 'csr-nodecode-run.log').read_text()
    named = 'RENDER_STAT selected listener preserves all fields'
    hits = [line for line in log.splitlines() if '[FAIL]' in line and named in line]
    assert result.returncode == 1 and hits, (result.returncode, hits)
    print('Missing-decode mutant rejected, rc=1:')
    for line in hits:
        print(line.replace('[FAIL]', '[EXPECTED MUTANT FAILURE]'))
print('CSR decode probe passed; disposable sources and build deleted.')
