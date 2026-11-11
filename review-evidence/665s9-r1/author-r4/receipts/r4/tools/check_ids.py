"""check_ids.py <tree> [<base tree>]: every check ID of the mailbox suite (suite.hpp, suite_face.hpp) and the
functions whose labels carry it; an ID carried in two files, or in two functions of one file, is listed as shared.
Labels are the string literals that open with the ID (F4's face labels are built by label() in one function)."""
import re, sys
from collections import defaultdict
from pathlib import Path
def ids(tree):
    use, labels = defaultdict(set), defaultdict(set)
    for name in ("suite.hpp", "suite_face.hpp"):
        fn = "?"
        for line in (Path(tree) / "tb/verilator/mbx" / name).read_text().splitlines():
            m = re.match(r"\s*(?:[\w:<>&]+\s+)+([\w:]+)\s*\([^;]*\)\s*(?:const\s*)?\{\s*$", line)
            if m and m[1] not in ("if", "for", "while", "switch", "return"):
                fn = m[1]
            for i in re.findall(r'"([A-Z][0-9]{1,2})[ "]', line):
                use[i].add(f"{name}:{fn}")
                labels[i].add(re.search(r'"' + i + r'[^"]*"?', line)[0][:90])
    return use, labels
for tree in sys.argv[1:]:
    use, labels = ids(tree)
    print(f"=== {tree}: {len(use)} IDs")
    shared = {i: s for i, s in use.items() if len({x.split(':')[0] for x in s}) > 1 or len(s) > 1}
    for i in sorted(use, key=lambda k: (k[0], int(k[1:]))):
        print(f"{i:4s} {'IN TWO PLACES ' if i in shared else ''}{', '.join(sorted(use[i]))}")
        if i in shared:
            for l in sorted(labels[i]):
                print(f"       {l}")
