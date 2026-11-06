#!/usr/bin/env python3
"""Independent audit at the head: per mutant, the expect line that first fails its named check; parity of MUTANTS, the
README rule table, and the author's rule table. usage: audit_names.py <clone> <author mutant_rules.json> <author rule_table_check.md>"""
import ast, json, re, sys
from contextlib import ExitStack
from pathlib import Path
root = Path(sys.argv[1]).resolve()
H = root / 'tb/verilator/ctrl_service_hooks'
sys.dont_write_bytecode = True
sys.path.insert(0, str(H))
import hooks_selftest as s
fired = {}
orig = s.expect
last = []
def rec(cond, why=''):
    if not cond and not last:
        f = sys._getframe(1)
        last.append((f.f_lineno, f.f_code.co_name))
    return orig(cond, why)
s.expect = rec
names = [m[0] for m in s.MUTANTS]
print('mutants', len(names), 'unique', len(set(names)), 'checks', len(s.CHECKS))
exc = []
for name, make, named in s.MUTANTS:
    last.clear()
    with ExitStack() as st:
        st.enter_context(make())
        try:
            s.CHECKS[named]()
            res = 'NOT FAILED'
        except s.Failed:
            res = 'expect'
        except Exception as e:  # noqa
            res = f'EXC {type(e).__name__}'
            exc.append(name)
    fired[name] = (last[0] if last else None, res, named)
src = (H / 'hooks_selftest.py').read_text()
tree = ast.parse(src)
sites = sorted({n.lineno for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'expect'})
hit = {v[0][0] for v in fired.values() if v[0]}
print('expect call sites', len(sites), 'fired first by a mutant', len(hit & set(sites)), 'fired by none', len(set(sites) - hit))
# the sites in functions that are named checks or reached from them, as a second count
print('not expect-failed:', {k: v[1] for k, v in fired.items() if v[1] != 'expect'})
for n in ('supersede: the table names another group', 'supersede: the table names a second path',
          'supersede: a row of another path supersedes a refusal', 'supersede: every refusal is superseded',
          'bound: the margin is taken from a timeout of zero', 'held missing: its finding by name is dropped',
          'buckets: the window opens right after the registrations (the earlier rule)'):
    print(n, '->', fired[n])
print('L638-site fired by:', [k for k, v in fired.items() if v[0] and 636 <= v[0][0] <= 640])
readme = (H / 'README.md').read_text()
rows = re.findall(r'^\| (.+?) \| (.+?) \|$', readme, re.M)
table = {a.replace('\\|', '|'): b for a, b in rows}
miss = [(n, c) for n, _, c in s.MUTANTS if table.get(n) != c]
print('README rows disagreeing with MUTANTS:', miss)
in_rd = [k for k in table if re.match(r'^[a-zA-Z\- ]+[^|]*: ', k)]
print('README mutant-like rows not in MUTANTS:', [k for k in in_rd if k not in names])
rules = json.loads(Path(sys.argv[2]).read_text())
print('rules keys == MUTANTS:', set(rules) == set(names), 'order equal', list(rules) == names)
md = Path(sys.argv[3]).read_text().splitlines()
kinds, twins, firesd = {}, 0, []
wraps = 0
for line in md:
    c = [x.strip() for x in line.strip().strip('|').split(' | ')]
    if len(c) >= 6 and c[0] in names:
        k = c[2]
        wraps += k.startswith('wraps')
        twins += c[5] != '-'
        kinds[k.split()[0]] = kinds.get(k.split()[0], 0) + 1
        line_no = int(c[3].lstrip('L')) if c[3].startswith('L') else None
        got = fired[c[0]][0][0] if fired[c[0]][0] else None
        if line_no != got:
            firesd.append((c[0], line_no, got))
print('author table: kinds', kinds, 'wraps', wraps, 'twins', twins, 'fires disagreeing with mine:', firesd)
