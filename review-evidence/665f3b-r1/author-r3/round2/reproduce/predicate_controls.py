import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()/'sw/firmware/ctrl/test'))
import ctrl_mutants as m
import ctrl_reuse
work=Path(os.environ['WORK']) / 'predicate-controls'
ctrl_reuse.cut_reuse(work/'reuse')
selected=tuple(x for x in m.MUTANTS if x.name.startswith(('f3b-', 'pub-maap-', 'rv-maap-')))
m.sliced=lambda part:selected
raise SystemExit(m.campaign(work,work/'reuse',4))
