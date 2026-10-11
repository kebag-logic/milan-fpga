"""sha256 of a Yosys `write_verilog -noattr -norename` netlist, made independent of
where the design sat in all.v and of how many auto-indices yosys spent before it:
all.v line numbers are masked, every auto-index ($<n>, not a $paramod hash) is replaced by its numeric rank
among the file's auto-indices (a uniform shift keeps every rank), and the lines are
sorted, since write_verilog orders declarations by name and a shift across a digit
boundary reorders them. Equal digests = the same cells, wires and connections."""
import hashlib, re, sys
IDX = re.compile(r"\$([0-9]+)(?![0-9A-Za-z])")
for path in sys.argv[1:]:
    text = re.sub(r"all\.v:[0-9]+(\.[0-9]+-[0-9]+\.[0-9]+)?", "all.v:L", open(path).read())
    rank = {n: i for i, n in enumerate(sorted({int(m) for m in IDX.findall(text)}))}
    text = IDX.sub(lambda m: "$" + str(rank[int(m.group(1))]), text)
    body = "\n".join(sorted(text.split("\n")))
    print(path.rsplit("/", 1)[-1], hashlib.sha256(body.encode()).hexdigest())
