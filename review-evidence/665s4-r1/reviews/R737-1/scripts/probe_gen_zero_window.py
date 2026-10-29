#!/usr/bin/env python3
"""Reviewer probe: gen_flash_port.py on an export whose spiflash window is 0 bytes.
Usage: probe_gen_zero_window.py CLONE WORKDIR. Renders the generator's own passing
export with the window's size set to 0, runs main(), and prints the exit status
(or the exception) and whether anything was written."""
import sys
import traceback
from pathlib import Path
clone, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / 'sw/firmware/ctrl_nvm/plat'))
import gen_flash_port as g  # noqa: E402
spec = g.planted(g._set(('regions', 'spiflash'), [(0x0100_0000, 0)]))
csv_text, header = g.render(spec)
(work / 'csr.csv').write_text(csv_text)
(work / 'csr.h').write_text(header)
out = work / 'out'
try:
    rc = g.main(['--csr-csv', str(work / 'csr.csv'), '--csr-h', str(work / 'csr.h'), '--out', str(out)])
    print('main returned', rc)
except Exception:
    print('main raised:', traceback.format_exc().strip().splitlines()[-1])
print('written:', out.exists())
