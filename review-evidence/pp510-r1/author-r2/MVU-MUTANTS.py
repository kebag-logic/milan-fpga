"""Run after building tb/pp_top: python3 MVU-MUTANTS.py REPO LABEL SCRATCH.

Only disposable generated-ROM copies change. The source checkout stays intact.
"""
import hashlib, json, pathlib, re, shutil, subprocess, sys
root = pathlib.Path(sys.argv[1]).resolve()
label = sys.argv[2]
scratch = pathlib.Path(sys.argv[3]).resolve()
out = pathlib.Path(__file__).resolve().parent
suite = root / 'tb/pp_top'
original = (suite / 'ucode.hex').read_bytes()
words = original.decode().splitlines()
records = []
built_head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
harness_blob = subprocess.check_output(['git','hash-object','tb/pp_top/sim_main.cpp'],cwd=root,text=True).strip()
binary_sha256 = hashlib.sha256((suite / 'obj_dir/Vpp_top_sim').read_bytes()).hexdigest()
for name, index, old, new in [('success',560,'c00000000001','c00000000000'),
                              ('features',741,'230000000000','230000000003')]:
    assert words[index] == old
    work = scratch / (label + '-' + name)
    work.mkdir()
    (work / 'obj_dir').mkdir()
    shutil.copy2(suite / 'ltn_rom.hex', work)
    changed = words.copy()
    changed[index] = new
    assert sum(a != b for a,b in zip(words, changed)) == 1
    (work / 'ucode.hex').write_text('\n'.join(changed) + '\n')
    log = out / (label + '-' + name + '-mutant.log')
    with log.open('w') as stream:
        result = subprocess.run([str(suite / 'obj_dir/Vpp_top_sim')], cwd=work,
                                stdout=stream, stderr=subprocess.STDOUT, timeout=3600)
    text = log.read_text()
    failures = [line for line in text.splitlines() if line.startswith('FAIL:')]
    match = re.search(r'\[build default[^\]]*\] (\d+) checks, (\d+) failures', text)
    assert result.returncode == 1 and match, (result.returncode, text[-200:])
    if name == 'success':
        for ct in range(1,6):
            assert any(f'M4: MVU 0x{ct:04x} must answer ' in f for f in failures)
            assert any(f'M4: MVU 0x{ct:04x} NOT_IMPLEMENTED echo ' in f for f in failures)
        assert not any('M4:' in f and ('frame length' in f or 'retain command cdl' in f) for f in failures)
    else:
        assert len(failures) == 3
        assert any('M2: features_flags' in f for f in failures)
    record = dict(label=label, name=name, word=index, original=old, mutant=new,
                  rc=result.returncode, checks=int(match[1]), failures=int(match[2]),
                  m4_failures=[f for f in failures if 'M4' in f], log=log.name)
    records.append(record)
    print(json.dumps(record), flush=True)
    shutil.rmtree(work)
assert (suite / 'ucode.hex').read_bytes() == original
receipt = dict(head=built_head, harness_blob=harness_blob, binary_sha256=binary_sha256,
               rom_sha256=hashlib.sha256(original).hexdigest(), mutations=records)
(out / (label + '-mutation-results.json')).write_text(json.dumps(receipt, indent=2)+'\n')
print('Source ROM unchanged: ' + receipt['rom_sha256'], flush=True)
