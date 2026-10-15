#!/usr/bin/env python3
"""Reviewer probe harness: plant one fixture, run the walker's --write/--check, report rc and refusal text.

Usage: imported by probe scripts; set REPO to the checkout whose scripts/ are under review.
"""
import contextlib, io, json, os, sys, tempfile
from pathlib import Path

REPO = Path(os.environ['PROBE_REPO']).resolve()
sys.path.insert(0, str(REPO / 'scripts'))
os.chdir(REPO)
import ci_tool_inventory as inventory  # noqa: E402
from ci_inventory_patterns_selftest import Fixture  # noqa: E402
import yaml  # noqa: E402

RESULTS = []


def walker(fixture):
    out = {}
    saved = sys.argv
    try:
        for mode in ('--write', '--check'):
            sys.argv = ['ci_tool_inventory.py', '--root', str(fixture.root), mode]
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                try:
                    rc = inventory.main()
                except SystemExit as e:
                    rc = e.code
                except Exception as e:  # an unhandled crash is reported, never hidden
                    rc = f'CRASH {type(e).__name__}: {e}'
            out[mode] = (rc, buf.getvalue().strip().splitlines()[-1:] )
    finally:
        sys.argv = saved
    return out


def probe(name, files, run, env=None, expect_hidden='brand_new_command'):
    with tempfile.TemporaryDirectory(prefix='r638-6-probe-') as d:
        fx = Fixture(Path(d))
        for k, v in files.items():
            fx.file(k, v)
        step = {'run': run, **({'env': env} if env else {})}
        fx.workflow.write_text(yaml.safe_dump({'jobs': {'gate': {'steps': [step]}}}))
        res = walker(fx)
        inv = json.loads((fx.root / 'ci/image/tool-inventory.json').read_text()) if (fx.root / 'ci/image/tool-inventory.json').exists() else None
        row = {'probe': name, 'run': run, 'files': files, 'env': env,
               'write': res['--write'], 'check': res['--check'],
               'tools': [t['tool'] for t in inv['tools']] if inv else None}
        RESULTS.append(row)
        print(json.dumps({'probe': name, 'write_rc': res['--write'][0], 'write_msg': res['--write'][1],
                          'check_rc': res['--check'][0]}))
        return row


def persist(name, files, run, env=None):
    """Write the same fixture to a persistent directory for the real-tool comparison."""
    base = Path(os.environ['PROBE_OUT']) / name
    base.mkdir(parents=True, exist_ok=True)
    for k, v in files.items():
        p = base / k
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(v)
    (base / '.probe-run.sh').write_text(''.join(f'export {k}={v!r}\n'.replace("'", "'") for k, v in (env or {}).items()) + run + '\n')


def both(name, files, run, env=None):
    persist(name, files, run, env)
    return probe(name, files, run, env)


def dump(path):
    Path(path).write_text(json.dumps(RESULTS, indent=1, sort_keys=True) + '\n')
