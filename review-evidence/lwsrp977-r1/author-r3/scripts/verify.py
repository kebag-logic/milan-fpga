import concurrent.futures
import datetime
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

sys.dont_write_bytecode = True
ROOT = Path('$VALIDATION_STORAGE/lwsrp22-r2')
PACKET = Path(__file__).resolve().parents[1]
WORK = Path('$VALIDATION_STORAGE/lwsrp22-a861-r3')
RAW = PACKET / 'raw'
RECEIPTS = PACKET / 'receipts'
BASE = 'd1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b'
PREVIOUS = '50a2106483141fcd7d1b20654bcf0803e7c3020a'
HEAD = '16b6c950ca320d29876d84c33460c2652650f16d'
PREFIX = Path('$VALIDATION_STORAGE/977-a825/cgreen/prefix')
OPTIONS = ['ATTR_KEY', 'ATTR_BUCKETS', 'TIMER_SLOTS', 'TX_MERGE', 'ONE_PORT_MAP',
           'LEAN_VALIDATE', 'RAPID_REPLACE', 'LEAN_COPY', 'LEAN_TX']
OFF = [f'-DLWSRP_{name}=0' for name in OPTIONS]
END = [f'-DLWSRP_{name}=1' for name in OPTIONS[4:]]
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', CMAKE_PREFIX_PATH=str(PREFIX),
           LD_LIBRARY_PATH=str(PREFIX / 'lib'))

def run(command, cwd=ROOT, log=None):
    result = subprocess.run(['rtk', 'proxy', *map(str, command)], cwd=cwd, env=ENV,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if log:
        (RAW / log).write_bytes(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f'exit {result.returncode}: {command!r}; {result.stderr[-1000:]!r}')
    return result.stdout

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def receipt(name, payload):
    payload = dict(head=HEAD, base=BASE, recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), **payload)
    (RECEIPTS / name).write_text(json.dumps(payload, indent=2) + '\n')

def docs():
    commands = [
        ('sentences', ['python3', '-B', 'doc/tools/check_sentences.py']),
        ('references', ['python3', '-B', 'doc/tools/check_references.py']),
        ('reference-cases', ['python3', '-B', 'doc/tools/check_references.py', '--self-test']),
        ('links', ['python3', '-B', 'doc/tools/check_links.py', '--github-auth']),
        ('graphs', ['python3', '-B', 'doc/tools/render_mermaid.py', '--output', WORK / 'graphs'])]
    rows = []
    for label, command in commands:
        output = run(command, log=f'docs-{label}.log').decode()
        row = dict(check=label, exit_code=0, summary=output.strip().splitlines()[-1],
                   raw_sha256=digest(RAW / f'docs-{label}.log'))
        rows.append(row)
        print(row['summary'], flush=True)
    receipt('docs.json', dict(checks=rows, failures=0))

def log_planned_removals(paths, reason):
    with Path('$MANAGEMENT/2026-09-23/disk-cleanup.log').open('a') as log:
        for path in paths:
            log.write(f'{datetime.datetime.now(datetime.timezone.utc).isoformat()} A861 round3 planned rm: {path.resolve()} ({reason})\n')
        log.flush()
        os.fsync(log.fileno())

def units():
    rows = []
    for label, scale, flags in [('default', 'OFF', OFF), ('end-station', 'ON', END),
                                ('end-station-no-scale', 'OFF', OFF[:4] + END)]:
        for milan in ['OFF', 'ON']:
            name = f'{label}-{milan}'
            build = WORK / 'units' / name
            run(['cmake', '-S', ROOT, '-B', build, '-DCMAKE_BUILD_TYPE=Debug',
                 f'-DLWSRP_MILAN={milan}', f'-DLWSRP_SCALE={scale}',
                 '-DCMAKE_C_FLAGS=' + ' '.join(flags)], log=f'{name}-configure.log')
            # Some generators unlink the shared-library output before linking.
            log_planned_removals([build / 'libshlan.so'], 'possible shared-library relink cleanup before fresh build')
            run(['cmake', '--build', build, '--parallel', '4'], log=f'{name}-build.log')
            output = run([build / 'unit_tests'], log=f'{name}-unit.log').decode()
            run(['ctest', '--test-dir', build, '--output-on-failure'], log=f'{name}-runner.log')
            summary = output.strip().splitlines()[-1]
            row = dict(configuration=label, milan=milan, scale=scale, definitions=flags,
                       configure_exit=0, build_exit=0, unit_exit=0, runner_exit=0, summary=summary,
                       unit_raw_sha256=digest(RAW / f'{name}-unit.log'),
                       runner_raw_sha256=digest(RAW / f'{name}-runner.log'))
            rows.append(row)
            print(f'{name}: {summary}', flush=True)
    receipt('units.json', dict(builds=rows, failures=0))

def differential():
    spec = importlib.util.spec_from_file_location('differential_check', ROOT / 'tests/check_differential.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Select only the requested options-off case. Keep both drivers, the full
    # seed range, step counts, trace generation and equality logic unchanged.
    module.CONFIGS = {'default': []}
    module.FLAGS += OFF
    rows = []
    for milan in ['OFF', 'ON']:
        work = WORK / f'differential-{milan}'
        sys.argv = [str(ROOT / 'tests/check_differential.py'), '--work-dir', str(work),
                    '--milan', milan, '--no-mutants']
        rc = module.main()
        data = json.loads((work / 'differential.json').read_text())
        assert rc == 0 and len(data['rows']) == 2 and not data['problems']
        assert all(row['identical'] == 200 and row['excused'] == 0 for row in data['rows'])
        rows.append(dict(milan=milan, exit_code=rc, **{k: data[k] for k in ['rows', 'killed', 'problems']}))
    receipt('differential.json', dict(definitions=OFF, seeds=list(range(1, 201)), profiles=rows,
        scope='Only the default configuration was selected in the imported existing runner; both drivers and all trace comparisons were unchanged. No mutation or sanitizer campaign was selected.',
        comparisons=800, identical=800, excluded=0, failures=0))

def objects():
    trees = {}
    for label, revision in [('base', BASE), ('head', HEAD)]:
        tree = WORK / 'objects' / label
        tree.mkdir(parents=True)
        archive = run(['git', 'archive', revision, 'src'])
        with tarfile.open(fileobj=io.BytesIO(archive)) as source:
            source.extractall(tree, filter='data')
        trees[label] = tree
    sources = sorted(str(p.relative_to(trees['head'])) for p in trees['head'].rglob('*.c'))
    assert len(sources) == 10
    flags = [(opt, [f'-{opt}']) for opt in ['O0', 'O1', 'O2', 'O3', 'Os']]
    flags += [(f'{opt}-milan', [f'-{opt}', '-DLWSRP_MILAN=1']) for opt in ['O0', 'O2', 'Os']]
    flags += [(f'{opt}-pic', [f'-{opt}', '-fPIC']) for opt in ['O0', 'O2']]
    flags += [(f'{opt}-debug', [f'-{opt}', '-g']) for opt in ['O0', 'O2', 'Os']]
    compilers = [('compiler-A', 'gcc'), ('compiler-B', 'clang')]
    identities = []
    for label, binary in compilers:
        version = run([binary, '--version'], log=f'{label}-version.log')
        identities.append(dict(label=label, executable_sha256=digest(Path('/usr/bin') / binary),
                               version_output_sha256=hashlib.sha256(version).hexdigest()))

    def pair(job):
        compiler_label, compiler, flag_label, settings, source = job
        hashes = {}
        for label, tree in trees.items():
            output = WORK / 'objects' / 'output' / compiler_label / flag_label / label / (source.replace('/', '_') + '.o')
            output.parent.mkdir(parents=True, exist_ok=True)
            run([compiler, '-std=c11', *OFF, *settings, '-Isrc/include', '-Isrc', '-c', source, '-o', output], cwd=tree,
                log=f'{compiler_label}-{flag_label}-{label}-{source.replace("/", "_")}.log')
            if '-g' in settings:
                stripped = output.with_suffix('.stripped.o')
                run(['objcopy', '--strip-debug', output, stripped])
                output = stripped
            hashes[label] = digest(output)
        assert hashes['base'] == hashes['head'], (job, hashes)
        return dict(compiler=compiler_label, flags=settings, source=source,
                    debug_sections_removed='-g' in settings, base_sha256=hashes['base'], head_sha256=hashes['head'], identical=True)

    jobs = [(label, compiler, flag_label, settings, source)
            for label, compiler in compilers for flag_label, settings in flags for source in sources]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(pair, jobs))
    receipt('objects.json', dict(compilers=identities, definitions=OFF, sources=sources,
        flag_sets=len(flags), comparisons=len(rows), identical=len(rows), failures=0,
        non_debug_pairs=sum(not row['debug_sections_removed'] for row in rows),
        stripped_debug_pairs=sum(row['debug_sections_removed'] for row in rows), results=rows))
    print(f'Objects: {len(rows)} of {len(rows)} byte-identical; 10 sources, 2 compilers, 13 flag sets', flush=True)

if __name__ == '__main__':
    assert run(['git', 'rev-parse', 'HEAD']).decode().strip() == HEAD
    assert not run(['git', 'status', '--porcelain']).strip()
    {'docs': docs, 'units': units, 'differential': differential, 'objects': objects}[sys.argv[1]]()
