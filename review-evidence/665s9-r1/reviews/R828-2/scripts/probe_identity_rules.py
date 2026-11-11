"""probe_identity_rules.py <repo> <scratch dir>: drive check_image_identity's manifest and bitstream rules
directly on fabricated facts shaped like gate 23p's new control and new plant, at the tree as checked out and
under three planted copies of the module (if True, have == bound, lines comparing the manifest's ident removed)."""
import json, sys, types
from pathlib import Path

repo, tmp = Path(sys.argv[1]), Path(sys.argv[2])
tmp.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(repo / "sw/litex"))
import qspi_owner_transition as q  # noqa: E402

src = (repo / "sw/litex/check_image_identity.py").read_text()
IDENT_RULE = ("    if claimed[\"ident\"] != got[\"ident\"]:\n        found.append((\"manifest\", f\"the manifest's ident "
              "{claimed['ident']!r} is not the image's {got['ident']!r}\"))\n")
ARMS = {"head": (None, None), "if-true": ("    if have != bound:\n", "    if True:\n"),
        "have-eq-bound": ("    if have != bound:\n", "    if have == bound:\n"), "no-manifest-ident": (IDENT_RULE, "")}

def load(arm):
    old, new = ARMS[arm]
    text = src
    if old is not None:
        assert text.count(old) == 1, arm
        text = text.replace(old, new)
    mod = types.ModuleType(f"cii_{arm.replace('-', '_')}")
    mod.__file__ = str(repo / "sw/litex/check_image_identity.py")
    exec(compile(text, mod.__file__, "exec"), mod.__dict__)
    return mod

bit = tmp / "built.bit"
q._fake_bit(bit, b"\xff" * 16 + b"\xaa\x99\x55\x66built")
binding = json.loads(json.dumps(q.bitstream_binding(bit)))   # the manifest's JSON round trip
for arm in ARMS:
    m = load(arm)
    ident = "Milan TSN SoC - VexiiRiscv RV32 1-core baremetal " + m.SPLIT_WORD
    rtlv = m.rtl_version()
    base = {"schema": m.SCHEMA, "placement": m.SPLIT_WORD, "ident": ident,
            "version": f"0x{(rtlv[0] << 16) | rtlv[1]:08x}", "mailbox": {"major": 2, "minor": 4},
            "ctrl_firmware": {"path": "x", "sha256": "0"}, "bitstream": binding}
    got = {"ident": ident, "version": (rtlv[0] << 16) | rtlv[1], "mailbox_version": (2, 4), "bitstreams": [bit]}
    # control: a manifest binding the bitstream the image holds
    found = []; m._manifest_rules(dict(got, manifest=base), found); m._bitstream_rules(dict(got, manifest=base), None, found)
    print(f"{arm:18s} control (bound bitstream held): {'PASS' if not found else 'REFUSED ' + str([k for k, _ in found])}")
    # plant: the manifest's ident set to the all-fabric ident, the image's stays split
    planted = dict(base, ident=ident.rsplit(' ', 1)[0])
    found = []; m._manifest_rules(dict(got, manifest=planted), found)
    print(f"{arm:18s} plant (manifest ident changed): {'FINDING ' + ','.join(k for k, _ in found) if found else 'NOT FOUND'}")
