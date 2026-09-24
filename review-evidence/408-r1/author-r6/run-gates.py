from pathlib import Path
import json, os, shutil, subprocess, tarfile, tempfile, time
out = Path(__file__).resolve().parent
root = Path.cwd()
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True, timeout=120).strip()
assert head == '062e89ad098806ae5def8341fcb8c2815583ca00', head
assert not subprocess.check_output(['git', 'status', '--porcelain'], text=True, timeout=120)
results = []
def run(label, argv, cwd=root):
    print(f'START {label}: {argv}', flush=True)
    started = time.monotonic()
    with (out / f'{label}.log').open('w') as log:
        result = subprocess.run(argv, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, timeout=10800)
    entry = dict(label=label, argv=argv, head=head, returncode=result.returncode,
                 elapsed_seconds=round(time.monotonic()-started, 2), log=f'{label}.log')
    results.append(entry)
    (out / 'gates.json').write_text(json.dumps(results, indent=2)+'\n')
    print(f'END {label}: rc={result.returncode}, {entry["elapsed_seconds"]} seconds', flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
run('full-builder-sdk', ['python3', '-u', str(out/'full-builder-sdk.py')])
run('full-builder-absent', ['python3', '-u', str(out/'full-builder-absent.py')])
run('docs-git', ['python3', '-B', 'scripts/docs_check.py'])
# A tracked-file export, without repository metadata, matches the second CI mode.
# It stays in scratch and is removed after the gate; no other checkout is created.
with tempfile.TemporaryDirectory(prefix='408-a276-docs-', dir='$VALIDATION_STORAGE') as tmp:
    scratch = Path(tmp)
    archive = scratch/'source.tar'
    subprocess.run(['git', 'archive', '--format=tar', '--output', str(archive), head], check=True, timeout=300)
    exported = scratch/'source'
    exported.mkdir()
    with tarfile.open(archive) as tar:
        tar.extractall(exported, filter='data')
    run('docs-no-git', ['python3', '-B', 'scripts/docs_check.py'], exported)
for label, argv in [
    ('baremetal-only', ['python3','scripts/check_baremetal_only.py','--check']),
    ('em-dash', ['python3','scripts/check_em_dash.py','--base','759da623072358afdb0e9d570a7b4b6a788492c9']),
    ('doc-style', ['python3','scripts/check_doc_style.py']),
    ('toc', ['python3','scripts/gen_toc.py','--check']),
    ('doc-paths', ['python3','scripts/check_doc_paths.py']),
    ('python-idiom', ['python3','scripts/check_py_idiom.py']),
    ('diff-check', ['git','diff','--check']),
    ('committed-diff-check', ['git','diff','--check','991d59653ff82ccf73ef4df9477de1df8c8c5964','HEAD']),
]:
    run(label, argv)
assert subprocess.check_output(['git','rev-parse','HEAD'], text=True, timeout=120).strip() == head
assert not subprocess.check_output(['git','status','--porcelain'], text=True, timeout=120)
print(f'ALL {len(results)} REQUIRED/FINAL CHECKS RETURNED 0 AT {head}', flush=True)
