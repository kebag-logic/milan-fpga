#!/usr/bin/env python3
"""Reviewer mutation probes against the #509 audit script.

Usage: mutation_probes.py <clean-tree> <scratch-dir>
Each mutant is a fresh disposable copy of <clean-tree>; one file is edited in
it, then the audit (and for M3 a fresh-process CLI run) is executed there.
M1  processor packer normalizes the last byte of every descriptor body
    -> the audit must refuse to report 'accepted' (assert_packed_bytes / decoder).
M2  processor packer refuses AUDIO_UNIT sampling_rates_offset != 144
    -> the 'offset 143' packer probe must flip to 'refused', others unchanged.
M3  builder model_shape() hashes the IDENTIFY CONTROL bytes (a simulated #495 fix)
    -> compare the audit's in-process identity probe with a fresh-process
       regeneration after the same on-disk reset_time edit.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def mutant(clean: Path, scratch: Path, name: str, rel: str, old: str, new: str) -> Path:
    """Copy the clean tree and apply one exact, unique text replacement."""
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(clean, tree, symlinks=True)
    path = tree / rel
    text = path.read_text()
    assert text.count(old) == 1, (name, rel)
    path.write_text(text.replace(old, new))
    return tree


def audit(tree: Path, out: Path) -> dict:
    """Run the audit in a tree; return exit status and parsed receipt if any."""
    cp = subprocess.run([sys.executable, "-B", "scripts/audit_pp_descriptors.py", "--output", str(out)],
                        cwd=tree, capture_output=True, text=True, timeout=1800)
    res = dict(rc=cp.returncode, tail=(cp.stdout + cp.stderr).strip().splitlines()[-3:])
    if cp.returncode == 0:
        res["report"] = json.loads(out.read_text())
    return res


def main() -> None:
    clean, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    packer = "protocol-processor/hdl/aecp/desc/gen_desc_image.py"
    results = {}

    t = mutant(clean, scratch, "m1", packer,
               "        img[off:off + len(body)] = body\n",
               "        img[off:off + len(body)] = body[:-1] + b'\\x00'\n")
    r = audit(t, scratch / "m1.json")
    results["M1_packer_normalizes_last_byte"] = dict(rc=r["rc"], tail=r["tail"])

    t = mutant(clean, scratch, "m2", packer,
               "    entries = _index_entries(_grouped_descriptors(model), names, line_bytes)\n",
               "    for _d in model.get('descriptors', []):\n"
               "        if _u(_d.get('type', 0)) == 2 and int(_d['bytes'][280:284], 16) != 144:\n"
               "            raise ImageError('reviewer mutant: AUDIO_UNIT rates offset != 144')\n"
               "    entries = _index_entries(_grouped_descriptors(model), names, line_bytes)\n")
    r = audit(t, scratch / "m2.json")
    rows = {p["probe"]: p["result"] for p in r.get("report", {}).get("packer_probes", [])}
    base = {p["probe"]: p["result"] for p in json.loads((scratch.parent / "receipts" / "audit-run1.json")
                                                         .read_text())["packer_probes"]}
    results["M2_packer_refuses_offset"] = dict(rc=r["rc"], flipped={k: [base[k], v] for k, v in rows.items()
                                                                       if base.get(k) != v})

    t = mutant(clean, scratch, "m3", "sw/builder/endstation_builder.py",
               '        "aem_layout": AEM_LAYOUT_REV,\n',
               '        "aem_layout": AEM_LAYOUT_REV,\n'
               '        "identify_bytes": __import__("aem_descriptors").d_control_identify().hex(),\n')
    r = audit(t, scratch / "m3.json")
    ip = r.get("report", {}).get("identity_probe", {})
    results["M3_audit_identity_probe"] = dict(
        rc=r["rc"], tail=r["tail"], changed_offsets=ip.get("changed_offsets"),
        before_model_id=ip.get("before_entity", {}).get("model_id"),
        after_model_id=ip.get("after_entity", {}).get("model_id"))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
