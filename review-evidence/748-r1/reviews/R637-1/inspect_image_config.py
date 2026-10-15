#!/usr/bin/env python3
"""Read public registry configuration without starting or changing a container."""
import hashlib
import json
from pathlib import Path
import sys
import urllib.request
BASE = "https://registry-1.docker.io/v2/catthehacker/ubuntu/"
TOKEN_URL = "https://auth.docker.io/token?service=registry.docker.io&scope=repository:catthehacker/ubuntu:pull"
with urllib.request.urlopen(TOKEN_URL, timeout=30) as response:
    token = json.load(response)["token"]
accept = ", ".join(("application/vnd.oci.image.index.v1+json", "application/vnd.docker.distribution.manifest.list.v2+json", "application/vnd.oci.image.manifest.v1+json", "application/vnd.docker.distribution.manifest.v2+json"))
def fetch(path):
    request = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer " + token, "Accept": accept})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
    return json.loads(raw), "sha256:" + hashlib.sha256(raw).hexdigest()
index, tag_digest = fetch("manifests/full-latest")
manifest_digest = tag_digest
if "manifests" in index:
    chosen = next(m for m in index["manifests"] if m.get("platform", {}).get("os") == "linux" and m.get("platform", {}).get("architecture") == "amd64")
    manifest_digest = chosen["digest"]
    index, actual = fetch("manifests/" + manifest_digest)
    assert actual == manifest_digest
config_digest = index["config"]["digest"]
config, actual = fetch("blobs/" + config_digest)
assert actual == config_digest
result = {"image": "catthehacker/ubuntu:full-latest", "tag_digest": tag_digest, "amd64_manifest_digest": manifest_digest, "config_digest": config_digest, "created": config.get("created"), "env": config["config"]["Env"], "note": "Current public registry configuration only; not a claim about a replay container."}
print(json.dumps(result, indent=2))
