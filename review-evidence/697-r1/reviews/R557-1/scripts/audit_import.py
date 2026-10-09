#!/usr/bin/env python3
"""Compare pinned source blobs with the reviewed import, without modifying either."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repository", type=Path)
p.add_argument("source", type=Path)
p.add_argument("details", type=Path)
a = p.parse_args()
mapping = {f"sw/firmware/ctrl/{m}/{m}.{ext}": f"{directory}/{m}.{ext}" for m in ("adp", "acmp", "maap") for ext, directory in (("c", "src"), ("h", "include"))}
mapping["sw/firmware/ctrl/wire/wire.h"] = "include/wire.h"
records = []
for old, new in mapping.items():
    source = (a.source / old).read_bytes()
    expected = source.replace(b"SPDX-License-Identifier: CERN-OHL-W-2.0", b"SPDX-License-Identifier: MIT")
    actual = (a.repository / new).read_bytes()
    records.append({"source": old, "destination": new, "equal_after_spdx": expected == actual, "sha256": hashlib.sha256(actual).hexdigest()})
details = []
for name in ("test_adp.cpp", "test_adp_reentry.cpp", "test_acmp.cpp", "acmp_fake.hpp", "test_maap.cpp", "test_maap_debug.cpp"):
    text = (a.source / "sw/firmware/ctrl/test" / name).read_text()
    if name == "test_adp.cpp":
        text = text[:text.index("// ---- the adapter")] + text[text.index("TEST(AdpCore,"):text.index("TEST(AdpAdapter,")] + "\n} // namespace\n"
        text = re.sub(r"// test_adp.cpp.*?(?=#include)", "// ADP core cases over fake ports.\n\n", text, flags=re.S)
    if name == "test_maap.cpp" and "struct CsrRig" in text:
        text = text[:text.index("struct CsrRig")] + "\n} // namespace\n"
    for header in ("adp_mbx.h", "ctrl_app.h", "mbx_model.h", "mbx_wire.h", "maap_csr.h", "fw_gtest.hpp"):
        text = text.replace(f'#include "{header}"\n', "")
    text = re.sub(r"^FW_TALLY_LABEL.*?\n", "", text, flags=re.M)
    if name == "test_adp_reentry.cpp":
        text = re.sub(r"namespace fw_test \{.*?\n\}\n\}", "", text, flags=re.S)
    text = text.replace("SPDX-License-Identifier: CERN-OHL-W-2.0", "SPDX-License-Identifier: MIT")
    actual = re.sub(r"^// REQ: .*\n", "", (a.repository / "tests" / name).read_text(), flags=re.M)
    declarations = lambda x: set(re.findall(r"TEST(?:_P|_F)?\((\w+),\s*(\w+)\)", x))
    before, after = declarations(text), declarations(actual)
    records.append({"test": name, "source_core_declarations": len(before), "destination_declarations": len(after), "removed": sorted(before-after), "added": sorted(after-before), "equal_after_declared_cleanup_and_annotations": text == actual})
    details.extend(difflib.unified_diff(text.splitlines(True), actual.splitlines(True), fromfile="pinned/"+name, tofile="import/"+name))
a.details.write_text("".join(details))
commits = subprocess.check_output(["git", "rev-list", "HEAD"], cwd=a.repository, text=True).splitlines()
history = []
for commit in commits:
    fields = subprocess.check_output(["git", "show", "-s", "--format=%an <%ae>%n%cn <%ce>%n%B", commit], cwd=a.repository, text=True).strip().splitlines()
    history.append({"commit": commit, "holder_identity": fields[:2] == ["hackerman-kl <hackerman-kl@kebag-logic.com>"]*2, "subject": fields[2], "single_line": len(fields) == 3})
print(json.dumps({"files": records, "history": history}, indent=2))
