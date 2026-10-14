"""List source-lock rows whose staged download filename is shared."""
import collections, json, sys
d = json.load(open(sys.argv[1]))
rows = [("debs/" + r["filename"], r) for r in d["packages"]] + [(r["filename"], r) for r in d["sources"]]
groups = collections.defaultdict(list)
for name, row in rows:
    groups[name].append(row)
dups = {k: v for k, v in groups.items() if len(v) > 1}
print("rows", len(rows), "distinct filenames", len(groups), "shared filenames", len(dups))
for k, v in sorted(dups.items())[:10]:
    print(k, [(r["tool"], r["sha256"][:12], r["url"][-60:]) for r in v])
