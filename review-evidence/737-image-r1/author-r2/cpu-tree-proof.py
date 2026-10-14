import hashlib, json, pathlib, subprocess, sys, tarfile
sys.path.insert(0, 'ci/image')
import patch_provenance, privacy
work = pathlib.Path('$VALIDATION_STORAGE/737-a615')
pins = json.loads(pathlib.Path('ci/image/sources.lock.json').read_text())
rows = {r['tool']: r for r in pins['sources']}
places = {'VexiiRiscv': ''}
while True:
    before = len(places)
    for name, row in rows.items():
        if row.get('parent') in places:
            places[name] = '/'.join(filter(None, [places[row['parent']], row['path']]))
    if len(places) == before: break
expected = {}
for name, prefix in places.items():
    row = rows[name]
    path = work / 'context' / row['filename']
    with path.open('rb') as stream: digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    assert digest == row['sha256'] and path.stat().st_size == row['size']
    with tarfile.open(path) as archive:
        for member in archive:
            relative = member.name.partition('/')[2]
            if not relative or member.isdir(): continue
            key = '/'.join(filter(None,[prefix,relative]))
            if member.isfile():
                data = archive.extractfile(member).read()
                expected[key] = ['file', hashlib.sha256(data).hexdigest(), bool(member.mode & 0o111)]
            elif member.issym(): expected[key] = ['link', member.linkname, False]
            else: raise ValueError('unsupported upstream member kind')
proofs = patch_provenance.provenance(pins, work/'context', privacy.Policy())
for proof in proofs.values():
    if proof['tool'] == 'VexiiRiscv':
        matches = [key for key,value in expected.items() if value[1] == proof['upstream_member_sha256']]
        assert len(matches) == 1
        expected[matches[0]][1] = proof['member_sha256']
program = """import hashlib,json,pathlib,pythondata_cpu_vexiiriscv as cpu
root=pathlib.Path(cpu.data_location)/'ext/VexiiRiscv'
result={}
for path in root.rglob('*'):
    name=path.relative_to(root).as_posix()
    if path.is_symlink(): result[name]=['link',str(path.readlink()),False]
    elif path.is_file(): result[name]=['file',hashlib.sha256(path.read_bytes()).hexdigest(),bool(path.stat().st_mode & 0o111)]
print(json.dumps(result,sort_keys=True))
"""
actual = json.loads(subprocess.check_output(['sudo','-n','-u','alex','-g','docker','docker','run','--rm','--network','none',sys.argv[1],'python3','-c',program]))
missing=sorted(expected.keys()-actual.keys()); extra=sorted(actual.keys()-expected.keys())
changed=sorted(k for k in expected.keys() & actual.keys() if expected[k] != actual[k])
report={'image_reference':sys.argv[1], 'sources':{name:rows[name]['version'] for name in places}, 'expected_files':len(expected), 'actual_files':len(actual),'missing_count':len(missing),'extra_count':len(extra),'changed_count':len(changed),'tree_sha256':hashlib.sha256(json.dumps(actual,sort_keys=True).encode()).hexdigest()}
pathlib.Path('$MANAGEMENT/2026-09-23/737-a615/cpu-tree-proof.json').write_text(json.dumps(report,indent=2)+'\n')
if missing or extra or changed:
    (work/'cpu-tree-differences.json').write_text(json.dumps({'missing':missing,'extra':extra,'changed':changed},indent=2))
    raise AssertionError(report)
print('PASS: complete recursive patched CPU tree; '+str(len(actual))+' byte-identical files and links')
