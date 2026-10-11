from pathlib import Path
import importlib
import inspect
import json
import sys
sys.dont_write_bytecode = True
root = Path('$LANES/pp73-command-model')
out = Path('$VALIDATION_STORAGE/pp73-a595/r3')
sys.path.insert(0, str(root / 'scripts'))
registry = json.loads((root / 'hdl/aecp/ucode/aecp_fields.json').read_text())
lines = ['field\tstatus\tconsumer locations\tcheck\tscope']
plants = ['group\tplanted drift\tfailing gate words']
for entry in registry:
    locations = []
    for consumer in entry.get('consumer', '').split(';'):
        if consumer.strip():
            module, symbol = consumer.strip().split('.')
            fn = getattr(importlib.import_module('aecp_gate.' + module), symbol)
            path = Path(inspect.getsourcefile(fn)).relative_to(root)
            locations.append(f'{path}:{inspect.getsourcelines(fn)[1]}')
    lines.append('\t'.join([entry['path'], entry['status'], '; '.join(locations),
                            entry.get('check', ''), entry['reason']]))
    if entry['status'] == 'held':
        plants.append('\t'.join(['registry', entry['path'], '; '.join(entry['probe']['words'])]))
for module, names in [('plants',['MUTANTS']), ('field_plants',['MUTANTS']),
                      ('selftest',['OBSERVED_MUTANTS','FILE_MUTANTS','GENERATOR_MUTANTS'])]:
    mod = importlib.import_module('aecp_gate.' + module)
    for name in names:
        for what, _, words in getattr(mod, name):
            plants.append('\t'.join([module + '.' + name, what, '; '.join(words)]))
(out / 'consumer-locations.tsv').write_text('\n'.join(lines) + '\n')
(out / 'planted-drifts.tsv').write_text('\n'.join(plants) + '\n')
print(len(lines) - 1, 'fields;', len(plants) - 1, 'named planted drifts')
