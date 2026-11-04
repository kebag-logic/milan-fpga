#!/usr/bin/env python3
"""Splice the reviewer probe rows into a copy of the parser harness.

usage: probe_splice.py SIM_MAIN_IN PROBES_CPP SIM_MAIN_OUT

The probe method is declared beside check_pdelay_resp, defined ahead of
RxParserHarness::run, and called last in run(), so every existing check
runs first and unchanged.
"""
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
probes = Path(sys.argv[2]).read_text(encoding="utf-8")
decl = ("  void check_pdelay_resp();\n"
        "  void check_r771_probes();\n"
        "  void r771_report(const char *tag, uint16_t d0);\n"
        "  void r771_accept(const char *tag, const Frame &f, uint64_t w11);\n"
        "  void r771_refuse(const char *tag, const Frame &f);\n"
        "  int r771_event_latency(const std::vector<uint8_t> &b, bool gaps);\n")
for marker in ("  void check_pdelay_resp();\n", "int RxParserHarness::run() {\n",
               "  return report();\n}\n\n}  // namespace\n"):
    if src.count(marker) != 1:
        sys.exit(f"marker not unique: {marker!r}")
src = src.replace("  void check_pdelay_resp();\n", decl)
src = src.replace("int RxParserHarness::run() {\n",
                  probes + "\nint RxParserHarness::run() {\n")
src = src.replace("  return report();\n}\n\n}  // namespace\n",
                  "  check_r771_probes();\n  return report();\n}\n\n}  // namespace\n")
Path(sys.argv[3]).write_text(src, encoding="utf-8")
