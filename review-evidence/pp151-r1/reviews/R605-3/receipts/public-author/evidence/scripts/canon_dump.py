import re, sys
text = open(sys.argv[1]).read()
text = re.sub(r"all\.v:[0-9]+(\.[0-9]+-[0-9]+\.[0-9]+)?", "all.v:L", text)
seen = {}
text = re.sub(r"\$([0-9]+)(?![0-9A-Za-z_'])", lambda m: "$" + str(seen.setdefault(m.group(1), len(seen))), text)
sys.stdout.write(text)
