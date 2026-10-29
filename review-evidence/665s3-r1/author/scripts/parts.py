#!/usr/bin/env python3
"""The platform image's rom and sram beside the size fixture's at one point, by part, from the two link maps.

usage: parts.py PLAT_OUT FIX_OUT
Each argument is a ctrl_plat_image.py / ctrl_srp_image.py --output directory holding ctrl_app.map and size.json.
Every linked input section is attributed to one part; rom is what loads (.text, .rodata, .data's initial bytes),
sram is what runs there (.data, .bss, .stack). A part's figure is the platform's bytes minus the fixture's.
"alignment" is the fill between input sections plus the gaps each plan's need holds beyond its sections, so the
parts sum exactly to the difference of the two plans' needs. Prints JSON, then a markdown table.
"""
import json
import re
import sys
from pathlib import Path

ROM_OUT = {".text", ".rodata", ".rela.dyn", ".data"}
RAM_OUT = {".data", ".bss", ".stack"}
OUT_SECTION = re.compile(r"^(\.\S+)(?:\s+0x[0-9a-f]+\s+0x[0-9a-f]+.*)?$")
FULL = re.compile(r"^ (\S+)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\S+)$")
NAME_ONLY = re.compile(r"^ (\S+)$")
CONT = re.compile(r"^\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\S+)$")
FILL = re.compile(r"^ \*fill\*\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)")

BOOT = {"ctrl_plat_boot", "ctrl_plat_step", "ctrl_plat_generated_image", "reach", "maap_owner", "compose",
        "configure_sources", "stream_id"}
PORTS = {"window_read": "maap", "window_write": "maap", "allocation": "maap", "source": "acmp", "locked": "acmp",
         "stream": "acmp", "notice": "acmp", "licence": "srp", "random_value": "aecp", "path": "aecp"}
#: the fixture's generated pools and tables, which the platform's ctrl_plat.c holds under other names
FIXTURE_POOLS = {"image_arena", "image_model", "image_descriptors", "image_values", "image_events", "image_latency",
                 "image_maps", "image_map_scratch", "image_map_pools", "image_names", "image_entity",
                 "aecp_entity_image", "aecp_map_defaults"}
LABELS = {
    "boot": "the boot: `ctrl_plat_boot` with its inlined composition, MAAP owner and SRP source set-up, "
            "`ctrl_plat_step`, the image hook",
    "csr": "the CSR window: identity, policy, status and time of day (`ctrl_plat_csr.c`)",
    "console": "the console (`ctrl_plat_console.c`, its digit table)",
    "strings": "the console's and the boot's strings, merged",
    "maap": "MAAP's port: the window's two accesses and the allocation report (`ctrl_plat.c`), and `maap_csr.c`",
    "acmp": "ACMP's talker sources: `source`, `locked`, `stream`, `notice`",
    "srp": "SRP's licence port",
    "aecp": "AECP's observations: `random_value`, `path`",
    "main": "`main`, the generated policy and stream table, `env` (`ctrl_plat_main.c`)",
    "mmio": "the bus port (`ctrl_plat_mmio.c`)",
    "state": "the state: `struct ctrl_plat` against the fixture's state objects",
    "pools": "the AEM image, its pools and lwSRP's pool, under the platform's names and the fixture's",
    "entry": "the size fixture's entry, removed (`ctrl_aecp_image.c`'s `main` and callbacks)",
    "shared": "every other object, the same sources (compiled with the platform's bus map)",
    "library": "library members",
    "alignment": "alignment",
}


def entries(path: Path) -> list[tuple[str, str, int, str]]:
    """(output section, input section, size, object) for every linked input section and fill."""
    lines = path.read_text().split("Linker script and memory map", 1)[1].splitlines()
    out, pending, found = "", None, []
    for line in lines:
        if line.startswith(".") and (m := OUT_SECTION.match(line)):
            out, pending = m.group(1), None
            continue
        if (m := FILL.match(line)):
            found.append((out, "*fill*", int(m.group(2), 16), "*fill*"))
            pending = None
        elif (m := FULL.match(line)):
            found.append((out, m.group(1), int(m.group(3), 16), m.group(4)))
            pending = None
        elif (m := NAME_ONLY.match(line)) and not line.startswith(" *("):
            pending = m.group(1)
        elif pending and (m := CONT.match(line)):
            found.append((out, pending, int(m.group(2), 16), m.group(3)))
            pending = None
        else:
            pending = None
    return found


def obj_name(obj: str) -> str:
    """An object's name without its directory or its compile index."""
    base = obj.rsplit("/", 1)[-1]
    return re.sub(r"^\d+-", "", base)


def part(obj: str, name: str) -> str:
    """The part an input section of an object belongs to."""
    o = obj_name(obj)
    symbol = name.split(".")[-1] if name.count(".") >= 2 else ""
    if o == "*fill*":
        return "alignment"
    if o.startswith(("libc.a", "libcompiler_rt.a")):
        return "library"
    if o == "ctrl_plat_csr.o":
        return "csr"
    if o == "ctrl_plat_console.o":
        return "strings" if ".str1." in name else "console"
    if o == "ctrl_plat_mmio.o":
        return "mmio"
    if o == "ctrl_plat_main.o":
        return "main"
    if o == "maap_csr.o":
        return "maap"
    if o == "ctrl_plat.o":
        if ".str1." in name:
            return "strings"
        if name == ".bss.ctrl_plat":
            return "state"
        if name.startswith(".text."):
            fn = name.removeprefix(".text.")
            return "boot" if fn in BOOT else PORTS.get(fn, "boot")
        return "pools"
    if o == "ctrl_aecp_image.o":
        if name.startswith(".text") or ".str1." in name:
            return "entry"
        return "pools" if symbol in FIXTURE_POOLS else "state"
    return "shared"


def measure(directory: Path) -> dict:
    """Per part, the rom and sram bytes of one image, the gaps put in alignment so they sum to the needs."""
    report = json.loads((directory / "size.json").read_text())
    split = report["split"]
    sums: dict[str, list[int]] = {}
    rom = ram = 0
    detail = {}
    for out, name, size, obj in entries(directory / "ctrl_app.map"):
        key = part(obj, name)
        cell = sums.setdefault(key, [0, 0])
        if out in ROM_OUT:
            cell[0] += size
            rom += size
        if out in RAM_OUT:
            cell[1] += size
            ram += size
        if key in ("state", "pools") and size and out in RAM_OUT:
            detail[f"{obj_name(obj)}:{name}"] = size
    align = sums.setdefault("alignment", [0, 0])
    align[0] += split["rom"]["bytes"] - rom
    align[1] += split["sram"]["bytes"] - ram
    return {"needs": (split["rom"]["bytes"], split["sram"]["bytes"]), "tiles": split["tiles"], "parts": sums,
            "ram_detail": detail, "members": report.get("ctrl_plat_members", {})}


def main() -> int:
    """Both images' parts and their difference, checked to sum to the difference of the needs."""
    plat, fix = measure(Path(sys.argv[1])), measure(Path(sys.argv[2]))
    keys = [k for k in LABELS if k in plat["parts"] or k in fix["parts"]]
    keys += sorted((set(plat["parts"]) | set(fix["parts"])) - set(keys))
    delta = {k: [plat["parts"].get(k, [0, 0])[i] - fix["parts"].get(k, [0, 0])[i] for i in (0, 1)] for k in keys}
    need = [plat["needs"][i] - fix["needs"][i] for i in (0, 1)]
    total = [sum(v[i] for v in delta.values()) for i in (0, 1)]
    state = state_split(plat, fix)
    report = {"platform": plat, "fixture": fix, "delta": delta, "need_delta": need, "sum": total,
              "state_sram": state, "state_sums_match": sum(state.values()) == delta.get("state", [0, 0])[1]}
    print(json.dumps(report, indent=1))
    print()
    print("| Part | `rom`, B | `sram`, B |")
    print("|---|---:|---:|")
    for k in keys:
        if delta[k] != [0, 0]:
            print(f"| {LABELS.get(k, k)} | {delta[k][0]:+,} | {delta[k][1]:+,} |")
    print(f"| **The platform minus the fixture** | **{need[0]:+,}** | **{need[1]:+,}** |")
    print()
    print("| The state's `sram`, by member | B |")
    print("|---|---:|")
    for k, v in state.items():
        print(f"| {k} | {v:+,} |")
    return 0 if total == need and report["state_sums_match"] else 1


#: struct ctrl_plat's members with an object of the same type in the fixture
PAIRED = {"app": "image_app", "srp": "image_srp", "aecp": "image_aecp", "sources": "image_sources",
          "bridge": "image_aecp_bridge", "acmp": "image_acmp", "face": "image_face", "state": "image_state",
          "binding": "image_binding"}


def state_split(plat: dict, fix: dict) -> dict[str, int]:
    """The state's sram difference by member: the paired members against the fixture's objects, the members the
    fixture has no object for, and the other fields and padding against the fixture's unpaired objects."""
    members = plat["members"]
    whole = plat["ram_detail"].get("ctrl_plat.o:.bss.ctrl_plat", 0)
    fixture = {k.split(":", 1)[1].split(".")[-1]: v for k, v in fix["ram_detail"].items()
               if k.startswith("ctrl_aecp_image.o:") and k.split(".")[-1] not in FIXTURE_POOLS}
    paired = sum(members[m] for m in PAIRED) - sum(fixture.get(f, 0) for f in PAIRED.values())
    unpaired = {k: v for k, v in fixture.items() if k not in PAIRED.values()}
    return {"the paired members (app, srp, aecp, sources, bridge, acmp, face, state, binding) against the "
            "fixture's objects": paired,
            "`console`": members["console"],
            "`maap_csr`": members["maap_csr"],
            "`config`, `aecp_config` and `srp_config`, held statically": members["config"] + members["aecp_config"]
            + members["srp_config"],
            "the other fields and padding, against the fixture's " + ", ".join(f"`{k}`" for k in sorted(unpaired)):
            whole - sum(members.values()) - sum(unpaired.values())}


if __name__ == "__main__":
    sys.exit(main())
