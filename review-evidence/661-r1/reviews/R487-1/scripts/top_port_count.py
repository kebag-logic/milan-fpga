#!/usr/bin/env python3
"""Count protocol_processor_top's declared ports and parameters with the repository's own parser
(scripts/sv_ports.py) at each given processor revision.
Usage: top_port_count.py <parent-checkout> <processor-rev>..."""
import collections, subprocess, sys
root, revs = sys.argv[1], sys.argv[2:]
sys.path.insert(0, f"{root}/scripts")
import sv_ports  # noqa: E402
for rev in revs:
    text = subprocess.check_output(["git", "-C", f"{root}/protocol-processor", "show",
                                    f"{rev}:hdl/top/protocol_processor_top.sv"], text=True)
    decls = sv_ports.declarations(text)
    kinds = collections.Counter(d[4] for d in decls if d[0] == "protocol_processor_top")
    print(rev[:8], dict(kinds))
