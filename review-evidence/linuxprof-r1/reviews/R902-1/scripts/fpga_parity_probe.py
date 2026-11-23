"""Parity probe: the same one-key edits on the FPGA 1x1 config at a given tree, to tell base behaviour from new.
Usage: python3 -I fpga_parity_probe.py <tree-root> <workdir>"""
import sys
from pathlib import Path
root, work = Path(sys.argv[1]), Path(sys.argv[2]); work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / 'sw/builder'))
import yaml, endstation_builder as eb
FPGA = root / 'configs/endstation_ax7101_1x1_tdm8.yaml'
def run(tag, edit):
    doc = yaml.safe_load(FPGA.read_text()); edit(doc)
    f = work / f'{tag}.yaml'; f.write_text(yaml.safe_dump(doc, sort_keys=False))
    try:
        eb.load_config(str(f)); got = 'ACCEPT'
    except eb.ConfigError as exc: got = f'CONFIGERROR {str(exc)[:140]}'
    except Exception as exc: got = f'CRASH {type(exc).__name__}: {str(exc)[:140]}'
    print(f'{tag}: {got}')
def talker16(d):
    d['streams']['talkers'][0]['channels'] = d['audio_interface'].get('channels', 8) * 2 if isinstance(d['audio_interface'].get('channels'), int) else 16
run('clock_accuracy_x', lambda d: d.setdefault('gptp', {}).__setitem__('clock_accuracy', 'x'))
run('board_none', lambda d: d.__setitem__('board', None))
run('talker_wider_than_interface', talker16)
print('talkers:', yaml.safe_load(FPGA.read_text())['streams']['talkers'][:1], 'interface:', {k: v for k, v in yaml.safe_load(FPGA.read_text())['audio_interface'].items() if k in ('kind', 'channels')})
