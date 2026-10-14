#!/usr/bin/env python3
"""Reviewer-owned, independent privacy and metadata scan of an exported OCI image.

Usage: scan_image.py <image.tar> <out.json> <needles-file>
The needles file holds one lowercase needle per line; it is NOT published.
The report records needle index, layer, member-path hash, member sha256 and a
short redacted context class only, never the protected bytes themselves.
"""
import collections, gzip, hashlib, json, re, sys, tarfile

archive_path, out_path, needles_path = sys.argv[1:4]
needles = [l.strip().encode() for l in open(needles_path, encoding="utf-8") if l.strip()]
report = {"layers": [], "config": {}, "hits": []}
with tarfile.open(archive_path) as archive:
    index = json.load(archive.extractfile("index.json"))
    desc = index["manifests"][0]
    manifest = json.load(archive.extractfile("blobs/" + desc["digest"].replace(":", "/")))
    raw_cfg = archive.extractfile("blobs/" + manifest["config"]["digest"].replace(":", "/")).read()
    cfg = json.loads(raw_cfg)
    report["manifest"] = desc["digest"]
    report["config"] = {"digest": manifest["config"]["digest"], "Env": cfg["config"].get("Env"),
                        "Labels": cfg["config"].get("Labels"), "User": cfg["config"].get("User"),
                        "WorkingDir": cfg["config"].get("WorkingDir"), "Cmd": cfg["config"].get("Cmd"),
                        "Entrypoint": cfg["config"].get("Entrypoint"), "created": cfg.get("created"),
                        "history": cfg.get("history"), "manifest_annotations": manifest.get("annotations")}
    low = raw_cfg.lower()
    report["config"]["needle_hits"] = [i for i, n in enumerate(needles) if n in low]
    for n, layer in enumerate(manifest["layers"]):
        stats = collections.Counter()
        uids, unames, maxmtime, minmtime = set(), set(), 0, 1 << 62
        stream = archive.extractfile("blobs/" + layer["digest"].replace(":", "/"))
        with tarfile.open(fileobj=gzip.GzipFile(fileobj=stream), mode="r|") as t:
            for m in t:
                stats[m.type.decode()] += 1
                uids.add((m.uid, m.gid)); unames.add((m.uname, m.gname))
                maxmtime = max(maxmtime, int(m.mtime)); minmtime = min(minmtime, int(m.mtime))
                meta = (m.name + "\0" + m.linkname + "\0" + m.uname + "\0" + m.gname).lower().encode()
                for i, nd in enumerate(needles):
                    if nd in meta:
                        report["hits"].append({"layer": n, "where": "metadata", "needle": i,
                                               "path": m.name})
                for key in (m.pax_headers or {}):
                    stats["pax:" + key] += 1
                if m.isfile():
                    f = t.extractfile(m)
                    h = hashlib.sha256(); tail = b""; found = set()
                    while chunk := f.read(1 << 20):
                        h.update(chunk)
                        buf = (tail + chunk).lower()
                        for i, nd in enumerate(needles):
                            if i not in found and nd in buf:
                                found.add(i)
                        tail = (tail + chunk)[-256:]
                    for i in sorted(found):
                        report["hits"].append({"layer": n, "where": "content", "needle": i, "path": m.name,
                                               "sha256": h.hexdigest(), "size": m.size})
        report["layers"].append({"index": n, "digest": layer["digest"], "types": dict(stats),
                                 "uid_gid": sorted(uids), "uname_gname": sorted(unames),
                                 "min_mtime": minmtime, "max_mtime": maxmtime})
json.dump(report, open(out_path, "w"), indent=1, sort_keys=True)
c = collections.Counter((h["needle"], h["where"]) for h in report["hits"])
print("hits by (needle, where):", dict(c))
for l in report["layers"]:
    print(l["index"], l["digest"][:19], l["types"].get("0", 0), l["uid_gid"][:4], l["uname_gname"][:4],
          l["min_mtime"], l["max_mtime"], [k for k in l["types"] if k.startswith("pax:")])
print("config needle hits:", report["config"]["needle_hits"])
