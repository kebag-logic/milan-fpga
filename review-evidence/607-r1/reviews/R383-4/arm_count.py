"""Count, in a builder bank log, each run-list entry of the candidate's test_builder.py (exact-once check)."""
import ast, re, sys
src = open(sys.argv[1]).read(); log = open(sys.argv[2], errors="replace").read()
tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.If) and "__main__" in ast.unparse(n.test)][0]
runlist = [ast.unparse(e) for n in ast.walk(main) if isinstance(n, ast.For) and isinstance(n.iter, ast.Tuple) for e in n.iter.elts]
counts = {f: len(re.findall(r"(?:^|[^A-Za-z0-9_])" + re.escape(f) + r":(?:\n|$)", log, re.M)) for f in runlist}
bad = {f: c for f, c in counts.items() if c != 1}
pos = [log.find(f + ":\n") for f in runlist]
print(f"run-list entries={len(runlist)} printed-exactly-once={sum(c == 1 for c in counts.values())} anomalies={bad}")
print(f"log order follows run-list order: {pos == sorted(pos) and -1 not in pos}")
