#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise both real flows on native and converted elaboration guards."""
from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / 'syn/yosys'


def require(ok: bool, message: str) -> None:
    """Refuse an unrelated failure or a surviving planted guard."""
    if not ok:
        raise RuntimeError(message)


def fixture(names: int, task: str = 'converted') -> str:
    """A live register keeps positive controls measurable after mapping."""
    error = ('$display("Error [elaboration] planted NAME guard");' if task == 'converted'
             else '$display("Fatal [elaboration] planted NAME guard");' if task == 'fatal'
             else '$error("planted NAME guard");')
    return (f'module tcam #(parameter N_NAME_P = {names})(input clk, output reg q);\n'
            'if (N_NAME_P < 1 || N_NAME_P > 128) begin : refuse_names\n'
            f'initial {error}\nend\nalways @(posedge clk) q <= ~q;\nendmodule\n')


def stage_flow(work: Path, flow: str, helper: Path) -> Path:
    """Copy orchestration unchanged except root, allocator and fixture input."""
    text = (HERE / flow).read_text()
    replacements = {
        'R="$(cd "$(dirname "$0")/../.." && pwd)"': 'R=' + shlex.quote(str(ROOT)),
        '. "$(dirname "$0")/malloc.sh"': '. ' + shlex.quote(str(HERE / 'malloc.sh')),
        'sv2v --top="$top" $inc $srcs': 'cat "$GUARD_FIXTURE"',
        'sv2v --top="$top" $INC $srcs': 'cat "$GUARD_FIXTURE"',
        '"$R/syn/yosys/enforce_elaboration.py"': shlex.quote(str(helper)),
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    target = work / flow
    target.write_text(text)
    return target


def invoke(script: Path, work: Path, source: str, arguments: list[str],
           parameter: str = '') -> subprocess.CompletedProcess[str]:
    """Run the actual synthesis process with isolated input and artifacts."""
    input_path = work / 'fixture.v'
    input_path.write_text(source)
    env = dict(os.environ, GUARD_FIXTURE=str(input_path), OOC_TMP=str(work / 'ooc'),
               OOC_CHPARAM=parameter)
    return subprocess.run(['bash', str(script), *arguments], cwd=ROOT, env=env,
                          capture_output=True, text=True, check=False)


def controls(work: Path) -> int:
    """Check boundaries, both modes, parameter overrides and cache custody."""
    count = 0
    helper = HERE / 'enforce_elaboration.py'
    for flow in ('run.sh', 'ooc.sh'):
        script = stage_flow(work, flow, helper)
        args = ['--top', 'tcam', '--no-structural'] if flow == 'run.sh' else ['tcam']
        for task in ('converted', 'fatal', 'native'):
            for names in (1, 128, 0, 129, 235):
                run = invoke(script, work, fixture(names, task), args)
                expected = names in (1, 128)
                require((run.returncode == 0) == expected,
                        f'{flow} {task} N_NAME_P={names}: {run.stdout} {run.stderr}')
                if not expected:
                    require('yosys FAIL' in run.stdout or 'yosys:' in run.stdout,
                            'guard must fail inside synthesis, not fixture setup')
                    require('$error' in run.stdout, 'refusal must name the fatal task')
                count += 1
        if flow == 'ooc.sh':
            run = invoke(script, work, fixture(1), args, 'N_NAME_P=235')
            require(run.returncode != 0 and '$error' in run.stdout,
                    'parameter override escaped the active guard')
            count += 1
        else:
            run = invoke(script, work, fixture(235), args + ['--mode', 'elaborate'])
            require(run.returncode != 0 and '$error' in run.stdout, 'fast mode ignored guard')
            count += 1

        # Removing the enforcement must revive the original false green.
        broken = work / 'unenforced.py'
        broken.write_text('from pathlib import Path\nimport sys\nPath(sys.argv[1]).read_text()\n')
        script = stage_flow(work, flow, broken)
        cache = ['--cache', str(work / 'cache')] if flow == 'run.sh' else []
        run = invoke(script, work, fixture(235), args + cache)
        require(run.returncode == 0, 'unenforced converted guard must reproduce false green')
        script = stage_flow(work, flow, helper)
        run = invoke(script, work, fixture(235), args + cache)
        require(run.returncode != 0 and '$error' in run.stdout,
                'enforcement deletion survived, or an old false PASS was reused')
        count += 2
    return count


def main() -> None:
    """Temporary source fixtures never touch repository RTL or generated files."""
    with tempfile.TemporaryDirectory(prefix='elaboration-guards-') as directory:
        count = controls(Path(directory))
    print(f'elaboration guard self-test: {count} controls passed')


if __name__ == '__main__':
    main()
