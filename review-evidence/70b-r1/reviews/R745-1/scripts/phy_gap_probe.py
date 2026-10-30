#!/usr/bin/env python3
"""Probe: does the PHY boot-path arm catch a disabled-path poll that stops partway
through the console idle (a >250 ms gap with >= 4 publications)? Usage: REPO WORKDIR"""
import re, sys
from pathlib import Path
repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / 'sw/firmware/nvm_hosttest'))
import test_nvm_firmware as nvm  # noqa: E402
import test_phy_firmware as phy  # noqa: E402
src = (repo / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_text()
cfg = repo / 'configs/endstation_ax7101_1x1_tdm8.yaml'
# 1. the disabled path's boot time, from a clean run
d = work / 'clean'; phy.phy_csr(d)
b = nvm.make_bench(cfg, d, src.replace(*phy.SHAPE_OFF), ('-DNVM_HOST_PHY',))
raw, _, _ = nvm.run(b, '--boot', '--uart', 'milan_status', '--idle-ms', str(phy.IDLE_MS))
boot_ms = int(re.search(r'HOST phy at=boot .* now_ms=(\d+)', raw).group(1))
stop_ms = boot_ms + 600
print('disabled path boot now_ms', boot_ms, '-> plant stops the poll at', stop_ms, 'ms (400 ms of the 1000 ms idle unpolled)')
old = '\t\tif (phy_live)\n\t\t\tphy_link_tick(gettime_ns());\n'
new = f'\t\tif (phy_live && gettime_ns() < {stop_ms}000000ull)\n\t\t\tphy_link_tick(gettime_ns());\n'
assert src.count(old) == 1
got = phy.boot_path_findings(cfg, work / 'planted', src.replace(old, new))
print('findings on the planted copy:', got if got else 'NONE (the mid-idle stop escapes the arm)')
