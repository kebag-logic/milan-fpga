#!/usr/bin/env python3
"""Compare the reference page's measurement tables with an audit receipt.

Expectations below are transcribed by hand from
docs/reference/PP_DESCRIPTOR_OWNERSHIP.md at the reviewed head; they are not
derived from the receipt. Usage: check_page_vs_receipt.py <receipt.json>
Exit 0 only when every expectation matches.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

PAGE = {  # name: descriptors, image bytes, SI/SO, SPI/SPO, clusters/maps, ADP src/sink
    "arty_current": (32, 5792, (2, 1), (1, 1), (16, 1), (1, 2)),
    "arty_4x4": (64, 10112, (5, 5), (4, 4), (32, 4), (5, 5)),
    "arty_8ch": (96, 15360, (5, 5), (4, 4), (64, 4), (5, 5)),
    "ax7101_1x1_tdm8": (41, 7352, (2, 2), (1, 1), (25, 0), (2, 2)),
    "ax7101_8x8": (116, 18288, (9, 9), (8, 8), (72, 0), (9, 9)),
}
AU = {  # AUDIO_UNIT offset, (rate offset, count, length), rates, CLOCK_DOMAIN offset
    "arty_current": (712, (144, 3, 156), [48000, 96000, 192000], 3920),
    "arty_4x4": (712, (144, 1, 148), [48000], 6768),
    "arty_8ch": (712, (144, 1, 148), [48000], 9968),
    "ax7101_1x1_tdm8": (696, (144, 1, 148), [48000], 4840),
    "ax7101_8x8": (696, (144, 1, 148), [48000], 11872),
}
CRF_INPUT_INDEX = {"arty_current": 1, "arty_4x4": 4, "arty_8ch": 4,
                   "ax7101_1x1_tdm8": 1, "ax7101_8x8": 8}
MODEL_ID = {"arty_current": ("0x001BC50AC1000005", "pin"),
            "arty_4x4": ("0x001BC557FC6ABBC8", "hash"),
            "arty_8ch": ("0x001BC507C86F4172", "hash"),
            "ax7101_1x1_tdm8": ("0x001BC5C40236BA0E", "hash"),
            "ax7101_8x8": ("0x001BC572F79BC5D1", "hash")}
PACKER_REFUSED = {"metadata index gap", "duplicate row", "ENTITY name differs from name table",
                  "opaque 577-byte row"}
YAML_REFUSED = {"empty listener list", "static input map", "nine distinct rates", "duplicate rates"}
YAML_IMAGE_REFUSED = {"eight distinct rates"}


def main() -> int:
    """Check every transcribed expectation and print one line per failure."""
    report = json.loads(Path(sys.argv[1]).read_text())
    bad: list[str] = []

    def want(cond: bool, what: str) -> None:
        """Record one failed expectation."""
        if not cond:
            bad.append(what)

    for c in report["configurations"]:
        name = Path(c["config"]).stem.removeprefix("endstation_")
        rows = c["rows"]
        n = Counter(r["type"] for r in rows)
        f = {(r["type"], r["index"]): r for r in rows}
        d, size, s, sp, cm, adp = PAGE[name]
        ent = f[(0, 0)]["fields"]
        want((len(rows), c["image_bytes"]) == (d, size), f"{name} descriptors/bytes")
        want((n[5], n[6]) == s and (n[14], n[15]) == sp, f"{name} stream/port counts")
        want((n[20], n[23]) == cm, f"{name} clusters/maps")
        want((ent["talker_sources"], ent["listener_sinks"]) == adp, f"{name} ENTITY ADP counts")
        want((c["adp"]["talker_stream_sources"], c["adp"]["listener_stream_sinks"]) == adp,
             f"{name} builder ADP counts")
        want((ent["configurations"], ent["current_config"]) == (1, 0), f"{name} config count")
        want(f[(0, 0)]["length"] == 312, f"{name} ENTITY length")
        want((ent["model_id"], c["model_id"]["source"]) == MODEL_ID[name], f"{name} model id")
        want(ent["capabilities"] == "0x0000C588", f"{name} entity capabilities")
        au_off, (ro, rc, rl), rates, cd_off = AU[name]
        au = f[(2, 0)]
        want(au["image_offset"] == au_off and au["length"] == rl, f"{name} AU offset/length")
        want((au["fields"]["rates_offset"], au["fields"]["rates_count"]) == (ro, rc), f"{name} AU list")
        want(au["fields"]["rates"] == rates and au["fields"]["current_rate"] == 48000, f"{name} AU rates")
        cd = f[(36, 0)]
        want(cd["image_offset"] == cd_off and cd["length"] == 80, f"{name} CD offset/length")
        want((cd["fields"]["sources_offset"], cd["fields"]["sources"]) == (76, [0, 1]), f"{name} CD list")
        cs0, cs1 = f[(10, 0)], f[(10, 1)]
        want(cs0["fields"] == dict(source_type=0, location_type=10, location_index=0), f"{name} CS0")
        want(cs1["fields"] == dict(source_type=2, location_type=5,
                                   location_index=CRF_INPUT_INDEX[name]), f"{name} CS1")
        want(cs0["length"] == cs1["length"] == 86, f"{name} CS length")
        cfg = f[(1, 0)]
        want((cfg["length"], cfg["fields"]["counts_offset"], cfg["fields"]["counts_count"]) == (106, 74, 8),
             f"{name} CONFIGURATION")
        want([t for t, _ in cfg["fields"]["counts"]] == [2, 5, 6, 9, 36, 10, 26, 12], f"{name} CFG order")
        avb, ctl = f[(9, 0)], f[(26, 0)]
        want((avb["length"], avb["fields"]["port_number"], avb["fields"]["controls"]) == (102, 1, 0),
             f"{name} AVB_INTERFACE")
        want((ctl["length"], ctl["fields"]) == (113, dict(control_type="0x90E0F00000000001",
                                                          reset_time=0, values_offset=104)),
             f"{name} CONTROL")
        want(all(r["length"] == 90 and r["fields"]["channel_count"] == 1
                 for r in rows if r["type"] == 20), f"{name} clusters mono")
        want(all(r["length"] == 20 for r in rows if r["type"] in (14, 15)), f"{name} port length")
        want(all(r["fields"]["maps"] == 0 for r in rows if r["type"] == 14), f"{name} input maps")
        for r in rows:
            if r["type"] not in (5, 6):
                continue
            x = r["fields"]
            crf = x["formats"] == ["0x041060010000BB80"]
            want(x["current_format"] == x["formats"][0], f"{name} {r['type']}/{r['index']} current")
            want(x["formats_offset"] == 138 and x["redundant_count"] == 0 and x["timing"] == 0,
                 f"{name} {r['type']}/{r['index']} offsets")
            want(x["redundant_offset"] == r["length"] == 138 + 8 * x["formats_count"],
                 f"{name} {r['type']}/{r['index']} length")
            if r["type"] == 5:
                want(x["buffer_ns"] == 2126000 and x["flags"] == 3, f"{name} SI{r['index']} buffer/flags")
                want(crf or x["formats_count"] == 2, f"{name} SI{r['index']} AAF formats")
            else:
                want(x["flags"] == (3 if crf else 2), f"{name} SO{r['index']} flags")
        want(any(r["type"] == 6 and r["fields"]["formats"] == ["0x041060010000BB80"] for r in rows)
             == (name != "arty_current"), f"{name} CRF output presence")

    for p in report["packer_probes"]:
        exp = "refused" if p["probe"] in PACKER_REFUSED else "accepted"
        want(p["result"] == exp, f"packer {p['rule']} {p['probe']}: {p['result']}")
    want(len(report["packer_probes"]) == 30, "packer probe count")
    for p in report["config_probes"]:
        exp_l = "refused" if p["probe"] in YAML_REFUSED else "accepted"
        want(p["loader"] == exp_l, f"yaml {p['probe']} loader {p['loader']}")
        if exp_l == "accepted":
            exp_i = "refused" if p["probe"] in YAML_IMAGE_REFUSED else "accepted"
            want(p.get("image") == exp_i, f"yaml {p['probe']} image {p.get('image')}")
    want(len(report["config_probes"]) == 13, "yaml probe count")
    want([m["result"] for m in report["map_probes"]] == ["accepted", "refused"], "map probes")
    ident = report["identity_probe"]
    want(ident["model_id"] == "0x001BC557FC6ABBC8" and ident["changed_image_offsets"] == [6741],
         "identity offset")
    want(ident["before_sha256"].startswith("1b288e13ccbf") and ident["after_sha256"].startswith("bb036e26ddb7"),
         "identity hashes")
    want(ident["before_entity"] == ident["after_entity"], "identity ENTITY unchanged")

    for line in bad:
        print("MISMATCH", line)
    print(f"page-vs-receipt: {len(bad)} mismatch(es)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
