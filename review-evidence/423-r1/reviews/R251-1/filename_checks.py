#!/usr/bin/env python3
"""Focused source observations and existing filename controls; offline only."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

source, work, operation, receipt = map(Path, sys.argv[1:5])
sys.path.insert(0, str(source / 'scripts'))
import check_merge_containment as checker

original_run = subprocess.run


def logged_run(args, *a, **kw):
    """Record actual subprocess arguments and raw output without changing them."""
    row = {'cwd': os.getcwd(),
           'argv_repr': [repr(arg) for arg in args],
           'argv_bytes_hex': [os.fsencode(arg).hex() for arg in args]}
    try:
        result = original_run(args, *a, **kw)
        row['returncode'] = result.returncode
        for name in ('stdout', 'stderr'):
            value = getattr(result, name)
            row[name] = {'hex': value.hex()} if isinstance(value, bytes) else value
        return result
    except Exception as exc:
        row['exception'] = repr(exc)
        raise
    finally:
        with receipt.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(row, ensure_ascii=True) + '\n')


subprocess.run = logged_run


def show(label, value):
    print(json.dumps({'label': label, 'value': value}, ensure_ascii=True))


show('python', {'version': sys.version, 'fsencoding': sys.getfilesystemencoding(),
                'fserrors': sys.getfilesystemencodeerrors(),
                'utf8_mode': sys.flags.utf8_mode})

if str(operation) == 'sites':
    for raw in (b'plain.txt', b'\xc3\xa9.txt', b'\xe9.txt', b'\xff.txt',
                b'\xe2\x82\xac.txt', b'tab\tend\n'):
        fixed = raw.decode('utf-8', 'surrogateescape')
        try:
            argv = os.fsencode(fixed).hex()
        except UnicodeError as exc:
            argv = type(exc).__name__
        show('roundtrip', {'raw_hex': raw.hex(), 'fixed_utf8_string': ascii(fixed),
                          'subprocess_argv_hex_or_error': argv,
                          'filesystem_roundtrip_hex': os.fsencode(os.fsdecode(raw)).hex()})
    os.chdir(work / 'lp' / 'linear')
    show('commit-paths', checker._commit_paths('pr'))
    show('postimage-pr-vs-parent', checker._same_patch_postimage('pr', 'pr^'))
    exact = subprocess.run(['git', '--literal-pathspecs', 'diff', '--no-ext-diff',
                            '--no-textconv', '--quiet', 'pr', 'pr^', '--',
                            b'\xc3\xa9.txt'], capture_output=True)
    show('raw-path-diff-exit', exact.returncode)
    if hasattr(checker, 'replay_verdict'):
        import merge_containment_replay as proof
        os.chdir(work / 'lp' / 'merge')
        raw = b'\xc3\xa9.txt'
        for decoding, path in [('fixed-utf8', raw.decode('utf-8', 'surrogateescape')),
                               ('filesystem', os.fsdecode(raw))]:
            for ref in ('pr~2', 'main', 'pr'):
                try:
                    entry = proof._tree_entry(ref, path)
                except Exception as exc:
                    entry = {'exception': type(exc).__name__, 'message': str(exc)}
                show('tree-entry', {'decoding': decoding, 'ref': ref, 'entry': entry})
        show('retained-at-tip', proof._retained_at_tip('pr', 'main', checker._git))
    # Patch transport is an explicit reversible UTF-8 pair, not filesystem argv.
    patch = b'path\xc3\xa9\nCRLF\r\ninvalid\xff\n'
    show('patch-byte-roundtrip', patch.decode('utf-8', 'surrogateescape').encode(
        'utf-8', 'surrogateescape') == patch)
elif str(operation) == 'existing-path-format':
    from merge_containment_selftest import _Fixture
    from merge_containment_selftest_replay import _History
    from merge_containment_selftest_retention import _path_and_format_cases
    results = []

    def case(name, got, expected, why):
        row = {'name': name, 'got': got, 'expected': expected,
               'pass': got == expected, 'why': why}
        results.append(row)
        show('existing-assertion', row)

    def run(argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            rc = checker.main(['check_merge_containment.py', *argv])
        return rc, out.getvalue()

    with tempfile.TemporaryDirectory(prefix='r251-path-format-') as directory:
        os.chdir(directory)
        history = _History()
        history._git('init', '-q', '-b', 'main')
        _path_and_format_cases(_Fixture(checker, case, run), history)
    show('existing-summary', {'assertions': len(results),
                              'failures': sum(not row['pass'] for row in results)})
    raise SystemExit(any(not row['pass'] for row in results))
else:
    raise SystemExit('unknown operation')
