"""Compare all five packed images against the assigned base without another checkout."""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import types

ROOT = Path('$LANES/577-image-l6-l10')
BASE = '54ce877371ee6e8878cf67294e86c2a8481b62f6'
sys.path.insert(0, str(ROOT / 'sw/builder'))
import test_builder as test
source = subprocess.check_output(['git', 'show', BASE + ':sw/builder/endstation_builder.py'],
                                 cwd=ROOT, text=True)
baseline = types.ModuleType('baseline_builder')
baseline.__file__ = str(ROOT / 'sw/builder/endstation_builder.py')
sys.modules[baseline.__name__] = baseline
exec(compile(source, baseline.__file__, 'exec'), baseline.__dict__)
results = []
for name, path in test.CONFIGS.items():
    before_config = baseline.load_config(path)
    before = baseline._entity_model_image(before_config, baseline.emit_aem_overlay(before_config))['aem_desc.bin']
    config = test.eb.load_config(path)
    image = test.eb._entity_model_image(config, test.eb.emit_aem_overlay(config))['aem_desc.bin']
    assert before == image, name + ': shipping image changed'
    audio = test.image_descriptor(image, 0x0002)
    domain = test.image_descriptor(image, 0x0024)
    rate_offset, rate_count = struct.unpack_from('>HH', audio, 140)
    source_offset, source_count = struct.unpack_from('>HH', domain, 72)
    row = dict(configuration=name, bytes=len(image), sha256=hashlib.sha256(image).hexdigest(),
               base_equal=True, rates_offset=rate_offset, rates_count=rate_count,
               audio_unit_bytes=len(audio),
               rates=list(struct.unpack_from(f'>{rate_count}I', audio, rate_offset)),
               sources_offset=source_offset, sources_count=source_count,
               clock_domain_bytes=len(domain),
               sources=list(struct.unpack_from(f'>{source_count}H', domain, source_offset)))
    results.append(row)
    print(json.dumps(row))
Path(__file__).with_name('images.json').write_text(json.dumps(results, indent=2) + '\n')
