"""Each Python file a commit changes, compared by its syntax tree with every docstring removed (comments are not in
the tree): 'code unchanged' where the trees match; otherwise every string constant that differs, so a check's
printed description is told from a code change. C, C++ and header files are compared by their token stream with
comments removed (the C preprocessor's own comment stripping, gcc -fpreprocessed -dD -E -P), so a comment change is
told from a code one. Read only; exit 1 when any file differs in anything but those strings.
usage: python3 -I ast_same.py CHECKOUT OLD NEW"""
import ast
import subprocess
import sys

root, old, new = sys.argv[1:4]
git = lambda *a: subprocess.run(['git', '-C', root, *a], check=True, capture_output=True, text=True).stdout


def stripped(src: str) -> ast.AST:
    tree = ast.parse(src)
    for node in ast.walk(tree):
        body = getattr(node, 'body', None)
        if isinstance(body, list) and body and isinstance(body[0], ast.Expr) and \
                isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            node.body = body[1:] or [ast.Pass()]
    return tree


def strings(tree: ast.AST) -> list[str]:
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def tokens(src: str) -> str:
    r = subprocess.run(['gcc', '-fpreprocessed', '-dD', '-E', '-P', '-x', 'c', '-'], input=src, capture_output=True,
                       text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    return ' '.join(r.stdout.split())


bad = 0
files = git('diff', '--name-only', old, new).split()
print(f'# {old[:12]}..{new[:12]}: {len(files)} file(s)')
for path in files:
    a, b = git('show', f'{old}:{path}'), git('show', f'{new}:{path}')
    if path.endswith('.py'):
        ta, tb = stripped(a), stripped(b)
        if ast.dump(ta) == ast.dump(tb):
            print(f'{path}: code unchanged (docstrings and comments only)')
            continue
        sa, sb = strings(ta), strings(tb)
        shape = lambda t: ast.dump(t).replace("'", '"')
        for s in set(sa) | set(sb):
            pass
        # the trees with every string constant blanked: equal means only strings differ
        for t in (ta, tb):
            for n in ast.walk(t):
                if isinstance(n, ast.Constant) and isinstance(n.value, str):
                    n.value = ''
        if ast.dump(ta) == ast.dump(tb):
            diff = [(x, y) for x, y in zip(sa, sb) if x != y]
            print(f'{path}: code unchanged but {len(diff)} string constant(s):')
            for x, y in diff:
                print(f'    - {x!r}\n    + {y!r}')
        else:
            print(f'{path}: CODE CHANGED')
            bad += 1
    elif path.endswith(('.c', '.h', '.cpp')):
        same = tokens(a) == tokens(b)
        print(f'{path}: {"tokens unchanged (comments only)" if same else "TOKENS CHANGED"}')
        bad += not same
    else:
        print(f'{path}: not code ({path.rsplit(".", 1)[-1]})')
print('RESULT:', 'PASS: no code change but the strings listed' if not bad else f'FAIL: {bad} file(s) with a code change')
sys.exit(1 if bad else 0)
