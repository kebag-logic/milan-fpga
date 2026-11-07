"""hier_diff.py <dev.rpt> <head.rpt> [N]: the N largest instance movements (Total LUTs) between two Vivado
report_utilization -hierarchical tables, by instance path, with FF and DSP. Reads only the reports."""
import sys


def table(path):
    rows, stack = {}, []
    for line in open(path, errors="replace"):
        if not line.startswith("| ") or "Instance" in line:
            continue
        cells = line.rstrip("\n").split("|")[1:-1]
        if len(cells) != 10:
            continue
        name = cells[0]
        depth = (len(name) - len(name.lstrip(" "))) // 2
        inst = name.strip()
        stack[depth:] = [inst]
        key = "/".join(stack)
        lut, ff, dsp = int(cells[2]), int(cells[6]), int(cells[9])
        rows[key] = (lut, ff, dsp, depth)
    return rows


dev, head = table(sys.argv[1]), table(sys.argv[2])
n = int(sys.argv[3]) if len(sys.argv) > 3 else 25
moves = []
for key in set(dev) | set(head):
    d = dev.get(key, (0, 0, 0, None)); h = head.get(key, (0, 0, 0, None))
    moves.append((h[0] - d[0], h[1] - d[1], h[2] - d[2], key, d[0], h[0], (h[3] if h[3] is not None else d[3])))
moves.sort(key=lambda m: -abs(m[0]))
print("| Instance | depth | LUT dev | LUT head | LUT | FF | DSP |\n|---|---:|---:|---:|---:|---:|---:|")
for dl, df, dd, key, a, b, depth in moves[:n]:
    print(f"| `{key}` | {depth} | {a:,} | {b:,} | {dl:+,} | {df:+,} | {dd:+} |")
