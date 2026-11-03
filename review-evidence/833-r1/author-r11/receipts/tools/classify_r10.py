"""Group sweep survivors and mark which red probe cells are cells a repository listing lists."""
import ast, collections, sys
CLAIMED = {f"shell resume={r} new={k}" for r in ("first", "second", "last-in-grace", "first-past", "second-past", "last-pass") for k in ("none", "fake", "live")}
CLAIMED |= {"shell resume=one new=none", "shell resume=one new=fake", "shell resume=next-to-last-in-grace new=fake",
            "shell resume=next-to-last-in-grace new=live", "shell resume=three new=fake", "shell resume=five-half new=fake",
            "shell resume=ten new=none", "shell never new=none", "shell never new=fake", "shell live-new-holds gone=3",
            "noshell survivor=fake new=none", "noshell survivor=fake new=fake", "noshell survivor=fake new=live",
            "shell resume=one new=live", "shell never new=live"}  # round 10: S1.1 and F2 (S1.2)
g = collections.defaultdict(lambda: [[], set()])
for line in open(sys.argv[1]):
    if ": SURVIVOR" in line:
        name, rest = line.split(": SURVIVOR")
        cells = ast.literal_eval(rest.split("cells=")[1])
        p, c, l, s = name.split("|")
        g[(p, c)][0].append(f"{l}/{s}")
        g[(p, c)][1] |= set(cells)
for k in sorted(g):
    variants, cells = g[k]
    hit = sorted(cells & CLAIMED)
    print(f"{'LISTED-CELL ' if hit else 'unlisted    '}{'|'.join(k)} [{len(variants)} variants] listed={hit} unlisted={sorted(cells - CLAIMED)}")
