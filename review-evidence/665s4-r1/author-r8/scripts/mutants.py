#!/usr/bin/env python3
"""Plant each literal defect in a clean clone of the head, one at a time, and require its named check to fail in its
named words. usage: mutants.py <clone> <scratch> <table>. The clone is restored after each.
Exit 0 when every mutant is caught and the clone ends clean."""
import os
import subprocess
import sys
from pathlib import Path

clone, scratch, table = (Path(a).resolve() for a in sys.argv[1:4])
scratch.mkdir(parents=True, exist_ok=True)
TOOLS = Path(__file__).resolve().parent
PY = [sys.executable, '-B']
IMAGE = 'sw/firmware/ctrl/test/ctrl_plat_image.py'
TEST = 'sw/firmware/ctrl/test/ctrl_image_selftest.py'
SELFTEST = [*PY, TEST, '--require-rv32']
STOPPED = [sys.executable, '-B', str(TOOLS / 'stopped_probe.py'), str(clone), str(scratch / 'stopped')]
HEADERS = 'MAP_HEADERS = ("generated/csr.h", "generated/mem.h")'
ARM = ('    if flash_map is not None:\n'
       '        missing = [name for name in MAP_HEADERS if not (flash_map / name).is_file()]\n'
       '        if missing:\n'
       '            raise Refusal(PARTIAL_MAP.format(" and ".join(missing)))\n')
CALL = '        refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n'
LOOKUP = ('        cc = fw_rv32.compiler()\n        if cc is None:\n'
          '            raise Refusal("the pinned RV32 compiler is required")\n'
          '        objects, members = compile_all(cc, args, out)\n')
#: name: (file, anchor, replacement, the check it must fail, the words the check must say, what the check is called)
MUTANTS = {
    # the new refusal, each new check going red on its own
    'header-refusal-removed': (IMAGE, ARM, '', SELFTEST, "AssertionError: ('lacks-csr'", 'plat: lacking csr.h'),
    'csr-not-required': (IMAGE, HEADERS, 'MAP_HEADERS = ("generated/mem.h",)', SELFTEST,
                         "AssertionError: ('lacks-csr'", 'plat: lacking csr.h'),
    'mem-not-required': (IMAGE, HEADERS, 'MAP_HEADERS = ("generated/csr.h",)', SELFTEST,
                         "AssertionError: ('lacks-mem'", 'plat: lacking mem.h'),
    'lone-json-accepted': (IMAGE, '        if missing:\n', '        if len(missing) == 1:\n', SELFTEST,
                           "AssertionError: ('lacks-json-only', 'collect2: error: ld returned 1 exit status')",
                           'plat: JSON-only'),
    'one-header-accepted': (IMAGE, '        if missing:\n', '        if len(missing) == 2:\n', SELFTEST,
                            "AssertionError: ('lacks-csr'", 'plat: lacking csr.h'),
    'names-every-header': (IMAGE, '" and ".join(missing)', '" and ".join(MAP_HEADERS)', SELFTEST,
                           "AssertionError: ('lacks-csr', \"REFUSED: the flash map lacks generated/csr.h and",
                           'plat: lacking csr.h'),
    # a complete map is not refused, and the fixture that shows it has to be complete
    'complete-map-refused': (IMAGE, '        if missing:\n', '        if True:\n', SELFTEST,
                             'AssertionError: REFUSED: the flash map lacks', 'plat: complete map'),
    'fixture-json-only': (TEST, 'flash_map(work / "maps/complete", 1, (MAP_CSR, MAP_MEM))',
                          'flash_map(work / "maps/complete", 1, ())', SELFTEST,
                          'AssertionError: REFUSED: the flash map lacks generated/csr.h and generated/mem.h',
                          'plat: complete map'),
    # before the compiler is called
    'whole-refusal-after-compile': (IMAGE, CALL + LOOKUP, LOOKUP + CALL, SELFTEST,
                                    "AssertionError: ('both-archives', 'went on before its refusal'",
                                    'plat: no map, nothing left'),
    'header-refusal-after-compile': (IMAGE, CALL + LOOKUP,
                                     '        refuse_placeholder(None, (args.libc, args.compiler_runtime)) '
                                     'if args.flash_map is None else None\n' + LOOKUP + CALL, SELFTEST,
                                     "AssertionError: ('lacks-csr'", 'plat: lacking csr.h'),
    'json-only-refused-after-compile': (IMAGE, CALL + LOOKUP,
                                        '        if args.flash_map is None or any((args.flash_map / n).is_file() '
                                        'for n in MAP_HEADERS):\n    ' + CALL + LOOKUP + CALL, SELFTEST,
                                        "AssertionError: ('lacks-json-only', 'went on before its refusal'",
                                        'plat: JSON-only, nothing left'),
    # the round 7 refusal, whose function this round rewrote
    'no-map-refusal-removed': (IMAGE, CALL, '', SELFTEST, "AssertionError: ('both-archives'", 'plat: no map'),
    'any-archive-to-all': (IMAGE, 'any(path.exists() for path in archives)', 'all(path.exists() for path in archives)',
                           SELFTEST, "AssertionError: ('the-C-library-alone'", 'plat: no map'),
    'refused-with-a-map': (IMAGE, 'if flash_map is None and any(', 'if any(', SELFTEST,
                           'AssertionError: REFUSED: no --flash-map', 'plat: complete map'),
    'compile-only-refused': (IMAGE, 'if flash_map is None and any(path.exists() for path in archives):',
                             'if flash_map is None:', STOPPED, 'stopped_at_link False', 'ctrl_runs.stopped_at_link'),
}


def git(*argv: str) -> str:
    """git in the clone."""
    return subprocess.run(['git', '-C', str(clone), *argv], capture_output=True, text=True, check=True).stdout


def run(argv: list[str], log: Path) -> tuple[int, str]:
    """One check, its whole output in its log."""
    done = subprocess.run(argv, cwd=clone, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    log.write_text(done.stdout)
    return done.returncode, done.stdout


rows, escaped = [], 0
# the checks must be green with no mutant, or a red one proves nothing
for name, argv in (('head: ctrl_image_selftest', SELFTEST), ('head: stopped_at_link', STOPPED)):
    rc, said = run(argv, scratch / f"{name.split(': ')[1].replace(' ', '-')}.log")
    verdict = next((ln for ln in said.splitlines() if 'stopped_at_link' in ln), said.strip().splitlines()[-1])
    print(f'{name}: rc {rc}; {verdict[:140]}', flush=True)
    escaped += rc != 0
    rows.append(f'| {name} (no mutant) | none | | {rc} | | `{verdict[:110]}` |')
for name, (path, anchor, new, check, words, called) in MUTANTS.items():
    assert not git('status', '--porcelain', '--untracked-files=all'), 'the clone is not clean'
    text = (clone / path).read_text()
    assert text.count(anchor) == 1, (name, text.count(anchor))
    (clone / path).write_text(text.replace(anchor, new))
    rc, said = run(check, scratch / f'{name}.log')
    git('checkout', '--', path)
    caught = rc != 0 and words in said
    escaped += not caught
    line = next((ln.strip() for ln in said.splitlines() if words in ln), said.strip().splitlines()[-1])
    passed = sum(ln.startswith('PASS: plat:') for ln in said.splitlines())
    print(f'{name}: {"CAUGHT" if caught else "ESCAPED"}, rc {rc}, by {called}, {passed} plat checks passed first: '
          f'{line[:170]}', flush=True)
    rows.append(f'| {name} | `{Path(path).name}` | {called} | {rc} | {passed} | `{line[:130]}` |')
clean = not git('status', '--porcelain', '--untracked-files=all')
table.write_text('| Mutant | File | Caught by | rc | plat checks green first | Failing words |\n'
                 '|---|---|---|---:|---:|---|\n' + '\n'.join(rows) + '\n')
print(f'mutants: {len(MUTANTS)} planted, {escaped} escaped; clone clean after: {clean}')
sys.exit(1 if escaped or not clean else 0)
