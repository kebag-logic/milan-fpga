#!/usr/bin/env python3
"""Probe the mover's 12-bit length boundary with the submitted independent byte oracle."""
import os
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
out=packet/'scratch/dma-length';out.mkdir(parents=True,exist_ok=True)
tb=root/'tb/verilator/mbx'
text=(tb/'dma_main.cpp').read_text()
text=text.replace('../../common/verilator_harness.hpp',str(root/'tb/common/verilator_harness.hpp'))
text=text.replace('constexpr std::uint32_t kMask = 511;', 'constexpr std::uint32_t kMask = 1023;')
start=text.index('    shapes(b, check);')
end=text.index('    std::printf("bursts',start)
text=text[:start]+'''    for (unsigned len : {4092u, 4093u, 4094u, 4095u}) {
        b.reset();
        const std::string tag = std::to_string(len);
        receive_case(b, check, kMemBase + 0x100, len, 0, tag.c_str());
        b.reset();
        transmit_case(b, check, kMemBase + 0x100, len, 0, tag.c_str());
    }
'''+text[end:]
src=out/'probe.cpp';src.write_text(text)
env=dict(os.environ,VERILATOR='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator',VBUILD_JOBS='2')
flags=subprocess.check_output(['make','-s','print-dma-vflags'],cwd=tb,env=env,text=True).splitlines()
with (packet/'dma-length-build.log').open('w') as log:
 rc=subprocess.run([*flags,'--Mdir',str(out/'obj'),str(root/'hdl/milan/mailbox/KL_mbx_pkg.sv'),
                    str(root/'hdl/milan/mailbox/KL_mbx_dma.sv'),str(src),'-o','probe'],env=env,stdout=log,stderr=subprocess.STDOUT).returncode
if rc:sys.exit(rc)
with (packet/'dma-length.log').open('w') as log:
 rc=subprocess.run([str(out/'obj/probe')],stdout=log,stderr=subprocess.STDOUT).returncode
(packet/'dma-length.rc').write_text(str(rc)+'\n')
print('dma length boundary probe rc',rc)
sys.exit(rc)
