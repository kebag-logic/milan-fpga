import re, sys
RUN = re.compile(r'^ (?:\S*/cc1\w*|"[^"]*" -cc1) .*?(?<= )-E(?: |$)')
MARK = re.compile(r'^# [01] "(?:[01]\.c)"$')
err = open(sys.argv[1]).read().splitlines(); out = open(sys.argv[2]).read().splitlines()
print("runs", sum(1 for l in err if RUN.match(l)), "mains", len({l for l in out if MARK.match(l)}), "stdout lines", len(out))
