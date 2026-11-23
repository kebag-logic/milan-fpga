#!/usr/bin/env python3
"""Independent host-profile boundaries and defect-detection probes.

Usage: python3 boundary_probe.py REPO PACKET
All mutations are temporary input files or in-memory substitutions.
"""
import copy
import importlib
import json
import os
from pathlib import Path
import subprocess
import struct
import sys
import tempfile

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
os.chdir(repo)
tempfile.tempdir = str(packet / 'scratch')
sys.path.insert(0, str(repo / 'sw/builder'))
import endstation_builder as eb
import test_builder as tb
import yaml

source = repo / 'configs/host/endstation_host_example.yaml'
base = yaml.safe_load(source.read_text())
rows = []

def check(path, value, accept, delete=False, image=False):
    doc = copy.deepcopy(base)
    keys = path.split('.')
    node = doc
    for key in keys[:-1]:
        node = node.setdefault(key, {})
    if delete:
        node.pop(keys[-1])
    else:
        node[keys[-1]] = value
    with tempfile.TemporaryDirectory(prefix='boundary-') as directory:
        config = Path(directory) / 'host.yaml'
        config.write_text(yaml.safe_dump(doc))
        try:
            cfg = eb.load_config(str(config))
            if image:
                overlay = eb.emit_aem_overlay(cfg)
                blob = eb._entity_model_image(cfg, overlay)['aem_desc.bin']
                avb = tb.image_descriptor(blob, 9)
                for key, offset, width in tb.AVB_INTERFACE_GPTP_FIELDS:
                    assert int.from_bytes(avb[offset:offset+width], 'big') == cfg['gptp'][key] % (1 << (8*width))
            outcome, reason = 'accepted', ''
        except eb.ConfigError as error:
            outcome, reason = 'refused', str(error)
        assert (outcome == 'accepted') == accept, (path, value, outcome, reason)
        rows.append(dict(path=path, value=value, delete=delete, outcome=outcome, reason=reason))

for key in eb.HOST_GPTP_STATED:
    check('gptp.' + key, None, False, delete=True)
for key, low, high in [('port_number',1,65534), ('priority1',0,255), ('priority2',0,255),
                      ('clock_class',0,255), ('offset_scaled_log_variance',0,65535),
                      ('log_sync_interval',-128,127), ('log_announce_interval',-128,127),
                      ('log_pdelay_interval',-128,127)]:
    for value in (low,high):
        check('gptp.' + key, value, True, image=True)
    for value in (low-1,high+1,True,'1',1.5):
        check('gptp.' + key, value, False)
for key, good, bad in [
    ('board.constraints.link_mbps', [100,1000], [0,10,10000,True,'1000']),
    ('board.constraints.num_queues', [5,8], [0,9,True,'5']),
    ('audio_interface.channels', [1,32], [0,33,True,'8']),
    ('gptp.clock_accuracy', [0x20,0x31,0xFE], [0x1F,0x32,0x7F,0x80,0xFD,0xFF]),
]:
    for value in good:
        check(key, value, True)
    for value in bad:
        check(key, value, False)

# Demonstrate that the new input refusal test fails when a real guard is lost.
real = eb._load_host_board
def bypass_owner(cfg, path, control):
    cfg = copy.deepcopy(cfg)
    cfg['board']['gptp_owner'] = 'host-phc'
    return real(cfg, path, control)
eb._load_host_board = bypass_owner
try:
    try:
        tb.test_host_profile_refusals()
    except AssertionError as error:
        rows.append(dict(mutation='bypass required/valid host gptp_owner', killed=True, reason=str(error)))
    else:
        raise AssertionError('new refusal gate survived removal of owner validation')
finally:
    eb._load_host_board = real

# Demonstrate the existing packer lint executes on a host input, beyond loader checks.
cfg = eb.load_config(str(source))
overlay = eb.emit_aem_overlay(cfg)
blob = eb._entity_model_image(cfg, overlay)['aem_desc.bin']
for case in tb._image_contract_cases(blob):
    tb._assert_image_contract_case(cfg, overlay, case)
    rows.append(dict(image_lint_case=case[0], outcome=case[3] or 'accepted'))
tb._assert_image_presence(lambda: eb._entity_model_image(cfg, overlay)['aem_desc.bin'], 'host profile')
rows.append(dict(image_lint_presence='missing AUDIO_UNIT and CLOCK_DOMAIN refused'))

# Decode directly the first user's stream inventory and mandatory Configuration.
configuration = tb.image_descriptor(blob, 1)
decoded = []
def descriptor(kind, index):
    # Pinned packer section 07: consecutive equal-length runs share a type;
    # the consumer accumulates their counts to resolve the global index.
    entries = struct.unpack_from('>H', blob, 8)[0]
    offset = struct.unpack_from('>I', blob, 12)[0]
    first = 0
    for number in range(entries):
        config, dtype, count, size, data, names, stride = struct.unpack_from('>HHHHIHH', blob, offset+16*number)
        if (config, dtype) != (0,kind):
            continue
        if first <= index < first+count:
            start = data + (index-first)*stride
            return blob[start:start+size]
        first += count
    raise AssertionError((kind,index,'not found'))
for kind, index in [(5,0),(5,1),(6,0)]:
    desc = descriptor(kind, index)
    decoded.append(dict(type=kind,index=index,current_format=desc[74:82].hex(),length=len(desc)))
assert len(configuration) >= 74
assert [d['current_format'] for d in decoded] == ['0205022002006000','041060010000bb80','0205022002006000'], decoded
rows.append(dict(image_bytes=len(blob), configuration_bytes=len(configuration), streams=decoded))
(packet / 'boundary-result.json').write_text(json.dumps(rows, indent=2) + '\n')
print('PASS',len(rows),'boundary and mutation observations')
