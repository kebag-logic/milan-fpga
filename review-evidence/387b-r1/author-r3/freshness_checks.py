import os, sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, '$LANES/387-media-rebase/tb/verilator/milan_dp')
import gmstep_mutants as g
run = g.subprocess.run

def old_call(argv, **kwargs):
    return run([arg for arg in argv if arg != '--no-print-directory'], **kwargs)

for name, leg in g.LEGS.items():
    exe = leg.clean_mdir/leg.exe_name
    assert g.is_fresh(leg,exe), name+' clean binary was not fresh'
    print(name, 'nested is_fresh: True')
    with patch.object(g.subprocess,'run',side_effect=old_call):
        assert not g.is_fresh(leg,exe), name+' old implementation control survived'
    print(name, 'old directory-output control: False, caught')
    with tempfile.TemporaryDirectory(prefix='a277-freshness-') as tmp:
        candidate = Path(tmp)/'binary'
        assert not g.is_fresh(leg,candidate)
        candidate.touch()
        os.utime(candidate,(0,0))
        assert not g.is_fresh(leg,candidate)
    print(name, 'missing and stale candidates refused')
