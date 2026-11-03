"""List statements in a function range whose source, re-flowed at 120 columns, takes fewer lines (layout only)."""
import ast, sys, io, tokenize
path, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
src = open(path).read(); lines = src.splitlines()
tree = ast.parse(src)
def flat(seg):
    toks = list(tokenize.generate_tokens(io.StringIO(seg).readline))
    out, prev = "", None
    for t in toks:
        if t.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER, tokenize.COMMENT):
            continue
        if prev is not None:
            if t.start[0] == prev.end[0]:
                out += seg.splitlines()[t.start[0]-1][prev.end[1]:t.start[1]]
            else:
                out += "" if prev.string in "([{" or t.string in ")]}" else " "
        out += t.string; prev = t
    return out
for node in ast.walk(tree):
    if isinstance(node, ast.stmt) and not isinstance(node, (ast.For, ast.With, ast.FunctionDef, ast.If, ast.Try)) \
            and lo <= node.lineno <= hi and node.end_lineno > node.lineno:
        seg = "\n".join(lines[node.lineno-1:node.end_lineno])
        ind = len(lines[node.lineno-1]) - len(lines[node.lineno-1].lstrip())
        one = flat(seg.strip())
        # greedy break at ", " at depth >= 1
        depth, cuts = 0, []
        instr = None
        for i, ch in enumerate(one):
            if instr:
                if ch == instr and one[i-1] != "\\": instr = None
                continue
            if ch in "\"'": instr = ch
            elif ch in "([{": depth += 1
            elif ch in ")]}": depth -= 1
            elif ch == "," and depth >= 1 and one[i+1:i+2] == " ": cuts.append(i+1)
        out, start, width, cont = [], 0, 120 - ind, ind + 5
        last = 0
        cur_start = 0; avail = 120 - ind
        n = 1; pos = 0
        segs = []
        prevcut = 0
        for c in cuts + [len(one)]:
            if c - cur_start > avail:
                if prevcut == cur_start: n = 99; break
                n += 1; cur_start = prevcut + 1; avail = 120 - cont
            prevcut = c
        if len(one) - cur_start > avail: n += 1
        now = node.end_lineno - node.lineno + 1
        if n < now: print(f"{node.lineno}: {now} -> {n}: {one[:70]}")
