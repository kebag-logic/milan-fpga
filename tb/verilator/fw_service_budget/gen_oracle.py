#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Regenerate portable trace controls from completed, bound simulations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import run


def convert(build_dir: Path, plan: str) -> dict:
    """Check the recorded log, build and media against their original bytes."""
    stem = f'service-{plan}-1-0-0'
    receipt = json.loads((build_dir / (stem + '.json')).read_text())
    spec = json.loads((build_dir / 'service_spec.json').read_text())
    run.require(receipt['build_hashes'] == spec['build_hashes']
                == run.build_hashes(build_dir, spec), 'stale or unbound fixture build')
    raw = (build_dir / (stem + '.log')).read_bytes().decode()
    run.require(hashlib.sha256(raw.encode()).hexdigest() == receipt['log_sha256'],
                'fixture log digest mismatch')
    run.require(raw == receipt['raw_log'], 'fixture log differs from receipt')
    with tempfile.TemporaryDirectory(prefix='service-oracle-') as directory:
        media = run.oracle_media(Path(directory), receipt['shape'], receipt['media'])
    run.require(media == receipt['media'], 'fixture media differs from current built image')
    result = dict(shape=receipt['shape'], raw_log=raw, log_sha256=receipt['log_sha256'],
                  media={key: media[key] for key in ('populated', 'plan', 'slots_sha256')})
    graded = run.grade(raw, media)
    for key in ('rows', 'budget_findings', 'heartbeat', 'liveness'):
        run.require(graded[key] == receipt[key], 'fixture grading differs: ' + key)
        result[key] = graded[key]
    return result


def main() -> None:
    """Require both shapes and the paced case; never manufacture a trace."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--small-build', type=Path, required=True)
    parser.add_argument('--large-build', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=run.HERE / 'oracle.json')
    args = parser.parse_args()
    rows = [convert(args.small_build, 'all'), convert(args.large_build, 'all'),
            convert(args.small_build, 'uart-paced')]
    run.require([row['shape'] for row in rows] == [run.SHAPES[0], run.SHAPES[1], run.SHAPES[0]],
                'fixture shapes do not cover both supported builds')
    args.output.write_text(json.dumps(rows, indent=2) + '\n')


if __name__ == '__main__':
    main()
