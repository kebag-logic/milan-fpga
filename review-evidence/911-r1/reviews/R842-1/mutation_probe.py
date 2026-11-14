#!/usr/bin/env python3
"""Reproduce four board-refusal mutations in disposable source copies."""
import concurrent.futures
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile

repo, packet = map(Path, sys.argv[1:3])
scratch = packet / 'scratch'
baseline = scratch / 'mutation-baseline'
baseline.mkdir(exist_ok=True)
archive = subprocess.check_output(['git', 'archive', 'HEAD'], cwd=repo)
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    tar.extractall(baseline, filter='data')
del archive
mutations = {
    'M1': ('sw/litex/deploy.sh',
        '    "$PYTHON" "$HERE/qspi_owner_transition.py" check-board --layout "$layout" \\\n        --bit "$bit" --detect "$scratch/jtag-detect.txt" > /dev/null || {\n        echo "[deploy] REFUSED: the FPGA on the cable is not the image set\'s part." >&2\n        return 2\n    }\n', '', 'loaded the bridge'),
    'M2': ('sw/litex/qspi_owner_transition.py', '    if read != jedec:', '    if False and read != jedec:', 'flash-pair: accepted'),
    'M3': ('sw/litex/deploy.sh', '    prove_board "$layout" "$bit" "$tmp" || exit 2\n    write_target_bit', '    write_target_bit', 'flash: accepted'),
    'M4': ('sw/litex/qspi_owner_transition.py', '    if (not isinstance(device, str)', '    if (False and not isinstance(device, str)', "no 'names no flash device'"),
}
# M4 must remove the entire metadata predicate, not only its first term.
mutations['M4'] = ('sw/litex/qspi_owner_transition.py',
    '    if (not isinstance(device, str) or not device or type(jedec) is not int\n            or not 0 < jedec <= 0xFF_FFFF):',
    '    if False:', "no 'names no flash device'")

def run(item):
    name, (relative, old, new, expected) = item
    tree = scratch / ('mutation-' + name)
    shutil.copytree(baseline, tree, dirs_exist_ok=True)
    path = tree / relative
    source = path.read_text()
    assert source.count(old) == 1, (name, source.count(old))
    path.write_text(source.replace(old, new))
    env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
    code = "import sys; sys.path.insert(0,'sw/builder'); import test_builder as t; t.test_qspi_owner_transition_completed_write_prefixes()"
    result = subprocess.run(['python3', '-B', '-c', code], cwd=tree, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=550)
    output = result.stdout.decode(errors='replace').replace(str(scratch), '<scratch>')
    (packet / ('mutation-' + name + '.log')).write_text(output)
    (packet / ('mutation-' + name + '.rc')).write_text(str(result.returncode) + '\n')
    assert result.returncode != 0 and expected in output, (name, result.returncode, output[-1000:])
    print(name, 'KILLED', expected, flush=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(run, [(k, v) for k, v in mutations.items() if len(sys.argv) < 4 or k in sys.argv[3:]]))
