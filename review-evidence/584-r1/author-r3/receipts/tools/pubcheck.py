#!/usr/bin/env python3
"""Require a packet to survive the publication rewrite byte-for-byte.

Usage: pubcheck.py PACKET --privacy-dir DIRECTORY --publisher SCRIPT
Optional --rewrite OLD=NEW adds a private host-prefix mapping. The publisher
is parsed for its constant REPLACEMENTS tuple; it is never executed. The
manager's privacy module supplies the content scrub. Report relative paths.
"""
import argparse
import ast
import importlib
import re
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path)
    parser.add_argument('--privacy-dir', required=True)
    parser.add_argument('--publisher', required=True, type=Path)
    parser.add_argument('--rewrite', action='append', default=[])
    args = parser.parse_args()
    sys.path.insert(0, args.privacy_dir)
    privacy = importlib.import_module('privacy')
    tree = ast.parse(args.publisher.read_text())
    pairs = next(ast.literal_eval(node.value) for node in tree.body
                 if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name)
                 and t.id == 'REPLACEMENTS' for t in node.targets))
    pairs = [tuple(v.split('=', 1)) for v in args.rewrite] + list(pairs)
    files = sorted(p for p in args.packet.rglob('*') if p.is_file())
    bad = []
    for p in files:
        data = p.read_bytes()
        pub = data
        for before, after in pairs:
            pub = pub.replace(before.encode(), after.encode())
        pub = privacy.scrub_redact(pub)
        reasons = []
        if pub != data:
            reasons.append('publication rewrite changes bytes')
        if re.search(rb'/(?:home/[^/\s]+|data(?:-2)?/)', data):
            reasons.append('raw host prefix remains')
        if len(data) > 200000:
            reasons.append('file exceeds 200000 bytes')
        if p.is_symlink():
            reasons.append('symlink')
        if reasons:
            bad.append(str(p.relative_to(args.packet)) + ': ' + ', '.join(reasons))
    for problem in bad:
        print(problem)
    print(f'Publication check: {len(files)} files; {len(files)-len(bad)} unchanged; {len(bad)} failures')
    return bool(bad)


if __name__ == '__main__':
    sys.exit(main())
