#!/bin/bash
# The portable self-tests and native controls at the head, and the placement guard's function on a real csr.csv.
# portable_checks.sh <clone> <scratch> <boot-run-dir>
. "$(dirname "$0")/env.sh"
cd "$1" || exit 9
for c in "tb/verilator/nvm_split_target/run.py --self-test" "sw/firmware/ctrl_nvm/plat/gen_flash_port.py --self-test" \
         "tb/verilator/ctrl_service_budget/run.py --self-test" \
         "tb/verilator/ctrl_split_boot/run.py --build-dir $2/native --native-controls" "scripts/check_nvm_capture.py"; do
  python3 -B $c > "$2/out.log" 2>&1; rc=$?
  echo "rc=$rc: $c"; tail -2 "$2/out.log" | cut -c1-170
done
python3 -B - "$1" "$3" <<'PY'
import copy, json, shutil, sys, tempfile
from pathlib import Path
clone, run = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))
import split_soc
csr = (run / 'soc/csr.csv').read_text()
good = run / 'split-soc/flash-map'
print('guard on the real map:', split_soc.map_deviations(csr, good))
base = json.loads((good / 'flash_port.json').read_text())
for label, edit in (('master_cs +4', lambda p: p['registers'].__setitem__('spiflash_master_cs', p['registers']['spiflash_master_cs'] + 4)),
                    ('timer0_value at the stand-in', lambda p: p['registers'].__setitem__('timer0_value', 0xf0003810)),
                    ('window at the stand-in', lambda p: p['flash'].__setitem__('base', 0x20000000))):
    d = Path(tempfile.mkdtemp())
    p = copy.deepcopy(base); edit(p)
    (d / 'flash_port.json').write_text(json.dumps(p))
    print('guard,', label + ':', split_soc.map_deviations(csr, d))
    shutil.rmtree(d)
PY
