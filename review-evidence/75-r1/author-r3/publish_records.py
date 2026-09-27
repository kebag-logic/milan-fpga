"""Prepare the three non-stop cycle records for publication, without raw captures.

Usage: python3 publish_records.py OPERATOR_PACKET OUTPUT_DIRECTORY
Only the historical raw-capture path changes, to a relative identifier.
Original acquisition PASS labels are retained as historical evidence.
"""
import csv
import hashlib
import json
from pathlib import Path
import sys

from recompute import require


def main():
    packet, output = map(Path, sys.argv[1:])
    require(output.resolve() != packet.resolve(), 'output aliases input')
    summary = json.loads((output/'declarations-summary.json').read_text())
    sources = []
    for row in summary['nonstops']:
        name = f"talker-{row['cycle']:03d}"
        destination = output/name
        destination.mkdir(exist_ok=True)
        for source in sorted((packet/name).iterdir()):
            if source.name == 'MANIFEST.sha256':
                continue
            require(source.is_file() and source.stat().st_size <= 200_000, 'unexpected record')
            original = source.read_bytes()
            published = original
            if source.name == 'raw-artifacts.json':
                published = (json.dumps([
                    dict(identifier=f'{name}/tap.pcap', size=r['size'], sha256=r['sha256'])
                    for r in json.loads(original)
                ], indent=2)+'\n').encode()
            (destination/source.name).write_bytes(published)
            sources.append(dict(identifier=f'{name}/{source.name}',
                                source_sha256=hashlib.sha256(original).hexdigest(),
                                published_sha256=hashlib.sha256(published).hexdigest(),
                                transform='relative capture identifier' if published != original else 'unchanged'))
        manifest = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n'
                           for p in sorted(destination.iterdir()) if p.name != 'MANIFEST.sha256')
        (destination/'MANIFEST.sha256').write_text(manifest)
    with (output/'published-records.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(sources[0]))
        writer.writeheader()
        writer.writerows(sources)
    print(f"Prepared {len(summary['nonstops'])} cycle directories, {len(sources)} source records; no raw captures.")


if __name__ == '__main__':
    main()
