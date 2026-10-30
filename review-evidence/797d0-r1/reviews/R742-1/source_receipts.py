#!/usr/bin/env python3
"""Capture exact-head, numbered evidence for independently checked claims."""
from pathlib import Path
import json
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sections = {
 'shipping-placement': [('sw/litex/milan_soc.py',2616,2626), ('sw/litex/milan_soc.py',3838,3841)],
 'media-selection': [('hdl/milan/milan_datapath.sv',1750,1770), ('hdl/milan/milan_datapath.sv',790,820)],
 'steerable-grid': [('hdl/ieee1722/crf/KL_media_nco.sv',108,157)],
 'phy-publication': [('sw/firmware/milan_baremetal/milan_baremetal.c',1086,1100), ('sw/firmware/milan_baremetal/milan_baremetal.c',1655,1672), ('sw/litex/milan_soc.py',1893,1907)],
 'boot-policy': [('sw/litex/boot_policy.py',40,64), ('sw/firmware/milan_baremetal/milan_baremetal.c',1802,1818)],
 'ethernet-guard': [('hdl/common/csr/milan_csr.sv',883,897), ('hdl/common/csr/milan_csr.sv',1574,1580), ('hdl/common/csr/milan_csr.sv',1681,1689), ('hdl/common/csr/milan_csr.sv',1725,1732), ('hdl/common/csr/milan_csr.sv',2386,2390), ('sw/litex/milan_soc.py',2061,2087), ('sw/litex/patches/0002-liteeth-gmii-tx-clk-invert.patch',26,43)],
 'inactive-shaping': [('hdl/common/csr/milan_csr.sv',1993,2003), ('docs/reference/EGRESS_QUEUE_MAP.md',3,12), ('docs/reference/FR_NFR.md',169,176), ('docs/reference/MILAN_COMPLIANCE_MATRIX.md',260,268)],
 'missed-persistence': [('docs/integration/QSPI_FLASHBOOT.md',53,64), ('hdl/milan/KL_pp_shadow.sv',1123,1148), ('sw/firmware/milan_baremetal/milan_baremetal.c',1393,1431), ('sw/firmware/milan_baremetal/milan_baremetal.c',1665,1674), ('sw/firmware/milan_baremetal/milan_baremetal.c',1883,1893)],
 'missed-test-frameworks': [('docs/guides/VERIFICATION_DEVELOPER.md',22,48), ('scripts/run_litex_sims.sh',95,108), ('scripts/run_litex_sims.sh',150,178), ('sw/firmware/gtest/README.md',4,14), ('sw/firmware/gtest/fw_gtest_main.cpp',24,28)],
 'missed-queue-roles': [('docs/reference/EGRESS_QUEUE_MAP.md',31,40), ('hdl/common/ethernet_packet_pkg.sv',217,223), ('hdl/common/csr/milan_csr.sv',2005,2009)],
 'three-corrections': [('docs/README.md',70,74), ('docs/guides/VERIFICATION_DEVELOPER.md',123,130), ('docs/reference/REGISTER_MAP.md',423,429), ('docs/design/MEDIA_CLOCK_FOLLOWING.md',1,28), ('sw/litex/test_gmii_rx_capture.py',1,20), ('docs/findings/599_394_E1_LINK_CYCLES.md',1,35)],
}
lines = ['Exact head: ' + subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()]
for label, items in sections.items():
    lines.append('\n== ' + label + ' ==')
    for path, first, last in items:
        content = (root / path).read_text().splitlines()
        lines.extend(f'{path}:{i}: {content[i-1]}' for i in range(first,last+1))
data = json.loads((root / 'scripts/docs_inventory.json').read_text())
lines.append('\n== all finding quotations located independently ==')
for f in data['findings']:
    matches = [i for i,s in enumerate((root / f['page']).read_text().splitlines(),1) if f['quote'] in s]
    assert matches, f['id']
    lines.append(f"{f['id']}: {f['page']}:{','.join(map(str,matches))}: {f['quote']}")
paths = subprocess.check_output(['git','ls-files','-z'],cwd=root,text=True).split('\0')
lines.append('\nDeleted module check: ' + str([p for p in paths if Path(p).name == 'KL_lwsrp_ctx.sv']))
lines.append('Changed paths:\n' + subprocess.check_output(['git','diff','--name-only','1e80128f..HEAD'],cwd=root,text=True))
(out / 'source-excerpts.txt').write_text('\n'.join(lines)+'\n')
print('Saved numbered source receipts and located all 23 finding quotations.')
