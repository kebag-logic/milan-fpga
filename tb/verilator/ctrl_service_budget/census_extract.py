# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A compact census extract: every case manifest, and of each observation extract only the lines a grader reads.

usage: python3 -I census_extract.py PACKET OUT

PACKET is a text receipt packet with its full observation extracts (census.json, census/<variant>/<group>/...).
OUT receives census.json, published-qualification.json, one directory per case and FILES.json. Each case keeps its
scenario, stimulus, original grade and any journal byte for byte. Its observations are the packet's, less the SPAN and
CALL lines of every traced function no grader reads (READ_LABELS); every other line is kept, in order and unchanged.
FILES.json maps every file written to the packet files it comes from and their SHA256, each checked against the
packet's FILES inventory. Each compact case is regraded on the way (receipt_regrade.regrade) and must reproduce its
recorded grade exactly. receipt_regrade.py then runs on OUT as on a full packet, with OUT's part limit (PART_LIMIT).
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bind_save  # noqa: E402
import kept_grade  # noqa: E402
import poll_items  # noqa: E402
import receipt_regrade  # noqa: E402
import round_grade  # noqa: E402
import slice_grade  # noqa: E402

#: The traced functions a grader reads: poll_grade's first and last polls, items, offers and their handler
#: (poll_items), THE RETRY's rounds, attempts and builds (round_grade), SRP's records (kept_grade, slice_grade) and
#: AECP's frames (declaring_outputs, record_classes), and the saved-state store's seal and read-back calls that place a
#: bind within a save's phases (bind_save). The others (a pass's parts, poll_items.PART_SPANS and PART_CALLS, and the
#: store's other calls) serve the cost measurement, which no grader repeats.
READ_LABELS = frozenset({poll_items.FIRST, poll_items.LAST, poll_items.OFFER, poll_items.HANDLER,
                         *(label for label, _ in poll_items.ITEMS.values()), round_grade.ROUND, round_grade.ATTEMPT,
                         round_grade.BUILT, kept_grade.RECORD, slice_grade.RECORD, 'aecp_mbx:frame',
                         bind_save.SEAL_CALL, bind_save.READ_CALL})
#: The largest part a compact extract writes (its census.json states it; receipt_regrade.py caps it at 15 MB).
PART_LIMIT = 14_000_000


def sha(data: bytes) -> str:
    """SHA256 of exactly the bytes named."""
    return hashlib.sha256(data).hexdigest()


def read_line(line: str) -> bool:
    """Whether a grader reads this observation line: every line but a SPAN or CALL of a function none reads."""
    fields = line.split()
    return not fields or fields[0] not in ('SPAN', 'CALL') or fields[-1] in READ_LABELS


def compact(text: str) -> str:
    """The observation lines a grader reads, each unchanged and in order."""
    return ''.join(line for line in text.splitlines(keepends=True) if read_line(line))


def parts(directory: Path, name: str, data: bytes) -> dict:
    """Numbered text parts of at most PART_LIMIT bytes, cut at line ends, with each part's and the whole's hash."""
    directory.mkdir(parents=True, exist_ok=True)
    records, start = [], 0
    while start < len(data) or not records:
        end = min(start + PART_LIMIT, len(data))
        if end < len(data):
            end = data.rfind(b'\n', start, end) + 1
        piece = data[start:end]
        single = start == 0 and end == len(data)
        path = directory / (name if single else f'{name}.part{len(records) + 1:04d}.txt')
        path.write_bytes(piece)
        records.append(dict(file=path.name, bytes=len(piece), sha256=sha(piece)))
        start = end
        if not data:
            break
    return dict(bytes=len(data), sha256=sha(data), parts=records)


def inventory(packet: Path) -> dict[str, str]:
    """The packet's FILES inventory: every file's SHA256 by its path, from FILES.tsv or its numbered parts."""
    record = json.loads((packet / 'FILES.manifest.json').read_text())
    text = receipt_regrade.read_parts(packet, record).decode()
    rows = [line.split('\t') for line in text.splitlines()[1:] if line]
    return {path: digest for path, _, digest in rows}


def sources(packet: Path, directory: Path, record: dict, listed: dict[str, str]) -> list[dict]:
    """A packet record's parts as paths and SHA256, each the one the FILES inventory lists."""
    out = []
    for part in record['parts']:
        path = str((directory / part['file']).relative_to(packet))
        if listed.get(path) != part['sha256']:
            raise ValueError(f'{path}: not the file the FILES inventory lists')
        out.append(dict(path=path, sha256=part['sha256']))
    return out


def case(packet: Path, row: dict, out: Path, listed: dict[str, str]) -> tuple[dict, list[dict]]:
    """One case: its files written to OUT, its regrade checked, and its census row and FILES entries returned."""
    path = packet / row['manifest']
    if sha(path.read_bytes()) != row['sha256']:
        raise ValueError(f'manifest integrity failure: {row["case"]}')
    old, source = json.loads(path.read_text()), path.parent
    target = out / 'census' / row['case']
    manifest, files = dict(old), []
    for key, name in (('group', 'scenario.json'), ('stimulus', 'stimulus.txt'), ('grade', 'original-grade.json'),
                      ('journal', 'journal.hex.txt')):
        if key in old:
            manifest[key] = parts(target, name, receipt_regrade.read_parts(source, old[key]))
            files.append(dict(record=manifest[key], relation='identical', sources=sources(packet, source, old[key],
                                                                                            listed)))
    full = receipt_regrade.read_parts(source, old['extract'])
    manifest['full_extract'] = dict(bytes=old['extract']['bytes'], sha256=old['extract']['sha256'])
    manifest['extract'] = parts(target, 'observations.log', compact(full.decode()).encode())
    manifest['read_labels'] = sorted(READ_LABELS)
    files.append(dict(record=manifest['extract'], relation='the lines a grader reads, in order',
                      sources=sources(packet, source, old['extract'], listed)))
    (target / 'manifest.json').write_text(json.dumps(manifest, separators=(',', ':')) + '\n')
    files.append(dict(record=dict(parts=[dict(file='manifest.json')]), relation='the packet manifest, its extract '
                      'record replaced and the full extract named', sources=[dict(path=row['manifest'],
                                                                                   sha256=row['sha256'])]))
    receipt_regrade.regrade(target / 'manifest.json', limit=PART_LIMIT + 1)  # a part may be PART_LIMIT bytes exactly
    entries = [dict(path=str((target / p['file']).relative_to(out)), sha256=sha((target / p['file']).read_bytes()),
                    relation=f['relation'], sources=f['sources']) for f in files for p in f['record']['parts']]
    return dict(case=row['case'], manifest=str((target / 'manifest.json').relative_to(out)),
                sha256=sha((target / 'manifest.json').read_bytes())), entries


def main(argv: list[str]) -> int:
    """Write OUT from PACKET; exit 1 if any case does not regrade to its recorded grade."""
    if len(argv) != 2:
        print(__doc__)
        return 2
    packet, out = Path(argv[0]), Path(argv[1])
    census, listed = json.loads((packet / 'census.json').read_text()), inventory(packet)
    rows, files = [], []
    for row in census['cases']:
        written, entries = case(packet, row, out, listed)
        rows.append(written)
        files.extend(entries)
        print(f'EXTRACTED {row["case"]}: complete grade reproduced', flush=True)
    shutil.copyfile(packet / 'published-qualification.json', out / 'published-qualification.json')
    (out / 'census.json').write_text(json.dumps(dict(source_head=census['source_head'], part_limit=PART_LIMIT,
                                                     read_labels=sorted(READ_LABELS), cases=rows), indent=1) + '\n')
    (out / 'FILES.json').write_text(json.dumps(files, indent=1) + '\n')
    print(f'RESULT: PASS cases={len(rows)} files={len(files) + 3}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
