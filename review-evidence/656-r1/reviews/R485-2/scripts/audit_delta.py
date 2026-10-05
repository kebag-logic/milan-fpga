#!/usr/bin/env python3
"""Offline body-delta and rate receipts; run from any exact-head checkout."""
import argparse
import difflib
import hashlib
import json
from fractions import Fraction
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    receipts = args.packet / 'receipts'
    original = (receipts / 'PR-BODY.original.md').read_bytes()
    current = (receipts / 'PR-BODY.live.md').read_bytes()
    expected = '19d959618430f119f1313173309c578fee09efddd68597c808200014201b5c4d'
    assert hashlib.sha256(original).hexdigest() == expected
    blob = hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest()
    assert blob == '8c084b98a9b60cbec1b0d45dd15ce4bf94db36a7'
    start = b'- **INTERNAL against an asynchronous talker'
    end = b'- **The exact 160-PDU pin.**'

    def split(body):
        assert body.count(start) == 1 and body.count(end) == 1
        a = body.index(start)
        b = body.index(end, a)
        return body[:a], body[a:b], body[b:]

    old_prefix, old_bullet, old_suffix = split(original)
    new_prefix, new_bullet, new_suffix = split(current)
    assert old_prefix == new_prefix and old_suffix == new_suffix
    assert old_bullet != new_bullet
    assert b'0.48 events/s per fed pair per 10 ppm' in new_bullet
    assert b'0.51/s at plan A\'s\n  10.64 ppm' in new_bullet
    assert b'For this leg\'s\n  old axis-paced talker' in new_bullet
    assert b'clock slipped on the loopback path at INTERNAL before A2-a too.' in new_bullet
    delta = ''.join(difflib.unified_diff(
        original.decode().splitlines(True), current.decode().splitlines(True),
        fromfile='PR-BODY.original.md', tofile='PR-BODY.live.md'))
    (receipts / 'body.diff').write_text(delta)
    identity = json.loads((receipts / 'public-identity.json').read_text())
    assert identity['head'] == 'd0e29f6dda6f04f3ace1dbb395f57379e58cacaf'
    assert identity['tree'] == '289f09d8c7151617ffb019f49b5c972924e4fedd'
    print('Original public author body matches its original and published SHA-256.')
    print('Original public author body matches its recorded blob identity.')
    print('Only the INTERNAL limitation bullet differs; prefix and suffix are byte-identical.')
    print('Original body SHA-256:', hashlib.sha256(original).hexdigest())
    print('Live body SHA-256:', hashlib.sha256(current).hexdigest())
    print('Body diff SHA-256:', hashlib.sha256(delta.encode()).hexdigest())
    print('Public head:', identity['head'])
    print('Public tree:', identity['tree'])
    nominal = Fraction(48000)
    per_10_ppm = nominal * Fraction(10, 1000000)
    per_rounded_plan_ppm = nominal * Fraction(1064, 100000000)
    fsync = Fraction(50000000 * 782, 1591 * 512)
    slip = nominal - fsync
    print(f'48000 * 10 / 1000000 = {float(per_10_ppm):.8f} events/s per fed pair')
    print(f'48000 * 10.64 / 1000000 = {float(per_rounded_plan_ppm):.8f} events/s per fed pair')
    print(f'Plan FSYNC = {float(fsync):.9f} Hz')
    print(f'Exact plan offset relative to nominal = {float(slip / nominal * 1000000):.9f} ppm')
    print(f'Exact nominal-versus-plan slip = {float(slip):.9f} events/s per fed pair')
    print(f'Exact slip period = {float(1 / slip):.9f} s')
    assert per_10_ppm == Fraction(48, 100)
    assert round(float(per_rounded_plan_ppm), 2) == 0.51
    assert round(float(slip), 2) == 0.51
    print('PASS: numerical claims and body-edit scope.')


if __name__ == '__main__':
    main()
