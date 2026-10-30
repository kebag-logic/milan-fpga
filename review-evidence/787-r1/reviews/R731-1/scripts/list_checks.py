import json, sys
d = json.load(open(sys.argv[1]))
print("total", d["total_count"])
for c in sorted(d["check_runs"], key=lambda c: c["name"]):
    print("%-62s %-10s %-10s %s" % (c["name"][:62], c["status"], c["conclusion"], c["head_sha"][:8]))
