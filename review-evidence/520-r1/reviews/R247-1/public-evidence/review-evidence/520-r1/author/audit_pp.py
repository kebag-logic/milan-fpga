#!/usr/bin/env python3
"""Compare retained real synthesis inputs, stat counts and cache records."""
import argparse
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    args = parser.parse_args()
    root = args.evidence.resolve()
    summary = json.loads((root/'complete.json').read_text())
    assert summary['result'] == 'PASS' and summary['source_unchanged']
    runs = root/'runs'
    names = ('01-cold','04-changed','06-changed-uncached')
    artifacts = {name:runs/(name+'.trace.artifacts') for name in names}
    staged = {name:sha(path/'KL_pp_shadow.v') for name,path in artifacts.items()}
    assert len(set(staged.values())) == 1, staged
    images = ('ltn_rom.hex','ucode.hex','gptp_ucode.hex')
    image_sha = {name:{image:sha(path/image) for image in images} for name,path in artifacts.items()}
    assert image_sha['04-changed'] == image_sha['06-changed-uncached']
    changed = [image for image in images if image_sha['01-cold'][image] != image_sha['04-changed'][image]]
    assert changed == ['ucode.hex'], changed
    assert (artifacts['04-changed']/'ucode.hex').read_bytes() == b'INVALID_ROM_DATA\n'
    cells = {name:json.loads((path/'KL_pp_shadow.stat.json').read_text())['design']['num_cells']
             for name,path in artifacts.items()}
    assert cells == {'01-cold':1141365,'04-changed':1122602,'06-changed-uncached':1122602}, cells
    evidence = dict(head=summary['head'],tree=summary['tree'],result='PASS',staged_sha256=staged,
                    image_sha256=image_sha,changed_images=changed,stat_json_cells=cells,
                    raw_yosys_log_sha256={name:sha(path/'KL_pp_shadow.yos.log') for name,path in artifacts.items()})
    (root/'raw-input-audit.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence,indent=2))


if __name__ == '__main__':
    main()
