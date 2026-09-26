import sys, subprocess, runpy, json
from pathlib import Path
from unittest.mock import patch
root = Path('$LANES/565-8x8-clock')
mode = sys.argv[1]
sys.path.insert(0, str(root / 'sw/builder'))
selector = str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc')
cross = {selector, 'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
compiler = '$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc'
original = subprocess.run
hidden = set()
executed = 0
with Path('$VALIDATION_STORAGE/565-a344/builder-' + mode + '-audit.jsonl').open('w') as audit:
    def invoke(argv, **kwargs):
        global executed
        if str(argv[0]) not in cross:
            return original(argv, **kwargs)
        actual = list(argv)
        if mode == 'absent':
            hidden.add(str(argv[0]))
            audit.write(json.dumps({'requested':list(map(str,argv)), 'result':'deliberately absent'}) + '\n')
            raise FileNotFoundError('deliberately absent RV32 candidate')
        if str(argv[0]) == selector:
            actual[0] = compiler
        result = original(actual, **kwargs)
        audit.write(json.dumps({'requested':list(map(str,argv)), 'actual':list(map(str,actual)), 'rc':result.returncode}) + '\n')
        audit.flush()
        if '-std=gnu99' in actual:
            executed += 1
        return result
    sys.argv = ['test_builder.py'] + (['--require-rv32'] if mode == 'present' else [])
    with patch.object(subprocess, 'run', side_effect=invoke):
        runpy.run_path(str(root / 'sw/builder/test_builder.py'), run_name='__main__')
    if mode == 'absent':
        assert hidden == cross, hidden
        print('FULL BUILDER ABSENT: all three cross selectors hidden; original host probes and native tests retained')
    else:
        assert executed > 0
        print('FULL BUILDER PRESENT: compiler invocations', executed)
