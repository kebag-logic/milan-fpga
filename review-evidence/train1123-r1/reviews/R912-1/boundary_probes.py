#!/usr/bin/env python3
"""Exercise the two composition boundary corrections without rebuilding the banks."""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_configs as configs
import ctrl_boundary as boundary
from ctrl_capture import Capture
from ctrl_build import Refusal
path=root/'sw/litex/mac_link_status.py'
text=path.read_text()
assert configs.program(path,text)  # The standalone entry prints reset values; it compiles nothing.
original=configs.builder_texts
configs.builder_texts=lambda planted=None:{path:text}
try:
    configs.held(Capture((),(),(),()),configs.Scope(),known=())
    reason=configs.OUTSIDE.pop('sw/litex/mac_link_status.py')
    try:
        try:
            configs.held(Capture((),(),(),()),configs.Scope(),known=())
        except Refusal as error:
            assert 'sw/litex/mac_link_status.py' in str(error)
            print('PASS: removing the no-compile module classification is refused:',error)
        else:
            raise AssertionError('missing classification escaped')
    finally:
        configs.OUTSIDE['sw/litex/mac_link_status.py']=reason
finally:
    configs.builder_texts=original
page=boundary.README.read_text()
counts=boundary.population(192)
assert boundary.figures(page,counts)==[]
old=page.replace('192 pin controls','185 pin controls')
assert old!=page
reasons=boundary.figures(old,counts)
assert len(reasons)==1 and '185' in reasons[0] and '192' in reasons[0]
print('PASS: pre-fix pin population refused:',reasons[0])
assert boundary.figure_controls(page,counts)==(0,4)
print('PASS: four figure controls; population 192 supplied from the published executed gate, not re-executed here')
