"""Public-hygiene scan of published text for PR #604 round 2.

Usage: python3 hygiene_scan.py FILE_OR_DIR...
Reports, per file, matches of: absolute or temporary paths, the site-local
command-wrapper name, the lane-root variable, host/instrument/vendor/tool
names (matched by hash), and 48/64-bit hex identifiers (MAC addresses, entity or clock IDs).
Informational only; the reviewer classifies each hit in REPORT.md.
"""
import hashlib
import re
import sys
from pathlib import Path

PATTERNS = {
    'abs-or-tmp-path': r'(?<![\w.])/(?:tmp|home|data|root|Users|mnt|opt|srv|var)/[^\s"\'`)]*',
    'mac-colon': r'\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b',
    'hex48': r'(?<![0-9a-fA-F])[0-9a-fA-F]{12}(?![0-9a-fA-F])',
    'hex64': r'(?<![0-9a-fA-F])[0-9a-fA-F]{16}(?![0-9a-fA-F])',
    'serial-word': r'(?i)\bserial(?: number)?\s*[:=#]\s*\S+',
}
# Names that must not appear are matched by the first 16 hex digits of the
# sha256 of the lower-case word, so this published script does not repeat them.
# Shell-variable names ($NAME or ${NAME}) are matched the same way.
VAR_HASHES = {'lane-root-var': ['2ff22bcc1f6d88c5']}
NAME_HASHES = {
    "wrapper-name": [
        "3dc0deea30053c57"
    ],
    "host-names": [
        "697a7fbbba5c8e0f",
        "8316ad00aebd4551",
        "c592df4a86933b92"
    ],
    "vendor-or-instrument": [
        "1d0e1bac0cb69a45",
        "23ee7360409471e1",
        "26b47209413e5776",
        "3393b41eeeea1c11",
        "35ab2b8fa9e0fc93",
        "57b9816cc9da0fe1",
        "68eb6beb63efaebc",
        "6ed3bee7ecea8a3c",
        "75b62e504ca7021a",
        "7640da40298286a6",
        "80537d65d479a2f9",
        "81d3d8140035e928",
        "9dd0ccd73c86306b",
        "a617d67e744b7c2d",
        "ce3631a6a7b0b82b",
        "d4a83e68937b7294",
        "e4c698ced677a692",
        "e73b79a0b10f8cdb",
        "e97407735e49029c"
    ],
    "tool-or-model": [
        "053ea4804ef1bb33",
        "3ea125d0bff386e6",
        "57de4cf40144bdf7",
        "5d72436256ada538",
        "60965168ce762e94",
        "7d3194f79e645c42",
        "c70eca6b0f88f44d",
        "c857d09db23e6822"
    ]
}


def files(args):
    for a in map(Path, args):
        if a.is_dir():
            yield from sorted(p for p in a.rglob('*') if p.is_file())
        else:
            yield a


def main():
    total = 0
    for f in files(sys.argv[1:]):
        try:
            text = f.read_text(errors='replace')
        except OSError:
            continue
        hits = {}
        words = set(re.findall(r'[a-z0-9][a-z0-9-]*', text.lower()))
        for name, digests in NAME_HASHES.items():
            found = sorted(w for w in words if hashlib.sha256(w.encode()).hexdigest()[:16] in digests)
            if found:
                hits[name] = ['<name hash %s>' % hashlib.sha256(w.encode()).hexdigest()[:16] for w in found]
        for name, digests in VAR_HASHES.items():
            found = sorted(v for v in set(re.findall(r'\$\{?([A-Za-z_][A-Za-z0-9_]*)', text))
                           if hashlib.sha256(v.encode()).hexdigest()[:16] in digests)
            if found:
                hits[name] = ['<variable hash %s>' % hashlib.sha256(v.encode()).hexdigest()[:16] for v in found]
        for name, pat in PATTERNS.items():
            found = sorted(set(re.findall(pat, text)))
            # sha256 digests and git object ids are 64/40 hex; skip hex hits inside longer hex runs (handled by lookarounds)
            if found:
                hits[name] = found
        if hits:
            print(f'## {f}')
            for name, found in hits.items():
                total += len(found)
                shown = found[:12]
                print(f'  {name}: {len(found)} distinct: {shown}{" ..." if len(found) > 12 else ""}')
    print(f'TOTAL distinct hits: {total}')


if __name__ == '__main__':
    main()
