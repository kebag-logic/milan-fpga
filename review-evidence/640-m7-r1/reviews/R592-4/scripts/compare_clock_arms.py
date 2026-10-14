"""Compare the clock-checker self-test before and after its split.

Usage: compare_clock_arms.py OLD.py NEW.py
OLD builds the arms inline in selftest(); NEW returns them from selftest_arms().
Checks: (1) the statements that build the arms are AST-identical, with the old
annotated `arms` assignment matched to the new `return`; (2) the remainder of
selftest() is identical once the new `arms = selftest_arms(...)` call stands in
for the moved block and the new docstring on the nested `findings` is ignored;
(3) every other module-level definition and statement is unchanged.
"""
import ast
import sys


def func(tree, name):
    return next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)


def is_doc(st):
    return isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant) and isinstance(st.value.value, str)


def strip_docs(node):
    for n in ast.walk(node):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.body and is_doc(n.body[0]):
            n.body = n.body[1:]
    return node


old = ast.parse(open(sys.argv[1]).read())
new = ast.parse(open(sys.argv[2]).read())
os_, ns = func(old, "selftest"), func(new, "selftest")
na = func(new, "selftest_arms")

# (1) arm-building statements
old_pre = [s for s in os_.body if not isinstance(s, ast.With) and not is_doc(s)]
with_old = next(s for s in os_.body if isinstance(s, ast.With))
idx_ren = next(i for i, s in enumerate(with_old.body)
               if isinstance(s, ast.Assign) and getattr(s.targets[0], "id", None) == "renamed")
idx_arms = next(i for i, s in enumerate(with_old.body)
                if isinstance(s, ast.AnnAssign) and s.target.id == "arms")
old_build = [s for s in old_pre if not isinstance(s, (ast.Return, ast.Expr))]
old_build += with_old.body[idx_ren:idx_arms]
old_arms_value = with_old.body[idx_arms].value
new_body = [s for s in na.body if not is_doc(s)]
new_build, new_ret = new_body[:-1], new_body[-1]
ok1 = [ast.dump(s) for s in old_build] == [ast.dump(s) for s in new_build] \
    and ast.dump(old_arms_value) == ast.dump(new_ret.value)
print("(1) arm-building statements:", len(old_build), "old /", len(new_build), "new;",
      "arms list elements:", len(old_arms_value.elts), "old /", len(new_ret.value.elts), "new;",
      "IDENTICAL" if ok1 else "DIFFER")

# (2) remainder of selftest
old_rest = list(with_old.body[:idx_ren]) + [ast.Pass()] + list(with_old.body[idx_arms + 1:])
with_new = next(s for s in ns.body if isinstance(s, ast.With))
call_idx = next(i for i, s in enumerate(with_new.body)
                if isinstance(s, ast.Assign) and getattr(s.targets[0], "id", None) == "arms")
new_rest = list(with_new.body[:call_idx]) + [ast.Pass()] + list(with_new.body[call_idx + 1:])
o2 = [ast.dump(strip_docs(s)) for s in old_rest] + [ast.dump(s) for s in os_.body if isinstance(s, (ast.Expr, ast.Return)) and not is_doc(s)]
n2 = [ast.dump(strip_docs(s)) for s in new_rest] + [ast.dump(s) for s in ns.body if isinstance(s, (ast.Expr, ast.Return)) and not is_doc(s)]
ok2 = o2 == n2 and ast.dump(with_old.items[0]) == ast.dump(with_new.items[0])
print("(2) selftest remainder (docstrings ignored):", "IDENTICAL" if ok2 else "DIFFER")
print("    new selftest prelude statements outside with:",
      [type(s).__name__ for s in ns.body if not isinstance(s, ast.With)])

# (3) everything else
od = {x.name: ast.dump(x) for x in old.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))}
nd = {x.name: ast.dump(x) for x in new.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))}
ok3 = True
for k in sorted(set(od) | set(nd)):
    if k in ("selftest", "selftest_arms"):
        continue
    same = od.get(k) == nd.get(k)
    ok3 &= same
    print("(3)", k, "unchanged" if same else "CHANGED")
oa = [ast.dump(x) for x in old.body if not isinstance(x, (ast.FunctionDef, ast.ClassDef))]
nb = [ast.dump(x) for x in new.body if not isinstance(x, (ast.FunctionDef, ast.ClassDef))]
ok3 &= oa == nb
print("(3) module-level statements", "unchanged" if oa == nb else "CHANGED")
print("VERDICT:", "BEHAVIOUR-PRESERVING REFACTOR" if ok1 and ok2 and ok3 else "DIFFERENCE FOUND")
sys.exit(0 if ok1 and ok2 and ok3 else 1)
