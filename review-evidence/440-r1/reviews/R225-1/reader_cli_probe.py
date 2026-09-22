"""Actual gen_toc CLI line-ending/refusal probes in an isolated script tree."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

OUT = Path(__file__).resolve().parent
results = []
with tempfile.TemporaryDirectory(prefix='r225-reader-cli-') as tmp:
    root = Path(tmp)
    shutil.copytree(OUT / 'snapshots/head/scripts', root / 'scripts')
    for ident, prefix, expected in [
        ('crlf', '```\r\n```\r\n', 'NO TOC'),
        ('cr', '```\r```\r', 'NO TOC'),
        ('html-crlf', '<pre>\r\n</style>\r\n', 'NO TOC'),
        ('html-cr', '<pre>\r</style>\r', 'NO TOC'),
        ('nbsp', '```\n```\u00a0\n', 'NOT READ'),
        ('ff', '~~~\n~~~\f\n', 'NOT READ'),
        ('inner-space', '<pre>\n</pre >\n', 'below the 3-section'),
        ('inner-cr', '<pre>\n</pre\r>\n', 'below the 3-section'),
    ]:
        page = root / (ident + '.md')
        page.write_bytes(('# Page\n\n' + prefix + '## Alpha\n\n## Beta\n\n## Gamma\n\n## Delta\n').encode())
        command = ['python3', '-B', str(root / 'scripts/gen_toc.py'), '--check', str(page)]
        proc = subprocess.run(command, capture_output=True, text=True)
        expected_exit = 1 if expected == 'NO TOC' else 0
        passed = expected in proc.stdout and proc.returncode == expected_exit
        results.append(dict(id=ident, source=page.read_bytes().decode(), command=command,
                            exit=proc.returncode, stdout=proc.stdout, stderr=proc.stderr, pass_=passed))
(OUT / 'reader-cli.json').write_text(json.dumps(results, indent=2) + '\n')
assert all(r['pass_'] for r in results), results
print('Actual generator CLI:', len(results), 'reader/refusal cases PASS')
