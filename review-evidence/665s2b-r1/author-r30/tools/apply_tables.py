"""Write tables29.py's tables into the tree's literals, value by value, each literal's layout kept: load_grade.py's
STATED_US and STATED_US_DONOR at 1x1/1if and 8x8/2if, and poll_grade.py's STATED_US at one and two interfaces.
Refuses a key the literal does not hold. usage: python3 -I apply_tables.py LANE TABLES_JSON"""
import json
import re
import sys
from pathlib import Path

lane, tables = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
H = lane / 'tb/verilator/ctrl_service_budget'


def block(text, name, point):
    """The span of `point`'s dict inside the literal `name`."""
    start = text.index(f'\n{name} = {{')
    at = text.index(f"'{point}': {{", start) if isinstance(point, str) else text.index(f'{point}: dict(', start)
    end = text.index('}' if isinstance(point, str) else ')', at)
    return at, end


def put(text, name, point, values, keyform):
    at, end = block(text, name, point)
    part = text[at:end]
    for key, value in values.items():
        pat = keyform(key)
        found = re.findall(pat, part)
        if len(found) != 1:
            sys.exit(f'REFUSED {name} {point}: {key} found {len(found)} times')
        part = re.sub(pat, lambda m: m.group(1) + str(value), part)
    return text[:at] + part + text[end:]


lg = (H / 'load_grade.py').read_text()
for name in ('STATED_US', 'STATED_US_DONOR'):
    for point in ('1x1/1if', '8x8/2if'):
        lg = put(lg, name, point, tables[name][point], lambda k: r"('" + re.escape(k) + r"': )\d+")
(H / 'load_grade.py').write_text(lg)
pg = (H / 'poll_grade.py').read_text()
for n, point in (('1', 1), ('8', 2)):
    values = {k: v for k, v in tables['poll_grade'][n].items()}
    pg = put(pg, 'STATED_US', point, values, lambda k: r'(\b' + re.escape(k) + r'=)\d+')
(H / 'poll_grade.py').write_text(pg)
print('applied')
