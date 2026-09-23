#!/usr/bin/env python3
"""Each committed fixture shape's recorded headings against the base, previous
and head walks: which shapes agreed at the base and whether they still agree,
plus the r86_5 mapping of the family-one set.

Usage: fixture_base_check.py <clone> <scratch-dir>
"""
import json
import subprocess
import sys

HELPER = ("import json,sys;sys.path.insert(0,sys.argv[1]);import gen_toc;"
          "print(json.dumps([[[l,r] for l,r,_ in gen_toc.headings(p)] for p in json.load(sys.stdin)]))")
clone, scratch = sys.argv[1:3]
for fixture in ("gen_toc_family_one.json", "gen_toc_comment_shapes.json", "gen_toc_container_walk.json"):
    shapes = json.load(open(f"{clone}/scripts/{fixture}", encoding="ascii"))["shapes"]
    walks = {label: json.loads(subprocess.run(
        [sys.executable, "-B", "-c", HELPER, f"{scratch}/walk_{label}/scripts"],
        input=json.dumps([s["page"] for s in shapes]).encode(), capture_output=True, check=True).stdout)
        for label in ("base", "prev", "head")}
    agree = {label: [w == s["headings"] for w, s in zip(walks[label], shapes)] for label in walks}
    lost = [s["name"] for s, b, h in zip(shapes, agree["base"], agree["head"]) if b and not h]
    print(f"{fixture}: {len(shapes)} shapes; agree base {sum(agree['base'])}, prev {sum(agree['prev'])}, "
          f"head {sum(agree['head'])}; agreed at base but not at head: {lost}")
    mapped = sorted({s["r86_5"] for s in shapes if s.get("r86_5")})
    if mapped:
        print(f"  r86_5 descriptions mapped: {len(mapped)}: {mapped}")
    named = [s["name"] for s in shapes if "#516" in s["name"]]
    if named:
        print(f"  #516 variants: {len(named)}; head agrees on all: "
              f"{all(a for s, a in zip(shapes, agree['head']) if '#516' in s['name'])}")
