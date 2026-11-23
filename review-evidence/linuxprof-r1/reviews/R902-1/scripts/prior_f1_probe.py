"""Prior finding R900-1-F1 check: a board of [], "" or ["ax7101"] on the FPGA 1x1 must refuse through ConfigError.
Usage: python3 -I prior_f1_probe.py <tree-root> <workdir>"""
import sys
from pathlib import Path
root, work = Path(sys.argv[1]), Path(sys.argv[2]); work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / 'sw/builder'))
import yaml, endstation_builder as eb
src = yaml.safe_load((root / 'configs/endstation_ax7101_1x1_tdm8.yaml').read_text())
for i, v in enumerate(([], '', ['ax7101'])):
    f = work / f'b{i}.yaml'; f.write_text(yaml.safe_dump({**src, 'board': v}, sort_keys=False))
    try: eb.load_config(str(f)); got = 'ACCEPT'
    except eb.ConfigError as e: got = f'ConfigError: {e}'
    except Exception as e: got = f'{type(e).__name__}: {e}'
    print(f'board={v!r}: {got}')
