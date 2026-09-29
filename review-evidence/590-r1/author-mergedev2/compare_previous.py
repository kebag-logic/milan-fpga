"""Compare this round's native evidence with the previous merge-dev round's, byte for byte.

Both packets are rebuilt from their retained artifacts (each checked against its
stored and raw SHA-256). The previous round ran at `1f039cfe` with the processor
at `16be6768` and reproduced round 3 byte for byte. Service runs compare raw
logs, graded receipt fields and the bound build and measurement-input hashes;
capture arms compare raw logs, graded measurements and source lists. Every
bound repository input is also checked against the dev parent `b5c0f69d` (the
artifact-identity baseline), and every one that moved since `1f039cfe` must be
in the change set between the two heads.
"""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess

out = Path(__file__).parent
previous = Path('$MANAGEMENT/2026-09-23/590-a422')
root = Path('$LANES/590-592-599-firmware')
scratch = {out: '$VALIDATION_STORAGE/590-a430/native/', previous: '$VALIDATION_STORAGE/590-a422/native/'}
OLD_HEAD, DEV = '1f039cfe86d5337f5c9b7248696dba1c4bdda67e', 'b5c0f69d5d11f0ec4bc847a2cfdd13e89e199a8a'
SUBMODULES = ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'external')


def git(*args, cwd=root):
    return subprocess.check_output(['git', *args], cwd=cwd, stderr=subprocess.DEVNULL)


head = git('rev-parse', 'HEAD').decode().strip()
assert not git('status', '--porcelain').strip()
assert Path(git('rev-parse', '--show-toplevel', cwd=root / 'protocol-processor').decode().strip()) == root / 'protocol-processor'


def pin(commit, module):
    return git('ls-tree', commit, module).decode().split()[2]


def blob_sha256(commit, path):
    """SHA-256 of a tracked file at a parent commit, following submodule pins; None if untracked."""
    for module in SUBMODULES:
        if path.startswith(module + '/'):
            cwd, rev, rel = root / module, pin(commit, module), path[len(module) + 1:]
            break
    else:
        cwd, rev, rel = root, commit, path
    try:
        return hashlib.sha256(git('cat-file', 'blob', f'{rev}:{rel}', cwd=cwd)).hexdigest()
    except subprocess.CalledProcessError:
        return None


changed = set(git('diff', '--name-only', OLD_HEAD, head).decode().split())
for module in SUBMODULES:
    if module in changed:
        changed.discard(module)
        names = git('diff', '--name-only', pin(OLD_HEAD, module), pin(head, module), cwd=root / module).decode().split()
        changed |= {module + '/' + name for name in names}


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
    return path.replace(scratch[packet], '<build>/').replace(str(root) + '/', '')


def differing(old, new):
    return sorted(key for key in set(old) | set(new) if old.get(key) != new.get(key))


def repository_inputs(hashes):
    """Check every bound repository input against the head and the dev parent."""
    tracked = {key: value for key, value in hashes.items()
               if not key.startswith('build/') and blob_sha256(head, key) is not None}
    at_dev = {key: blob_sha256(DEV, key) for key in tracked}
    return dict(tracked=len(tracked),
                not_equal_to_head=sorted(k for k, v in tracked.items() if blob_sha256(head, k) != v),
                absent_at_dev_parent=sorted(k for k in tracked if at_dev[k] is None),
                differing_from_dev_parent=sorted(k for k, v in tracked.items()
                                                 if at_dev[k] is not None and at_dev[k] != v),
                untracked=sorted(k for k in hashes if not k.startswith('build/') and k not in tracked))


old, new = load(previous), load(out)
report = dict(head=head, previous_packet='590-a422', previous_head=OLD_HEAD, dev_parent=DEV,
              changed_since_previous=sorted(changed), service=[], capture=[])
graded = ('media', 'rows', 'events', 'heartbeat_max_gap_ms', 'heartbeat_500ms_met', 'budget_findings',
          'heartbeat', 'liveness', 'phy', 'service_findings', 'shape', 'cpu_hz', 'sys_hz',
          'device_wait_us', 'program_wait_us')
services = sorted(name[:-len('-spec.json')] for name in new if name.startswith('service-')
                  and name.endswith('-spec.json'))
assert len(services) == 16, services
for name in services:
    row = dict(name=name, raw_log_sha256=digest(new[name + '-raw.log']),
               previous_raw_log_sha256=digest(old[name + '-raw.log']))
    row['raw_log_identical'] = new[name + '-raw.log'] == old[name + '-raw.log']
    if name + '-receipt.json' in new:
        a, b = json.loads(old[name + '-receipt.json']), json.loads(new[name + '-receipt.json'])
        assert sorted(a) == sorted(b), name
        row['graded_fields_differing'] = [key for key in graded if a.get(key) != b.get(key)]
        row['build_hashes_differing'] = differing(a['build_hashes'], b['build_hashes'])
        row['input_hashes_differing'] = differing(a['input_hashes'], b['input_hashes'])
        row['moved_repository_inputs_outside_change_set'] = sorted(
            key for key in row['build_hashes_differing'] + row['input_hashes_differing']
            if not key.startswith('build/') and key not in changed)
        row['build_inputs'] = repository_inputs(b['build_hashes'])
        row['measurement_inputs'] = repository_inputs(b['input_hashes'])
    else:
        row['receipt'] = 'none: no-publish returns before a receipt, by design'
    sa, sb = json.loads(old[name + '-spec.json']), json.loads(new[name + '-spec.json'])
    row['spec_build_hashes_differing'] = differing(sa.get('build_hashes', {}), sb.get('build_hashes', {}))
    row['spec_fields_differing'] = [key for key in sorted(set(sa) | set(sb)) if key != 'build_hashes'
                                    and json.dumps(sa.get(key)).replace(scratch[previous], '<build>/')
                                    != json.dumps(sb.get(key)).replace(scratch[out], '<build>/')]
    report['service'].append(row)
receipt = json.loads((root / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
controls = ('capture-byte-only', 'capture-skip-copy', 'capture-no-traffic')
arms = sorted(name[:-len('-sources.json')] for name in new if name.startswith('capture-')
              and name.endswith('-sources.json'))
assert len(arms) == 9, arms
for name in arms:
    row = dict(name=name, raw_log_sha256=digest(new[name + '-raw.log']),
               previous_raw_log_sha256=digest(old[name + '-raw.log']))
    row['raw_log_identical'] = new[name + '-raw.log'] == old[name + '-raw.log']
    if name + '.json' in new:
        a, b = json.loads(old[name + '.json']), json.loads(new[name + '.json'])
        row['measurement_fields_differing'] = differing(a, b)
        row['measurement_identical'] = old[name + '.json'] == new[name + '.json']
        row['maximum_ms'], row['previous_maximum_ms'] = b['maximum_ms'], a['maximum_ms']
    sa, sb = json.loads(old[name + '-sources.json']), json.loads(new[name + '-sources.json'])
    la = [relative(path, previous) for path in sa['sources'] + sa['includes']]
    lb = [relative(path, out) for path in sb['sources'] + sb['includes']]
    row['source_count'] = len(sb['sources'])
    row['source_and_include_lists_identical'] = la == lb
    row['sources_changed_since_previous'] = sorted(path for path in lb if path in changed)
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
(out / 'previous-comparison.json').write_text(json.dumps(report, indent=2) + '\n')
print('changed since previous:', len(changed), 'paths')
for row in report['service'] + report['capture']:
    flags = {key: value for key, value in row.items() if key.endswith('differing') or key.endswith('identical')
             or key.endswith('outside_change_set') or key == 'sources_changed_since_previous'}
    for key in ('build_inputs', 'measurement_inputs'):
        if key in row:
            flags[key] = {k: v for k, v in row[key].items() if k != 'tracked'}
    print(row['name'], json.dumps(flags))
