"""Compare run_suite's phase sequences at two revisions of the engine harness.

usage: python3 -I phase_lists.py <old sim_main.cpp> <new sim_main.cpp>
Old: the self-publication branch and the fall-through list inside run_suite.
New: the bodies of run_the_self_publication_phases and run_every_phase.
"""
import re, sys

def body(text, start_re):
    m = re.search(start_re, text)
    i = text.index("{", m.end() - 1)
    depth, j = 0, i
    while True:
        depth += {"{": 1, "}": -1}.get(text[j], 0)
        if depth == 0:
            return text[i + 1:j]
        j += 1

def stmts(block):
    return [s.strip() for s in re.sub(r"//[^\n]*", "", block).split(";") if s.strip()]

old, new = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
ob = body(old, r"int run_suite\(\) \{")
branch = body(ob, r"if \(self_present == 0\) \{")
rest = ob[ob.index(branch) + len(branch) + 1:]
o_self, o_all = stmts(branch), stmts(rest)
n_self = stmts(body(new, r"void run_the_self_publication_phases\(\) \{"))
n_all = stmts(body(new, r"void run_every_phase\(\) \{"))
n_suite = stmts(body(new, r"int run_suite\(\) \{"))
print("old self branch", len(o_self), "statements; old fall-through", len(o_all))
print("new self", len(n_self), "; new every", len(n_all))
print("old self minus tally/return == new self:", o_self[:-2] == n_self, o_self[-2:])
print("old fall-through minus tally/return == new every:", o_all[:-2] == n_all, o_all[-2:])
print("new run_suite:", n_suite)
print("any return/exit/goto/break in new phase lists:",
      any(re.match(r"(return|exit|goto|break)\b", s) for s in n_self + n_all))
