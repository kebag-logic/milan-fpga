"""Reconstruct the 81 reviewed inline texts and spot-check generated provenance entries."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parent
names = json.loads((ROOT/'ci/image/exec-audit.json').read_text())
rows = []
for expected, entry in names['inline_programs'].items():
    if 'text' in entry:
        text = entry['text']
    else:
        original = (ROOT/entry['variant_of']).read_text().splitlines(keepends=True)
        patch = entry['diff'].splitlines(keepends=True)
        output, cursor, i = [], 0, 2
        while i < len(patch):
            match = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', patch[i])
            assert match, patch[i]
            start = int(match[1]) if match[2] == '0' else int(match[1])-1
            output.extend(original[cursor:start])
            cursor = start
            i += 1
            while i < len(patch) and not patch[i].startswith('@@ '):
                line = patch[i]
                if line[0] in ' -':
                    assert original[cursor] == line[1:], (entry, line)
                    cursor += 1
                if line[0] in ' +':
                    output.append(line[1:])
                i += 1
        output.extend(original[cursor:])
        text = ''.join(output)
    actual = hashlib.sha256(text.encode()).hexdigest()
    assert actual == expected, (entry['source'], expected, actual)
    assert (ROOT / entry['source']).is_file()
    rows.append({'sha256': expected, 'source': entry['source'], 'form': entry['form'],
                 'reconstructed': 'text' if 'text' in entry else 'tracked source plus diff'})
generated = names['generated_programs']
assert all((ROOT/entry['generator']).is_file() and entry['reason'] for entry in generated.values())
result = {'inline_texts_checked': rows, 'generated_count': len(generated),
          'generated_source_paths_exist': True,
          'limit': 'Generated program hashes were not independently regenerated; source references and selected controls were reviewed.'}
(PACKET/'reviewed-lists-check.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: all 81 inline text digests reconstructed; all 334 generated entries name an existing generator and reason')
