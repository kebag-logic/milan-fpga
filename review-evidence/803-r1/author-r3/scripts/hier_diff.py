"""hier_diff.py <base.rpt> <head.rpt> [depth]: compare two Vivado report_utilization -hierarchical tables (placed),
instance by instance to <depth> levels below the top (default 2), printing Total LUTs and FFs of each side and the
head-minus-base delta, largest absolute LUT delta first; instances present on one side only are listed too."""
import sys


def parse(path, depth):
    rows, stack = {}, []
    for line in open(path, encoding='utf-8', errors='replace'):
        if not line.startswith('| ') or 'Instance' in line:
            continue
        cells = line.rstrip('\n').split('|')
        name_cell = cells[1]
        indent = (len(name_cell) - len(name_cell.lstrip(' ')) - 1) // 2
        name = name_cell.strip()
        try:
            lut, ff = int(cells[3]), int(cells[7])
        except (ValueError, IndexError):
            continue
        del stack[indent:]
        stack.append(name)
        if name.startswith('('):
            key = '/'.join(stack[:-1]) + '/(self)'
        else:
            key = '/'.join(stack)
        if indent <= depth:
            rows[key] = (lut, ff)
    return rows


base_path, head_path = sys.argv[1], sys.argv[2]
depth = int(sys.argv[3]) if len(sys.argv) > 3 else 2
base, head = parse(base_path, depth), parse(head_path, depth)
keys = sorted(set(base) | set(head),
              key=lambda k: -abs(head.get(k, (0, 0))[0] - base.get(k, (0, 0))[0]))
print(f'{"instance":70} {"LUT base":>9} {"LUT head":>9} {"dLUT":>6} {"FF base":>8} {"FF head":>8} {"dFF":>6}')
for k in keys:
    b, h = base.get(k), head.get(k)
    bl, bf = b if b else (0, 0)
    hl, hf = h if h else (0, 0)
    if b and h and (hl - bl, hf - bf) == (0, 0):
        continue
    tag = '' if (b and h) else ('  (head only)' if h else '  (base only)')
    print(f'{k:70} {bl:9} {hl:9} {hl - bl:+6} {bf:8} {hf:8} {hf - bf:+6}{tag}')
