"""Compare this round's merge-head native evidence with the round-3 evidence, byte for byte.

Both packets are rebuilt from their retained artifacts (each checked against its
stored and raw SHA-256). Service runs compare raw logs, graded receipt fields,
and the bound build and measurement-input hashes. Capture arms compare raw logs,
graded measurements and the source lists. The merge-head capture builds are
also checked against every identity the committed capture receipt binds.
"""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess

out = Path(__file__).parent
round3 = Path('$MANAGEMENT/2026-09-23/590-a411')
root = Path('$LANES/590-592-599-firmware')
scratch = {out: '$VALIDATION_STORAGE/590-a422/native/', round3: '$VALIDATION_STORAGE/590-a411/'}
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
changed = set(subprocess.check_output(['git', 'diff', '--name-only', '93262f25', '9e3df3ed'],
                                      cwd=root, text=True).split())


def load(packet):
    result = {}
    for item in json.loads((packet / 'native-artifacts.json').read_text()):
        parts = []
        for stored in item['stored']:
            raw = (packet / stored['path']).read_bytes()
            assert len(raw) == stored['size'] and hashlib.sha256(raw).hexdigest() == stored['sha256']
            parts.append(raw)
        body, name = b''.join(parts), item['name']
        if name.endswith('.gz'):
            body, name = gzip.decompress(body), name[:-3]
        assert len(body) == item['raw_size'] and hashlib.sha256(body).hexdigest() == item['raw_sha256']
        assert name not in result, name
        result[name] = body
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(path, packet):
    path = path.replace(scratch[packet], '<build>/')
    return path.replace(str(root) + '/', '')


def differing(old, new):
    return sorted(key for key in set(old) | set(new) if old.get(key) != new.get(key))


old, new = load(round3), load(out)
report = dict(head=head, round3_packet='590-a411', service=[], capture=[])
graded = ('media', 'rows', 'events', 'heartbeat_max_gap_ms', 'heartbeat_500ms_met', 'budget_findings',
          'heartbeat', 'liveness', 'phy', 'service_findings', 'shape', 'cpu_hz', 'sys_hz',
          'device_wait_us', 'program_wait_us')
services = sorted(name[:-len('-spec.json')] for name in new if name.startswith('service-')
                  and name.endswith('-spec.json'))
assert len(services) == 16, services
for name in services:
    row = dict(name=name, raw_log_sha256=digest(new[name + '-raw.log']),
               round3_raw_log_sha256=digest(old[name + '-raw.log']))
    row['raw_log_identical'] = new[name + '-raw.log'] == old[name + '-raw.log']
    if name + '-receipt.json' in new:
        a, b = json.loads(old[name + '-receipt.json']), json.loads(new[name + '-receipt.json'])
        row['receipt_keys'] = sorted(b)
        assert sorted(a) == sorted(b), name
        row['graded_fields_differing'] = [key for key in graded if a.get(key) != b.get(key)]
        row['build_hashes_differing'] = differing(a['build_hashes'], b['build_hashes'])
        row['input_hashes_differing'] = differing(a['input_hashes'], b['input_hashes'])
    else:
        row['receipt'] = 'none: no-publish returns before a receipt, by design'
    sa, sb = json.loads(old[name + '-spec.json']), json.loads(new[name + '-spec.json'])
    row['spec_build_hashes_differing'] = differing(sa.get('build_hashes', {}), sb.get('build_hashes', {}))
    row['spec_fields_differing'] = [key for key in sorted(set(sa) | set(sb)) if key != 'build_hashes'
                                    and json.dumps(sa.get(key)).replace(scratch[round3], '<build>/')
                                    != json.dumps(sb.get(key)).replace(scratch[out], '<build>/')]
    row['build_hashes_all_changed_by_merge'] = set(row['spec_build_hashes_differing']) <= changed
    report['service'].append(row)
controls = {'capture-byte-only': ('capture-byte-only-capture.log', 'capture-byte-only-measurement.json'),
            'capture-skip-copy': ('capture-skip-copy-capture.log', None),
            'capture-no-traffic': ('capture-no-traffic-capture.log', 'capture-no-traffic-measurement.json')}
receipt = json.loads((root / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
arms = sorted(name[:-len('-sources.json')] for name in new if name.startswith('capture-')
              and name.endswith('-sources.json'))
assert len(arms) == 9, arms
for name in arms:
    old_log, old_json = controls.get(name, (name + '-raw.log', name + '.json'))
    row = dict(name=name, raw_log_sha256=digest(new[name + '-raw.log']),
               round3_raw_log_sha256=digest(old[old_log]))
    row['raw_log_identical'] = new[name + '-raw.log'] == old[old_log]
    if old_json is not None:
        a, b = json.loads(old[old_json]), json.loads(new[name + '.json'])
        row['measurement_fields_differing'] = differing(a, b)
        row['maximum_ms'], row['round3_maximum_ms'] = b['maximum_ms'], a['maximum_ms']
    sa, sb = json.loads(old[name + '-sources.json']), json.loads(new[name + '-sources.json'])
    la = [relative(path, round3) for path in sa['sources'] + sa['includes']]
    lb = [relative(path, out) for path in sb['sources'] + sb['includes']]
    row['source_count'] = len(sb['sources'])
    row['source_and_include_lists_identical'] = la == lb
    row['sources_changed_by_merge'] = sorted(path for path in lb if path in changed)
    row['spec_fields_differing'] = [key for key in differing(sa, sb) if key not in ('sources', 'includes')]
    if name not in controls:
        build = Path(scratch[out] + name)
        spec = json.loads(new[name + '-sources.json'])
        committed = [arm for arm in receipt['measurements'] if (arm['shape'], arm['cpu_hz'], arm['traffic'])
                     == (spec['shape'], spec['cpu_hz'], spec['traffic'])]
        assert len(committed) == 1, name
        committed = committed[0]
        cpu = [Path(path) for path in spec['sources'] if Path(path).name.startswith('VexiiRiscvLitex_')]
        assert len(cpu) == 1
        identities = dict(cpu_netlist_sha256=digest(cpu[0].read_bytes()),
                          instrumented_firmware_sha256=digest((build / 'measurement_firmware/milan_baremetal.c').read_bytes()),
                          bios_sha256=digest((build / 'software/bios/bios.bin').read_bytes()),
                          gptp_ucode_sha256=digest((build / 'generated' / spec['shape'] / 'gptp_ucode.hex').read_bytes()),
                          config_sha256=digest((root / 'configs' / (spec['shape'] + '.yaml')).read_bytes()))
        row['receipt_identities_differing'] = [key for key, value in identities.items() if committed[key] != value]
        row['receipt_graded_fields_differing'] = [key for key in b if committed.get(key) != b[key]]
    report['capture'].append(row)
(out / 'round3-comparison.json').write_text(json.dumps(report, indent=2) + '\n')
for row in report['service'] + report['capture']:
    flags = {key: value for key, value in row.items() if key.endswith('differing') or key.endswith('identical')
             or key == 'sources_changed_by_merge'}
    print(row['name'], json.dumps(flags))
