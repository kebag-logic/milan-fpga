"""Compare round 8 reviewers' published dict-literal edits with MUTANTS at a clone: python3 -I bytecheck.py <clone> <script>..."""
import ast, sys, re
sys.path.insert(0, sys.argv.pop(1) + "/scripts")
from process_test_support import MUTANTS
def edits_from(path):
    src = open(path).read()
    tree = ast.parse(src)
    found = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    try:
                        val = ast.literal_eval(v)
                    except Exception:
                        continue
                    found[k.value] = val
    return found
pairs = {"r8-resume-beside-new-live": "resume-beside-new-live",
         "r8-sigterm-trap-command-after-late-grace-resume": "sigterm-trap-command-after-resume-from-1.5s"}
for path in sys.argv[1:]:
    for name, val in edits_from(path).items():
        target = pairs.get(name, name)
        if target in MUTANTS:
            mine = MUTANTS[target][2:]
            def flat(v):
                if isinstance(v, (list, tuple)) and v and all(isinstance(x, str) for x in v) and len(v) == 2:
                    return [tuple(v)]
                out = []
                if isinstance(v, (list, tuple)):
                    for x in v:
                        out += flat(x)
                return out
            theirs = flat(val)
            print(f"{path.split('/')[-1]}: {name} -> {target}: {'SAME' if list(mine) == theirs else 'DIFF ' + repr(theirs)[:300]}")
