"""Experiment: put R763-10's EXTRA listings at a chosen place and add the F1 mutant (scratch only)."""
import sys
from pathlib import Path
tree, where = Path(sys.argv[1]), sys.argv[2]
test = tree / "scripts/test_suite_cancellation.py"
text = test.read_text()
EXTRA = '''        for words, under in (("a stubborn parent beside a stopped shell", owner_pid),
                             ("a stubborn parent under a stopped shell", shell)):
            kept(words, lambda _clock, under=under: {shell: (owner_pid, "2"), parent: (under, "5"),
                                                     child: (parent, "4")},
                 [(0, "SIGTERM", "parent"), (0, "SIGTERM", "child"), (2, "SIGKILL", "child"),
                  (4, "SIGKILL", "parent"), *[(14, "SIGKILL", n) for n in ("shell", "parent", "child")],
                  (14, "verdict")], shell)
'''
anchors = {"early": '              (14, "SIGKILL", "parent"), (14, "SIGKILL", "child"), (14, "verdict")])\n',
           "end": '            kept(f"a lone {when} resume", cell(resume), window(resume, ("shell",)), shell)\n    print("owner-stated'}
a = anchors[where]
assert text.count(a) == 1
if where == "early":
    text = text.replace(a, a + EXTRA)
else:
    head = '            kept(f"a lone {when} resume", cell(resume), window(resume, ("shell",)), shell)\n'
    text = text.replace(a, head + EXTRA + '    print("owner-stated')
test.write_text(text)
sup = tree / "scripts/process_test_support.py"
s = sup.read_text()
end = '''         " (self.root_notified and resumed is None and owned[pid][0] == root_pid):")),
}'''
assert s.count(end) == 1
s = s.replace(end, end[:-1] + '''    "first-census-parent-unspared-beside-shell": ("owner_stated_seconds", "a stubborn parent beside a stopped shell's",
        ("if any(parent == pid and child in live for child, (parent, _start) in owned.items()):",
         "if any(parent == pid and child in live and not (self.root_notified and (child, _start) in"
         " initial) for child, (parent, _start) in owned.items()):")),
}''')
sup.write_text(s)
print("placed", where)
