from pathlib import Path
import hashlib
import json
import subprocess
from run_gate import OUT, ROOT, run

MUTANTS = [
    ('41', 'hdl/milan/KL_pp_shadow.sv',
     '      .SRP_DOM_DEF_VID_P (SRP_DOM_DEF_VID_P),\n', '', 'pp_shadow'),
    ('43', 'hdl/milan/milan_datapath.sv',
     '      .SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C),\n', '', 'pp_shadow'),
    ('35', 'hdl/common/csr/milan_csr.sv',
     'lwsrp_ctrl <= LWSRP_CTRL_RST_C;',
     "lwsrp_ctrl <= LWSRP_CTRL_RST_C & ~32'h3;", 'csr'),
]

for receipt, rel, old, new, suite in MUTANTS:
    path = ROOT / rel
    original = path.read_bytes()
    text = original.decode()
    assert text.count(old) == 1
    try:
        path.write_text(text.replace(old, new))
        rc = run('final-mutant-' + receipt, ['make', '-C', 'tb/verilator/' + suite])
        log = (OUT / ('final-mutant-' + receipt + '.log')).read_text()
        assert rc != 0 and ('[FAIL]' in log or '[FAIL ' in log or '[FAIL]' in log.upper()), log[-2000:]
    finally:
        path.write_bytes(original)
    assert hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(original).digest()
    print('Receipt ' + receipt + ': DETECTED; original source restored', flush=True)

for suite in ('pp_shadow', 'csr'):
    assert run('final-restored-' + suite, ['make', '-C', 'tb/verilator/' + suite]) == 0
