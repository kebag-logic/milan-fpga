#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Fetch the pinned host-side Bash parser without installing system packages."""

import argparse
import json
from pathlib import Path

from build import ROOT, verified_download


def main() -> int:
    """Keep the authenticated parser outside the source checkout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--pin', type=Path, help='reviewed public artifact record for a pin refresh')
    parser.add_argument('--record-pin', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(ROOT):
        raise ValueError('parser storage must be outside the checkout')
    lock = ROOT / 'ci/image/sources.lock.json'
    sources = json.loads(lock.read_text())
    pin = json.loads(args.pin.read_text()) if args.pin else sources['host_tools']['shfmt']
    if args.record_pin and not args.pin:
        raise ValueError('--record-pin requires --pin')
    verified_download({'tool': 'shfmt', **pin}, output)
    output.chmod(0o755)
    if args.record_pin:
        sources.setdefault('host_tools', {})['shfmt'] = pin
        lock.write_text(json.dumps(sources, sort_keys=True, indent=2) + '\n')
    print(f"PASS: shfmt {pin['version']} authenticated by size and SHA-256")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
