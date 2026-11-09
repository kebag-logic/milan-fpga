"""Parse a Vivado report_utilization -hierarchical table into {path: (LUT, FF)}."""
def rows(path):
    out, stack = {}, []
    for line in open(path):
        if not line.startswith("|") or "Instance" in line:
            continue
        cells = line.rstrip("\n").split("|")[1:-1]
        if len(cells) < 8:
            continue
        name = cells[0]
        indent = len(name) - len(name.lstrip())
        try:
            lut, ff = int(cells[2]), int(cells[6])
        except ValueError:
            continue
        while stack and stack[-1][0] >= indent:
            stack.pop()
        stack.append((indent, name.strip()))
        out["/".join(s[1] for s in stack)] = (lut, ff)
    return out

