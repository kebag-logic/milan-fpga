#!/usr/bin/env python3
"""Use only in the disposable offline namespace."""
import importlib.util,sys
from pathlib import Path
source=Path(sys.argv[1]);spec=importlib.util.spec_from_file_location('closing_control',source)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
f=m.selftest_fixture();r=m.ValidatedRun(f.pr,f.repository,f.base);t=m.SelftestTally()
m.selftest_act_signal_window(t,f,r)
print(f'failures={t.failures}')
sys.exit(bool(t.failures))
