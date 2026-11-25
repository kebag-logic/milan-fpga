#!/usr/bin/env python3
"""Focused, disposable controls; run SOURCE PINNED_TEST_PREFIX as arguments."""
import concurrent.futures
import hashlib
import io
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tarfile
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1]).resolve()
SDK = Path(sys.argv[2]).resolve()
HEAD = 'ec727b64663b4eef2fc8da1ea5e0eae6541597d1'
SCRATCH = OUT / 'scratch'
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
ENV = os.environ.copy()
for key in list(ENV):
    if key.startswith('GTEST_'):
        del ENV[key]
ENV.update(ASAN_OPTIONS='detect_leaks=1:halt_on_error=1', UBSAN_OPTIONS='halt_on_error=1')

def clean(text):
    for p, label in ((str(SOURCE), '<source>'), (str(OUT), '<packet>'), (str(SDK), '<test-prefix>')):
        text = text.replace(p, label)
    return text

def run(args, cwd, name, expected=0):
    p = subprocess.run(list(map(str, args)), cwd=cwd, env=ENV, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, timeout=240)
    (OUT / (name + '.log')).write_text(clean(p.stdout))
    (OUT / (name + '.rc')).write_text(str(p.returncode) + '\n')
    if expected is not None:
        assert p.returncode == expected, (name, p.returncode)
    return p

def integrity(name):
    def git(*a):
        return subprocess.check_output(['git', '-C', str(SOURCE), *a])
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    entries = git('ls-tree', '-rz', 'HEAD').split(b'\0')
    checked, links = [], []
    expected_index = []
    for entry in entries:
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, kind, sha = meta.decode().split()
        path = path.decode()
        expected_index.append(f'{mode} {sha} 0\t{path}')
        if kind == 'commit':
            links.append({'path': path, 'sha': sha})
            continue
        p = SOURCE / path
        data = os.readlink(p).encode() if p.is_symlink() else p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        actual_mode = '120000' if p.is_symlink() else ('100755' if p.stat().st_mode & 0o111 else '100644')
        assert actual == sha and actual_mode == mode, path
        checked.append({'path': path, 'blob': sha, 'mode': mode})
    index = git('ls-files', '--stage').decode().splitlines()
    assert sorted(index) == sorted(expected_index)
    result = {'head': HEAD, 'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
              'tracked_blobs': checked, 'gitlinks': links, 'index_matches': True,
              'status': git('status', '--porcelain=v1').decode()}
    assert not result['status']
    (OUT / name).write_text(json.dumps(result, indent=2) + '\n')

def extract(name):
    dest = SCRATCH / name
    dest.mkdir(parents=True, exist_ok=True)
    data = subprocess.check_output(['git', '-C', str(SOURCE), 'archive', HEAD])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(dest, filter='data')
    return dest

def host(instrumented):
    tag = 'memory' if instrumented else 'native'
    root = extract(tag)
    flags = ['-O0', '-g', '-Wall', '-Wextra', '-Werror', '-Iinclude', '-fno-omit-frame-pointer']
    if instrumented:
        flags += ['-fsanitize=address,undefined']
    for src, obj in [('tests/test_adp.cpp', 'tests.o'), ('tests/main.cpp', 'main.o')]:
        run(['g++', '-std=c++20', *flags, '-isystem', SDK/'include', '-c', src, '-o', obj],
            root, tag + '-' + obj + '-build')
    original = (root/'src/adp.c').read_text()
    mutations = json.loads((root/'tests/mutations.json').read_text())
    chosen = [m for m in mutations if m['name'].startswith(('adp-control-length-', 'adp-long-control-length-',
                                                          'adp-short-control-length-', 'adp-minimum-control-length-'))]
    if instrumented:
        chosen = [m for m in chosen if m['name'] == 'adp-long-control-length-reads-surplus']
    results = []
    for m in [None, *chosen]:
        name = m['name'] if m else 'head'
        text = original
        if m:
            assert text.count(m['old']) == 1
            text = text.replace(m['old'], m['new'])
        (root/'src/adp.c').write_text(text)
        run(['gcc', '-std=c11', *flags, '-DNDEBUG', '-DCTRL_REENTRY_ASSERT', '-c', 'src/adp.c', '-o', 'adp.o'],
            root, tag + '-' + name + '-compile')
        run(['g++', *flags, 'tests.o', 'main.o', 'adp.o', SDK/'lib/libgmock.a', SDK/'lib/libgtest.a',
             '-pthread', '-o', 'probe'], root, tag + '-' + name + '-link')
        filters = ['*'] if m is None else [':'.join(k['test'] for k in m['kills'])]
        if instrumented and m:
            filters += ['*AcceptsLongControlDataLength*']
        for i, filt in enumerate(filters):
            label = tag + '-' + name + '-' + str(i)
            report = root/'result.xml'
            report.unlink(missing_ok=True)
            p = run(['./probe', '--gtest_filter=' + filt, '--gtest_output=xml:result.xml'], root, label, None)
            failures, total = [], 0
            if report.exists():
                xml = ET.parse(report)
                for case in xml.findall('.//testcase'):
                    total += 1
                    if case.findall('failure'):
                        failures.append(case.attrib['classname'] + '.' + case.attrib['name'])
            if not m:
                assert p.returncode == 0 and total == 49 and not failures
            elif instrumented and i == 1:
                assert p.returncode != 0 and 'heap-buffer-overflow' in p.stdout
            else:
                assert p.returncode != 0 and len(failures) == 5
                assert all(k['needle'] in p.stdout for k in m['kills'])
            results.append({'control': name, 'filter': filt, 'rc': p.returncode,
                            'tests': total, 'failed': failures,
                            'boundary_diagnostic': 'heap-buffer-overflow' in p.stdout})
    (OUT/(tag+'-results.json')).write_text(json.dumps(results, indent=2)+'\n')
    return {tag: 'PASS', 'runs': len(results)}

def rv32():
    root = extract('rv32')
    original = (root/'src/adp.c').read_text()
    guard = '(wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) < ADP_CONTROL_DATA_LENGTH ||'
    variants = [('head', guard, 0), ('exact', guard.replace(' < ', ' != '), 64),
                ('low-octet', guard.replace('0x07FF', '0x00FF'), 64), ('no-bound', '', 63)]
    results = []
    for name, replacement, expected in variants:
        (root/'src/adp.c').write_text(original.replace(guard, replacement))
        run(['cmake', '-S', '.', '-B', 'build', '-DCMAKE_TOOLCHAIN_FILE=cmake/rv32.cmake',
             '-DCMAKE_BUILD_TYPE=Debug'], root, 'rv32-'+name+'-configure')
        run(['cmake', '--build', 'build', '-j4'], root, 'rv32-'+name+'-build')
        p = run(['qemu-system-riscv32', '-machine', 'virt', '-nographic', '-bios', 'none',
                 '-kernel', 'build/rv32_smoke.elf', '-no-reboot'], root, 'rv32-'+name+'-smoke', expected)
        results.append({'control': name, 'expected_exit': expected, 'actual_exit': p.returncode})
    (OUT/'rv32-controls.json').write_text(json.dumps(results, indent=2)+'\n')
    return {'rv32': 'PASS', 'runs': len(results)}

if __name__ == '__main__':
    integrity('integrity-before.json')
    # One foreground driver waits for three independent campaigns; at most six compilation jobs.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(host, False), pool.submit(host, True), pool.submit(rv32)]
        results = [f.result() for f in futures]
    integrity('integrity-after.json')
    print(json.dumps(results))
