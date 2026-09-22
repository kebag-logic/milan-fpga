"""Independent R225 mutations, applied only to disposable copies."""
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

OUT = Path(__file__).resolve().parent
SCRIPTS = OUT / 'snapshots/head/scripts'
source = (SCRIPTS / 'gen_toc.py').read_text()
end = 'return bool(re.search(r"</(?:%s)>" % "|".join(RAW_HTML_TAGS), line, ASCII_FOLD))'
trailer = 'and not m.group(2).strip(CLASSES["blank"]):  # CommonMark 4.5 trailer'
mutants = {
    'fence-python-strip': source.replace(trailer, 'and not m.group(2).strip():  # mutant'),
    'fence-no-tab': source.replace(trailer, 'and not m.group(2).strip(" "):  # mutant'),
    'inner-blank': source.replace(end, end.replace('(?:%s)>', '(?:%s)\\s*>')),
    'unicode-fold': source.replace(end, end.replace('ASCII_FOLD', 're.IGNORECASE')),
    'case-sensitive': source.replace(end, end.replace('ASCII_FOLD', 're.ASCII')),
    'no-later-close': source.replace('TEXT if _type_1_end(line) else HTML', 'TEXT if False else HTML'),
    'no-opening-close': source.replace('closed = _type_1_end(line)', 'closed = False'),
    'only-line-start': source.replace(end, end.replace('r"</', 'r"^</')),
    'drop-style-close': source.replace(end, end.replace('"|".join(RAW_HTML_TAGS)', '"pre|script|textarea"')),
    'matching-name-only': source.replace('def _type_1_end(line: str)', 'def _type_1_end(line: str, tag: str)')
        .replace('_type_1_end(line)', '_type_1_end(line, tag)')
        .replace(end, 'return bool(re.search(r"</%s>" % tag, line, ASCII_FOLD))'),
    'exact-fence-length': source.replace('len(m.group(1)) >= len(delim)', 'len(m.group(1)) == len(delim)'),
}
records = []
for name, mutated in mutants.items():
    assert mutated != source, name
    dest = OUT / 'mutations' / name
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'change.patch').write_text(''.join(difflib.unified_diff(source.splitlines(True), mutated.splitlines(True),
        fromfile='head/scripts/gen_toc.py', tofile='mutant/scripts/gen_toc.py')))
    with tempfile.TemporaryDirectory(prefix='r225-mutation-') as tmp:
        scripts = Path(tmp) / 'scripts'
        shutil.copytree(SCRIPTS, scripts)
        (scripts / 'gen_toc.py').write_text(mutated)
        outcomes = {}
        for script in ['gen_toc.py', 'check_em_dash.py']:
            proc = subprocess.run(['python3', '-B', str(scripts / script), '--selftest'], capture_output=True, text=True)
            (dest / (script + '.stdout')).write_text(proc.stdout)
            (dest / (script + '.stderr')).write_text(proc.stderr)
            behavior = [line for line in (proc.stdout + proc.stderr).splitlines() if 'I440' in line]
            outcomes[script] = dict(exit=proc.returncode, i440_failures=behavior)
        records.append(dict(mutant=name, results=outcomes))
        print(name, {k: (v['exit'], len(v['i440_failures'])) for k, v in outcomes.items()}, flush=True)
(OUT / 'mutations.json').write_text(json.dumps(records, indent=2) + '\n')
# The final mutation is exploratory: fence length is unchanged by issue 440.
# Its survival is recorded as optional coverage hardening, not an AC failure.
assert all(r['results']['gen_toc.py']['exit'] != 0 for r in records if r['mutant'] != 'exact-fence-length')
assert all(r['results']['gen_toc.py']['i440_failures'] for r in records if r['mutant'] != 'exact-fence-length')
assert (SCRIPTS / 'gen_toc.py').read_text() == source
print('Source snapshot unchanged:', hashlib.sha256(source.encode()).hexdigest())
