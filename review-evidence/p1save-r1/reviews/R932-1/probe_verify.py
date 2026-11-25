#!/usr/bin/env python3
"""Check whether the frame timing grade proves a complete post-program read."""
from pathlib import Path
from types import SimpleNamespace
import struct
import sys
import zlib

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
sys.path.insert(0, str(root / 'scripts'))
import grade
import save_burst
import save_grade

image = 512
base = 0xe40000
address = base + save_burst.delta_room(image)[0]
frame = struct.pack('<7I', save_burst.KLD3_MAGIC, save_burst.KLD3_VER, 7, 5, 40, 30, 0) + bytes(32)
frame += struct.pack('<I', zlib.crc32(frame))
assert len(frame) == 64

def check(name, reads):
    log = SimpleNamespace(sys_hz=100000000, programmed=[(1000, address, frame)],
                          flash_ops=[(1000, grade.FLASH_PROGRAM, address, len(frame))], reads=reads)
    saves = save_burst.frame_saves(log, image, [base])
    print(name, 'input_reads=', reads, 'merged_reads=', save_grade.merged_reads(log),
          'durable=', saves[0]['durable'])
    return saves[0]['durable']

assert check('NO_POST_PROGRAM_READ', [(800, 900, address, 64)]) is None
assert check('FULL_POST_PROGRAM_CONTROL', [(800, 900, address, 64), (1100, 1200, address, 64)]) == 1200
escaped = check('ONLY_FOUR_BYTES_AFTER_PROGRAM', [(800, 900, address, 64), (1100, 1200, address, 4)])
assert escaped == 1200, 'The reproduction no longer matches the reviewed defect'
print('REPRODUCED: a 64-byte frame is credited as verified after only four post-program bytes.')

# Repeat through the complete save reconstruction with valid container/frame CRCs.
import selftest_burst as fixture
before = fixture.container({0: bytes(64)}, 5, ver=0x00030001)
after = fixture.container({0: b'changed'.ljust(64, b'\0')}, 7, ver=0x00030001)
frame = fixture.delta(before, after)
programmed = [(110, base, before[:256]), (111, base + 256, before[256:]), (1000, address, frame)]
log = SimpleNamespace(sys_hz=100000000, programmed=programmed, stepped=[], polls=[],
                      flash_ops=[(100, grade.FLASH_ERASE, base, 0),
                                 (110, grade.FLASH_PROGRAM, base, 256),
                                 (111, grade.FLASH_PROGRAM, base + 256, 256),
                                 (1000, grade.FLASH_PROGRAM, address, len(frame))],
                      reads=[(200, 300, base, 512), (800, 900, address, len(frame)),
                             (1100, 1200, address, 4)])
saves = save_burst.saves(log, image)
print('FULL_RECONSTRUCTION', [{k: v for k, v in s.items() if k not in ('blob', 'pages')} for s in saves])
assert saves[-1]['kind'] == 'frame' and saves[-1]['seq'] == 7 and saves[-1]['durable'] == 1200
assert saves[-1]['blob'] == after
print('REPRODUCED with valid frame and reconstructed container: full save grade also credits partial verification.')
