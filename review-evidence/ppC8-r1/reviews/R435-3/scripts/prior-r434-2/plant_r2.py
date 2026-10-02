#!/usr/bin/env python3
"""Round-2 reviewer plants: the four round-1 plants whose target text changed,
ported to the round-2 code with the same weakening, plus new plants on the
round-2 delta. Each plant replaces one exact string in one file of a disposable
copy of the head tree, then runs the desc_store gate.
Usage: plant_r2.py <head-tree> <work-dir> <plant-name>  (prints NAME KILLED|SURVIVED|BADPLANT)"""
import sys, shutil, subprocess, pathlib
D = "hdl/aecp/desc/"
R, L, G = D + "model_rules.py", D + "model_lint.py", D + "gen_desc_image.py"
PLANTS = {
 # --- round-1 plants, ported (same weakening on the round-2 code) ---
 "P-cli-writes-first":    (G, "    try:\n        model_ids = _model_ids_file(", "    open(args.output, 'wb').close()\n    try:\n        model_ids = _model_ids_file("),
 "P-covers-ut-current":   (R, "return ((entry ^ up_to) & ~channels == current & ~channels", "return ((entry ^ up_to) & ~channels == current & ~up_to & ~channels"),
 "P-iface-count-only":    (R, "            if seen[1] != index:", "            if False:"),
 "P-order-no-control-arm": (R, "if top and walked and max(top) > min(walked):", "if False:"),
 # --- new: L12 ---
 "N-max-refuses-507-508": (R, "if len(body) > DESCRIPTOR_MAX:", "if len(body) > DESCRIPTOR_MAX - 2:"),
 "N-max-accepts-516":     (R, "DESCRIPTOR_MAX = 508 ", "DESCRIPTOR_MAX = 516 "),
 "N-extent-no-count":     (R, "    if count is not None and len(body) != size + entry * count:", "    if False:"),
 "N-extent-no-offset":    (R, "    if offset is not None and offset != size:", "    if False:"),
 # --- new: L8 identify-format ---
 "N-identify-no-length":  (R, "wrong = [f\"is {len(body)} bytes, not 113\"] if len(body) != 113 else []", "wrong = []"),
 "N-identify-no-step":    (R, "(106, 1, 255, \"step\"), ", ""),
 "N-identify-no-unit":    (R, ", (109, 2, 0x0000, \"unit\"))", ")"),
 "N-identify-no-values-offset": (R, "(94, 2, 104, \"values_offset\"),", ""),
 "N-identify-no-count":   (R, "(96, 2, 1, \"number_of_values\"), ", ""),
 "N-identify-no-minimum": (R, "(104, 1, 0, \"minimum\"),", ""),
 "N-identify-no-type":    (R, "IDENTIFY_FORMAT = ((80, 2, 0x0001, \"control_value_type\"), ", "IDENTIFY_FORMAT = ("),
 "N-identify-no-mask":    (R, "                found &= 0x3FFF ", "                pass "),
 # --- new: waivers (overlap, strict types) ---
 "N-overlap-identical-only": (L, "and set(other.indices()) & set(waiver.indices()):", "and other.indices() == waiver.indices():"),
 "N-overlap-off":         (L, "        if other is None:\n", "        if True:\n"),
 "N-type-bool-accepted":  (L, "    if isinstance(item[\"type\"], bool) or not isinstance(", "    if not isinstance("),
 # --- new: digest exclusions (each over-inclusion would refuse an unchanged structure under a record) ---
 "N-digest-keeps-domain-current": (L, "    D.CLOCK_DOMAIN: ((70, 72),), ", "    "),
 "N-digest-keeps-rate-current":   (L, "    D.AUDIO_UNIT: ((136, 140),), ", "    "),
 "N-digest-keeps-current-format": (L, "D.STREAM_INPUT: ((74, 82),), D.STREAM_OUTPUT: ((74, 82),),", ""),
 "N-digest-keeps-current-config": (L, "(116, 308), (310, 312)),", "(116, 308)),"),
 "N-digest-keeps-entity-name":    (L, "D.ENTITY: ((4, 20), (36, 112),", "D.ENTITY: ((4, 20),"),
 "N-digest-keeps-source-flags":   (L, "D.CLOCK_SOURCE: ((70, 72), (74, 82)),", "D.CLOCK_SOURCE: ((74, 82),),"),
 "N-digest-keeps-gptp-dataset":   (L, "D.AVB_INTERFACE: ((70, 76), (78, 96)),", "D.AVB_INTERFACE: ((70, 76),),"),
 "N-digest-keeps-bode":           (L, "    return [(offset + 48, offset + 48 + 12 * count)]", "    return []"),
 "N-digest-mixer-no-linear":      (L, "D.MIXER: (80, 86, None, frozenset({\"linear\"})),", "D.MIXER: (80, 86, None, frozenset()),"),
 "N-digest-transcoder-off":       (L, "D.SIGNAL_TRANSCODER: (80, 82, 84, frozenset({\"linear\", \"selector\", \"array\"}))}", "D.SIGNAL_TRANSCODER: (80, 82, 84, frozenset())}"),
 # --- new: the round-2 ownership survey (conforming-model positives) ---
 "N-owners-no-jack":      (R, "CONTROL_OWNERS = ((D.JACK_INPUT, 74, 76), (D.JACK_OUTPUT, 74, 76), ", "CONTROL_OWNERS = ("),
 "N-owners-no-avb":       (R, "(D.AVB_INTERFACE, 98, 100),\n", "\n"),
 "N-owners-no-ptp":       (R, ", (D.PTP_INSTANCE, 82, 84))", ")"),
 "N-owners-no-control-block": (R, "                  (D.CONTROL_BLOCK, 70, 72), ", "                  "),
 "N-unit-no-ext-port-ranges": (R, "    (80, 82, D.EXTERNAL_PORT_INPUT), (84, 86, D.EXTERNAL_PORT_OUTPUT),\n", "    (80, 82, 0x7FF0), (84, 86, 0x7FF1),\n"),
 "N-port-controls-not-walked": (R, "                _claim_fields(ctx, (cfg, ptype, port), spans, walked=True)", "                _claim_fields(ctx, (cfg, ptype, port), spans, walked=False)"),
 # --- new: L5 / L4 / CRF arms of round 2 ---
 "N-l5-missing-port-finding": (R, "            seen = first.setdefault(port, (cfg, index))", "            seen = first.setdefault(port, (cfg, index))\n            if cfg and index not in ctx.of(0, D.AVB_INTERFACE):\n                ctx.bad(\"interface-index\", (cfg, D.AVB_INTERFACE, index), \"x\")"),
 "N-crf-only-current":    (R, "other = sorted({w for w in words if _family(w) == \"CRF\" and w != CRF_MILAN})", "other = sorted({w for w in words[:1] if _family(w) == \"CRF\" and w != CRF_MILAN})"),
}
if __name__ == "__main__":
    head, work, name = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
    path, old, new = PLANTS[name]
    tree = work / name
    if tree.exists(): shutil.rmtree(tree)
    shutil.copytree(head / "hdl/aecp/desc", tree / "hdl/aecp/desc"); shutil.copytree(head / "tb/desc_store", tree / "tb/desc_store", ignore=shutil.ignore_patterns("obj_dir"))
    f = tree / path; text = f.read_text(encoding="utf-8")
    if text.count(old) != 1:
        print(f"{name} BADPLANT (pattern count {text.count(old)})"); sys.exit(0)
    f.write_text(text.replace(old, new), encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"], cwd=tree / "tb/desc_store", capture_output=True, text=True, timeout=600)
    fails = [l for l in r.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    print(f"{name} {'KILLED' if r.returncode else 'SURVIVED'} rc={r.returncode} {fails[:3]}")
