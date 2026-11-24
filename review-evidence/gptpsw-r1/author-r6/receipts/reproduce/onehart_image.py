from pathlib import Path
import hashlib, json, os, subprocess, sys
root = Path(os.environ['A837_SOURCE'])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import build
out = Path(sys.argv[1]); shape = sys.argv[2]
harts = int(sys.argv[3]) if len(sys.argv) > 3 else 1
elf = build.firmware(out, shape, 2, extra=build.ImageArgs(harts=harts))
record = dict(elf=str(elf), sha256=hashlib.sha256(elf.read_bytes()).hexdigest(), bytes=elf.stat().st_size,
              head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),
              shape=shape, harts=harts, interfaces=2)
(out/'identity.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
