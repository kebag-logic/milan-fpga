import argparse, ast, hashlib, importlib, json, pathlib, sys, time
parser = argparse.ArgumentParser()
parser.add_argument("--tree", type=pathlib.Path, required=True)
parser.add_argument("--group", type=int, required=True)
parser.add_argument("--evidence", type=pathlib.Path, required=True)
parser.add_argument("--require-rv32", action="store_true", required=True)
args = parser.parse_args()
source = args.tree / "sw/builder/test_builder.py"
tree = ast.parse(source.read_text())
main = next(n for n in tree.body if isinstance(n, ast.If) and ast.unparse(n.test) == "__name__ == '__main__'")
loop = next(n for n in main.body if isinstance(n, ast.For) and ast.unparse(n.target) == "fn")
names = [n.id for n in loop.iter.elts]
assert len(names) == len(set(names))
groups = []; pending = []
for name in names:
    if name in ("test_baremetal_profile_contract", "test_every_recipe_elaborates"):
        if pending: groups.append(pending); pending = []
        groups.append([name])
    else:
        pending.append(name)
        if len(pending) == 15: groups.append(pending); pending = []
if pending: groups.append(pending)
sys.path.insert(0, str(source.parent))
builder = importlib.import_module("test_builder")
namespace = dict(vars(builder))
for node in main.body:
    if isinstance(node, ast.ImportFrom):
        module = importlib.import_module(node.module)
        for item in node.names: namespace[item.asname or item.name] = getattr(module, item.name)
assert all(callable(namespace[name]) for name in names)
results = []
for name in groups[args.group]:
    print(name + ":", flush=True)
    start = time.monotonic()
    namespace[name]()
    results.append({"name": name, "elapsed_ms": round((time.monotonic()-start)*1000)})
    print("PASS " + name, flush=True)
report = {"source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "groups": groups,
          "group": args.group, "results": results, "recorded_skips": builder.SKIPPED,
          "argv": sys.argv, "require_rv32": True}
args.evidence.write_text(json.dumps(report, indent=2)+"\n")
print("PASS: every unchanged gate function assigned to this group", flush=True)
