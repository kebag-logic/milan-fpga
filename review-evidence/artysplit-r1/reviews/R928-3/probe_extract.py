"""Run focused extractor boundaries without changing the reviewed checkout.

Usage: python3 -B probe_extract.py SOURCE SCRATCH
"""
import json
import sys
from pathlib import Path
from unittest.mock import patch

source, scratch = map(Path, sys.argv[1:3])
sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
import census_extract as extract
import receipt_regrade as replay

scratch.mkdir(parents=True, exist_ok=True)
for size in (extract.PART_LIMIT - 1, extract.PART_LIMIT, extract.PART_LIMIT + 1):
    # Short complete text lines, including a newline at the exact part boundary.
    data = b'X\n' * (size // 2) + (b'\n' if size % 2 else b'')
    folder = scratch / str(size)
    record = extract.parts(folder, 'observations.log', data)
    result = {'input_bytes': size, 'part_bytes': [p['bytes'] for p in record['parts']]}
    for label, limit in [('extractor_case', extract.PART_LIMIT),
                         ('regrader_main', min(extract.PART_LIMIT + 1, replay.EXTRACT_PART_LIMIT))]:
        try:
            result[label] = 'PASS' if replay.read_parts(folder, record, limit) == data else 'DIFF'
        except ValueError as error:
            result[label] = str(error)
    print(json.dumps(result), flush=True)

# Detect the no-progress branch without an unbounded filesystem-writing loop.
data = b'X' * (extract.PART_LIMIT + 1)
start = 0
end = min(start + extract.PART_LIMIT, len(data))
if end < len(data):
    end = data.rfind(b'\n', start, end) + 1
print(json.dumps({'overlong_line_next_start': end, 'previous_start': start,
                  'progress': end > start}), flush=True)

class ProbeStop(Exception):
    pass

writes = []
def bounded_write(path, piece):
    writes.append(len(piece))
    if len(writes) == 3:
        raise ProbeStop
    return len(piece)

with patch.object(Path, 'write_bytes', bounded_write):
    try:
        extract.parts(scratch / 'overlong', 'observations.log', data)
    except ProbeStop:
        print(json.dumps({'overlong_line_actual_writer_calls': writes,
                          'stopped_by_probe': True}), flush=True)

if len(sys.argv) > 3:
    # A real published case plus ignorable diagnostic lines, partitioned as a legacy
    # packet. This exercises case(), including its unchanged original grade.
    import copy
    public = Path(sys.argv[3])
    old_path = public / 'census/answering-every-port/notice-burst-0/manifest.json'
    old = json.loads(old_path.read_text())
    observed = replay.read_parts(old_path.parent, old['extract'], extract.PART_LIMIT + 1)
    for wanted in (extract.PART_LIMIT - 1, extract.PART_LIMIT):
        packet = scratch / f'legacy-{wanted}'
        packet.mkdir(exist_ok=True)
        manifest = copy.deepcopy(old)
        listed = {}
        for key in ('group', 'stimulus', 'grade', 'extract'):
            data = replay.read_parts(old_path.parent, old[key], extract.PART_LIMIT + 1)
            if key == 'extract':
                pad = wanted - len(data)
                assert pad > 0
                data += (b'==' + b' ' * 97 + b'\n') * (pad // 100)
                if pad % 100:
                    remainder = pad % 100
                    data += b'\n' if remainder == 1 else b'==' if remainder == 2 else b'==' + b' ' * (remainder - 3) + b'\n'
                assert len(data) == wanted
            # Use the same partitioner with the legacy packet's smaller size;
            # it writes positive-progress parts for these short lines.
            with patch.object(extract, 'PART_LIMIT', 180000):
                manifest[key] = extract.parts(packet, key + '.txt', data)
            for part in manifest[key]['parts']:
                listed[part['file']] = part['sha256']
        raw = (json.dumps(manifest) + '\n').encode()
        (packet / 'manifest.json').write_bytes(raw)
        row = dict(case='boundary', manifest='manifest.json', sha256=extract.sha(raw))
        try:
            extract.case(packet, row, scratch / f'case-out-{wanted}', listed)
            result = 'complete original grade reproduced'
        except ValueError as error:
            result = str(error)
        print(json.dumps({'real_case_observation_bytes': wanted, 'extract_case': result}), flush=True)
