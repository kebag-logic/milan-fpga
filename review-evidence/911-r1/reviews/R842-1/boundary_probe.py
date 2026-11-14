#!/usr/bin/env python3
"""Independent layout, identification and documented-command probes."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

repo, packet = map(Path, sys.argv[1:3])
sys.path.insert(0, str(repo / 'sw/litex'))
import flash_map
import layout_from_soch
import qspi_owner_transition as q

fixture = packet / 'scratch/boundaries'
(fixture / 'gateware').mkdir(parents=True, exist_ok=True)
bit = fixture / 'gateware/alinx_ax7101.bit'
layout_path = fixture / 'flashboot_layout.json'
detect = fixture / 'detect.txt'
flash = fixture / 'flash.txt'
slot = 10 * 1024**2
layout = {
    'manifest': 'baremetal', 'gptp_owner': 'fabric', 'cpu_xlen': 32,
    'flash_device': 'n25q128a13', 'flash_jedec_id': 0x20ba18,
    'images': [{'name': 'bitstream', 'offset': 0, 'budget': slot},
               {'name': 'aem', 'offset': slot, 'budget': 65536}],
}
for part, expected in [(None, 0x400000), ('xc7a200t-fbg484-2', slot)]:
    rows, size, erase = flash_map.load_map(part)
    assert flash_map.check_map(rows, size, erase) == []
    assert next(r[1] for r in rows if r[0] == 'aem') == expected
    rebuilt = layout_from_soch._manifest_and_images([{'name': 'aem', 'offset': expected, 'addr': 0, 'budget': 65536}])[1]
    assert rebuilt[0]['budget'] == rebuilt[1]['offset'] == expected
print('Both maps aligned, non-overlapping and in 16 MiB; reconstruction follows compiled AEM offsets.')
for length, accepted in [(9730652, True), (slot, True), (slot + 1, False)]:
    q._fake_bit(bit, bytes.fromhex('aa995566') + b'\x55' * (length - 4), part=b'7a200tfbg484\0')
    layout.update(q.bitstream_binding(bit))
    layout_path.write_text(json.dumps(layout))
    try:
        q.validate_artifact_pair(layout_path, bit, 'xc7a200tfbg484')
        assert accepted
    except q.TransitionError as error:
        assert not accepted and 'exceeds' in str(error), error
    print('Payload length', length, 'ACCEPT' if accepted else 'REFUSE')
q._fake_bit(bit, bytes.fromhex('aa995566') + b'payload', part=b'7a200tfbg484\0')
layout.update(q.bitstream_binding(bit))
layout_path.write_text(json.dumps(layout))
good_die = '\tmodel  xc7a200\n'
good_flash = '20 ba 18 read 20ba18\n'
cases = [
    ('correct', good_die, good_flash, True),
    ('alternate JEDEC form', good_die, 'JEDEC ID: 0x20ba18\n', True),
    ('both agreeing forms', good_die, good_flash + 'JEDEC ID: 0x20ba18\n', True),
    ('wrong die', 'model xc7a100\n', good_flash, False),
    ('empty die', '', good_flash, False),
    ('two different dies', good_die + 'model xc7a100\n', good_flash, False),
    ('wrong flash', good_die, 'JEDEC ID: 0x20ba19\n', False),
    ('empty flash', good_die, '', False),
    ('conflicting flash forms', good_die, good_flash + 'JEDEC ID: 0x20ba19\n', False),
]
for name, die_text, flash_text, accepted in cases:
    detect.write_text(die_text)
    flash.write_text(flash_text)
    try:
        q.check_board(layout_path, bit, detect, flash)
        assert accepted, name
    except q.TransitionError:
        assert not accepted, name
    print('Identification:', name, 'ACCEPT' if accepted else 'REFUSE')
for invalid in [None, 0, -1, 0x1000000, True, '20ba18']:
    layout['flash_jedec_id'] = invalid
    layout_path.write_text(json.dumps(layout))
    try:
        q.check_board(layout_path, bit, detect, flash)
    except q.TransitionError as error:
        assert 'names no flash device' in str(error)
    else:
        raise AssertionError(invalid)
print('Malformed layout JEDEC IDs: all six refused before identification parsing.')
layout['flash_jedec_id'] = 0x20ba18
layout_path.write_text(json.dumps(layout))
(fixture / 'aem_desc.bin').write_bytes(b'AEMI-fixture')
bin_dir = fixture / 'bin'
bin_dir.mkdir(exist_ok=True)
stub = bin_dir / 'openFPGALoader'
stub.write_text('#!/usr/bin/env python3\nimport json,os,sys\nwith open(os.environ["GUIDE_LOG"],"a") as f: f.write(json.dumps(sys.argv[1:])+"\\n")\n')
stub.chmod(0o755)
doc = (repo / 'docs/guides/BOARD_DEPLOYMENT.md').read_text()
section = doc.split('## Flash an image set over JTAG\n')[1].split('\n## ')[0]
blocks = re.findall(r'```sh\n(.*?)```', section, re.S)
assert len(blocks) == 3
program = '\n'.join(blocks).replace('B=<image set directory>', 'B=' + str(fixture))
log = fixture / 'guide-argv.jsonl'
log.write_text('')
env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'], GUIDE_LOG=str(log))
result = subprocess.run(['bash', '-eu', '-c', program], env=env, capture_output=True, text=True)
assert result.returncode == 0, result.stderr
calls = [json.loads(row) for row in log.read_text().splitlines()]
assert len(calls) == 3
assert all(row[row.index('--fpga-part') + 1] == 'xc7a200tfbg484' for row in calls)
assert '-f' not in calls[0] and '--write-flash' not in calls[0]
assert calls[1][calls[1].index('-o') + 1] == '0xa00000'
assert '--write-flash' in calls[1] and '--verify' in calls[1] and '-f' in calls[2] and '--verify' in calls[2]
print('Three documented JTAG shell blocks execute with fixture image set and stub cable: layout-derived part, SRAM load, AEM first at 0xa00000, verified bitstream last.')
print('No programmer or hardware accessed; fixture bitstream is synthetic.')
