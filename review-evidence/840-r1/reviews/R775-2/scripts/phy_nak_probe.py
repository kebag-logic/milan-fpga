#!/usr/bin/env python3
"""Probe the unmutated firmware with a NAK on registers 4 and 0 during the PHY init.

Usage: phy_nak_probe.py <repo>. A temporary copy of phy_host.c gains a NAK of
each register in turn at the point the shipped test NAKs register 9; each run
must write nothing in that poll and then advertise on the retry.
"""
import pathlib
import subprocess
import sys
import tempfile

repo = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / 'sw/firmware/nvm_hosttest'))
sys.dont_write_bytecode = True
import test_nvm_firmware as nvm  # noqa: E402
import test_phy_firmware as phy  # noqa: E402

source = nvm.FIRMWARE.read_text()
host = (repo / 'sw/firmware/nvm_hosttest/phy_host.c').read_text()
ANCHOR = 'nak_register = 9;\n\tnow += 125000000u;\n\texpect_poll(now, 0);'
assert host.count(ANCHOR) == 1
with tempfile.TemporaryDirectory(prefix='r775-nak-') as tmp:
    work = pathlib.Path(tmp)
    nvm.make_bench(repo / 'configs/endstation_ax7101_1x1_tdm8.yaml', work, source)
    phy.phy_csr(work)
    (work / 'phy_peer.h').write_text((repo / 'sw/firmware/nvm_hosttest/phy_peer.h').read_text())
    (work / 'milan_baremetal.c').write_text(nvm.FENCE_RE.sub('(void)0;', source))
    for reg in (4, 0):
        (work / 'phy_host.c').write_text(host.replace(ANCHOR, f'nak_register = {reg};\n\tnow += 125000000u;\n\tphy_link_tick(now);\n\tprintf("NAK_POLL status=%u writes=%u\\n", status_word, writes);'))
        subprocess.run(['gcc', '-std=gnu11', '-O1', '-Wno-format', '-ffunction-sections', '-fdata-sections', '-Wl,--gc-sections', f'-I{work}', f'-I{nvm.STUBS}',
                        str(work / 'phy_host.c'), '-o', str(work / 'phy')], check=True, timeout=120,
                       capture_output=True)
        run = subprocess.run([str(work / 'phy')], capture_output=True, text=True, timeout=120)
        line = [l for l in run.stdout.splitlines() if l.startswith(('NAK_POLL', 'PHY_ADVERTISEMENT'))][:2]
        print(f'NAK reg {reg}: rc {run.returncode} {line} {run.stderr[-120:].strip()}')
