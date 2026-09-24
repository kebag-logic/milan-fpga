from pathlib import Path
import ast, inspect, json, re, subprocess, sys, tempfile
sys.path.insert(0, str(Path.cwd() / 'sw/builder'))
import test_firmware_compiler as driver
b = driver.builder
sdk = Path('$VALIDATION_STORAGE/504-manager-r1/sdk-install')
driver.sdk.verify(sdk)
tree = ast.parse(inspect.getsource(b.test_baremetal_profile_contract))
corpus = next(ast.literal_eval(node.value) for node in ast.walk(tree)
              if isinstance(node, ast.Assign)
              and any(isinstance(n, ast.Name) and n.id == 'lexer_corpus' for n in node.targets))
label, source, kept = next(row for row in corpus if row[0].startswith('a /*/ opener'))
with tempfile.TemporaryDirectory(prefix='408-a276-corpus-') as tmp:
    path = Path(tmp) / 'comment.c'
    path.write_text(source)
    argv = [str(sdk / driver.sdk.COMPILER), '-std=gnu99', '-E', str(path)]
    result = subprocess.run(argv, capture_output=True, text=True, timeout=120)
    measured = tuple(re.findall(r'\bint\s+(\w+)\s*;', result.stdout, re.ASCII))
    assert result.returncode == 0, result.stderr
    assert kept == measured == ('a', 'z'), (kept, measured)
    print(json.dumps(dict(label=label, source=source, argv=argv,
                          returncode=result.returncode, kept=kept,
                          measured=measured, stdout=result.stdout, stderr=result.stderr)))
original = inspect.getsource(b._c_phases)
before = 'stop = raw.find("\\n" if raw[i + 1] == "/" else "*/", i + 2)'
after = before.replace('i + 2)', 'i + 1)')
assert original.count(before) == 1
# Only the in-memory function changes. The worktree is never patched.
exec(compile(original.replace(before, after), '<block-closer-early>', 'exec'), b.__dict__)
b._C_PHASES_CACHE.clear()
for mode, destination in [('sdk', sdk), ('absent', None)]:
    try:
        driver.run_gate(destination, Path(__file__).with_name(f'corpus-control-{mode}-argv.jsonl'), require=bool(destination))
    except AssertionError as exc:
        message = str(exc)
        assert label in message and "('a', 'b', 'z')" in message, message
        print(f'EXPECTED REFUSAL {mode}: {message}')
    else:
        raise AssertionError(f'{mode}: block-closer-early mutant passed')
print('CORPUS CONTROL PASS: pinned compiler agrees; closer regression refused in both modes')
