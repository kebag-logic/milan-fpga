from pathlib import Path
import json
import subprocess
import sys

# Only the full builder process sees absent cross-compiler candidates.
# Host compilers, child Python processes, HOME and the shared SDK are unchanged.
if sys.argv[0] == 'sw/builder/test_builder.py':
    records = Path('$MANAGEMENT/2026-09-23/387-a269/full-builder-absent-argv.jsonl')
    assert not records.exists()
    cross = {str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc'),
             'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
    real_run = subprocess.run

    def absent_run(args, *positional, **keyword):
        if isinstance(args, (list, tuple)) and args and str(args[0]) in cross:
            with records.open('a') as stream:
                stream.write(json.dumps(dict(requested=list(args), executed=None,
                                            result='deliberately absent')) + '\n')
            raise FileNotFoundError('deliberately absent RV32 candidate')
        return real_run(args, *positional, **keyword)

    subprocess.run = absent_run
