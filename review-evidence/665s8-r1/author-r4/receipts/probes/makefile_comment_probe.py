"""An edit of milan_dp's Makefile that keeps it valid make (a comment line): reused() must still refuse it."""
import json, shutil, subprocess, sys
from pathlib import Path
root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_wire_timing'))
import wire_build as wb
out = scratch / 'makefile-probe'
shutil.rmtree(out, ignore_errors=True)
for rel in ('image/ctrl_app.elf', 'soc/gateware/rom.init', 'wire_config.hpp', 'split/' + wb.SPLIT_ARCHIVE, 'native/Vsim'):
    (out / rel).parent.mkdir(parents=True, exist_ok=True)
    (out / rel).write_text('stand-in\n')
spec = dict(elf=str(out / 'image/ctrl_app.elf'), sources=[str(root / 'hdl/milan/mailbox/KL_mbx_wb.sv')])
spec['inputs'] = wb.inputs(out, spec)
spec['executable_sha256'] = wb.digest(out / 'native/Vsim')
(out / 'build.json').write_text(json.dumps(spec))
path = root / 'tb/verilator/milan_dp/Makefile'
original = path.read_bytes()
try:
    path.write_bytes(original + b'\n# probe\n')
    try:
        wb.reused(out)
        print('tb/verilator/milan_dp/Makefile (a comment line): ACCEPTED (stale build reused)')
    except RuntimeError as why:
        print(f'tb/verilator/milan_dp/Makefile (a comment line): refused: {why}')
finally:
    path.write_bytes(original)
print('tracked tree restored:', subprocess.run(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=no'],
                                                capture_output=True, text=True).stdout.strip() == '')
