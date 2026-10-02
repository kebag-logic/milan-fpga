#!/usr/bin/env python3
"""Round-3 reviewer plants on the round-3 delta (L4 Annex C arms, the
identify-format mask, the digest's field-by-field claim, the one guarded
loader, partial waiver overlap, the 508-octet boundary). Same harness as
../r2/plant_r2.py: one exact-string replacement per disposable copy of
hdl/aecp/desc and tb/desc_store, then the whole desc_store gate.
Usage: plant_r3.py <head-tree> <work-dir> <plant-name>  (prints NAME KILLED|SURVIVED|BADPLANT)
       plant_r3.py --list"""
import importlib.util
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("plant_r2", here.parent / "r2" / "plant_r2.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
R, L, G = base.R, base.L, base.G
base.PLANTS.clear()
base.PLANTS.update({
 # --- F1: L4 stream-layout, both layouts ---
 "F1-annexc-refused":     (R, "    annex_c = offset == ANNEX_C_OFFSET\n", "    annex_c = False\n"),
 "F1-tail-anywhere":      (R, "    if tail and not annex_c:\n", "    if False:\n"),
 "F1-tail78-r1-allowed":  (R, "    if tail and not annex_c:\n", "    if tail > 1 and not annex_c:\n"),
 "F1-rmax-9":             (R, "REDUNDANT_MAX = 8 ", "REDUNDANT_MAX = 9 "),
 "F1-rmax-7":             (R, "REDUNDANT_MAX = 8 ", "REDUNDANT_MAX = 7 "),
 "F1-rmax-only-78":       (R, "    if tail > REDUNDANT_MAX:\n", "    if tail > REDUNDANT_MAX and not annex_c:\n"),
 "F1-tail-8R":            (R, "    end = formats_end + 2 * tail\n", "    end = formats_end + 8 * tail\n"),
 "F1-tail-no-length":     (R, "    end = formats_end + 2 * tail\n", "    end = formats_end\n"),
 "F1-redundant-at-138":   (R, "    formats_end = (ANNEX_C_OFFSET if annex_c else FORMATS_OFFSET) + 8 * count\n",
                              "    formats_end = FORMATS_OFFSET + 8 * count\n"),
 "F1-offset-any":         (R, "    if offset is not None and offset not in (FORMATS_OFFSET, ANNEX_C_OFFSET):\n",
                              "    if False:\n"),
 "F1-redundant-off":      (R, "    if redundant is not None and redundant != formats_end:\n", "    if False:\n"),
 "F1-length-off":         (R, "    if len(body) != end:\n        ctx.bad(\"stream-layout\", where, f\"is {len(body)} bytes; {made} make {end}\")",
                              "    if False:\n        ctx.bad(\"stream-layout\", where, f\"is {len(body)} bytes; {made} make {end}\")"),
 # --- F2: identify-format mask, one flag at a time ---
 "F2-mask-keeps-u":       (R, "                found &= 0x3FFF ", "                found &= 0xBFFF "),
 "F2-mask-keeps-r":       (R, "                found &= 0x3FFF ", "                found &= 0x7FFF "),
 # --- F2: L12 508-octet boundary and partial overlap ---
 "F2-max-refuses-508":    (R, "if len(body) > DESCRIPTOR_MAX:", "if len(body) >= DESCRIPTOR_MAX:"),
 "F2-overlap-nested-only": (L, "and set(other.indices()) & set(waiver.indices()):",
                               "and (set(other.indices()) <= set(waiver.indices()) or set(waiver.indices()) <= set(other.indices())):"),
 # --- F2: the digest, field by field against IEEE 1722.1-2021 6.2.2.8 ---
 "D-video-off":           (L, "    D.VIDEO_CLUSTER: ((85, 89), (93, 97), (101, 103), (107, 111), (115, 117)),\n", ""),
 "D-video-color-narrow":  (L, "(107, 111), (115, 117)),", "(107, 111), (115, 116)),"),
 "D-sensor-rate-off":     (L, "    D.SENSOR_CLUSTER: ((84, 92), (96, 100)),", "    D.SENSOR_CLUSTER: ((84, 92),),"),
 "D-memobj-narrow":       (L, "    D.MEMORY_OBJECT: ((92, 100),),", "    D.MEMORY_OBJECT: ((92, 99),),"),
 "D-selector-widen":      (L, "    D.SIGNAL_SELECTOR: ((84, 90),),", "    D.SIGNAL_SELECTOR: ((84, 92),),"),
 "D-domain-widen":        (L, "    D.CLOCK_DOMAIN: ((70, 72),),", "    D.CLOCK_DOMAIN: ((70, 74),),"),
 "D-avb-flags-excluded":  (L, "D.AVB_INTERFACE: ((70, 76), (78, 96)),", "D.AVB_INTERFACE: ((70, 96),),"),
 "D-avb-port-excluded":   (L, "D.AVB_INTERFACE: ((70, 76), (78, 96)),", "D.AVB_INTERFACE: ((70, 76), (78, 98)),"),
 "D-entity-strings-excluded": (L, "(36, 112), (116, 308),", "(36, 308),"),
 "D-entity-counts-excluded": (L, "(116, 308), (310, 312)),", "(116, 312)),"),
 "D-source-type-excluded": (L, "D.CLOCK_SOURCE: ((70, 72), (74, 82)),", "D.CLOCK_SOURCE: ((70, 82),),"),
 "D-named-no-ptp-port":   (L, "    | frozenset(range(0x1F, 0x29))", "    | frozenset(range(0x1F, 0x28))"),
 "D-named-plus-locale":   (L, "NAMED = frozenset(range(0x01, 0x0C))", "NAMED = frozenset(range(0x01, 0x0D))"),
 "D-whole-no-vendor":     (L, "WHOLE = frozenset({0x001F, 0x0021, 0x0022, 0x0023, 0x3FFE})",
                              "WHOLE = frozenset({0x001F, 0x0021, 0x0022, 0x0023})"),
 "D-whole-no-smpte":      (L, "WHOLE = frozenset({0x001F, 0x0021, 0x0022, 0x0023, 0x3FFE})",
                              "WHOLE = frozenset({0x001F, 0x0022, 0x0023, 0x3FFE})"),
 "D-family-from-int8":    (L, "        if base + 1 <= value_type <= base + 9:", "        if base <= value_type <= base + 9:"),
 "D-selector-string-off": (L, "    if value_type == 0x0014:\n        return \"selector\", 2\n", ""),
 "D-mixer-selector":      (L, "D.MIXER: (80, 86, None, frozenset({\"linear\"})),",
                              "D.MIXER: (80, 86, None, frozenset({\"linear\", \"selector\", \"array\"})),"),
 "D-matrix-whole":        (L, "D.MATRIX: (80, 94, 96, frozenset({\"linear\", \"selector\", \"array\"})),",
                              "D.MATRIX: (80, 94, 96, frozenset({\"linear\", \"selector\", \"array\", \"whole\"})),"),
 "D-array-current-shift": (L, "        return [(offset + 4 + 4 * width, offset + 4 + (4 + count) * width)]",
                              "        return [(offset + 4 * width, offset + (4 + count) * width)]"),
 "D-linear-current-default": (L, "        return [(offset + k * step + 4 * width, offset + k * step + 5 * width) for k in range(count)]",
                                 "        return [(offset + k * step + 3 * width, offset + k * step + 4 * width) for k in range(count)]"),
 "D-bode-first-only":     (L, "    return [(offset + 48, offset + 48 + 12 * count)]", "    return [(offset + 48, offset + 60)]"),
 # --- R435-2 S1: the one guarded loader ---
 "S1-no-guard":           (G, "    if spec is None or spec.loader is None:\n        raise ImportError(f\"no {name}.py beside {__file__}\")\n", ""),
 "S1-own-loader":         (L, "beside: Callable[[str], ModuleType]\n",
                              "def beside(name: str) -> ModuleType:\n"
                              "    import importlib.util as _u, pathlib as _p\n"
                              "    _s = _u.spec_from_file_location(name, _p.Path(__file__).resolve().with_name(f\"{name}.py\"))\n"
                              "    _m = _u.module_from_spec(_s); _s.loader.exec_module(_m); return _m\n"),
})
if __name__ == "__main__":
    if sys.argv[1:] == ["--list"]:
        print("\n".join(base.PLANTS)); sys.exit(0)
    exec(compile(open(here.parent / "r2" / "plant_r2.py").read().split("if __name__")[1].split(":", 1)[1]
                 .replace("\n    ", "\n"), "main", "exec"), {**base.__dict__, "PLANTS": base.PLANTS})
