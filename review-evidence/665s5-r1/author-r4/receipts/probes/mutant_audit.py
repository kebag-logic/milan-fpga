#!/usr/bin/env python3
"""The audit of every self-test mutant: the assertion it fires, and what holds it.

usage: mutant_audit.py CHECKOUT RULES.json

For each mutant it records the assertion that fails its named check: the line, the statement and the failing words.
Then it deletes that assertion from the self-test's source, in memory, and runs the mutant again, until it escapes,
so the chain lists every assertion that holds it. RULES.json gives, per mutant, a text of the assertion that is the
rule it names, written by reading the mutant and its check. A mutant is `own rule` only when its first assertion
carries that text and it fails by an assertion, not an exception; anything else is reported and the exit status is 1.
"""
import ast
import json
import sys
import traceback
import types
from contextlib import ExitStack
from pathlib import Path

root, rules = Path(sys.argv[1]).resolve(), json.loads(Path(sys.argv[2]).read_text())
path = root / 'tb/verilator/ctrl_service_hooks/hooks_selftest.py'
sys.path.insert(0, str(path.parent))
SOURCE = path.read_text()
LOADED = 0


def load(source: str) -> types.ModuleType:
    """The self-test from this source text, under a new name."""
    global LOADED
    LOADED += 1
    module = types.ModuleType(f'selftest_{LOADED}')
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    exec(compile(source, str(path), 'exec'), module.__dict__)
    return module


def statements(source: str) -> list[tuple[int, int]]:
    """Each `expect(...)` statement's first and last line."""
    return [(n.lineno, n.end_lineno) for n in ast.walk(ast.parse(source))
            if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
            and getattr(n.value.func, 'id', '') == 'expect']


def delete(source: str, line: int) -> str:
    """The source with the statement holding this line replaced by pass, the numbering kept."""
    first, last = next((a, b) for a, b in statements(source) if a <= line <= b)
    lines = source.split('\n')
    indent = lines[first - 1][:len(lines[first - 1]) - len(lines[first - 1].lstrip())]
    lines[first - 1:last] = [indent + 'pass'] + [''] * (last - first)
    return '\n'.join(lines)


def fired(module: types.ModuleType, name: str) -> tuple[str, int, str] | None:
    """The mutant's failure of its named check: its kind, its line and its words; None when it escapes."""
    _, make, named = next(m for m in module.MUTANTS if m[0] == name)
    with ExitStack() as stack:
        stack.enter_context(make())
        try:
            module.CHECKS[named]()
            return None
        except Exception as error:  # noqa: BLE001  a crash is reported, not hidden
            frames = [f for f in traceback.extract_tb(error.__traceback__)
                      if f.filename == str(path) and f.name != 'expect']
            kind = 'assertion' if isinstance(error, module.Failed) else f'EXCEPTION {type(error).__name__}'
            return kind, frames[-1].lineno, str(error)


def statement_text(source: str, line: int) -> str:
    """The statement holding this line, on one line."""
    first, last = next(((a, b) for a, b in statements(source) if a <= line <= b), (line, line))
    return ' '.join(x.strip() for x in source.split('\n')[first - 1:last])


def main() -> int:
    base = load(SOURCE)
    assert not any(base.run_checks().values()), 'the self-test fails unmutated'
    names = [m[0] for m in base.MUTANTS]
    assert len(names) == len(set(names)), 'two mutants share a name'
    missing = [n for n in names if n not in rules]
    extra = [n for n in rules if n not in names]
    off = []
    fires: dict[int, int] = {}
    chains: dict[int, int] = {}
    for name in names:
        source, chain, named = SOURCE, [], next(m[2] for m in base.MUTANTS if m[0] == name)
        got = fired(base, name)
        while got is not None:
            chain.append((*got, statement_text(source, got[1])))
            if got[0] != 'assertion':
                break
            source = delete(source, got[1])
            got = fired(load(source), name)
        first = chain[0] if chain else None
        want = rules.get(name)
        verdict = 'own rule'
        if first is None:
            verdict = 'ESCAPED'
        elif first[0] != 'assertion':
            verdict = 'CRASH'
        elif want is None or want not in first[3]:
            verdict = 'OFF RULE'
        if verdict != 'own rule':
            off.append(name)
        print(f'{verdict} | {name} | check: {named}')
        for n, (kind, line, words, text) in enumerate(chain):
            print(f'    {"fires" if n == 0 else "then "} L{line} [{kind}] {text[:150]}')
            if n == 0:
                print(f'          words: {words[:130]}')
        print('    escapes with nothing deleted' if not chain else f'    escapes after {len(chain)} deletion(s)'
              if chain[-1][0] == 'assertion' else '    no escape')
        if chain:
            fires[chain[0][1]] = fires.get(chain[0][1], 0) + 1
        chains[len(chain)] = chains.get(len(chain), 0) + 1
    print(f'\n{len(names)} mutants, {len(names) - len(off)} on their own rule, {len(off)} not: {off}')
    print(f'no rule written for {missing}; rule for no mutant {extra}')
    print(f'chain lengths: {dict(sorted(chains.items()))}; {len(fires)} distinct assertions fired first')
    return 1 if off or missing or extra else 0


if __name__ == '__main__':
    raise SystemExit(main())
