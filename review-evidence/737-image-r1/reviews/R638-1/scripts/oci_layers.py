#!/usr/bin/env python3
"""Read a `docker save` OCI archive: map history to layers, summarise or diff layer members.

usage: oci_layers.py summary <archive>
       oci_layers.py diff <archiveA> <archiveB>
       oci_layers.py scan <archive> <regex>...   (content and metadata privacy scan)
"""
import gzip, hashlib, io, json, re, sys, tarfile

def open_image(path):
    outer = tarfile.open(path)
    def blob(digest):
        return outer.extractfile("blobs/" + digest.replace(":", "/")).read()
    index = json.loads(outer.extractfile("index.json").read())
    desc = index["manifests"][0]
    manifest = json.loads(blob(desc["digest"]))
    if "manifests" in manifest:
        manifest = json.loads(blob(manifest["manifests"][0]["digest"]))
    config = json.loads(blob(manifest["config"]["digest"]))
    hist = [h for h in config["history"] if not h.get("empty_layer")]
    layers = []
    for i, (layer, h) in enumerate(zip(manifest["layers"], hist)):
        layers.append({"index": i, "digest": layer["digest"], "media": layer["mediaType"],
                       "created_by": h.get("created_by", "")[:120], "created": h.get("created"),
                       "data": lambda d=layer["digest"]: blob(d)})
    return outer, manifest, config, layers

def members(data):
    raw = gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data
    with tarfile.open(fileobj=io.BytesIO(raw)) as t:
        for m in t.getmembers():
            content = t.extractfile(m).read() if m.isfile() else b""
            yield m, content

def summary(path):
    _, manifest, config, layers = open_image(path)
    print(json.dumps({"config_created": config.get("created"), "env": config["config"].get("Env"),
                      "labels": config["config"].get("Labels"), "user": config["config"].get("User")}))
    for l in layers:
        print(l["index"], l["digest"][7:19], l["created"], l["created_by"])

def diff(pa, pb):
    _, _, ca, la = open_image(pa)
    _, _, cb, lb = open_image(pb)
    for a, b in zip(la, lb):
        ma = {m.name: (m, hashlib.sha256(c).hexdigest()) for m, c in members(a["data"]())}
        mb = {m.name: (m, hashlib.sha256(c).hexdigest()) for m, c in members(b["data"]())}
        names = sorted(set(ma) | set(mb))
        content, meta, only = [], 0, []
        mtime_only = 0
        for n in names:
            if n not in ma or n not in mb:
                only.append(n); continue
            (x, hx), (y, hy) = ma[n], mb[n]
            if hx != hy or x.linkname != y.linkname or x.mode != y.mode:
                content.append(n)
            elif x.mtime != y.mtime:
                mtime_only += 1
        print(json.dumps({"layer": a["index"], "by": a["created_by"][:60], "members": len(names),
                          "same_digest": a["digest"] == b["digest"], "content_or_mode_diff": len(content),
                          "mtime_only_diff": mtime_only, "present_in_one_only": len(only),
                          "content_diff_examples": content[:12], "only_examples": only[:6]}))

def scan(path, patterns):
    _, manifest, config, layers = open_image(path)
    rx = re.compile("|".join(patterns).encode())
    meta_text = json.dumps(config).encode()
    for hit in sorted(set(m.group(0) for m in rx.finditer(meta_text))):
        print(json.dumps({"where": "config/history", "match": hit.decode(errors="replace")}))
    counts = {}
    for l in layers:
        for m, c in members(l["data"]()):
            for field in (m.name, m.linkname, m.uname, m.gname):
                if field and rx.search(field.encode()):
                    print(json.dumps({"layer": l["index"], "member": m.name, "field": field}))
            for hit in set(x.group(0) for x in rx.finditer(c)):
                key = (l["index"], hit)
                counts.setdefault(key, []).append(m.name)
            if m.uid not in (0,) or m.gid not in (0,):
                counts.setdefault((l["index"], b"<non-root owner %d:%d>" % (m.uid, m.gid)), []).append(m.name)
    for (layer, hit), files in sorted(counts.items()):
        print(json.dumps({"layer": layer, "match": hit.decode(errors="replace"), "files": len(files),
                          "examples": files[:5]}))

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "summary": summary(sys.argv[2])
    elif mode == "diff": diff(sys.argv[2], sys.argv[3])
    elif mode == "scan": scan(sys.argv[2], sys.argv[3:])
