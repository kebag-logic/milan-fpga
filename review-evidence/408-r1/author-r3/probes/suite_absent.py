"""Run the WHOLE test_builder suite with cross compilers hidden, using the
same CompilerAudit test_firmware_compiler.py uses for its absent control."""
import re, sys, tempfile, subprocess
from pathlib import Path
from unittest.mock import patch
LANE = "$LANES/408-409-boot-gate-retire"
sys.path.insert(0, LANE + "/scripts")
sys.path.insert(0, LANE + "/sw/builder")
import test_builder as builder
import test_firmware_compiler as tfc
# extract the __main__ function-call list from the source
src = Path(LANE + "/sw/builder/test_builder.py").read_text()
block = src.split("for fn in (test_all_configs_build,", 1)[1].split("):", 1)[0]
names = [n.strip() for n in ("test_all_configs_build," + block).split(",") if n.strip()]
fns = [getattr(builder, n) for n in names]
with tempfile.TemporaryDirectory(prefix="milan-suite-absent-") as tmp:
    with open(Path(tmp) / "audit.jsonl", "w") as stream:
        audit = tfc.CompilerAudit(stream, None)  # None -> absent cross tools
        with patch.object(subprocess, "run", side_effect=audit.invoke), \
                patch.object(sys, "argv", [__file__]), \
                patch.object(builder, "SKIPPED", []):
            for fn in fns:
                print(f"{fn.__name__}:")
                fn()
            assert audit.hidden == audit.cross, audit.hidden
            assert audit.compiles == 0, "absent mode compiled firmware"
            sk = builder.SKIPPED
    if sk:
        print(f"\n{len(sk)} GATE ARM(S) DID NOT RUN:")
        for gate, why, _k in sk:
            print(f"  - [{gate}] {why[:120]}")
        print(f"ALL GATES PASS EXCEPT {len(sk)} NOT RUN")
    else:
        print("ALL GATES PASS")
print(f"suite-absent compiles={audit.compiles} hidden={audit.hidden}")
