import json, sys, glob
slopes = []
for f in sorted(glob.glob(sys.argv[1] + "/c*.json")):
    d = json.load(open(f))
    late = d["tap"]["late_pdus"]
    first = [late[0]]
    for p in late[1:]:
        if p["s"] - first[-1]["s"] < 0.0002: first.append(p)
        else: break
    n = len(first)
    xs = list(range(n)); ys = [p["late_us"] for p in first]
    mx = sum(xs)/n; my = sum(ys)/n
    sl = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sum((x-mx)**2 for x in xs)
    sp = [round((b["s"]-a["s"])*1e6, 1) for a, b in zip(first, first[1:])]
    slopes.append(sl)
    pr = d["tap"]["priming"]
    print(d["cycle"], "n", n, "peak", max(ys), "slope_us_per_pdu", round(sl, 3), "spacing_us", min(sp), max(sp),
          "burst_after_first_pdu_s", round(first[0]["s"] - pr["first_pdu_after_command_ms"] / 1e3, 4))
print("mean slope", round(sum(slopes)/len(slopes), 3), "min", round(min(slopes), 3), "max", round(max(slopes), 3))
