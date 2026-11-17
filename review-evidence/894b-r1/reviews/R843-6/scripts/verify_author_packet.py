#!/usr/bin/env python3
"""Verify an extracted author packet against its own INDEX.md and the archive's MANIFEST.json, and decode the two
RV32I words the image identity receipt names. usage: python3 -I verify_author_packet.py PACKET_DIR ARCHIVE_MANIFEST"""
import hashlib
import json
import re
import sys
from pathlib import Path

packet, manifest = Path(sys.argv[1]), Path(sys.argv[2])
index = {a: b for a, b in re.findall(r'^\| `([^`]+)` \| [\d,]+ \| `([0-9a-f]{64})` \|', (packet / 'INDEX.md').read_text(), re.M)}
entries = [e for e in json.loads(manifest.read_text()) if e['file'].startswith(packet.name + '/')]
files = sorted(p for p in packet.rglob('*') if p.is_file())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pub_ok = sum(sha(packet.parent / e['file']) == e['published_sha256'] for e in entries)
redacted = [e['file'] for e in entries if e['path_redacted']]
orig_eq_index = sum(index.get(e['file'][len(packet.name) + 1:]) == e['original_sha256'] for e in entries
                    if e['file'][len(packet.name) + 1:] in index)
index_eq_bytes = sum(sha(packet / k) == v for k, v in index.items() if (packet / k).exists())
print(f'packet {packet.name}: {len(files)} files, {len(entries)} archive manifest entries, {len(index)} INDEX entries')
print(f'archive published_sha256 equal to the bytes: {pub_ok} of {len(entries)}')
print(f'INDEX sha256 equal to the archive original_sha256: {orig_eq_index} of {len(index)}')
print(f'INDEX sha256 equal to the published bytes: {index_eq_bytes} of {len(index)} '
      f'(the rest are the {len(redacted)} path-redacted files)')
for f in redacted:
    print(f'  path_redacted: {f}')
print('INDEX title:', (packet / 'INDEX.md').read_text().splitlines()[0])
for word in (0x7ea00693, 0x7eb00693):
    imm, rs1, f3, rd, op = word >> 20, (word >> 15) & 31, (word >> 12) & 7, (word >> 7) & 31, word & 127
    print(f'{word:08x}: opcode {op:#04x} funct3 {f3} rd x{rd} rs1 x{rs1} imm {imm}'
          f' -> {"addi a3, zero, %d (li a3,%d)" % (imm, imm) if (op, f3, rs1, rd) == (0x13, 0, 0, 13) else "?"}')
join_cs, tx_row = 19, 74.26
for tx_ms in (70, 75):
    hold = 2 * 1000 + join_cs + (tx_ms + 9) // 10
    print(f'CTRL_LOOP_TX_MS {tx_ms}: SRP_REDECLARE_CS {hold} cs; after a JoinTime ({join_cs * 10} ms) and the tx row '
          f'{tx_row} ms, {hold * 10 - join_cs * 10 - tx_row:.2f} ms remain against 20000 (IEEE 802.1Q-2018 35.2.2.8)')
