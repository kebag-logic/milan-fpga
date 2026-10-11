#!/usr/bin/env python3
"""Export one AX7101 SoC (no Vivado, no software) from a given source tree.

    python export_soc.py <tree> <config-stem> <output-dir> [extra milan_soc args...]

Run with the LiteX interpreter. The design argv is the tree's own
end-station builder's (emit_soc_argv), with --entity-gen-dir from that tree's
configs/generated, then --no-compile-software --no-compile-gateware and the
output directory. Extra arguments (e.g. --ctrl-mailbox --ctrl-firmware ELF)
are appended. Writes <output-dir>.argv.json and exits with milan_soc's code.
"""
import contextlib
import json
import os
import sys
from pathlib import Path


def main() -> int:
    tree, stem, out, extra = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve(), sys.argv[4:]
    sys.path.insert(0, str(tree / "sw/builder"))
    sys.path.insert(0, str(tree / "sw/litex"))
    os.chdir(tree / "sw/litex")
    import endstation_builder as eb
    cfg_path = tree / "configs" / f"{stem}.yaml"
    cfg = eb.load_config(str(cfg_path))
    with contextlib.redirect_stdout(None):
        eb.build(str(cfg_path))
    argv = eb.emit_soc_argv(cfg) + ["--entity-gen-dir", str(tree / "configs/generated" / cfg["name"]),
                                     "--no-compile-software", "--no-compile-gateware",
                                     "--output-dir", str(out), *extra]
    Path(str(out) + ".argv.json").write_text(json.dumps(argv, indent=1) + "\n")
    import milan_soc
    sys.argv = ["milan_soc.py", *argv]
    try:
        milan_soc.main()
    except SystemExit as exc:
        return 0 if exc.code is None else (exc.code if isinstance(exc.code, int) else 1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
