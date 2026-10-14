"""Check the round-8 run's artifact index (bios.bin, instrumented firmware) against receipt arm hashes.

Usage: python3 -I artifacts_vs_receipt.py <receipt.json> <CAPTURE-ARTIFACTS.json> <old-receipt.json>
"""
import json
import sys

receipt = json.load(open(sys.argv[1]))
index = {e['file']: e['sha256'] for e in json.load(open(sys.argv[2]))}
old = json.load(open(sys.argv[3]))
ok = True
for arm, prev in zip(receipt['measurements'], old['measurements']):
    tag = '%s-%d-%s' % ('8x8' if '8x8' in arm['shape'] else '1x1', arm['cpu_hz'] // 1_000_000, arm['traffic'])
    base = f'capture52/{tag}/capture-{tag}/'
    bios = index[base + 'software/bios/bios.bin']
    fw = index[base + 'measurement_firmware/milan_baremetal.c']
    good = (bios == arm['bios_sha256'] == prev['bios_sha256']
            and fw == arm['instrumented_firmware_sha256'] == prev['instrumented_firmware_sha256'])
    ok &= good
    print(tag, 'bios', bios[:12], 'fw', fw[:12], 'match_receipt_and_round7=%s' % good,
          'Vsim', index[base + 'native/Vsim'][:12])
print('ARTIFACTS_MATCH' if ok else 'ARTIFACTS_DIFFER')
