import hashlib, json, pathlib, tarfile, sys
first, second = map(pathlib.Path, sys.argv[1:3])
def metadata(path):
    archive = tarfile.open(path / "image.tar")
    def blob(digest): return archive.extractfile("blobs/"+digest.replace(":", "/"))
    def obj(row):
        data = blob(row["digest"]).read()
        assert len(data) == row["size"]
        assert "sha256:"+hashlib.sha256(data).hexdigest() == row["digest"]
        return json.loads(data)
    index = json.load(archive.extractfile("index.json")); assert len(index["manifests"]) == 1
    descriptor = index["manifests"][0]; manifest = obj(descriptor)
    if "manifests" in manifest:
        selected = [r for r in manifest["manifests"] if r.get("platform", {}).get("architecture") == "amd64"]
        assert len(selected) == 1
        descriptor = selected[0]; manifest = obj(descriptor)
    config = obj(manifest["config"])
    for layer in manifest["layers"]:
        with blob(layer["digest"]) as stream: digest = "sha256:"+hashlib.file_digest(stream,"sha256").hexdigest()
        assert digest == layer["digest"]
    archive.close()
    receipt = json.loads((path/"validation-tools.receipt.json").read_text())
    assert receipt["image_digest"] == descriptor["digest"]
    assert receipt["image_id"] == manifest["config"]["digest"]
    return {"manifest":descriptor["digest"],"config":manifest["config"]["digest"],
            "layers":[r["digest"] for r in manifest["layers"]],"diff_ids":config["rootfs"]["diff_ids"],
            "recipe":receipt["recipe_sha256"],"build_ms":receipt["build_ms"],"size_bytes":receipt["size_bytes"]}
a,b = metadata(first),metadata(second)
for key in ("manifest","config","layers","diff_ids","recipe","size_bytes"): assert a[key] == b[key], key
report={"cold_a":a,"cold_b":b,"identical_manifest_config_and_all_layers":True,"cold_builds":2,
        "scope":"same host, BuildKit no-cache for both; source download cache reused and checksum verified"}
pathlib.Path(sys.argv[3]).write_text(json.dumps(report,indent=2)+"\n")
print("PASS: identical manifest, config and all "+str(len(a["layers"]))+" authenticated OCI layers")
