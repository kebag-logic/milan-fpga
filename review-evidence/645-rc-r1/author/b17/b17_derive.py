import json, sys, glob
rows = []
for f in sorted(glob.glob(sys.argv[1] + "/c*.json")):
    d = json.load(open(f))
    pr = d["tap"]["priming"]
    sl = d["poll"]["slips"][0]
    late = d["tap"]["late_pdus"]
    # bursts: group late PDUs closer than 5 ms
    bursts = []
    for p in late:
        if bursts and p["s"] - bursts[-1][-1]["s"] < 0.005:
            bursts[-1].append(p)
        else:
            bursts.append([p])
    b = [(round(x[0]["s"], 4), max(y["late_us"] for y in x), len(x)) for x in bursts]
    pre = [x for x in b if x[0] < sl["s_lo"]]
    ins = [x for x in b if sl["s_lo"] <= x[0] <= sl["s_hi"]]
    post = [x for x in b if x[0] > sl["s_hi"]]
    print(d["cycle"], "first_pdu_ms", pr["first_pdu_after_command_ms"], "first_phase_us", pr["first_pdu_phase_us_mod_pdu"],
          "first_phase_tick", pr["first_pdu_phase_tick"], "p50_tick", pr["phase_tick"]["p50"],
          "late p999", pr["lateness_us"]["p999"], "max", pr["lateness_us"]["max"],
          "slip", sl["s_lo"], sl["s_hi"], "pre", pre, "in", ins[:3], "n_in", len(ins), "post_max", max([x[1] for x in post] or [0]), "n_post", len(post),
          "first_burst", b[0] if b else None)
