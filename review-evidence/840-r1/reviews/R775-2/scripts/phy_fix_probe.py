#!/usr/bin/env python3
"""Show that a small harness change grades the two open findings.

Usage: phy_fix_probe.py <repo>. In a temporary copy of phy_host.c only, the
auto-negotiation-disabled arm starts its kept fields in a mixed pattern, and
NAK arms for registers 4 and 0 precede the shipped advertisement check. The
committed firmware must pass; each escaped mutant must then fail by name.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

repo = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / 'sw/firmware/nvm_hosttest'))
sys.dont_write_bytecode = True
import test_nvm_firmware as nvm  # noqa: E402
import test_phy_firmware as phy  # noqa: E402

host = (repo / 'sw/firmware/nvm_hosttest/phy_host.c').read_text()
ARM = ('\t\tregisters[0] = 0x2100;\n\t\tregisters[1] = 0x0124;\n\t\tregisters[4] = 0x4fe1;\n'
       '\t\tregisters[5] = 0x01e1;\n\t\tregisters[9] = 0xfdff;\n')
assert host.count(ARM) == 1
host = host.replace(ARM, ARM.replace('0x4fe1', '0x47e1').replace('0xfdff', '0xedff'))
NAK = ('\tnak_register = 32;\n\tnow += 125000000u;\n\t{\n\t\tunsigned int before = publishes;\n\n'
       '\t\tphy_link_tick(now);\n\t\texpect_gigabit_only_advertisement(0, 1);')
assert host.count(NAK) == 1
extra = ''.join(f'\tnak_register = {reg};\n\tnow += 125000000u;\n\tphy_link_tick(now);\n\t{{\n'
                f'\t\tconst int no_write_before_register_{reg}_read = writes == 0u;\n\n'
                f'\t\tassert(no_write_before_register_{reg}_read);\n\t}}\n' for reg in (4, 0))
host = host.replace(NAK, extra + NAK)
COND = '\tif (advertisement < 0 || gigabit < 0 || control < 0)\n\t\treturn 0;\n'
WRITE4 = 'phy_mdio_write(4, (unsigned int)advertisement &\n\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));'
WRITE9 = 'PHY_GBCR_MASTER_SLAVE) |\n\t\t       PHY_GBCR_1000_FULL);'
MUTANTS = {
    'as committed': None,
    'nak-reg4-not-checked': (COND, '\tif (gigabit < 0 || control < 0)\n\t\treturn 0;\n'),
    'nak-reg0-not-checked': (COND, '\tif (advertisement < 0 || gigabit < 0)\n\t\treturn 0;\n'),
    'force-pause-on': (WRITE4, 'phy_mdio_write(4, 0x0c00u | ((unsigned int)advertisement &\n'
                               '\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED)));'),
    'force-manual-master': (WRITE9, 'PHY_GBCR_MASTER_SLAVE) | 0x1c00u |\n\t\t       PHY_GBCR_1000_FULL);'),
    'force-manual-config-only': (WRITE9, 'PHY_GBCR_MASTER_SLAVE) | 0x1000u |\n\t\t       PHY_GBCR_1000_FULL);'),
}
source = nvm.FIRMWARE.read_text()
with tempfile.TemporaryDirectory(prefix='r775-fix-') as tmp:
    work = pathlib.Path(tmp)
    nvm.make_bench(repo / 'configs/endstation_ax7101_1x1_tdm8.yaml', work, source)
    phy.phy_csr(work)
    (work / 'phy_peer.h').write_text((repo / 'sw/firmware/nvm_hosttest/phy_peer.h').read_text())
    (work / 'phy_host.c').write_text(host)
    command = ['gcc', '-std=gnu11', '-O1', '-Wall', '-Wextra', '-Werror', '-Wno-format', '-ffunction-sections',
               '-fdata-sections', '-Wl,--gc-sections', f'-I{work}', f'-I{nvm.STUBS}',
               str(work / 'phy_host.c'), '-o', str(work / 'phy')]
    for name, plant in MUTANTS.items():
        text = nvm.FENCE_RE.sub('(void)0;', source)
        if plant:
            assert text.count(plant[0]) == 1, name
            text = text.replace(*plant)
        (work / 'milan_baremetal.c').write_text(text)
        subprocess.run(command, check=True, capture_output=True, timeout=120)
        run = subprocess.run([str(work / 'phy')], capture_output=True, text=True, timeout=120)
        hit = re.search(r"Assertion `(.+?)' failed", run.stderr)
        print(f"{name}: rc {run.returncode} "
              f"{hit[1] if hit else 'PHY_OK' if 'PHY_OK' in run.stdout else run.stderr[-100:]}")
