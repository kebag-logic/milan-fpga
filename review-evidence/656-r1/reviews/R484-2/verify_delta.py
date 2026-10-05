#!/usr/bin/env python3
"""Read-only, portable reproduction of the R484-2 body and rate checks.

Usage: python3 verify_delta.py CHECKOUT OUTPUT_DIRECTORY
Requires read access to the public repository through the command-line API.
Full API responses stay in OUTPUT_DIRECTORY/scratch, never in the receipt set.
"""
import base64
import difflib
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

HEAD = 'd0e29f6dda6f04f3ace1dbb395f57379e58cacaf'
TREE = '289f09d8c7151617ffb019f49b5c972924e4fedd'
BASE = 'c0280fc008ef9c5c1650402a58bab3e47a92127b'
EVIDENCE = 'e5cae5f54a7efc54eb1b22095e310bb8324ace4e'
REPO = 'repos/kebag-logic/milan-fpga'


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', f'{REPO}/{path}']))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    checkout, output = map(Path, sys.argv[1:])
    scratch = output / 'scratch'
    receipts = output / 'receipts'
    scratch.mkdir(parents=True, exist_ok=True)
    receipts.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

    def git(*args):
        return subprocess.check_output(['git', '-C', str(checkout), *args], env=env)

    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('rev-parse', 'HEAD^{tree}').decode().strip() == TREE
    pr = api('pulls/662')
    commit = api(f'git/commits/{HEAD}')
    dev = api('git/ref/heads/dev')
    assert pr['head']['sha'] == HEAD
    assert commit['tree']['sha'] == TREE
    published = api(f'contents/review-evidence/656-r1/author/PR-BODY.md?ref={EVIDENCE}')
    original = base64.b64decode(published['content'])
    live = pr['body'].encode()
    assert published['sha'] == '8c084b98a9b60cbec1b0d45dd15ce4bf94db36a7'
    assert sha(original) == '19d959618430f119f1313173309c578fee09efddd68597c808200014201b5c4d'
    for name, data in [('original-body.md', original), ('live-body.md', live)]:
        (scratch / name).write_bytes(data)
    (scratch / 'latest-pr.json').write_text(json.dumps(pr, indent=2) + '\n')
    marker = b'- **INTERNAL against an asynchronous talker is not graded by this leg.**'
    following = b'- **The exact 160-PDU pin.**'

    def partition(body):
        start = body.index(marker)
        end = body.index(following, start)
        return body[:start], body[start:end], body[end:]

    old_parts, new_parts = partition(original), partition(live)
    assert old_parts[0] == new_parts[0], 'Changes before the authorized bullet'
    assert old_parts[2] == new_parts[2], 'Changes after the authorized bullet'
    expected = (
        '- **INTERNAL against an asynchronous talker is not graded by this leg.** It still slips\n'
        '  about 0.48 events/s per fed pair per 10 ppm on the loopback path (0.51/s at plan A\'s\n'
        '  10.64 ppm), counted on `SLIP_LB`. That is A2-a\'s documented consequence. For this leg\'s\n'
        '  old axis-paced talker the slip sat at the TDM junction before A2-a; a talker on any other\n'
        '  clock slipped on the loopback path at INTERNAL before A2-a too. A zero-glitch run\n'
        '  through the loopback lane (#396) needs the DUT to follow the talker, or the talker to follow\n'
        '  the DUT.\n'
    ).encode()
    assert new_parts[1] == expected, 'Unexpected replacement wording'
    diff = ''.join(difflib.unified_diff(original.decode().splitlines(True),
                                      live.decode().splitlines(True),
                                      fromfile='published-author-PR-BODY.md',
                                      tofile='live-PR-662-body.md'))
    (receipts / 'body.diff').write_text(diff)
    source = git('diff', '--no-ext-diff', '--no-textconv', f'{BASE}..{HEAD}')
    (receipts / 'source.diff').write_bytes(source)
    changed = git('diff', '--name-only', f'{BASE}..{HEAD}').decode().splitlines()
    assert changed == ['tb/verilator/milan_dp/README.md',
                       'tb/verilator/milan_dp/sim_ax1x1gptp.cpp']
    hz = Fraction(50_000_000)
    audio = hz * Fraction(782, 1591)
    fsync = audio / 512
    excess = 48000 - fsync
    ppm = excess / 48000 * 1_000_000
    per_10 = Fraction(48000 * 10, 1_000_000)
    per_1064 = Fraction(48000) * Fraction('10.64') / 1_000_000
    assert per_10 == Fraction('0.48')
    assert round(float(per_1064), 2) == .51
    assert round(float(excess), 2) == .51
    summary = {
        'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
        'published_head': pr['head']['sha'], 'published_tree': commit['tree']['sha'],
        'local_head': HEAD, 'local_tree': TREE, 'source_base': BASE,
        'live_dev_at_read': dev['object']['sha'],
        'pr_updated_at': pr['updated_at'],
        'original_public_blob': published['sha'],
        'original_body_sha256': sha(original), 'live_body_sha256': sha(live),
        'body_change': 'Only the INTERNAL-against-an-asynchronous-talker bullet',
        'unchanged_prefix_bytes': len(old_parts[0]),
        'unchanged_suffix_bytes': len(old_parts[2]),
        'source_diff_sha256': sha(source), 'source_changed_files': changed,
        'events_per_second_per_pair_at_10_ppm': float(per_10),
        'events_per_second_per_pair_at_10_64_ppm': float(per_1064),
        'modeled_fsync_hz': float(fsync), 'modeled_ppm_below_nominal': float(ppm),
        'modeled_excess_events_per_second_per_pair': float(excess),
        'modeled_seconds_per_slip': float(1 / excess),
        'new_pdu_period_axis_cycles': str(6 * 512 * Fraction(1591, 782)),
        'result': 'PASS',
    }
    (receipts / 'delta-check.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
