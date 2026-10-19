#!/usr/bin/env python3
"""Reviewer probes on a disposable copy of the processor tree (never the clone).

usage: probe_rdc.py TREE VARIANT
  tail   : tb/pp_top AX CONTROL fixture grown to 113 bytes (stride 120) with a
           distinct byte @112, so RDC0..RDC5 grade E_RDESCCT's non-empty TAIL
           through the real store and response buffer; plus PROBE-NSD, a
           READ_DESCRIPTOR of CONTROL 1 (absent) graded as the 4-byte
           NO_SUCH_DESCRIPTOR stub.
  missnop: 'tail' plus E_RDESCCT's locate-miss branch replaced with NOP.
  vendor : 'tail' plus PROBE-VENDOR, CONTROL 0 given a non-IDENTIFY control_type.
Each edit must match exactly once, or the probe refuses.
"""
import sys
from pathlib import Path


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    n = text.count(old)
    if n != 1:
        sys.exit(f"REFUSED {path}: anchor occurs {n} times: {old[:60]!r}")
    path.write_text(text.replace(old, new, 1))


def tail(tree: Path) -> None:
    sim = tree / "tb/pp_top/sim_main.cpp"
    edit(sim, "{CFGIX, 0x001A, 1, 112, 9, 112, 0},",
         "{CFGIX, 0x001A, 1, 113, 9, 120, 0},")
    edit(sim, "        io.dram[e.off + CT_CUR] = CT_IMAGE_CUR;\n",
         "        io.dram[e.off + CT_CUR] = CT_IMAGE_CUR;\n"
         "        io.dram[e.off + 112] = 0xB8;   // PROBE: string[0]'s second byte\n")
    edit(sim, "    rd_control_after_set();\n  }\n",
         "    rd_control_after_set();\n"
         "    {\n"
         "      ++seq;\n"
         "      const auto r = ask(AEM_READ_DESCRIPTOR, rdesc(CFGIX, 0x001A, 1));\n"
         "      std::vector<uint8_t> pl(8, 0);\n"
         "      putbe(&pl[0], CFGIX, 2);\n"
         "      putbe(&pl[4], 0x001A, 2);\n"
         "      putbe(&pl[6], 1, 2);\n"
         "      const auto w = want(CTLR_MAC, CTLR_EID, AECP_NO_SUCH_DESCRIPTOR,\n"
         "                          AEM_READ_DESCRIPTOR, pl);\n"
         "      CHECK(r == w, \"PROBE-NSD READ_DESCRIPTOR CONTROL 1 (absent): \"\n"
         "            \"NO_SUCH_DESCRIPTOR stub byte-exact (status %d)\", st(r));\n"
         "      if (!r.empty() && r != w) { dump(\"got\", r); dump(\"exp\", w); }\n"
         "    }\n"
         "  }\n")
    # RDC6 shrinks CONTROL to 111 bytes inside the same slot; keep it.


def missnop(tree: Path) -> None:
    gen = tree / "hdl/aecp/ucode/gen_ucode.py"
    edit(gen, "    u('DESC_ADDR', ra=14, imm=RGN_LOCATE),       # requested CONTROL[index]\n"
              "    u('BR_STATUS', cnd=0, imm=E_RDSTUB),\n",
         "    u('DESC_ADDR', ra=14, imm=RGN_LOCATE),       # requested CONTROL[index]\n"
         "    u('NOP'),                                    # PROBE\n")


def vendor(tree: Path) -> None:
    """PROBE-VENDOR: CONTROL 0 with a non-IDENTIFY control_type (a vendor
    CONTROL_LINEAR_UINT8, which the model lint admits beside the IDENTIFY);
    IEEE 7.2.22 / 7.3.6.2 want its own current value, the image's 0x5A."""
    sim = tree / "tb/pp_top/sim_main.cpp"
    edit(sim, "    rd_ctrl(\"RDC3 ...and restored, CONTROL 0 carries 255 again\");\n",
         "    rd_ctrl(\"RDC3 ...and restored, CONTROL 0 carries 255 again\");\n"
         "    {\n"
         "      uint8_t ct[8];\n"
         "      for (int k = 0; k < 8; ++k) ct[k] = io.dram[at + 82 + k];\n"
         "      putbe(&io.dram[at + 82], 0x0011223344556677ull, 8);\n"
         "      rd_ctrl_image(\"PROBE-VENDOR CONTROL 0 with a vendor control_type, \"\n"
         "                    \"IDENTIFY 255: its own current value, the image's\");\n"
         "      for (int k = 0; k < 8; ++k) io.dram[at + 82 + k] = ct[k];\n"
         "    }\n")


def main() -> None:
    tree, variant = Path(sys.argv[1]), sys.argv[2]
    tail(tree)
    if variant == "missnop":
        missnop(tree)
    elif variant == "vendor":
        vendor(tree)
    elif variant != "tail":
        sys.exit(f"unknown variant {variant}")
    print(f"probe {variant} planted in {tree}")


if __name__ == "__main__":
    main()
