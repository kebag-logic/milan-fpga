#!/usr/bin/env python3
"""Round-2 reviewer mutants against the #509 audit's identity control and refusals.

Usage: round2_mutants.py <clean-tree> <scratch-dir>
Each mutant is a fresh disposable copy of <clean-tree> with one exact, unique
text replacement; the audit is then run there (optionally under python3 -O).
K1  identity probe generates 'after' from the pre-loaded config (the R330-1 M1 defect)
    -> the control must refuse (AuditError), normal and -O.
K2  the control's model_shape ignores the changed field
    -> the control must refuse.
K3  the probe patches only the assembler, not the descriptor module
    -> the control must refuse (its derivation cannot see the change).
K4  the probe patches only the descriptor module, not the assembler
    -> informational: does anything refuse when the packed image does not change?
K5  R330-1 M1 packer mutant (normalizes the last body byte), under python3 -O
    -> must still refuse (explicit AuditError, not a stripped assert).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

AUDIT = "scripts/audit_pp_descriptors.py"
PACKER = "protocol-processor/hdl/aecp/desc/gen_desc_image.py"
PATCHES = ('    with patch.object(descriptors, "d_control_identify", changed), \\\n'
           '            patch.object(assemble, "d_control_identify", changed):\n')
MUTANTS = {
    "K1_stale_config": (AUDIT, "        _, after = generate(builder.load_config(path))\n",
                        "        _, after = generate(cfg)\n", ["", "-O"]),
    "K2_control_ignores_field": (AUDIT,
                                 "        return dict(original(cfg), audit_identify=descriptors.d_control_identify().hex())\n",
                                 "        return dict(original(cfg))\n", [""]),
    "K3_assembler_patch_only": (AUDIT, PATCHES,
                                '    with patch.object(assemble, "d_control_identify", changed):\n', [""]),
    "K4_descriptor_patch_only": (AUDIT, PATCHES,
                                 '    with patch.object(descriptors, "d_control_identify", changed):\n', [""]),
    "K5_packer_normalizes_last_byte": (PACKER, "        img[off:off + len(body)] = body\n",
                                       "        img[off:off + len(body)] = body[:-1] + b'\\x00'\n", ["-O"]),
}


def main() -> None:
    clean, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    results = {}
    for name, (rel, old, new, modes) in MUTANTS.items():
        tree = scratch / name
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(clean, tree, symlinks=True)
        path = tree / rel
        text = path.read_text()
        assert text.count(old) == 1, (name, rel)
        path.write_text(text.replace(old, new))
        for mode in modes:
            out = scratch / f"{name}{mode}.json"
            cmd = [sys.executable, "-B"] + ([mode] if mode else []) + [AUDIT, "--output", str(out)]
            cp = subprocess.run(cmd, cwd=tree, capture_output=True, text=True, timeout=1800)
            res = dict(mode=mode or "normal", rc=cp.returncode,
                       tail=(cp.stdout + cp.stderr).strip().splitlines()[-1:])
            if cp.returncode == 0:
                ip = json.loads(out.read_text())["identity_probe"]
                res.update(changed_image_offsets=ip["changed_image_offsets"],
                           before_model_id=ip["before_entity"]["model_id"],
                           after_model_id=ip["after_entity"]["model_id"])
            results[f"{name}{mode}"] = res
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
