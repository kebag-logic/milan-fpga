#!/usr/bin/env python3
"""Summarise the capture receipt change between two commits of a checkout.

Usage (from the repository root): receipt_delta.py <base-rev> <head-rev>
Prints per-arm row equality, changed scalar keys, maxima and the hashes the
receipt pins against the files at <head-rev>.
"""
import hashlib
import json
import subprocess
import sys

PATH = 'tb/verilator/nvm_capture_cpu/measurements.json'


def show(rev: str, path: str) -> bytes:
    return subprocess.run(['git', 'show', f'{rev}:{path}'], check=True,
                          capture_output=True).stdout


def main() -> int:
    base_rev, head_rev = sys.argv[1:3]
    base, head = (json.loads(show(r, PATH)) for r in (base_rev, head_rev))
    out = {'top_level_changed': sorted(k for k in set(base) | set(head)
                                       if base.get(k) != head.get(k))}
    key = lambda a: (a['shape'], a['cpu_hz'], a['traffic'])
    bm = {key(a): a for a in base['measurements']}
    arms = []
    for arm in head['measurements']:
        old = bm.get(key(arm), {})
        arms.append(dict(arm=list(key(arm)), captures=arm['captures'],
                         rows=len(arm['rows']),
                         rows_equal_base=arm['rows'] == old.get('rows'),
                         changed_keys=sorted(k for k in set(arm) | set(old)
                                             if k != 'rows' and arm.get(k) != old.get(k)),
                         configured_cpu_hz=arm['configured_cpu_hz'],
                         minimum_ms=arm['minimum_ms'], maximum_ms=arm['maximum_ms'],
                         all_ok=all(r['ok'] == 1 and r['mismatches'] == 0 and r['open'] == 0
                                    for r in arm['rows'])))
    out['arms'] = arms
    out['maxima'] = head['maxima']
    out['maxima_equal_base'] = head['maxima'] == base['maxima']
    pins = {}
    for name, digest in head['harness_sha256'].items():
        data = show(head_rev, f'tb/verilator/nvm_capture_cpu/{name}')
        pins[name] = hashlib.sha256(data).hexdigest() == digest
    fw = show(head_rev, 'sw/firmware/milan_baremetal/milan_baremetal.c')
    pins['product_firmware'] = hashlib.sha256(fw).hexdigest() == head['product_firmware_sha256']
    cfg = {}
    for arm in head['measurements']:
        data = show(head_rev, f"configs/{arm['shape']}.yaml")
        cfg[arm['shape']] = hashlib.sha256(data).hexdigest() == arm.get('config_sha256')
    out['pinned_hashes_match_head'] = pins
    out['config_sha256_match_head'] = cfg
    sub = {}
    for path, pin in head.get('processor_pins', {}).items():
        line = subprocess.run(['git', 'ls-tree', head_rev, path], check=True,
                              capture_output=True, text=True).stdout.split()
        sub[path] = line[2] == pin if line else None
    out['processor_pins_match_gitlinks'] = sub
    out['base_field'] = head.get('base')
    print(json.dumps(out, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
