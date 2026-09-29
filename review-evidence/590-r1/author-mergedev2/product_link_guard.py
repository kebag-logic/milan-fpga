"""Exercise the dispatch dependency using the actual product BIOS link recipe.

Same recipe as the round-3 control; the round-3 BIOS objects are only read,
and every output goes to this round's work and log directories.
"""
from pathlib import Path
import hashlib
import json
import shlex
import subprocess

out = Path(__file__).parent
work = Path('$VALIDATION_STORAGE/590-a430/link-guard')
work.mkdir(parents=True, exist_ok=True)
bios = Path('$VALIDATION_STORAGE/590-a411/service-1x1-all/software/bios')
makefile = '$WORKSPACE_HOME/litex-milan/litex/litex/soc/software/bios/Makefile'
recipe = subprocess.check_output(['timeout', '120', 'make', '-n', '-f', makefile,
                                  '-W', 'main.o', 'bios.elf', 'V=1'], cwd=bios, text=True)
command = shlex.split(recipe.replace('\\\n', '').splitlines()[0])
assert '-Wl,--whole-archive' in command
stripped = work / 'main-no-marker.o'
subprocess.run(['timeout', '120', '$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux-objcopy',
                '--strip-symbol=bios_dispatch_hook_required', str(bios / 'main.o'), str(stripped)], check=True)
rows = []
for control in ('present', 'missing-marker'):
    args = list(command)
    args[args.index('-o') + 1] = str(work / (control + '.elf'))
    args[args.index('-Wl,-Map,bios.elf.map')] = '-Wl,-Map,' + str(work / (control + '.map'))
    if control == 'missing-marker':
        args[args.index('main.o')] = str(stripped)
    log = out / 'logs' / ('product-link-' + control + '.log')
    result = subprocess.run(['timeout', '120', *args], cwd=bios, capture_output=True, text=True, timeout=130)
    log.write_text(result.stdout + result.stderr)
    assert (result.returncode == 0) == (control == 'present')
    if control == 'missing-marker':
        assert 'undefined reference to `bios_dispatch_hook_required' in result.stderr
    rows.append(dict(control=control, command=args, rc=result.returncode,
                     size=log.stat().st_size, sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
(out / 'product-link-guard.json').write_text(json.dumps(rows, indent=2) + '\n')
print('PASS: actual RV32 BIOS links with marker; missing marker fails by name')
