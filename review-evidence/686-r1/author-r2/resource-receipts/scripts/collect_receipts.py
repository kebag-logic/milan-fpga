#!/usr/bin/env python3
"""Collect the raw receipts of one pp_resource_gate.py record (issue #686, R549-1-F4).

usage: collect_receipts.py <repo> <measurement-dir> <endpoint> <out-dir>

Run from a checkout whose tree is the one the measurement read. Writes into
<out-dir>:
  record.json            pp_resource_gate.py record output for the directory
  inputs.manifest.json   every digest component in digest order: file name,
                         role (repo / generated / measurement / external), repo-relative
                         path for repo files, sha256 of the digested bytes;
                         then the generics and the memory-image list
  inputs/<role>/...      the digested bytes of every non-repo input (the
                         exporter's files after the gate's own normalisation),
                         gzipped above 200 KB
  <script>.tcl           the executed recipe script
  reports                utilization, hierarchy, route status, clock.xdc,
                         baseline_images.json, the Design Timing Summary
                         excerpt and the CARRY4 rows of the primitive census
  logs                   the Vivado log, gzipped
  files.sha256           sha256 and size of every original artifact, the
                         large ones that are not copied included
Host path prefixes in copied text are replaced by role placeholders; the
manifest records the digest of the bytes the gate digests, so the
replacement does not reach any value a record holds.
"""
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

LIMIT = 200 * 1024


def main() -> int:
    repo, mdir, endpoint, out = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                                 sys.argv[3], Path(sys.argv[4]).resolve())
    sys.path.insert(0, str(repo / "syn/ooc"))
    import pp_resource_gate as gate  # noqa: E402 (repository module at the measured tree)

    out.mkdir(parents=True, exist_ok=True)
    kind = gate.kind_of(mdir)
    script_name = gate.SCRIPTS[kind]
    script = (mdir / script_name).read_text()
    rec = gate.record(mdir, kind)
    files, roots = gate.located(mdir, script)
    prefixes = [(str(repo), "<repo>"), (str(mdir), "<measurement>"),
                (roots[0], "<generated>"), (str(Path.home()), "<home>")]

    def redact(text: str) -> str:
        for prefix, role in sorted(prefixes, key=lambda p: -len(p[0])):
            text = text.replace(prefix, role)
        return text

    def put(rel: str, data: bytes) -> str:
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if len(data) > LIMIT:
            target = target.with_name(target.name + ".gz")
            target.write_bytes(gzip.compress(data, 9, mtime=0))
        else:
            target.write_bytes(data)
        return str(target.relative_to(out))

    entries = []
    digest = hashlib.sha256()
    for path in files:
        data = path.read_bytes()
        if str(path).startswith(roots[0] + "/"):
            text = re.sub(r"//[^\n]*", "", data.decode(errors="replace"))
            for index, root in enumerate(roots):
                text = text.replace(root, f"$ROOT{index}")
            data = text.encode()
        sha = hashlib.sha256(data).hexdigest()
        digest.update(path.name.encode() + b"\0" + hashlib.sha256(data).digest())
        entry = {"name": path.name, "sha256": sha}
        if str(path).startswith(roots[0] + "/"):
            role = "generated"
        elif str(path).startswith(str(mdir) + "/"):
            role = "measurement"
        elif str(path).startswith(str(repo) + "/"):
            role = "repo"
        else:
            role = "external"  # the CPU core the LiteX environment supplies
        entry["role"] = role
        if role == "repo":
            entry["path"] = str(path.relative_to(repo))
        else:
            entry["copy"] = put(f"inputs/{role}/{len(entries):03d}_{path.name}", data)
        entries.append(entry)
    generics = gate.GENERICS.findall(script)
    for generic in generics:
        digest.update(re.sub(r'"[^"]*/([^/"]+)"', r'"\1"', generic).encode() + b"\0")
    images = json.loads((mdir / "baseline_images.json").read_text())
    for image in sorted(images, key=lambda row: Path(row["path"]).name):
        digest.update(f"{Path(image['path']).name}\0{image['sha256']}\0".encode())
    if digest.hexdigest() != rec["inputs_sha256"]:
        print("manifest digest does not reproduce the record's inputs_sha256")
        return 1
    manifest = {"endpoint": endpoint, "kind": kind, "inputs_sha256": rec["inputs_sha256"],
                "files": entries,
                "generics": [re.sub(r'"[^"]*/([^/"]+)"', r'"\1"', g) for g in generics],
                "images": [{"name": Path(i["path"]).name, "sha256": i["sha256"]}
                           for i in sorted(images, key=lambda row: Path(row["path"]).name)]}
    (out / "inputs.manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    (out / "record.json").write_text(json.dumps(rec, indent=1) + "\n")

    sums = []
    small = [script_name, "baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_images.json"]
    small += [p.name for p in sorted(mdir.glob("*_route_status.rpt"))]
    small += ["clock.xdc"] if (mdir / "clock.xdc").is_file() else []
    for name in small:
        put(name, redact((mdir / name).read_text()).encode())
    timing = (mdir / "baseline_timing.rpt").read_text()
    block = timing.split("| Design Timing Summary")
    head = [line for line in timing.splitlines()[:12] if not line.startswith("| Host")]
    excerpt = "| Design Timing Summary" + block[1].split("\n\n\n")[0] + "\n"
    (out / "baseline_timing.summary.rpt").write_text(redact("\n".join(head)) + "\n\n" + excerpt)
    cells = (mdir / "baseline_cells.tsv").read_text().splitlines()
    carry = [cells[0]] + [line for line in cells[1:] if line.endswith("\tCARRY4")]
    put("baseline_cells.carry4.tsv", ("\n".join(carry) + "\n").encode())
    put("baseline.log", redact((mdir / "baseline.log").read_text()).encode())
    for path in sorted(p for p in mdir.iterdir() if p.is_file()):
        data = path.read_bytes()
        sums.append(f"{hashlib.sha256(data).hexdigest()}  {len(data):>11}  {path.name}")
    (out / "files.sha256").write_text("\n".join(sums) + "\n")
    print(f"{endpoint}: {len(entries)} inputs, digest {rec['inputs_sha256']} reproduced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
