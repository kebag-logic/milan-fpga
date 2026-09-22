"""R225 public-evidence replay and independent boundary probes. No product writes."""
import ast
import collections
import concurrent.futures
import hashlib
from html.parser import HTMLParser
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.request

OUT = Path(__file__).resolve().parent
REPO = Path('$VALIDATION_STORAGE/reviews/r225-507-r1')
BASE = 'b17580b91deb11f3441dfc5d7f9fafe539d929b8'
HEAD = '0d43ff25d38917e77bb5c3d2ddb6473013cea3ba'
ARCHIVE = 'ada8bf7b1cb74cc89e5a451bb2dcd659722ffa28'
FILES = ['gen_toc.py', 'gen_toc_cases.py', 'gen_toc_guards.py',
         'check_em_dash.py', 'gen_toc_closer_cases.py']

def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=True) + '\n')

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])

class HTMLHeadings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h2 = 0
    def handle_starttag(self, tag, attrs):
        self.h2 += tag == 'h2'

def count_html(data):
    parser = HTMLHeadings()
    parser.feed(data.decode())
    return parser.h2

def setup():
    for version, rev in [('base', BASE), ('head', HEAD)]:
        dest = OUT / 'snapshots' / version / 'scripts'
        dest.mkdir(parents=True, exist_ok=True)
        for name in FILES:
            if version == 'base' and name == 'gen_toc_closer_cases.py':
                continue
            (dest / name).write_bytes(git('show', f'{rev}:scripts/{name}'))
    fixtures = json.loads((OUT / 'public-evidence/author/fixtures.json').read_text())
    def fetch(row):
        path = f'review-evidence/440-r1/author/renderer/{row["id"]}/response.html'
        data = urllib.request.urlopen(f'https://raw.githubusercontent.com/kebag-logic/milan-fpga/{ARCHIVE}/{path}').read()
        dest = OUT / 'public-renderer' / row['id']
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'response.html').write_bytes(data)
        return dict(id=row['id'], url=f'https://github.com/kebag-logic/milan-fpga/blob/{ARCHIVE}/{path}',
                    sha256=hashlib.sha256(data).hexdigest(), h2=count_html(data))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(fetch, fixtures))
    save('public-renderer-index.json', results)
    (OUT / 'candidate.diff').write_bytes(git('diff', BASE, HEAD))
    print('Saved exact source snapshots and', len(results), 'public HTML responses', flush=True)

def independent_rows():
    rows = []
    def add(name, source, expected):
        rows.append(dict(id=name, source=source, expected=expected))
    # Explicit grammar expectations, independent of candidate constants and tests.
    trailers = ['', ' ', '\t', ' \t ', 'x', '\f', '\u00a0', '`', '~', ' x', ' \tX']
    for marker in ['`', '~']:
        for opening in [3, 4, 7]:
            for closing in [2, 3, 4, 7, 8]:
                for indent in ['', ' ', '   ', '    ', '\t']:
                    for trailer in trailers:
                        for eof in ['', '\n']:
                            expected = int(closing >= opening and len(indent) <= 3 and '\t' not in indent
                                           and all(c in ' \t' for c in trailer))
                            # An extra matching marker is part of the closing run.
                            if trailer == marker:
                                expected = int(closing + 1 >= opening and len(indent) <= 3 and '\t' not in indent)
                            source = marker * opening + '\n' + indent + marker * closing + trailer + '\n## Probe' + eof
                            add(f'fence-{len(rows)}', source, expected)
    names = ['pre', 'script', 'style', 'textarea']
    for opener in names:
        for closer in names:
            for spelling in [closer, closer.upper(), closer.capitalize()]:
                for join in ['\n', ' x ']:
                    for eof in ['', '\n']:
                        add(f'html-valid-{len(rows)}', f'<{opener}>{join}before </{spelling}> after\n## Probe' + eof, 1)
        for close in ['</pre >', '</pre\t>', '</pre\r>', '</pre\f>', '</prelude>', '</ pre>',
                      '</pre/>', '</pre', '</scriptX>', '</\u017fcript>', '</scr\u0131pt>', '</scr\u0130pt>',
                      '</\u017ftyle>', '</textarea\u00a0>']:
            for join in ['\n', 'x']:
                add(f'html-invalid-{len(rows)}', f'<{opener}>{join}{close}\n## Probe', 0)
    for source in ['```\n## Probe', '~~~\n## Probe', '<pre>\n## Probe', '<script>\n## Probe',
                   '<style>\n## Probe', '<textarea>\n## Probe', '<pre></style>\n<script>\n## Probe',
                   '<div>\n</pre>\n## Probe', '<!--\n</pre>\n## Probe', '```\n</pre>\n## Probe']:
        add(f'eof-state-{len(rows)}', source, 0)
    return rows

def observe(version):
    sys.path.insert(0, str(OUT / 'snapshots' / version / 'scripts'))
    toc = importlib.import_module('gen_toc')
    cases = importlib.import_module('gen_toc_cases')
    fixtures = json.loads((OUT / 'public-evidence/author/fixtures.json').read_text())
    renderer = {r['id']: r['h2'] for r in json.loads((OUT / 'public-renderer-index.json').read_text())}
    observed = []
    with tempfile.TemporaryDirectory(prefix='r225-reader-') as tmp:
        path = Path(tmp) / 'input.txt'
        for row in fixtures:
            path.write_bytes(row['source'].encode())
            source = row['source']
            normalized = path.read_text()
            def result(text):
                return dict(h2=sum(h[0] == 2 for h in toc.headings(text)), refused=len(toc.refusals(text)),
                            blocks=toc.blocks(text))
            observed.append(dict(id=row['id'], renderer=renderer[row['id']], raw=result(source), reader=result(normalized)))
    save(f'corpus-{version}.json', observed)
    rows = independent_rows()
    for row in rows:
        row['actual'] = sum(h[0] == 2 for h in toc.headings(row['source']))
    save(f'boundaries-{version}.json', rows)
    families = {}
    for name in ['walk', 'tag', 'guard', 'heading', 'predecessor', 'provenance', 'refusal']:
        families[name] = [(title, source) for title, source, _ in getattr(cases, name + '_arms')()]
    save(f'controls-{version}.json', families)
    pages = {}
    for population, rev in [('base', BASE), ('head', HEAD)]:
        pages[population] = {}
        for path in git('ls-tree', '-r', '--name-only', rev).decode().splitlines():
            if not path.endswith('.md'):
                continue
            text = git('show', f'{rev}:{path}').decode().replace('\r\n', '\n').replace('\r', '\n')
            pages[population][path] = dict(blocks=toc.blocks(text), kinds=toc.line_kinds(text),
                                          headings=toc.headings(text), owns=toc.owns(path, text),
                                          refusal=toc.refusals(text), generated=toc.generated_block(text, path))
    save(f'pages-{version}.json', pages)
    print(version, 'corpus', len(observed), 'independent boundaries', len(rows),
          'boundary mismatches', sum(r['actual'] != r['expected'] for r in rows),
          'retained arms', sum(map(len, families.values())), flush=True)

def e2e(version):
    sys.path.insert(0, str(OUT / 'snapshots' / version / 'scripts'))
    gate = importlib.import_module('check_em_dash')
    toc = importlib.import_module('gen_toc')
    heading = '## Old \u2014 heading\n'
    tail = '\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n'
    nav = ('## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n'
           '- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n'
           '- **[Gamma](#gamma)** -- What gamma holds.\n\n')
    prefixes = [('inner-space', '<pre>\n</pre >\n', 0), ('inner-tab', '<style>x</style\t>\n', 0),
                ('cross', '<pre>\n</style>\n', 1), ('cross-inline', '<script>x</TEXTAREA>\n', 1),
                ('ascii', '<style>\n</StYlE>\n', 1), ('long-s', '<script>\n</\u017fcript>\n', 0),
                ('dotless', '<script>\n</scr\u0131pt>\n', 0), ('dotted', '<script>\n</scr\u0130pt>\n', 0),
                ('fence-tab', '```\n```\t\n', 1), ('long-fence', '```\n````` \t\n', 1),
                ('bad-long-fence', '```\n````` x\n', 0), ('fence-nbsp', '```\n```\u00a0\n', 0),
                ('fence-ff', '~~~\n~~~\f\n', 0), ('crlf', '```\r\n```\r\n', 1),
                ('cr', '```\r```\r', 1), ('html-cr', '<pre>\r</style>\r', 1),
                ('inner-cr', '<pre>\n</pre\r>\n', 0)]
    result = []
    with tempfile.TemporaryDirectory(prefix='r225-real-git-') as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, 'init', '-q', '--initial-branch=main')
        for name, prefix, expected in prefixes:
            (repo / (name + '.md')).write_bytes(('# Page\n\n' + prefix + heading + tail).encode())
        base = gate._commit(repo, 'disposable review base')
        for name, prefix, expected in prefixes:
            (repo / (name + '.md')).write_text('# Page\n\n' + nav + heading + tail)
        gate._commit(repo, 'disposable review candidate')
        for name, prefix, expected in prefixes:
            change = gate.Change(name + '.md', name + '.md')
            verdict = gate.Verdict()
            gate.judge_page(repo, base, change, verdict)
            normalized = gate.git(repo, 'show', base + ':' + name + '.md')
            result.append(dict(id=name, expected_exempt=expected, exempt=verdict.exempt,
                               findings=verdict.findings, added=[vars(a) for a in gate.added_lines(repo, base, change)],
                               base_git_reader_has_cr='\r' in normalized,
                               normalized_base_headings=toc.headings(normalized)))
    save(f'e2e-{version}.json', result)
    print(version, 'real-Git label cases', len(result), 'exemption mismatches',
          sum(r['expected_exempt'] != r['exempt'] for r in result), flush=True)

def live():
    fixtures = json.loads((OUT / 'public-evidence/author/fixtures.json').read_text())
    chosen = [r for r in fixtures if r['id'] in {
        'F-backtick-U0009', 'F-backtick-U000C', 'F-tilde-U00A0', 'T-later-U0020',
        'T-opening-U0009', 'N-later-pre-style', 'N-opening-script-TEXTAREA',
        'N-later-textarea-PRE', 'N-opening-style-SCRIPT', 'B-fence-crlf', 'B-fence-cr',
        'B-type1-cr', 'B-inner-slash', 'B-long-name', 'B-reset'}]
    chosen += [dict(id='live-' + str(i), source=s) for i, s in enumerate([
        '<script>\n</\u017fcript>\n## Probe', '<script>\n</scr\u0131pt>\n## Probe',
        '<script>\n</scr\u0130pt>\n## Probe', '```\n````` \t\n## Probe',
        '```\n````` x\n## Probe', '<pre>\ntext </sTyLe> text\n## Probe',
        '<pre>\n</pre\r>\n## Probe', '````\n```\n## Probe',
        '~~~\n~~~~\t\n## Probe', '<pre></style>\n## Probe'])]
    sys.path.insert(0, str(OUT / 'snapshots/head/scripts'))
    import gen_toc as toc
    results = []
    for row in chosen:
        request = json.dumps(dict(text=row['source'], mode='gfm')).encode()
        proc = subprocess.run(['gh', 'api', 'markdown', '--method', 'POST', '--input', '-'],
                              input=request, capture_output=True)
        folder = OUT / 'live-renderer' / row['id']
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'request.json').write_bytes(request)
        (folder / 'response.html').write_bytes(proc.stdout)
        normalized = row['source'].replace('\r\n', '\n').replace('\r', '\n')
        results.append(dict(id=row['id'], source=row['source'], exit=proc.returncode,
                            stderr=proc.stderr.decode(), renderer_h2=count_html(proc.stdout),
                            head_h2=sum(h[0] == 2 for h in toc.headings(normalized)),
                            refused=bool(toc.refusals(normalized)),
                            response_sha256=hashlib.sha256(proc.stdout).hexdigest()))
    save('live-renderer.json', results)
    print('Fresh GFM', len(results), 'rows; mismatches',
          sum(r['renderer_h2'] != r['head_h2'] or r['exit'] != 0 for r in results), flush=True)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'setup': setup()
    elif mode == 'observe': observe(sys.argv[2])
    elif mode == 'e2e': e2e(sys.argv[2])
    elif mode == 'live': live()
