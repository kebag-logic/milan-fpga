"""Reviewer probes of the host profile's loaders: each row edits the annotated host example (or the FPGA 1x1) at
one key and records whether load_config accepts it, refuses it with ConfigError, or raises anything else.
Usage: python3 -I host_robustness_probe.py <tree-root> <workdir>"""
import copy, sys, tempfile, traceback
from pathlib import Path
root, work = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / 'sw/builder'))
import yaml, endstation_builder as eb
HOST = root / 'configs/host/endstation_host_example.yaml'
FPGA = root / 'configs/endstation_ax7101_1x1_tdm8.yaml'
DEL = object()
def put(doc, path, value):
    *head, last = path.split('.')
    for k in head:
        doc = doc[int(k)] if isinstance(doc, list) else doc.setdefault(k, {})
    if value is DEL:
        doc.pop(last, None)
    elif isinstance(doc, list):
        doc[int(last)] = value
    else:
        doc[last] = value
ROWS = [  # (base, path, value, expectation)
    ('host', None, None, 'accept'),
    ('host', 'clocking.crf_sink', False, 'refuse: AAF talker needs a CRF input (Milan v1.2 7.2.2)'),
    ('host', 'streams.listeners', [{'name': 'A', 'channels': 8}, {'name': 'B', 'channels': 8}], 'refuse: 2 AAF inputs need a CRF output (7.2.3)'),
    ('host', 'gptp', None, 'refuse'),
    ('host', 'gptp', [], 'refuse'),
    ('host', 'gptp.priority1', True, 'refuse'),
    ('host', 'gptp.priority1', 256, 'refuse'),
    ('host', 'gptp.port_number', 0, 'refuse'),
    ('host', 'gptp.port_number', 0xFFFF, 'refuse'),
    ('host', 'gptp.domain', 1, 'refuse (Milan domain 0) or as FPGA'),
    ('host', 'gptp.domain', DEL, 'accept (domain defaults as FPGA)'),
    ('host', 'gptp.clock_accuracy', 'x', 'refuse'),
    ('host', 'gptp.log_sync_interval', 1.5, 'refuse'),
    ('host', 'gptp.ingress_latency_ns', 10, 'refuse'),
    ('host', 'board.gptp_owner', 'fabric', 'refuse'),
    ('host', 'board.gptp_owner', DEL, 'refuse'),
    ('host', 'board.gptp_owner', ['host-phc'], 'refuse'),
    ('host', 'board.features', {'fabric_gptp': True}, 'refuse'),
    ('host', 'board.constraints', None, 'refuse'),
    ('host', 'board.constraints.link_mbps', 10, 'refuse'),
    ('host', 'board.constraints.link_mbps', True, 'refuse'),
    ('host', 'board.constraints.num_queues', 0, 'refuse'),
    ('host', 'board.constraints.num_queues', True, 'refuse'),
    ('host', 'board.constraints.sys_clk_hz', 100000000, 'refuse'),
    ('host', 'soc', {}, 'refuse'),
    ('host', 'control.placement', 'all-fabric', 'refuse'),
    ('host', 'control', DEL, 'refuse or default'),
    ('host', 'audio_interface.kind', 'tdm8', 'refuse'),
    ('host', 'audio_interface.channels', 0, 'refuse'),
    ('host', 'audio_interface.channels', 33, 'refuse'),
    ('host', 'audio_interface.channels', True, 'refuse'),
    ('host', 'audio_interface.channels', DEL, 'refuse'),
    ('host', 'audio_interface.word_length_bits', 20, 'refuse'),
    ('host', 'audio_interface.cluster_mapping', {'policy': 'role-pools'}, 'refuse'),
    ('host', 'streams.talkers.0.channels', 16, 'refuse (wider than interface) or as FPGA'),
    ('host', 'streams.talkers', [], 'as FPGA'),
    ('host', 'board.target', 'HOST', 'refuse'),
    ('host', 'board', None, 'refuse'),
    ('host', 'board', 7, 'refuse'),
    ('fpga', None, None, 'accept'),
    ('fpga', 'board.gptp_owner', 'host-phc', 'refuse'),
    ('fpga', 'board.target', 'host', 'refuse'),
    ('fpga', 'board.features.fabric_gptp', False, 'refuse'),
    ('fpga', 'gptp', DEL, 'refuse'),
    ('fpga', 'audio_interface.kind', 'usb_audio', 'refuse'),
    ('fpga', 'board', None, 'base behaviour'),
]
work.mkdir(parents=True, exist_ok=True)
bad = 0
for i, (base, path, value, want) in enumerate(ROWS):
    doc = yaml.safe_load((HOST if base == 'host' else FPGA).read_text())
    if path is not None:
        put(doc, path, value if value is DEL else copy.deepcopy(value))
    f = work / f'row{i:02d}.yaml'
    f.write_text(yaml.safe_dump(doc, sort_keys=False))
    try:
        eb.load_config(str(f)); got = 'ACCEPT'
    except eb.ConfigError as exc:
        got = f'CONFIGERROR {str(exc)[:150]}'
    except Exception as exc:
        got = f'CRASH {type(exc).__name__}: {str(exc)[:150]}'
    v = 'OK' if (want.startswith('accept') == (got == 'ACCEPT')) and not got.startswith('CRASH') else 'CHECK'
    if want.startswith(('as FPGA', 'base', 'refuse or', 'refuse (')): v = 'INFO' if not got.startswith('CRASH') else 'CHECK'
    bad += v == 'CHECK'
    shown = '<deleted>' if value is DEL else repr(value)
    print(f'{v:5} {base:4} {path}={shown} | want {want} | got {got}')
print(f'rows {len(ROWS)}, CHECK {bad}')
